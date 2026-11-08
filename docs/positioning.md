# Positioning against RCBSF

The nearest prior work, and what this pack must say to be distinguishable from it.

## The baseline

Xu, S., Wang, Y., Jia, X., Wu, Z., Liu, K., & Dong, A. X. (2026). *RCBSF: A multi-agent framework for
automated contract revision via Stackelberg game.* In Findings of the Association for Computational
Linguistics: ACL 2026 (pp. 18728–18756). Association for Computational Linguistics.
https://doi.org/10.18653/v1/2026.findings-acl.935

RCBSF models contract revision as a **bilevel Stackelberg game**: a *Global Prescriptive Agent* (leader)
imposes numeric **risk budgets**; a follower system — a *Constrained Revision Agent* plus a *Local
Verification Agent* — iteratively optimises the text inside those budgets. It proves bilevel convergence to
an equilibrium with strictly superior utility, and reports an 84.21% Risk Resolution Rate against iterative
baselines.

Two things follow. First, "applying Stackelberg games to automated text revision" is no longer an open
claim — it was published in 2026. Second, the comparison is not rhetorical: RCBSF has a convergence proof
and a benchmark metric that this pack does not have.

## Differentiation

| Dimension | RCBSF | EconTone equilibrium |
|---|---|---|
| Domain | legal contracts | academic economics prose |
| Constraint form | **numeric risk budgets** (scalar caps) | **categorical validity**: canonical terminology, claim strength tied to the design — lexicographic, not weighted |
| What the leader does | sets budgets (parameters) | **edits the text** subject to the constraints |
| Follower's action set | same text space, any revision within budget | **disjoint linguistic unit**: sentence boundaries and rhythm moves only |
| Why the leader's constraints survive | a verifier agent checks the follower's output | **by construction**: the follower cannot change a content word, so it cannot alter a term or a claim |
| Verification | an LLM agent (LVA) | **mechanical guards**: content-word multiset check, proxy bands, no model in the loop |
| Equilibrium evidence | utility comparison, RRR | **certificate**: schedule admissibility, every rejected move, the metric it would have broken |
| Objective of the follower | utility within budget | **soft**: maximise rhythm proximity, never force it |

The load-bearing difference is the fifth row. RCBSF must *verify* that the follower respected the leader's
budget; this pack arranges the game so that the follower **cannot** violate it — the action sets are disjoint
by construction, and a script rather than a model confirms it. That is a structural guarantee in place of a
supervisory one.

The cost is stated plainly: RCBSF proves convergence; this pack does not. Its guarantee is invariance, not
optimality. It also stops at a *local* equilibrium (no single legal move improves the score), which is weaker
than a bilevel convergence theorem.

## The three claims that survive

1. **Lexicographic disciplinary constraints.** Prior work constrains text with scalar budgets or weighted
   objectives. Here the constraints are categorical and non-tradeable: a canonical term and a claim
   proportionate to the design outrank everything, and rhythm is an enhancement by definition.
2. **Action-set ownership by linguistic unit.** Sentence-internal edits belong to the leaders; boundary moves
   belong to the follower. Because a boundary move cannot change a word, the leader's objective is invariant
   to the follower's strategy — a guarantee obtained from the structure of the move set rather than from
   monitoring.
3. **A mechanically checkable equilibrium certificate.** The delivered artefact includes the admissible
   schedule, the accepted moves, the rejected moves with the metric each would have broken, and the stopping
   condition. A reader can re-run the guards and reproduce the stopping point.

## Positioning paragraph (200 words, for an introduction)

> Automated revision systems increasingly treat writing as a constrained optimisation problem, and recent work
> formalises this as a Stackelberg game in which a leader imposes risk budgets and a follower optimises inside
> them (Xu et al., 2026). That formulation assumes the follower can act anywhere in the text and that
> compliance must therefore be verified. Academic prose imposes a different structure. Its constraints are
> categorical rather than numeric — a canonical term cannot be traded for a smoother clause, and a causal claim
> cannot exceed what the design identifies — and its editors already operate on different linguistic units:
> word-level passes rewrite inside sentences, while the rhythm pass moves sentence boundaries and nothing else.
> We exploit that separation. We formulate revision as a lexicographic Stackelberg game in which the follower's
> action set is disjoint from the leaders', so the hard constraints are invariant to the follower's strategy by
> construction rather than by supervision; compliance is checked by a content-word guard instead of a model.
> The equilibrium is reported as a certificate: the admissible schedule, every rejected move with the metric it
> would have broken, and the stopping condition. We do not prove convergence, and we stop at a local
> equilibrium; the contribution is a structural guarantee and an auditable stopping point for prose whose
> constraints cannot be priced.

## What would make this a paper rather than a claim

1. **A benchmark**: 40–60 abstracts and body paragraphs from open-access economics papers, each with three
   conditions — single skill, fixed pipeline, equilibrium orchestration.
2. **Metrics already implemented**: scorecard total, rhythm proximity, `risk_index`, plus the guard's
   violation count (should be zero by construction — that is the point).
3. **A human check** on meaning preservation and on whether the certificate's rejected moves are judged
   correct by an economist reader.
4. **An ablation** that removes the disjointness: let the follower rewrite words too, and measure how often
   the terminology constraint breaks. That experiment is the argument for the whole design.

## Claims to avoid

- "First to apply game theory to text revision" — false since 2026.
- "First Stackelberg framework for writing" — RCBSF occupies it.
- "Provably optimal" — we certify a local equilibrium, not an optimum.
- "Outperforms RCBSF" — different domain, different metric; no comparison is possible without a shared task.
