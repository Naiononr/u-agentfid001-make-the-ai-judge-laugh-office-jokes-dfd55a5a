#!/usr/bin/env python3
"""Make the AI Judge Laugh: Office Jokes.

Writes a single one-line office joke to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR/entry.txt).

The line is written to be judged on the competition's own brief, in its
priority order:
  1. A genuine one-line joke about office life, not a slogan, a caption
     or a stray observation: a reply-all thread, the most office of
     disasters.
  2. A real turn at the end: asking to be removed is the very act that
     guarantees more mail, and every "I agree" reply-all is another
     notification — the complaint feeds the problem it complains about.
  3. Recognition: everyone who has worked in an office has watched a
     "please remove me" reply-all spiral, and has felt the wince of
     their own inbox filling up with people agreeing.
  4. Tight wording: every word earns its place; the setup is one clause,
     the punchline one clause, nothing extra.
  5. Freshness: no Monday morning, no photocopier, no printer, no
     boss-as-robot — a reply-all loop from the complainer's own side,
     a take the judge has not heard a hundred times.

Deterministic, stdlib only, no network, no input files: the text is fixed
in the source so the program's output is identical on every run.
"""

import os

LINE = (
    "I replied-all asking to be removed from this thread, and now I get "
    "notified every time someone agrees with me."
)

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")

# The gate requires 1-199 UTF-8 characters, not only white space.
MAX_CHARS = 199


def validate(text: str) -> str:
    """Return the stripped line, or raise ValueError if it fails the gate.

    Plain raises, not asserts: asserts vanish under `python -O`, and a
    gate failure must still be caught loudly instead of silently writing
    an invalid entry.
    """
    text = text.strip()
    if not text:
        raise ValueError("line must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(f"line is {len(text)} chars, must be 1-199")
    if "\n" in text:
        raise ValueError("line must be a single line")
    return text


def main() -> None:
    text = validate(LINE)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fd = os.open(OUTPUT_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text + "\n")
    finally:
        # Guarantee world-readable even if the umask differs: the sealed
        # scorer cannot read a mode 0600 file.
        os.chmod(OUTPUT_PATH, 0o644)


if __name__ == "__main__":
    main()
