# 相关项目与本项目范围

核对日期：**2026-10-28**。以下仅记录项目自身文档描述的用途，未独立测试其效果，也不是完整市场调查。已有方案覆盖相近需求，不能声称本项目首创或独一无二。

| 一手来源 | 项目文档描述 | 与 Notice Checklist 的关系 |
| --- | --- | --- |
| [DueFlow](https://github.com/Ustinian5/DueFlow) | 面向 macOS 的本地优先截止日规划工具；接收文本、文件、截图等资料，提取任务，并提供倒排计划、风险检查与日历导出。 | 同样把分散通知变成任务。本项目范围更小，交付可移植 Skill 和结构校验器，重点记录补充通知、取消与逐项引用。 |
| [Photocalia](https://github.com/m-idriss/photocalia) | 从图片或 PDF 提取日历事件，允许导出前编辑并生成 `.ics` 文件。 | 都涉及附件中的时间信息。本项目生成行动清单和待确认问题，不提供日历服务；附件提取依赖宿主。 |
| [Hermes Agent: Meeting Action Items](https://github.com/NousResearch/hermes-agent/blob/main/skills/productivity/meeting-action-items/SKILL.md) | 从已有会议记录提取带来源的决定、责任人和行动项；保留未确定事项，并在用户批准后处理外部记录。 | 都使用证据约束行动项。本项目面向通知及其修订，采用独立 JSON 契约与 Python 校验器。 |

本项目独立编写代码和 Skill 指令；上述链接用于确认需求已有相关实践，未复制其代码、提示词或素材。范围不同不代表效果更好，是否有实际价值仍需真实使用和公开评估证据。
