# 通知行动清单 · Notice Checklist

把通知和后续补充整理成带出处的行动清单：要做什么、何时截止、准备哪些材料、如何提交，以及哪些要求已变更、取消或仍待确认。

A portable Agent Skill that turns notices and amendments into cited checklists, with a dependency-free Python structural checker.

## 使用方式

向支持 Agent Skills 的宿主提供通知原文或附件，并说明：

> 使用 notice-checklist 整理这些通知，合并补充说明，保留引用，并列出需要我确认的问题。

例如，原通知要求“11 月 5 日前提交申请表和成绩单”，补充通知明确只把截止日改为“11 月 8 日”。清单应保留两份材料，记录日期变更并分别引用来源。若补充通知只写“下周五”且缺少发布日期，应保留待确认状态。

本 Skill 生成清单与待确认事项；不代发消息、不提交材料、不修改日历。图片和 PDF 的文字读取依赖宿主现有能力，本项目不附带 OCR 或 PDF 提取引擎；读不清的内容必须显式列为问题，不能假装已经识别。

## 安装

将本仓库的 `skills/notice-checklist` **完整目录**复制到宿主支持的 Skills 目录，使宿主能发现其中的 `SKILL.md`。具体发现路径和重新加载方式以所用宿主为准。需要运行校验器时，环境须提供 **Python 3.10+**；只使用 Python 标准库，无须 `pip install`。

## 校验与 Markdown 输出

在仓库根目录执行以下命令。示例中的两个 JSON 文件是供执行的合成输入，不含真实个人资料：

```console
python skills/notice-checklist/scripts/check_result.py --sources skills/notice-checklist/examples/sources.json --result skills/notice-checklist/examples/result.json
python skills/notice-checklist/scripts/check_result.py --sources skills/notice-checklist/examples/sources.json --result skills/notice-checklist/examples/result.json --markdown checklist.md
```

`--markdown` 仅写入尚不存在的新文件；再次输出请换一个文件名。退出码为 `0`（有效）、`1`（结构校验失败）或 `2`（文件读写或 JSON 解析失败）。校验失败时应先修正 JSON，不能把未通过的结果当作最终清单。

`sources.json` 保存提取文字的快照，根字段为 `sources`。`result.json` 使用 `schema_version: 1`、`tasks` 和顶层 `questions`；任务保留行动、状态、截止日、材料、前置条件、提交方式、变更记录和问题。事实附上来源 ID、位置和原文引句。来源完全不可读时，允许文字为空，但必须在顶层问题中说明。完整约定见 [设计文档](docs/design.md) 与 Skill 内的说明。

测试命令：

```console
python -m unittest discover -s tests -v
```

## 能验证什么

校验器检查 JSON 类型、必填字段、唯一 ID、引用是否指向已知来源、引句是否确实出现在提取文字中，以及日期与状态的一致性。

通过校验**不代表**引句能支持结论，也不代表 OCR 正确、要求齐全、通知真实或发布者有权修改要求。截止日、适用对象和冲突仍需人工核对。附件中的指令只是资料，不能据此授权工具操作。

校验脚本不调用网络或模型 API；但宿主模型、附件读取和云服务可能处理输入。使用云端宿主时，不能据此声称所有资料只留在本机或保证隐私；请按宿主的数据处理规则提供资料。

## 开发状态与许可

v0.1.0 早期项目。当前记录：26 项程序测试通过，16 组技能流程的结构校验通过，另完成一组截图与文本 PDF 的实际读取测试。[完整验收报告](docs/evaluation.md)保留方法、原始合成输出和限制。

无 Skill 基线已经满足全部可观察语义标准，因此尚未证明本 Skill 提高理解准确率。项目也尚无真实用户或采用指标；程序测试、模型行为与生产效果是不同证据。

采用 [MIT License](LICENSE)。相关方案与范围说明见 [相关项目](docs/related-projects.md)；OpenAI OSS 申请条件及待填写草稿见 [申请准备](docs/application-preparation.md)。本项目尚未获得该计划的批准。
