#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rhythm_score.py — turn the prosody report into one best-effort number.

The rhythm gate is an enhancement, not a requirement. It does not have to reach every band; it has
to get as close as it can without touching a word. This script reads the prosody report and returns a
0-100 proximity score, so a revision can be judged as "closer" or "no closer" instead of pass/fail.

    python rhythm_score.py DRAFT.md --profile intro
    python rhythm_score.py DRAFT.md --json
    python rhythm_score.py selftest

Scoring: each banded metric scores 100 inside the band, 50 in WARN, 0 in RED. The mean is the base
score; any red-line marker multiplies it by 0.4 (a marker is a sentence-level defect, not a band miss).
This is a heuristic proximity measure, not a quality grade.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# prefer the installed skill: it is the version carrying --profile and the calibrated bands
CHECKER = os.path.expandvars(
    r"%USERPROFILE%\.dsh\skills\econtone-prosody\scripts\prosody_check.py")
if not os.path.exists(CHECKER):
    CHECKER = os.path.join(HERE, "prosody_check.py")
# prefer the PATH interpreter: it usually carries nltk/cmudict, which the skill's bands assume
import shutil  # noqa: E402
PYTHON = shutil.which("python") or sys.executable

ROW = re.compile(r"^\s{2}([A-Za-z_]+)\s+([\d.]+)\s+(OK|WARN|RED)\b")
POINTS = {"OK": 100.0, "WARN": 50.0, "RED": 0.0}
MARKER = re.compile(r"^    \[(SLURRY|POUNDING|ROBOTIC|DENSE|FLAT)\]", re.M)


def run_checker(path, profile):
    p = subprocess.run([PYTHON, CHECKER, path, "--profile", profile],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.stdout or p.stderr or ""


def score(report):
    rows = []
    for line in report.splitlines():
        m = ROW.match(line)
        if m:
            rows.append({"metric": m.group(1), "value": float(m.group(2)), "band": m.group(3)})
    if not rows:
        return {"score": None, "rows": [], "markers": [], "note": "could not parse the prosody report"}
    base = sum(POINTS[r["band"]] for r in rows) / len(rows)
    markers = MARKER.findall(report)
    factor = 0.4 if markers else 1.0
    return {"score": round(base * factor, 1), "base": round(base, 1), "rows": rows,
            "markers": markers, "note": "proximity score; not a quality grade"}


def selftest():
    fake = """
  nPVI                           39.7  OK     35-41 (red <15)
  alternation_rate               59.5  OK     52-62 (red >78)
  mean_words_per_sentence        18.0  WARN   16-34 (red >45)
"""
    r = score(fake)
    assert r["score"] == round((100 + 100 + 50) / 3, 1), r
    fake2 = fake + "\n    [POUNDING] Sentence 1 has a 7-syllable stressed run\n"
    r2 = score(fake2)
    assert r2["score"] == round(r["base"] * 0.4, 1), r2
    assert score("no metrics here")["score"] is None
    return 3


def main():
    args = sys.argv[1:]
    if args[:1] == ["selftest"]:
        print("selftest: %d assertions passed" % selftest())
        return 0
    if not args:
        print(__doc__)
        return 2
    path = args[0]
    profile = "body"
    if "--profile" in args:
        profile = args[args.index("--profile") + 1]
    report = run_checker(path, profile)
    r = score(report)
    if "--json" in args:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print("RHYTHM SCORE %s / 100  %s" % (r["score"], "(markers: %s)" % ", ".join(r["markers"])
                                             if r["markers"] else ""))
        for row in r["rows"]:
            print("  %-26s %8.1f  %s" % (row["metric"], row["value"], row["band"]))
        print("  %s" % r["note"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
