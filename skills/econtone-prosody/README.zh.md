# econtone-prosody

**句界与节奏。** 只移动句子边界、调整语序与虚词，不改动实词内容。

[English](README.md) | **中文**

## 输入与输出

| 输入 | 输出 |
|---|---|
| 朗读时节奏失衡的段落 | 句界调整（拆分、合并、语序、语态、虚词）、九项指标、标记判定 |

```bash
python scripts/prosody_check.py draft.md --profile abstract
python scripts/rhythm_score.py draft.md --profile abstract
python scripts/segmentation_guard.py before.md after.md
```

## 九项指标与五个标记

指标包括 `nPVI`、重音占比、重音交替、重音间隔变异系数、每词音节数、句长统计与排比密度。

五个红线标记：`SLURRY`（长句堆叠）、`POUNDING`（重音串）、`ROBOTIC`（句长均匀）、`DENSE`（密度过高）、
`FLAT`（句长无变化）。

## 守卫

`segmentation_guard.py` 判定一次改动是否仅为句界调整：

- `boundary-only` —— 实词多重集不变，合规；
- `licensed-rewording` —— 仅虚词变化，合规；
- `illegal` —— 实词增删，拒绝。

## 节奏是增强项

本 skill 最大化接近度得分，达到局部最优即停止，**不强制进入参考带**。若某动作会触发红线标记或使痕迹指标恶化，
应报告而非执行。

## 限制

指标基于音节与词长的近似估计，非音系学标注；参考带由 42 篇论文标定，对非经济学文体（如法学评论）未必适用。
