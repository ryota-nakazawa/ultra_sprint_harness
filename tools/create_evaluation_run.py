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
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    timestamp = datetime.now(timezone.utc).replace(microsecond=0)
    run_id = f"{timestamp.strftime('%Y%m%dT%H%M%SZ')}-iteration-{args.iteration:02d}"
    run_dir = project_dir / "evaluation-runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    receipt = {
        "run_id": run_id,
        "project": project_dir.name,
        "iteration": args.iteration,
        "evaluator_agent_id": args.agent_id,
        "evaluator_nickname": args.agent_nickname or None,
        "spawned_by": "orchestrator",
        "context_isolation": "fresh_context",
        "allowed_inputs": [
            "artifact",
            "run-instructions",
            "project-requirements.md",
            "acceptance-criteria.md",
            "eval-cases.md",
            "eval-profile.md",
            "traceability.md (when present)",
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
    print(run_dir)


if __name__ == "__main__":
    main()
