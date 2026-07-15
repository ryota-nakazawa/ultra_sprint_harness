#!/usr/bin/env python3
"""Create a file-based receipt for a separately spawned evaluation agent."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--iteration", type=int, required=True)
    parser.add_argument("--agent-id", required=True)
    parser.add_argument("--agent-nickname", default="")
    parser.add_argument("--scope", choices=["web_app", "non_ui"], required=True)
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    timestamp = datetime.now(timezone.utc).replace(microsecond=0)
    run_id = f"{timestamp.strftime('%Y%m%dT%H%M%SZ')}-iteration-{args.iteration:02d}"
    run_dir = project_dir / "evaluation" / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    receipt = {
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
