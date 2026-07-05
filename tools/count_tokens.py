#!/usr/bin/env python3
"""Count tokens for a manifest of files using tiktoken.

Usage:
  python tools/count_tokens.py path/to/manifest.tsv
  python tools/count_tokens.py path/to/manifest.tsv --passes 1 --report metrics/example-token-usage.md

Manifest format:
  bucket<TAB>path<TAB>label

bucket is typically input or output. Paths may be repo-relative or absolute.
"""

from __future__ import annotations

import argparse
import os
from collections import defaultdict
from pathlib import Path

import tiktoken


def read_manifest(path: Path) -> list[tuple[str, Path, str]]:
    rows: list[tuple[str, Path, str]] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            raise ValueError(f"{path}:{line_number}: expected bucket<TAB>path<TAB>label")
        bucket, file_path = parts[0], Path(os.path.expandvars(parts[1])).expanduser()
        label = parts[2] if len(parts) >= 3 else parts[1]
        rows.append((bucket, file_path, label))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--encoding", default="o200k_base")
    parser.add_argument("--passes", type=int, default=1, help="Number of successful PoC passes for CoP-token.")
    parser.add_argument("--report", type=Path, help="Write a Markdown token usage report.")
    args = parser.parse_args()
    if args.passes <= 0:
        raise ValueError("--passes must be a positive integer")

    repo_root = Path.cwd()
    encoder = tiktoken.get_encoding(args.encoding)
    totals: dict[str, int] = defaultdict(int)
    rows: list[tuple[str, str, int, int, Path]] = []

    print("bucket\tlabel\tbytes\ttokens\tpath")
    for bucket, file_path, label in read_manifest(args.manifest):
        resolved = file_path if file_path.is_absolute() else repo_root / file_path
        text = resolved.read_text(encoding="utf-8")
        byte_count = len(text.encode("utf-8"))
        token_count = len(encoder.encode(text))
        totals[bucket] += token_count
        rows.append((bucket, label, byte_count, token_count, file_path))
        print(f"{bucket}\t{label}\t{byte_count}\t{token_count}\t{file_path}")

    print()
    print("bucket\ttokens")
    for bucket in sorted(totals):
        print(f"{bucket}\t{totals[bucket]}")
    total = sum(totals.values())
    print(f"total\t{total}")
    print(f"cop_token\t{total / args.passes:.2f}")

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        project_name = args.manifest.stem.removesuffix("-token-manifest")
        file_rows = "\n".join(
            f"| {bucket} | {label} | {token_count:,} |"
            for bucket, label, _byte_count, token_count, _file_path in rows
        )
        bucket_rows = "\n".join(f"| {bucket} | {tokens:,} |" for bucket, tokens in sorted(totals.items()))
        report = "\n".join(
            [
                f"# {project_name} token usage",
                "",
                "## Method",
                "",
                "- Tool: `tiktoken`",
                f"- Encoding: `{args.encoding}`",
                f"- Manifest: `{args.manifest}`",
                "- Scope: files listed in the manifest as inputs and generated outputs.",
                "- Caveat: this is a lower-bound estimate from visible text. It excludes Codex system/developer instructions, tool schemas, hidden reasoning, cache effects, and transient tool output that was not saved to files.",
                "- Calibration multiplier `k = measured tokens / estimated tokens`: TBD.",
                "- Calibration procedure: in the next real project, compare this estimate with measured usage from Codex session logs under `~/.codex/sessions/` and record `k` here.",
                "",
                "## Result",
                "",
                "| Bucket | Tokens |",
                "|---|---:|",
                bucket_rows,
                f"| total | {total:,} |",
                "",
                "## File Breakdown",
                "",
                "| Bucket | File | Tokens |",
                "|---|---|---:|",
                file_rows,
                "",
                "## CoP-token",
                "",
                "```text",
                f"estimated CoP-token = {total:,} tokens / {args.passes} pass",
                f"                    = {total / args.passes:,.0f} tokens per pass",
                "```",
                "",
            ]
        )
        args.report.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
