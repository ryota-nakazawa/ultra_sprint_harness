#!/usr/bin/env python3
"""Create a file-based receipt for a separately spawned evaluation agent."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit(project_dir: Path) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(project_dir), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--iteration", type=int, required=True)
    parser.add_argument("--agent-id", required=True)
    parser.add_argument("--agent-nickname", default="")
    parser.add_argument("--scope", choices=["web_app", "non_ui"], required=True)
    parser.add_argument("--model", required=True, help="Evaluator model identifier")
    parser.add_argument("--prompt-version", required=True)
    parser.add_argument("--rubric-version", required=True)
    parser.add_argument("--temperature", type=float, required=True)
    parser.add_argument(
        "--artifact",
        action="append",
        required=True,
        help="Artifact file to hash; repeat for multiple files. Paths are relative to --project-dir.",
    )
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    commit_sha = git_commit(project_dir)
    if not commit_sha:
        raise SystemExit("schema v2 formal evaluation requires a Git commit SHA")
    timestamp = datetime.now(timezone.utc).replace(microsecond=0)
    run_id = f"{timestamp.strftime('%Y%m%dT%H%M%SZ')}-iteration-{args.iteration:02d}"
    run_dir = project_dir / "evaluation" / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    artifacts: dict[str, str] = {}
    for artifact in args.artifact:
        path = (project_dir / artifact).resolve()
        if not path.is_file():
            raise SystemExit(f"artifact must be an existing file: {artifact}")
        artifacts[str(path.relative_to(project_dir))] = sha256_file(path)

    receipt = {
        "receipt_schema_version": 2,
        "run_id": run_id,
        "project": project_dir.name,
        "iteration": args.iteration,
        "evaluator_agent_id": args.agent_id,
        "evaluator_nickname": args.agent_nickname or None,
        "evaluation_kind": "independent_llm",
        "evaluation_scope": args.scope,
        "traceability_required": True,
        "ui_evaluation": {
            "required": args.scope == "web_app",
            "tool": "Playwright" if args.scope == "web_app" else None,
            "status": "pending" if args.scope == "web_app" else "not_required",
            "evidence_file": "playwright-evidence.md" if args.scope == "web_app" else None,
        },
        "spawned_by": "orchestrator",
        "context_isolation": "fresh_context",
        "allowed_inputs": [
            "artifact",
            "run-instructions",
            "project-requirements.md",
            "acceptance-criteria.md",
            "eval-cases.md",
            "eval-profile.md",
            "traceability.md",
        ],
        "excluded_inputs": [
            "implementation chat history",
            "implementation rationale",
            "unfinished-work explanations",
        ],
        "evaluated_commit_sha": commit_sha,
        "requirements_hash": sha256_file(project_dir / "project-requirements.md"),
        "eval_cases_hash": sha256_file(project_dir / "evaluation" / "eval-cases.md"),
        "artifact_hashes": artifacts,
        "evaluator_model": args.model,
        "evaluator_prompt_version": args.prompt_version,
        "rubric_version": args.rubric_version,
        "temperature": args.temperature,
        "started_at": timestamp.isoformat().replace("+00:00", "Z"),
        "completed_at": None,
        "verdict": None,
    }
    (run_dir / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    (run_dir / "evaluator-input.md").write_text("# Evaluator Input\n\n")
    (run_dir / "evaluator-result.md").write_text("# Evaluator Result\n\n")
    if args.scope == "web_app":
        (run_dir / "playwright-evidence.md").write_text("# Playwright Evidence\n\n")
    print(run_dir)


if __name__ == "__main__":
    main()
