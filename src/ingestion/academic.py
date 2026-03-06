"""Academic publication search — Semantic Scholar and PubMed APIs.

Both APIs are free and require no API keys.
- Semantic Scholar: https://api.semanticscholar.org/
- PubMed E-utilities: https://eutils.ncbi.nlm.nih.gov/
"""

import logging
from typing import Optional
from xml.etree import ElementTree

import httpx

logger = logging.getLogger(__name__)

_TIMEOUT = httpx.Timeout(20.0, connect=10.0)


# ── Semantic Scholar ─────────────────────────────────────────────────────

_S2_BASE = "https://api.semanticscholar.org/graph/v1"


def search_semantic_scholar(
    query: str,
    limit: int = 20,
) -> list[dict]:
    """Search Semantic Scholar for papers matching a query.

    Returns list of dicts with keys: paper_id, title, abstract, authors,
    citation_count, year, doi, url
    """
    params = {
        "query": query,
        "limit": min(limit, 100),
        "fields": "title,abstract,authors,citationCount,year,externalIds,url",
    }

    try:
        resp = httpx.get(
            f"{_S2_BASE}/paper/search",
            params=params,
            timeout=_TIMEOUT,
        )
        resp.raise_for_status()
    except httpx.HTTPError as e:
        logger.warning("Semantic Scholar search failed: %s", e)
        return []

    data = resp.json()
    papers = []

    for item in data.get("data", []):
        authors = [
            {
                "name": a.get("name", ""),
                "authorId": a.get("authorId"),
            }
            for a in item.get("authors", [])
        ]

        external_ids = item.get("externalIds", {}) or {}
        doi = external_ids.get("DOI", "")

        papers.append({
            "paper_id": item.get("paperId", ""),
            "title": item.get("title", ""),
            "abstract": item.get("abstract", ""),
            "authors": authors,
            "citation_count": item.get("citationCount", 0),
            "year": item.get("year"),
            "doi": doi,
            "url": item.get("url", ""),
            "source": "semantic_scholar",
        })

    logger.info("Semantic Scholar returned %d papers for %r", len(papers), query)
    return papers


def get_s2_author_profile(author_id: str) -> Optional[dict]:
    """Get detailed author profile from Semantic Scholar.

    Parameters
    ----------
    author_id : Semantic Scholar author ID

    Returns
    -------
    dict with keys: author_id, name, h_index, citation_count,
    paper_count, affiliations, url
    """
    fields = "name,hIndex,citationCount,paperCount,affiliations,url"

    try:
        resp = httpx.get(
            f"{_S2_BASE}/author/{author_id}",
            params={"fields": fields},
            timeout=_TIMEOUT,
        )
        resp.raise_for_status()
    except httpx.HTTPError as e:
        logger.warning("Failed to fetch S2 author %s: %s", author_id, e)
        return None

    data = resp.json()
    return {
        "author_id": str(author_id),
        "name": data.get("name", ""),
        "h_index": data.get("hIndex", 0),
        "citation_count": data.get("citationCount", 0),
        "paper_count": data.get("paperCount", 0),
        "affiliations": data.get("affiliations", []),
        "url": data.get("url", ""),
        "platform": "academic",
    }


# ── PubMed E-utilities ──────────────────────────────────────────────────

_PUBMED_SEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
_PUBMED_FETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def search_pubmed(query: str, limit: int = 20) -> list[dict]:
    """Search PubMed for biomedical papers matching a query.

    Returns list of dicts with keys: pmid, title, abstract, authors,
    journal, year, url
    """
    # Step 1: Search for PMIDs
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": min(limit, 100),
        "retmode": "json",
        "sort": "relevance",
    }

    try:
        resp = httpx.get(_PUBMED_SEARCH, params=search_params, timeout=_TIMEOUT)
        resp.raise_for_status()
    except httpx.HTTPError as e:
        logger.warning("PubMed search failed: %s", e)
        return []

    search_data = resp.json()
    pmids = search_data.get("esearchresult", {}).get("idlist", [])

    if not pmids:
        return []

    # Step 2: Fetch details for each PMID
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
    }

    try:
        resp = httpx.get(_PUBMED_FETCH, params=fetch_params, timeout=_TIMEOUT)
        resp.raise_for_status()
    except httpx.HTTPError as e:
        logger.warning("PubMed fetch failed: %s", e)
        return []

    papers = _parse_pubmed_xml(resp.text)
    logger.info("PubMed returned %d papers for %r", len(papers), query)
    return papers


def _parse_pubmed_xml(xml_text: str) -> list[dict]:
    """Parse PubMed XML response into structured paper dicts."""
    papers = []

    try:
        root = ElementTree.fromstring(xml_text)
    except ElementTree.ParseError as e:
        logger.warning("Failed to parse PubMed XML: %s", e)
        return []

    for article in root.findall(".//PubmedArticle"):
        citation = article.find(".//MedlineCitation")
        if citation is None:
            continue

        pmid_el = citation.find("PMID")
        pmid = pmid_el.text if pmid_el is not None else ""

        article_el = citation.find("Article")
        if article_el is None:
            continue

        title_el = article_el.find("ArticleTitle")
        title = title_el.text if title_el is not None else ""

        # Extract abstract
        abstract_parts = []
        abstract_el = article_el.find("Abstract")
        if abstract_el is not None:
            for text_el in abstract_el.findall("AbstractText"):
                if text_el.text:
                    label = text_el.get("Label", "")
                    if label:
                        abstract_parts.append(f"{label}: {text_el.text}")
                    else:
                        abstract_parts.append(text_el.text)
        abstract = " ".join(abstract_parts)

        # Extract authors
        authors = []
        author_list = article_el.find("AuthorList")
        if author_list is not None:
            for author_el in author_list.findall("Author"):
                last = author_el.findtext("LastName", "")
                first = author_el.findtext("ForeName", "")
                if last:
                    authors.append({"name": f"{first} {last}".strip()})

        # Extract journal and year
        journal_el = article_el.find("Journal")
        journal = ""
        year = None
        if journal_el is not None:
            journal_title = journal_el.find("Title")
            journal = journal_title.text if journal_title is not None else ""
            pub_date = journal_el.find(".//Year")
            if pub_date is not None:
                try:
                    year = int(pub_date.text)
                except (ValueError, TypeError):
                    pass

        papers.append({
            "pmid": pmid,
            "title": title,
            "abstract": abstract,
            "authors": authors,
            "journal": journal,
            "year": year,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
            "source": "pubmed",
        })

    return papers


# ── Orchestration ────────────────────────────────────────────────────────

def search_academic(
    query: str,
    limit: int = 20,
) -> list[dict]:
    """Search across Semantic Scholar and PubMed, deduplicate by title.

    Returns combined list of paper dicts.
    """
    s2_papers = search_semantic_scholar(query, limit)
    pubmed_papers = search_pubmed(query, limit)

    # Deduplicate by normalized title
    seen_titles = set()
    combined = []

    for paper in s2_papers + pubmed_papers:
        norm_title = paper.get("title", "").lower().strip()
        if norm_title and norm_title not in seen_titles:
            seen_titles.add(norm_title)
            combined.append(paper)

    logger.info(
        "Academic search for %r: %d S2 + %d PubMed = %d unique papers",
        query, len(s2_papers), len(pubmed_papers), len(combined),
    )
    return combined[:limit * 2]  # Allow slightly more than limit after dedup


def extract_academic_creators(papers: list[dict]) -> dict[str, dict]:
    """Group papers by first author to build creator profiles.

    Returns dict mapping author name -> {name, papers, total_citations, ...}
    """
    author_map: dict[str, dict] = {}

    for paper in papers:
        authors = paper.get("authors", [])
        if not authors:
            continue

        # Use first author as the "creator"
        first_author = authors[0]
        author_name = first_author.get("name", "Unknown")

        if author_name not in author_map:
            author_map[author_name] = {
                "name": author_name,
                "author_id": first_author.get("authorId"),
                "platform": "academic",
                "platform_id": first_author.get("authorId"),
                "papers": [],
                "total_citations": 0,
                "profile_url": "",
            }

        author_map[author_name]["papers"].append(paper)
        author_map[author_name]["total_citations"] += paper.get("citation_count", 0)

    # Try to enrich with S2 author profiles
    for author_name, author_data in author_map.items():
        s2_id = author_data.get("author_id")
        if s2_id:
            profile = get_s2_author_profile(s2_id)
            if profile:
                author_data["h_index"] = profile.get("h_index", 0)
                author_data["profile_url"] = profile.get("url", "")
                author_data["affiliations"] = profile.get("affiliations", [])

    return author_map
