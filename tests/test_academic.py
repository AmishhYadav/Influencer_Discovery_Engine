"""Tests for academic publication search module."""

import pytest
from unittest.mock import patch, MagicMock

from src.ingestion.academic import (
    search_semantic_scholar,
    search_pubmed,
    _parse_pubmed_xml,
    search_academic,
    extract_academic_creators,
)


# ── Mock Data ────────────────────────────────────────────────────────────

MOCK_S2_RESPONSE = {
    "data": [
        {
            "paperId": "abc123",
            "title": "Plant-Based Diets and Cardiovascular Health",
            "abstract": "A systematic review of plant-based dietary patterns...",
            "authors": [
                {"name": "Jane Smith", "authorId": "12345"},
                {"name": "John Doe", "authorId": "67890"},
            ],
            "citationCount": 150,
            "year": 2023,
            "externalIds": {"DOI": "10.1234/test"},
            "url": "https://api.semanticscholar.org/abc123",
        },
        {
            "paperId": "def456",
            "title": "Environmental Impact of Animal Agriculture",
            "abstract": "This meta-analysis examines greenhouse gas emissions...",
            "authors": [
                {"name": "Jane Smith", "authorId": "12345"},
            ],
            "citationCount": 85,
            "year": 2022,
            "externalIds": {},
            "url": "https://api.semanticscholar.org/def456",
        },
    ]
}

MOCK_PUBMED_XML = """<?xml version="1.0" encoding="UTF-8"?>
<PubmedArticleSet>
  <PubmedArticle>
    <MedlineCitation>
      <PMID>12345678</PMID>
      <Article>
        <ArticleTitle>Nutritional Benefits of Plant-Based Diets</ArticleTitle>
        <Abstract>
          <AbstractText Label="BACKGROUND">Plant-based diets are growing in popularity.</AbstractText>
          <AbstractText Label="RESULTS">Significant health improvements were observed.</AbstractText>
        </Abstract>
        <AuthorList>
          <Author>
            <LastName>Garcia</LastName>
            <ForeName>Maria</ForeName>
          </Author>
          <Author>
            <LastName>Chen</LastName>
            <ForeName>Wei</ForeName>
          </Author>
        </AuthorList>
        <Journal>
          <Title>Journal of Nutrition</Title>
          <JournalIssue>
            <PubDate>
              <Year>2024</Year>
            </PubDate>
          </JournalIssue>
        </Journal>
      </Article>
    </MedlineCitation>
  </PubmedArticle>
</PubmedArticleSet>
"""

MOCK_PUBMED_SEARCH = {
    "esearchresult": {
        "idlist": ["12345678"],
    }
}


# ── Tests ────────────────────────────────────────────────────────────────

class TestSemanticScholar:
    @patch("src.ingestion.academic.httpx.get")
    def test_search_returns_papers(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = MOCK_S2_RESPONSE
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        papers = search_semantic_scholar("plant-based diet")
        assert len(papers) == 2
        assert papers[0]["title"] == "Plant-Based Diets and Cardiovascular Health"
        assert papers[0]["citation_count"] == 150
        assert papers[0]["authors"][0]["name"] == "Jane Smith"
        assert papers[0]["doi"] == "10.1234/test"

    @patch("src.ingestion.academic.httpx.get")
    def test_handles_error(self, mock_get):
        import httpx
        mock_get.side_effect = httpx.HTTPError("API error")

        papers = search_semantic_scholar("test query")
        assert papers == []


class TestPubMed:
    def test_parse_xml(self):
        papers = _parse_pubmed_xml(MOCK_PUBMED_XML)
        assert len(papers) == 1
        assert papers[0]["pmid"] == "12345678"
        assert papers[0]["title"] == "Nutritional Benefits of Plant-Based Diets"
        assert "BACKGROUND" in papers[0]["abstract"]
        assert papers[0]["authors"][0]["name"] == "Maria Garcia"
        assert papers[0]["year"] == 2024

    @patch("src.ingestion.academic.httpx.get")
    def test_search_pubmed_full_flow(self, mock_get):
        # First call: search, second call: fetch
        search_resp = MagicMock()
        search_resp.json.return_value = MOCK_PUBMED_SEARCH
        search_resp.raise_for_status = MagicMock()

        fetch_resp = MagicMock()
        fetch_resp.text = MOCK_PUBMED_XML
        fetch_resp.raise_for_status = MagicMock()

        mock_get.side_effect = [search_resp, fetch_resp]

        papers = search_pubmed("plant-based nutrition")
        assert len(papers) == 1
        assert papers[0]["source"] == "pubmed"

    def test_parse_invalid_xml(self):
        papers = _parse_pubmed_xml("not valid xml <><>")
        assert papers == []


class TestSearchAcademic:
    @patch("src.ingestion.academic.search_pubmed")
    @patch("src.ingestion.academic.search_semantic_scholar")
    def test_deduplicates_by_title(self, mock_s2, mock_pm):
        mock_s2.return_value = [
            {"title": "Same Paper", "authors": [{"name": "A"}], "source": "s2"},
        ]
        mock_pm.return_value = [
            {"title": "Same Paper", "authors": [{"name": "A"}], "source": "pm"},
            {"title": "Different Paper", "authors": [{"name": "B"}], "source": "pm"},
        ]

        results = search_academic("test")
        titles = [r["title"] for r in results]
        assert titles.count("Same Paper") == 1
        assert "Different Paper" in titles


class TestExtractAcademicCreators:
    def test_groups_by_first_author(self):
        papers = [
            {
                "title": "Paper 1",
                "authors": [{"name": "Jane Smith", "authorId": "123"}],
                "citation_count": 100,
            },
            {
                "title": "Paper 2",
                "authors": [{"name": "Jane Smith", "authorId": "123"}],
                "citation_count": 50,
            },
            {
                "title": "Paper 3",
                "authors": [{"name": "John Doe", "authorId": "456"}],
                "citation_count": 200,
            },
        ]

        with patch("src.ingestion.academic.get_s2_author_profile", return_value=None):
            creators = extract_academic_creators(papers)

        assert "Jane Smith" in creators
        assert "John Doe" in creators
        assert len(creators["Jane Smith"]["papers"]) == 2
        assert creators["Jane Smith"]["total_citations"] == 150
        assert creators["John Doe"]["total_citations"] == 200

    def test_handles_empty_authors(self):
        papers = [{"title": "No Author", "authors": [], "citation_count": 10}]
        creators = extract_academic_creators(papers)
        assert len(creators) == 0
