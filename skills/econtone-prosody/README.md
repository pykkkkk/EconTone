# econtone-prosody

**English** | [中文](README.zh.md)

### The rhythm gate: nine banded metrics, five sentence-level red-line markers

Part of the **EconTone** pack. Runs last: `econtone-polish` drafts → `econtone-ai-trace` strips traces →
**`econtone-prosody`** measures how the finished English reads aloud.

## What it measures

| Metric | Companion |
|---|---|
| nPVI (normalised pairwise variability of stress) | stress contrast across the paragraph |
| % stressed syllables | content vs function load |
| alternation rate | mechanical, metronomic beat |
| inter-stress CV | spacing between stresses |
| syllables / word | lexical weight |
| mean, p95 and CV of words per sentence | syntactic density and rhythm variation |
| parallelism per 100 words | density of `and/but/or/;` |

Five markers name the offending sentence: **SLURRY**, **POUNDING**, **ROBOTIC**, **DENSE**, **FLAT**.
A marker is blocking: any marker forces `REVISE`, even when all nine bands read OK.

Two stress engines are supported. CMUdict is used when `nltk` and its `cmudict` corpus are importable;
otherwise the checker falls back silently to a built-in lexicon plus a first-syllable heuristic. The
report always prints which engine ran, and each engine has its own band set, because CMUdict marks
secondary stress and the heuristic does not.

## Files

- `scripts/prosody_check.py` — the checker (standard library only; `--profile body|abstract|intro`,
  `--json`, `--text`, `--no-cmu`, `selftest`)
- `references/prosody_target_card.md` — derivations, marker definitions, the adjust-and-re-run loop
- `tests/fixtures.json`, `tests/run_fixtures.py` — golden regression: four published paragraphs that
  must PASS, three constructed paragraphs that must REVISE

## References

The **metric definitions** come from the speech-rhythm literature below. The **bands, the marker
thresholds and the calibration corpus are this skill's own work** and are not results reported in
these papers: 42 open-access economics / finance / management papers (2016–2021, eight per year,
first author at a world-top department), 42 abstracts, 42 introductions and 794 body paragraphs. The
comfort band is the 10th–90th percentile of that corpus; the red lines sit beyond its tail.

- Dellwo, V. (2006). Rhythm and speech rate: A variation coefficient for ΔC. In P. Karnowski &
  I. Szigeti (Eds.), *Language and Language Processing* (pp. 231–241). Peter Lang.
- Grabe, E., & Low, E. L. (2002). Durational variability in speech and the rhythm class hypothesis.
  In C. Gussenhoven & N. Warner (Eds.), *Laboratory Phonology 7* (pp. 515–546). Mouton de Gruyter.
  https://doi.org/10.1515/9783110197105.515
- Ramus, F., Nespor, M., & Mehler, J. (1999). Correlates of linguistic rhythm in the speech signal.
  *Cognition*, 73(3), 265–292.

Two further sources inform the *interpretation*, not the metrics:

- Tian, E. (2023). *GPTZero* [software]. https://gptzero.me — the name and framing of "burstiness",
  which is the same quantity this skill reports as `cv_words_per_sentence`.
- McCarthy, P. M., & Jarvis, S. (2010). MTLD, vocd-D, and HD-D: A validation study of sophisticated
  approaches to lexical diversity assessment. *Behavior Research Methods*, 42(2), 381–392. — used by
  the sibling `econtone-ai-trace` scanner, not by this gate.

## Licence

MIT. The calibration corpus is not redistributed: only aggregate percentiles are published here.
