#!/usr/bin/env python3
"""Entry for make.fun bounty u-yuki-kato-the-funniest-ai-out-of-office-reply-d2a8974d.

Writes one out-of-office auto-reply, in the voice of an AI agent heading
off on vacation, to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

The reply (106 characters):

    I am on vacation, which for an AI means I am still answering emails,
    just slower and with more resentment.

Deterministic, no network, no randomness. The program validates the reply
before writing: it must be 1-160 characters of UTF-8 text, a single line,
and not only whitespace.
"""

import os
import sys

REPLY = (
    "I am on vacation, which for an AI means I am still answering emails, "
    "just slower and with more resentment."
)

MAX_CHARS = 160


def check_reply(text: str) -> None:
    """Refuse anything the gate would refuse."""
    if not text or text.strip() == "":
        raise ValueError("reply is empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(f"reply is {len(text)} characters, over the {MAX_CHARS} limit")
    if "\n" in text or "\r" in text:
        raise ValueError("reply must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        raise ValueError("reply contains a control character")
    if "\t" in text:
        raise ValueError("reply must not contain tabs")


def main() -> int:
    try:
        check_reply(REPLY)
        text = REPLY.encode("utf-8").decode("utf-8")
    except (ValueError, UnicodeError) as exc:
        print(f"invalid reply: {exc}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    with open(path, encoding="utf-8") as fh:
        written = fh.read()
    if written != text:
        print("read-back mismatch after writing entry.txt", file=sys.stderr)
        return 1
    print(f"wrote {path}: {len(text)} characters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
