# First equilibrium measurements

Two texts, three execution skills, eight coalitions per text. Every number below was produced by the
scripts in this repository; nothing is estimated.

## The coalitions

Players: **P** = `econtone-polish`, **T** = `econtone-ai-trace`, **R** = `econtone-prosody`.
The text is the ESTP abstract (208 words, 8 sentences).

| Coalition | rhythm score | risk_index | scorecard total |
|---|---|---|---|
| `{}` (input) | 92.9 | 21.6 | 90 |
| `{P}` | 92.9 | 24.0 | 90 |
| `{T}` | 100.0 | 17.3 | 90 |
| `{R}` | 100.0 | 15.8 | 90 |
| `{P,T}` | 100.0 | 19.4 | 90 |
| `{P,R}` | 92.9 | 20.2 | 90 |
| `{T,R}` | 100.0 | 12.0 | 91 |
| `{P,T,R}` | 100.0 | 19.4 | 90 |

## Shapley on the scorecard: uninformative, and that is the finding

```
P  -0.33     T  +0.17     R  +0.17     total 0.00
```

The scorecard is a four-row composite that saturates: seven of the eight coalitions score exactly 90. A
value function with no resolution produces Shapley values that are arithmetic noise. **Any Shapley
analysis must first prove its value function discriminates.**

## Shapley on a diagnostic composite: v = rhythm score − risk_index

```
P  -5.53     T  +9.02     R  +5.82     total +9.30
```

Here the numbers separate. Three observations:

1. **Trace and rhythm carry the whole gain** (+14.84 between them) on this diagnostic.
2. **Polish scores negative** (−5.53). It is not a measurement error: polish raises `risk_index`
   (24.0 against the input's 21.6), and on top of `{T,R}` it lifts it from 12.0 to 19.4 while the rhythm
   score is already at 100.
3. **The all-three coalition is not the best combination**: `{T,R}` = 88.0, `{P,T,R}` = 80.6. Adding the
   leader *lowers* this composite by 7.4.

## Why point 2 is not an argument against polishing

The composite `rhythm − risk` omits the hard constraints. Polish is the only player that fixes
terminology and claim language — on this abstract it expands `AI`, repairs `instrumental variable
estimations`, hyphenates `inverted-U` and `industry–university–research`, and removes `promotional effect`.
Those gains are **not priceable** in a scalar without weights, and the design refuses to price them: validity
is a constraint, not a term in a sum.

So the correct reading is:

> Trace and prosody contribute +9.3 to the diagnostic composite; polish contributes −5.5 to it and is
> nevertheless mandatory, because it is the only player that acts on the hard constraint.

## The methodological consequence

**Shapley must be run inside a layer, not across the hard constraint.** Scalarising validity would require
weights, and the whole point of the lexicographic order is that no weight exists. A Shapley table that spans
validity therefore measures the wrong game — it rewards fluent prose and punishes correct terminology.

What is legitimate:

- Shapley over `{T, R}` for the diagnostic composite (both are measured, both are priceable).
- Shapley over wordings for the leader's own objective (P1/P2), if a finer validity measure is built.
- Reporting the leader's contribution as **a constraint satisfied**, not as points.

## Reproduce

```bash
python tools/coalitions.py          # builds the eight coalition texts and scores them
python tools/shapley_real.py        # rhythm + risk per coalition, then Shapley
```
