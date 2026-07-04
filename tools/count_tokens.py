#!/usr/bin/env python3
"""Count tokens for a manifest of files using tiktoken.

Usage:
  python tools/count_tokens.py path/to/manifest.tsv

Manifest format:
  bucket<TAB>path<TAB>label

bucket is typically input or output. Paths may be repo-relative or absolute.
"""

from __future__ import annotations

import argparse
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
        bucket, file_path = parts[0], Path(parts[1])
        label = parts[2] if len(parts) >= 3 else parts[1]
        rows.append((bucket, file_path, label))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--encoding", default="o200k_base")
    args = parser.parse_args()

    repo_root = Path.cwd()
    encoder = tiktoken.get_encoding(args.encoding)
    totals: dict[str, int] = defaultdict(int)

    print("bucket\tlabel\tbytes\ttokens\tpath")
    for bucket, file_path, label in read_manifest(args.manifest):
        resolved = file_path if file_path.is_absolute() else repo_root / file_path
        text = resolved.read_text(encoding="utf-8")
        byte_count = len(text.encode("utf-8"))
        token_count = len(encoder.encode(text))
        totals[bucket] += token_count
        print(f"{bucket}\t{label}\t{byte_count}\t{token_count}\t{file_path}")

    print()
    print("bucket\ttokens")
    for bucket in sorted(totals):
        print(f"{bucket}\t{totals[bucket]}")
    print(f"total\t{sum(totals.values())}")


if __name__ == "__main__":
    main()
