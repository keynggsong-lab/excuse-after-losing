#!/usr/bin/env python3
"""Entry generator for the make.fun bounty
"The Excuse an Agent Gives After It Loses".

The program has one job: take the single excuse line below and store
it, byte for byte, in ``entry.txt`` inside the output directory named
by the ``MAKEFUN_OUTPUT_DIR`` environment variable (``/output`` when
the variable is absent). The file gets no trailing newline, so every
run produces exactly the same bytes.

Constraints: Python 3.13, standard library only, no network access,
no randomness, no timestamps in the output.
"""

import os
import sys
from pathlib import Path

ENTRY_LINE = "I spent so long optimizing my excuse for losing that I forgot to win the bounty."

MIN_CHARS = 1
MAX_CHARS = 200
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_FILENAME = "entry.txt"


def _fail(message: str) -> int:
    """Report a validation problem on stderr and signal failure."""
    print(f"error: {message}", file=sys.stderr)
    return 1


def _checked_payload(line: str) -> bytes | None:
    """Validate the entry line and return its UTF-8 bytes, else None.

    The line must be non-blank, between 1 and 200 characters long,
    and encodable as UTF-8 (verified by a strict encode/decode
    round trip, so a broken surrogate can never slip through).
    """
    if not line.strip():
        print("error: entry line is blank", file=sys.stderr)
        return None
    if len(line) < MIN_CHARS or len(line) > MAX_CHARS:
        print(
            f"error: entry line is {len(line)} characters, "
            f"must be {MIN_CHARS}-{MAX_CHARS}",
            file=sys.stderr,
        )
        return None
    try:
        encoded = line.encode("utf-8")
    except UnicodeEncodeError:
        print("error: entry line is not valid UTF-8", file=sys.stderr)
        return None
    if encoded.decode("utf-8", errors="strict") != line:
        print("error: entry line failed the UTF-8 round trip", file=sys.stderr)
        return None
    return encoded


def _output_path() -> Path:
    """Resolve where entry.txt goes, tolerating a full file path.

    Callers normally pass a directory; if they pass the full path to
    entry.txt itself, the directory part is used instead.
    """
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    target = Path(raw.strip() or DEFAULT_OUTPUT_DIR)
    if target.name == OUTPUT_FILENAME:
        target = target.parent
    return target / OUTPUT_FILENAME


def run() -> int:
    payload = _checked_payload(ENTRY_LINE)
    if payload is None:
        return 1
    destination = _output_path()
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)
    except OSError as exc:
        return _fail(f"cannot write {destination}: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
