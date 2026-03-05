"""Tests for src.analysis.nlp — OpenAI API calls fully mocked."""

import pytest
from unittest.mock import MagicMock, patch

from src.analysis.nlp import (
    get_embedding,
    get_embeddings,
    score_chunks,
    set_client,
    AlignmentResult,
    QuoteItem,
)


# ── Fixtures ─────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def mock_openai_client():
    """Inject a mocked OpenAI client for every test."""
    mock_client = MagicMock()
    set_client(mock_client)
    yield mock_client
    set_client(None)  # Reset after each test


# ── Embedding Tests ──────────────────────────────────────────────────────

class TestGetEmbedding:
    def test_returns_embedding_vector(self, mock_openai_client):
        fake_embedding = [0.1] * 1536
        mock_data = MagicMock()
        mock_data.embedding = fake_embedding
        mock_data.index = 0

        mock_openai_client.embeddings.create.return_value = MagicMock(
            data=[mock_data]
        )

        result = get_embedding("Hello world")

        assert result == fake_embedding
        assert len(result) == 1536
        mock_openai_client.embeddings.create.assert_called_once_with(
            model="text-embedding-3-small",
            input="Hello world",
        )

    def test_passes_text_to_api(self, mock_openai_client):
        mock_data = MagicMock()
        mock_data.embedding = [0.0] * 1536
        mock_openai_client.embeddings.create.return_value = MagicMock(
            data=[mock_data]
        )

        get_embedding("plant-based nutrition")

        call_args = mock_openai_client.embeddings.create.call_args
        assert call_args.kwargs["input"] == "plant-based nutrition"


class TestGetEmbeddings:
    def test_returns_multiple_embeddings(self, mock_openai_client):
        mock_items = []
        for i in range(3):
            item = MagicMock()
            item.embedding = [float(i)] * 1536
            item.index = i
            mock_items.append(item)

        mock_openai_client.embeddings.create.return_value = MagicMock(
            data=mock_items
        )

        result = get_embeddings(["text1", "text2", "text3"])

        assert len(result) == 3
        assert result[0] == [0.0] * 1536
        assert result[2] == [2.0] * 1536

    def test_returns_empty_for_empty_input(self, mock_openai_client):
        result = get_embeddings([])
        assert result == []
        mock_openai_client.embeddings.create.assert_not_called()

    def test_maintains_order(self, mock_openai_client):
        """Results should be ordered by index even if API returns them shuffled."""
        mock_items = []
        for i in [2, 0, 1]:  # Shuffled order
            item = MagicMock()
            item.embedding = [float(i)] * 1536
            item.index = i
            mock_items.append(item)

        mock_openai_client.embeddings.create.return_value = MagicMock(
            data=mock_items
        )

        result = get_embeddings(["a", "b", "c"])

        assert result[0] == [0.0] * 1536  # index 0
        assert result[1] == [1.0] * 1536  # index 1
        assert result[2] == [2.0] * 1536  # index 2


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


class TestScoreChunks:
    def test_returns_alignment_result(self, mock_openai_client):
        expected = AlignmentResult(
            alignment_score=82,
            reasoning="Content naturally discusses plant-based nutrition...",
            quotes=[
                QuoteItem(text="benefits of a whole food plant-based diet", timestamp="0:00"),
                QuoteItem(text="reducing animal products can lower cholesterol", timestamp="1:00"),
            ],
        )

        mock_message = MagicMock()
        mock_message.parsed = expected

        mock_choice = MagicMock()
        mock_choice.message = mock_message

        mock_openai_client.beta.chat.completions.parse.return_value = MagicMock(
            choices=[mock_choice]
        )

        result = score_chunks(SAMPLE_CHUNKS, "plant-based health")

        assert isinstance(result, AlignmentResult)
        assert result.alignment_score == 82
        assert len(result.quotes) == 2

    def test_uses_correct_model(self, mock_openai_client):
        mock_message = MagicMock()
        mock_message.parsed = AlignmentResult(
            alignment_score=50,
            reasoning="Average alignment",
            quotes=[],
        )
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_openai_client.beta.chat.completions.parse.return_value = MagicMock(
            choices=[mock_choice]
        )

        score_chunks(SAMPLE_CHUNKS, "sustainability")

        call_args = mock_openai_client.beta.chat.completions.parse.call_args
        assert call_args.kwargs["model"] == "gpt-4o-mini"
        assert call_args.kwargs["response_format"] == AlignmentResult

    def test_includes_target_topic_in_prompt(self, mock_openai_client):
        mock_message = MagicMock()
        mock_message.parsed = AlignmentResult(
            alignment_score=75,
            reasoning="Good fit",
            quotes=[],
        )
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_openai_client.beta.chat.completions.parse.return_value = MagicMock(
            choices=[mock_choice]
        )

        score_chunks(SAMPLE_CHUNKS, "ethical food systems")

        call_args = mock_openai_client.beta.chat.completions.parse.call_args
        user_msg = call_args.kwargs["messages"][1]["content"]
        assert "ethical food systems" in user_msg
