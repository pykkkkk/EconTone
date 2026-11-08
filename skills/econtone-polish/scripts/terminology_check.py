#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""terminology_check.py — glossary and consistency checker for EconTone drafts.

Companion to the econtone-polish skill, Step 4 (diction). Reads the glossary in
references/terminology.md and reports three things:

  1. BANNED   — an "Avoid" variant from the glossary appears in the draft
  2. ACRONYM  — an acronym is used without a first-mention expansion
  3. MIXED    — Chinese characters left inside an English draft (or vice versa)

Reporting only: it never rewrites. A hit is a candidate, not a verdict.

Usage
-----
    python terminology_check.py DRAFT.md
    python terminology_check.py DRAFT.md --json
    python terminology_check.py DRAFT.md --glossary references/terminology.md
    python terminology_check.py selftest

Standard library only; read-only; no network.
"""

# --- Force UTF-8 on stdout/stderr -------------------------------------------
import sys as _sys

for _stream in (_sys.stdout, _sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")
del _sys, _stream

import argparse
import json
import os
import sys
import re

# English variants that are wrong regardless of the glossary column, which is
# mostly Chinese. Curated from SKILL.md Step 4 and the anti-pattern table.
EXTRA_BANNED = [
    "parallel trend hypothesis",
    "instrumental variable method",
    "difference-in-difference",
    "diff-in-diff",
    "endogeneity problem",
    "the problem of",
    "it is worth noting that",
    "in order to",
    "utilize", "utilise", "utilizing", "utilising",
]

CJK = re.compile(r"[\u4e00-\u9fff]")
ASCII_WORD = re.compile(r"[A-Za-z]")


def parse_glossary(path):
    """Return (banned_terms, canonical_rows) parsed from a pipe table."""
    banned, rows = [], []
    if not os.path.exists(path):
        return banned, rows
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line.startswith("|") or set(line) <= set("|-: "):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 3:
                continue
            canonical, _chinese, avoid = cells[0], cells[1], cells[2]
            if canonical.lower().startswith("english"):
                continue  # header row
            rows.append(canonical)
            for item in re.split(r"[、,，;；/]", avoid):
                item = re.sub(r"[（(].*?[）)]", "", item).strip()
                if item and ASCII_WORD.search(item) and item != "—":
                    banned.append(item)
    return banned, rows


def check(text, banned, rows, lang="en"):
    lines = text.splitlines()
    hits = []

    for term in banned:
        pat = re.compile(r"(?<![A-Za-z])" + re.escape(term) + r"(?![A-Za-z])", re.I)
        for i, line in enumerate(lines, 1):
            if pat.search(line):
                hits.append({"kind": "BANNED", "term": term, "line": i,
                             "text": line.strip()[:160],
                             "why": "glossary lists this as a variant to avoid"})

    acr = {}
    for row in rows:
        m = re.match(r"^(.*?)\s*\(([A-Z]{2,6})\)\s*$", row)
        if m:
            acr[m.group(2)] = m.group(1).strip()
    body = "\n".join(lines)
    for short, full in acr.items():
        used_short = re.search(r"\b" + re.escape(short) + r"\b", body)
        used_full = re.search(re.escape(full), body, re.I)
        if used_short and not used_full:
            hits.append({"kind": "ACRONYM", "term": short, "line": 0,
                         "text": full, "why": "acronym used but the full form never appears"})

    script = CJK if lang == "en" else ASCII_WORD
    for i, line in enumerate(lines, 1):
        if line.strip() and script.search(line):
            hits.append({"kind": "MIXED", "term": "", "line": i,
                         "text": line.strip()[:160],
                         "why": "wrong script for this draft language"})

    return hits


def selftest():
    checks = []
    banned = ["parallel trend hypothesis", "instrumental variable method"]
    rows = ["parallel trends assumption", "local average treatment effect (LATE)"]
    text = ("We rely on the parallel trend hypothesis. "
            "The estimate uses an instrumental variable method.\n"
            "The LATE is reported below.\n")
    hits = check(text, banned, rows, "en")
    kinds = {(h["kind"], h["term"]) for h in hits}
    checks.append(("banned variant detected", ("BANNED", "parallel trend hypothesis") in kinds))
    checks.append(("second banned variant detected", ("BANNED", "instrumental variable method") in kinds))
    checks.append(("acronym without expansion", ("ACRONYM", "LATE") in kinds))
    zh = check("This is fine. 但这一行有中文。", banned, rows, "en")
    checks.append(("mixed script detected", any(h["kind"] == "MIXED" for h in zh)))
    clean = check("We rely on the parallel trends assumption.\n", banned, rows, "en")
    checks.append(("clean text has no hits", not clean))
    failed = [n for n, c in checks if not c]
    for n, c in checks:
        print(("  PASS " if c else "  FAIL ") + n)
    print("\nselftest: %d/%d passed" % (len(checks) - len(failed), len(checks)))
    return not failed


def main():
    ap = argparse.ArgumentParser(description="Glossary and consistency checker.")
    ap.add_argument("file", nargs="?")
    ap.add_argument("--glossary", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "references", "terminology.md"))
    ap.add_argument("--lang", choices=["en", "zh"], default="en")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("cmd", nargs="?")
    args = ap.parse_args()

    if args.cmd == "selftest" or args.file == "selftest":
        return 0 if selftest() else 1

    if not args.file:
        ap.print_help()
        return 2
    try:
        with open(args.file, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError as e:
        print("cannot read %s: %s" % (args.file, e))
        return 2

    banned, rows = parse_glossary(args.glossary)
    banned += EXTRA_BANNED
    hits = check(text, banned, rows, args.lang)

    if args.json:
        print(json.dumps({"file": args.file, "glossary_terms": len(rows),
                          "banned_terms": len(banned), "hits": hits},
                         ensure_ascii=False, indent=2))
        return 0

    print("TERMINOLOGY CHECK — %s" % args.file)
    print("  glossary: %d terms, %d banned variants" % (len(rows), len(banned)))
    if not hits:
        print("  no hits")
        return 0
    for kind in ("BANNED", "ACRONYM", "MIXED"):
        group = [h for h in hits if h["kind"] == kind]
        if not group:
            continue
        print("\n  %s (%d)" % (kind, len(group)))
        for h in group[:20]:
            where = "L%d " % h["line"] if h["line"] else ""
            label = h["term"] or h["text"]
            print("    %s%s — %s" % (where, label, h["why"]))
            if h["line"]:
                print("           | %s" % h["text"])
    print("\n  hits are candidates, not verdicts: read the line before changing it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
