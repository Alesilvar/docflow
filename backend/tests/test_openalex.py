import httpx
import pytest

from app.integrations.openalex import (
    OpenAlexClient,
    OpenAlexRateLimitError,
    OpenAlexTimeoutError,
    OpenAlexUpstreamError,
    reconstruct_abstract,
)


def build_client(handler: httpx.MockTransport) -> OpenAlexClient:
    return OpenAlexClient(client=httpx.Client(transport=handler, base_url="https://api.openalex.org"))


def test_reconstruct_abstract_orders_words_by_position() -> None:
    abstract = reconstruct_abstract({"world": [1], "Hello": [0], "again": [2]})

    assert abstract == "Hello world again"


def test_reconstruct_abstract_returns_none_for_missing_or_invalid_data() -> None:
    assert reconstruct_abstract(None) is None
    assert reconstruct_abstract({"word": [0, 0]}) is None


def test_search_normalizes_work_and_request_parameters() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/works"
        assert request.url.params["search"] == "climate change"
        assert request.url.params["filter"] == "from_publication_date:2020-01-01,to_publication_date:2024-12-31"
        return httpx.Response(
            200,
            json={
                "meta": {"count": 26},
                "results": [
                    {
                        "id": "https://openalex.org/W123",
                        "title": "Climate evidence",
                        "publication_year": 2024,
                        "doi": "https://doi.org/10.1000/example",
                        "abstract_inverted_index": {"Evidence": [1], "Climate": [0]},
                        "authorships": [
                            {"author": {"display_name": "Ada Lovelace"}},
                            {"author": {"display_name": "Grace Hopper"}},
                        ],
                        "primary_location": {"landing_page_url": "https://example.org/paper"},
                    }
                ],
            },
        )

    result = build_client(httpx.MockTransport(handler)).search_works(
        " climate change ", from_year=2020, to_year=2024, per_page=1
    )

    assert result.page == 1
    assert result.has_next is True
    assert result.total_count == 26
    assert result.items[0].title == "Climate evidence"
    assert result.items[0].authors == ["Ada Lovelace", "Grace Hopper"]
    assert result.items[0].abstract == "Climate Evidence"
    assert result.items[0].source_url == "https://example.org/paper"


def test_search_handles_rate_limit_timeout_and_upstream_error() -> None:
    rate_limited = build_client(
        httpx.MockTransport(lambda request: httpx.Response(429, json={"error": "limited"}))
    )
    with pytest.raises(OpenAlexRateLimitError):
        rate_limited.search_works("test")

    def timeout_handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("slow", request=request)

    timed_out = build_client(httpx.MockTransport(timeout_handler))
    with pytest.raises(OpenAlexTimeoutError):
        timed_out.search_works("test")

    unavailable = build_client(httpx.MockTransport(lambda request: httpx.Response(503)))
    with pytest.raises(OpenAlexUpstreamError, match="503"):
        unavailable.search_works("test")


def test_search_rejects_invalid_pagination_and_years() -> None:
    client = build_client(httpx.MockTransport(lambda request: httpx.Response(200, json={})))

    with pytest.raises(ValueError, match="query"):
        client.search_works("  ")
    with pytest.raises(ValueError, match="page"):
        client.search_works("test", page=0)
    with pytest.raises(ValueError, match="per_page"):
        client.search_works("test", per_page=101)
    with pytest.raises(ValueError, match="from_year"):
        client.search_works("test", from_year=2025, to_year=2024)
