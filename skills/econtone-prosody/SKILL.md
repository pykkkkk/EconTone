---
name: econtone-prosody
description: >
  Rhythm-and-density gate for English academic prose that already exists: measures
  nPVI, %stressed syllables, stress alternation, inter-stress CV, syllables per word,
  sentence-length statistics and parallelism density, and reports five sentence-level
  red-line markers (SLURRY / POUNDING / ROBOTIC / DENSE / FLAT). Load when the
  question is how a passage reads — 韵律, 节奏, 句子长短, 拗口, 读着累, prosody,
  rhythm, cadence, readability, sentence rhythm — or when econtone-polish hands
  off its Block A for the final gate. English only; it does not translate, retune
  terminology, or change content.
metadata:
  pack: econtone
  role: gate
---

# Prosody Polish (PP) — the rhythm-and-density gate

Draft-level editing — terminology, register, causal language, AI traces — belongs to
`econtone-polish` (TJP). This skill answers the one question those passes cannot:
**does the finished English read smoothly, sentence by sentence?**

It is a measuring instrument with a repair loop attached, not a rewriter. Every number it
reports is a proxy for reading comfort, and the proxy is only worth acting on when the
offending sentence is named.

---

## When to load

- The user has an **English** passage of two or more sentences and asks about rhythm, flow,
  cadence, sentence length, or "读起来累不累".
- TJP has produced a Block A and the user agrees to run the gate.
- A paragraph keeps getting flagged as "flat" or "mechanical" and nobody can say why.

## When not to load

- **One sentence.** The metrics are undefined or unstable on a single sentence.
- **Chinese output** (e.g. TJP's `TR-EN2ZH`). The checker scores English phonology.
- **The text is not written yet.** This gate measures; it does not compose.
- **You want terminology, hedging, or causal-language fixes.** That is TJP's Step 3–5.

---

## Hard constraints (read before adjusting)

This gate runs after drafting and **before** the final trace check. Two things are outside its authority:

1. **Terminology.** Never swap a canonical term for a shorter synonym to fix `syllables/word` or
   `parallelism`. "Identification" stays "identification" even at five syllables.
2. **AI traces.** Never reintroduce what the trace pass removed — stacked connectives, `thus`
   chains, `respectively` padding, symmetrical clause pairs — even when it would lift CV or settle a
   parallelism count.

When the only remaining fix would break either rule, record a waiver with the reason and stop. A
WARN with a written waiver is the correct outcome; a clean metric table bought with a worse sentence
is not.

## One natural paragraph per measurement

The metrics are paragraph-scoped. If the input holds more than one paragraph, split on blank lines
and report each paragraph separately — never pool them into a single average, which hides a flat
paragraph inside a varied document. For a single-paragraph request, confirm with the user that the
text really is one paragraph before running; a two-paragraph paste measured as one unit produces a
meaningless CV.

## Procedure

1. **Materialise the text.** Paste → a `.md` file in the workspace (or accept the `.tex`
   path). Never edit the user's source in place.
2. **Baseline first.** Run the checker *before* touching a word, so the before/after table
   later means something.
3. **Read the report.** Nine banded metrics plus any sentence-level marker. A marker names
   the sentence that caused it.
4. **Adjust, then re-run.** Use the recipes below; never flatten prose to make a number look
   clean.
5. **Stop at the exit gate** — not when the numbers look nice.
6. **Report** the before/after table, the verdict, and any waiver with its reason.

```bash
python scripts/prosody_check.py DRAFT.md                  # human-readable
python scripts/prosody_check.py DRAFT.md --json > p.json  # machine-readable
python scripts/prosody_check.py --text "..."              # quick probe
python scripts/prosody_check.py selftest                  # 27 assertions
```

---

## The section decides the band

A journal abstract is not a body paragraph, and the same cadence rules do not apply to both. An abstract
runs four to six sentences; its sentence-length spread is **structurally** narrower than a body section's,
so a body-calibrated band will call a perfectly ordinary abstract flat.

Three profiles ship with the skill — `abstract`, `intro`, `body` — and they differ exactly where the corpus
shows a genre effect:

| Band | abstract | intro | body |
|---|---|---|---|
| `cv_words_per_sentence` floor | 14 | 18 | generic |
| `mean_words_per_sentence` | 16–34 | 14–31 | 16–34 |
| `parallel_per100` | 2.8–6.8 | 1.4–8.0 | default |

**Always pass `--profile`.** The default is `body`; applying it to an abstract reports failures that are
artefacts of the genre, not defects of the prose. If the section is unknown, ask the user instead of guessing:
a two-point rhythm difference can flip the verdict.

## The target bands (calibrated on 42 published papers)

Comfort band = the 10th-90th percentile of published prose in 42 OA economics / finance /
management papers (2016-2021, 8 per year, first author at a world-top department): 42 abstracts,
42 introductions, 794 body paragraphs. Red lines sit beyond the corpus tail.

| Dimension | body | abstract | intro | Red line (marker) |
|---|---|---|---|---|
| nPVI (stress contrast) | 35–41 | 35–41 | 35–41 | `< 15` → FLAT |
| % stressed syllables | 31–41 | 29–39 | 30–40 | — |
| alternation rate | 52–62 | 52–62 | 52–62 | `> 78` → ROBOTIC |
| inter-stress CV | 43–57 | 43–54 | 43–57 | — |
| syll / word | 1.6–2.0 | 1.8–2.2 | 1.6–2.0 | `> 2.2` (abstract 2.4) |
| **words / sentence** | **16–34** | **16–34** | **14–31** | `> 45` → DENSE |
| p95 words / sentence | ≤ 62 | ≤ 56 | ≤ 62 | `> 95` |
| **CV words / sentence** | **≥ 24** | **≥ 23** | **≥ 30** | `< 15` → FLAT |
| parallelism / 100 words | 1.4–7.7 | 2.8–6.8 | 1.4–8.0 | `> 10` → gunfire |

Pass a profile with `--profile abstract|body|intro`. The default is `body`.

The earlier bands (36-42 stressed, 22-35 words, CV ≥ 50, parallelism 2.5-4.5) were fit to a
hand-built 9-paper sample and rejected 61-76% of real published paragraphs; these replace them.


## Red-line markers are blocking

A marker is a **sentence-level** finding, not an aggregate hint:

1. **SLURRY** — ≥ 10 unstressed syllables in a run (`of/for/in/the` + relative clauses stacked).
2. **POUNDING** — ≥ 7 stressed syllables in a run (piled monosyllabic content words).
3. **ROBOTIC** — alternation > 78% *and* inter-stress CV < 35%.
4. **DENSE** — mean sentence length above 45 words.
5. **FLAT** — nPVI < 15.

**Any marker forces `REVISE`, even when all nine bands read OK.** A clean metric table does not
override a flagged sentence. This is enforced in the code (`verdict` includes `markers`) and
locked by three self-test assertions.

---

## Exit gate

Rhythm is an **enhancement, not a requirement** — this gate improves a text that is already correct.
It never rewrites a word, and it never trades away meaning or terminology to hit a number.

- **Move only boundaries.** Splitting and merging are the entire action set. Verify every move with
  `python scripts/segmentation_guard.py BEFORE.md AFTER.md` — if a single word changed, the move is
  illegal and belongs to the polish or trace pass instead.
- **Maximise, do not force.** `python scripts/rhythm_score.py DRAFT.md --profile intro` returns a 0–100
  proximity score. Stop when no remaining split or merge raises the score. A score of 60 with no marker
  and intact wording beats a 100 bought with a rewritten clause.
- **One hard stop.** No red-line marker in the delivered text: a marker names a sentence that reads
  badly, and that is fixable by segmentation alone.
- `PASS` (all bands inside) is the best outcome, not the admission ticket. `ADJUST` with a recorded
  distance and no marker is a legitimate delivery.

---

## The move set (v2)

You own more than boundaries now. Legal moves, verified by `scripts/segmentation_guard.py`:

| # | Move | Changes | Legal? |
|---|---|---|---|
| 1 | split a sentence at a clause boundary | boundary | `boundary-only` |
| 2 | merge two sentences (semicolon or connective) | boundary | `boundary-only` |
| 3 | adjust the function words at a seam (`and` -> `It`) | function words | `boundary-only` |
| 6 | semicolon <-> period | punctuation | `boundary-only` |
| 9 | reorder clauses inside a sentence (fronting) | content order | `licensed-rewording` |
| 10 | switch voice (active <-> passive) | inflection | `licensed-rewording` |
| 13 | insert or delete a function word to break a stressed run | function words | `licensed-rewording` |

Run the guard with `--licensed` for #9, #10 and #13. Anything the guard classes `illegal` is not yours,
and **guard legality is necessary but not sufficient**: #5 would pass the guard and is still not yours to
execute, because it manufactures a demonstrative and repeated use becomes a template. #5, #11 and #12 are
proposals.

### Proposals (not moves)

Three moves are proposal-only — **#5** (sentence-style appositive), **#11** (nominalisation change) and
**#12** (synonym shift). File one instead of executing it:

```
PROPOSAL #12  "use" -> "utilise"
  target: syllables/word 2.21 -> 2.09 (band 1.8-2.2)
  risk:   register (Latinism); terminology: not a canonical term
  owner:  econtone-polish decides; econtone-ai-trace checks the result
```

`econtone-polish` accepts or rejects it; a rejection is recorded as equilibrium evidence, not as a
failure. You never execute #5, #11 or #12 yourself.

## Adjustment recipes

| Symptom | Fix | Watch out |
|---|---|---|
| SLURRY (long unstressed run) | split the sentence, or switch the clause to active voice with a concrete subject | splitting adds a sentence and lowers mean words/sentence — check the band afterwards |
| POUNDING (monosyllable pile-up) | insert a connective or a weak syllable; swap one Anglo-Saxon noun for a Latinate one | the opposite failure is real: all-Latinate prose fails `syllables/word` |
| ROBOTIC alternation | write one deliberately long sentence next to a short one | alternating every sentence is what triggered it |
| DENSE | split at the argument boundary, not at the comma | keep the identification argument in one sentence even if long |
| monotone CV (< 35%) | plant a 5–8 word sentence and one 35–40 word sentence | uniform mid-length sentences are the actual failure mode |
| parallelism > 6 | drop one `and/but/or`, or convert a coordinated clause into a subordinate one | parallel lists of subgroups are legitimate — do not break them just for the number |
| `syllables/word` > 2.0 | swap a Latinate noun for a shorter one | deleting short words raises the ratio (denominator effect); substitute, do not delete |

Two traps worth knowing, both observed in practice:

- **Deleting words to fix length backfires.** `syllables/word` is a ratio; removing short
  function words makes it *worse*. Substitute weight, do not delete it.
- **A lower sentence-length stdev is not progress.** It can come from flattening. Verify in the
  structural scanner (`scan_ai_traces.py` in TJP): `within ±2 words` should stay low and the
  `≥2× length ratio` share high.

---

## Reporting format

```
| metric | before | after |
| ...    | ...    | ...   |

VERDICT: PASS (RED=0, WARN=0, MARKERS=0)
WARN waived: mean_syll_per_word 1.9 — technical vocabulary floor, no substitution left
```

If you changed the prose, hand back the **edited text**, not just the numbers. The user asked for
a readable paragraph, not a dashboard.

---

## Stress engine (CMUdict, optional)

Stress patterns come from **CMUdict** when `nltk` and its `cmudict` corpus are importable;
otherwise the checker falls back to a built-in lexicon plus a first-syllable heuristic, silently.
The report header always prints which engine ran:

```
2 sentences, 34 words (body prose only) | engine: cmudict
```

- Enable: `pip install nltk` then `python -m nltk.downloader cmudict`.
- Disable for one run: `--no-cmu`.
- The stress metrics carry **engine-specific bands**: CMUdict marks secondary stress, so its
  `%stressed` band sits near 48-57 instead of 31-41. Both band sets were calibrated on the same
  42-paper corpus, so a cmudict run is compared against cmudict prose.

**Which interpreter to call.** The engine is chosen by *which Python runs the script*, so name it:

| Interpreter | nltk / cmudict | Engine |
|---|---|---|
| the `python` on PATH | present on this machine | `cmudict` |
| the DSH bundled runtime (`...\dsh-runtimes\...\python.exe`) | absent | heuristic fallback |

**Prefer the PATH `python` for this skill.** The bundled interpreter is stdlib-only and will
silently fall back, which changes the stress metrics and therefore which band set applies. If a run
reports `engine: heuristic`, say so when reporting the verdict: the numbers are still usable, but
they are heuristic numbers.

## Caveats

- **Stress is a heuristic.** A small lexicon plus a first-syllable rule; multi-syllable and
  Latinate words are mis-estimated. CMUdict or acoustic data would be better.
- **"Comfort" is not a validated psychometric.** These metrics measure rhythm contrast and
  regularity, one facet of reading ease. Never optimise a single number.
- **The bands come from an internal calibration corpus** (7 papers, re-validated on 9), not from
  a published study. Treat them as heuristics.
- **English only.** The checker will run on Latin-script text of any language, but the stress
  model is English.

---

## Files

- `scripts/prosody_check.py` — the checker: nine banded metrics, five markers, `--json`,
  `--text`, `selftest` (27 assertions). Standard library only, read-only, no network.
- `references/prosody_target_card.md` — the derivations, marker definitions, and the
  adjust-and-re-run loop.
- `tests/fixtures.json` + `tests/run_fixtures.py` — golden regression: four published
  paragraphs that must PASS, three constructed paragraphs that must REVISE (DENSE, flat CV,
  POUNDING). Run it after any threshold edit:

  ```bash
  python tests/run_fixtures.py
  ```

## Position in the EconTone pack

PP is the **last** stage. If both pack members run, TJP always goes first and PP second, because
PP moves sentence boundaries: running PP before TJP would leave every `原文片段 → 修改后` row in
TJP's Block B pointing at text that no longer exists.

PP also runs standalone: any finished English paragraph can enter here directly, without TJP.

## The stress engine is part of the measurement

`--stress-engine auto|cmudict|heuristic` selects how stressed syllables are found. The choice changes the
numbers, so it is not an implementation detail:

| engine | source of stress | what it scores |
|---|---|---|
| `cmudict` | the CMU pronouncing dictionary | every banded metric, including nPVI, alternation and inter-stress CV |
| `heuristic` | syllable-count estimate | the same metrics, but nPVI, alternation and inter-stress CV are marked `INFO` and **not scored** |

Two rules follow:

1. **Every report states its engine.** `prosody_check.py` prints `engine: ...` in the header; `rhythm_score.py`
   prints `ENGINE: ...` before the score. A report without that line is incomplete.
2. **Scores are comparable only within one engine.** A heuristic score and a cmudict score measure different
   things; putting them in the same table is an error, and a delta across engines means nothing.

If `--stress-engine cmudict` is requested but the corpus is unavailable, the script exits with status 2 rather
than silently falling back: a silent fallback would produce a number labelled with the wrong engine.
