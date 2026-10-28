# Notice Checklist Implementation Plan

> For agentic workers: use executing-plans for implementation and fresh independent review for the finished project. The user authorized execution in this chat.

Goal: ship a tested, portable skill and an honest OpenAI OSS application preparation package.

Architecture: semantic extraction by the host model; deterministic structural checks and Markdown rendering by one Python script. No runtime dependencies beyond Python 3.10+.

Spec: `docs/design.md`.

## Global constraints

- All source, scratch, tests and outputs physically on E:.
- Preserve user originals; no account connections, automatic sends or calendar mutations.
- Structural validation is not semantic or authenticity verification.
- No invented publication, adoption or grant claims.

## Review focus

- Partial amendments must retain earlier unaffected requirements.
- Conflicting/relative dates must not become fabricated exact dates.
- JSON shape errors and broken citations must yield actionable diagnostics.
- Notice text and Markdown syntax must remain data.
- Invalid results must not produce a plausible final checklist.

## Task 1 — Behavior baseline and synthetic cases

- [x] Create 12–20 independent synthetic scenarios and hand-checked expectations.
- [x] Run a no-skill baseline; preserve verbatim outputs and observed gaps.

## Task 2 — Checker and rendering

Files: `skills/notice-checklist/scripts/check_result.py`, `tests/test_check_result.py`.

Interfaces: `validate_result(sources, result) -> list[str]`; `render_markdown(sources, result) -> str`; CLI `--sources`, `--result`, optional `--markdown` (new output file only).

- [x] Write failing behavior tests for references, date/status rules, malformed inputs and safe output.
- [x] Run them and retain the RED log.
- [x] Implement the minimal checker and renderer.
- [x] Run the full standard-library unittest suite and retain the GREEN log.

## Task 3 — Skill and evaluation

- [x] Initialize and author the skill; add one executable example and format reference.
- [x] Run the same scenarios with the skill in fresh agents; record observed outcomes.
- [x] Test a synthetic screenshot/PDF input and fix demonstrated gaps.
- [x] Validate packaging and discovery metadata.

## Task 4 — Public-ready delivery

- [x] Add README, MIT license, competitor/source notes and application draft without fabricated metrics.
- [x] Run independent code/behavior review and fix material findings with regression tests.
- [x] Install the skill through an E:-backed discovery junction, verify it, and build a clean ZIP.
- [x] Check GitHub publishing availability; complete every local prerequisite before requesting missing account details or publication approval.
