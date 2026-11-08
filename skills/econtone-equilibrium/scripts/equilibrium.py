#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""equilibrium.py — the committee's three decision instruments.

    python equilibrium.py shapley data.json     contribution of each skill (needs all 2^n coalitions)
    python equilibrium.py bargain data.json     Nash bargaining over one contested move
    python equilibrium.py core    data.json     is any coalition of moves jointly profitable?
    python equilibrium.py selftest

Everything is exact arithmetic over numbers you supply; nothing here estimates a metric.
"""
import itertools
import json
import math
import sys

OBJECTIVES = ("validity", "trace", "rhythm")


# ---------------------------------------------------------------- Shapley
def shapley(players, values):
    n = len(players)

    def key(combo):
        return ",".join(sorted(combo, key=players.index))

    missing = [s for s in itertools.chain.from_iterable(
        itertools.combinations(players, k) for k in range(n + 1)) if key(s) not in values]
    if missing:
        return {"complete": False, "missing": [key(m) or "{}" for m in missing], "phi": None}
    phi = {p: 0.0 for p in players}
    for p in players:
        others = [x for x in players if x != p]
        for k in range(n):
            for s in itertools.combinations(others, k):
                w = math.factorial(k) * math.factorial(n - k - 1) / math.factorial(n)
                phi[p] += w * (values[key(tuple(s) + (p,))] - values[key(s)])
    return {"complete": True, "phi": {k: round(v, 2) for k, v in phi.items()},
            "total": round(values[key(players)] - values[""], 2)}


# ---------------------------------------------------------------- Bargain
def bargain(disagreement, moves, weights=None):
    w = weights or {"trace": 1.0, "rhythm": 1.0}
    rows = []
    for m in moves:
        dt = m["trace"] - disagreement["trace"]
        dr = m["rhythm"] - disagreement["rhythm"]
        feasible = dt > 0 and dr > 0
        prod = (dt ** w["trace"]) * (dr ** w["rhythm"]) if feasible else None
        rows.append({"move": m["name"], "d_trace": round(dt, 2), "d_rhythm": round(dr, 2),
                     "feasible": feasible, "product": None if prod is None else round(prod, 3)})
    feasible_rows = [r for r in rows if r["feasible"]]
    best = max(feasible_rows, key=lambda r: r["product"]) if feasible_rows else None
    return {"rows": rows, "winner": best["move"] if best else None,
            "note": "a move is admissible only if it beats the disagreement point on both axes"}


# ---------------------------------------------------------------- Core
def core(moves, tol=1e-9):
    """A coalition blocks if its summed deltas are weakly positive everywhere and strictly positive
    somewhere. Any blocking coalition means the empty set is not in the core."""
    blocking = []
    for r in range(1, len(moves) + 1):
        for combo in itertools.combinations(moves, r):
            s = {o: sum(m["delta"].get(o, 0.0) for m in combo) for o in OBJECTIVES}
            if all(s[o] >= -tol for o in OBJECTIVES) and any(s[o] > tol for o in OBJECTIVES):
                blocking.append({"coalition": [m["name"] for m in combo],
                                 "delta": {k: round(v, 2) for k, v in s.items()}})
    return {"core_empty": bool(blocking), "blocking": blocking}


def selftest():
    n = 0
    # Shapley: the textbook three-player example
    vals = {"": 0, "A": 30, "B": 20, "C": 10, "A,B": 60, "A,C": 45, "B,C": 35, "A,B,C": 80}
    r = shapley(["A", "B", "C"], vals)
    assert r["complete"] and abs(sum(r["phi"].values()) - 80) < 0.01
    assert r["phi"] == {"A": 37.5, "B": 27.5, "C": 15.0}, r["phi"]
    n += 1
    # incomplete data is reported, never imputed
    r = shapley(["A", "B"], {"": 0, "A": 5})
    assert not r["complete"] and "B" in ",".join(r["missing"])
    n += 1
    # bargaining: a move that improves one axis and hurts the other is inadmissible
    b = bargain({"trace": 50, "rhythm": 90},
                [{"name": "split", "trace": 34, "rhythm": 100},
                 {"name": "rewrite", "trace": 54, "rhythm": 97}])
    assert b["winner"] == "rewrite", b
    n += 1
    # core: two moves that are individually blocked but jointly profitable
    c = core([{"name": "a", "delta": {"validity": 0, "trace": -2, "rhythm": 3}},
              {"name": "b", "delta": {"validity": 0, "trace": 3, "rhythm": -1}}])
    assert c["core_empty"] and any(set(x["coalition"]) == {"a", "b"} for x in c["blocking"])
    n += 1
    return n


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "selftest":
        print("selftest: %d assertions passed" % selftest())
        return 0
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    cmd, path = sys.argv[1], sys.argv[2]
    data = json.load(open(path, encoding="utf-8-sig"))
    if cmd == "shapley":
        r = shapley(data["players"], data["values"])
        if not r["complete"]:
            print("shapley: INCOMPLETE — missing coalitions: %s" % ", ".join(r["missing"]))
            print("  nothing imputed; measure the missing coalitions first")
            return 1
        for k, v in r["phi"].items():
            print("  %-8s %+7.2f" % (k, v))
        print("  total gain %.2f" % r["total"])
    elif cmd == "bargain":
        r = bargain(data["disagreement"], data["moves"], data.get("weights"))
        for row in r["rows"]:
            print("  %-10s d_trace %+6.2f  d_rhythm %+6.2f  %s" %
                  (row["move"], row["d_trace"], row["d_rhythm"],
                   ("product %.3f" % row["product"]) if row["feasible"] else "inadmissible"))
        print("  winner: %s" % (r["winner"] or "none — keep the disagreement point"))
    elif cmd == "core":
        r = core(data["moves"])
        print("  core empty: %s" % r["core_empty"])
        for b in r["blocking"][:10]:
            print("  blocking: %s -> %s" % (b["coalition"], b["delta"]))
        if not r["blocking"]:
            print("  no coalition is jointly profitable: the equilibrium is core-stable")
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
