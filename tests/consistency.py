#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consistency.py — vertical and horizontal checks across the repository."""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
problems, notes = [], []


def fail(rule, detail):
    problems.append("%-16s %s" % (rule, detail))


MD = []
for dp, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
    for f in files:
        if f.endswith(".md"):
            MD.append(os.path.join(dp, f))

# A. structure + frontmatter
skill_dirs = sorted(d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d)))
if len(skill_dirs) != 5:
    fail("structure", "expected 5 skills, found %d" % len(skill_dirs))
for d in skill_dirs:
    for f in ("SKILL.md", "README.md"):
        if not os.path.exists(os.path.join(SKILLS, d, f)):
            fail("structure", "%s missing %s" % (d, f))
    head = open(os.path.join(SKILLS, d, "SKILL.md"), encoding="utf-8").read(400)
    m = re.search(r"^name:\s*(\S+)", head, re.M)
    if not m or m.group(1) != d:
        fail("frontmatter", "%s name=%r" % (d, m.group(1) if m else None))

# B. pack.json vs tree
pack = json.load(open(os.path.join(ROOT, "pack.json"), encoding="utf-8"))
names = sorted(m["name"] for m in pack["members"])
if names != skill_dirs:
    fail("pack.json", "members %s != dirs %s" % (names, skill_dirs))
for m in pack["members"]:
    if not os.path.isdir(os.path.join(ROOT, m["path"].lstrip("./"))):
        fail("pack.json", "%s path missing" % m["name"])

# C. links and path claims
link = re.compile(r"\]\(([^)#\s]+)\)")
claim_re = re.compile(r"`((?:skills|docs|examples|tests|logo)/[^`\s]+)`")
for p in MD:
    text = open(p, encoding="utf-8", errors="replace").read()
    rel = os.path.relpath(p, ROOT)
    for target in link.findall(text):
        if target.startswith(("http", "mailto", "#")):
            continue
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(p), target))):
            fail("broken link", "%s -> %s" % (rel, target))
    for claim in claim_re.findall(text):
        if "*" in claim:
            continue
        cand = claim.rstrip("/")
        ok = (os.path.exists(os.path.join(ROOT, cand))
              or os.path.exists(os.path.normpath(os.path.join(os.path.dirname(p), cand))))
        if not ok:
            fail("path claim", "%s -> %s" % (rel, claim))

# D. script claims resolve inside the skill
for d in skill_dirs:
    text = open(os.path.join(SKILLS, d, "SKILL.md"), encoding="utf-8").read()
    for name in re.findall(r"(?:scripts|tests)/([A-Za-z0-9_.]+\.(?:py|json))", text):
        if not (os.path.exists(os.path.join(SKILLS, d, "scripts", name))
                or os.path.exists(os.path.join(SKILLS, d, "tests", name))):
            fail("script claim", "%s -> %s" % (d, name))

# E. retired names
for p in MD + [os.path.join(ROOT, "pack.json")]:
    if "econtone-committee" in open(p, encoding="utf-8", errors="replace").read():
        fail("retired name", os.path.relpath(p, ROOT))

# F. links into a skill must name a real skill
skill_link = re.compile(r"(?:^|[\s(])skills/(econtone-[a-z-]+)")
for p in MD:
    for name in skill_link.findall(open(p, encoding="utf-8", errors="replace").read()):
        if name not in skill_dirs:
            fail("unknown skill", "%s -> %s" % (os.path.relpath(p, ROOT), name))

# G. counts
readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
run_all = open(os.path.join(ROOT, "tests", "run_all.py"), encoding="utf-8").read()
n_checks = len(re.findall(r"^\s+\(", run_all, re.M))
notes.append("checks in run_all.py: %d" % n_checks)
for a, b in re.findall(r"(\d+)/(\d+) checks", readme):
    if int(b) != n_checks:
        fail("count claim", "README says %s/%s, run_all has %d" % (a, b, n_checks))
if "five skills" in readme.lower() and len(skill_dirs) != 5:
    fail("count claim", "README says five skills")

# H. version
m = re.search(r"^## (\d+\.\d+\.\d+)", open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8").read(), re.M)
if m and m.group(1) != pack.get("version"):
    fail("version", "pack.json %s != CHANGELOG %s" % (pack.get("version"), m.group(1)))

# I. every selftest script is in CI
for dp, _, fs in os.walk(os.path.join(ROOT, "skills")):
    for f in fs:
        if not f.endswith(".py"):
            continue
        path = os.path.join(dp, f)
        text = open(path, encoding="utf-8").read()
        if 'argv[1] == "selftest"' in text:
            rel = os.path.relpath(path, ROOT).replace("\\", "/")
            if rel not in run_all:
                fail("untested", "%s not in run_all.py" % rel)



# K. the --profile vocabulary must agree across every script that accepts it
PROFILE_RE = re.compile(r'add_argument\("--profile"[^)]*\)')
CHOICE_RE = re.compile(r'choices=\[([^\]]*)\]')
profiles = {}
for dp, _, fs in os.walk(os.path.join(ROOT, "skills")):
    for f in fs:
        if not f.endswith(".py"):
            continue
        path = os.path.join(dp, f)
        src = open(path, encoding="utf-8").read()
        for decl in PROFILE_RE.findall(src):
            m = CHOICE_RE.search(decl)
            rel = os.path.relpath(path, ROOT).replace("\\", "/")
            if not m:
                fail("profile choices", "%s accepts --profile without choices" % rel)
                continue
            vals = tuple(sorted(v.strip().strip('"\'') for v in m.group(1).split(",") if v.strip()))
            profiles[rel] = vals
if len({v for v in profiles.values()}) > 1:
    names = {v: [k for k, x in profiles.items() if x == v] for v in set(profiles.values())}
    fail("profile choices", "disagreement: %s" % names)
notes.append("profile vocabularies: %s" % (sorted(set(profiles.values())) if profiles else "none"))

# J. schema drift: every move field play.py reads must be declared in move.schema.json
PLAY = os.path.join(ROOT, "skills", "econtone-equilibrium", "scripts", "play.py")
SCHEMA = os.path.join(ROOT, "skills", "econtone-equilibrium", "scripts", "move.schema.json")
if os.path.exists(PLAY) and os.path.exists(SCHEMA):
    play_src = open(PLAY, encoding="utf-8").read()
    fields = set(re.findall(r'mv\["(\w+)"\]', play_src)) | set(re.findall(r'mv\.get\("(\w+)"', play_src))
    declared = set(json.load(open(SCHEMA, encoding="utf-8"))["items"]["properties"])
    for f in sorted(fields - declared):
        fail("schema drift", "play.py reads move field %r, schema does not declare it" % f)
    if not fields:
        fail("schema drift", "no move fields found in play.py -- pattern changed?")

if "--json" in sys.argv:
    print(json.dumps({"problems": problems, "notes": notes}, ensure_ascii=False, indent=2))
else:
    print("CONSISTENCY — %s" % ROOT)
    for n in notes:
        print("  note  %s" % n)
    for p in problems:
        print("  FAIL  %s" % p)
    if not problems:
        print("  PASS  structure | pack.json | links | path claims | script claims")
        print("        retired names | cross-skill links | counts | version | CI coverage")
sys.exit(1 if problems else 0)
