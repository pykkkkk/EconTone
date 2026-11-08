---
name: econtone-score
description: >
  Scores an English economics / management document against the same four checks the downstream
  EconTone skills run — terminology and register (econtone-polish), claim strength and structure
  (econtone-polish), AI-trace risk (econtone-ai-trace), rhythm (econtone-prosody) — and returns a
  weighted scorecard (40 / 40 / 10 / 10) plus an editing latitude that tells the editors how hard they may
  press. Scores only: it never edits the text and never suggests rewrites. Load when the user asks "is this ready", "score this draft", "what should I fix first",
  or before starting a polish run on existing text.
metadata:
  pack: econtone
  role: triage
---

# EconTone Score — the triage gate

The three downstream skills are thorough and expensive. This one is cheap and fast: it runs the same
four checks, simplified, and tells you which of them the draft actually needs.

## Hard boundary

**Score, do not edit.** Output is a four-row table, one overall number, and an editing latitude. No revised text,
no sentence-level suggestions, no "consider changing X to Y". If the user wants fixes, hand off to the
member that owns them.

## The scorecard (40 / 40 / 10 / 10 = 100)

Each row is a simplified version of what one downstream skill checks.

| # | Row | Owner | What it counts | Points |
|---|---|---|---|---|
| **P1** | Terminology & register | `econtone-polish` | banned glossary variants; register defect hits (hype, ornate, filler) | **40** |
| **P2** | Claims & structure | `econtone-polish` | causal verbs with no identification language; significance with no magnitude; no stated design | **40** |
| **T1** | AI-trace risk | `econtone-ai-trace` | `risk_index` from the detector-proxy scanner | **10** |
| **R1** | Rhythm | `econtone-prosody` | verdict, red markers, WARN count | **10** |

Scoring rule per row: start at full marks and deduct, then scale to the row's weight — the deductions are printed next to the score, so every
number is traceable to a scanner line. A row whose scanner is missing prints `n/a` and is excluded
from the total, and the latitude is computed from the rows that did run.

### What was deliberately left out

The full members check far more than this table does: 32 writing rules, 37 sentence patterns, nine
rhythm metrics, five markers, three trace scanners, seven detector proxies. **The scorecard is not a
summary of those; it is a filter.** If a row scores low, run that member and let it do the detailed
work.

## No routing: the pipeline always runs

**The score does not dispatch.** There are no thresholds and no "skip polish" branch. Every draft
goes through the whole pipeline - polish, then prosody, then the final trace check - because the
score is an orientation aid, not a gate. What the score changes is **how hard the editors press**,
which is the next section.

## How hard to edit

The total feeds an *editing latitude*: how much the downstream members may touch.

```
editing latitude
1.00 | *****************************                      
0.95 |                              ***                   
0.90 |                                 **                 
0.85 |                                  **                
0.80 |                                    *               
0.75 |                                     **             
0.70 |                                       *            
0.65 |                                        *           
0.60 |                                         *          
0.55 |                                          *         
0.50 |                                           *        
0.45 |                                            *       
0.40 |                                            *       
0.35 |                                             *      
0.30 |                                              *     
0.25 |                                               *    
0.20 |                                                *   
0.15 |                                                 *  
0.10 |                                                 *  
0.05 |                                                  * 
0.00 |                                                   *
     + ---------------------------------------------------
       0                        5                        1
         0                        50                       100
```

Reading it:

| total | latitude | what the editors may do |
|---|---|---|
| ≤ 50 | 100–71% | restructure, cut, re-order - never changing the meaning |
| 50–75 | 71–50% | fix what is wrong; no restructuring; keep sentences that work |
| 75–90 | 50–16% | corrections only: errors, terminology, claims that overstate the design |
| > 90 | < 16% | only outright errors; change nothing else, even if it could read better |

Two rules sit above the curve:

1. **Meaning is invariant.** No edit may change what the author claims, hedges, or concludes. When a
   fix requires a different claim, stop and flag it; do not rewrite the claim.
2. **A high score buys restraint, not silence.** Even at 95 the editors fix errors; they just stop
   there. Editing for the sake of being seen is a defect, not diligence.

## Procedure

1. Read the file (read-only). Nothing is written.
2. Pick the profile — `body` (default), `abstract`, `intro` — rhythm bands depend on it.
3. Run:

```bash
python scripts/score.py DRAFT.md
python scripts/score.py DRAFT.md --profile abstract --json
```

4. Report the table, the latitude band, and the two lowest rows. Stop.

## Output

```
EconTone score - draft.md (profile: abstract)
  P1 Terminology & register      34/40   1 banned variant(s)
  P2 Claims & structure          27/40   1 causal verb(s), no identification language; no stated design
  T1 AI-trace risk                6/10   risk_index 40 (moderate)
  R1 Rhythm                       8/10   ADJUST: 0 RED, 0 markers, 5 WARN
  --------------------------------------------------------------
  TOTAL 75 / 100   (rows with n/a are excluded)
  EDITING LATITUDE 71%  [minimal]
  corrections only: errors, terminology, claims that overstate the design; no stylistic rewriting
  (orientation only - nothing was modified; the full pipeline still runs)
```

## Honesty

- A score is a diagnostic, not a verdict on publishability: it sees whether the prose *claims* an
  identification, not whether the identification is right.
- **The latitude curve is a design choice, not a measurement.** It says how much *may* be touched, not how
  much *should* be. A generous scorer hands out latitude too easily: the deductions have not been calibrated
  on a labelled corpus the way the prosody bands were. Until they are, treat a high latitude as permission
  with a caveat, not as an instruction to rewrite.
