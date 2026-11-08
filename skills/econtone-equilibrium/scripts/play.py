#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""play.py — compute the equilibrium over several rounds. Deterministic.

Moves may be written by a model; the decision is not. Each round re-measures the surviving candidates
against the *current* text, accepts at most one move, and repeats until nothing is acceptable or the
round budget is spent.

    python play.py --current draft.md --moves moves.json --profile abstract --rounds 3 --out cert.json
    python play.py selftest

moves.json:

    [{"id": "m1", "player": "polish", "kind": "wording", "after": "cand/m1.md", "base": "draft.md"},
     {"id": "m2", "player": "prosody", "kind": "boundary", "after": "cand/m2.md", "base": "cand/m1.md"}]

`base` is the text the candidate was built from. A candidate whose base is not the current text is
**stale**: it is skipped, not guessed at, because applying it would silently undo the previous round.

Rules, in order: validity (no new terminology hit) -> trace (no worse risk tier, no +10) -> boundary
moves need a LEGAL guard, no marker, burstiness not RED -> any measured gain is a reason to accept.
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.dirname(os.path.dirname(HERE))
PY = sys.executable


def _script(skill, name):
    cand = os.path.join(SKILLS, skill, "scripts", name)
    if os.path.exists(cand):
        return cand
    local = os.path.join(HERE, name)
    return local if os.path.exists(local) else None


def _run(script, args):
    if not script:
        return ""
    p = subprocess.run([PY, script] + args, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.stdout or p.stderr or ""


def measure(path, profile, texts):
    rhythm = _run(texts["rhythm"], [path, "--profile", profile])
    det = _run(texts["detect"], [path])
    term = _run(texts["term"], [path])
    reg = _run(texts["register"], [path])
    m_rhythm = re.search(r"RHYTHM SCORE ([\d.]+)", rhythm)
    m_risk = re.search(r"risk_index ([\d.]+)", det)
    m_burst = re.search(r"Burstiness \(sentence-length CV %\)\s+([\d.]+)", det)
    markers = re.findall(r"\[(SLURRY|POUNDING|ROBOTIC|DENSE|FLAT)\]", rhythm + det)
    banned = len(re.findall(r"^\s+L\d+ ", term, re.M))
    defect_block = reg.split("CONTEXT")[0]
    register_hits = len(re.findall(r"tokens:", defect_block))
    tier = 2 if "MODERATE" in det else (3 if "HIGH" in det else 1)
    return {
        "rhythm": float(m_rhythm.group(1)) if m_rhythm else None,
        "risk": float(m_risk.group(1)) if m_risk else None,
        "burstiness": float(m_burst.group(1)) if m_burst else None,
        "markers": sorted(set(markers)),
        "terminology_hits": banned,
        "register_hits": register_hits,
        "tier": tier,
    }


def decide(base, cand, kind, guard_legal):
    """Pure function: same numbers, same verdict."""
    if cand["terminology_hits"] > base["terminology_hits"]:
        return False, "rejected: adds %d terminology hit(s)" % (
            cand["terminology_hits"] - base["terminology_hits"])
    if cand.get("tier", 1) > base.get("tier", 1):
        return False, "rejected: risk tier %d -> %d" % (base.get("tier", 1), cand.get("tier", 1))
    if cand["risk"] is not None and base["risk"] is not None and cand["risk"] > base["risk"] + 10:
        return False, "rejected: risk_index %.1f -> %.1f (+>10)" % (base["risk"], cand["risk"])
    if kind == "boundary":
        if not guard_legal:
            return False, "rejected: guard ILLEGAL (content changed)"
        if cand["markers"]:
            return False, "rejected: marker %s" % ",".join(cand["markers"])
        if cand["burstiness"] is not None and cand["burstiness"] < 35.0:
            return False, "rejected: burstiness %.1f falls into RED" % cand["burstiness"]
    gains = []
    if cand["terminology_hits"] < base["terminology_hits"]:
        gains.append("terminology -%d" % (base["terminology_hits"] - cand["terminology_hits"]))
    if cand.get("register_hits", 0) < base.get("register_hits", 0):
        gains.append("register -%d" % (base["register_hits"] - cand["register_hits"]))
    if cand["rhythm"] is not None and base["rhythm"] is not None and cand["rhythm"] > base["rhythm"]:
        gains.append("rhythm %+.1f" % (cand["rhythm"] - base["rhythm"]))
    if cand["risk"] is not None and base["risk"] is not None and cand["risk"] < base["risk"] - 1e-9:
        gains.append("trace %.1f" % (base["risk"] - cand["risk"]))
    if not gains:
        return False, "rejected: no measured objective improves"
    return True, "accepted: " + ", ".join(gains)


def is_stale(move_base, current):
    return os.path.normcase(os.path.abspath(move_base)) != os.path.normcase(os.path.abspath(current))


def selftest():
    n = 0
    base = {"rhythm": 92.9, "risk": 20.0, "burstiness": 40.0, "markers": [],
            "terminology_hits": 0, "register_hits": 0, "tier": 1}
    ok = {"rhythm": 100.0, "risk": 19.0, "burstiness": 41.0, "markers": [],
          "terminology_hits": 0, "register_hits": 0, "tier": 1}
    assert decide(base, ok, "wording", True)[0]
    n += 1
    assert not decide(base, dict(ok, terminology_hits=1), "wording", True)[0]
    n += 1
    assert not decide(base, dict(ok, risk=25.0, tier=2), "wording", True)[0]
    n += 1
    assert not decide(base, dict(ok, burstiness=24.9), "boundary", True)[0]
    n += 1
    assert not decide(base, ok, "boundary", False)[0]
    n += 1
    assert not decide(base, dict(ok, rhythm=92.9, risk=20.0), "wording", True)[0]
    n += 1
    assert decide(dict(base, terminology_hits=1), dict(ok, rhythm=92.9), "wording", True)[0]
    n += 1
    assert is_stale("a.md", "b.md") and not is_stale("a.md", "./a.md")
    n += 1
    return n


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        print("selftest: %d assertions passed" % selftest())
        return 0
    ap = argparse.ArgumentParser()
    ap.add_argument("--current", required=True)
    ap.add_argument("--moves", required=True)
    ap.add_argument("--profile", default="body")
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--out", default="certificate.json")
    a = ap.parse_args()

    texts = {
        "rhythm": _script("econtone-prosody", "rhythm_score.py"),
        "detect": _script("econtone-ai-trace", "scan_detectability.py"),
        "term": _script("econtone-polish", "terminology_check.py"),
        "register": _script("econtone-ai-trace", "scan_register.py"),
    }
    guard = _script("econtone-prosody", "segmentation_guard.py")

    moves = json.load(open(a.moves, encoding="utf-8-sig"))
    root = os.path.dirname(os.path.abspath(a.moves))
    for mv in moves:
        mv["after"] = mv["after"] if os.path.isabs(mv["after"]) else os.path.join(root, mv["after"])
        b = mv.get("base", os.path.basename(a.current))
        mv["base"] = b if os.path.isabs(b) else os.path.join(root, b)

    current = os.path.abspath(a.current)
    auto = []
    for mv in moves:
        if mv.get("gate") != "mechanical":
            continue
        if is_stale(mv["base"], current):
            auto.append({"id": mv["id"], "flagged": "stale at pre-pass"})
            continue
        auto.append({"id": mv["id"], "applied": True})
        current = mv["after"]
    chain, rounds, used = [current], [], set(m["id"] for m in moves if m.get("gate") == "mechanical")
    base_m = measure(current, a.profile, texts)

    for r in range(1, a.rounds + 1):
        evaluated, best = [], None
        for mv in moves:
            if mv["id"] in used:
                continue
            if is_stale(mv["base"], current):
                evaluated.append({"id": mv["id"], "player": mv.get("player", "?"),
                                  "accepted": False, "stale": True,
                                  "reason": "stale: built on %s, current is %s"
                                            % (os.path.basename(mv["base"]), os.path.basename(current))})
                continue
            cand = measure(mv["after"], a.profile, texts)
            legal = True
            if mv.get("kind") == "boundary":
                legal = "LEGAL" in _run(guard, [current, mv["after"]])
            ok, reason = decide(base_m, cand, mv.get("kind", "wording"), legal)
            row = {"id": mv["id"], "player": mv.get("player", "?"), "accepted": ok,
                   "reason": reason, "metrics": cand, "after": mv["after"], "base": mv["base"]}
            evaluated.append(row)
            if ok and (best is None or (cand["rhythm"] or 0) > (best["metrics"]["rhythm"] or 0)):
                best = row
        rounds.append({"round": r, "current": current, "moves": evaluated,
                       "accepted": best["id"] if best else None})
        if not best:
            break
        used.add(best["id"])
        current = best["after"]
        chain.append(current)
        base_m = best["metrics"]

    cert = {
        "rounds": rounds,
        "chain": chain,
        "final_text_path": current,
        "final_metrics": base_m,
        "mechanical_auto_applied": auto,
        "rule": "lexicographic; boundary moves need a LEGAL guard; stale candidates are skipped",
        "stopped_because": ("no acceptable move in round %d" % len(rounds))
        if not rounds[-1]["accepted"] else "round budget exhausted",
    }
    json.dump(cert, open(a.out, "w", encoding="utf-8"), indent=2)

    print("ROUNDS: %d   FINAL: %s" % (len(rounds), os.path.basename(current)))
    for rd in rounds:
        print("  round %d  accepted: %s" % (rd["round"], rd["accepted"] or "none"))
        for row in rd["moves"]:
            print("    %-5s %-8s %s" % (row["id"], row.get("player", "?"), row["reason"]))
    print("certificate -> %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
