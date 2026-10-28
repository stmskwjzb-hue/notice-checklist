# Extraction format, version 1

The checker uses only Python's standard library. Source and result JSON are separate so that broken or invented quote references can be detected against an extraction snapshot.

## sources.json

An object with exactly one key, sources: a nonempty list of objects with:

| Field | Value |
|---|---|
| id | Unique nonempty string, e.g. S1 |
| label | Nonempty user-readable source name |
| text | Exact extracted or pasted text; empty only when unreadable |

Source IDs and labels do not prove identity, authority or authenticity. Retain original files separately. For OCR, review the image when a critical date or character is uncertain. An empty source needs a visible top-level question.

## result.json

Exactly schema_version: 1, tasks: [] and questions: []. Top-level questions describe missing/unreadable inputs or issues that cannot be attached to a known task. An informational notice can have zero tasks.

Every task has all these keys:

| Field | Value |
|---|---|
| id | Unique nonempty task ID |
| action | Cited fact describing the action |
| status | active, cancelled, or needs_confirmation |
| deadline | null if absent, otherwise a cited fact plus iso |
| materials | List of cited facts, possibly empty |
| prerequisites | List of cited facts, possibly empty |
| submission | Cited fact, or null if absent |
| changes | List of cited facts explaining amendments/cancellation |
| questions | List of nonempty strings |

A fact is {"text": "description", "evidence": [...]}. Each evidence item has exactly source_id, location and quote, all nonempty strings. Copy quotes exactly from source text. A location should identify an actual page, message, line, or region: do not fabricate line numbers for an image.

For deadlines, add iso: null if unresolved; YYYY-MM-DD for an evidenced date without a clock time; or an ISO timestamp with a UTC offset, e.g. 2026-11-02T12:00:00+08:00. The original deadline wording remains in text and its exact source in evidence. Record any user-confirmed anchor in the source snapshot as a separately labelled user clarification.

An unresolved stated deadline requires needs_confirmation and a question, unless the task was cancelled. A cancelled task requires a cited change. Retain unaffected materials and prerequisites after a partial update; do not remove a task merely because a later notice omits it.

## What the checker establishes

It checks shapes and required fields, unique IDs, quote membership in source text, references, date syntax/calendar validity, and status consistency. It renders safe Markdown and refuses an existing output file.

It does not check semantic entailment, completeness, OCR accuracy, whether a location is correct, source authority, timezone justification or authenticity. A fabricated interpretation can still contain a genuine but irrelevant quote. Review meaning against the originals.
