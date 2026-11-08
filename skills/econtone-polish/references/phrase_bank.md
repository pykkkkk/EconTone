# Phrase bank for economics papers

Patterns organised by rhetorical function. `{}` marks a placeholder. These are **synthesised templates** built to
satisfy the rules in `econ_writing_rules.md` — they are not quotations from any source, and no source is
paraphrased line by line. Never deliver a sentence with an unfilled `{}`.

Each row carries a **use condition**; the template is wrong when the condition fails.

## 1. Positioning and contribution

| Pattern | Use only if |
|---|---|
| `This paper asks whether {X} affects {Y}.` | you have a design that supports "affects" |
| `We provide evidence that {finding}, using {design} and {data}.` | evidence exists; drop "first" unless true |
| `Relative to prior work, we {identify / document / quantify} {what}.` | you can name the prior work |
| `The contribution is threefold: {a}; {b}; {c}.` | no more than three items |
| `Our estimates imply {magnitude}, about {x}% of {baseline}.` | you have both the coefficient and the baseline |
| `This matters because {stake}: {number or institutional fact}.` | the motivation sentence carries evidence |

## 2. Identification

| Pattern | Use only if |
|---|---|
| `Identification comes from {variation}, conditional on {assumption}.` | any causal claim |
| `We exploit {policy shock / threshold / instrument} to isolate {variation}.` | the variation is genuinely exogenous |
| `The key assumption is {assumption}; we probe it with {test}.` | a test exists; say "probe", not "prove" |
| `Estimates are local to {compliers / the cutoff / the treated}.` | LATE or RDD |
| `Absent the reform, {group} would have followed the same trend as {comparison}.` | DID with a stated comparison group |
| `Standard errors are clustered at {level}, the level of treatment assignment.` | clustering follows assignment |

## 3. Data

| Pattern | Use only if |
|---|---|
| `We use {survey / administrative} data covering {population} from {period} ({N} observations).` | first data sentence |
| `The sample is restricted to {criterion}; Appendix Table {A} compares it with the full sample.` | a restriction exists and was checked |
| `{Variable} is measured as {definition}, in {unit}.` | first use of the variable |
| `Coverage is {x}% of {population}; attrition is {y}% and uncorrelated with {observable}.` | panel or linked data |

## 4. Results

| Pattern | Use only if |
|---|---|
| `A one-standard-deviation increase in {X} is associated with a {β} {unit} increase in {Y} ({p}).` | descriptive claim |
| `The estimate implies a {x}% increase relative to the control mean of {m}.` | causal claim with a baseline |
| `The effect is {precisely / imprecisely} estimated: the 95% CI excludes {value}.` | reporting a null or a noisy estimate |
| `Column {n} adds {controls / fixed effects}; the coefficient moves from {a} to {b}.` | describing a table column by column |
| `Table {n} shows {what}; the first row reads as {interpretation}.` | the table exists and is referenced in order |

## 5. Mechanism

| Pattern | Use only if |
|---|---|
| `One channel is {M}: {X} raises {M}, and {M} raises {Y}.` | both links are estimated |
| `Consistent with {channel}, the effect is concentrated among {subgroup}.` | the evidence is indirect |
| `These data cannot separate {channel A} from {channel B}.` | the honest case |

## 6. Robustness

| Pattern | Use only if |
|---|---|
| `A concern is {threat}. We address it with {test}; the estimate is {stable / attenuated}.` | one test per threat |
| `Results are robust to {alternative sample / specification / inference}.` | only what was actually run |
| `The placebo outcome {Z} shows no effect ({β}, {p}), as the design implies.` | a placebo was run |

## 7. Limitations

| Pattern | Use only if |
|---|---|
| `Our estimates speak to {population, period}; extrapolation to {other} requires {assumption}.` | external validity is discussed |
| `With {N} clusters, inference relies on {wild bootstrap / asymptotics}.` | few clusters |
| `We cannot rule out {alternative}, though {evidence} makes it less likely.` | an alternative exists |

## 8. Conclusion and policy

| Pattern | Use only if |
|---|---|
| `These results suggest that {policy} would {effect} for {group}, at a cost of {c}.` | cost data are in hand |
| `The findings are consistent with {view} but do not establish {stronger claim}.` | closing sentence |
| `Whether {mechanism} generalises is an open question.` | scope is genuinely open |

## 9. Transitions (ration them)

| Pattern | Note |
|---|---|
| `By contrast, {X}.` | real contrast only, not decoration |
| `The same pattern holds for {Y}.` | parallel evidence |
| `Two caveats follow.` | introduces limits without a fourth "However" |
| `Taken together, {claim}.` | at most once per paragraph |

## Do not use

- `It is worth noting that…`, `It should be noted that…`
- `In order to…` (use `To…`)
- `The results show that A has a positive impact on B` (no magnitude)
- `As can be seen from Table X…`
- `We use the DID method to study…` (name the identification strategy instead)
- `significant` standing alone, without a coefficient or a magnitude
