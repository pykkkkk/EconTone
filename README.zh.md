# EconTone

**博弈思想的经济学写作优化。** 五个 skill，一个均衡。

[English](README.md) | **中文**

<p align="center">
  <img src="https://img.shields.io/badge/skills-5-111111?style=flat-square" alt="5 skills">
  <img src="https://img.shields.io/badge/game-lexicographic_Stackelberg-E8B23A?style=flat-square" alt="game model">
  <img src="https://img.shields.io/badge/glossary-135_term_pairs-2A4A6B?style=flat-square" alt="glossary">
  <img src="https://img.shields.io/badge/prosody-9_metrics_5_markers-111111?style=flat-square" alt="prosody">
  <img src="https://img.shields.io/badge/rules-32-E8B23A?style=flat-square" alt="writing rules">
  <img src="https://img.shields.io/badge/checks-12%2F12-2A4A6B?style=flat-square" alt="checks">
</p>

---

## 目录

- [为什么使用](#为什么使用) · [流程](#流程) · [证据](#证据)
- [安装](#安装) · [怎么提问](#怎么提问) · [基于 DSH 开发](#基于-dsh-开发)
- [文献](#文献) · [致谢](#致谢) · [许可](#许可) · [状态：测试阶段](#状态测试阶段)

润色一段文字并非单一决策，而是一组冲突：句子更紧，术语可能失准；主张更清晰，限定可能消失；节奏更顺，力度可能变弱。多数工具以流畅度评分隐式化解该冲突。

EconTone 将其建模为**博弈**。三名参与者，动作集互斥：`econtone-polish` 在句内改写，受硬约束限制；`econtone-ai-trace` 清理语体而不削弱该约束；`econtone-prosody` 仅移动句子边界，因而**在构造上**无法损伤前两者已确立的内容。第四个 skill 在改动前评分，第五个计算均衡。

**均衡由脚本计算，不由投票决定。** `play.py` 测量每个候选动作、套用规则、输出证书：调度、被接受的动作、被拒绝的动作，以及拒绝它的那个数字。

```
术语         硬约束——不可交易
主张强度     硬约束——不可交易
AI 痕迹      次级目标
节奏         增强项——最大化后即停止
```

## 为什么使用

| | |
|---|---|
| **先测量，后编辑** | 评分给出**编辑幅度**：25% 时只能修正错误，98% 时可重构。 |
| **动作集互斥** | 韵律席无权改词，故其动作无法削弱术语或主张强度；该性质由守卫脚本验证，而非依赖模型自律。 |
| **记录拒绝** | 被拒动作及其数字一并写入证书。被拒的动作即证据。 |
| **五个 skill 各自独立** | 只润色、只查痕迹、只调节奏，均可单独使用。 |

## 流程

```
草稿 → econtone-score（评分与幅度）→ econtone-polish → econtone-ai-trace
     → econtone-prosody → econtone-equilibrium（组合与证书）
```

> **关于耗时。** 一次完整的均衡求解会用四个脚本测量每个候选动作，并在每次接受后重新测量；
> 处理一节通常在**十分钟以上**。它不是卡住了，而是在测量。发起后可以暂时离开，回来看证书即可。

字典序而非加权：节奏收益不能换取规范术语，痕迹修正不能换取过度主张。

## 证据

| 事项 | 数字 |
|---|---|
| 韵律带宽的标定语料 | 42 篇开放获取论文，22 种期刊，802 个正文段落 |
| 检查项 | 12/12，无需模型、无需联网 |
| 阈值不可漂移 | 自检断言与 7 个黄金样本（4 必 PASS，3 必 REVISE） |
| 写作规则来源 | 6 份研究生写作指南，32 条规则逐条标注出处 |

## 安装

**一行指令。** 把下面这句发给你的 agent：

> https://github.com/pykkkkk/EconTone —— 安装这个 skill 包。

无需构建、无需修改清单、无需安装依赖。也可手动执行：

```bash
git clone https://github.com/pykkkkk/EconTone.git
cp -r EconTone/skills/econtone-* ~/.dsh/skills/
```

## 依赖

**无需安装任何第三方包。** 全部脚本仅使用 Python 标准库：`argparse`、`collections`、`importlib`、
`itertools`、`json`、`math`、`os`、`re`、`shutil`、`statistics`、`subprocess`、`sys`、`tempfile`。
不含 `numpy`、`pandas`，无构建步骤。

| 项目 | 状态 |
|---|---|
| Python 3.8 及以上 | 必需（建议 3.10+） |
| 任何第三方包 | **非必需** |
| `nltk` + `cmudict` | **可选** —— 见下 |

**可选：更准确的重音测量。** `econtone-prosody` 需要估计重读音节。若装有 `nltk` 及其 `cmudict` 语料，
则使用词典标注的真实重音模式；否则回退到启发式估计，并在输出中注明
（`stress source: heuristic (nltk missing)`）。参考带仍然有效，只是测量更粗。启用方式：

```bash
pip install nltk
python -m nltk.downloader cmudict
```

其余全部功能——三个扫描器、评分卡、均衡引擎、12 项检查——在未安装任何依赖的 Python 上均可运行。

## 怎么提问

五个 skill 不是一个按钮。提问方式决定执行哪一个、允许走多远。详见
[`docs/prompting-zh.md`](docs/prompting-zh.md)（[English](docs/prompting.md)）：各 skill 的输入输出、
三种调用方式、提示词的四个要素、六个模板、六类常见错误提示。

## 基于 DSH 开发

本包在 **DeepSeek Harness（DSH）** 上开发，采用其 skill 格式发布：每个成员是一个目录，内含 `SKILL.md`
（YAML frontmatter + 指令），可选 `scripts/` 与 `references/`。依赖到此为止——没有脚本 import DSH 的 API，
没有脚本读取 harness 变量，扫描器均为标准库 Python。

| 环境 | 运行方式 |
|---|---|
| DSH | 原生支持，五个 skill 直接加载 |
| 任何读取 `SKILL.md` 的 harness | 原生支持，目录结构相同 |
| 纯 shell / CI | `python tests/run_all.py`（12 项，无模型、无网络） |

## 文献

完整文献表见 [`docs/references.md`](docs/references.md)（APA 第 7 版，五节）。文献列出的是**依赖来源**：
方法定义、写作建议、检索过的目录；本项目中的**数值**（带宽、阈值、标记等级、`risk_index` 的构成）均为
自身标定，不出自任何一篇被引文献。

## 致谢

- **DeepSeek Harness** —— 开发环境与发布格式。
- **`logo-design`**（MIT，[`kaankiziltug/logo-design-skill`](https://github.com/kaankiziltug/logo-design-skill)）——
  设计流程与 `svg_audit.py`。标志本身自绘；其 1,432 个真实标志库仅用于了解品类既有形状并加以规避，
  未描摹任何一件。详见 [`docs/logo-notes.md`](docs/logo-notes.md)。
- **标定语料** —— 42 篇开放获取论文，列于 [`docs/references.md`](docs/references.md)，不随仓库分发。

## 许可

代码 Apache-2.0，文本 CC0 1.0（无需署名），名称与标志不授权。理由见 [`LICENSING.md`](LICENSING.md)。

## 状态：测试阶段

框架完整，每条判定路径都有脚本，但**评估尚薄**：两篇文本、八个联盟、无大规模基准，评分卡阈值亦为暂定。
现有数字描述的是这些工具，而非证明这些工具正确。
