# econtone-score

### The triage gate: a four-row scorecard and an editing latitude

Part of the **EconTone** pack. Runs first, edits nothing:
`econtone-score` → `econtone-polish` → `econtone-prosody` → `econtone-ai-trace`.

## What it does

Four rows, weighted **40 / 40 / 10 / 10**:

| Row | Owner | What it counts |
|---|---|---|
| **P1** Terminology & register | `econtone-polish` | banned glossary variants; register defect hits |
| **P2** Claims & structure | `econtone-polish` | causal verbs with no identification language; significance with no magnitude; no stated design |
| **T1** AI-trace risk | `econtone-ai-trace` | `risk_index` from the detector-proxy scanner |
| **R1** Rhythm | `econtone-prosody` | verdict, red markers, WARN count |

The total sets the **editing latitude** — how hard the downstream members may press:

```
1.00 | *****************************
0.75 |                                     **
0.50 |                                           *
0.25 |                                               *
0.00 |                                                   *
     + ---------------------------------------------------
         0                        50                       100
```

| total | latitude | the editors may |
|---|---|---|
| ≤ 50 | 100–71% | restructure, cut, re-order — never changing the meaning |
| 50–75 | 71–50% | fix what is wrong; no restructuring |
| 75–90 | 50–16% | corrections only: errors, terminology, overclaims |
| > 90 | < 16% | only outright errors |

## It does not route

There are no thresholds and no "skip polish" branch: every draft runs the full pipeline. The score is an
orientation aid for how much latitude to take, not a gate. And it never edits: no revised text, no
sentence-level suggestions.

## Usage

```bash
python scripts/score.py DRAFT.md
python scripts/score.py DRAFT.md --profile abstract --json
```

`--profile body|abstract|intro` selects the rhythm band set. A row whose scanner is missing prints `n/a`
and is excluded from the total.

## Files

- `scripts/score.py` — standard library only, read-only, no network; calls the sibling scanners when they
  are installed and falls back to `n/a` when they are not.

## Honesty

The thresholds are **provisional**: the deductions have not been calibrated on a labelled corpus the way
the prosody bands were. They are deliberately generous toward routing drafts into `econtone-polish`, so a
high latitude is permission with a caveat, not an instruction to rewrite.

## Licence

MIT.
