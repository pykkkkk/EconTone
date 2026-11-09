# EconTone 1.0.1

Released 2026-11-09. This is the first release after 1.0.0 and it changes what the tool can decide, not just
how it reads: the orchestrator now sees its own detectors, the stress engine is an explicit parameter, and
every skill can print the chain of evidence behind its verdict.

Upgrade by replacing the five skill directories; there is no migration step and no new required dependency.

---

## Added

**Evidence chain, one per skill.** `scripts/evidence.py` ships inside all five members. It runs the skill's own
scripts on a draft and writes a page with a Mermaid flowchart, a table of scripts with their exit codes, the
reference files the model is instructed to read, and the rules applied.

```bash
python scripts/evidence.py draft.md      # -> evidence-<skill>.md
```

`econtone-equilibrium` reads a certificate instead (`evidence.py cert.json`), so the chain follows the
equilibrium rather than a single pass. The diagram is Mermaid and renders on GitHub; nothing leaves the machine
and no renderer is bundled.

**Explicit stress engine.** `--stress-engine auto|cmudict|heuristic`, on both `prosody_check.py` and
`rhythm_score.py`. `auto` uses CMUdict when importable, `cmudict` requires it and exits 2 if the corpus is
missing, `heuristic` forces the estimator. `rhythm_score.py` probes for an interpreter that can import nltk
and forwards the chosen engine, so a run costs the same everywhere.

**Chinese editions.** Every README — the pack home, five skills, examples — now has a `README.zh.md` written
in an academic register, with a language toggle at the top of each file. Links inside the Chinese editions point
to Chinese documents.

**Prompting guide.** `docs/prompting.md` and `docs/prompting-zh.md`: what each skill expects and returns, three
ways to invoke one, the four parts of a prompt, six templates, and six prompts that reliably produce bad results.

**Collocation table.** `references/terminology.md` now carries pairings whose basis is disciplinary convention
rather than measurement — `counterfactual exercise` → `counterfactual analysis`, `impact` for a coefficient →
`effect`, `prove` for an estimate → `show`, and others. The table states its own epistemic status.

**Repository fronts.** Requirements section (standard library only; `nltk` optional and what it buys), one-line
install, table of contents, badges that describe the method rather than the corpus, DSH origin, credits,
reference list, and a written versioning policy.

---

## Changed

**The orchestrator now scores what its own detectors report.**

| axis | before | now |
|---|---|---|
| transition-peg density | ignored | a decrease counts as a gain |
| burstiness | hard guard only | out of RED counts as a gain, boundary moves only |
| risk tier | compared | tier improvement counts as a gain |
| unknown tier | silently ranked as `LOW` | not compared: unknown is not safe |
| candidate selection | highest rhythm wins | player priority first (polish → trace → prosody), then rhythm |

**Abstract bands.** `mean_words_per_sentence` and `cv_words_per_sentence` are now the 10th–90th percentiles of
the 42-abstract corpus (16.5–33.5 and 22.7–72.6), replacing values that were close but not derived from the
abstracts directly.

**Heuristic runs no longer score the three stress metrics.** Under a heuristic engine, `nPVI`,
`alternation_rate` and `inter_stress_CV` are reported as `INFO` and excluded from the score and the verdict.
They are measurable only under CMUdict.

**Move validation.** A missing `after` or `base` file, or an unknown `kind`, is now an `error:` row instead of a
rejection. The certificate separates "refused" from "malformed".

**`mechanical_check.py` exit codes** are `0` clean, `2` findings, `1` error. Previously findings and crashes both
returned 1.

**Translation mode.** The source structure is not a constraint: claims, magnitudes and hedges are preserved,
rhetoric (`一方面…另一方面…`, `研究表明`, semicolon-chained clauses) is not. The output is advice; the rules stay
strict and the author overrides.

---

## Fixed

- `ELEVATED` risk tiers were parsed as the lowest rank, so an improvement to `MODERATE` was refused as a
  worsening. Tiers are now mapped explicitly.
- Move files generated against `move.schema.json` were rejected by validators, because the schema declared
  `additionalProperties: false` without listing `base` or `gate`. Both are now declared.
- `play.py` accepted any string for `--profile` and passed it to the scanners, which fell back to default bands
  silently. It now declares `choices`.
- A selftest asserted case-insensitive path behaviour and passed only on Windows; it failed on Linux CI. The
  assertion now compares a path with itself.
- The CI workflow and the `.git` directory could be destroyed by a rebuild; the release script now preserves
  `.git` and the workflow is restored.

---

## Verification

```
12/12 checks pass, no agent harness, no network
consistency: structure | pack.json | links | path claims | script claims |
             retired names | cross-skill links | counts | version | CI coverage |
             schema drift | profile vocabulary
prosody selftest 31/31 · rhythm_score 3/3 · play 12 · equilibrium 4
```

New consistency rules guard the two failure modes found during this cycle: a move field read by `play.py` but not
declared in the schema, and a `--profile` vocabulary that drifts between scripts.

---

## Known limits

- **Evaluation is thin.** Two texts and eight coalitions. The MDPI probe (ten 2016 abstracts) is exploratory and
  is not a benchmark.
- **Latitude is recorded, not enforced.** `play.py` does not read the scorecard, so the editing latitude remains
  an instruction the leader follows rather than a constraint the engine checks.
- **Cross-engine scores are not comparable.** A heuristic run and a CMUdict run measure different things; every
  report now states which engine produced its numbers.
- **The candidate set bounds the equilibrium.** `play.py` iterates over moves it is given; it does not generate
  new ones. Completeness of that set is the caller's responsibility.
