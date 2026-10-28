# 实际媒体读取观察

- 输入仅为 outputs/notice-checklist/tests/media/01-original-notice.png 与 02-amendment.pdf。未读取示例 JSON、测试代码、设计、行为评分表、根生成脚本或以前评估。
- PNG 用 host view_image 实际查看后人工逐行转录；没有使用 OCR 程序。图片清晰，截止、材料和时区可读，位置按图片真实区域记录。
- PDF 为 1 页，用 pypdf 从原件提取文字；随后用 pypdfium2 渲染 amendment-page-1.png 并通过 view_image 核对整页，关键文字与提取一致。
- 补充通知明确指向 10 月 26 日原通知。人工语义复核确认：截止改为 2026-11-02 12:00（UTC+08:00）；上传 PDF；报名表和照片保留；无取消事项。上传入口未提供，已列为任务级待确认。
- 两份原件均写明合成测试样例，非真实报名。清单保留该上下文，未提交材料、联网或联系任何人；原件未修改。
- 此测试验证 host 提供的图片视觉读取、PDF 文本提取与渲染能力，不能称为技能自带 OCR，也未验证扫描型 PDF 的 OCR 能力。
- 按技能文档运行 check_result.py --sources sources.json --result result.json --markdown checklist.md；首次执行实际进程退出码 0，输出 {"valid": true, "semantic_review_required": true}。
- 已回读 checklist.md 并与两份原件人工比对。检查器通过仅证明结构与字面引用通过，不能证明完整性、语义或来源真实性。
