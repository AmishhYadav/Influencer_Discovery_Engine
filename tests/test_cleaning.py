"""Tests for src.ingestion.cleaner — transcript cleaning logic."""

import pytest

from src.ingestion.cleaner import clean_transcript


# ── Sample data ──────────────────────────────────────────────────────────

RAW_TRANSCRIPT = [
    {"text": "Welcome to the show", "start": 0.0, "duration": 3.5},
    {"text": "[Music]", "start": 3.5, "duration": 2.0},
    {"text": "Today we talk about plant-based health", "start": 5.5, "duration": 5.0},
    {"text": "[Applause]", "start": 10.5, "duration": 1.5},
    {"text": "This video is brought to you by NordVPN", "start": 12.0, "duration": 8.0},
    {"text": "Use code HEALTH for 20% off", "start": 20.0, "duration": 4.0},
    {"text": "Back to the science of nutrition", "start": 24.0, "duration": 6.0},
    {"text": "", "start": 30.0, "duration": 1.0},
    {"text": "   ", "start": 31.0, "duration": 0.5},
    {"text": "[Laughter]", "start": 31.5, "duration": 1.0},
    {"text": "Support the channel by subscribing", "start": 32.5, "duration": 3.0},
]


class TestCleanTranscript:
    def test_removes_filler_tags(self):
        result = clean_transcript(RAW_TRANSCRIPT)
        texts = [s["text"] for s in result]
        assert "[Music]" not in texts
        assert "[Applause]" not in texts
        assert "[Laughter]" not in texts

    def test_removes_sponsor_reads(self):
        result = clean_transcript(RAW_TRANSCRIPT)
        texts = [s["text"].lower() for s in result]
        assert not any("nordvpn" in t for t in texts)
        assert not any("use code" in t for t in texts)

    def test_removes_support_channel(self):
        result = clean_transcript(RAW_TRANSCRIPT)
        texts = [s["text"].lower() for s in result]
        assert not any("support the channel" in t for t in texts)

    def test_keeps_real_content(self):
        result = clean_transcript(RAW_TRANSCRIPT)
        texts = [s["text"] for s in result]
        assert "Welcome to the show" in texts
        assert "Today we talk about plant-based health" in texts
        assert "Back to the science of nutrition" in texts

    def test_removes_empty_segments(self):
        result = clean_transcript(RAW_TRANSCRIPT)
        texts = [s["text"] for s in result]
        assert "" not in texts
        assert "   " not in texts

    def test_handles_none_input(self):
        assert clean_transcript(None) == []

    def test_handles_empty_list(self):
        assert clean_transcript([]) == []

    def test_preserves_timestamps(self):
        result = clean_transcript(RAW_TRANSCRIPT)
        # Find the "Back to the science" segment and check timestamps
        segment = next(s for s in result if "science of nutrition" in s["text"])
        assert segment["start"] == 24.0
        assert segment["duration"] == 6.0
