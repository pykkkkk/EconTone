# Why EconTone is dual-licensed

**Code: Apache-2.0. Prose: CC0 1.0. The name and mark: neither.**

This file is the argument for that split, written so a reader — or a lawyer, or a maintainer in two years — can
see what was decided and why, rather than having to infer it from two files in the root.

## 1. The problem with one licence

This repository is not one kind of work:

| Kind | Example | What people do with it |
|---|---|---|
| Executable code | `skills/econtone-prosody/scripts/prosody_check.py` | install it, call it, embed it in a pipeline |
| Prose knowledge | `econ_writing_rules.md`, `phrase_bank.md` | quote it, paste it into prompts, teach from it |
| Data | `skills/econtone-prosody/tests/fixtures.json` | run it as part of a test suite |
| Identity | the name, the crescent mark | refer to the project |

A single licence over-serves one of these. MIT on everything lets the code be used freely but says nothing about
patents or the name; a copyleft licence on everything would keep the code out of the proprietary pipelines where
a writing checker is most useful.

## 2. The split

| Path | Licence | File |
|---|---|---|
| `skills/econtone-*/scripts/**`, `skills/econtone-*/tests/**`, `tests/` | **Apache-2.0** | `LICENSE` |
| `**/README.md`, `skills/econtone-*/references/**`, `docs/**`, this file | **CC0 1.0** | `LICENSE-DOCS.md` |
| the name "EconTone" and the mark | **not licensed** | `docs/trademark-notes.md` |

Redistributing the whole repository means carrying all three notices.

## 3. Why Apache-2.0 for the code

1. **Patent grant (§3).** MIT says nothing about patents. These scripts implement published statistical
   metrics; the risk is small, but a patent grant costs the licensor nothing and removes a question a corporate
   reviewer would otherwise ask.
2. **Trademark carve-out (§6).** Apache explicitly does *not* grant the name — and the mark is the part we are
   least willing to see reused.
3. **NOTICE mechanism (§4d).** Attribution travels with the code without a header in every file.
4. **Explicit contribution terms (§5).** A pull request is contributed under the licence by default.
5. **Patent retaliation (§3, final sentence).** If someone sues over the code, their patent licence ends.

Cost: a longer file and a NOTICE obligation. Both are routine for an engineering audience.

## 4. Why not MIT for the code

MIT is shorter and more familiar, and for a pure utility it would be enough. It provides neither a patent grant
nor a trademark clause, and this project has a mark it wants to keep. The usual objection — "Apache is harder
for hobbyists" — does not hold: Apache-2.0 is OSI-approved, used by Kubernetes, TensorFlow and Android, and no
one needs a lawyer to install something Apache-licensed.

## 5. Why not GPL / AGPL

The code is a small utility meant to be dropped into someone else's agent pipeline. GPL would require that
pipeline to be GPL; AGPL would extend that to a hosted service and is treated as a hard blocker by most platform
teams. Copyleft on the code would not protect the prose anyway — the two travel separately.

## 6. Why CC0 for the prose

1. **The failure mode that matters is disuse, not plagiarism.** A rule that nobody copies helps nobody. CC0
   removes the last piece of friction — a citation line someone forgets to add, or adds wrongly.
2. **Attribution requirements are hard to police and easy to satisfy badly.** "Adapted from EconTone" pasted at
   the bottom of a page satisfies CC BY and communicates nothing. We would rather not run a regime whose main
   effect is to produce that line.
3. **The prose is a compilation of advice that circulates freely in the field.** The sentences are ours; the
   practices are not. Charging a citation for them would be a strange kind of rent.
4. **It matches what the tool itself does.** The polish skill refuses to inflate its own contribution; the
   licence does the same. Under CC0 nobody has to think about us again after reading.

What we give up, stated plainly: **credit**, and any legal lever if someone republishes the rules commercially
without acknowledgement. That is the price of the friction we wanted to remove, and it was chosen deliberately —
an earlier draft of this repository used CC BY 4.0 and was changed.

## 7. Why not CC BY, and why not CC BY-SA

- **CC BY** requires attribution. It is a perfectly good licence, and it was this repository's first choice. It
  was dropped because the requirement buys enforcement we will not exercise and imposes a condition on the
  reader that the project does not care about. Attribution is welcome; it is not a term.
- **CC BY-SA** adds share-alike on top. That reads well until an adopter wants 40 rules inside a 300-page
  proprietary handbook; then it is a non-starter and they use nothing at all.

## 8. Why the prose is not under Apache-2.0

Apache is a software licence: written in terms of Source and Object form, awkward for creative text, and CC
itself advises against using it for prose. Licensing documentation under a code licence is legally possible and
practically confusing.

## 9. Objections, answered

**"Two licences is confusing."** Two lines in the README and this file resolve it. The alternative — one licence
that either over-permits the prose or over-restricts the code — is a worse confusion.

**"Doesn't CC0 let a company sell my rules with no credit at all?"** Yes. A company that resells them owes
nothing. We accept that: the rules are worth more circulating than fenced, and a bad actor who strips the name
would have stripped it under CC BY too, only more quietly.

**"What about the papers and guides you built on?"** They are cited, not distributed, and they keep their own
rights. `docs/provenance.md` separates our code, the borrowed methods and the third-party text, and states that
the repository licence cannot cover the last of them. The citation lists are scholarship, not licence terms.

**"Can I use the logo?"** Not under either licence. The mark is unregistered and unlicensed; if you fork, use
your own mark.

## 10. The cost, stated plainly

- a second licence file to explain;
- no credit requirement, and therefore no credit expectation;
- an enforcement asymmetry: misuse of the prose is easy to see and — under CC0 — legally unactionable;
- and no registration behind any of it: a licence is not a trademark, and neither is a defence against someone
  else claiming the name.

That is the trade: a slightly heavier licence structure in exchange for code that is frictionless and prose that
is genuinely free.
