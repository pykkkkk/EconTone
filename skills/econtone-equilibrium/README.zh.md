# econtone-equilibrium

**编排。** 不投票，求解：给定动作集与约束，哪个组合稳定。

[English](README.md) | **中文**

## 三名参与者

| 参与者 | skill | 动作 | 不得违反 |
|---|---|---|---|
| 领导者 | `econtone-polish` | 句内改写 | 意义不变 |
| 第二位 | `econtone-ai-trace` | 句内改写 | 领导者设定的有效性 |
| 跟随者 | `econtone-prosody` | 句界、语序、语态、虚词 | 守卫、标记停止、痕迹清洁度 |

## 均衡的计算

```bash
python scripts/play.py --current draft.md --moves moves.json --profile abstract --rounds 3
python scripts/equilibrium.py shapley data.json
python scripts/equilibrium.py bargain data.json
python scripts/equilibrium.py core data.json
```

`play.py` 按字典序判定：术语命中不得增加 → 风险档位不得恶化（或单次上升不超过 10） → 句界动作需守卫
LEGAL、无标记、`burstiness` 未进入红灯 → 存活动作中任一可测改善即接受。

多轮：每轮接受至多一个动作，随后以新文本重测。基线已变动的候选标记为 `stale` 并跳过，避免静默撤销上一轮成果。

## 机械修正不在博弈内

拼写与语法错误是**准入条件**，在首轮之前无条件应用，记入证书的 `auto_applied`，不参与计票。

## 交付四段

1. 定稿文本；
2. 均衡结果（证书：胜出动作、测得增量、停止条件）；
3. 修改动作（接受与否，及决定它的数字）；
4. 其他选项（被拒动作改写的建议，及采纳代价）。

## 限制

`play.py` 只在**已有候选集**上迭代，不自行生成新候选；候选集的完备性决定均衡质量。均衡是相对于已提出动作集的
局部结果，不是全局最优。
