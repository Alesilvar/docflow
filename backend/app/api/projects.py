from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.papers import error_response
from app.db.models import ResearchProject
from app.db.session import get_session
from app.integrations.openalex import PaperSearchItem
from app.services.projects import ProjectNotFoundError, create_project, save_paper_to_project

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


class ProjectCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    research_question: str | None = Field(default=None, max_length=5000)


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    research_question: str | None


class SavePaperRequest(BaseModel):
    openalex_id: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1)
    year: int | None = Field(default=None, ge=1000, le=2100)
    authors: list[str] = Field(default_factory=list)
    doi: str | None = None
    abstract: str | None = None
    source_url: str = Field(min_length=1)


class SavePaperResponse(BaseModel):
    paper_id: UUID
    saved: bool


def project_response(project: ResearchProject) -> ProjectResponse:
    return ProjectResponse(id=project.id, name=project.name, research_question=project.research_question)


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project_route(payload: ProjectCreateRequest, session: Session = Depends(get_session)) -> ProjectResponse:
    project = create_project(session, payload.name, payload.research_question)
    session.commit()
    return project_response(project)


@router.get("", response_model=list[ProjectResponse])
def list_projects(session: Session = Depends(get_session)) -> list[ProjectResponse]:
    projects = session.scalars(select(ResearchProject).order_by(ResearchProject.created_at.desc())).all()
    return [project_response(project) for project in projects]


@router.post("/{project_id}/papers", response_model=SavePaperResponse)
def save_project_paper(
    project_id: UUID,
    payload: SavePaperRequest,
    session: Session = Depends(get_session),
) -> SavePaperResponse | JSONResponse:
    item = PaperSearchItem(**payload.model_dump())
    try:
        paper, saved = save_paper_to_project(session, project_id, item)
    except ProjectNotFoundError:
        return error_response(404, "project_not_found", "The requested project does not exist.")
    session.commit()
    return SavePaperResponse(paper_id=paper.id, saved=saved)
