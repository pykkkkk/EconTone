---
name: econtone-polish
description: >
  Top-journal academic translation and polish for economics, management, and
  quantitative social science: Chinese-English translation and English-only
  polish. Targets AER, QJE, JPE, Econometrica, MS, JFE, JEEA, REStud and
  comparable SSCI outlets. Enforces causal-inference / econometrics terminology
  and covers abstracts, introductions, results, robustness, mechanisms, and
  conclusions. Triggers include: 翻译, 润色, polish, translate, AER/QJE/MS
  writing, 顶刊改写, 学术英语, 实证写作, 摘要修改, 引言润色. (Formerly
  top-journal-polish / TJP; the gates now live in econtone-ai-trace and
  econtone-prosody.)
metadata:
  pack: econtone
  role: drafting
agent_created: true
---

# Top-Journal Academic Translation & Polish

## Purpose

Provide publication-grade translation and writing polish aligned with the editorial conventions of
AER, QJE, JPE, Econometrica, Management Science, JFE, JEEA, and REStud.
Covers Chinese ↔ English translation and English-only polish for empirical economics,
theoretical modeling, applied econometrics, and quantitative social-science manuscripts.

---

## Trigger Conditions

Load this skill when the user:
- Pastes Chinese or English text and asks for translation, polish, rewriting, or proofreading
- Mentions a target journal (AER, QJE, MS, JFE, etc.)
- Asks about academic phrasing, sentence structure, or terminology for economics / management papers
- Uses phrases such as 润色, 翻译, polish, translate, 顶刊写作, 改写, 学术英语

---

## Workflow

### Step 0 — Mechanical corrections (unconditional)

Spelling, US/UK consistency, and grammar are **errors, not choices**. Fix them first, before task typing,
before terminology, before anything else. They are never submitted to the equilibrium and never traded
away: a correction that fixes an error is applied whether or not it improves any metric.

```bash
python scripts/mechanical_check.py DRAFT.md          # report
python scripts/mechanical_check.py DRAFT.md --json
```

It reports: mixed US/UK spellings (a document must pick one column), misspellings, doubled words, spaces
before punctuation, `a`/`an` agreement, and LaTeX artefacts (`\par`, `` `` ``, `''`) left in prose.

Rules:
- **One spelling column per document.** If both appear, convert to the target journal's convention and
  say which one you converted to.
- **Every fix is logged** in Block B under *Mechanical*, with the token and the correction.
- **A grammar fix is never rejected** for raising a risk index or lowering a rhythm score. Those are
  diagnostics; a broken sentence is a defect.

**Grammar is not scripted.** `mechanical_check.py` judges spelling, US/UK consistency and mechanical
slips only — it does not judge agreement, tense, articles, or preposition use, and no regex will. That
judgement is yours, and it is still mandatory: read for grammar before touching anything else and fix every
error you find. Log it under *Mechanical* like the scripted fixes, with the sentence and the correction.
An error the script cannot see is still an error.

### Step 1 — Identify Task Type

Determine which of the three task types applies:

| Code | Task | Description |
|------|------|-------------|
| `TR-ZH2EN` | Chinese → English translation | Full translation with terminology alignment |
| `TR-EN2ZH` | English → Chinese translation | Technical back-translation for review purposes |
| `PO-EN` | English polish only | Style, logic, and terminology improvement |

If the user specifies a **target journal**, activate the journal-specific style rules in
`references/journal_styles.md` for that outlet.

---

### Step 2 — Classify Text Segment

Before polishing, classify the pasted segment:

- **Abstract** → dense, structured, 4–6 sentences: motivation / gap / method / main finding / implication
- **Introduction** → inverted-pyramid narrative; establish fact, identify gap, preview contribution, roadmap
- **Literature Review** → tight citation-linked comparisons; avoid long summaries
- **Theoretical Framework** → formal, compact; every assumption stated; notation consistent with standard field usage
- **Empirical Specification / Identification** → explicit identification strategy, data description, estimation equation
- **Results** → coefficient-centered; significance only when economically meaningful; avoid "significant at 5%"-only claims
- **Robustness / Placebo** → structured list of threats and responses; parallel construction
- **Mechanism / Heterogeneity** → causal channel logic; avoid "suggest" when evidence is direct
- **Conclusion** → mirror introduction; no new citations; policy implications scoped correctly
- **Other** → apply general top-journal prose standards

Load `references/terminology.md` for all task types.

---

### Step 2b — Scope: sentences are fixed

You may change words, syntax and punctuation **inside** a sentence. You may not split one sentence into
two, merge two into one, or reorder sentences: **sentence boundaries belong to `econtone-prosody`**, which
moves them without touching a word. If a fix only works by changing a boundary, record it in Block B as
`[BOUNDARY]` and hand it over — do not do it here.

### Step 3 — Fact-Check Claims Against Causal Inference Principles

Before applying terminology rules, verify the substantive correctness of the text's causal-inference claims. A translation or polish that is terminologically accurate but factually incorrect can mislead readers and undermine credibility.

**Procedure:**

1. **Identify the causal claim(s)** — Extract the core causal statements from the user's text (e.g., "X causes Y", "Z is a mediator/confounder/collider", "the identifying assumption is ...", "SUTVA is violated because ...").

2. **Verify against the bundled fact reference** — Load `references/causal_facts.md` and check each claim against the canonical principles listed there (potential outcomes & effect types §1, DAG primitives §2, identification-strategy assumptions §3, effect interpretation §4, inference caveats §5, and the error checklist §6). This file is **self-contained**: it requires no external textbook, connector, or private knowledge base.
   For the design-level cross-check — what each design identifies, what the paper must report, and the
   overclaim that design invites — load `references/causal_mixtape.md`.

3. **Add a "Substantive Check" row to Block B** — If the user's text contains a factual error or a misleading causal claim, add a row to the Revision Notes table with the following format:

   ```
   # | 用户原文 | [Corrected text] | Substantive Check: causal_facts.md §X states that [correct claim]. The user's statement [what was wrong]. [Corrected to ...]. |
   ```

   If the claim is correct, include a brief verification note (e.g., "Substantive Check: Confirmed — consistent with causal_facts.md §2 (DAG primitives)"). This demonstrates rigor and builds trust.

4. **Fallback** — If a claim is not explicitly covered by `causal_facts.md`, assess it with general causal-inference expertise (the agent's built-in knowledge). Note in Block B: "Substantive Check: Not found in causal_facts.md; verified against general causal-inference knowledge." Do not fabricate a citation to the reference file.

5. **Boundary rule** — Do NOT alter the user's original intended meaning or add content the user did not write. The fact-check step only flags *factual inaccuracies* in the text's causal claims (e.g., mistaking a collider for a mediator, claiming SUTVA holds when interference is clearly present, misstating an identifying assumption). It does not introduce new arguments.

---

### Step 4 — Enforce Diction: Terminology, Register, Word Choice

Two references drive this step: `references/econ_writing_rules.md` (32 rules distilled from the writing-tutorial library, each attributed to its source) and `references/phrase_bank.md` (sentence patterns by rhetorical function). Rules are checks, not suggestions: every hit you fix is logged in Block B with the rule number.

Wrong terminology and wrong register both read as "not an economist", so they are one step, run in
this order.

**4.1 Terms first.** Load `references/terminology.md` and honour its 禁止使用 / Avoid column.

- Use only the canonical form — never a textbook, domestic-journal, or colloquial variant.
- Resolve ambiguous words by domain: in a DAG context "部分" is *nodes* (not *parts*) and "路径" is
  *paths* (not *routes*).
- DID / PSM / RDD / IV / CDAG vocabulary takes the international standard form only
  (*parallel trends assumption*, not *parallel trend hypothesis*; *instrumental variables (IV)*
  *estimation*, not *instrumental variable method*).

**4.2 Register second.** Load `references/word_choice.md` and apply its three governing rules:
disciplinary priority, the neutral band, and intensity-matched substitution.

**4.3 Connectives and adverbs are diction too.** The words that most often betray a non-native or
machine voice are not nouns: `moreover`, `furthermore`, `importantly`, `notably`, `in particular`,
stacked `thus`, `respectively` closing a paired statement, `thereby + -ing`. Police them with the
same severity as a wrong technical term — and the same restraint: one occurrence is prose, four is
a tic.

**4.4 Run the checker, then fix every hit.**

```bash
python scripts/terminology_check.py DRAFT.md            # glossary + consistency report
python scripts/terminology_check.py DRAFT.md --json     # machine-readable
```

It reports three things: banned variants from the glossary, acronyms used without a first-mention
expansion, and mixed-script leaks (Chinese left inside an English draft). A hit is a candidate, not
a verdict: `DID` after the first-mention expansion is correct, and `the problem of` survives inside a
quotation. Read the line before changing it.

**4.5 Log every change** in Block B under **Terminology** or **Word choice / Register**, with the
intensity-matched alternative and a one-line reason.

---

### Step 4b — Editing latitude (how hard to press)

If `econtone-score` was run, its total sets the editing latitude. Without a score, assume **reduced**.

| total | latitude | what you may do |
|---|---|---|
| ≤ 50 | 100–71% | restructure, cut, re-order - never changing the meaning |
| 50–75 | 71–50% | fix what is wrong; no restructuring |
| 75–90 | 50–16% | corrections only: errors, terminology, overclaims |
| > 90 | < 16% | only outright errors |

**Meaning is invariant.** If a fix would change what the author claims, hedge, or conclude, stop and
flag it in Block B instead of rewriting. A high score buys restraint: at 90+ you may fix errors and
nothing else, even where the prose could be better.

### Step 5 — Produce the Two Blocks

Deliver **two clearly labeled blocks**. Draft both here; the Revision Notes are re-synced against the delivered text after the optional gates (see *Finalizing the blocks* below):

#### Block A — 【润色定稿版 / Polished Version】

Deliver the polished or translated text with no inline annotations.
- For `TR-ZH2EN`: produce fluent, native-level academic English
- For `TR-EN2ZH`: produce precise, natural Chinese that retains technical accuracy
- For `PO-EN`: produce a clean revised version ready for submission

#### Block B — 【修改备注 / Revision Notes】

Provide a structured comment table with the following columns:

| # | 原文片段 / Original | 修改后 / Revised | 修改依据 / Rationale |
|---|---------------------|-----------------|---------------------|

Rationale entries must specify:
- **Terminology**: why a specific term was chosen over alternatives
- **Word choice / Register**: which neutral-band or intensity-matched alternative was chosen and why
- **Sentence logic**: restructuring reason (passive → active, nominalization removed, etc.)
- **Journal convention**: citation to journal-specific convention where applicable
- **Causal language**: any upgrade from correlation language to identification language

**Finalizing the blocks.** Both blocks are drafted here and finalized at delivery, not frozen at this step. Once the AI-trace gate (`econtone-ai-trace`) or the prosody gate (`econtone-prosody`) has altered Block A:

1. Walk Block B row by row and make every `修改后 / Revised` cell match the delivered wording.
2. Drop any row whose change a later pass reverted.
3. Fold an AI-trace self-correction, or a prosody-gate edit, into the existing row it touches; never add a row that narrates "removed an AI trace" or "re-ran the prosody gate". A rewritten passage with no row of its own simply stays undocumented: Block B explains stylistic decisions, it does not audit the pipeline.
4. Keep Block B in the order of the delivered text, so the reader can follow Block A top to bottom.

---

### Step 6 — Journal-Specific Adaptation (if requested)

When the user names a target journal, apply the additional style rules from `references/journal_styles.md`.

Activate the relevant journal section:
- `[AER]` — American Economic Review
- `[QJE]` — Quarterly Journal of Economics
- `[JPE]` — Journal of Political Economy
- `[ECTA]` — Econometrica
- `[MS]` — Management Science
- `[JFE]` — Journal of Financial Economics
- `[JEEA]` — Journal of the European Economic Association
- `[REStud]` — Review of Economic Studies

---

### Step 7 — Hand-off to the prosody gate (optional)

`econtone-ai-trace` owns the measured anti-AI pass: three scanners, baseline → rewrite → re-measure,
and a before/after delta table. This skill ships no scanner of its own.

- **Offer it** when the user wants a submission-ready voice, or says the draft "reads like a model
  wrote it".
- **Order.** It is now the **final** check, after the prosody gate: run the trace pass last, and re-measure
  rhythm only if the trace fix changed sentence boundaries.
- **Scope.** A style pass only. Numbers, equations, citations, and exhibit content are out of scope.

---

### Step 8 — Hand-off to the prosody gate (optional)

`econtone-prosody` owns the rhythm-and-density gate: nine banded metrics, five sentence-level
red-line markers, the adjust-and-re-run loop, and the exit gate. This skill ships neither the
checker nor the target card.

- **When to offer it.** Block A is English and holds **two or more sentences** after body-prose
  cleaning. Single sentences and `TR-EN2ZH` output (Chinese) are out of scope.
- **How to invoke.** Hand `econtone-prosody` Block A as a file path; it returns a verdict and a
  before/after table.
- **Precedence — a constraint, not a preference.** The gate ranks **below** terminology and **below**
  the AI-trace pass. A rhythm fix must never (i) substitute a shorter synonym for a canonical term
  from `references/terminology.md`, or (ii) reintroduce a trace the Step 7 pass removed — stacked
  connectives, `respectively` padding, symmetrical clauses. When the only remaining fix would break
  either rule, record a waiver and leave the sentence alone.
- **If the user declines.** Say the gate was not run; never imply it passed.

---

## Quality Standards

### Language Quality
- Zero Chinglish constructions (subject-verb-object inversion, over-nominalization, literal conjunction translation)
- Consistent tense usage within sections (results in past tense; general claims in present tense)
- Hedging calibrated to evidence strength: "consistent with" / "suggests" / "provides evidence that" / "establishes"
- Avoid vague intensifiers: "very," "quite," "relatively," "obviously"
- Neutral register only: no literary/ornate diction and no journalistic hype (see `references/word_choice.md`)

### Identification Language
- Distinguish between descriptive patterns ("is associated with") and causal claims ("increases," "reduces")
- Only use causal language when the identification strategy supports it
- State identification assumptions explicitly in empirical sections

### Citation and Reference Style
- Do not alter citations; flag missing citation information with `[CITE?]`
- Journal acronym usage: spell out on first mention, abbreviate thereafter

### Equations and Notation
- Do not alter mathematical content
- Flag inconsistent notation with inline comment `[NOTATION: suggest unifying with ...]`

---

## Anti-Patterns to Fix

Correct these on sight. Punctuation, transition-peg, and diction traces are enumerated **once**, in the `econtone-ai-trace` checklists; literary and journalistic diction is governed by `references/word_choice.md` through Step 4. Only the patterns those sections do not cover are repeated here.

| Anti-pattern | Correction |
|---|---|
| "This paper studies..." | "This paper examines / investigates / estimates..." |
| "significant effect" (without magnitude) | Add coefficient size or elasticity |
| "As can be seen from Table X..." | "Table X reports..." or restructure to lead with finding |
| "In order to solve this problem..." | "To address this limitation..." |
| "The results show that A has a positive impact on B" | "A 1 SD increase in A is associated with a β-unit increase in B (p < 0.01)" |
| 混淆 "显著" 与 "重要" | 统计显著 → statistically significant; 经济重要 → economically meaningful |
| "We use DID method to study..." | "We exploit [exogenous variation / natural experiment] in a difference-in-differences framework..." |
| 直译 "平行趋势假设" → "parallel trend hypothesis" | → "parallel trends assumption" |
| 直译 "工具变量" → "instrumental variable method" | → "instrumental variables (IV) estimation" / "2SLS" |
| **"……的问题" 直译为 "the problem of ..."** | **删除 "the problem of"，直接陈述事实。中文"……的问题"为冗余口语表达，英译时删除不影响语义。例：**"资源错误分配的问题" → "misallocation of resources"（非 "the problem of misallocation of resources"）** |

## Reference Files

- `references/terminology.md` — Canonical causal-inference and econometrics terminology (EN ↔ ZH)
- `references/causal_facts.md` — Canonical causal-inference facts/principles for the Step 3 fact-check (self-contained; no external dependency)
- `references/causal_mixtape.md` — Design-by-design notes distilled from Cunningham's *Causal Inference: The Mixtape*: identifying assumption, what the paper must report, the overclaim to catch, and a copy-editing lookup table
- `references/word_choice.md` — Strict diction control: academic usage conventions, neutral three-band register, and intensity-matched synonym spectra
- `references/journal_styles.md` — Journal-specific style rules for AER, QJE, JPE, ECTA, MS, JFE, JEEA, REStud
- The AI-trace method reference moved to `econtone-ai-trace` (`references/anti_ai_trace_audit.md` there); this skill keeps no copy
- `references/econ_writing_rules.md` — 32 executable rules from the economics writing-tutorial library (causal language, nominalisation, sections, common errors), each tagged with its source
- `references/phrase_bank.md` — sentence patterns by function (contribution, identification, data, results, mechanism, robustness, limitations, policy), with use conditions
- The prosody gate's target card now lives in the sibling skill `econtone-prosody` (`references/prosody_target_card.md` there); this skill keeps no copy

## Scripts

Standard library only, read-only, no network, no subprocess. Input accepts `.tex`, `.md`, or plain text (`-` reads stdin).

- `scripts/terminology_check.py <file> [--json] [--lang en|zh] [selftest]` — Step 4 glossary and consistency checker: banned variants, acronyms used without first-mention expansion, and mixed-script leaks

The AI-trace scanners (`scan_ai_traces.py`, `scan_register.py`, `scan_detectability.py`) moved to `econtone-ai-trace`; the prosody checker moved to `econtone-prosody`.

