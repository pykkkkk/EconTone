# EconTone 1.0.2

Released 2026-11-10. A small release with one structural change: the orchestrator now has **two regimes**, and
the design principle behind it — *the last mile belongs to the author* — is written into the skill rather than
left implicit.

No new dependency. Replace the five skill directories.

---

## Added

**Two regimes.** `play.py --mode constrained|free`.

| regime | who may move a sentence boundary | guard | use when |
|---|---|---|---|
| `constrained` (default) | only `econtone-prosody` | a boundary move must return LEGAL | single-skill calls, production text, anything the author will sign |
| `free` | either player | the guard measures and reports the content change, but does not block | the structure itself is in question: a paragraph that may need re-cutting, a translation that inherited its sentence order |

Free mode lifts the **ownership** of boundaries, not the substance. Terminology hits may still not rise and the
risk tier may still not worsen; those rules bind in both regimes.

**The author as the last mile.** `econtone-equilibrium/SKILL.md` now opens this section:

> A paper is signed by a person. Everything this pack produces is therefore a menu of actions, not a verdict:
> each row states what could change, what it would buy, and what it would cost. A strategy is a combination of
> those actions, and the certificate offers a recommended one — but the author may add, drop or reorder moves to
> suit a taste that no measurement captures.

For a writer without a settled sense of the discipline, the same menu teaches: terminology and claim strength
are marked as hard constraints, register follows the field, rhythm is presented as an aesthetic choice.

## Changed

- Certificates record `mode`, and each move records a `guard` field — in a free run a cross-boundary move shows
  `ILLEGAL (content changed; allowed in free mode)`, so freedom stays auditable.
- Standard output prints `MODE: constrained|free` with the round count.

## Measured difference between the regimes

The same candidate — a move that splits a sentence and changes a content word:

```
constrained   rejected: guard ILLEGAL (content changed)
free          accepted: rhythm +7.1, trace 21.9, tier -1, burstiness out of RED (32.5 -> 50.7)
```

## Verification

```
12/12 checks pass · play.py selftest 12 · consistency PASS
```

## Known limits

- Free mode is not a licence to rewrite content: only the boundary rule is lifted, and every content change is
  recorded.
- Evaluation remains thin (two texts, eight coalitions); the regimes are tested on synthetic and published
  abstracts, not on a benchmark.
