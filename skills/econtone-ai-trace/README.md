# econtone-ai-trace

**English** | [中文](README.zh.md)

### The measured anti-AI-trace pass: three scanners, one before/after table

Part of the **EconTone** pack. Runs between the two other members:
`econtone-polish` drafts → **`econtone-ai-trace`** cleans the voice → `econtone-prosody` gates the rhythm.

## What it does

Three standard-library scanners measure what a read-through judges by feel:

| Scanner | Measures |
|---|---|
| `scan_ai_traces.py` | punctuation traces, transition-peg density, repeated syntactic templates, long-sentence load, sentence-length rhythm |
| `scan_register.py` | diction: defect bands (hype, ornate, assertive filler, over-assertive verbs, AI emphasis adverbs, wordy nominalisation) and context bands |
| `scan_detectability.py` | detector-facing proxies: burstiness, formulaic density, self-repetition, MTLD, hedge density, paragraph shape, and a `risk_index` |

The pass is a **measured loop**: baseline → triage → rewrite → re-measure → verify rhythm. The deliverable
is a before/after delta table, not an assertion that the text "sounds more human".

**Honesty boundary.** `risk_index` is a false-positive-risk diagnostic, **not** a detector, and must never
be optimised as a target. Density is the signal, not presence: `respectively`, `rather than` and an
explanatory colon are legitimate journal prose.

## Files

- `scripts/scan_ai_traces.py`, `scripts/scan_register.py`, `scripts/scan_detectability.py`
- `references/anti_ai_trace_audit.md` — the five-stage method, thresholds, trace-to-fix mapping, pitfalls,
  and the delta-table format

## References

The detector-facing proxies are the ones the commercial-detection literature and the tools it studies
actually score; the *thresholds and the composition of `risk_index` are this skill's own* and are not
reported in these papers.

- Liang, W., Yuksekgonul, M., Mao, Y., Wu, E., & Zou, J. (2023). GPT detectors are biased against
  non-native English writers. *Patterns*, 4(7), 100779.
- Sadasivan, V. S., Kumar, A., Balasubramanian, S., Wang, W., & Feizi, S. (2023). Can AI-generated text
  be reliably detected? *arXiv preprint* arXiv:2303.11156.
- Tian, E. (2023). *GPTZero* [software]. https://gptzero.me
- Weber-Wulff, D., Anohina-Naumeca, A., Bjelobaba, S., Foltýnek, T., Guerrero-Dib, J., Popoola, O.,
  Šigut, P., & Waddington, L. (2023). Testing of detection tools for AI-generated text.
  *International Journal for Educational Integrity*, 19(1).
  https://doi.org/10.1007/s40979-023-00146-z

The lexical-diversity and formulaic-language measures come from:

- Biber, D., Johansson, S., Leech, G., Conrad, S., & Finegan, E. (1999). *Longman Grammar of Spoken and
  Written English*. Longman.
- McCarthy, P. M., & Jarvis, S. (2010). MTLD, vocd-D, and HD-D: A validation study of sophisticated
  approaches to lexical diversity assessment. *Behavior Research Methods*, 42(2), 381–392.
- Wray, A. (2002). *Formulaic Language and the Lexicon*. Cambridge University Press.

Hedging is measured here as *hedge density*; its use as a **register** decision (calibrating a claim to
the evidence) belongs to `econtone-polish`, which cites the same source:

- Hyland, K. (1998). *Hedging in Scientific Research Articles*. John Benjamins.

## Licence

MIT. The reference corpus behind the era-stratified bands is described in
`references/anti_ai_trace_audit.md`; the papers themselves are not redistributed.
