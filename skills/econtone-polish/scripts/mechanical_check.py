#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mechanical_check.py — spelling, US/UK consistency, and grammar slips.

These are errors, not style choices. They are corrected before any other pass and are not submitted to
the equilibrium: a move that fixes one is applied unconditionally.

    python mechanical_check.py DRAFT.md
    python mechanical_check.py DRAFT.md --json
    python mechanical_check.py selftest
"""
import json
import re
import sys

US_UK = {
    "analyze": "analyse", "analyzed": "analysed", "analyzing": "analysing",
    "behavior": "behaviour", "behaviors": "behaviours",
    "labor": "labour", "organization": "organisation", "organizations": "organisations",
    "organize": "organise", "organized": "organised", "center": "centre", "centers": "centres",
    "program": "programme", "programs": "programmes", "modeling": "modelling",
    "modeled": "modelled", "defense": "defence", "favor": "favour", "color": "colour",
    "honor": "honour", "enrollment": "enrolment", "fulfill": "fulfil", "judgment": "judgement",
    "catalog": "catalogue", "counseling": "counselling", "traveled": "travelled",
    "canceled": "cancelled", "labeled": "labelled", "signaling": "signalling",
}

CONFUSIONS = [
    ("could of", "could have"), ("would of", "would have"), ("should of", "should have"),
    ("alot", "a lot"), ("irregardless", "regardless"), ("definately", "definitely"),
    ("recieve", "receive"), ("seperate", "separate"), ("occured", "occurred"),
    ("accomodate", "accommodate"), ("untill", "until"), ("wether", "whether"),
]

LATEX = [(r"\\par\b", "paragraph command left in prose"), (r"``", "LaTeX open quote"),
         (r"''", "LaTeX close quote")]


def check(text):
    f = []
    us, uk = set(), set()
    for m in re.finditer(r"[A-Za-z]+", text):
        w = m.group(0).lower()
        if w in US_UK:
            us.add(w)
        elif w in set(US_UK.values()):
            uk.add(w)
    if us and uk:
        for w in sorted(us):
            f.append({"kind": "us/uk", "token": w, "suggest": US_UK[w],
                      "why": "the document mixes US and UK spellings"})
        for w in sorted(uk):
            f.append({"kind": "us/uk", "token": w, "suggest": w,
                      "why": "the document mixes US and UK spellings"})
    for wrong, right in CONFUSIONS:
        if re.search(r"\b%s\b" % re.escape(wrong), text, re.I):
            f.append({"kind": "spelling", "token": wrong, "suggest": right, "why": "misspelling"})
    for m in re.finditer(r"\b([A-Za-z]+)\s+\1\b", text, re.I):
        f.append({"kind": "doubled", "token": m.group(0), "suggest": m.group(1), "why": "word repeated"})
    for m in re.finditer(r"\s+[,;.:!?]", text):
        f.append({"kind": "spacing", "token": m.group(0).strip() or " ",
                  "suggest": m.group(0).strip(), "why": "space before punctuation"})
    for m in re.finditer(r"\ba\s+([aeiou][a-z]+)\b", text):
        f.append({"kind": "article", "token": m.group(0), "suggest": "an " + m.group(1),
                  "why": "vowel sound takes 'an'"})
    for pat, why in LATEX:
        for _ in re.finditer(pat, text):
            f.append({"kind": "latex", "token": pat, "suggest": "", "why": why})
    return f


def selftest():
    n = 0
    assert any(x["kind"] == "us/uk" for x in check("We analyze the behaviour of labor markets."))
    n += 1
    assert not [x for x in check("We analyse the behaviour of labour markets.") if x["kind"] == "us/uk"]
    n += 1
    assert any(x["kind"] == "doubled" for x in check("The the effect is clear."))
    n += 1
    kinds = {x["kind"] for x in check("Results are a outcome of the policy .")}
    assert "article" in kinds and "spacing" in kinds, kinds
    n += 1
    kinds = {x["kind"] for x in check("\\par The policy ``worked''.")}
    assert "latex" in kinds
    n += 1
    assert any(x["kind"] == "spelling" for x in check("It is alot of work."))
    n += 1
    return n


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        print("selftest: %d assertions passed" % selftest())
        return 0
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    text = open(sys.argv[1], encoding="utf-8", errors="replace").read()
    findings = check(text)
    if "--json" in sys.argv:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
    else:
        print("MECHANICAL CHECK — %s" % sys.argv[1])
        if not findings:
            print("  clean: no spelling, consistency or grammar slip detected")
        for x in findings:
            print("  %-9s %-14s -> %-12s %s" % (x["kind"], x["token"], x["suggest"], x["why"]))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
