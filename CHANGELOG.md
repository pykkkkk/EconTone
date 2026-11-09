# Changelog

## Versioning policy

A release number changes when the **structure or the feature set** changes: a new script, a new skill, a new
judgement rule, a new interface, a band recalibration that moves verdicts. Bug fixes, documentation edits and
threshold tweaks that restore intended behaviour **do not** open a new release; they are folded into the
version in force and described as corrections.

Why: a reader who sees 1.0.0 assumes the release notes describe the shape of the tool, not a running tally of
patch strings. Corrections accumulate silently; the moment a correction changes what the tool can decide, that
is a new release.

**1.0.0 is the release in force.** The orchestrator fixes listed below (peg density and burstiness counted as
gains, unknown risk tiers, player priority, mechanical-check exit codes) are corrections to 1.0.0, not 1.0.1.

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
