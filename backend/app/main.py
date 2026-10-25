"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.papers import router as papers_router
from app.api.projects import router as projects_router

app = FastAPI(
    title="ResearchFlow AI API",
    version="0.1.0",
    description="API for the ResearchFlow AI literature-review workflow.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(papers_router)
app.include_router(projects_router)


@app.get("/api/v1/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Return a lightweight status response for local checks and CI."""
    return {"status": "ok", "service": "researchflow-api"}
