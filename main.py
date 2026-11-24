#!/usr/bin/env python3
"""Write one line of the worst AI advice to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The line is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 140 characters, not only white space. The entry
is written by write_entry(), which creates the output directory first;
a failure to write is reported as one clean line on stderr with a
non-zero exit instead of a traceback.
"""

import os
import sys
from pathlib import Path

ENTRY = "Certainly! If your smoke alarm keeps beeping, remove the battery. No beep, no fire."

MIN_CHARS = 1
MAX_CHARS = 140
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 140 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    A blank-only entry fails on the white-space rule, not the length
    rule, so the message always says what is actually wrong.
    """
    if not text.strip():
        raise ValueError("entry is only white space")
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"entry is {chars} characters, outside 1-140")
    return chars


def write_entry(path: Path, text: str) -> None:
    """Create the output directory and write the entry text to path.

    Raises OSError to the caller, which reports it cleanly instead of
    letting a traceback escape.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    try:
        chars = validate(ENTRY)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    try:
        write_entry(path, ENTRY)
    except OSError as exc:
        print(f"could not write {path}: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
