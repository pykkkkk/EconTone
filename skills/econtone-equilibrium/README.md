# econtone-equilibrium

### The equilibrium orchestrator: the optimal combination of the three execution skills

Part of the **EconTone** pack. No voting, no ballots: it solves for the combination of legal moves that
leaves every player with nothing profitable left to do.

## What it decides

The pack has one orientation skill, three execution skills, and this one. The execution skills each work
alone — *together a fire, apart a sky full of stars* — and the orchestrator decides **which of them run, in
what order, and where the system stops**.

| Player | Legal moves | Objective | Bound by |
|---|---|---|---|
| `econtone-polish` (leader) | wording inside a sentence | professional validity | meaning invariance |
| `econtone-ai-trace` (second) | wording inside a sentence | trace cleanliness | validity unchanged |
| `econtone-prosody` (follower) | splits and merges only | rhythm proximity | guard + no marker + traces not RED |

## The game

```
maximise rhythm        subject to  validity unchanged and traces not degraded
maximise cleanliness   subject to  validity unchanged
maximise validity      subject to  meaning invariance
```

Lexicographic: a rhythm gain never buys a term, and a trace fix never buys an overclaim.

## Why the equilibrium is computable

The follower's action set is disjoint from the leaders': boundaries move, words do not. So a split can
never lower terminology or claim validity — the coupling is only through the trace proxies, and that is
what the guard measures. `segmentation_guard.py` proves the move was boundary-only; `rhythm_score.py`
provides the follower's objective.

## Procedure in one line each

1. Score → editing latitude (bounds the leader).
2. Prove the schedule: P → T → R is the only admissible order of six.
3. Each player moves under guards; every accepted move is measured, every rejection recorded.
4. Stop when no legal move is profitable — that is the equilibrium.
5. Deliver the certificate, the final text, and the residual risks.

## What it will not do

- Vote. A majority cannot restore a canonical term or legalise a boundary move.
- Write new prose. It schedules, accepts, rejects.
- Optimise a proxy as a target (`burstiness`, `risk_index`).
- Run a player whose objective is already met, to look busy.

## Instruments

`scripts/equilibrium.py` — `shapley` (contribution of each skill, needs all 2^n
coalitions), `bargain` (Nash bargaining over a contested move), `core` (is any coalition of moves
jointly profitable?). 4 self-test assertions.

## Files

- `SKILL.md` — the game, the admissibility table, the procedure, the certificate format
