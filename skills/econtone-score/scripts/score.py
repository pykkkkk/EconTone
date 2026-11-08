#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""score.py — EconTone orientation scorecard.

Four rows weighted 40 / 40 / 10 / 10, one total, and an EDITING LATITUDE derived from the total.
It does not route: the pack always runs score -> polish -> prosody -> ai-trace.
It does not edit and does not suggest replacement text.

    python score.py DRAFT.md
    python score.py DRAFT.md --profile abstract --json

Latitude curve: full latitude up to 50, then the right half of a semicircle down to 0 at 100.
    50 -> 100%   60 -> 95%   75 -> 71%   85 -> 45%   90 -> 31%   95 -> 16%   100 -> 0%
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS_ROOT = os.path.dirname(os.path.dirname(HERE))

CAUSAL = re.compile(r"\b(increases?|reduces?|causes?|leads? to|drives?|affects?|improves?|"
                    r"raises?|lowers?|boosts?|harms?)\b", re.I)
IDENT = re.compile(r"\b(identification|identify|instrument|2sls|difference-in-differences|"
                   r"\bdid\b|regression discontinuity|\brdd\b|exogenous|parallel trends|"
                   r"randomly assigned|natural experiment|event study|synthetic control)\b", re.I)
SIG = re.compile(r"\bsignificant(ly)?\b", re.I)
MAG = re.compile(r"\b(percent|percentage points?|standard deviation|elasticity|coefficient|"
                 r"points?|pp)\b", re.I)


def script(skill, name):
    p = os.path.join(SKILLS_ROOT, skill, "scripts", name)
    return p if os.path.exists(p) else None


def run(script_path, args, as_json=True, timeout=120):
    if not script_path:
        return None
    try:
        cmd = [sys.executable, script_path] + args + (["--json"] if as_json else [])
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                             encoding="utf-8", errors="replace")
        if out.returncode != 0:
            return None
        if as_json:
            return json.loads(out.stdout) if out.stdout.strip() else None
        return out.stdout
    except Exception:
        return None


def p1(path):
    d = run(script("econtone-polish", "terminology_check.py"), [path])
    reg = run(script("econtone-ai-trace", "scan_register.py"), [path, "--limit", "3"], as_json=False)
    if d is None and not reg:
        return None, "no scanners available"
    banned = other = 0
    if d:
        hits = d.get("hits") or []
        banned = sum(1 for h in hits if h.get("kind") == "BANNED")
        other = len(hits) - banned
    defect = 0
    if reg:
        block = reg.split("CONTEXT")[0]
        defect = sum(int(m) for m in re.findall(r"\((\d+) lines?\)", block))
    pts = 25 - min(8, 4 * banned) - min(4, 2 * other) - min(8, 2 * defect)
    why = []
    if banned:
        why.append("%d banned variant(s)" % banned)
    if other:
        why.append("%d other glossary hit(s)" % other)
    if defect:
        why.append("%d register defect line(s)" % defect)
    return max(0, pts), "; ".join(why) or "clean"


def p2(text):
    causal = CAUSAL.findall(text)
    has_id = bool(IDENT.search(text))
    sig_no_mag = sum(1 for s in re.split(r"(?<=[.!?])\s+", text) if SIG.search(s) and not MAG.search(s))
    pts = 25
    why = []
    if causal and not has_id:
        pts -= min(10, 3 * len(causal))
        why.append("%d causal verb(s), no identification language" % len(causal))
    if sig_no_mag:
        pts -= min(6, 2 * sig_no_mag)
        why.append("%d significance claim(s) without a magnitude" % sig_no_mag)
    if not has_id:
        pts -= 3
        why.append("no stated design")
    return max(0, pts), "; ".join(why) or "claims match the evidence language"


def t1(path):
    d = run(script("econtone-ai-trace", "scan_detectability.py"), [path])
    if not d:
        return None, "scan_detectability.py not available"
    risk = d.get("risk") or {}
    idx = risk.get("risk_index")
    if idx is None:
        return None, "risk_index missing"
    return max(0, round(25 * (1 - float(idx) / 100.0))), "risk_index %.0f (%s)" % (
        float(idx), risk.get("tier", "?"))


def r1(path, profile):
    d = run(script("econtone-prosody", "prosody_check.py"), [path, "--profile", profile])
    if not d:
        return None, "prosody_check.py not available"
    if "overall" in d:
        v = d["overall"]
        verdict, red, warn, mk = v["verdict"], v["n_red"], v["n_warn"], v["n_markers"]
    else:
        verdict = d.get("verdict")
        red, warn, mk = d.get("n_red", 0), d.get("n_warn", 0), d.get("n_markers", 0)
    pts = 25 - 8 * red - 6 * mk - 1 * warn
    return max(0, pts), "%s: %d RED, %d marker(s), %d WARN" % (verdict, red, mk, warn)


def latitude(score):
    """Editing latitude in [0, 1]: plateau to 50, then the right half of a semicircle."""
    if score <= 50:
        return 1.0
    x = (score - 50) / 50.0
    return max(0.0, math.cos(math.pi * 0.5 * x))


def band(score):
    """Bands follow the latitude curve, so the label and the percentage can never disagree."""
    lat = latitude(score)
    if lat >= 0.70:
        return "full", "restructure, cut, rewrite, re-order — subject to never changing the meaning"
    if lat >= 0.50:
        return "reduced", "fix what is wrong; do not restructure; keep the author's sentences where they work"
    if lat >= 0.16:
        return "minimal", "corrections only: errors, terminology, claims that overstate the design; no stylistic rewriting"
    return "corrections-only", "only fix outright errors; change nothing else, even if it could read better"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--profile", choices=["body", "abstract", "intro"], default="body")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    text = open(a.file, encoding="utf-8", errors="replace").read()
    path = os.path.abspath(a.file)

    rows = [
        ("P1", "Terminology & register", "econtone-polish") + p1(path),
        ("P2", "Claims & structure", "econtone-polish") + p2(text),
        ("T1", "AI-trace risk", "econtone-ai-trace") + t1(path),
        ("R1", "Rhythm", "econtone-prosody") + r1(path, a.profile),
    ]
    W = {"P1": 40, "P2": 40, "T1": 10, "R1": 10}
    rows = [(r[0], r[1], r[2],
             None if r[3] is None else round(r[3] * W[r[0]] / 25.0),
             r[4], W[r[0]]) for r in rows]
    total = sum(r[3] for r in rows if r[3] is not None)
    lat = latitude(total)
    bname, badvice = band(total)

    if a.json:
        print(json.dumps({"file": a.file, "profile": a.profile,
                          "rows": [{"id": r[0], "row": r[1], "owner": r[2], "score": r[3],
                                    "max": r[5], "evidence": r[4]} for r in rows],
                          "total": total, "editing_latitude": round(100 * lat),
                          "band": bname, "advice": badvice,
                          "note": "orientation only; the pack always runs the full pipeline"},
                         ensure_ascii=False, indent=2))
        return 0

    print("EconTone score - %s (profile: %s)" % (os.path.basename(a.file), a.profile))
    for rid, name, owner, score, why, mx in rows:
        shown = "   n/a" if score is None else "%3d/%-3d" % (score, mx)
        print("  %s %-26s %s  %s" % (rid, name, shown, why))
    print("  " + "-" * 62)
    print("  TOTAL %d / 100   (rows with n/a are excluded)" % total)
    print("  EDITING LATITUDE %d%%  [%s]" % (round(100 * lat), bname))
    print("  " + badvice)
    print("  (orientation only - nothing was modified; the full pipeline still runs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
