# Economics writing rules (distilled from the `writing-tutorial` library)

Every rule is a check, not a suggestion. Each carries a source tag; tags mean:

- **[Bellemare 2020]**, **[Dudenhefer 2009]**, **[Harvard 2001/2014]**, **[Gordon n.d.]**,
  **[Nikolov 2020]**, **[Powers 2012]** — the rule paraphrases something that source actually says.
  Verified against the full text in `writing-tutorial/_text/`.
- **[Practice]** — standard in the field (identification reporting, inference) but **not** attributed to these
  handouts, because they do not say it.
- **[House style]** — this skill's own preference; overridable by the user.

Nothing here is a verbatim quotation. Where a short phrase is quoted it appears in quotation marks with its source.

## 1. Causal language

1. Match the verb to the design. Without an identifying strategy, write `is associated with`, `predicts`,
   `covaries with`; reserve `increases / reduces / leads to` for designs that support it. **[Practice]**
2. Do not overclaim what the paper can do. Bellemare is blunt: "Do not lie about what your paper can and cannot
   do!" — if results are not causally identified, say so. **[Bellemare 2020]**
3. Report the effect type actually identified (ATE, ATT, LATE, ITT); a LATE is not an ATE. **[Practice]**
4. Pair every coefficient with an economic magnitude (SD change, percent, elasticity). A "significant" coefficient
   with no size is incomplete. **[Practice]**
5. State the identifying assumptions in the empirical-strategy section, not in a footnote. **[Practice]**

## 2. Sentences

6. Cut nominalisations: `the implementation of the evaluation of the program` → `evaluating the program`.
   Dudenhefer calls them noun forms of words that can also be verbs, and advises avoiding them. **[Dudenhefer 2009]**
7. Let actions be verbs: `conduct an analysis of` → `analyze`; `make an assessment of` → `assess`.
   **[Dudenhefer 2009]**
8. Avoid the passive voice, except where the agent is irrelevant. Bellemare: "the passive voice should be avoided".
   **[Bellemare 2020]**
9. Keep tense stable. Bellemare extends the same warning to tense: past tense is for summarising and concluding,
   not for general claims. **[Bellemare 2020]**
10. One paragraph, one claim: the first sentence states it, the rest supports it. **[Practice]**
11. Delete filler: `very`, `quite`, `it is worth noting that`, `needless to say`. **[Practice]**

## 3. Title and abstract

12. Titles should not begin with filler constructions; Bellemare recalls the advice that paper titles "should never
    start with" certain openers (e.g. "The Effects of…"). Keep the title on the mechanism or the finding.
    **[Bellemare 2020]**
13. The abstract carries problem, method, main result with magnitude, and implication. No literature review, no
    citations, no footnotes. **[Practice]** (the handouts describe the abstract's role but not this exact list)
14. The title, abstract and introduction are the parts most likely to change late in the project; budget revision
    time for them. **[Bellemare 2020]**

## 4. Introduction

15. Get to the contribution early; readers want it "sooner rather than later". **[Bellemare 2020]**
16. A roadmap is acceptable — Bellemare explicitly tells writers to provide the reader with one — but it is not
    where the contribution lives. Do not let it displace the contribution paragraph. **[Bellemare 2020]**
17. Motivate with a fact or a number, not an adjective. **[Practice]**
18. `This paper studies…` is grammatical and the Harvard guide uses it as an example of direct, active voice; it is
    not an error. Prefer a sharper verb (`examines`, `estimates`, `documents`) only when it adds information.
    **[Harvard 2001/2014]**

## 5. Data and descriptives

19. The data section answers three questions: where the data come from, what they cover, and why they fit this
    question. **[Practice]**
20. A descriptives table must be readable on its own: variable definitions, units, sample period, observation
    counts in the notes. **[Harvard 2001/2014]**
21. Say how sample restrictions affect external validity; do not file it under "data limitations" and move on.
    **[Practice]**

## 6. Results

22. Coefficient first, significance second. Reversing the order reads as "significance only". **[Practice]**
23. A table sentence should say what the table shows, e.g. "Table 1 shows the incomes earned by full-time
    workers" — Dudenhefer gives this as the model single sentence. **[Dudenhefer 2009]**
24. Robustness answers a named threat, one test per threat; it is not a list. **[Practice]**
25. The mechanism section explains a channel; it does not re-report the main coefficient. **[Practice]**
26. Heterogeneity needs an ex-ante reason; slicing samples until something is significant is p-hacking. **[Practice]**

## 7. Conclusion

27. No new results, no new citations. **[Harvard 2001/2014]**
28. Policy implications must match identification strength: an association licenses "worth attention", not
    "should be implemented". **[Practice]**

## 8. Common errors

29. Numbers in the text must match the tables. **[Gordon n.d.]**
30. Every exhibit must be referenced in the text, in order. **[Gordon n.d.]**
31. One symbol, one meaning; do not reuse a coefficient name for a different parameter. **[Bellemare 2020]**
32. One citation style throughout; the reference list and the in-text citations must agree.
    **[Harvard 2001/2014; AEA style guide]**

## How to use

- **Step 4**: apply 1–11 as a sentence-level checklist; log every fix in Block B with the rule number.
- **Step 5**: apply 12–28 by section function (missing magnitude, missing threat, missing channel).
- Never add evidence the author did not supply. Where evidence is missing, insert `[CITE?]` or `[MAGNITUDE?]`
  and hand the decision back.
