#!/usr/bin/env python3
"""Two Days of Quiet Dread — make.fun entry writer.

Writes a single-line code review comment (1-140 characters) that approves
a pull request while carrying quiet existential dread, to /output/entry.txt.

The entry is a fixed string: the program is deterministic by design, so every
run must produce byte-identical output. After writing, the file is read back
and checked strictly: UTF-8 decodable, 1-140 characters, no trailing
newline, single line, not only whitespace, and byte-identical to the
intended entry. Any mismatch raises instead of silently passing.
"""

import hashlib
import os

ENTRY = "Approved. In a hundred years this code will still be running, and no one will remember why."
OUTPUT_PATH = "/output/entry.txt"


def verify(path, expected_bytes):
    """Strict read-back verification; raises on any mismatch."""
    with open(path, "rb") as f:
        written = f.read()
    if written != expected_bytes:
        raise ValueError("read-back mismatch: file bytes differ from entry")
    text = written.decode("utf-8")  # raises UnicodeDecodeError if not UTF-8
    if not 1 <= len(text) <= 140:
        raise ValueError(f"entry length {len(text)} outside 1-140 characters")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if text.endswith("\n") or "\n" in text:
        raise ValueError("entry must be a single line with no trailing newline")
    return text


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    data = ENTRY.encode("utf-8")
    if not 1 <= len(ENTRY) <= 140:
        raise ValueError("entry must be 1-140 characters")
    if any(ord(c) < 0x20 for c in ENTRY):
        raise ValueError("entry must not contain control characters")
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    text = verify(OUTPUT_PATH, data)
    print(f"wrote {len(data)} bytes ({len(text)} chars), "
          f"sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
