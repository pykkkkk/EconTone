#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""segmentation_guard.py — classify a revision as boundary-only, licensed rewording, or illegal.

The prosody gate owns more than boundaries now. Its action set is:

    #1 split        #2 merge        #3 seam function word     #6 ; <-> .
    #5 sentence-style appositive    #9 clause reordering
    #10 voice switch                #13 function-word insert/delete to break a stress run

Those moves may reorder content words or change their grammatical form, but they may not replace them.
Anything else — a synonym swap (#12) or a nominalisation (#11) — must be *proposed* to econtone-polish,
never executed here.

Classification
--------------
boundary-only       content words identical, in the same order        always legal
licensed-rewording  same content words, reordered or re-inflected     legal only with --licensed
illegal             a content word was added, removed or replaced     always rejected

    python segmentation_guard.py BEFORE.md AFTER.md
    python segmentation_guard.py BEFORE.md AFTER.md --licensed
    python segmentation_guard.py selftest

Exit codes: 0 legal, 1 illegal, 2 usage.
"""
import json
import re
import sys

TOKEN = re.compile(r"[A-Za-z0-9']+")

STOP = {
    "a", "an", "the", "and", "or", "but", "if", "then", "than", "that", "this", "these", "those",
    "it", "its", "they", "their", "them", "we", "our", "us", "i", "you", "your", "he", "she", "his",
    "her", "is", "are", "was", "were", "be", "been", "being", "am", "do", "does", "did", "has",
    "have", "had", "will", "would", "can", "could", "may", "might", "must", "shall", "should",
    "of", "in", "on", "at", "to", "for", "from", "by", "with", "as", "into", "about", "over",
    "after", "before", "between", "through", "during", "without", "within", "under", "above",
    "not", "no", "nor", "so", "such", "which", "who", "whom", "whose", "what", "when", "where",
    "while", "because", "although", "though", "since", "both", "each", "either", "neither", "any",
    "all", "some", "more", "most", "other", "only", "own", "same", "there", "here", "further",
}


def content_words(text):
    return [t.lower() for t in TOKEN.findall(text) if t.lower() not in STOP]


def stem(word):
    """A deliberately light stemmer: enough for report/reported/reporting, nothing cleverer."""
    for suf in ("ingly", "edly", "ing", "ed", "es", "s"):
        if word.endswith(suf) and len(word) - len(suf) >= 4:
            return word[: -len(suf)]
    return word


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def classify(a_text, b_text):
    a, b = content_words(a_text), content_words(b_text)
    if a == b:
        kind = "boundary-only"
    elif sorted(stem(w) for w in a) == sorted(stem(w) for w in b):
        kind = "licensed-rewording"
    else:
        kind = "illegal"
    missing = [w for w in sorted(set(a) - set(b))][:8]
    added = [w for w in sorted(set(b) - set(a))][:8]
    return {"class": kind, "sentences_before": len(sentences(a_text)),
            "sentences_after": len(sentences(b_text)),
            "removed": missing, "added": added,
            "content_before": len(a), "content_after": len(b)}


def selftest():
    n = 0
    assert classify("The design is simple; it works well.",
                    "The design is simple. It works well.")["class"] == "boundary-only"
    n += 1
    assert classify("The design is simple. It works well.",
                    "The design is simple and it works well.")["class"] == "boundary-only"
    n += 1
    assert classify("We report a large effect.",
                    "A large effect is reported.")["class"] == "licensed-rewording"
    n += 1
    assert classify("Because costs fell, entry rose.", "Entry rose because costs fell.")["class"] == "licensed-rewording"
    n += 1
    assert classify("The effect is large.", "The effect is substantial.")["class"] == "illegal"
    n += 1
    assert classify("We exploit a policy shock.", "We exploit a shock.")["class"] == "illegal"
    n += 1
    return n


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    licensed = "--licensed" in sys.argv
    if args[:1] == ["selftest"]:
        print("selftest: %d assertions passed" % selftest())
        return 0
    if len(args) != 2:
        print(__doc__)
        return 2
    r = classify(open(args[0], encoding="utf-8").read(), open(args[1], encoding="utf-8").read())
    legal = r["class"] == "boundary-only" or (r["class"] == "licensed-rewording" and licensed)
    if "--json" in sys.argv:
        r["legal"] = legal
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print("guard: %s  (%s)" % (r["class"], "LEGAL" if legal else "REJECTED"))
        print("  sentences: %d -> %d | content words: %d -> %d"
              % (r["sentences_before"], r["sentences_after"], r["content_before"], r["content_after"]))
        if r["removed"]:
            print("  removed: %s" % ", ".join(r["removed"]))
        if r["added"]:
            print("  added:   %s" % ", ".join(r["added"]))
        if r["class"] == "licensed-rewording" and not licensed:
            print("  -> re-run with --licensed if this is move #5/#9/#10/#13")
    return 0 if legal else 1


if __name__ == "__main__":
    sys.exit(main())
