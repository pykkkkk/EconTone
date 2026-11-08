# Changelog

All notable changes to this skill are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `references/anti_ai_trace_audit.md` — the Step 8 method as a **measured loop**
  (baseline → triage → rewrite → re-measure → verify rhythm). Includes the
  threshold and target-band table, the trace-to-fix mapping, an eight-point
  pitfall list, the delta-table deliverable format, and a generic worked
  example.
- `scripts/scan_ai_traces.py` — structural probes: punctuation traces,
  transition-peg density, repeated syntactic templates, long-sentence load
  (`>45`/`>60` English words), and sentence-length rhythm (`within ±2 words`,
  `≥2× length ratio`, longest same-length run, length histogram).
- `scripts/scan_register.py` — diction probes split into **defect** bands
  (hype/journalistic, ornate/literary, assertive filler, over-assertive verbs,
  AI emphasis adverbs, wordy nominalisation) and **context** bands
  (self-narration, vague intensifier, precision claim, vague quantifier,
  repeated contrast frame).
- `scripts/prosody_check.py` — Step 9 rhythm-and-density gate: nPVI, %stressed,
  alternation rate, inter-stress CV, syllables/word, sentence-length stats, and
  parallelism density, plus sentence-level red-line markers
  (SLURRY / POUNDING / ROBOTIC / DENSE / FLAT). Standard library only.
- `references/prosody_target_card.md` — Step 9 method: the rhythm-and-density
  target card (bands, red-line markers, the adjust-and-re-run loop) and its
  caveats. Thresholds **re-validated on a 9-paper era-stratified corpus** (4
  pre-2020 + 5 papers 2021+; the two eras are statistically indistinguishable on
  every metric).
- `scripts/scan_detectability.py` — **new** Step 8 detector-facing false-positive-risk
  scanner. Measures six published statistical proxies that commercial AI detectors
  actually score (burstiness / sentence-length CV%, formulaic density,
  self-repetition %, MTLD, hedge density, paragraph-shape CV%) and reports a
  `risk_index`. Bands are era-stratified (pre-2020 vs 2021+ corpus). The script
  carries an explicit **honesty boundary: a diagnostic, not a detector; never
  optimised as a target**. 30 self-test assertions.

### Documentation
- `README.md`: new **References** section listing the scholarship the method borrows
  from — rhythm metrics (Grabe & Low 2002; Ramus et al. 1999; Dellwo 2006), lexical
  diversity (McCarthy & Jarvis 2010), formulaic language (Biber et al. 1999; Wray
  2002), hedging (Hyland 1998), AI-text detection (Tian 2023; Sadasivan et al. 2023;
  Liang et al. 2023; Weber-Wulff et al. 2023), and the causal-inference canon
  (Angrist & Pischke 2009; Imbens & Angrist 1994; Hahn et al. 2001; Rosenbaum & Rubin
  1983; Roth et al. 2023). Inline author-year citations now sit at each borrowed
  metric or claim. The section also states what is *not* borrowed: the trace lists,
  register bands, and target numbers are this skill's own compilation and
  calibration, not published results.
### Changed
- **README rewritten around the writing guidance.** New *Writing guidance (1.2)* section explains the two references, the tag system (`[Source]` / `[Practice]` / `[House style]`), the three source-check corrections, and the provenance rule: the six handouts are cited, never redistributed. The reference table now lists six files; the bibliography gains a *Writing guidance* group with nine entries (six local handouts, three external: Cochrane, Shapiro, AEA style guide); the licence note states the handouts are outside the MIT grant.


- **Writing references rewritten in English and re-verified.** `econ_writing_rules.md` and `phrase_bank.md` are now English, and every rule carries a source tag that distinguishes a paraphrase of a specific handout from general field practice. Three claims were corrected after checking the full texts: (a) the Harvard guide presents "This paper studies" as an example of direct voice, so it is no longer listed as an error; (b) Bellemare explicitly recommends a roadmap, so the rule now limits its placement rather than telling writers to omit it; (c) Dudenhefer offers "Table 1 shows..." as the model table sentence, so it is no longer banned.


- **Writing-tutorial library wired in.** New `references/econ_writing_rules.md` (32 rules distilled from Bellemare 2020, Dudenhefer 2009, Gordon n.d., Powers 2012, Nikolov 2020, Neugeboren & Jacobson) and `references/phrase_bank.md` (sentence patterns by function). Step 4 now opens by loading both; every rule hit is logged in Block B by rule number.


- **Step 8 extracted to `econtone-ai-trace`.** The three scanners and
  `references/anti_ai_trace_audit.md` moved out; Step 7 now hands Block A to that gate.
- **Step 4 and Step 5 merged into one diction step**: terminology first, register second, then
  connectives and adverbs. Added `scripts/terminology_check.py`, which reads the *avoid* column of
  `references/terminology.md` and reports banned variants, acronyms without a first-mention
  expansion, and mixed-script leaks.
- **Renumbered**: Step 6 → 5 (two blocks), Step 7 → 6 (journal), Steps 8–9 → 7 and 8 (hand-offs).
- **Precedence recorded**: the prosody gate ranks below terminology and below the trace pass, so it
  may not swap a canonical term for a shorter synonym or reintroduce a removed trace.
- Ships four reference files and one script; README rebuilt around the three-member pack.

- **Renamed and split (EconTone pack).** `top-journal-polish` is now `econtone-polish`,
  and the Step 9 rhythm gate is its own skill, `econtone-prosody`.
  `scripts/prosody_check.py` and `references/prosody_target_card.md` moved there, so the
  gate is the single source of truth for its bands, its checker, and its exit gate.
- **Step 9 is now a hand-off, not a stage.** Offer `econtone-prosody` when Block A is
  English and holds two or more sentences; run it after Step 8 (never before, it moves
  sentence boundaries); if the user declines, say the gate was not run and do not imply
  it passed.
- This skill now ships five reference files and three scripts; the README, the workflow
  table, the project structure, and the self-test block were updated to match.


- Step 8 now opens with the programmatic pre-scan: run both scanners, take a
  baseline **before** editing, re-measure afterwards, and deliver a
  before/after delta table. Three governing rules added: density is the signal
  rather than presence; a falling sentence-length stdev is not by itself
  success; the pass is a style pass and must not touch content.
- `### Reference Files` now lists `references/anti_ai_trace_audit.md`, and a new
  `## Scripts` section documents all three tools.
- `references/anti_ai_trace_audit.md` gains **§3b Detector-facing proxies** with the
  proxy table, the five-point honesty boundary, and the era-stratified calibration
  table (OLD vs NEW medians). The Step 8 baseline now runs all three scanners and
  the §6 delta table adds the detector-proxy rows.
- **Prosody card correction (Step 9):** `cv_words_per_sentence` was rewarding
  uniformity and flagging every real top-journal paper (CV 55–88%) as WARN. The
  band is flipped to reward variation (**OK ≥ 50%, RED < 35%**) — it is the same
  quantity detectors call "burstiness", so high CV is now the human-like target on
  both gates. `p95_words_per_sentence` loosened (RED only > 95, was > 60) and
  `mean_words_per_sentence` widened to 22–35. Calibration-lock assertions added to
  `prosody_check.py` (24/24) and `scan_detectability.py` (30/30) selftests.
- README: Features table gains a *Measured anti-AI audit* row; Project structure
  updated.
- New **Step 9 — Prosody Polish**: runs after Step 8 (AI-trace reflection) and
  before delivery as the final quantitative rhythm-and-density gate. Scoped to
  **paragraph-level or longer** tasks only (skipped for single-sentence requests
  and for `TR-EN2ZH`, since the checker measures English phonology).

- **Block-B timing resolved:** Step 6 now produces the *draft* of Blocks A and B and
  adds a **Finalizing the blocks** rule — after the Step 8/9 passes, every
  `修改后 / Revised` cell is re-synced to the delivered text, reverted rows are
  dropped, and Step 8/9 self-corrections fold into existing rows instead of adding
  meta rows. Step 6 renamed to "Produce the Two Blocks".
- **Anti-Patterns table de-duplicated:** the 11 rows that restated the Step 8
  checklists (dashes, explanatory colons, transition pegs, `respectively`,
  `thereby`, literary/journalistic diction, and the Chinese punctuation rows) are
  removed; the section keeps the 10 patterns that Step 8 and Step 5 do not cover,
  behind a one-line pointer.
- `scripts/prosody_check.py`: the verdict ignored sentence-level red-line markers. A
  paragraph could print `VERDICT: PASS (RED=0, WARN=0)` while a `[SLURRY]` marker fired
  in the same report, and the "fix RED markers first" line was suppressed. The verdict
  is now `REVISE` whenever any SLURRY / POUNDING / ROBOTIC / DENSE / FLAT marker fires,
  even with every banded metric OK; the human-readable line also reports `MARKERS=n` and
  the JSON payload gains `n_markers`. Three self-test assertions lock the behaviour
  (27/27). `references/prosody_target_card.md` now states that a marker is blocking.
### Fixed
- `scripts/*.py`: force UTF-8 on `stdout`/`stderr`. On a zh-CN Windows the
  interpreter defaults to the legacy ANSI code page (GBK), so every report line
  containing `—`, `–`, or CJK text reached a UTF-8 consumer as replacement
  glyphs. All four scripts now reconfigure their streams before printing;
  `selftest` still passes (prosody 24/24, detectability 30/30).
- `scripts/scan_detectability.py`: the CLI help advertised `'='` as the stdin
  marker while the code (like the other three scripts) accepts `-`. Help fixed.
- `scripts/prosody_check.py`: the usage comment advertised 17 assertions; the
  suite contains 24.
- `SKILL.md` Step 8: "Two scripts do the measuring" while three were listed.

### Design notes
- Both scripts are standard library only, read-only, with no network access and
  no subprocess. Input accepts `.tex` (preamble, floats, tables, and display
  maths stripped), `.md` (code fences and tables stripped), and plain text;
  `-` reads stdin. `--json` emits machine-readable output.
- English and Chinese are both supported. Latin prose is measured in words;
  Chinese prose is measured in characters (CJK ideographs plus Latin tokens),
  and the long-sentence default rises from 45 words to 60 characters, because
  word-counting a CJK sentence counts clauses rather than length.
- Citation commands are replaced by a **capitalised** placeholder before
  sentence segmentation. Unwrapping them to bare author keys leaves a
  lower-case token at the start of a sentence, which defeats the splitter and
  manufactures phantom long sentences.
- Known limitation, documented in the reference: display equations and float
  bodies are stripped before segmentation, so a sentence ending immediately
  before a display and the one beginning immediately after it can be measured
  as a single sentence. Boundary artefacts must be discounted by hand.
