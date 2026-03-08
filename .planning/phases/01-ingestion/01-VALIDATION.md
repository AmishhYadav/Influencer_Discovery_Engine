---
phase: 1
slug: ingestion
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-03-06
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | none — Wave 0 installs |
| **Quick run command** | `pytest -m unit` |
| **Full suite command** | `pytest` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest -m unit`
- **After every plan wave:** Run `pytest`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 1-01-01 | 01 | 1 | DATA-02 | unit | `pytest tests/test_youtube_api.py` | ❌ W0 | ⬜ pending |
| 1-01-02 | 01 | 1 | DATA-01 | unit | `pytest tests/test_transcript_api.py` | ❌ W0 | ⬜ pending |
| 1-01-03 | 01 | 1 | DATA-03 | unit | `pytest tests/test_cleaning.py` | ❌ W0 | ⬜ pending |
| 1-02-01 | 02 | 2 | API-01 | unit | `pytest tests/test_db.py` | ❌ W0 | ⬜ pending |
| 1-02-02 | 02 | 2 | DATA-01 | integration| `pytest tests/test_cli.py` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/conftest.py` — shared fixtures for mocking YouTube API and DB
- [ ] `tests/test_youtube_api.py` — stubs for YouTube API wrapper
- [ ] `tests/test_transcript_api.py` — stubs for transcript fetching
- [ ] `tests/test_cleaning.py` — stubs for transcript cleaning
- [ ] `tests/test_db.py` — stubs for database
- [ ] `tests/test_cli.py` — stubs for CLI

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Run CLI end-to-end against live YouTube | DATA-01 | Requires real network call | Run `python ingest.py --query "plant based health"`, verify output |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
