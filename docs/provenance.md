# Provenance: what is ours, what is borrowed, and what that means for the licence

Short answer: **the code is ours, the methods are not ours, and the papers are not redistributed.** Those are
three different things, and only the first two are covered by the repository licence.

## 1. Code

Every script in this repository was written for this project. It is standard-library Python — no `nltk`, no
`numpy`, no `scipy`, no copied package internals, no vendored snippets. You can check the claim:

```bash
grep -rn "github.com\|stackoverflow\|^import \(numpy\|scipy\|pandas\|nltk\)" econtone-*/scripts
```

The CMUdict path is optional and only reads a corpus the user installs; when it is absent the checker falls back
to a built-in lexicon. No third-party code is shipped.

## 2. Methods

The metrics are not invented here, and they are cited:

| Metric | Source |
|---|---|
| nPVI, ΔC, %V | Grabe & Low (2002); Ramus, Nespor & Mehler (1999); Dellwo (2006) |
| MTLD | McCarthy & Jarvis (2010) |
| burstiness, formulaic density, hedge density | the detector literature: Liang et al. (2023); Sadasivan et al. (2023); Weber-Wulff et al. (2023) |

**Implementing a published formula is not copying it.** Copyright protects the expression of a paper — its prose,
its figures, its code if it ships one — not the arithmetic it describes. Writing our own implementation of nPVI
from the definition does not make this repository a derivative work of Grabe & Low.

What is *not* borrowed: the **thresholds**. The 10th–90th percentile bands, the five markers, the weights inside
`risk_index`, and the score deductions are this project's own calibration on its own corpus. They are not results
reported in the cited papers, and the papers are not responsible for them.

## 3. Text

- `econ_writing_rules.md` **paraphrases** six graduate writing guides. It quotes at most a short clause, in
  quotation marks, with the source named. The guides themselves are not in this repository.
- `phrase_bank.md` is **synthesised**: templates written to satisfy those rules, with an explicit use condition.
  It does not reproduce, and is not a line-by-line rewrite of, any handout.
- `terminology.md`, `word_choice.md`, `journal_styles.md` are original compilations.
- The calibration corpus is **not distributed**. Only aggregate percentiles and the list of outlets appear.

## 4. What the licence covers

The licence (Apache-2.0 for the code, CC0 1.0 for the prose) covers **this repository's code
and its own prose**. It cannot cover, and does not claim to cover:

- the cited papers and guides, which remain under their own copyright;
- the calibration corpus, which is not redistributed;
- the **name and mark**, which are not licensed by a software licence at all — see
  [`trademark-notes.md`](trademark-notes.md).

If you reuse this project, you inherit whatever obligations the works it cites impose. Our own prose asks nothing of you.

## 5. Honest limits

- "Written for this project" is a statement about authorship, not a guarantee of non-resemblance: two
  implementations of nPVI in Python will look alike because the formula is four lines long.
- If a future contributor adapts code from a package, that fact must be recorded here, and the package's licence
  respected. Nothing like that exists today.
