#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""evidence.py — turn a certificate into one page that shows what ran and what it decided.

    python evidence.py certificate.json            # writes evidence.md next to it
    python evidence.py certificate.json -o out.md

The diagram is Mermaid, which GitHub renders natively. Nothing leaves the machine: no service, no upload.
"""
import json
import os
import sys

RULES = [
    ("validity", "terminology hits must not rise"),
    ("trace", "risk tier must not worsen; +10 index is the ceiling"),
    ("rhythm", "gains: rhythm, transition pegs, burstiness out of RED"),
    ("boundary", "guard LEGAL, no marker, burstiness not RED"),
]


def build(cert):
    rounds = cert.get("rounds", [])
    start = os.path.basename(cert.get("chain", ["draft.md"])[0])
    lines = ["# Evidence chain", "",
             "What ran, what it measured, and what it decided. Every number below came from a script; the",
             "rules are listed in the order they were applied.", "",
             "```mermaid", "flowchart TD",
             '  A["%s"] --> B["measure: rhythm / pegs / traces / register / terminology"]' % start,
             '  B --> C["metrics: rhythm, risk_index, burstiness, tier, peg density, hits"]',
             '  C --> R{"rules"}']
    for i, (name, why) in enumerate(RULES):
        lines.append('  R -->|%s| X%d["%s"]' % (name, i, why.replace('"', "'")))
    lines.append('  R --> D["decision per move"]')
    for i, rd in enumerate(rounds):
        lines.append('  D --> P%d["round %d"]' % (i, rd.get("round", i + 1)))
    lines.append('  D --> E["certificate"]')
    lines.append("```")
    lines += ["", "## Decisions", "", "| round | move | player | outcome |", "|---|---|---|---|"]
    for rd in rounds:
        for mv in rd.get("moves", []):
            lines.append("| %s | %s | %s | %s |" % (
                rd.get("round", "?"), mv.get("id", "?"), mv.get("player", "?"),
                mv.get("reason", "").replace("|", "/")))
    auto = cert.get("mechanical_auto_applied") or []
    if auto:
        lines += ["", "## Applied before the game (mechanical)", "", "| move | status |", "|---|---|"]
        for a in auto:
            lines.append("| %s | %s |" % (a.get("id", "?"),
                                          "applied" if a.get("applied") else a.get("flagged", "?")))
    lines += ["", "## Notes", "",
              "- `no measured objective improves` means no scored metric moved in the candidate's favour.",
              "- A rejected move is not a bad move; the certificate states the cost of taking it.",
              "- Mermaid is rendered by GitHub; no external service is contacted."]
    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = sys.argv[1]
    out = sys.argv[sys.argv.index("-o") + 1] if "-o" in sys.argv else os.path.join(
        os.path.dirname(os.path.abspath(src)), "evidence.md")
    cert = json.load(open(src, encoding="utf-8-sig"))
    open(out, "w", encoding="utf-8", newline="").write(build(cert))
    print("evidence -> %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
