# Prompting guide

> 中文版 / Chinese version: [`prompting-zh.md`](prompting-zh.md)

How to ask EconTone for what you want, and how to tell when you are asking for the wrong thing.

The five skills are not a single button. Each one accepts a different kind of request and returns a
different kind of answer; a prompt that works for `econtone-prosody` will waste `econtone-polish`. This
guide is organised around that fact.

---

## 1. What each skill expects

| Skill | Give it | It gives back | Don't ask it for |
|---|---|---|---|
| `econtone-score` | a draft and the target journal | four-row scorecard, total, editing latitude | rewrites — it never edits |
| `econtone-polish` | text plus the intended claim | revised text, a change log, `[MAGNITUDE?]` marks | numbers you did not measure |
| `econtone-ai-trace` | a text that "reads like AI" | before/after metrics and a rewrite | a guarantee that a detector will pass you |
| `econtone-prosody` | a passage that is hard to read aloud | boundary moves only, plus metrics | word changes — it may not touch content |
| `econtone-equilibrium` | two or more candidate versions | the winning combination and why the others lost | a vote or a preference ranking |

---

## 2. Three ways to invoke a skill

**Name it.** Most reliable, and the only way to be sure which one runs.

> Use `econtone-polish` on this paragraph. Target: *Journal of Development Economics*.

**Describe the job.** The description is written so that ordinary language lands on the right skill.

> This section reads like it was written by a machine. Clean it up and show me the before/after numbers.

**Paste and state an intent.** Short texts often route on the verb alone.

> Make this abstract read better without changing any claim.

If two skills are plausible, name one. "Make it better" routes to `econtone-polish` by default, which is
usually what you want — but not when the problem is rhythm.

---

## 3. The four parts of a good prompt

```
[text]        what to work on — paste it, or name the file
[goal]        what "better" means here: the journal, the reader, the section
[constraints] what must not change: terms, numbers, claim strength, length
[context]     what the draft is for: abstract, referee response, grant pitch
```

**Say where the text sits.** "Abstract", "introduction", "Section 4" is not decoration: the rhythm bands
differ by section, and a body-calibrated band judges an abstract by the wrong ruler. One clause is enough:
*"this is the abstract, for Regional Science and Urban Economics"*.

A prompt missing `constraints` is the single most common cause of a bad result. Without them the polish
pass will smooth a hedge into a claim, and you will not notice until a referee does.

---

## 4. Templates

### Score first, edit second

> Score this abstract for an AER submission with `econtone-score`. I want the four rows, the total, and the
> editing latitude. Do not edit anything yet.

Use this when you do not know how much work the text needs. The latitude number tells you whether to ask for
a polish pass at all: at 34% the honest answer is "fix the errors", not "rewrite it".

### Polish with a hard constraint

> Polish this paragraph for *Management Science* with `econtone-polish`. Keep every term of art and every
> number exactly as written. If a claim has no magnitude, mark it `[MAGNITUDE?]` instead of inventing one.
> Show me a table of what changed and why.

### De-AI a passage

> This paragraph reads like AI output. Run `econtone-ai-trace`: give me the baseline metrics, rewrite it,
> then re-measure and show the delta. Do not split or merge sentences — that is a different pass.

### Fix rhythm without touching words

> This paragraph is hard to read aloud. Use `econtone-prosody` and move sentence boundaries only. If a split
> would push the text into a red-line marker, tell me and leave it alone.

### Choose between versions

> Here are two versions of the same paragraph. Run `econtone-equilibrium` and tell me which combination of
> moves is stable, which moves you rejected and why, and what I lose by taking the one you rejected.

### The full pipeline

> Run the whole pipeline on this section: score, then polish, then traces, then prosody, then the
> equilibrium. I want the final text, the equilibrium certificate, the list of actions, and the suggestions
> you rejected.

---

## 5. Bad prompts, and what to say instead

| Instead of | Say | Why |
|---|---|---|
| "Make this better" | "Polish for *JFE*; keep terms and numbers; mark missing magnitudes" | "better" has no constraint, so fluency wins |
| "Make it sound more natural" | "Reduce AI-trace risk; show the before/after metrics" | "natural" is not measurable; the scanners are |
| "Fix the flow" | "Fix rhythm; boundaries only; keep the words" | "flow" invites a rewrite that changes claims |
| "This is 90% done, just polish it" | "Score it first; if latitude is under 40%, fix errors only" | the latitude is the honest answer, not your estimate |
| "Add a number so it looks stronger" | "Mark the missing magnitude" | the tool will refuse; better to ask for the mark |
| "Make it undetectable" | "Reduce the measured proxies; tell me what remains" | no tool can promise a detector outcome |

---

## 6. Long documents

Section by section, with the score once at the top:

> Score the whole paper for an AER submission. Then polish Section 3 only, keeping my notation. We will do
> the rest one section at a time.

Do not ask for the equilibrium across a whole paper in one turn. The move set grows with the text, and the
certificate stops being readable long before it stops being correct.

---

## 7. What not to ask for

- **A number you did not measure.** The pack marks `[MAGNITUDE?]` on purpose. Asking it to fill the gap turns
  a writing tool into a fabrication tool.
- **A guarantee about AI detectors.** `risk_index` is an internal diagnostic built from published proxies.
  It is not a prediction of any commercial detector, and the skill says so.
- **A rewrite that changes the claim.** Claim strength is a hard constraint. If you want a stronger claim, say
  so explicitly — then it becomes an editorial decision you own, not a silent edit.
- **A vote.** The equilibrium is computed, not voted. If you want a preference ranking, you want a different
  tool.

---

## 8. Quick reference

```
need a number?          econtone-score      "score this for <journal>, no edits"
need better words?      econtone-polish     "polish for <journal>, keep terms and numbers"
need less AI?           econtone-ai-trace   "baseline, rewrite, re-measure, show delta"
need better cadence?    econtone-prosody    "boundaries only, report markers"
need to choose?         econtone-equilibrium "which combination is stable, what did you reject"
need all of it?         name all five, in order
```
