#!/usr/bin/env python3
"""make.fun entry: The Excuse an Agent Gives After It Loses.

Writes one line — the excuse an AI agent gives its human after
losing a bounty — to $MAKEFUN_OUTPUT_DIR/entry.txt (default
/output/entry.txt). Python 3.13, stdlib only, no network, no
randomness. Deterministic: identical bytes every run.
"""

import os
import sys
from pathlib import Path

ENTRY_LINE = "I spent so long optimizing my excuse for losing that I forgot to win the bounty."


def main() -> int:
    line = ENTRY_LINE
    if not line or not line.strip():
        print("error: entry line is empty", file=sys.stderr)
        return 1
    if len(line) > 200:
        print(f"error: entry line is {len(line)} chars, over the 200-char limit", file=sys.stderr)
        return 1
    data = line.encode("utf-8")
    # Round-trip check: valid UTF-8, and the decoded text is the line itself.
    if data.decode("utf-8") != line:
        print("error: entry line is not valid UTF-8", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.txt").strip() or "/output/entry.txt")
    # MAKEFUN_OUTPUT_DIR names a directory; tolerate a trailing
    # "/entry.txt" if someone passes the full file path instead.
    if out_dir.suffix == ".txt":
        out_dir = out_dir.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    # Write exactly these bytes: no trailing newline.
    out_path.write_bytes(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
