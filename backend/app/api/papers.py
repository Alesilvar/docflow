"""Paper search API routes."""

from __future__ import annotations

from collections.abc import Generator
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.integrations.openalex import (
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    OpenAlexClient,
    OpenAlexRateLimitError,
    OpenAlexTimeoutError,
    OpenAlexUpstreamError,
    PaperSearchItem,
    PaperSearchPage,
)

router = APIRouter(prefix="/api/v1/papers", tags=["papers"])


class PaperSearchItemResponse(BaseModel):
    openalex_id: str
    title: str
    year: int | None
    authors: list[str]
    doi: str | None
    abstract: str | None
    source_url: str


class PaperSearchResponse(BaseModel):
    items: list[PaperSearchItemResponse]
    page: int
    has_next: bool
    total_count: int | None


def get_openalex_client() -> Generator[OpenAlexClient, None, None]:
    """Provide and safely close one OpenAlex client per request."""

    client = OpenAlexClient()
    try:
        yield client
    finally:
        client.close()


def to_response_item(item: PaperSearchItem) -> PaperSearchItemResponse:
    return PaperSearchItemResponse(
        openalex_id=item.openalex_id,
        title=item.title,
        year=item.year,
        authors=item.authors,
        doi=item.doi,
        abstract=item.abstract,
        source_url=item.source_url,
    )


def to_search_response(page: PaperSearchPage) -> PaperSearchResponse:
    return PaperSearchResponse(
        items=[to_response_item(item) for item in page.items],
        page=page.page,
        has_next=page.has_next,
        total_count=page.total_count,
    )


def error_response(status_code: int, code: str, message: str) -> JSONResponse:
    """Return a consistent API error without exposing upstream internals."""

    return JSONResponse(
        status_code=status_code,
        content={
            "error": {"code": code, "message": message},
            "request_id": str(uuid4()),
        },
    )


@router.get(
    "/search",
    response_model=PaperSearchResponse,
    responses={
        400: {"description": "Invalid search parameters"},
        429: {"description": "OpenAlex rate limit reached"},
        503: {"description": "OpenAlex is unavailable"},
        504: {"description": "OpenAlex timed out"},
    },
)
def search_papers(
    query: Annotated[str, Query(min_length=1, max_length=500)],
    from_year: Annotated[int | None, Query(ge=1000, le=2100)] = None,
    to_year: Annotated[int | None, Query(ge=1000, le=2100)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,
    client: OpenAlexClient = Depends(get_openalex_client),
) -> PaperSearchResponse | JSONResponse:
    """Search publications through the OpenAlex adapter."""

    try:
        results = client.search_works(
            query,
            from_year=from_year,
            to_year=to_year,
            page=page,
            per_page=per_page,
        )
    except ValueError as exc:
        return error_response(400, "invalid_search_parameters", str(exc))
    except OpenAlexRateLimitError:
        return error_response(429, "openalex_rate_limited", "OpenAlex is temporarily rate limited.")
    except OpenAlexTimeoutError:
        return error_response(504, "openalex_timeout", "OpenAlex did not respond in time.")
    except OpenAlexUpstreamError:
        return error_response(503, "openalex_unavailable", "OpenAlex is temporarily unavailable.")

    return to_search_response(results)
