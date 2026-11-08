# Causal inference by design — working notes from *The Mixtape*

Companion to `causal_facts.md`. Where that file states principles, this one is organised by **design**: what each
design identifies, what the paper must report, and the sentence-level overclaim the design invites.

- **Source.** Scott Cunningham, *Causal Inference: The Mixtape*, 2nd edition (online, work in progress),
  <https://mixtape.scunning.com/>. Pages read 2026-11-07.
- **Status: paraphrase.** No sentence here is quoted from the book. The identifying assumptions follow its
  exposition; **every "overclaim to catch" line is this skill's editorial construction**, not the author's
  verdict on any particular paper. The closing section marks what is explicit in the book and what was inferred.
- **How to use it.** In Step 3, after the fact-check, match the paper's design to one section and test the prose
  against its four bullets. In Step 4, the lookup table at the end turns the same material into copy-editing
  checks.
- **Not covered.** The online second edition is incomplete and is a mixtape, not a survey: it has no chapter on
  shift-share beyond a mention, no formal treatment of mediation, and introduces several recent estimators at
  introduction depth.

---

# Causal Inference: The Mixtape — working notes

*Causal Inference: The Mixtape* (2nd edition, online, in progress) is Scott Cunningham's design-based tour of
applied causal inference, written for practitioners rather than econometricians. Its organising claim is that
no estimator identifies anything: identification comes from the treatment assignment mechanism, and each
chapter is one such mechanism — randomisation, conditional independence, a cutoff, an instrument, parallel
trends, a factor structure. Designs are therefore introduced as answers to the question "how did some units end
up treated and others not?", and each is paired with a named target parameter (ATE, ATT, LATE, ATT(g,t)) and an
assumption the author expects you to defend in public. Regression appears throughout, but as a statistical
model that inherits credibility from the design rather than conferring it.

## 1. Potential outcomes and randomisation (ch. 3)

- **Question it answers:** what would have happened to the same units had they not been treated, and which
  average of those individual differences the policy question actually needs — ATE, ATT or ATU.
- **Identifying assumption:** randomisation, (Y¹,Y⁰) ⟂ D, so that treated and control units are exchangeable,
  together with SUTVA (no interference between units, a single version of the treatment) and the switching
  equation Y = DY¹ + (1−D)Y⁰.
- **What the paper must report:** the assignment mechanism, including the level at which randomisation
  occurred, and a balance table on pre-treatment covariates; the estimand actually delivered (ATE vs ATT vs
  ITT/TOT) and how non-compliance and attrition are handled; randomisation inference under a sharp null when the
  number of assignment units is small; the decomposition of the raw difference in means into ATE plus selection
  bias plus heterogeneous-effect bias, which is what the design is supposed to eliminate.
- **The overclaim to catch in the prose:** "randomised, therefore causal" — when assignment was by cluster and
  interference is plausible, SUTVA is the assumption in doubt, not the arithmetic. Also "the treatment had no
  effect" from an ITT with low take-up, and "the effect" where the design only ever identified an effect on the
  treated.

## 2. Directed acyclic graphs (ch. 4)

- **Question it answers:** which variables must be conditioned on, and which must be left alone, for the
  surviving association between treatment and outcome to be causal rather than a backdoor path.
- **Identifying assumption:** the graph — including its absent arrows — is a correct statement of the
  data-generating process, and the backdoor criterion is satisfied: every backdoor path is blocked by
  conditioning on non-colliders, and no collider is conditioned on.
- **What the paper must report:** the DAG itself, or a verbal equivalent, with the paths enumerated; the
  minimal sufficient adjustment set and the reason each control belongs in it; a defence of the missing arrows,
  since those absences carry the exclusion restrictions; and a note on which controls were added only for
  precision, since neutral covariates that predict the outcome buy precision without buying identification.
- **The overclaim to catch in the prose:** "we control for a rich set of covariates, so confounding is
  addressed." Conditioning on a collider — occupation, promotion, survival, selection into the sample — opens a
  path instead of closing one, and can reverse the sign of the coefficient. Flag the same sentence when the
  controls are post-treatment, and flag "no effect remains once we control for X" whenever the control set was
  never justified against a graph.

## 3. Unconfoundedness, matching and regression (ch. 5)

- **Question it answers:** the effect of a treatment that units choose for themselves, when selection into
  treatment is on observables rich enough to make treated and control units comparable within cells of X.
- **Identifying assumption:** conditional independence, (Y¹,Y⁰) ⟂ D | X — treatment is as good as randomly
  assigned within covariate cells — plus overlap, 0 < Pr(D=1|X) < 1. For the ATT the weaker Y⁰ ⟂ D | X is enough,
  and weak common support suffices.
- **What the paper must report:** the estimator (subclassification, matching, IPW, regression, or a doubly
  robust combination) and the parameter it targets; balance on covariates by normalised differences rather than
  p-values, shown before and after weighting; the overlap region, trimming rule, and how many treated
  observations fall outside it; and sensitivity of the estimate to functional form, caliper and covariate set,
  since matching interpolates and regression extrapolates.
- **The overclaim to catch in the prose:** "we control for observables, so the estimate is causal."
  Unconfoundedness is a claim about how people chose treatment, not a property of the regression; a paper that
  never says why selection is on observables has assumed the conclusion. Also "the matching estimate reproduces
  the experimental benchmark" — one famous replication is not a licence — and "no effect" when the estimate is an
  ATT computed on a thin overlap region.

## 4. Regression discontinuity (ch. 6)

- **Question it answers:** the effect of a treatment for units at a known cutoff in a running variable, where
  treatment status changes discontinuously and nothing else should.
- **Identifying assumption:** continuity — E[Y⁰|X] and E[Y¹|X] are continuous in the running variable at the
  cutoff c, so any jump in the observed outcome at c is attributable to the treatment — together with no
  manipulation of X around c and a cutoff that is not itself correlated with other determinants of the outcome.
- **What the paper must report:** the binned outcome plot with separate fits on each side; the bandwidth,
  kernel and polynomial order, plus the estimate's sensitivity to all three; a density test for sorting and
  covariate-balance and placebo-cutoff tests; and inference that avoids clustering on the running variable, using
  bias-corrected or honest intervals when the approximation bias is non-trivial.
- **The overclaim to catch in the prose:** "the effect of X on Y" where only a local effect at the cutoff is
  identified. Generalising from 21-year-olds to all ages, or from one score threshold to the whole distribution,
  is extrapolation the design does not license. Also "no discontinuity, so no effect" from a thin local sample,
  and "significant" reported from conventional confidence intervals in a setting where conventional intervals are
  known to over-reject.

## 5. Instrumental variables (ch. 7)

- **Question it answers:** the effect of an endogenous treatment, using a variable that shifts treatment and
  reaches the outcome only through it; with heterogeneous effects, the answer is the effect for compliers.
- **Identifying assumption:** the LATE assumptions — independence of Z from the potential outcomes, the
  exclusion restriction (Z affects Y only through D), a non-zero first stage, and monotonicity (no defiers) —
  plus SUTVA. Under all five, the Wald ratio and 2SLS identify the average effect for compliers.
- **What the paper must report:** the first stage and the reduced form, as coefficients and as pictures, since
  the "strange" reduced form is the argument; first-stage strength, reported as an F statistic and, where
  instruments are many or the F is marginal, as an effective F or a weak-IV-robust interval; a characterisation
  of the complier group and why that margin answers the question; and the institutional argument for exclusion,
  which no test can supply.
- **The overclaim to catch in the prose:** "IV solves endogeneity" with no exclusion argument; "the instrument
  is exogenous because the overidentification test does not reject", which is unavailable when the model is just
  identified; "the effect of D" presented as an ATE when it is a LATE; and "the first stage is strong" resting on
  an F near 10.

## 6. Panel data and fixed effects (ch. 8)

- **Question it answers:** the effect identified from within-unit changes over time, when the confounder is a
  fixed characteristic of the unit rather than something the researcher can measure.
- **Identifying assumption:** strict exogeneity conditional on the unobserved effect, E[ε_it | D_i1,…,D_iT,
  u_i] = 0 — treatment may be arbitrarily related to the time-invariant u_i but not to the idiosyncratic error —
  together with no reverse causality and a genuinely time-invariant omitted heterogeneity.
- **What the paper must report:** the within estimate next to pooled OLS and between estimates, so the reader
  can see what the fixed effects did; a statement of what is absorbed, including any treatment that never changes
  within unit; standard errors clustered at the panel level with the number of clusters stated; and a discussion
  of time-varying confounders and of feedback from outcome to treatment.
- **The overclaim to catch in the prose:** "fixed effects remove omitted variable bias." They remove one
  specific form of it and nothing else: time-varying unobserved heterogeneity, measurement error in the
  treatment, and simultaneity all survive demeaning. The police-and-crime positive coefficient is the standard
  warning — "more police cause more crime" is a sentence no copy-editor should let through — and a within
  coefficient is not an ATE for the population.

## 7. Difference-in-differences, 2×2 (ch. 9)

- **Question it answers:** the effect of a treatment in one group over one period, identified by that group's
  change relative to the change in an untreated comparison group — four averages and three subtractions.
- **Identifying assumption:** parallel trends, E[Y⁰_post − Y⁰_pre | D=1] = E[Y⁰_post − Y⁰_pre | D=0], plus no
  anticipation (no effect before the treatment begins) and, in repeated cross-sections, no compositional change
  in who is sampled.
- **What the paper must report:** the four averages and three subtractions, or the numerically identical
  interaction, TWFE or long-difference regression; an event study with pre-period coefficients and confidence
  intervals; falsification exercises of both kinds the book catalogues — same outcome with an alternative group,
  same group with an alternative outcome — and placebo cutoffs; standard errors clustered at the level of
  treatment assignment, plus an argument that the comparison group was not already treated.
- **The overclaim to catch in the prose:** "the parallel trends assumption is satisfied." It is untestable; the
  defensible sentence is that pre-treatment trends are consistent with it. Also "the effect is X" where the
  comparison group is already treated and its trend therefore contains treatment dynamics, and "time trends are
  controlled for" as though two-way fixed effects did that by construction rather than by assumption.

## 8. Complex difference-in-differences (ch. 10)

- **Question it answers:** the same question under harder data — treatment arriving at different times,
  unbalanced panels, repeated cross-sections, covariates, triple differences, or a treatment that switches on and
  off.
- **Identifying assumption:** parallel trends for the particular group-time comparisons actually used
  (never-treated, or not-yet-treated, possibly conditional on covariates), with no anticipation or limited
  anticipation; and, if the number is a TWFE coefficient, no heterogeneity in treatment effects across cohorts or
  over event time — otherwise the coefficient is a variance-weighted average of 2×2 comparisons whose weights can
  be negative.
- **What the paper must report:** the estimator and its comparison group; a cohort-specific or
  interaction-weighted event study with the omitted reference period named; a Goodman-Bacon-style decomposition,
  or at least a statement of which 2×2 comparisons carry the weight, alongside a heterogeneity-robust estimate
  (Callaway–Sant'Anna group-time ATTs, Sun–Abraham interaction weights, Borusyak–Jaravel–Spiess imputation, or de
  Chaisemartin–D'Haultfœuille for joiners and leavers); and a sensitivity analysis for the pre-trend conclusion —
  honest bounds, short gaps versus long differences — plus, for repeated cross-sections, evidence that
  composition is stable.
- **The overclaim to catch in the prose:** "the TWFE coefficient is the ATT" under staggered adoption with
  dynamic effects; "the event study shows no pre-trend" when that event study is itself a TWFE object
  contaminated by already-treated units and by a normalisation choice; "we used Callaway–Sant'Anna, so the
  estimate is robust" with the wrong comparison group or an anticipation window that does not match the
  institution; and "the triple difference is a falsification test" — it is a design whose assumption is equal
  non-parallel-trends bias in both DiDs, so the placebo DiD need not be zero.

## 9. Synthetic control (ch. 11)

- **Question it answers:** the effect of an intervention on one or a few aggregate units, using a weighted
  combination of untreated units as the counterfactual — including when no single unit and no regression will do.
- **Identifying assumption:** an approximate factor model for the untreated potential outcome, Y⁰_it = α_t +
  θ_t Z_i + λ_t u_i + ε_it, with a long and closely fitting pre-period; weights that are non-negative and sum to
  one, so the synthetic unit is a convex combination inside the convex hull of the donor pool; and no
  anticipation, with a donor pool free of treated or contaminated units.
- **What the paper must report:** pre-treatment fit — RMSPE and the gap plot before treatment — since
  post-treatment divergence means nothing without it; the weight table, because transparency is the method's
  selling point; the donor pool and the reasons units were dropped; and placebo inference, namely the treated
  unit's rank in the distribution of post/pre RMSPE ratios and the exact p-value that follows, with robustness to
  donor pool, predictors and, where fit is imperfect, augmented or matrix-completion versions.
- **The overclaim to catch in the prose:** "synthetic control shows a large effect" when the pre-period fit is
  poor, in which case the gap is prediction error; "significant at the 5% level" from a rank p-value computed on
  a small donor pool; "no parallel trends assumption is needed" — a different and stronger assumption about the
  factor structure replaces it; and generalising a one-unit ATT to units that were never in the donor pool's
  reach.

## Copy-editing checks

| If the paper says… | …check that it also says |
| --- | --- |
| "X causes Y", "the effect of X on Y" | which design supplies the counterfactual, which assumption is doing the work, and which parameter the number estimates. |
| "randomised", "experiment" | the level of randomisation, whether units can interfere, attrition and take-up, and whether the estimate is ITT or TOT. |
| "controlling for…", "rich covariates" | the graph or selection argument justifying each control, and that no control is a collider or post-treatment. |
| "unconfoundedness holds", "matching", "propensity score" | covariate balance and overlap, the estimand (ATT or ATE), and sensitivity to specification. |
| "the cutoff identifies…" | bandwidth, kernel, polynomial order, a sorting/density test, balance at the cutoff, and that the claim is local to it. |
| "IV estimates the effect of…" | the first stage and its strength, the complier population, and the exclusion argument, which is narrative. |
| "the first stage is strong (F > 10)" | an effective F or weak-IV-robust interval when instruments are many or the F is marginal. |
| "fixed effects", "within estimator" | that the confounder is time-invariant, that feedback is ruled out, and how many clusters there are. |
| "parallel trends" stated as fact | an event study, the reference period, falsification tests, and the admission that the assumption is untestable. |
| "the event study shows no pre-trend" | power on the pre-period coefficients, the cohort weighting, and whether already-treated units serve as controls. |
| "two-way fixed effects DiD" with staggered adoption | a Bacon-style decomposition and a heterogeneity-robust estimator beside it. |
| "the triple difference confirms…" | that the placebo DiD need only equal the main DiD's bias, not equal zero. |
| "synthetic control", "the effect is significant" | pre-period RMSPE and fit, the weight table, donor-pool exclusions, and the rank-based placebo p-value. |
| "no effect", "we find nothing" | the confidence interval, the minimum detectable effect, and whether the estimand applies to that population. |

## Where the book is explicit vs where I inferred

**Explicit in the book.** SUTVA, independence and the switching equation, with the decomposition of a
difference in means into ATE, selection bias and heterogeneous-effect bias (ch. 3). The backdoor criterion and
collider logic, including the warning that controlling for a collider opens a path (ch. 4). Unconfoundedness as
conditional independence, common support, and the distinction between strong and weak unconfoundedness when the
target is the ATT (ch. 5). Continuity at the cutoff, the local character of the RD estimand, and density,
balance and placebo-cutoff tests (ch. 6). The LATE assumptions enumerated one at a time — SUTVA, independence,
exclusion, non-zero first stage, monotonicity — and the point that exclusion is untestable (ch. 7). Strict
exogeneity conditional on the unobserved effect, and the two cases where fixed effects fail: time-varying
heterogeneity and reverse causality (ch. 8). Parallel trends, no anticipation, the instruction to avoid
already-treated controls, and the catalogue of falsifications (ch. 9). Triple difference as a design rather
than a falsification, with equal non-parallel-trends bias as its assumption (ch. 10). The factor model, the
weight constraints, and placebo inference by post/pre RMSPE rank (ch. 11).

**Inferred, or mine rather than the book's.** Every sentence in the "overclaim" bullets is my construction: the
book teaches the assumptions and repeatedly warns about the corresponding errors, but it does not issue
copy-editing rules, and no sentence here should be quoted as the author's verdict on a specific paper. The
"what the paper must report" lists are a triage of what the chapters themselves do and recommend; the book
prints partial checklists for unconfoundedness and for DiD, but not in this form. The
translations into editorial instructions — that a conventional RD interval over-rejects, that a within
coefficient is not an ATE, that a rank p-value is not a sampling p-value — are mine, faithful to the chapters'
arguments but sharper than their wording. On weak instruments I have kept to the level of "report the first
stage and something beyond the F"; the second edition says it updated this material and I have not reproduced
its specific recommended thresholds. On synthetic difference-in-differences and matrix completion I describe
the family and its assumptions at textbook level rather than tracking the chapter's exposition, which I read
only in part.

**Completeness of the second edition.** The book is explicit that it is a mixtape rather than a survey, so
absence is not an error. It has no chapter on shift-share/Bartik beyond its appearance in the IV chapter's list
of instrument designs, no formal treatment of mediation, no separate discussion of RD with multiple cutoffs or
of geographic RD, and no full treatment of sensitivity analysis beyond the honest-DiD bounds. Chapters 10 and
11 introduce several estimators — de Chaisemartin–D'Haultfœuille, Borusyak–Jaravel–Spiess, matrix completion,
synthetic DiD — at introduction depth, and a copy-editor should not treat those sections as the last word on
how the estimators behave. The author also takes a contestable position worth knowing: he argues that synthetic
control is not part of the difference-in-differences family, because it does not rest on parallel trends.
