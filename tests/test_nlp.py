"""Tests for src.analysis.nlp — Gemini API calls fully mocked."""

import pytest
from unittest.mock import MagicMock, patch

from src.analysis.nlp import (
    get_embedding,
    get_embeddings,
    score_chunks,
    score_text_content,
    set_client,
    AlignmentResult,
    QuoteItem,
)
from google.genai import types


# ── Fixtures ─────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def mock_gemini_client():
    """Inject a mocked Gemini client for every test."""
    mock_client = MagicMock()
    set_client(mock_client)
    yield mock_client
    set_client(None)  # Reset after each test


# ── Embedding Tests ──────────────────────────────────────────────────────

class TestGetEmbedding:
    def test_returns_embedding_vector(self, mock_gemini_client):
        fake_embedding = [0.1] * 1536
        mock_embed = MagicMock()
        mock_embed.values = fake_embedding

        mock_gemini_client.models.embed_content.return_value = MagicMock(
            embeddings=[mock_embed]
        )

        result = get_embedding("Hello world")

        assert result == fake_embedding
        assert len(result) == 1536
        mock_gemini_client.models.embed_content.assert_called_once()
        call_args = mock_gemini_client.models.embed_content.call_args
        assert call_args.kwargs["model"] == "text-embedding-004"
        assert call_args.kwargs["contents"] == "Hello world"

    def test_passes_text_to_api(self, mock_gemini_client):
        mock_embed = MagicMock()
        mock_embed.values = [0.0] * 1536
        mock_gemini_client.models.embed_content.return_value = MagicMock(
            embeddings=[mock_embed]
        )

        get_embedding("plant-based nutrition")

        call_args = mock_gemini_client.models.embed_content.call_args
        assert call_args.kwargs["contents"] == "plant-based nutrition"


class TestGetEmbeddings:
    def test_returns_multiple_embeddings(self, mock_gemini_client):
        mock_items = []
        for i in range(3):
            item = MagicMock()
            item.values = [float(i)] * 1536
            mock_items.append(item)

        mock_gemini_client.models.embed_content.return_value = MagicMock(
            embeddings=mock_items
        )

        result = get_embeddings(["text1", "text2", "text3"])

        assert len(result) == 3
        assert result[0] == [0.0] * 1536
        assert result[2] == [2.0] * 1536

    def test_returns_empty_for_empty_input(self, mock_gemini_client):
        result = get_embeddings([])
        assert result == []
        mock_gemini_client.models.embed_content.assert_not_called()


# ── Scoring Tests ────────────────────────────────────────────────────────

SAMPLE_CHUNKS = [
    {
        "text": "Today we discuss the benefits of a whole food plant-based diet",
        "start_time": 0.0,
        "end_time": 60.0,
    },
    {
        "text": "Studies show that reducing animal products can lower cholesterol",
        "start_time": 60.0,
        "end_time": 120.0,
    },
]

SAMPLE_TEXTS = [
    "A deep dive into nutrition science...",
    "Why I stopped eating meat.",
]


class TestScoreChunks:
    def test_returns_alignment_result(self, mock_gemini_client):
        expected_json = '{"alignment_score": 82, "reasoning": "Content naturally discusses plant-based nutrition...", "quotes": [{"text": "benefits of a whole food plant-based diet", "timestamp": "0:00"}, {"text": "reducing animal products can lower cholesterol", "timestamp": "1:00"}]}'

        mock_gemini_client.models.generate_content.return_value = MagicMock(
            text=expected_json
        )

        result = score_chunks(SAMPLE_CHUNKS, "plant-based health")

        assert isinstance(result, AlignmentResult)
        assert result.alignment_score == 82
        assert len(result.quotes) == 2

    def test_uses_correct_model(self, mock_gemini_client):
        expected_json = '{"alignment_score": 50, "reasoning": "Average alignment", "quotes": []}'
        mock_gemini_client.models.generate_content.return_value = MagicMock(
            text=expected_json
        )

        score_chunks(SAMPLE_CHUNKS, "sustainability")

        call_args = mock_gemini_client.models.generate_content.call_args
        assert call_args.kwargs["model"] == "gemini-2.5-flash"
        assert call_args.kwargs["config"].response_schema == AlignmentResult
        assert call_args.kwargs["config"].response_mime_type == "application/json"

    def test_includes_target_topic_in_prompt(self, mock_gemini_client):
        expected_json = '{"alignment_score": 75, "reasoning": "Good fit", "quotes": []}'
        mock_gemini_client.models.generate_content.return_value = MagicMock(
            text=expected_json
        )

        score_chunks(SAMPLE_CHUNKS, "ethical food systems")

        call_args = mock_gemini_client.models.generate_content.call_args
        contents = call_args.kwargs["contents"]
        assert len(contents) == 1
        user_msg = contents[0].parts[0].text
        assert "ethical food systems" in user_msg


class TestScoreTextContent:
    def test_returns_alignment_result(self, mock_gemini_client):
        expected_json = '{"alignment_score": 90, "reasoning": "Direct focus", "quotes": [{"text": "nutrition science", "timestamp": ""}]}'

        mock_gemini_client.models.generate_content.return_value = MagicMock(
            text=expected_json
        )

        result = score_text_content(SAMPLE_TEXTS, "plant-based health")

        assert isinstance(result, AlignmentResult)
        assert result.alignment_score == 90
        assert len(result.quotes) == 1

    def test_includes_target_topic_in_prompt(self, mock_gemini_client):
        expected_json = '{"alignment_score": 75, "reasoning": "Good fit", "quotes": []}'
        mock_gemini_client.models.generate_content.return_value = MagicMock(
            text=expected_json
        )

        score_text_content(SAMPLE_TEXTS, "ethical food systems")

        call_args = mock_gemini_client.models.generate_content.call_args
        contents = call_args.kwargs["contents"]
        assert len(contents) == 1
        user_msg = contents[0].parts[0].text
        assert "ethical food systems" in user_msg
