---
name: econtone-ai-trace
description: >
  Measured anti-AI-trace pass for English economics and management prose that already
  exists: three standard-library scanners measure punctuation traces, transition-peg
  density, repeated syntactic templates, long-sentence load, diction defects, and the
  statistical proxies commercial detectors score (burstiness, formulaic density,
  self-repetition, MTLD, hedge density, paragraph shape). Runs baseline -> triage ->
  rewrite -> re-measure and delivers a before/after delta table. Load when a draft
  "reads like a model wrote it", when 去 AI 味 / AI 痕迹 / humanize / detector risk is
  the ask, or when econtone-polish hands off its Block A.
metadata:
  pack: econtone
  role: gate
---

# AI-Trace Gate (EconTone)

A draft can be correct, idiomatic, and still read as machine-written. This skill measures the
traces that make it read that way, rewrites them, and re-measures so the improvement is shown
rather than asserted.

## When to load

- The user asks to strip AI tells: 去 AI 味, AI 痕迹, humanize, "make it sound like a person".
- A draft is submission-ready except for voice, and the user wants evidence of change.
- `econtone-polish` hands off its Block A for the optional trace gate.

## When not to load

- The text is still being drafted — finish the content first.
- The user wants rhythm/cadence repair: that is `econtone-prosody`.
- The user wants terminology or register fixes with no trace dimension: `econtone-polish` Step 4.

### Step 2b — Scope: sentences are fixed

You may change words, syntax and punctuation **inside** a sentence. You may not split one sentence into
two, merge two into one, or reorder sentences: **sentence boundaries belong to `econtone-prosody`**, which
moves them without touching a word. If a fix only works by changing a boundary, record it in Block B as
`[BOUNDARY]` and hand it over — do not do it here.

## The measured loop

Load `references/anti_ai_trace_audit.md`: five stages (baseline -> triage -> rewrite ->
re-measure -> verify rhythm), the threshold table, the trace-to-fix mapping, and the pitfalls.
The three scanners do the measuring:

```bash
python scripts/scan_ai_traces.py manuscript.tex           # structure: punctuation, pegs, templates, long sentences, rhythm
python scripts/scan_register.py manuscript.tex --limit 8  # diction: defect bands and context probes
python scripts/scan_detectability.py manuscript.tex       # detector-facing proxies -> risk_index
```

Take a **baseline before editing**, re-run afterwards, and deliver a **before/after delta table**.
Three rules govern the loop:

1. **Density is the signal, not presence.** `respectively`, `rather than`, and a colon introducing a
   list are legitimate journal prose. Never zero out a probe to make a number look clean.
2. **Never read a falling sentence-length stdev as success on its own.** Deleting outliers and
   flattening the prose both lower it. Verify rhythm in the `[E]` block: healthy prose keeps
   *adjacent pairs within ±2 words* low and the *≥2× length ratio* high.
3. **The pass is a style pass.** Numbers, equations, citations, and exhibits are out of scope.
   Apply rewrites as exact-match replacements with a `count == 1` check so partial application
   cannot pass silently.

`scan_detectability.py` measures the *statistical proxies commercial AI detectors actually score*
and reports a `risk_index`. It is a **false-positive-risk diagnostic, not a detector**, and is never
optimised as a target; the honesty boundary and the era-stratified calibration are in
`references/anti_ai_trace_audit.md` §3b.

## Trace checklists

#### English AI-Trace Checklist

| Pattern | Why It Looks AI-Generated | Replacement |
|---------|---------------------------|-------------|
| Em dash `—` or colon `:` used to insert an explanatory clause mid-sentence | Overuse of both em dashes and colons for explanation is a hallmark of LLM output | Rethink: does the clause need to be an appositive? If so, use parentheses or a comma-restricted relative clause. If contrast or explanation is needed, use a sentence break instead. |
| "that is" as a clause-level connector | "that is" is AI's default restatement device; human writers prefer "i.e.," "namely," or rewrite without the restatement | Either use "i.e.," (followed by a comma, then the restatement) or eliminate the restatement and merge the content directly into the preceding text |
| "In other words" | Same as "that is" — restatement marker that real academic writing uses sparingly | Delete the phrase and integrate the clarification directly; if the restatement is truly necessary, use "that is," |
| "Note that" at sentence start | This is AI's go-to attention-drawing device; genuine academic prose uses "Note that" only in technical asides | If the sentence is a normal argumentative step, remove "Note that" and let the sentence stand on its own. If it is a genuine caution (e.g., about a data limitation), keep it. |
| "It is worth noting that" | Wordy, hedge-stacking, AI-preferred | Delete entirely and start with the factual content. |
| "respectively" at the end of a paired statement | Overused by AI to pair items; humans usually restructure to make the pairing clearer through parallel sentence construction | Either delete "respectively" and rewrite as two short sentences, or keep only when the pairing would be genuinely ambiguous without it |
| "In particular," / "Specifically," / "More broadly," at sentence start | AI overuses these as generic transition pegs. They create a mechanical paragraph texture when used in more than one out of every four sentences. | Vary transitions or use a content-carrying transition (e.g., "The indirect effect tells a different story: ..." instead of "In particular, the indirect effect...") |
| Overly symmetrical parallel structures | AI tends to produce clauses of equal length and identical grammar in successive sentences, producing a "recited" rhythm | Break the rhythm: vary sentence length, swap clause order, or use a short interrupting sentence |
| "Importantly," / "Critically," / "Notably," as sentence-opening adverbs | These adverbs are AI's shortcut for emphasis without evidence | Either incorporate the emphasis into the content ("The key result is that X increases Y by Z%") or remove the adverb entirely |
| Parenthetical hedge stacks: "potentially, ... may ... possibly" | AI stacks multiple hedging devices in a single clause | Keep at most one hedge per clause. Choose the strongest one justified by the evidence. |
| "thereby" + gerund clause | "thereby doing" is AI's preferred way to express result | Replace with "and thus VERB" (finite verb) or separate into a new sentence. Only keep "thereby + -ing" when it genuinely improves readability (rarely). |

#### Chinese AI-Trace Checklist

| Pattern | Why It Looks AI-Generated | Replacement |
|---------|---------------------------|-------------|
| 破折号 `——` 或冒号 `：` 连接解释性插入语 | AI 过量使用破折号和冒号代替括号或重述句 | 改用括号、逗号从句，或拆分句子。若为解释性内容，直接融入上下文。 |
| 引号 `「」` 或 `""` 标记术语或特殊用法 | AI 倾向于用引号标记每一个非日常词汇 | 只有初次定义的术语或用反讽义时使用引号。常规专业术语直接使用不加引号。 |
| "即"（that is）做句间重述 | 在中文学术写作中，AI 过量使用 "即" 重述上一句的内容 | 要么删除重述句合并内容，要么将 "即" 改为 "换言之"（更书面的中文），或直接使用标点（冒号或分号）引导重述。 |
| "需要注意的是" / "值得注意的是" | 典型 AI 提示语气，在中文顶刊中极少出现 | 直接删除，内容保持不变。 |
| "换言之" / "换句话说" 作为段内转接 | AI 在中文中仿照 "in other words" 直译 | 删除，将解释内容直接融入上下文。 |
| 连续的"第一，第二，第三，第四" | AI 偏好机械列举 | 改用实质性过渡（如 "在理论层面，……；在实证层面，……"），或调整段落结构减少列举层级。 |
| "与此同时" / "此外" 在每段段首 | AI 生成的段落过渡模板 | 根据逻辑关系替换为 "相对而言""相比之下""进一步说" 等更具体的连接语，或直接省略。 |
| "综上所述" 开头的结论段 | 大量中式英文论文的 AI 改写痕迹 | 直接陈述核心结论，不需要 "综上所述" 做过渡标记。 |
## Exit criteria

- No **defect-band** hit left unaddressed; context-band hits judged in context and reported.
- The delta table shows the direction of movement, with any probe deliberately left unchanged and
  the reason it was left (density, not zero).
- Numbers, equations, citations, and exhibit content unchanged.

## Files

- `scripts/scan_ai_traces.py` — structure probes (punctuation, pegs, templates, long sentences, rhythm)
- `scripts/scan_register.py` — diction probes, defect bands vs context bands
- `scripts/scan_detectability.py` — detector-facing proxies and `risk_index` (30-assertion selftest)
- `references/anti_ai_trace_audit.md` — the method, thresholds, trace-to-fix mapping, delta-table format

## Position in the EconTone pack

Final gate: `econtone-score` triages -> `econtone-polish` drafts -> `econtone-prosody` tunes rhythm ->
**`econtone-ai-trace`** checks the delivered text one last time. It runs **last** because it is the
delivery safeguard: a rhythm edit can reintroduce a stacked connective, and only this pass would see it.
Precedence runs the other way - terminology outranks traces, traces outrank rhythm - so when this pass
and the rhythm gate disagree, the trace fix stands and the rhythm verdict is re-measured.
