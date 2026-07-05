#!/usr/bin/env python3
"""Run lightweight evals for Ultra Sprint Harness artifacts."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = REPO_ROOT / "evals" / "cases" / "contact-triage.jsonl"


def count_tokens(text: str) -> tuple[int, str]:
    try:
        import tiktoken

        encoder = tiktoken.get_encoding("o200k_base")
        return len(encoder.encode(text)), "tiktoken o200k_base"
    except Exception:
        return max(1, len(text) // 2), "chars/2 fallback"


def load_cases(path: Path) -> list[dict]:
    cases: list[dict] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            cases.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSONL") from exc
    return cases


def read_project_files(project_dir: Path) -> tuple[str, str]:
    app_js = (project_dir / "app.js").read_text(encoding="utf-8")
    index_html = (project_dir / "index.html").read_text(encoding="utf-8")
    return app_js, index_html


def auto_judge(case: dict) -> dict:
    project_dir = REPO_ROOT / case["input"]["project_dir"]
    app_js, index_html = read_project_files(project_dir)
    check = case["input"]["check"]
    expected = case["expected"]

    if check == "seed_ticket_count":
        count = app_js.count('["2026-07-04')
        passed = count >= expected["min_count"]
        evidence = f"projects/contact-triage-dryrun/app.js has {count} seed ticket rows."
    elif check == "urgency_labels":
        missing = [label for label in expected["labels"] if f'"{label}"' not in app_js and f">{label}<" not in index_html]
        passed = not missing
        evidence = f"app.js/index.html contain urgency labels; missing={missing}."
    elif check == "category_labels":
        missing = [label for label in expected["labels"] if f'"{label}"' not in app_js and f">{label}<" not in index_html]
        passed = not missing
        evidence = f"app.js/index.html contain category labels; missing={missing}."
    elif check == "dashboard_counts":
        missing = [selector for selector in expected["selectors"] if selector not in index_html and selector not in app_js]
        passed = not missing
        evidence = f"index.html/app.js contain dashboard selectors; missing={missing}."
    elif check == "editable_fields":
        missing = [selector for selector in expected["selectors"] if selector not in index_html and selector not in app_js]
        passed = not missing
        evidence = f"index.html/app.js contain edit controls; missing={missing}."
    elif check == "csv_import":
        missing_selectors = [selector for selector in expected["selectors"] if selector not in index_html and selector not in app_js]
        missing_functions = [fn for fn in expected["functions"] if f"function {fn}" not in app_js and f"{fn} =" not in app_js]
        missing_listeners = [listener for listener in expected.get("listeners", []) if listener not in app_js]
        passed = not missing_selectors and not missing_functions and not missing_listeners
        evidence = f"CSV selectors missing={missing_selectors}; functions missing={missing_functions}; listeners missing={missing_listeners}."
    else:
        return {"id": case["id"], "verdict": "cannot_judge", "evidence": f"Unknown auto check: {check}"}

    return {"id": case["id"], "verdict": "pass" if passed else "fail", "evidence": evidence}


def judge_case(case: dict) -> dict:
    judge_type = case.get("judge_type", "auto")
    if judge_type == "auto":
        return auto_judge(case)
    if judge_type == "subagent":
        return {
            "id": case["id"],
            "verdict": "cannot_judge",
            "evidence": "No subagent runner is configured for local evals; use judge-instructions.md with an independent judge.",
        }
    return {"id": case["id"], "verdict": "cannot_judge", "evidence": f"Unknown judge_type: {judge_type}"}


def run_child(case: dict) -> dict:
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
            "verdict": "fail",
            "evidence": completed.stderr.strip() or "Child process failed without stderr.",
            "tokens": 0,
            "token_method": "n/a",
        }
    return json.loads(completed.stdout)


def summarize(results: list[dict]) -> None:
    by_case: dict[str, list[dict]] = defaultdict(list)
    for result in results:
        by_case[result["id"]].append(result)

    executable_tok_per_pass: list[float] = []
    zero_s_cases: list[str] = []
    failure_reasons: Counter[str] = Counter()

    print("case\tS\tavg_tokens\ttok/pass\tfailures")
    for case_id in sorted(by_case):
        case_results = by_case[case_id]
        passes = sum(1 for result in case_results if result["verdict"] == "pass")
        s_value = passes / len(case_results)
        avg_tokens = mean(result.get("tokens", 0) for result in case_results)
        failures = [result["evidence"] for result in case_results if result["verdict"] != "pass"]

        if s_value == 0:
            tok_per_pass = None
            zero_s_cases.append(case_id)
        else:
            tok_per_pass = avg_tokens / s_value
            executable_tok_per_pass.append(tok_per_pass)

        for result in case_results:
            if result["verdict"] != "pass":
                failure_reasons[result["verdict"]] += 1

        tok_text = "n/a" if tok_per_pass is None else f"{tok_per_pass:.1f}"
        print(f"{case_id}\t{s_value:.2f}\t{avg_tokens:.1f}\t{tok_text}\t{len(failures)}")

    total_passes = sum(1 for result in results if result["verdict"] == "pass")
    total_s = total_passes / len(results) if results else 0
    overall_tok_pass = mean(executable_tok_per_pass) if executable_tok_per_pass else 0
    print()
    print(f"overall_S\t{total_s:.2f}")
    print(f"overall_tok/pass\t{overall_tok_pass:.1f}")
    print(f"S=0_cases\t{', '.join(zero_s_cases) if zero_s_cases else 'none'}")
    print("failure_reasons\t" + json.dumps(dict(failure_reasons), ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--runs", type=int, default=4)
    parser.add_argument("--child-case-json")
    args = parser.parse_args()

    if args.child_case_json:
        case = json.loads(args.child_case_json)
        result = judge_case(case)
        input_tokens, token_method = count_tokens(json.dumps(case, ensure_ascii=False))
        output_tokens, _ = count_tokens(json.dumps(result, ensure_ascii=False))
        result["tokens"] = input_tokens + output_tokens
        result["token_method"] = token_method
        print(json.dumps(result, ensure_ascii=False))
        return

    if args.runs <= 0:
        raise ValueError("--runs must be a positive integer")

    cases = load_cases(args.cases)
    results = []
    for case in cases:
        for _ in range(args.runs):
            results.append(run_child(case))
    summarize(results)


if __name__ == "__main__":
    main()
