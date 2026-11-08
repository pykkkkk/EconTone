# econtone-polish

### Publication-grade translation and polish for economics, management, and quantitative social science

Part of the **EconTone** pack. Drafts and polishes English (and translates 中文 ↔ English) to the
editorial conventions of AER, QJE, JPE, Econometrica, Management Science, JFE, JEEA and REStud.
Two optional gates sit in sibling skills: `econtone-ai-trace` (anti-AI-trace pass) and
`econtone-prosody` (rhythm gate).

---

## What it does

1. **Identifies the task** — `TR-ZH2EN`, `TR-EN2ZH`, or `PO-EN`.
2. **Classifies the segment** — abstract, introduction, identification, results, robustness,
   mechanism, conclusion — and applies segment-specific conventions.
3. **Fact-checks causal claims** against the bundled `causal_facts.md` *before* touching wording.
4. **Enforces diction** — canonical terms from a 135-pair glossary, neutral register, and a
   connective/adverb pass — then runs the **writing rules** distilled from the economics
   writing-guidance library and checks the draft against the **phrase bank**.
5. **Produces two blocks** — Block A (clean text) and Block B (a revision table with a stated
   rationale for every change).
6. **Adapts to a named journal** — AER ≠ QJE ≠ Econometrica voice.

| Step | Action | Guard |
|---|---|---|
| **1** | Identify task type | — |
| **2** | Classify the segment | — |
| **3** | Fact-check causal claims against `causal_facts.md` | Never alters intended meaning; writes a *Substantive Check* row |
| **4** | Enforce diction (terms → register → connectives), run `terminology_check.py`, apply the 32 writing rules | A checker hit is a candidate, not a verdict; every rule fix is logged by rule number |
| **5** | Produce Block A + Block B | Fixed two-block output; Block B re-synced after the gates |
| **6** | Layer journal style (if named) | — |
| **7** | Hand-off to `econtone-ai-trace` | Optional; style pass only |
| **8** | Hand-off to `econtone-prosody` | Optional; ranks below terminology and the trace pass |

## The pack

| Member | Role | Takes |
|---|---|---|
| `econtone-polish` | drafting | raw text → Blocks A + B |
| `econtone-ai-trace` | gate | a draft → trace baseline, rewrites, before/after delta table |
| `econtone-prosody` | gate | a draft → nine banded metrics, five markers, verdict |

**Precedence**: terminology > AI-trace > prosody. A rhythm fix may never replace a canonical term or
reintroduce a trace the previous pass removed; when nothing else is left, the gate waives the item.

## Writing guidance (new in 1.2)

Two references turn the field's writing advice into checks.

| File | What it is |
|---|---|
| `references/econ_writing_rules.md` | **32 rules** in eight groups — causal language, sentences, title/abstract, introduction, data, results, conclusion, common errors |
| `references/phrase_bank.md` | **37 sentence patterns** by rhetorical function — positioning, identification, data, results, mechanism, robustness, limitations, policy, transitions |

**How the rules are tagged.** Every rule carries a source tag, and the tags are not interchangeable:

- `[Bellemare 2020]`, `[Dudenhefer 2014]`, `[Harvard 2001/2014]`, `[Gordon n.d.]`, `[Nikolov 2020]`,
  `[Powers 2012]` — the rule paraphrases something that handout actually says, checked against the
  full text.
- `[Practice]` — standard practice in the field (effect-type reporting, clustering) that **these
  handouts do not state**; it is not attributed to them.
- `[House style]` — this skill's own preference, open to override.

Three early drafts were corrected after checking the sources, and the corrections are part of the
record: the Harvard guide presents "This paper studies" as an example of *direct voice* rather than
an error; Bellemare explicitly recommends a roadmap; Dudenhefer offers "Table 1 shows…" as the model
table sentence.

**The phrase bank is synthesised, not quoted.** Each pattern is a template built to satisfy the
rules, with an explicit *use condition*; it is not copied from, or line-by-line paraphrased out of,
any handout. A pattern whose condition fails is wrong even if it reads well.

**Provenance and reuse.** The six handouts behind these files are course materials and working
papers held locally for study. They are **not redistributed** with this skill: the reference files
carry citations only, the phrase bank carries no quotation, and the rules are paraphrase. Anyone
reusing this material should obtain the originals from their authors and cite them as below.

## Reference files

| File | Purpose |
|---|---|
| `references/terminology.md` | 12 categories, 135 canonical EN↔ZH pairs with an explicit *avoid* column |
| `references/causal_facts.md` | Self-contained causal-inference facts for the Step 3 fact-check |
| `references/causal_mixtape.md` | Design-by-design notes from Cunningham's *Mixtape*: assumption, what to report, the overclaim to catch |
| `references/word_choice.md` | Neutral three-band register, intensity spectra, reporting verbs, hedging |
| `references/journal_styles.md` | Per-outlet voice, structure, and prohibited patterns (8 outlets) |
| `references/econ_writing_rules.md` | 32 executable writing rules, each tagged with its source or marked as practice |
| `references/phrase_bank.md` | 37 sentence templates by function, each with a use condition |

## Scripts

`scripts/terminology_check.py <file> [--json] [--lang en|zh] [selftest]` — parses the glossary and
reports banned variants, acronyms used without a first-mention expansion, and mixed-script leaks.
Standard library only, read-only, no network. Five self-test assertions.

```bash
python scripts/terminology_check.py DRAFT.md
python scripts/terminology_check.py DRAFT.md --json
```

## Quality standards

- **Zero Chinglish** — no SVO inversion, over-nominalization, or literal conjunction translation.
- **Calibrated hedging** — *consistent with* / *suggests* / *provides evidence that* / *establishes*,
  matched to evidence strength.
- **Identification language** — descriptive ("is associated with") vs causal ("increases") never
  confused; causal verbs only when the design supports them.
- **Significance ≠ importance** — statistical significance separated from economic magnitude.
- **Neutral register** — no literary ornament, no journalistic hype, substitutions stay in band.
- **Rule-checked** — every Step 4 fix cites the rule number; a rule that cannot be met without new
  evidence is flagged (`[CITE?]`, `[MAGNITUDE?]`), never invented.

## Installation

A plain skill bundle: `SKILL.md` plus `references/` and `scripts/`.

```powershell
Copy-Item -Recurse econtone-polish "$env:USERPROFILE\.dsh\skills\"
Test-Path "$env:USERPROFILE\.dsh\skills\econtone-polish\SKILL.md"   # → True
```

The gates install the same way (`econtone-ai-trace`, `econtone-prosody`); the whole pack is three
sibling directories plus `econtone/` for the manifest.

## Usage

- *"把这段摘要翻译成 AER 风格英文"*
- *"Polish this introduction for QJE"*
- *"润色这段实证结果，然后跑一遍去 AI 痕"*
- *"Translate this paragraph back to Chinese for review"*

Trigger phrases: `翻译`, `润色`, `polish`, `translate`, `顶刊写作`, `改写`, `学术英语`, `摘要修改`,
`引言润色`, plus any named journal.

## Customization

- **Add a journal**: append a `[Journal]` section to `references/journal_styles.md`; Step 6 picks it up.
- **Extend terminology**: add rows to `references/terminology.md` and fill the *avoid* column — the
  checker reads that column directly, so a new banned variant is enforced the moment it is listed.
- **Extend word choice**: add words or spectra to `references/word_choice.md` §2–§3, keeping the
  neutral band in the middle column.
- **Add a writing rule**: append to `references/econ_writing_rules.md` with a tag — a citation, or
  `[Practice]`/`[House style]`. Never tag a rule with a source that does not support it.
- **Add a pattern**: append to `references/phrase_bank.md` with a use condition. A template without a
  condition is a trap.
- **Retune the gates**: the trace and prosody bands live in their own skills.

## Disclaimer

This skill improves writing and terminology; it does not constitute methodological advice and does
not guarantee acceptance. The author remains responsible for substance, identification, and
correctness.

---

## References

Citations in this file cover the **writing guidance** and the **causal-inference facts** this skill
uses directly. The prosody and detection literature moved with the split and is now maintained in the
sibling skills:

- rhythm metrics and the calibration corpus -> [`econtone-prosody/README.md`](../econtone-prosody/README.md)
- AI-text detection, lexical diversity, formulaic language -> [`econtone-ai-trace/README.md`](../econtone-ai-trace/README.md)

The trace lists, register bands and target numbers are this skill's own compilations, not results
reported in any of these papers. The writing rules paraphrase the sources in the first group; the
phrase bank quotes none of them.

**Writing guidance**

- Bellemare, M. F. (2020). *How to Write Applied Papers in Economics.* Working paper, 7 September
  2020.
- Cochrane, J. H. (n.d.). *Writing Tips for PhD Students.* https://www.johnhcochrane.com/
- Dudenhefer, P. (2014). *A Guide to Writing in Economics.* Duke University, Department of Economics
  (March 2014).
- Gordon, R. J. (n.d.). *Tips for Writing Papers and Some Common Mistakes to Avoid.* Economics 101-6,
  Northwestern University.
- Neugeboren, R., with Jacobson, M. (2001; rev. 2005, 2014). *Writing Economics: A Guide for Harvard
  Economics Concentrators.* Harvard University.
- Nikolov, P. (2020). *Writing Tips for Economics Research Papers.* 20 July 2020.
- Powers (2012). *Econ 191: Writing in Economics* [course handout], 17 January 2012. The handout does
  not print the author's full name; to be completed from the course record.
- Shapiro, J. M. (n.d.). *Four Steps to an Applied Micro Paper.*
  https://scholar.harvard.edu/files/shapiro/files/foursteps.pdf
- American Economic Association. *AEA Journals: Policies and Style Guide.*
  https://www.aeaweb.org/journals/policies

**Register and hedging**

- Hyland, K. (1998). *Hedging in Scientific Research Articles.* John Benjamins. Used here for the
  register ladder (Step 4); the same source is cited by `econtone-ai-trace` for hedge density.

**Causal inference and econometrics**

- Cunningham, S. (2021). *Causal Inference: The Mixtape.* Yale University Press.
  https://mixtape.scunning.com/ — source of the design-by-design notes in `references/causal_mixtape.md` (paraphrased, not reproduced).
- Angrist, J. D., & Pischke, J.-S. (2009). *Mostly Harmless Econometrics: An Empiricist's Companion.*
  Princeton University Press.
- Hahn, J., Todd, P., & van der Klaauw, W. (2001). Identification and estimation of treatment effects
  with a regression-discontinuity design. *Econometrica*, 69(1), 201-209.
- Imbens, G. W., & Angrist, J. D. (1994). Identification and estimation of local average treatment
  effects. *Econometrica*, 62(2), 467-475.
- Rosenbaum, P. R., & Rubin, D. B. (1983). The central role of the propensity score in observational
  studies for causal effects. *Biometrika*, 70(1), 41-55.
- Roth, J., Sant'Anna, P. H. C., Bilinski, A., & Poe, J. (2023). What's trending in
  difference-in-differences? A synthesis of the recent econometrics literature. *Journal of
  Econometrics*, 235(2), 2218-2244. https://doi.org/10.1016/j.jeconom.2023.03.008

---

## License

Released under the [MIT License](LICENSE). Free to use, modify, and redistribute.
The course handouts listed above are **not** covered by this licence and are not distributed with
the skill.
