# econtone-ai-trace

**AI 痕迹的测量与清理。** 先测量、再改写、后重测，输出前后差值表。

[English](README.md) | **中文**

## 三个扫描器

```bash
python scripts/scan_ai_traces.py draft.md      # 标点痕迹、过渡词、句式模板
python scripts/scan_register.py draft.md       # 语域缺陷、空泛强化词
python scripts/scan_detectability.py draft.md  # 统计代理指标与 risk_index
```

`risk_index` 由已发表代理指标按固定权重合成，用于**内部比较**，不是任何商业检测器的预测值，也不应作为优化目标。

## 输入与输出

| 输入 | 输出 |
|---|---|
| 存在 AI 痕迹的文本 | 基线指标、改写稿、重测指标、差值表 |

## 关键指标

| 指标 | 含义 | 参考带 |
|---|---|---|
| `Burstiness` | 句长方差系数 | ≥50 类人，35–50 警告，<35 红灯 |
| `risk_index` | 代理指标合成值 | 仅用于同文对比 |
| 句式模板密度 | 重复句式占比 | 越低越好 |

## 不做什么

- 不保证通过任何检测器；
- 不为降低指标而拆句——句界属于 `econtone-prosody`；
- 不以牺牲术语或主张强度换取更低的风险值。
