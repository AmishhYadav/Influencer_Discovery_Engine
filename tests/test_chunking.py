"""Tests for src.analysis.chunker — transcript chunking logic."""

import pytest

from src.analysis.chunker import chunk_transcript


# Build a transcript of 10 segments, each 10 seconds long
SAMPLE_TRANSCRIPT = [
    {"text": f"Segment {i}", "start": float(i * 10), "duration": 10.0}
    for i in range(10)
]
# Total duration: 0–100 seconds


class TestChunkTranscript:
    def test_basic_chunking(self):
        """Default 60s window should produce multiple chunks."""
        chunks = chunk_transcript(SAMPLE_TRANSCRIPT)
        assert len(chunks) >= 2
        # First chunk starts at 0
        assert chunks[0]["start_time"] == 0.0

    def test_chunk_text_is_joined(self):
        """Each chunk's text should be space-joined segment texts."""
        chunks = chunk_transcript(SAMPLE_TRANSCRIPT, window_seconds=30.0)
        first = chunks[0]
        assert "Segment 0" in first["text"]
        assert "Segment 1" in first["text"]
        assert "Segment 2" in first["text"]

    def test_overlap_creates_shared_segments(self):
        """With overlap, adjacent chunks should share some segments."""
        chunks = chunk_transcript(
            SAMPLE_TRANSCRIPT, window_seconds=40.0, overlap_seconds=10.0
        )
        if len(chunks) >= 2:
            # The end of chunk 0 and start of chunk 1 should overlap
            assert chunks[1]["start_time"] < chunks[0]["end_time"]

    def test_end_time_is_accurate(self):
        """end_time should be start + duration of the last included segment."""
        chunks = chunk_transcript(SAMPLE_TRANSCRIPT, window_seconds=20.0)
        first = chunks[0]
        # First chunk covers segments 0 and 1 (0–20s)
        assert first["end_time"] == pytest.approx(20.0, abs=0.1)

    def test_handles_empty_transcript(self):
        assert chunk_transcript([]) == []

    def test_handles_none_like_empty(self):
        assert chunk_transcript([]) == []

    def test_single_segment(self):
        single = [{"text": "Hello", "start": 0.0, "duration": 5.0}]
        chunks = chunk_transcript(single)
        assert len(chunks) == 1
        assert chunks[0]["text"] == "Hello"
        assert chunks[0]["start_time"] == 0.0
        assert chunks[0]["end_time"] == 5.0

    def test_all_keys_present(self):
        chunks = chunk_transcript(SAMPLE_TRANSCRIPT)
        for chunk in chunks:
            assert "text" in chunk
            assert "start_time" in chunk
            assert "end_time" in chunk

    def test_no_empty_text_chunks(self):
        """No chunk should have empty text."""
        chunks = chunk_transcript(SAMPLE_TRANSCRIPT)
        for chunk in chunks:
            assert chunk["text"].strip() != ""
