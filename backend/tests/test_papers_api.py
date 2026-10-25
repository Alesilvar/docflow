from fastapi.responses import JSONResponse

from app.api.papers import search_papers
from app.integrations.openalex import (
    OpenAlexRateLimitError,
    OpenAlexTimeoutError,
    OpenAlexUpstreamError,
    PaperSearchItem,
    PaperSearchPage,
)


class FakeOpenAlexClient:
    def __init__(self, result: PaperSearchPage | Exception) -> None:
        self.result = result
        self.received: dict[str, object] | None = None

    def search_works(self, query: str, **kwargs: object) -> PaperSearchPage:
        self.received = {"query": query, **kwargs}
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


def test_search_papers_returns_normalized_api_contract() -> None:
    client = FakeOpenAlexClient(
        PaperSearchPage(
            items=[
                PaperSearchItem(
                    openalex_id="https://openalex.org/W123",
                    title="Example paper",
                    year=2024,
                    authors=["Ada Lovelace"],
                    doi=None,
                    abstract=None,
                    source_url="https://openalex.org/W123",
                )
            ],
            page=2,
            has_next=True,
            total_count=32,
        )
    )

    response = search_papers("literature review", from_year=2020, to_year=2024, page=2, per_page=10, client=client)  # type: ignore[arg-type]

    assert response.model_dump() == {
        "items": [
            {
                "openalex_id": "https://openalex.org/W123",
                "title": "Example paper",
                "year": 2024,
                "authors": ["Ada Lovelace"],
                "doi": None,
                "abstract": None,
                "source_url": "https://openalex.org/W123",
            }
        ],
        "page": 2,
        "has_next": True,
        "total_count": 32,
    }
    assert client.received == {
        "query": "literature review",
        "from_year": 2020,
        "to_year": 2024,
        "page": 2,
        "per_page": 10,
    }


def test_search_papers_returns_controlled_upstream_errors() -> None:
    cases = [
        (OpenAlexRateLimitError("limited"), 429, "openalex_rate_limited"),
        (OpenAlexTimeoutError("slow"), 504, "openalex_timeout"),
        (OpenAlexUpstreamError(503), 503, "openalex_unavailable"),
        (ValueError("invalid years"), 400, "invalid_search_parameters"),
    ]

    for error, status_code, code in cases:
        response = search_papers("test", client=FakeOpenAlexClient(error))  # type: ignore[arg-type]

        assert isinstance(response, JSONResponse)
        assert response.status_code == status_code
        assert f'"code":"{code}"'.encode() in response.body
        assert b'"request_id"' in response.body
