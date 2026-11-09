#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""evidence.py — one page per skill: what it read, what it ran, which rules it applied.

    python evidence.py DRAFT.md            # -> evidence-<skill>.md next to the draft
    python evidence.py DRAFT.md -o out.md

The skill is detected from this file's own location, so the same script ships inside every member and each
copy stays standalone. The diagram is Mermaid, rendered by GitHub; nothing leaves the machine.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.basename(os.path.dirname(HERE))          # .../econtone-prosody/scripts -> econtone-prosody
PY = sys.executable

PLAN = {
    "econtone-score": {
        "steps": [("score.py", ["{draft}", "--profile", "{profile}"])],
        "refs": [],
        "rules": ["P1 terminology 40 / P2 claims 40 / T1 traces 10 / R1 rhythm 10",
                  "latitude = cosine quarter-wave above 50, 100% -> 0",
                  "scores only: it never edits"],
    },
    "econtone-polish": {
        "steps": [("mechanical_check.py", ["{draft}"]),
                  ("terminology_check.py", ["{draft}"])],
        "refs": ["references/terminology.md", "references/word_choice.md",
                 "references/econ_writing_rules.md", "references/causal_facts.md",
                 "references/phrase_bank.md", "references/journal_styles.md"],
        "rules": ["Step 0: spelling, US/UK, grammar -- unconditional, outside the game",
                  "Step 3: claim strength must match the design; missing magnitude -> [MAGNITUDE?]",
                  "Step 4: canonical terms only; register neutral band; connectives policed",
                  "sentences are fixed: boundaries belong to econtone-prosody"],
    },
    "econtone-ai-trace": {
        "steps": [("scan_ai_traces.py", ["{draft}"]),
                  ("scan_register.py", ["{draft}"]),
                  ("scan_detectability.py", ["{draft}"])],
        "refs": ["references/anti_ai_trace_audit.md"],
        "rules": ["risk_index is a diagnostic, not a detector prediction",
                  "traces outrank rhythm; never trade a term for a lower proxy",
                  "sentence boundaries are out of scope"],
    },
    "econtone-prosody": {
        "steps": [("prosody_check.py", ["{draft}", "--profile", "{profile}"]),
                  ("rhythm_score.py", ["{draft}", "--profile", "{profile}"])],
        "refs": [],
        "rules": ["nine banded metrics, bands from 42 papers by section (abstract / intro / body)",
                  "five red-line markers are blocking",
                  "stress rows are scored only under the cmudict engine",
                  "boundary moves only: the guard must return LEGAL"],
    },
    "econtone-equilibrium": {
        "steps": [],
        "refs": [],
        "rules": ["lexicographic: validity > traces > rhythm",
                  "boundary moves need a LEGAL guard, no marker, burstiness not RED",
                  "mechanical corrections are applied before round 1",
                  "certificate records every rejected move and the number that refused it"],
    },
}


def run(script, args):
    p = os.path.join(HERE, script)
    if not os.path.exists(p):
        return 127, "missing script"
    r = subprocess.run([PY, p] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "") + (r.stderr or "")
    return r.returncode, out.strip()


def summarise(script, out):
    name = os.path.basename(script)
    if name == "score.py":
        m = re.search(r"TOTAL (\d+)", out)
        t = re.search(r"EDITING LATITUDE (\d+)%", out)
        return "total %s, latitude %s%%" % (m.group(1) if m else "?", t.group(1) if t else "?")
    if name == "rhythm_score.py":
        m = re.search(r"RHYTHM SCORE ([\d.]+)", out) or re.search(r'"score":\s*([\d.]+)', out)
        e = re.search(r"ENGINE: (\w+)", out) or re.search(r'"engine":\s*"(\w+)"', out)
        return "rhythm %s, engine %s" % (m.group(1) if m else "?", e.group(1) if e else "?")
    if name == "prosody_check.py":
        m = re.search(r"VERDICT: (\w+)", out)
        return "verdict %s" % (m.group(1) if m else "?")
    if "detectability" in script:
        m = re.search(r"risk_index ([\d.]+)", out)
        return "risk_index %s" % (m.group(1) if m else "?")
    if "register" in script:
        return "%d register token line(s)" % len(re.findall(r"tokens:", out))
    if "traces" in script:
        m = re.search(r"\(([\d.]+)%\)", out)
        return "transition pegs %s%%" % (m.group(1) if m else "?")
    if "terminology" in script:
        return "no hits" if "no hits" in out else "%d hit line(s)" % len(re.findall(r"^\s+L\d+ ", out, re.M))
    if "mechanical" in script:
        hits = len(re.findall(r"^\s{2}\S+\s+\S+\s+->", out, re.M))
        return "clean" if "clean" in out else "%d finding(s)" % hits
    return "ran"


def build(skill, draft):
    plan = PLAN.get(skill, {"steps": [], "refs": [], "rules": []})
    profile = "abstract" if "abstract" in draft.lower() else "body"
    rows = []
    for script, args in plan["steps"]:
        args = [a.format(draft=draft, profile=profile) for a in args]
        code, out = run(script, args)
        rows.append((script, code, summarise(script, out), out))

    lines = ["# Evidence chain — %s" % skill, "",
             "Draft: `%s`" % os.path.basename(draft), "",
             "```mermaid", "flowchart TD",
             '  A["%s"] --> S["%s"]' % (os.path.basename(draft), skill)]
    for i, (script, code, summary, _) in enumerate(rows):
        lines.append('  S --> R%d["%s<br/>%s"]' % (i, script, summary.replace('"', "'")))
    if plan["refs"]:
        lines.append('  S --> F["references read by the model"]')
        for j, ref in enumerate(plan["refs"]):
            lines.append('  F --> F%d["%s"]' % (j, os.path.basename(ref)))
    lines.append('  S --> U["rules applied"]')
    for k, rule in enumerate(plan["rules"]):
        lines.append('  U --> U%d["%s"]' % (k, rule.replace('"', "'")[:70]))
    lines.append("```")
    lines += ["", "## Scripts", "", "| script | exit | what it reported |", "|---|---|---|"]
    for script, code, summary, _ in rows:
        lines.append("| `%s` | %d | %s |" % (script, code, summary))
    if plan["refs"]:
        lines += ["", "## Reference files the model is instructed to read", "", "| file |", "|---|"]
        for ref in plan["refs"]:
            lines.append("| `%s` |" % ref)
    lines += ["", "## Rules applied", ""]
    for rule in plan["rules"]:
        lines.append("- %s" % rule)
    lines += ["", "> Generated by `evidence.py`. Exit codes are shown so a failed script is visible rather than",
              "> silently omitted. Mermaid is rendered by GitHub; no external service is contacted."]
    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    draft = sys.argv[1]
    out = sys.argv[sys.argv.index("-o") + 1] if "-o" in sys.argv else os.path.join(
        os.path.dirname(os.path.abspath(draft)), "evidence-%s.md" % SKILL)
    open(out, "w", encoding="utf-8", newline="").write(build(SKILL, draft))
    print("evidence -> %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
