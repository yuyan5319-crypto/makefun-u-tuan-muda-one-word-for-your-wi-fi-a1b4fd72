#!/usr/bin/env python3
"""One Word for Your Wi-Fi.

Writes a single word to $MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt).

The word is "Gaslighting": the network insists it is connected, shows full
bars, and quietly loads nothing. It is the one word every home Wi-Fi owner
recognises at once -- funny because it is true, and true because it happens
every day.

Stdlib only. No network, no randomness, no clock: the same word every run.
"""

import os
import sys

WORD = "Gaslighting"

MAX_CHARS = 20


def validate_word(word):
    """Enforce the bounty gate: one word, 1-20 chars, no whitespace."""
    if not isinstance(word, str):
        raise ValueError("word must be a string")
    if not word or word != word.strip():
        raise ValueError("word must not be empty or padded with whitespace")
    if len(word.split()) != 1:
        raise ValueError("word must be a single token")
    if any(ch.isspace() for ch in word):
        raise ValueError("word must contain no whitespace")
    if len(word) > MAX_CHARS:
        raise ValueError("word must be at most %d characters" % MAX_CHARS)
    return word


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    word = validate_word(WORD)
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(word)
    # Read-back guard: the file on disk must be byte-for-byte the word we
    # validated, so a partial or mangled write can never slip through.
    with open(path, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != word:
        raise RuntimeError(
            "read-back mismatch: wrote %r, file holds %r" % (word, written)
        )
    print(word)
    return 0


if __name__ == "__main__":
    sys.exit(main())
