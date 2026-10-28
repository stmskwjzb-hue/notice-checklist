# OpenAI OSS 申请准备

核对日期：**2026-10-28**。公开仓库：[stmskwjzb-hue/notice-checklist](https://github.com/stmskwjzb-hue/notice-checklist)。申请已由用户暂缓，尚未提交，也未获得批准。若以后继续申请，提交前须再次核对官方页面，并由真实申请人检查全部内容。

## 官方条件与本项目现状

[申请表](https://openai.com/form/codex-for-oss/) 与 [官方项目说明](https://developers.openai.com/community/codex-for-oss) 面向开源维护者，考虑使用情况、生态意义及持续维护证据。官方列出的支持包括六个月 ChatGPT Pro（含 Codex）、有条件的 Codex Security，以及用于符合条件的开源维护工作的 API credits。API credits 是额外且酌情提供的支持，不随 Pro 自动保证发放。

[项目条款](https://learn.chatgpt.com/docs/codex-for-oss-terms) 要求如实提供身份、仓库及维护角色，可能进一步核验；是否入选和福利范围由 OpenAI 决定，提交不保证获批。福利通常不可转让；条款可能变化，申请材料不应含保密信息。

本项目是早期 MIT Agent Skill，尚无真实用户、下载量或其他采用指标，生态价值尚未证明。可解释预期用途并提供实际开发证据，但不能把“开源”或“是 Skill”当作一定符合条件，更不能编造 stars、用户或维护记录。

## 仍需申请人提供

以下内容应由真实申请人私下填入官方表单，不要为了准备申请而公开个人邮箱或组织信息：

| 字段 | 待补充内容 |
| --- | --- |
| First name / Last name | 真实姓名 |
| Email | 与有效 ChatGPT 账号关联的邮箱 |
| GitHub username | stmskwjzb-hue |
| GitHub repository URL | https://github.com/stmskwjzb-hue/notice-checklist |
| Maintainer role | 实际 primary 或 core maintainer 身份及可核验的关系 |
| OpenAI Organization ID | 如申请 API credits，提供对应 API 组织的真实 ID |
| Requested support | 由申请人选择是否需要 API credits / Codex Security |

表单的资格说明、API 用途说明及补充说明均显示最多 500 字符。下列英文草稿分别低于 500 字符；它们是待复核文本，不含假身份或假指标。若后续项目事实变化，提交前应同步修改。

## Why does this repository qualify? — 草稿

```text
Notice Checklist is an early-stage MIT-licensed Agent Skill for turning notices and amendments into traceable checklists. It preserves cited requirements, cancellations and unresolved questions, with a dependency-free Python structural checker. It has no users or adoption metrics yet. Its proposed value is a small, reusable workflow for everyday notices; ecosystem impact remains unproven.
```

## How will you use API credits for your project? — 可选草稿

仅在申请人确实打算开展以下工作并选择申请 API credits 时使用：

```text
If awarded API credits, I would use them for reproducible evaluations of notice extraction, amendment handling and citation fidelity on synthetic fixtures, plus regression review during maintenance. The skill itself requires no API integration. This is an early-stage proposal with no current users, adoption metrics or established API workload. I would publish evaluation methods and limitations.
```

## 发布与提交前待办

1. 核实 stmskwjzb-hue 是实际维护者账号，并核对公开仓库中的最终源码与许可。
2. 把最终源码、MIT 许可、合成示例及实际测试和评估证据发布到仓库；保留失败结果与限制说明。
3. 用最终运行记录更新开发状态，复核文档中的命令和示例。
4. 由申请人核实两段草稿和隐私信息、阅读当时有效的条款，再自行决定是否提交。

目前不能声称已被 OpenAI 接纳、已有社区采用，或 API credits 已获批。此准备文档本身不执行发送、提交或发布操作。
