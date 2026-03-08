---
phase: 2
slug: analysis-engine
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-03-06
---

# Phase 2 — Validation Strategy

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
| 2-01-01 | 01 | 1 | API-01 | unit | `pytest tests/test_db_vector.py` | ❌ W0 | ⬜ pending |
| 2-01-02 | 01 | 1 | NLP-01 | unit | `pytest tests/test_chunking.py` | ❌ W0 | ⬜ pending |
| 2-02-01 | 02 | 2 | NLP-02 | unit | `pytest tests/test_openai_api.py` | ❌ W0 | ⬜ pending |
| 2-02-02 | 02 | 2 | NLP-03 | unit | `pytest tests/test_openai_api.py` | ❌ W0 | ⬜ pending |
| 2-03-01 | 03 | 3 | API-01 | integration| `pytest tests/test_analysis_cli.py`| ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_db_vector.py` — stubs for testing pgvector/DB changes
- [ ] `tests/test_chunking.py` — stubs for testing text chunker
- [ ] `tests/test_openai_api.py` — stubs for mocking OpenAI SDK calls
- [ ] `tests/test_analysis_cli.py` — stubs for testing CLI integration

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Run CLI end-to-end | NLP-01 | Requires real API call to OpenAI | Run `python analyze.py --channel-id <id>`, verify output makes sense |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
