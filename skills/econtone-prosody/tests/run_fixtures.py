#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_fixtures.py — golden regression tests for the prosody gate.

Each fixture is a paragraph plus the verdict it must receive. Positive fixtures are
real published paragraphs the calibrated bands must accept; negative fixtures are
constructed failures the gate must catch. Run this after any threshold edit:

    python tests/run_fixtures.py
    python tests/run_fixtures.py --checker scripts/prosody_check.py

Exit code 0 only when every fixture matches.
"""
import argparse
import importlib.util
import json
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CHECKER = os.path.join(HERE, "..", "scripts", "prosody_check.py")


def load_checker(path):
    spec = importlib.util.spec_from_file_location("prosody_check", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checker", default=DEFAULT_CHECKER)
    ap.add_argument("--fixtures", default=os.path.join(HERE, "fixtures.json"))
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    pc = load_checker(args.checker)
    fixtures = json.load(open(args.fixtures, encoding="utf-8"))

    fails = 0
    print("%-14s %-9s %-8s %-8s %s" % ("fixture", "expect", "got", "markers", "result"))
    print("-" * 64)
    for fx in fixtures:
        pc.apply_profile(fx.get("profile", "body"))
        agg = pc.analyse_text(fx["text"])
        rep = pc.build_report(agg, fx["name"]) if agg else None
        got = rep["verdict"] if rep else "NO PROSE"
        names = [m["name"] for m in (rep["red_line_markers"] if rep else [])]
        ok = got == fx["expect"]
        missing = [m for m in fx.get("expect_markers", []) if m not in names]
        if missing:
            ok = False
        print("%-14s %-9s %-8s %-8s %s" % (
            fx["name"], fx["expect"], got, ",".join(names) or "-",
            "ok" if ok else "FAIL" + (" (missing %s)" % ",".join(missing) if missing else "")))
        if not ok:
            fails += 1
            if rep:
                bad = [m for m in rep["metrics"] if m["status"] != "OK"]
                for m in bad:
                    print("      %-26s %6.1f  %-4s  %s" % (m["metric"], m["value"], m["status"], m["band"]))
        if args.verbose:
            print("      why:", fx["why"])
    print("-" * 64)
    print("%d/%d fixtures passed" % (len(fixtures) - fails, len(fixtures)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
