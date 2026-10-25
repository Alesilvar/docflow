"""OpenAlex client and normalization utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

OPENALEX_BASE_URL = "https://api.openalex.org"
DEFAULT_PAGE_SIZE = 25
MAX_PAGE_SIZE = 100


class OpenAlexError(Exception):
    """Base exception for errors communicating with OpenAlex."""


class OpenAlexTimeoutError(OpenAlexError):
    """OpenAlex did not respond before the configured timeout."""


class OpenAlexRateLimitError(OpenAlexError):
    """OpenAlex rejected the request due to a rate limit."""


class OpenAlexUpstreamError(OpenAlexError):
    """OpenAlex returned an unsuccessful response unrelated to rate limiting."""

    def __init__(self, status_code: int) -> None:
        self.status_code = status_code
        super().__init__(f"OpenAlex returned HTTP {status_code}")


@dataclass(frozen=True)
class PaperSearchItem:
    """Internal representation of a searchable publication."""

    openalex_id: str
    title: str
    year: int | None
    authors: list[str]
    doi: str | None
    abstract: str | None
    source_url: str


@dataclass(frozen=True)
class PaperSearchPage:
    """Normalized page of OpenAlex search results."""

    items: list[PaperSearchItem]
    page: int
    has_next: bool
    total_count: int | None


def reconstruct_abstract(inverted_index: object) -> str | None:
    """Rebuild OpenAlex's inverted abstract index into normal reading order.

    Invalid or incomplete external data is treated as unavailable instead of being
    guessed. This protects later AI analysis from an invented input text.
    """

    if not isinstance(inverted_index, dict) or not inverted_index:
        return None

    positions: dict[int, str] = {}
    for word, word_positions in inverted_index.items():
        if not isinstance(word, str) or not isinstance(word_positions, list):
            return None
        for position in word_positions:
            if not isinstance(position, int) or position < 0 or position in positions:
                return None
            positions[position] = word

    if not positions:
        return None

    return " ".join(positions[position] for position in sorted(positions))


def normalize_work(work: dict[str, Any]) -> PaperSearchItem:
    """Map an OpenAlex work response to the application's stable data shape."""

    openalex_id = work.get("id")
    if not isinstance(openalex_id, str) or not openalex_id:
        raise ValueError("OpenAlex work is missing its id")

    title = work.get("title") or work.get("display_name") or "Untitled work"
    if not isinstance(title, str):
        title = "Untitled work"

    year = work.get("publication_year")
    if not isinstance(year, int):
        year = None

    doi = work.get("doi")
    if not isinstance(doi, str) or not doi:
        doi = None

    authors: list[str] = []
    authorships = work.get("authorships")
    if isinstance(authorships, list):
        for authorship in authorships:
            if not isinstance(authorship, dict):
                continue
            author = authorship.get("author")
            if not isinstance(author, dict):
                continue
            name = author.get("display_name")
            if isinstance(name, str) and name:
                authors.append(name)

    source_url = openalex_id
    primary_location = work.get("primary_location")
    if isinstance(primary_location, dict):
        landing_page_url = primary_location.get("landing_page_url")
        if isinstance(landing_page_url, str) and landing_page_url:
            source_url = landing_page_url

    return PaperSearchItem(
        openalex_id=openalex_id,
        title=title,
        year=year,
        authors=authors,
        doi=doi,
        abstract=reconstruct_abstract(work.get("abstract_inverted_index")),
        source_url=source_url,
    )


class OpenAlexClient:
    """Small HTTP adapter that isolates OpenAlex from application services."""

    def __init__(
        self,
        client: httpx.Client | None = None,
        *,
        base_url: str = OPENALEX_BASE_URL,
        timeout_seconds: float = 10.0,
    ) -> None:
        self._owns_client = client is None
        self._client = client or httpx.Client(
            base_url=base_url,
            timeout=httpx.Timeout(timeout_seconds, connect=5.0),
            headers={"Accept": "application/json"},
        )

    def close(self) -> None:
        """Close only an HTTP client created by this adapter."""

        if self._owns_client:
            self._client.close()

    def search_works(
        self,
        query: str,
        *,
        from_year: int | None = None,
        to_year: int | None = None,
        page: int = 1,
        per_page: int = DEFAULT_PAGE_SIZE,
    ) -> PaperSearchPage:
        """Search OpenAlex works and return a normalized, bounded result page."""

        normalized_query = query.strip()
        if not normalized_query:
            raise ValueError("query must not be empty")
        if page < 1:
            raise ValueError("page must be at least 1")
        if not 1 <= per_page <= MAX_PAGE_SIZE:
            raise ValueError(f"per_page must be between 1 and {MAX_PAGE_SIZE}")
        if from_year is not None and to_year is not None and from_year > to_year:
            raise ValueError("from_year must not be greater than to_year")

        params: dict[str, str | int] = {
            "search": normalized_query,
            "page": page,
            "per-page": per_page,
        }
        filters: list[str] = []
        if from_year is not None:
            filters.append(f"from_publication_date:{from_year}-01-01")
        if to_year is not None:
            filters.append(f"to_publication_date:{to_year}-12-31")
        if filters:
            params["filter"] = ",".join(filters)

        try:
            response = self._client.get("/works", params=params)
        except httpx.TimeoutException as exc:
            raise OpenAlexTimeoutError("OpenAlex request timed out") from exc
        except httpx.HTTPError as exc:
            raise OpenAlexUpstreamError(status_code=503) from exc

        if response.status_code == 429:
            raise OpenAlexRateLimitError("OpenAlex rate limit reached")
        if response.is_error:
            raise OpenAlexUpstreamError(response.status_code)

        payload = response.json()
        results = payload.get("results") if isinstance(payload, dict) else None
        meta = payload.get("meta") if isinstance(payload, dict) else None
        if not isinstance(results, list) or not isinstance(meta, dict):
            raise OpenAlexUpstreamError(status_code=502)

        total_count = meta.get("count")
        if not isinstance(total_count, int):
            total_count = None

        return PaperSearchPage(
            items=[normalize_work(work) for work in results if isinstance(work, dict)],
            page=page,
            has_next=len(results) == per_page,
            total_count=total_count,
        )
