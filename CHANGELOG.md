# Changelog

## Versioning policy

A release number changes when the **structure or the feature set** changes: a new script, a new skill, a new
judgement rule, a new interface, a band recalibration that moves verdicts. Bug fixes, documentation edits and
threshold tweaks that restore intended behaviour **do not** open a new release; they are folded into the
version in force and described as corrections.

Why: a reader who sees 1.0.0 assumes the release notes describe the shape of the tool, not a running tally of
patch strings. Corrections accumulate silently; the moment a correction changes what the tool can decide, that
is a new release.

**1.0.2 is the release in force.** It opened because the orchestrator gained a second regime (`--mode free`),
which changes what the tool can decide. Corrections and additions that do not change the shape of the tool wait
under *Unreleased* until the next structural change.

## Unreleased

- `scripts/compare_modes.py` — runs every candidate once per regime and writes a four-part comparison page
  ending in **How to use the two results**. Held back from a version number on purpose: the release policy in
  this file opens a version when the shape of the tool changes, and this is one script.

## 1.0.2 — two regimes (2026-11-10)

Full notes: [`RELEASE-1.0.2.md`](RELEASE-1.0.2.md).

**Added.** `--mode constrained|free` on `play.py`. In `constrained` (default) sentence boundaries belong to
`econtone-prosody` and a boundary move must return LEGAL; in `free` either player may cross a boundary, and the
guard still measures and reports the content change but does not block. Terminology hits and the risk tier
remain hard constraints in both modes.

**Added.** The design principle is now written into the skill: *the last mile belongs to the author*. The
certificate is a menu of **actions** with prices; a **strategy** is a combination the author assembles. The
recommended path is a default, not a verdict.

**Changed.** Certificates record `mode` and, per move, a `guard` field, so a free run stays auditable. Standard
output prints the mode alongside the round count.

**Limits unchanged.** Free mode does not relax validity or trace: it lifts the ownership of boundaries only.

## 1.0.1 — the first release after 1.0.0 (2026-11-09)

Full notes: [`RELEASE-1.0.1.md`](RELEASE-1.0.1.md). Summary of what changed since 1.0.0.

**Added.** `evidence.py` in all five skills (Mermaid evidence chain: scripts, exit codes, references, rules);
`--stress-engine auto|cmudict|heuristic` with an interpreter probe that looks for nltk; Chinese editions of
every README with language toggles; a prompting guide in English and Chinese; a collocation table in the
terminology reference; requirements, one-line install, table of contents, method badges, DSH origin, credits,
reference list, and a written versioning policy.

**Changed.** The orchestrator now counts transition-peg density, burstiness out of RED (boundary moves) and
risk-tier improvement as gains; unknown risk tiers are no longer ranked as `LOW`; candidate selection follows
the documented player priority instead of rhythm greed; abstract bands are the corpus 10th–90th percentiles;
heuristic runs report the three stress metrics as `INFO` instead of scoring them; malformed moves are errors,
not rejections; `mechanical_check.py` returns 0/2/1.

**Fixed.** `ELEVATED` tiers were parsed as the lowest rank; the move schema omitted `base` and `gate`;
`play.py` accepted any `--profile` string; a selftest passed only on Windows; a rebuild could destroy `.git`
and the CI workflow.

**Limits unchanged.** Evaluation remains thin; latitude is recorded, not enforced; cross-engine scores are not
comparable; the equilibrium is bounded by the candidate set it is given.

## 1.0.0 — first public release (2026-11-08)

**Five skills, one equilibrium.**

- `econtone-score` — a four-row scorecard (terminology 40, claims 40, traces 10, rhythm 10) that returns an
  **editing latitude**: how hard the downstream editors may press, from 25% (errors only) to 98% (restructure).
- `econtone-polish` — drafting: 135 canonical EN↔ZH term pairs, 32 writing rules distilled from six graduate
  guides (each tagged with its source), 37 sentence patterns, and a **Step 0** that fixes spelling, US/UK
  consistency and grammar before anything else.
- `econtone-ai-trace` — three scanners, a `risk_index`, and a baseline → rewrite → re-measure delta table.
- `econtone-prosody` — nine banded metrics calibrated on 42 open-access papers, five red-line markers, a
  segmentation guard, and a rhythm proximity score.
- `econtone-equilibrium` — the orchestrator: a lexicographic Stackelberg game, a deterministic `play.py`
  that computes the equilibrium over multi-round candidate moves, plus Shapley, Nash bargaining and a core
  check.

**Principles fixed in the code, not just in prose**

- Mechanical and grammatical errors are the **price of admission**, never a move in the game.
- Rhythm is an **enhancement**: it maximises proximity and stops when no legal move helps.
- Word-level edits and sentence-boundary moves have **disjoint owners**, so the follower cannot damage the
  leader's constraints by construction — verified by a guard, not by a model.
- Every rejected move is recorded with the number that rejected it.

**Verification at release**

- 11/11 checks pass without an agent harness (`tests/run_all.py`).
- 42-paper corpus: 42 abstracts, 42 introductions, 802 body paragraphs, CC BY 38 / CC BY-NC 4.
- 7 golden rhythm fixtures (4 must PASS, 3 must REVISE).
- First equilibrium measurements in `docs/equilibrium-results.md`.

**Status: testing.** The framework is complete; the evaluation is thin — two texts, eight coalitions, no
large-scale benchmark, and the scorecard thresholds are provisional.
