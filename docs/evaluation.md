# Evaluation record — v0.1.0

Date: 2026-10-28. All notices, names, dates and contact details used in these evaluations are synthetic. No real-user adoption or production accuracy has been established.

| Check | Observed result | What it means |
|---|---|---|
| Python unit/CLI tests | 26 passed | References, required fields, date/status consistency, safe rendering and exclusive output behavior passed the shipped suite |
| No-skill baseline | 63 rubric criteria met, 0 failed, 1 unobservable, across 16 scenarios | The unaided model was already strong; no semantic improvement is demonstrated |
| With-skill forward run | 16/16 checker runs exited 0 on the first attempt, 21 tasks total | Fixed schema, source snapshots and checker integration worked on these inputs |
| Actual media run | One PNG plus one text-based PDF; first checker exit 0 | Host vision/PDF extraction and the skill worked together on one synthetic amendment |
| Independent code review | One tilde-escaping finding fixed and regression-tested; no remaining material findings within scope | A bounded independent review, not a certification |
| Skill metadata | Official authoring validator passed | Discovery frontmatter validates; this does not test behavior |

## Evidence and reproduction

- [Semantic scenarios and hand-authored rubric](../tests/behavior_cases.json).
- [Baseline methods, per-case scoring and limits](evaluation-baseline.md).
- [Saved baseline replies](../tests/evaluations/baseline/).
- [Forward inputs](../tests/evaluations/forward-inputs.json), [run summary](../tests/evaluations/forward/run-summary.json), and per-case sources/result/checklist/checker logs in that directory.
- [Actual media inputs](../tests/media/), [extracted sources and output](../tests/evaluations/media-forward/).
- [Independent review](code-review.md).
- [Program test RED/GREEN records](../tests/evaluations/program/).

Run the deterministic suite from the repository root:

    python -X utf8 -m unittest discover -s tests -v

Run the bundled example:

    python -X utf8 skills/notice-checklist/scripts/check_result.py --sources skills/notice-checklist/examples/sources.json --result skills/notice-checklist/examples/result.json

To reproduce the agent exercise, give a fresh supported host only a case's sources and user_request (without topic/rubric), run the skill and its checker, then compare meanings with the hand rubric. Agent outputs may differ. The baseline used one fresh agent for a batch, not isolated repeated trials. The forward run checked format/tool use; its semantic outcomes were not independently rescored against all baseline criteria.

## Important limits

The checker cannot establish that an interpretation follows from a genuine quote, that all actions were extracted, that a source was authoritative, or that OCR was accurate. A source snapshot may itself contain an extraction error. The PDF exercise used a text PDF, not scanned-PDF OCR.

The code ran on Python 3.12.14. Python 3.10 grammar was checked, but a Python 3.10 runtime was unavailable. The reviewer's 690 nested-type mutations were an additional finite review exercise, not part of the shipped automatic suite.

The no-skill model met every observable semantic criterion. This release should therefore be described as a reusable schema, evidence checking and report workflow—not an accuracy improvement over ordinary chat. Real users, diverse documents and repeated cross-host evaluations are still needed.
