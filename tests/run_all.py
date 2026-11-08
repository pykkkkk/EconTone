#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run every check that can run without an agent harness.

    python tests/run_all.py

Exit code 0 only if every check passes. No third-party dependencies.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable

CHECKS = [
    ("prosody: 29 self-test assertions", ["skills/econtone-prosody/scripts/prosody_check.py", "selftest"]),
    ("prosody: 7 golden fixtures", ["skills/econtone-prosody/tests/run_fixtures.py"]),
    ("polish: terminology self-test", ["skills/econtone-polish/scripts/terminology_check.py", "selftest"]),
    ("ai-trace: detectability self-test", ["skills/econtone-ai-trace/scripts/scan_detectability.py", "selftest"]),
    ("score: smoke run on the sample", ["skills/econtone-score/scripts/score.py", "tests/sample.md", "--profile", "abstract"]),
    ("prosody: segmentation guard", ["skills/econtone-prosody/scripts/segmentation_guard.py", "selftest"]),
    ("prosody: rhythm score", ["skills/econtone-prosody/scripts/rhythm_score.py", "selftest"]),
    ("equilibrium: instrument self-test", ["skills/econtone-equilibrium/scripts/equilibrium.py", "selftest"]),
    ("equilibrium: play decision rule", ["skills/econtone-equilibrium/scripts/play.py", "selftest"]),
    ("polish: mechanical check", ["skills/econtone-polish/scripts/mechanical_check.py", "selftest"]),
    ("repo: consistency", ["tests/consistency.py"]),
    ("polish: checker runs on the sample", ["skills/econtone-polish/scripts/terminology_check.py", "tests/sample.md"]),
]


def run(argv):
    p = subprocess.run([PY] + [os.path.join(ROOT, a) if a.endswith(".py") or a.endswith(".md") else a
                              for a in argv],
                       cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def main():
    failed = 0
    for name, argv in CHECKS:
        rc, out = run(argv)
        tail = [l for l in out.strip().splitlines() if l.strip()][-1:] or [""]
        status = "PASS" if rc == 0 else "FAIL"
        if rc != 0:
            failed += 1
        safe = tail[0].encode("ascii", "replace").decode()
        print("%-4s %-38s %s" % (status, name, safe[:80]))
    print("-" * 78)
    print("%d/%d checks passed" % (len(CHECKS) - failed, len(CHECKS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
