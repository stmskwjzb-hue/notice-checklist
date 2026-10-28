"""Behavior tests for the public checker, with hand-written source evidence."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "notice-checklist" / "scripts" / "check_result.py"


def sample():
    sources = {"sources": [
        {"id": "S1", "label": "原通知.txt", "text": "2026年10月30日17:00前提交报名表和照片，交给办公室。"},
        {"id": "S2", "label": "补充通知.txt", "text": "报名材料截止改为2026年11月2日12:00，提交方式改为上传PDF。"},
    ]}
    def fact(text, quote, source="S1"):
        return {"text": text, "evidence": [{"source_id": source, "location": "第1行", "quote": quote}]}
    result = {"schema_version": 1, "questions": [], "tasks": [{
        "id": "T1", "action": fact("提交报名材料", "提交报名表和照片"),
        "status": "active",
        "deadline": dict(fact("2026年11月2日12:00", "2026年11月2日12:00", "S2"), iso="2026-11-02T12:00:00+08:00"),
        "materials": [fact("报名表和照片", "报名表和照片")], "prerequisites": [],
        "submission": fact("上传PDF", "上传PDF", "S2"),
        "changes": [fact("截止和提交方式调整；原材料要求保留", "报名材料截止改为2026年11月2日12:00，提交方式改为上传PDF。", "S2")],
        "questions": [],
    }]}
    return sources, result


class CheckerTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), "The checker has not been implemented yet")
        spec = importlib.util.spec_from_file_location("notice_checker", SCRIPT)
        self.checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.checker)
        self.sources, self.result = sample()

    def errors(self):
        return self.checker.validate_result(self.sources, self.result)

    def test_accepts_a_cited_partial_amendment(self):
        self.assertEqual([], self.errors())

    def test_rejects_unknown_source_id(self):
        self.result["tasks"][0]["action"]["evidence"][0]["source_id"] = "S99"
        self.assertTrue(any("source_id" in e for e in self.errors()))

    def test_rejects_a_quote_missing_from_its_source(self):
        self.result["tasks"][0]["action"]["evidence"][0]["quote"] = "材料已经自动提交成功"
        self.assertTrue(any("quote" in e for e in self.errors()))

    def test_rejects_facts_with_no_evidence(self):
        self.result["tasks"][0]["materials"][0]["evidence"] = []
        self.assertTrue(any("evidence" in e for e in self.errors()))

    def test_rejects_a_missing_evidence_location(self):
        self.result["tasks"][0]["action"]["evidence"][0]["location"] = ""
        self.assertTrue(any("location" in e for e in self.errors()))

    def test_rejects_duplicate_source_ids(self):
        self.sources["sources"].append(copy.deepcopy(self.sources["sources"][0]))
        self.assertTrue(any("duplicate" in e for e in self.errors()))

    def test_rejects_duplicate_task_ids(self):
        self.result["tasks"].append(copy.deepcopy(self.result["tasks"][0]))
        self.assertTrue(any("duplicate" in e for e in self.errors()))

    def test_rejects_impossible_dates(self):
        self.result["tasks"][0]["deadline"]["iso"] = "2026-02-30"
        self.assertTrue(any("iso" in e for e in self.errors()))

    def test_rejects_a_timestamp_without_timezone(self):
        self.result["tasks"][0]["deadline"]["iso"] = "2026-11-02T12:00:00"
        self.assertTrue(any("iso" in e for e in self.errors()))

    def test_accepts_a_date_without_inventing_a_clock_time(self):
        self.result["tasks"][0]["deadline"]["iso"] = "2026-11-02"
        self.assertEqual([], self.errors())

    def test_unresolved_deadline_requires_visible_confirmation(self):
        self.result["tasks"][0]["deadline"]["iso"] = None
        self.assertTrue(any("confirmation" in e for e in self.errors()))
        self.result["tasks"][0]["status"] = "needs_confirmation"
        self.result["tasks"][0]["questions"] = ["通知未给出时区，请确认。"]
        self.assertEqual([], self.errors())

    def test_cancelled_tasks_require_a_cited_change(self):
        self.result["tasks"][0]["status"] = "cancelled"
        self.result["tasks"][0]["changes"] = []
        self.assertTrue(any("cancelled" in e for e in self.errors()))

    def test_unknown_status_is_rejected(self):
        self.result["tasks"][0]["status"] = "done"
        self.assertTrue(any("status" in e for e in self.errors()))

    def test_unreadable_source_requires_a_top_level_question(self):
        self.sources["sources"].append({"id": "S3", "label": "模糊截图.png", "text": ""})
        self.assertTrue(any("unreadable" in e for e in self.errors()))
        self.result["questions"] = ["S3 模糊截图无法读取，请补充清晰版本。"]
        self.assertEqual([], self.errors())

    def test_no_action_notice_can_have_an_empty_checklist(self):
        self.result["tasks"] = []
        self.assertEqual([], self.errors())
        self.assertIn("没有列出可执行事项", self.checker.render_markdown(self.sources, self.result))

    def test_malformed_containers_produce_diagnostics_not_tracebacks(self):
        for sources, result in [(None, None), ([], {}), ({"sources": [None]}, self.result),
                                (self.sources, {"schema_version": 1, "tasks": [None], "questions": []})]:
            with self.subTest(sources=sources, result=result):
                self.assertTrue(self.checker.validate_result(sources, result))

    def test_missing_fields_and_misspellings_are_not_silently_dropped(self):
        del self.result["tasks"][0]["materials"]
        self.result["tasks"][0]["material"] = []
        self.assertTrue(any("materials" in e for e in self.errors()))
        self.assertTrue(any("material" in e for e in self.errors()))

    def test_boolean_is_not_a_schema_version(self):
        self.result["schema_version"] = True
        self.assertTrue(self.errors())

    def test_renderer_keeps_cancelled_tasks_out_of_active_section(self):
        self.result["tasks"][0]["status"] = "cancelled"
        rendered = self.checker.render_markdown(self.sources, self.result)
        active, cancelled = rendered.split("## 已取消事项", 1)
        self.assertNotIn("提交报名材料", active)
        self.assertIn("提交报名材料", cancelled)
        self.assertIn("报名表和照片", rendered)

    def test_renderer_escapes_source_html_and_markdown(self):
        self.sources["sources"][0]["label"] = '<script>alert(1)</script>|[link](https://invalid.test)'
        rendered = self.checker.render_markdown(self.sources, self.result)
        self.assertNotIn("<script>", rendered)
        self.assertNotIn("[link](https://invalid.test)", rendered)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn("\\|", rendered)

    def test_renderer_refuses_invalid_results(self):
        self.result["tasks"][0]["action"]["evidence"] = []
        with self.assertRaises(ValueError):
            self.checker.render_markdown(self.sources, self.result)

    def test_renderer_preserves_literal_tildes_in_active_facts_and_quotes(self):
        self.sources["sources"][0]["text"] += " ~~提交报名表~~"
        self.result["tasks"][0]["action"]["text"] = "~~提交报名表~~"
        self.result["tasks"][0]["action"]["evidence"][0]["quote"] = "~~提交报名表~~"
        rendered = self.checker.render_markdown(self.sources, self.result)
        self.assertNotIn("~~提交报名表~~", rendered)
        self.assertIn(r"\~\~提交报名表\~\~", rendered)


class CliTests(unittest.TestCase):
    def run_case(self, result=None, malformed=False, existing_output=False):
        self.assertTrue(SCRIPT.is_file(), "The checker has not been implemented yet")
        scratch = ROOT / ".test-tmp"
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            folder = Path(directory)
            sources, good = sample()
            source_path, result_path, output = folder / "sources.json", folder / "result.json", folder / "checklist.md"
            source_path.write_text(json.dumps(sources, ensure_ascii=False), encoding="utf-8")
            result_path.write_text("{" if malformed else json.dumps(result if result is not None else good, ensure_ascii=False), encoding="utf-8")
            if existing_output:
                output.write_text("existing user output", encoding="utf-8")
            completed = subprocess.run([sys.executable, str(SCRIPT), "--sources", str(source_path), "--result", str(result_path), "--markdown", str(output)], capture_output=True, text=True, encoding="utf-8")
            content = output.read_text(encoding="utf-8") if output.exists() else None
            self.assertEqual(sources, json.loads(source_path.read_text(encoding="utf-8")))
            return completed, content

    def test_cli_emits_a_checked_report_and_honest_scope(self):
        completed, content = self.run_case()
        self.assertEqual(0, completed.returncode, completed.stderr + completed.stdout)
        self.assertTrue(json.loads(completed.stdout)["semantic_review_required"])
        self.assertIn("上传PDF", content)

    def test_cli_invalid_result_does_not_write_a_checklist(self):
        _, result = sample()
        result["tasks"][0]["deadline"]["iso"] = "2026-13-20"
        completed, content = self.run_case(result=result)
        self.assertEqual(1, completed.returncode)
        self.assertIsNone(content)

    def test_cli_preserves_an_existing_output(self):
        completed, content = self.run_case(existing_output=True)
        self.assertEqual(2, completed.returncode)
        self.assertEqual("existing user output", content)

    def test_cli_reports_malformed_json_without_a_traceback(self):
        completed, content = self.run_case(malformed=True)
        self.assertEqual(2, completed.returncode)
        self.assertNotIn("Traceback", completed.stderr)
        self.assertFalse(json.loads(completed.stdout)["valid"])
        self.assertIsNone(content)


if __name__ == "__main__":
    unittest.main()
