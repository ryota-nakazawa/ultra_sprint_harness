#!/usr/bin/env python3
"""Run static and runtime evals for Ultra Sprint Harness artifacts."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = REPO_ROOT / "evals" / "cases" / "contact-triage.jsonl"


def count_tokens(text: str) -> int:
    try:
        import tiktoken

        encoder = tiktoken.get_encoding("o200k_base")
        return len(encoder.encode(text))
    except Exception:
        return max(1, len(text) // 2)


def load_cases(path: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            case = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSONL") from exc
        if "target" not in case:
            raise ValueError(f"{path}:{line_number}: missing target")
        cases.append(case)
    return cases


def read_project_files(project_dir: Path) -> tuple[str, str, str]:
    app_js = (project_dir / "app.js").read_text(encoding="utf-8")
    index_html = (project_dir / "index.html").read_text(encoding="utf-8")
    triage_rules = (project_dir / "triageRules.js").read_text(encoding="utf-8")
    return app_js, index_html, triage_rules


def count_seed_rows(app_js: str) -> int:
    match = re.search(r"const\s+seedTickets\s*=\s*\[(.*?)\];", app_js, flags=re.S)
    if not match:
        return 0
    return len(re.findall(r"^\s*\[", match.group(1), flags=re.M))


def judge_static(case: dict[str, Any]) -> dict[str, Any]:
    project_dir = REPO_ROOT / case["input"]["project_dir"]
    app_js, index_html, triage_rules = read_project_files(project_dir)
    combined = "\n".join([app_js, index_html, triage_rules])
    check = case["input"]["check"]
    expected = case["expected"]

    if check == "seed_ticket_count":
        count = count_seed_rows(app_js)
        passed = count >= expected["min_count"]
        evidence = f"app.js seedTickets has {count} rows."
    elif check == "urgency_labels":
        missing = [label for label in expected["labels"] if f'"{label}"' not in combined and f">{label}<" not in index_html]
        passed = not missing
        evidence = f"project files contain urgency labels; missing={missing}."
    elif check == "category_labels":
        missing = [label for label in expected["labels"] if f'"{label}"' not in combined and f">{label}<" not in index_html]
        passed = not missing
        evidence = f"project files contain category labels; missing={missing}."
    elif check == "dashboard_counts":
        missing = [selector for selector in expected["selectors"] if selector not in combined]
        passed = not missing
        evidence = f"project files contain dashboard selectors; missing={missing}."
    elif check == "editable_fields":
        missing = [selector for selector in expected["selectors"] if selector not in combined]
        passed = not missing
        evidence = f"project files contain edit controls; missing={missing}."
    elif check == "csv_import":
        missing_selectors = [selector for selector in expected["selectors"] if selector not in combined]
        missing_functions = [fn for fn in expected["functions"] if f"function {fn}" not in combined and f"{fn} =" not in combined]
        missing_listeners = [listener for listener in expected.get("listeners", []) if listener not in combined]
        passed = not missing_selectors and not missing_functions and not missing_listeners
        evidence = f"CSV selectors missing={missing_selectors}; functions missing={missing_functions}; listeners missing={missing_listeners}."
    else:
        return {"id": case["id"], "target": "static", "verdict": "cannot_judge", "evidence": f"Unknown static check: {check}"}

    return {"id": case["id"], "target": "static", "verdict": "pass" if passed else "fail", "evidence": evidence}


def run_runtime_adapter(case: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
    completed = subprocess.run(
        case["runner"],
        cwd=REPO_ROOT,
        input=json.dumps(case["input"], ensure_ascii=False),
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return {}, completed.stderr.strip() or "Runtime adapter failed without stderr."
    try:
        return json.loads(completed.stdout), None
    except json.JSONDecodeError as exc:
        return {}, f"Runtime adapter returned invalid JSON: {exc}"


def judge_runtime(case: dict[str, Any]) -> dict[str, Any]:
    output, error = run_runtime_adapter(case)
    if error:
        return {"id": case["id"], "target": "runtime", "verdict": "fail", "evidence": error, "tokens": None}

    judge_type = case.get("judge_type", "auto")
    if judge_type != "auto":
        return {
            "id": case["id"],
            "target": "runtime",
            "verdict": "cannot_judge",
            "evidence": "No subagent runner is configured for local evals; use judge-instructions.md with an independent judge.",
            "tokens": None,
        }

    expected = case["expected"]
    mismatches = {key: {"expected": value, "actual": output.get(key)} for key, value in expected.items() if output.get(key) != value}
    passed = not mismatches
    tokens = None
    token_note = "n/a: runner does not call an LLM"
    if case.get("token_source") == "llm_io":
        tokens = count_tokens(json.dumps(case["input"], ensure_ascii=False)) + count_tokens(json.dumps(output, ensure_ascii=False))
        token_note = "tiktoken o200k_base over runtime input+output"

    return {
        "id": case["id"],
        "target": "runtime",
        "verdict": "pass" if passed else "fail",
        "evidence": f"output={output}; mismatches={mismatches}",
        "tokens": tokens,
        "token_note": token_note,
    }


def judge_case(case: dict[str, Any]) -> dict[str, Any]:
    target = case.get("target")
    if target == "static":
        return judge_static(case)
    if target == "runtime":
        return judge_runtime(case)
    return {"id": case["id"], "target": target, "verdict": "cannot_judge", "evidence": f"Unknown target: {target}"}


def run_child(case: dict[str, Any]) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, __file__, "--child-case-json", json.dumps(case, ensure_ascii=False)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return {
            "id": case["id"],
            "target": case.get("target", "unknown"),
            "verdict": "fail",
            "evidence": completed.stderr.strip() or "Child process failed without stderr.",
            "tokens": None,
        }
    return json.loads(completed.stdout)


def summarize_static(results: list[dict[str, Any]]) -> None:
    if not results:
        return
    print("## static")
    print("case\tverdict\tevidence")
    for result in sorted(results, key=lambda item: item["id"]):
        print(f"{result['id']}\t{result['verdict']}\t{result['evidence']}")
    counts = Counter(result["verdict"] for result in results)
    print("summary\t" + json.dumps(dict(counts), ensure_ascii=False))
    print()


def summarize_runtime(results: list[dict[str, Any]]) -> None:
    if not results:
        return

    by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for result in results:
        by_case[result["id"]].append(result)

    zero_s_cases: list[str] = []
    executable_tok_per_pass: list[float] = []
    failure_reasons: Counter[str] = Counter()

    print("## runtime")
    print("case\tS\tavg_call_tokens\ttok/pass\tfailures\ttoken_note")
    for case_id in sorted(by_case):
        case_results = by_case[case_id]
        passes = sum(1 for result in case_results if result["verdict"] == "pass")
        s_value = passes / len(case_results)
        token_values = [result["tokens"] for result in case_results if isinstance(result.get("tokens"), int)]
        avg_tokens = mean(token_values) if token_values else None
        failures = [result for result in case_results if result["verdict"] != "pass"]
        token_note = next((result.get("token_note") for result in case_results if result.get("token_note")), "n/a")

        if s_value == 0:
            zero_s_cases.append(case_id)
            tok_per_pass = None
        elif avg_tokens is None:
            tok_per_pass = None
        else:
            tok_per_pass = avg_tokens / s_value
            executable_tok_per_pass.append(tok_per_pass)

        for result in failures:
            failure_reasons[result["verdict"]] += 1

        avg_text = "n/a" if avg_tokens is None else f"{avg_tokens:.1f}"
        tok_text = "n/a" if tok_per_pass is None else f"{tok_per_pass:.1f}"
        print(f"{case_id}\t{s_value:.2f}\t{avg_text}\t{tok_text}\t{len(failures)}\t{token_note}")

    total_passes = sum(1 for result in results if result["verdict"] == "pass")
    total_s = total_passes / len(results) if results else 0
    overall_tok_pass = mean(executable_tok_per_pass) if executable_tok_per_pass else None
    print()
    print(f"overall_runtime_S\t{total_s:.2f}")
    print(f"overall_runtime_tok/pass\t{'n/a' if overall_tok_pass is None else f'{overall_tok_pass:.1f}'}")
    print(f"S=0_cases\t{', '.join(zero_s_cases) if zero_s_cases else 'none'}")
    print("failure_reasons\t" + json.dumps(dict(failure_reasons), ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--runs", type=int, default=4)
    parser.add_argument("--child-case-json")
    args = parser.parse_args()

    if args.child_case_json:
        print(json.dumps(judge_case(json.loads(args.child_case_json)), ensure_ascii=False))
        return

    if args.runs <= 0:
        raise ValueError("--runs must be a positive integer")

    cases = load_cases(args.cases)
    static_results: list[dict[str, Any]] = []
    runtime_results: list[dict[str, Any]] = []
    for case in cases:
        if case["target"] == "static":
            static_results.append(run_child(case))
        elif case["target"] == "runtime":
            for _ in range(args.runs):
                runtime_results.append(run_child(case))
        else:
            static_results.append({"id": case["id"], "target": case["target"], "verdict": "cannot_judge", "evidence": "Unknown target"})

    summarize_static(static_results)
    summarize_runtime(runtime_results)


if __name__ == "__main__":
    main()
