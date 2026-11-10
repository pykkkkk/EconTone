---
name: econtone-equilibrium
description: >
  Equilibrium orchestrator for EconTone. Instead of voting, it solves for the optimal combination of
  the three execution skills — econtone-polish, econtone-ai-trace, econtone-prosody — under a
  lexicographic objective: professional validity is a hard constraint, traces are second, rhythm is an
  enhancement. Returns the schedule actually used, every move accepted or rejected with its reason, and
  an equilibrium certificate. Load when several passes exist, when the user asks "which combination
  should I run", or when a pipeline run must be shown to have stopped for a reason.
metadata:
  pack: econtone
  role: orchestrator
---

# EconTone Equilibrium — the orchestrator

> 聚是一团火，散是满天星 — *together a fire, apart a sky full of stars.*

Each execution skill is complete on its own: call `econtone-polish` for wording, `econtone-ai-trace` for
voice, `econtone-prosody` for cadence, and each delivers. Together they are a system whose **equilibrium**
this skill computes. It holds no ballot and casts no vote: it solves a game.

## Why no voting

A vote answers "which candidate do we prefer", and it produces a text that four seats tolerated. The
question here is different: **which combination of legal moves leaves every player with nothing profitable
left to do?** That is an equilibrium, and it is a property of the move set — not of a preference.
Majorities cannot buy a canonical term back, and they cannot make a boundary move legal.

## The players

| Player | Skill | Legal moves | Objective | May never violate |
|---|---|---|---|---|
| **Leader** | `econtone-polish` | rewrites *inside* a sentence | professional validity: terminology, register, claim strength | meaning invariance |
| **Second** | `econtone-ai-trace` | rewrites *inside* a sentence | trace cleanliness (`risk_index`, burstiness, pegs) | validity set by the leader |
| **Follower** | `econtone-prosody` | splits, merges, clause reordering, voice switch, function-word moves (moves #1,2,3,6,9,10,13) | rhythm proximity score | the guard, the marker stop, and trace cleanliness |

The leader's and second's action sets coincide (wording); the follower's overlaps only at the edges
(clause order, voice, function words) and never at the substance. That
disjointness is what makes the equilibrium computable instead of merely arguable: a boundary move cannot
change a word, so it cannot lower terminology or claim validity — **by construction**.

## The game

```
lexicographic Stackelberg

  leader    polish     maximise validity      V is a constraint, not a score
  second    ai-trace   maximise cleanliness   subject to V unchanged
  follower  prosody    maximise rhythm score  subject to V unchanged, C not degraded

  equilibrium = a profile in which no player has a legal move that raises its own objective
                without violating a higher-priority constraint, and the follower's boundaries are
                optimal given the leaders' wording.
```

The scorecard (`econtone-score`) does not play. It sets the **editing latitude**, which caps how large
the leader's move set is: at latitude 25% the leader may fix errors and nothing else; at 98% it may
restructure. The same wording, different feasible set, different equilibrium.

## Three instruments beyond the Stackelberg core

The equilibrium above answers "where do we stop". Three cheaper questions sit around it, each with a
script and each producing a number rather than an opinion.

| Instrument | Question | Command |
|---|---|---|
| **Shapley** | how much did each skill contribute? | `equilibrium.py shapley data.json` |
| **Nash bargaining** | is this contested move worth taking? | `equilibrium.py bargain data.json` |
| **Core** | is any *coalition* of moves jointly profitable? | `equilibrium.py core data.json` |

**Shapley** needs all 2^n coalitions measured. The script refuses to impute a missing one — an incomplete
table returns `INCOMPLETE` and the missing keys, because a contribution estimate built on guessed cells is
worse than no estimate.

**Bargaining** replaces the hard "rhythm yields" rule when a move improves one axis and hurts the other.
A move is admissible only if it beats the disagreement point on both axes; among those, the Nash product
`(Δtrace)(Δrhythm)` picks the winner, symmetric by default and weighted when the author states a preference.

**Core** strengthens the stopping certificate: instead of "no single legal move is profitable", it checks
every subset of candidate moves. If a coalition blocks — jointly positive on all axes while no member is
individually profitable — the current text is not core-stable and the blocking coalition must be reported.
In the two runs so far the core check found exactly one blocking singleton (a trace rewrite worth +3.9 trace
and +7.1 rhythm), which is what the pipeline then adopted.

### Translation restructures; the trace proxy may follow

Translating into English legitimately changes sentence structure, and restructuring tends to raise
`risk_index`. The script **will reject** such a move, and that is intended: the rule is strict so that every
rejection carries a number. The certificate then reports the rejected text, the metric that refused it, and
what adopting it would cost. **The author decides.** A rule that could be relaxed on request would stop being
a rule, and the report would lose the only thing that makes it useful — a stated price.

## The last mile belongs to the author

A paper is signed by a person. Everything this pack produces is therefore a **menu of actions**, not a verdict:
each row states what could change, what it would buy, and what it would cost. A **strategy** is a combination of
those actions, and the certificate offers a recommended one — but the author may add, drop or reorder moves to
suit a taste that no measurement captures.

This is why the report lists rejected moves with their price rather than discarding them: a scholar who prefers
the rejected version can take it, and will know what it costs.

For a writer without a settled sense of the discipline, the same menu is a teaching device: terminology and
claim strength are **hard constraints** and are marked as such, register follows the field, and rhythm is
presented as an aesthetic choice rather than a rule.

## Comparing the two regimes

When the author has not chosen a regime, run both and report them side by side:

```bash
python scripts/compare_modes.py --current draft.md --moves moves.json --profile abstract -o comparison.md
```

The script runs **each candidate on its own** in each regime — a shared run would let the first acceptance hide
the others — picks the best accepted result per regime, and writes one page with a fixed structure:

1. the two results (file, sentence count, word count);
2. one metrics table (draft / constrained / free: total, rhythm, risk, burstiness, tier);
3. what differed, move by move, with the guard verdict;
4. **How to use the two results** — always present, always in the same order.

Section 4 is rule-driven, never asserted: it says whether to ship the free version for a rewrite, whether the
constrained version is the submission copy, what did *not* change between them, and the reminder that the
certificate is where the choice is recorded. If the numbers do not support a recommendation, the bullet says so.

Every comparison names the regime in the certificate (`mode`) and the guard outcome per move, so a reader can
tell a refusal from a permission.

## Two regimes: constrained and free

| regime | who may move a sentence boundary | guard | use when |
|---|---|---|---|
| `constrained` (default) | only `econtone-prosody` | boundary moves must return LEGAL | single-skill calls, production text, anything the author will sign |
| `free` | either player | the guard still measures and reports, but does not block | the structure itself is in question: a paragraph that may need re-cutting, a translation whose sentence order is inherited |

`--mode free` lifts the **ownership** of boundaries, not the substance: terminology hits must still not rise and
the risk tier must not worsen. Every move records whether it changed content (`ILLEGAL (content changed;
allowed in free mode)`), so a free run is auditable rather than permissive.

Calling one skill on its own is always constrained. The two regimes exist in the orchestrator, because that is
where a combination is chosen.

## The output is advice, not a verdict

Everything this pack produces is a **suggestion with its measurements attached**. The certificate names what
was accepted, what was refused and why; the author may take the refused text, rewrite a third version, or
reject the lot. Nothing here is final on the author's behalf, and no script tries to be.

This is why the rules stay strict. A relaxed rule produces a quieter report; a strict rule produces a report
with a price on every alternative. The second is what an author can actually decide with.

## The entry rule, in the author's words

> 博弈考虑的是如何让一段基本合格的 text 尽可能地达到优秀；如果它不合格，那还没有资格进入博弈环节。

*The game asks how to take a basically competent text and make it as good as it can be. A text that is
not yet competent has not earned a place in the game.*

This is the reason the mechanical pass sits outside the equilibrium rather than inside it. A spelling
error, a grammar slip, a broken sentence: these are not moves to be weighed against a rhythm gain. They
are the price of admission. Measure them, fix them, and only then start the game — the numbers a broken
text produces describe the breakage, not the prose.

## Outside the game: mechanical corrections

A move that fixes a spelling, a US/UK inconsistency, or a grammar error is `"gate": "mechanical"`. It is
applied **before round 1**, unconditionally, and recorded as `auto-applied (mechanical)` — it never enters
the tally and cannot be rejected for raising a risk index or lowering the rhythm score. A grammar error is
a defect, not a trade-off.

**Entry condition.** A text enters the game only once its spelling and grammar are clean. The scripted
checks cover spelling and consistency; grammar is the leader's judgement, applied in the same pre-pass and
marked `gate: mechanical`. Do not measure, score, or run equilibria on a text that still contains a
linguistic error — the numbers would describe the error, not the prose.

## How the equilibrium is computed

**The scripts decide; the model only proposes.** `scripts/play.py` reads a move list, measures every
candidate with the same instruments the skills use, applies the lexicographic rules, and writes a
certificate. Same inputs, same certificate.

```bash
python scripts/play.py --current draft.md --moves moves.json --profile abstract --out certificate.json
python scripts/play.py selftest          # 8 assertions on the decision rule
```

**Multi-round.** `--rounds N` (default 3) re-measures the surviving candidates after each acceptance and
repeats until nothing is acceptable. A candidate whose `base` is no longer the current text is **stale**: it
is skipped rather than applied on top of the wrong text, because that would silently undo the previous round.
Real run: round 1 accepted the polish move, round 2 re-evaluated the prosody move that had been stale and
rejected it (`risk_index 7.9 -> 24.7`), then stopped.

A move is a claim, never a verdict:

```json
{"id": "m1", "player": "polish", "kind": "wording", "after": "cand/m1.md", "note": "..."}
```

`kind` is `wording` or `boundary`. `after` is the full text produced by the move — not a diff, so the
decision never depends on how the change was described. `scripts/move.schema.json` fixes the format.

The rule, in order:

1. **validity** — a move that adds a terminology hit is rejected;
2. **trace** — a move that worsens the risk tier, or raises `risk_index` by more than 10, is rejected;
3. **boundary moves** additionally need `segmentation_guard.py` LEGAL, no marker, burstiness not RED;
4. among survivors, any measured improvement (terminology, register, rhythm) is a gain; none means reject.

## When sub-agents are used

Advisory, not decisive. They widen the candidate set; they never adjudicate it.

| Trigger | Why |
|---|---|
| text is longer than ~1,500 words | a single context cannot search the move space widely enough |
| fewer than two candidates have been proposed | one candidate cannot show a preference; the equilibrium is trivial |
| the user asks for an audit | an independent reader re-derives the guards and flags disagreements |

When triggered, each proposer returns **only** schema-valid moves — no prose commentary, no ranking. The
orchestrator then runs `play.py` on the union. A sub-agent's opinion of its own move is discarded by
construction: the certificate records measurements, not votes.

## What the user receives

Four things, always, in this order:

1. **the final text** — the equilibrium text, ready to paste;
2. **the equilibrium result** — the certificate: which move won, its measured deltas, and the stopping
   condition, with the file path so it can be re-checked;
3. **the modification actions** — every accepted and rejected move with the number that decided it;
4. **other options** — the rejected moves re-framed as suggestions, plus any residual risk no skill may
   fix. The user may prefer a rejected move; the certificate gives them the cost of taking it.

## Status: testing

The framework is complete and every decision path has a script, but the **evaluation is thin**: two
texts, eight coalitions, no large-scale benchmark, and the scorecard's own thresholds are provisional.
Treat the numbers as measurements of these instruments, not as evidence that the instruments are right.

## Procedure

### 0 — Parameterise
Run `econtone-score`. Record the latitude. It bounds the leader; it never binds the follower.

### 1 — Check admissibility of the schedule before running it
Three players admit six orders; only one is admissible. Do not assume it — show it:

| Order | Verdict | Why |
|---|---|---|
| P → T → R | **admissible** | wording settled before boundaries move; precedence respected |
| P → R → T | rejected | T rewrites after the boundaries moved; its changes would invalidate R's measurements |
| T → P → R | rejected | the second player would set constraints for the leader |
| T → R → P | rejected | both violations above |
| R → … | rejected | the follower cannot move before the leaders have chosen the wording |

State the rejection of the other five in the output. This table *is* the proof that the pipeline is not
an arbitrary sequence.

### 2 — Let each player move, with guards
- **polish** executes within its latitude; then `econtone-score` is re-read for V.
- **ai-trace** proposes rewrites; accept one only if V is unchanged **and** cleanliness is non-worse.
  Reject otherwise, and record the rejection — a rejected move is evidence, not a failure.
- **prosody** proposes splits and merges; accept only if all three hold:
  `segmentation_guard.py BEFORE.md AFTER.md` is LEGAL, the result carries no red-line marker, and
  burstiness does not fall into RED. Accept the move that raises `rhythm_score.py` the most.

Moves #5 (sentence-style appositive), #11 (nominalisation) and #12 (synonym shift) are **not** the
follower's to execute: it files a proposal, the leader decides. A rejected proposal is part of the
equilibrium record — #5 in particular is rejected whenever the paragraph already carries a demonstrative.

### 3 — Stop on the equilibrium condition, not on a target
When no player has a legal, profitable move, stop. That is the equilibrium. Two frequent outcomes:

- **No profitable boundary move exists** because the only out-of-band metric is word-level
  (`syllables/word`), which the follower's action set cannot touch. Say exactly that; do not split a
  sentence to look busy.
- **A profitable boundary move exists but the trace guard blocks it.** Record the rejected move and the
  metric it would have broken. The delivered text is the one *before* the move.

### 4 — Skip stages when their marginal gain is zero
The optimal *combination* is not always all three. Skip a player when its objective is already met:

| Signal | Decision |
|---|---|
| trace `risk_index` LOW and burstiness OK | run ai-trace only as a check, not as an editor |
| `rhythm_score` already at maximum | run prosody only as a verification |
| latitude < 30% | polish corrects; do not let it restructure |
| any blocking defect (marker, canonical-term miss) | run that player regardless of the other signals |

### 5 — Deliver the certificate

```
## Schedule
P -> T -> R, admissible (the other five orders are shown rejected in the table above)

## Moves
| # | player | move | accepted? | metric before -> after | reason |

## Equilibrium certificate
No legal move remains that raises any player's objective without violating a higher-priority
constraint. [One sentence naming what was tried and rejected, with numbers.]

## Text
<final text>

## Residual risks
<what no skill may fix: missing magnitudes, unsupported claims, citations>
```

## Hard rules

1. **No voting.** If a decision needs a majority, it is not this skill's decision — it is a constraint
   violation or a residual risk to hand back to the author.
2. **No new prose.** The orchestrator schedules and accepts or rejects moves; it does not write.
3. **Never trade a hard constraint for a soft one.** Rhythm is an enhancement; a canonical term is not.
4. **Never optimise a proxy as a target.** `burstiness` and `risk_index` are diagnostics; a text that
   scores well and reads worse is a failure of this skill.
5. **Record rejections.** The equilibrium is defined by the moves that were refused.

## Failure modes

- **Voting reappears** ("the orchestrator prefers v2"): reject — preferences do not enter the equilibrium.
- **Stage theatre**: running a player whose objective is already met, to show activity.
- **Proxy chasing**: splitting sentences until `burstiness` crosses 50%.
- **Assuming the schedule**: running P→T→R because the README says so, instead of showing the other five
  orders are inadmissible.

## Position in the pack

`econtone-score` orients → the three execution skills each work alone → **`econtone-equilibrium`** computes
their optimal combination when more than one pass is in play, and certifies where the system stopped.
