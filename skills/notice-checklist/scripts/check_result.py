"""Check notice extraction structure and literal citations, not semantic truth.

Python 3.10+; standard library only.
"""
import argparse
from datetime import date, datetime
import html
import json
from pathlib import Path
import re


def validate_result(sources, result):
    """Return diagnostics; an empty list means structural checks passed only."""
    errors = []

    def fields(value, required, path):
        if not isinstance(value, dict):
            errors.append(f"{path}: expected an object")
            return False
        missing, extra = required - value.keys(), value.keys() - required
        if missing:
            errors.append(f"{path}: missing fields {', '.join(sorted(missing))}")
        if extra:
            errors.append(f"{path}: unknown fields {', '.join(sorted(map(str, extra)))}")
        return not missing and not extra

    def string(value, path, allow_empty=False):
        if not isinstance(value, str) or (not allow_empty and not value.strip()):
            errors.append(f"{path}: expected {'a string' if allow_empty else 'a nonempty string'}")
            return False
        return True

    def strings(value, path):
        if not isinstance(value, list):
            errors.append(f"{path}: expected a list of strings")
            return False
        return all([string(item, f"{path}[{i}]") for i, item in enumerate(value)])

    source_text = {}
    unreadable = []
    if fields(sources, {"sources"}, "sources"):
        if not isinstance(sources["sources"], list) or not sources["sources"]:
            errors.append("sources.sources: expected a nonempty list")
        else:
            for i, source in enumerate(sources["sources"]):
                path = f"sources.sources[{i}]"
                if not fields(source, {"id", "label", "text"}, path):
                    continue
                valid_id = string(source["id"], path + ".id")
                string(source["label"], path + ".label")
                valid_text = string(source["text"], path + ".text", allow_empty=True)
                if valid_id and source["id"] in source_text:
                    errors.append(path + ".id: duplicate source id")
                elif valid_id and valid_text:
                    source_text[source["id"]] = source["text"]
                    if not source["text"].strip():
                        unreadable.append(source["id"])

    def fact(value, path, deadline=False):
        required = {"text", "evidence", "iso"} if deadline else {"text", "evidence"}
        if not fields(value, required, path):
            return
        string(value["text"], path + ".text")
        evidence = value["evidence"]
        if not isinstance(evidence, list) or not evidence:
            errors.append(path + ".evidence: expected at least one citation")
            return
        for i, item in enumerate(evidence):
            loc = f"{path}.evidence[{i}]"
            if not fields(item, {"source_id", "location", "quote"}, loc):
                continue
            valid_id = string(item["source_id"], loc + ".source_id")
            valid_quote = string(item["quote"], loc + ".quote")
            string(item["location"], loc + ".location")
            if valid_id:
                if item["source_id"] not in source_text:
                    errors.append(loc + ".source_id: unknown source")
                elif valid_quote and item["quote"] not in source_text[item["source_id"]]:
                    errors.append(loc + ".quote: exact text not found in this source")
        if deadline and value["iso"] is not None:
            iso = value["iso"]
            try:
                if not isinstance(iso, str):
                    raise ValueError()
                if re.fullmatch(r"\d{4}-\d{2}-\d{2}", iso):
                    date.fromisoformat(iso)
                elif re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)", iso):
                    datetime.fromisoformat(iso.replace("Z", "+00:00"))
                else:
                    raise ValueError()
            except ValueError:
                errors.append(path + ".iso: expected a valid YYYY-MM-DD or timestamp with UTC offset")

    if not fields(result, {"schema_version", "tasks", "questions"}, "result"):
        return errors
    if type(result["schema_version"]) is not int or result["schema_version"] != 1:
        errors.append("result.schema_version: expected integer 1")
    strings(result["questions"], "result.questions")
    if unreadable and not result["questions"]:
        errors.append("result.questions: unreadable sources require a visible question: " + ", ".join(unreadable))
    if not isinstance(result["tasks"], list):
        errors.append("result.tasks: expected a list")
        return errors
    ids = set()
    required = {"id", "action", "status", "deadline", "materials", "prerequisites", "submission", "changes", "questions"}
    for i, task in enumerate(result["tasks"]):
        path = f"result.tasks[{i}]"
        if not fields(task, required, path):
            continue
        if string(task["id"], path + ".id"):
            if task["id"] in ids:
                errors.append(path + ".id: duplicate task id")
            ids.add(task["id"])
        if task["status"] not in ("active", "cancelled", "needs_confirmation"):
            errors.append(path + ".status: expected active, cancelled or needs_confirmation")
        fact(task["action"], path + ".action")
        for key in ("materials", "prerequisites", "changes"):
            if not isinstance(task[key], list):
                errors.append(path + "." + key + ": expected a list")
            else:
                for j, value in enumerate(task[key]):
                    fact(value, f"{path}.{key}[{j}]")
        strings(task["questions"], path + ".questions")
        if task["submission"] is not None:
            fact(task["submission"], path + ".submission")
        if task["deadline"] is not None:
            fact(task["deadline"], path + ".deadline", deadline=True)
            if isinstance(task["deadline"], dict) and task["deadline"].get("iso") is None and task["status"] != "cancelled":
                if task["status"] != "needs_confirmation" or not task["questions"]:
                    errors.append(path + ".deadline: unresolved date requires confirmation status and a question")
        if task["status"] == "needs_confirmation" and not task["questions"]:
            errors.append(path + ".questions: confirmation requires a visible question")
        if task["status"] == "cancelled" and not task["changes"]:
            errors.append(path + ".changes: cancelled task requires a cited change")
    return errors


def render_markdown(sources, result):
    """Render validated facts; source markup remains data."""
    errors = validate_result(sources, result)
    if errors:
        raise ValueError("; ".join(errors))

    def escape(text):
        text = html.escape(text, quote=False).replace("\\", "\\\\")
        for char in (chr(96), "*", "_", "[", "]", "|", "!", "~"):
            text = text.replace(char, "\\" + char)
        return text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")

    citations = []

    def show(value):
        if value is None:
            return "未提供"
        refs = []
        for evidence in value["evidence"]:
            if evidence not in citations:
                citations.append(evidence)
            refs.append(str(citations.index(evidence) + 1))
        return escape(value["text"]) + "〔" + ",".join(refs) + "〕"

    lines = ["# 通知核对清单", "", "本表须回看原文核对；结构校验不证明理解正确、材料完整或来源真实。", "", "## 当前事项", ""]
    active = [task for task in result["tasks"] if task["status"] != "cancelled"]
    if active:
        lines += ["| 状态 | 事项 | 截止原文 | 材料／前提 | 提交方式 |", "|---|---|---|---|---|"]
        for task in active:
            status = "待确认" if task["status"] == "needs_confirmation" else "待办"
            requirements = "；".join(show(item) for item in task["materials"] + task["prerequisites"]) or "未提供"
            lines.append(f"| {status} | {show(task['action'])} | {show(task['deadline'])} | {requirements} | {show(task['submission'])} |")
    else:
        lines.append("没有列出可执行事项；请结合下方取消和待确认记录检查。")
    lines += ["", "## 已取消事项", ""]
    cancelled = [task for task in result["tasks"] if task["status"] == "cancelled"]
    lines += ["- " + show(task["action"]) for task in cancelled] or ["无。"]
    lines += ["", "## 变更记录", ""]
    changes = [(task, change) for task in result["tasks"] for change in task["changes"]]
    lines += [f"- {escape(task['id'])}：{show(change)}" for task, change in changes] or ["无。"]
    lines += ["", "## 待确认", ""]
    questions = result["questions"] + [f"{task['id']}：{q}" for task in result["tasks"] for q in task["questions"]]
    lines += ["- " + escape(question) for question in questions] or ["无已记录问题；仍需核对原文。"]
    lines += ["", "## 出处摘录", ""]
    labels = {source["id"]: source["label"] for source in sources["sources"]}
    for i, evidence in enumerate(citations, 1):
        lines.append(f"{i}. {escape(evidence['source_id'])} · {escape(labels[evidence['source_id']])} · {escape(evidence['location'])}：{escape(evidence['quote'])}")
    if not citations:
        lines.append("无引用；没有据此生成事项。")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", required=True, type=Path)
    parser.add_argument("--result", required=True, type=Path)
    parser.add_argument("--markdown", type=Path, help="Write a NEW checklist file after structural validation")
    args = parser.parse_args()
    try:
        sources = json.loads(args.sources.read_text(encoding="utf-8-sig"))
        result = json.loads(args.result.read_text(encoding="utf-8-sig"))
        errors = validate_result(sources, result)
        if errors:
            print(json.dumps({"valid": False, "errors": errors}, ensure_ascii=True))
            return 1
        if args.markdown:
            with args.markdown.open("x", encoding="utf-8", newline="\n") as output:
                output.write(render_markdown(sources, result))
        print(json.dumps({"valid": True, "semantic_review_required": True}, ensure_ascii=True))
        return 0
    except (OSError, ValueError) as error:
        print(json.dumps({"valid": False, "errors": [str(error)]}, ensure_ascii=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
