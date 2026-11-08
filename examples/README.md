# A complete run, start to finish

**English** | [中文](README.zh.md)

One abstract, four stages, every number below produced by the scripts in this repository. The draft is
**synthetic** — written for this example, belonging to no one's paper — and it was written to contain the
defects the pack exists to catch.

| Stage | File | Result |
|---|---|---|
| 1 · draft | [`stage-1-draft.md`](stage-1-draft.md) | 6 sentences, 108 words |
| 2 · score | [`stage-2-score.txt`](stage-2-score.txt) | **56 / 100**, editing latitude 98% |
| 3 · rhythm | [`stage-2-prosody.txt`](stage-2-prosody.txt) | ADJUST — 2 WARN, no red markers |
| 4 · traces | [`stage-2-ai-trace.txt`](stage-2-ai-trace.txt) | `risk_index` 50 |
| 5 · final | [`stage-5-final.md`](stage-5-final.md) | 6 sentences, 109 words |
| 6 · re-measure | [`stage-5-score.txt`](stage-5-score.txt) | **97 / 100**, latitude 9%; rhythm **PASS** |

## What the draft looked like

> In order to investigate the impact of minimum wage increases on youth employment in China, this paper
> utilizes provincial panel data from 2004 to 2019. We employ a fixed-effects model and find that minimum wage
> increases significantly reduce youth employment. It is worth noting that the effect is more pronounced for
> low-skilled workers. The mechanism is that firms substitute capital for labor when labor becomes more
> expensive. In addition, we conduct a series of robustness checks which confirm our findings. These results
> underscore the importance of flexible labor markets and offer important policy implications for developing
> countries, highlighting the transformative potential of minimum wage reform for inclusive growth.

## What the scorecard caught

```
P1 Terminology & register      24/40   2 banned variant(s); 1 register defect line(s)
P2 Claims & structure          18/40   3 causal verb(s), no identification language;
                                       1 significance claim(s) without a magnitude; no stated design
T1 AI-trace risk                5/10   risk_index 50
R1 Rhythm                       9/10   ADJUST: 0 RED, 0 marker(s), 2 WARN
TOTAL 56 / 100     EDITING LATITUDE 98%  [full]
```

A latitude of 98% is the point: at 56 the editors are allowed to restructure. At 97 they are not.

## The edits

| # | Draft | Final | Why |
|---|---|---|---|
| 1 | `In order to investigate` | `This paper asks whether` | filler opener; the question should be named |
| 2 | `utilizes` | `using` | banned variant |
| 3 | `the impact of X on Y` | `whether X are associated with Y` | causal claim with no design behind it |
| 4 | `We employ a fixed-effects model` | `a two-way fixed-effects model … clustered at the province level` | the design has to be stated, not gestured at |
| 5 | `significantly reduce` | `negative … at about [MAGNITUDE?] percentage points` | significance without a magnitude |
| 6 | `It is worth noting that` | — | filler, deleted |
| 7 | `The mechanism is that firms substitute capital` | `Whether the pattern reflects substitution … these data cannot answer` | a mechanism claim with no mechanism evidence |
| 8 | `a series of robustness checks which confirm` | — | "a series" is not a test; nothing to cite |
| 9 | `underscore the importance … transformative potential` | — | hype band, deleted |
| 10 | — | `We do not claim identification` | the sentence the draft was missing |

**[MAGNITUDE?] is deliberate.** The tool does not invent a coefficient the author never supplied; it marks
the gap and hands the decision back. A demo that filled in a number would be showing the opposite of how this
pack behaves.

## What the rhythm gate said

```
draft:  inter_stress_CV 40.6 WARN (43–54)   parallel_per100 1.9 WARN (2.8–6.8)   VERDICT ADJUST
final:  inter_stress_CV 47.4 OK             parallel_per100 3.7 OK             VERDICT PASS
```

## Reproduce it

From the repository root:

```bash
python skills/econtone-score/scripts/score.py     examples/stage-1-draft.md --profile abstract
python skills/econtone-prosody/scripts/prosody_check.py examples/stage-1-draft.md --profile abstract
python skills/econtone-ai-trace/scripts/scan_detectability.py examples/stage-1-draft.md
```

The `.txt` files in this folder are the verbatim stdout of those commands, captured once and committed so the
result can be checked without running anything.

## What this example does not show

- **The polish step is an editorial act, not a script.** Stages 2, 3, 4 and 6 are machine output; stage 5 is
  the edit a writer made in response to them. The numbers are measured, the prose is judged.
- **No magnitude was produced.** The draft never reported one, so the final says `[MAGNITUDE?]`.
- **A 97 is not "ready to submit".** The score sees whether the prose *claims* an identification, not whether
  the identification is right.
