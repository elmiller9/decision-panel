#!/usr/bin/env python3
"""Tally decision-record outcomes by stated confidence.

Usage:  python calibration.py <decision-folder>

Reads DR-*.md files (YAML front matter written by the panel-review skill) and prints, per
confidence bucket, how many resolved decisions turned out as expected or better, next to the
rate that bucket claims. Standard library only; no YAML dependency (front matter is flat
`key: value`).
"""
import pathlib
import re
import sys

CLAIMS = {"high": "85%+", "moderate": "65-85%", "lean": "50-65%", "low": "<50%"}
ORDER = ["high", "moderate", "lean", "low"]
GOOD = {"as-expected", "better"}


def front_matter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.split("#", 1)[0].strip().lower()
    return fields


def main(folder: str) -> int:
    root = pathlib.Path(folder)
    if not root.is_dir():
        print(f"not a folder: {folder}")
        return 2
    tally = {b: [0, 0] for b in ORDER}  # bucket -> [resolved, good]
    skipped = 0
    for path in sorted(root.glob("DR-*.md")):
        fm = front_matter(path.read_text(encoding="utf-8"))
        bucket, outcome = fm.get("confidence"), fm.get("outcome")
        if bucket not in tally or not outcome or outcome == "pending":
            skipped += 1
            continue
        tally[bucket][0] += 1
        tally[bucket][1] += outcome in GOOD

    resolved = sum(t[0] for t in tally.values())
    print(f"Resolved decisions: {resolved} (pending or unreadable: {skipped})\n")
    print(f"{'Bucket':<10}{'Resolved':>9}{'Good':>6}{'Actual':>9}   Claimed")
    for b in ORDER:
        n, good = tally[b]
        actual = f"{good / n:.0%}" if n else "-"
        note = "  (too few to judge)" if 0 < n < 5 else ""
        print(f"{b:<10}{n:>9}{good:>6}{actual:>9}   {CLAIMS[b]}{note}")
    if resolved < 10:
        print("\nFewer than 10 resolved decisions: treat these numbers as anecdotes, not calibration.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
