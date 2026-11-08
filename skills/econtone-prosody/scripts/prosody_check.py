#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prosody_check.py  —  Prosody Target-Card checker for the econtone-prosody skill

Quantifies the *phonological rhythm* of an English academic draft and compares it
against the "best prosody" target card derived from a 7-paper top-5 econ/management
corpus study and **re-validated on a 9-paper era-stratified corpus** (4 pre-2020 +
5 papers 2021+; the two eras are statistically indistinguishable). See
references/prosody_target_card.md. It is the **final
quantitative gate** of the EconTone pack, run after econtone-polish has drafted the
text (and standalone on any finished English paragraph): it catches low comfort from
rhythm and density that the terminology, register, and AI-trace passes miss.

METHOD (text-only, no audio, no TTS)
- Syllable stress is estimated with a small lexicon + a first-syllable heuristic.
  A production tool should use CMUdict (nltk) or acoustic data; the heuristic is a
  honest diagnostic, not ground truth.
- Metrics are grounded in speech-rhythm theory: nPVI (Grabe & Low 2002),
  %stressed (Ramus 1999), alternation rate, inter-stress-interval CV (Dellwo 2006
  Varco), plus sentence-length / parallelism density from the prose layer.
- "Comfort" is NOT a validated psychometric here. The checker emits a diagnostic
  verdict (OK / WARN / RED per metric + red-line markers), NOT a single score to
  maximise. Treat its output as a signal to act on, then re-run.
- A red-line marker is blocking, not advisory: any SLURRY / POUNDING / ROBOTIC /   DENSE / FLAT sentence forces REVISE even when all nine banded metrics are OK.

USAGE
  python scripts/prosody_check.py DRAFT.md                 # human-readable report
  python scripts/prosody_check.py DRAFT.md --json > p.json # machine-readable
  python scripts/prosody_check.py --text "..."            # analyse a string
  python scripts/prosody_check.py selftest                # 27 assertions

Standard library only; no third-party dependencies.
"""

# --- Force UTF-8 on stdout/stderr -------------------------------------------
# These reports contain em dashes, en dashes and (with --lang zh) CJK text.
# Windows defaults sys.stdout to the legacy ANSI code page (GBK on zh-CN), so
# those characters become replacement glyphs once the output is piped to a
# UTF-8 consumer. Reconfigure the streams: the bytes on the wire must be UTF-8.
import sys as _sys
for _stream in (_sys.stdout, _sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")
del _sys, _stream

import argparse
import json
import math
import re
import sys

# ---------------------------------------------------------------------------
# 1. Stress estimation (lexicon override + first-syllable heuristic)
# ---------------------------------------------------------------------------
# 1 = stressed syllable, 0 = unstressed. Patterns are per syllable, left->right.
# Each pattern's length MUST equal the word's true syllable count.
STRESS_OVERRIDE = {
    "the": [0], "a": [0], "an": [0], "of": [0], "to": [0], "in": [0],
    "on": [0], "at": [0], "by": [0], "for": [0], "and": [0], "or": [0],
    "is": [0], "are": [0], "was": [0], "were": [0], "be": [0], "been": [0],
    "being": [0], "as": [0], "that": [0], "this": [0], "these": [0],
    "those": [0], "it": [0], "its": [0], "with": [0], "from": [0],
    "but": [0], "than": [0], "then": [0], "so": [0], "into": [0],
    "develop": [0, 1, 0], "today": [0, 1], "because": [0, 1], "away": [0, 1],
    "about": [0, 1], "above": [0, 1], "across": [0, 1], "before": [0, 1],
    "important": [0, 1, 0], "individual": [0, 1, 0, 0, 0],
    "particularly": [0, 0, 1, 0, 0], "economic": [0, 1, 0, 0],
    "analysis": [0, 1, 0, 0], "parameter": [0, 1, 0, 0],
    "identify": [0, 1, 0, 0], "necessary": [0, 1, 0],
    "consequence": [0, 1, 0], "different": [0, 1, 0],
    "specific": [0, 1, 0], "political": [0, 1, 0, 0],
    "unlikely": [0, 1, 0], "however": [0, 1, 0], "therefore": [0, 1],
    "method": [0, 1], "data": [0, 1], "model": [0, 1],
    "result": [0, 1], "effect": [0, 1], "increase": [0, 1],
    "decrease": [0, 1], "evidence": [0, 1, 0], "provide": [0, 1],
    "suggest": [0, 1], "between": [0, 1], "measure": [0, 1],
    "compare": [0, 1], "require": [0, 1], "remain": [0, 1],
    "estimate": [0, 1, 0], "significant": [0, 1, 0, 0], "available": [0, 1, 0, 0],
    "potential": [0, 1, 0], "relative": [0, 1, 0], "positive": [0, 1, 0],
    "negative": [0, 1, 0], "consistent": [0, 1, 0], "marginal": [0, 1, 0],
    "subsample": [0, 1, 0], "mechanism": [0, 1, 0], "literature": [0, 1, 0, 0],
    "heterogeneity": [0, 0, 1, 0, 0, 0], "robustness": [0, 1, 0],
    "characteristic": [0, 1, 0, 0, 0], "instrument": [0, 1, 0],
}

FUNCTION_WORDS = set(STRESS_OVERRIDE.keys()) | {
    "we", "they", "he", "she", "you", "i", "do", "does", "did", "has",
    "have", "had", "can", "could", "should", "would", "will", "may", "might",
    "not", "no", "our", "their", "his", "her", "my", "your", "which", "who",
    "what", "when", "where", "why", "how", "if", "while", "although", "though",
    "than", "over", "under", "after", "during", "through", "against",
}

VOWELS = set("aeiouy")


# --- Optional CMUdict stress -------------------------------------------------
# If nltk and its cmudict corpus are available we use real stress patterns; if
# anything is missing we fall back to the lexicon + heuristic, silently. The
# report always says which engine produced the numbers.
USE_CMU = True
_CMU = None
_CMU_STATE = "unknown"   # cmudict | no_nltk | no_data


def _cmu():
    global _CMU, _CMU_STATE
    if _CMU_STATE != "unknown":
        return _CMU
    try:
        from nltk.corpus import cmudict
    except Exception:
        _CMU_STATE, _CMU = "no_nltk", None
        return None
    try:
        _CMU = cmudict.dict()
        _CMU_STATE = "cmudict"
    except Exception:
        _CMU_STATE, _CMU = "no_data", None
    return _CMU


def engine_name():
    if not USE_CMU:
        return "heuristic (--no-cmu)"
    _cmu()
    if _CMU_STATE == "cmudict":
        return "cmudict"
    if _CMU_STATE == "no_nltk":
        return "heuristic (nltk missing)"
    return "heuristic (cmudict data missing)"


def _cmu_stress(word):
    d = _cmu() if USE_CMU else None
    if not d:
        return None
    prons = d.get(word)
    if not prons:
        return None
    out = []
    for ph in prons[0]:
        if ph[-1].isdigit():
            out.append(0 if ph[-1] == "0" else 1)
    return out or None


def count_syllables(word):
    """Heuristic syllable count: vowel groups, minus trailing silent e."""
    word = word.lower()
    if not word:
        return 1
    if word.endswith("e") and len(word) > 2 and word[-2] not in VOWELS:
        word = word[:-1]
    groups = re.findall(r"[aeiouy]+", word)
    return max(1, len(groups))


def estimate_stress(word):
    """Return list of 0/1 per syllable."""
    w = word.lower().strip(".,;:!?\"'()[]{}")
    if not w:
        return [0]
    pat = _cmu_stress(w)
    if pat:
        return pat
    if w in STRESS_OVERRIDE:
        return list(STRESS_OVERRIDE[w])
    n = count_syllables(w)
    if n == 1:
        return [0] if w in FUNCTION_WORDS else [1]
    return [1] + [0] * (n - 1)


def tokenize(text):
    return re.findall(r"[A-Za-z']+", text)


# ---------------------------------------------------------------------------
# 2. Text cleaning (keep body prose only)
# ---------------------------------------------------------------------------
def clean_markdown(text):
    """Strip non-prose elements so the rhythm check reflects real reading text."""
    lines = text.splitlines()
    out = []
    in_code = False
    for ln in lines:
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        # headings
        if re.match(r"^\s{0,3}#{1,6}\s", ln):
            continue
        # markdown tables (>=2 pipes)
        if ln.count("|") >= 2 and re.search(r"[-:|]{3,}", ln):
            continue
        out.append(ln)
    body = "\n".join(out)
    # inline code / math
    body = re.sub(r"`[^`]*`", " ", body)
    body = re.sub(r"\$\$.*?\$\$", " ", body, flags=re.DOTALL)
    body = re.sub(r"\$[^$]*\$", " ", body)
    # citations: [12], [3, 4], (Author et al., 2020), (Smith, 2019)
    body = re.sub(r"\[\d+(?:\s*,\s*\d+)*\]", " ", body)
    body = re.sub(r"\([A-Z][a-zA-Z]*(?:\s+(?:and|&|et\s+al\.?))?,?\s*(?:\d{4}[a-z]?)\)", " ", body)
    # bold / italic markers
    body = re.sub(r"\*\*([^*]+)\*\*", r"\1", body)
    body = re.sub(r"\*([^*]+)\*", r"\1", body)
    return body


def split_sentences(text):
    """Naive sentence splitter on . ! ? followed by space+capital or end."""
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
    sents = [p.strip() for p in parts if p.strip()]
    return sents


# ---------------------------------------------------------------------------
# 3. Rhythm metrics (per text and per sentence)
# ---------------------------------------------------------------------------
def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def _pstdev(xs):
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def _nPVI(weights):
    if len(weights) < 2:
        return 0.0
    s = 0.0
    for k in range(len(weights) - 1):
        dk, dk1 = weights[k], weights[k + 1]
        if dk + dk1 == 0:
            continue
        s += abs(dk - dk1) / ((dk + dk1) / 2.0)
    return 100.0 * s / (len(weights) - 1)


def _longest_run(seq, val):
    best = cur = 0
    for x in seq:
        cur = cur + 1 if x == val else 0
        best = max(best, cur)
    return best


def analyse_sentence(text):
    words = tokenize(text)
    if not words:
        return None
    stress_seq = []
    weight_seq = []
    syl_per_word = []
    for w in words:
        pat = estimate_stress(w)
        stress_seq.extend(pat)
        for s in pat:
            weight_seq.append(2.0 if s == 1 else 1.0)
        syl_per_word.append(len(pat))
    n_syl = len(stress_seq)
    n_stress = sum(stress_seq)
    gaps = []
    last = -1
    for i, s in enumerate(stress_seq):
        if s == 1:
            if last >= 0:
                gaps.append(i - last)
            last = i
    isi_cv = (_pstdev(gaps) / _mean(gaps)) * 100.0 if gaps and _mean(gaps) else 0.0
    spw_cv = (_pstdev(syl_per_word) / _mean(syl_per_word)) * 100.0 if syl_per_word and _mean(syl_per_word) else 0.0
    # parallelism density: and/but/or/; per 100 words
    parallel = len(re.findall(r"\b(and|but|or)\b", text)) + text.count(";")
    return {
        "words": len(words),
        "syllables": n_syl,
        "stressed": n_stress,
        "nPVI": _nPVI(weight_seq),
        "pct_stressed": 100.0 * n_stress / n_syl if n_syl else 0.0,
        "alternation_rate": _alt_rate(stress_seq),
        "longest_unstressed_run": _longest_run(stress_seq, 0),
        "longest_stressed_run": _longest_run(stress_seq, 1),
        "inter_stress_CV": isi_cv,
        "syll_per_word_CV": spw_cv,
        "mean_syll_per_word": _mean(syl_per_word),
        "parallel_count": parallel,
        "stress_seq": stress_seq,
    }


def _alt_rate(stress_seq):
    if len(stress_seq) < 2:
        return 0.0
    alt = sum(1 for k in range(len(stress_seq) - 1) if stress_seq[k] != stress_seq[k + 1])
    return 100.0 * alt / (len(stress_seq) - 1)


def analyse_text(text):
    sents = split_sentences(clean_markdown(text))
    sents = [s for s in sents if analyse_sentence(s)]
    if not sents:
        return None
    per = [analyse_sentence(s) for s in sents]
    wps = [p["words"] for p in per]
    wps_sorted = sorted(wps)
    p95 = wps_sorted[min(len(wps_sorted) - 1, int(0.95 * len(wps_sorted)))]
    # aggregate stress sequence across sentences
    full_seq = []
    for p in per:
        full_seq.extend(p["stress_seq"])
    # document-level metrics
    agg = {
        "sentences": len(per),
        "words": sum(p["words"] for p in per),
        "syllables": sum(p["syllables"] for p in per),
        "stressed": sum(p["stressed"] for p in per),
        "nPVI": _nPVI(_doc_weights(per)),
        "pct_stressed": 100.0 * sum(p["stressed"] for p in per) / sum(p["syllables"] for p in per),
        "alternation_rate": _alt_rate(full_seq),
        "longest_unstressed_run": _longest_run(full_seq, 0),
        "longest_stressed_run": _longest_run(full_seq, 1),
        "inter_stress_CV": _doc_isi_cv(full_seq),
        "syll_per_word_CV": _mean([p["syll_per_word_CV"] for p in per]),
        "mean_syll_per_word": _mean([p["mean_syll_per_word"] for p in per]),
        "mean_words_per_sentence": _mean(wps),
        "cv_words_per_sentence": (_pstdev(wps) / _mean(wps)) * 100.0 if _mean(wps) else 0.0,
        "p95_words_per_sentence": p95,
        "parallel_per100": 100.0 * sum(p["parallel_count"] for p in per) / max(1, sum(p["words"] for p in per)),
        "_per_sentence": per,
        "_sentences": sents,
    }
    return agg


def _doc_weights(per):
    w = []
    for p in per:
        # reconstruct weight_seq from stress_seq
        w.extend(2.0 if s == 1 else 1.0 for s in p["stress_seq"])
    return w


def _doc_isi_cv(full_seq):
    gaps = []
    last = -1
    for i, s in enumerate(full_seq):
        if s == 1:
            if last >= 0:
                gaps.append(i - last)
            last = i
    return (_pstdev(gaps) / _mean(gaps)) * 100.0 if gaps and _mean(gaps) else 0.0


# ---------------------------------------------------------------------------
# 4. Target card (authoritative thresholds; mirror of references/14)
# ---------------------------------------------------------------------------
# band: (lo, hi, red_lo, red_hi, advice)
# red_lo/red_hi None => no red in that direction; WARN outside [lo,hi].
TARGET_CARD = {
    "nPVI": (35.0, 41.0, 15.0, None,
             "Raise contrast by mixing short and long stressed-unstressed units; avoid monotone listing."),
    "pct_stressed": (31.0, 41.0, None, None,
                     "Keep ~1 in 3 syllables stressed; heavy Latinate stacking lowers this."),
    "alternation_rate": (52.0, 62.0, None, 78.0,
                         "Break machine-like alternation with an occasional long or parallel sentence."),
    "inter_stress_CV": (43.0, 57.0, None, None,
                        "Vary the spacing between stressed syllables; avoid metronomic rhythm."),
    "mean_syll_per_word": (1.6, 2.0, None, 2.2,
                           "Swap a Latinate noun for a shorter word to lower syllable load."),
    "mean_words_per_sentence": (16.0, 34.0, None, 45.0,
                                "Split over-long sentences; most sentences land 16-34 words."),
    "p95_words_per_sentence": (None, 62.0, None, 95.0,
                               "One long sentence is fine; a 95th percentile above ~95 words is bloat."),
    "cv_words_per_sentence": (24.0, None, 15.0, None,
                              "Reward varied sentence length; only a very flat length distribution is a defect."),
    "parallel_per100": (1.4, 7.7, None, 10.0,
                        "Thin out the densest and/but/or chains; ordinary coordination is fine."),
}

# Bands recalibrated on 42 published economics / finance / management papers
# (2016-2021, 8 per year, OA, first author at a world-top department):
# 42 abstracts, 42 introductions, 794 body paragraphs. The comfort band is the
# 10th-90th percentile of published prose; the red line sits beyond the corpus
# tail, so a journal paragraph is not flagged for being a journal paragraph.
#
# Profiles differ only where the corpus shows a genre effect.
_HEUR_BASE = dict(TARGET_CARD)

# Stress metrics depend on the engine: CMUdict marks secondary stress, the
# lexicon heuristic only the first syllable. Bands below are the 10th-90th
# percentiles of the same 42-paper corpus re-measured with cmudict, so a
# cmudict run is compared against cmudict prose, not against heuristic prose.
# Non-stress metrics are engine-independent and are not overridden.
CMU_BANDS = {
    "body": {"nPVI": (38.6, 46.4, 15.0, None, "CMUdict-calibrated contrast band."),
             "pct_stressed": (47.8, 57.3, None, None, "CMUdict counts secondary stress; ~half of syllables carry one."),
             "alternation_rate": (58.0, 69.5, None, 82.0, "CMUdict-calibrated alternation band."),
             "inter_stress_CV": (43.0, 54.3, None, None, "CMUdict-calibrated spacing band.")},
    "abstract": {"nPVI": (41.2, 45.0, 15.0, None, "CMUdict-calibrated contrast band."),
                 "pct_stressed": (46.7, 55.5, None, None, "CMUdict-calibrated stress share."),
                 "alternation_rate": (61.8, 67.5, None, 82.0, "CMUdict-calibrated alternation band."),
                 "inter_stress_CV": (44.6, 51.9, None, None, "CMUdict-calibrated spacing band.")},
    "intro": {"nPVI": (40.7, 45.4, 15.0, None, "CMUdict-calibrated contrast band."),
              "pct_stressed": (47.0, 57.3, None, None, "CMUdict-calibrated stress share."),
              "alternation_rate": (61.1, 68.2, None, 82.0, "CMUdict-calibrated alternation band."),
              "inter_stress_CV": (43.2, 51.9, None, None, "CMUdict-calibrated spacing band.")},
}

PROFILES = {
    "body": {},
    "abstract": {
        "pct_stressed": (29.0, 39.0, None, None, "Keep ~1 in 3 syllables stressed."),
        "mean_syll_per_word": (1.8, 2.2, None, 2.4, "Abstracts run denser; keep under 2.4 syllables per word."),
        "mean_words_per_sentence": (16.0, 34.0, None, 45.0, "Abstract sentences run shorter than body prose."),
        "p95_words_per_sentence": (None, 56.0, None, 80.0, "A 56-word 95th percentile is the abstract norm."),
        "cv_words_per_sentence": (23.0, None, 14.0, None, "Abstracts vary less; only a very flat spread is a defect."),
        "parallel_per100": (2.8, 6.8, None, 9.0, "Abstracts carry slightly more coordination."),
        "inter_stress_CV": (43.0, 54.0, None, None, "Vary stress spacing."),
    },
    "intro": {
        "pct_stressed": (30.0, 40.0, None, None, "Keep ~1 in 3 syllables stressed."),
        "mean_words_per_sentence": (14.0, 31.0, None, 45.0, "Introductions run shorter sentences than body prose."),
        "cv_words_per_sentence": (30.0, None, 18.0, None, "Introductions vary a lot; only a flat spread is a defect."),
        "parallel_per100": (1.4, 8.0, None, 10.0, "Introductions carry the most coordination."),
    },
}


def apply_profile(name):
    """Rebuild TARGET_CARD for a genre and the active stress engine."""
    TARGET_CARD.clear()
    TARGET_CARD.update(_HEUR_BASE)
    for key, val in PROFILES.get(name, {}).items():
        TARGET_CARD[key] = val
    if _cmu() is not None:
        for key, val in CMU_BANDS.get(name, {}).items():
            TARGET_CARD[key] = val


def _status(key, val):
    lo, hi, rlo, rhi, _ = TARGET_CARD[key]
    if rlo is not None and val < rlo:
        return "RED"
    if rhi is not None and val > rhi:
        return "RED"
    if lo is not None and val < lo:
        return "WARN"
    if hi is not None and val > hi:
        return "WARN"
    return "OK"


# ---------------------------------------------------------------------------
# 5. Red-line markers (sentence-level, point at the offending sentence)
# ---------------------------------------------------------------------------
def red_line_markers(agg):
    markers = []
    per = agg["_per_sentence"]
    sents = agg["_sentences"]
    # SLURRY: any sentence with >=10 unstressed run (corpus p97)
    worst_slurry = None
    for i, p in enumerate(per):
        if p["longest_unstressed_run"] >= 10:
            if worst_slurry is None or p["longest_unstressed_run"] > worst_slurry[1]:
                worst_slurry = (i, p["longest_unstressed_run"])
    if worst_slurry:
        i, run = worst_slurry
        markers.append(("SLURRY",
                        "Sentence %d has a %d-syllable unstressed run (of/for/in/the + relative clauses). "
                        "Split it or switch to active voice." % (i + 1, run),
                        sents[i]))
    # POUNDING: any sentence with >=7 stressed run (corpus p95)
    worst_pound = None
    for i, p in enumerate(per):
        if p["longest_stressed_run"] >= 7:
            if worst_pound is None or p["longest_stressed_run"] > worst_pound[1]:
                worst_pound = (i, p["longest_stressed_run"])
    if worst_pound:
        i, run = worst_pound
        markers.append(("POUNDING",
                        "Sentence %d has a %d-syllable stressed run (piled monosyllabic content words). "
                        "Insert a weak syllable or a connective." % (i + 1, run),
                        sents[i]))
    # ROBOTIC: high alternation + low inter-stress CV (mechanical beat)
    if agg["alternation_rate"] > 78.0 and agg["inter_stress_CV"] < 35.0:
        markers.append(("ROBOTIC",
                        "Stress alternates at %.0f%% with flat spacing (CV %.0f%%) -> mechanical beat. "
                        "Break the pattern with a longer or parallel sentence." %
                        (agg["alternation_rate"], agg["inter_stress_CV"]),
                        None))
    # DENSE: mean sentence length > 40 (red) handled in band too; add explicit marker
    if agg["mean_words_per_sentence"] > 45.0:
        markers.append(("DENSE",
                        "Mean sentence length %.1f words exceeds the 45-word red line." %
                        agg["mean_words_per_sentence"],
                        None))
    # FLAT: nPVI < 15
    if agg["nPVI"] < 15.0:
        markers.append(("FLAT",
                        "nPVI %.1f < 15 -> monotone stress contrast." % agg["nPVI"],
                        None))
    return markers


# ---------------------------------------------------------------------------
# 6. Reporting
# ---------------------------------------------------------------------------
def _band_str(key):
    def _fmt(x):
        if x is None:
            return "—"
        if abs(x - round(x)) < 1e-9:
            return "%d" % int(round(x))
        return "%.1f" % x

    lo, hi, rlo, rhi, _ = TARGET_CARD[key]
    parts = []
    if lo is not None:
        parts.append(_fmt(lo))
    if hi is not None:
        parts.append(_fmt(hi))
    band = "–".join(parts) if parts else "—"
    red = ""
    if rlo is not None:
        red = " (red <%s)" % _fmt(rlo)
    elif rhi is not None:
        red = " (red >%s)" % _fmt(rhi)
    return band + red


def build_report(agg, source=""):
    if agg is None:
        return {"error": "no prose found after cleaning", "source": source}
    rows = []
    for key in ["nPVI", "pct_stressed", "alternation_rate", "inter_stress_CV",
                "mean_syll_per_word", "mean_words_per_sentence", "p95_words_per_sentence",
                "cv_words_per_sentence", "parallel_per100"]:
        val = agg[key]
        st = _status(key, val)
        rows.append({"metric": key, "value": round(val, 1), "status": st,
                     "band": _band_str(key)})
    markers = red_line_markers(agg)
    n_red = sum(1 for r in rows if r["status"] == "RED")
    n_warn = sum(1 for r in rows if r["status"] == "WARN")
    # A sentence-level red-line marker is blocking: the exit gate is "no RED-line
    # marker", so clean metric bands must not override a marker.
    verdict = ("REVISE" if (n_red > 0 or markers)
               else ("ADJUST" if n_warn > 0 else "PASS"))
    return {
        "source": source,
        "sentences": agg["sentences"],
        "words": agg["words"],
        "metrics": rows,
        "red_line_markers": [{"name": m[0], "message": m[1], "sentence": m[2]} for m in markers],
        "n_red": n_red,
        "n_warn": n_warn,
        "n_markers": len(markers),
        "verdict": verdict,
    }


def print_report(rep):
    if "error" in rep:
        print("PROSODY CHECK — %s" % rep["source"])
        print("  %s" % rep["error"])
        return
    print("PROSODY CHECK — %s" % rep["source"])
    print("  %d sentences, %d words (body prose only) | engine: %s"
          % (rep["sentences"], rep["words"], engine_name()))
    print("  " + "-" * 60)
    print("  %-26s %8s  %-5s  %s" % ("metric", "value", "band", "target"))
    for r in rep["metrics"]:
        print("  %-26s %8.1f  %-5s  %s" % (r["metric"], r["value"], r["status"], r["band"]))
    print("  " + "-" * 60)
    if rep["red_line_markers"]:
        print("  RED-LINE MARKERS:")
        for m in rep["red_line_markers"]:
            print("    [%s] %s" % (m["name"], m["message"]))
            if m["sentence"]:
                snip = m["sentence"]
                if len(snip) > 120:
                    snip = snip[:117] + "..."
                print("           >>> %s" % snip)
    else:
        print("  RED-LINE MARKERS: none")
    print("  " + "-" * 60)
    print("  VERDICT: %s  (RED=%d, WARN=%d, MARKERS=%d)" % (rep["verdict"], rep["n_red"], rep["n_warn"], rep["n_markers"]))
    if rep["verdict"] != "PASS":
        print("  ACTION: fix RED markers first, then WARN; re-run until PASS.")
    print()


def split_paragraphs(text):
    """Split raw text into natural paragraphs (blank line, or LaTeX \\par)."""
    text = re.sub(r"\\par\b", "\n\n", text)
    parts = re.split(r"\n\s*\n+", text)
    return [p.strip() for p in parts if p.strip()]


def analyse_paragraphs(text):
    """Measure each natural paragraph separately; never pool paragraphs."""
    out = []
    for idx, para in enumerate(split_paragraphs(text), 1):
        agg = analyse_text(para)
        if agg and agg["sentences"] >= 2:
            out.append((idx, agg))
    if not out:
        agg = analyse_text(text)
        if agg:
            out = [(1, agg)]
    return out


def worst_verdict(reports):
    rank = {"PASS": 0, "ADJUST": 1, "REVISE": 2}
    return max((r["verdict"] for r in reports), key=lambda v: rank.get(v, 0))


def print_paragraphs(reports, overall, source, profile):
    print("PROSODY CHECK — %s" % source)
    print("  profile=%s | %d paragraphs | %d sentences | %d words"
          % (profile, len(reports), sum(r["sentences"] for r in reports),
             sum(r["words"] for r in reports)))
    print("  " + "-" * 60)
    for i, r in enumerate(reports, 1):
        reds = [m["metric"] + "=" + str(m["value"]) for m in r["metrics"] if m["status"] == "RED"]
        warns = [m["metric"] for m in r["metrics"] if m["status"] == "WARN"]
        names = [m["name"] for m in r["red_line_markers"]]
        note = ", ".join(reds[:3] + warns[:2])
        if names:
            note = (note + " | " if note else "") + ",".join(names)
        print("  [%2d] %2d sent %4d w  %-7s R%d W%d M%d  %s"
              % (i, r["sentences"], r["words"], r["verdict"], r["n_red"], r["n_warn"],
                 r["n_markers"], note))
    print("  " + "-" * 60)
    print("  OVERALL: %s  (worst of %d paragraphs; RED=%d, WARN=%d, MARKERS=%d)"
          % (overall["verdict"], overall["paragraphs"], overall["n_red"],
             overall["n_warn"], overall["n_markers"]))
    if overall["verdict"] != "PASS":
        print("  ACTION: fix the paragraphs marked REVISE first, then ADJUST.")
    print()


# ---------------------------------------------------------------------------
# 7. selftest

# ---------------------------------------------------------------------------
def selftest():
    global USE_CMU
    USE_CMU = False   # unit assertions describe the heuristic path
    checks = []

    def ok(name, cond):
        checks.append((name, bool(cond)))

    # metric math
    ok("nPVI constant seq ~0", abs(_nPVI([1, 1, 1, 1])) < 1e-9)
    ok("nPVI alternating", _nPVI([1, 2, 1, 2]) > 30)
    ok("alt_rate full alt =100", abs(_alt_rate([0, 1, 0, 1]) - 100.0) < 1e-9)
    ok("alt_rate flat =0", abs(_alt_rate([1, 1, 1]) - 0.0) < 1e-9)
    ok("longest_run 0s", _longest_run([1, 0, 0, 0, 1, 0], 0) == 3)
    ok("syllables 'economic'=4", count_syllables("economic") == 4)
    ok("syllables 'the'=1", count_syllables("the") == 1)
    ok("stress 'the'=[0]", estimate_stress("the") == [0])
    ok("stress 'method'=[0,1]", estimate_stress("method") == [0, 1])

    # status logic
    TARGET_CARD["_t"] = (10.0, 20.0, 5.0, 30.0, "")
    ok("status OK", _status("_t", 15) == "OK")
    ok("status WARN-low", _status("_t", 8) == "WARN")
    ok("status WARN-high", _status("_t", 25) == "WARN")
    ok("status RED-low", _status("_t", 4) == "RED")
    ok("status RED-high", _status("_t", 31) == "RED")
    del TARGET_CARD["_t"]

    # Calibration locks (9-paper top-5 corpus, pre-2020 + 2021+):
    # sentence-length CV must reward variation, NOT uniformity, because it is the
    # same quantity detectors call "burstiness" -- high = human-like.
    ok("calibration: cv_sent_len 60 OK (real prose 55-88)",
       _status("cv_words_per_sentence", 60) == "OK")
    ok("calibration: cv_sent_len 70 OK (real prose range)",
       _status("cv_words_per_sentence", 70) == "OK")
    ok("calibration: cv_sent_len 12 RED (monotonous/templated)",
       _status("cv_words_per_sentence", 12) == "RED")
    ok("calibration: cv_sent_len 20 WARN (a little flat)",
       _status("cv_words_per_sentence", 20) == "WARN")
    # p95: an occasional long sentence is normal; only >95 is bloat.
    ok("calibration: p95 83 WARN (real prose 62-83, not RED)",
       _status("p95_words_per_sentence", 83) == "WARN")
    ok("calibration: p95 100 RED (genuine bloat)",
       _status("p95_words_per_sentence", 100) == "RED")
    ok("calibration: p95 55 OK (real prose)",
       _status("p95_words_per_sentence", 55) == "OK")

    # cleaning drops citations / headings / tables
    sample = "# Heading\n\nWe find an effect (Smith, 2019) of about 9% [3, 4].\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\nThis is a second sentence that is reasonably long and varied in its rhythm."
    agg = analyse_text(sample)
    ok("cleaning: sentences found", agg is not None and agg["sentences"] >= 1)
    ok("cleaning: citation removed (no 'Smith')", "Smith" not in " ".join(agg["_sentences"]))
    ok("cleaning: table removed", agg["words"] < 60)

    # engine detection: cmudict when present, silent fallback otherwise
    USE_CMU = True   # engine probe runs regardless of the heuristic pin above
    _cmu()
    if _CMU_STATE == "cmudict":
        ok("cmu: 'method' has a 2-syllable pattern", len(_cmu_stress("method") or []) == 2)
    else:
        ok("cmu: fallback state recorded", _CMU_STATE in ("no_nltk", "no_data"))
    USE_CMU = False

    # paragraph scoping: two paragraphs must be measured separately
    two = ("First paragraph sentence one is here and it runs a while. "
           "Second sentence of the same paragraph also has some length to it.\n\n"
           "Third paragraph starts fresh with a short line. "
           "Fourth sentence closes the second paragraph with more words than the first had.")
    groups = analyse_paragraphs(two)
    ok("paragraphs: split into 2", len(groups) == 2)
    ok("paragraphs: each measured alone", all(g[1]["sentences"] >= 2 for g in groups))

    # A red-line marker must force REVISE even when every banded metric is OK.
    marker_text = "This is a short test of the marker logic. Another sentence follows here."
    agg_m = analyse_text(marker_text)
    agg_m["_per_sentence"][0]["longest_unstressed_run"] = 12
    marker_rep = build_report(agg_m, "selftest")
    ok("marker: slurry detected", bool(marker_rep["red_line_markers"]))
    ok("marker: forces REVISE", marker_rep["verdict"] == "REVISE")
    ok("marker: reported in payload", marker_rep["n_markers"] >= 1)

    failed = [n for n, c in checks if not c]
    for n, c in checks:
        print(("  PASS " if c else "  FAIL ") + n)
    print("\nselftest: %d/%d passed" % (len(checks) - len(failed), len(checks)))
    return len(failed) == 0


# ---------------------------------------------------------------------------
# 8. CLI
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="LWH prosody target-card checker")
    ap.add_argument("file", nargs="?", help="markdown/txt draft to check")
    ap.add_argument("--text", help="analyse a string instead of a file")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    ap.add_argument("--no-cmu", action="store_true", help="ignore CMUdict even if installed")
    ap.add_argument("--profile", choices=["body", "abstract", "intro"], default="body",
                    help="genre band set: body (default), abstract, intro")
    ap.add_argument("cmd", nargs="?", help="use 'selftest' to run assertions")
    args = ap.parse_args()
    global USE_CMU
    if args.no_cmu:
        USE_CMU = False
    apply_profile(args.profile)

    if args.cmd == "selftest" or (args.file == "selftest"):
        ok_run = selftest()
        sys.exit(0 if ok_run else 1)

    text = None
    source = ""
    if args.text:
        text = args.text
        source = "INPUT"
    elif args.file:
        try:
            with open(args.file, encoding="utf-8") as f:
                text = f.read()
            source = args.file
        except OSError as e:
            print("cannot read %s: %s" % (args.file, e))
            sys.exit(2)
    else:
        # demo
        text = ("Internet usage increases the probability of nonfarm employment by about nine percent, "
                "and the effect is strongest for households with limited education. These results suggest "
                "that digital access reshapes rural labor markets, though we cannot rule out unobserved "
                "heterogeneity. In the context of the implementation of the consideration of the evaluation "
                "of the assessment of the framework the committee observed that the mechanism remained "
                "unsupported by the available evidence from the baseline survey of the participating villages.")
        source = "DEMO"

    groups = analyse_paragraphs(text)
    if not groups:
        print_report(build_report(None, source))
        return
    reports = [build_report(agg, source) for _, agg in groups]
    if len(reports) == 1:
        if args.json:
            print(json.dumps(reports[0], ensure_ascii=False, indent=2))
        else:
            print_report(reports[0])
        return
    overall = {"paragraphs": len(reports),
               "verdict": worst_verdict(reports),
               "n_red": sum(r["n_red"] for r in reports),
               "n_warn": sum(r["n_warn"] for r in reports),
               "n_markers": sum(r["n_markers"] for r in reports)}
    if args.json:
        print(json.dumps({"source": source, "profile": args.profile,
                          "paragraphs": reports, "overall": overall},
                         ensure_ascii=False, indent=2))
    else:
        print_paragraphs(reports, overall, source, args.profile)


if __name__ == "__main__":
    main()
