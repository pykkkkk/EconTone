#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compare_modes.py — run the equilibrium twice (constrained and free) and report both.

    python compare_modes.py --current draft.md --moves moves.json --profile abstract
    python compare_modes.py --current draft.md --moves moves.json -o comparison.md

Produces one page with a fixed structure: two results, one metrics table, what differs, and the standing
section **How to use the two results**, whose recommendation is derived from the numbers rather than asserted.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EQ = HERE
SKILLS = os.path.dirname(os.path.dirname(HERE))
PY = sys.executable


def run(args):
    p = subprocess.run([PY] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.stdout or p.stderr or ""


def measure(path, profile):
    score = run([os.path.join(SKILLS, "econtone-score", "scripts", "score.py"), path, "--profile", profile])
    rhythm = run([os.path.join(SKILLS, "econtone-prosody", "scripts", "rhythm_score.py"), path, "--profile", profile])
    det = run([os.path.join(SKILLS, "econtone-ai-trace", "scripts", "scan_detectability.py"), path])
    g = lambda pat, txt: (re.search(pat, txt).group(1) if re.search(pat, txt) else "?")
    return {
        "total": g(r"TOTAL (\d+)", score),
        "rhythm": g(r"RHYTHM SCORE ([\d.]+)", rhythm),
        "markers": (re.search(r"markers: ([^)]+)\)", rhythm).group(1) if "markers:" in rhythm else "none"),
        "risk": g(r"risk_index ([\d.]+)", det),
        "burst": g(r"Burstiness \(sentence-length CV %\)\s+([\d.]+)", det),
        "tier": g(r"tier\s+\S+\s+(\S+)", det),
    }


def words(path):
    return len(open(path, encoding="utf-8").read().split())


def sentences(path):
    text = open(path, encoding="utf-8").read()
    return len(re.findall(r"[.!?](?:\s|$)", text))


def run_mode(mode, current, moves, profile, tag):
    """Each candidate gets its own run: a shared run would let the first acceptance hide the other.

    Returns (best_final_path, cert, rows, per_move) where per_move lists every attempted candidate.
    """
    attempts = []
    move_list = json.load(open(moves, encoding="utf-8-sig"))
    for mv in move_list:
        tmp = os.path.join(os.path.dirname(os.path.abspath(moves)), "one-%s-%s.json" % (tag, mv["id"]))
        json.dump([mv], open(tmp, "w", encoding="utf-8"), indent=2)
        cert_path = os.path.join(os.path.dirname(os.path.abspath(moves)), "cert-%s-%s.json" % (tag, mv["id"]))
        run([os.path.join(EQ, "play.py"), "--mode", mode, "--current", current, "--moves", tmp,
             "--profile", profile, "--rounds", "2", "--out", cert_path])
        cert = json.load(open(cert_path, encoding="utf-8-sig"))
        rows = [m for rd in cert["rounds"] for m in rd["moves"]]
        attempts.append({"mode": mode, "id": mv["id"], "final": cert["final_text_path"],
                         "accepted": any(m.get("accepted") for m in rows), "rows": rows,
                         "m": measure(cert["final_text_path"], profile)})
    accepted = [a for a in attempts if a["accepted"]] or attempts
    best = max(accepted, key=lambda a: (int(a["m"]["total"]) if a["m"]["total"] != "?" else -1,
                                        -(float(a["m"]["risk"]) if a["m"]["risk"] not in ("?", "None") else 999)))
    return best["final"], None, best["rows"], attempts


def advise(c, f, base, n_base, n_c, n_f):
    """Rule-driven, so the recommendation never asserts more than the numbers do."""
    out = []
    fb = float(f["burst"]) if f["burst"] not in ("?", "None") else None
    rk = lambda d: float(d["risk"]) if d["risk"] != "?" else None

    if fb is not None and fb >= 35 and rk(f) is not None and rk(base) is not None and rk(f) < rk(base):
        out.append("- **Use the free result to rewrite the paragraph.** It is the only one that pulls "
                   "burstiness out of the red band (%.1f) while lowering risk (%.1f -> %.1f)." % (fb, rk(base), rk(f)))
    else:
        out.append("- **Do not ship the free result as-is.** Its burstiness (%.1f) or risk does not improve "
                   "enough to justify the structural change." % (fb if fb is not None else -1))

    if c["total"] != "?" and f["total"] != "?" and int(c["total"]) >= int(f["total"]) - 2:
        out.append("- **Use the constrained result for a submission.** It keeps the sentence count (%d -> %d) "
                   "and still scores %s, within two points of the free run." % (n_base, n_c, c["total"]))
    else:
        out.append("- **Compare the two texts by hand before choosing.** The free run scores %s against %s, a gap "
                   "large enough that the structural rewrite is doing real work." % (f["total"], c["total"]))

    if n_c == n_f:
        out.append("- **Note what did not change.** Both texts keep %d sentences; the difference is in how the "
                   "clauses are grouped, not in how many there are — a referee will read it as a rewrite, not a "
                   "re-edit." % n_f)
    else:
        out.append("- **Note what did change.** The free run moves from %d to %d sentences; a referee comparing "
                   "drafts will see the restructure, so the certificate is the explanation." % (n_c, n_f))
    out.append("- **Record which one you took** and why — the certificate is the only place the choice is "
               "documented.")
    return out


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    args = dict(zip(a[::2], a[1::2]))
    current = args.get("--current")
    moves = args.get("--moves")
    profile = args.get("--profile", "body")
    if not current or not moves:
        print(__doc__)
        return 2
    out = args.get("-o", os.path.join(os.path.dirname(os.path.abspath(current)), "mode-comparison.md"))

    c_path, _, c_rows, c_all = run_mode("constrained", current, moves, profile, "c")
    f_path, _, f_rows, f_all = run_mode("free", current, moves, profile, "f")

    base, c, f = measure(current, profile), measure(c_path, profile), measure(f_path, profile)

    L = ["# Two regimes, two results", "",
         "| | constrained | free |", "|---|---|---|",
         "| final text | `%s` | `%s` |" % (os.path.basename(c_path), os.path.basename(f_path)),
         "| sentences | %d | %d |" % (sentences(c_path), sentences(f_path)),
         "| words | %d | %d |" % (words(c_path), words(f_path)), "",
         "## Metrics", "", "| file | total | rhythm | risk_index | burstiness | tier |", "|---|---|---|---|---|---|",
         "| draft | %s | %s | %s | %s | %s |" % (base["total"], base["rhythm"], base["risk"], base["burst"], base["tier"]),
         "| constrained | %s | %s | %s | %s | %s |" % (c["total"], c["rhythm"], c["risk"], c["burst"], c["tier"]),
         "| free | %s | %s | %s | %s | %s |" % (f["total"], f["rhythm"], f["risk"], f["burst"], f["tier"]),
         "", "## What differs", ""]
    for label, rows in (("constrained", c_rows), ("free", f_rows)):
        for mv in rows:
            L.append("- **%s** `%s` (%s): %s%s" % (label, mv["id"], mv.get("player", "?"), mv.get("reason", ""),
                                                   ("  — guard: " + mv["guard"]) if mv.get("guard") else ""))
    L += ["", "## How to use the two results", ""] + advise(c, f, base, sentences(current), sentences(c_path), sentences(f_path)) + [""]
    open(out, "w", encoding="utf-8", newline="").write("\n".join(L))
    print("comparison -> %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
