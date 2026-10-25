import csv
from io import StringIO
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.papers import error_response
from app.db.models import Paper, ProjectPaper, ResearchProject
from app.db.session import get_session
from app.integrations.openalex import PaperSearchItem
from app.services.projects import ProjectNotFoundError, create_project, list_project_papers, remove_paper_from_project, save_paper_to_project, update_project_paper

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


class RemovePaperResponse(BaseModel):
    removed: bool


class SavedPaperResponse(BaseModel):
    id: UUID
    openalex_id: str
    title: str
    year: int | None
    authors: list[str]
    doi: str | None
    abstract: str | None
    source_url: str
    notes: str | None = None
    status: str


class ProjectPaperUpdateRequest(BaseModel):
    notes: str | None = Field(default=None, max_length=10000)
    status: str | None = Field(default=None, max_length=30)


def project_response(project: ResearchProject) -> ProjectResponse:
    return ProjectResponse(id=project.id, name=project.name, research_question=project.research_question)


def saved_paper_response(paper: Paper, link: ProjectPaper) -> SavedPaperResponse:
    return SavedPaperResponse(id=paper.id, openalex_id=paper.openalex_id, title=paper.title, year=paper.publication_year, authors=[], doi=paper.doi, abstract=paper.abstract_text, source_url=paper.landing_url, notes=link.notes, status=link.status)


def project_paper_rows(session: Session, project_id: UUID) -> list[tuple[Paper, ProjectPaper]]:
    return list(session.execute(select(Paper, ProjectPaper).join(ProjectPaper).where(ProjectPaper.project_id == project_id).order_by(ProjectPaper.added_at.desc())))


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


@router.get("/{project_id}/papers", response_model=list[SavedPaperResponse])
def list_saved_papers(project_id: UUID, session: Session = Depends(get_session)) -> list[SavedPaperResponse] | JSONResponse:
    try:
        list_project_papers(session, project_id)
        return [saved_paper_response(paper, link) for paper, link in project_paper_rows(session, project_id)]
    except ProjectNotFoundError:
        return error_response(404, "project_not_found", "The requested project does not exist.")


@router.delete("/{project_id}/papers/{paper_id}", response_model=RemovePaperResponse)
def remove_saved_paper(project_id: UUID, paper_id: UUID, session: Session = Depends(get_session)) -> RemovePaperResponse | JSONResponse:
    try:
        removed = remove_paper_from_project(session, project_id, paper_id)
    except ProjectNotFoundError:
        return error_response(404, "project_not_found", "The requested project does not exist.")
    if not removed:
        return error_response(404, "project_paper_not_found", "The article is not saved in this project.")
    session.commit()
    return RemovePaperResponse(removed=True)


@router.patch("/{project_id}/papers/{paper_id}", response_model=SavedPaperResponse)
def update_saved_paper(project_id: UUID, paper_id: UUID, payload: ProjectPaperUpdateRequest, session: Session = Depends(get_session)) -> SavedPaperResponse | JSONResponse:
    try:
        link = update_project_paper(session, project_id, paper_id, **payload.model_dump(exclude_unset=True))
    except ProjectNotFoundError:
        return error_response(404, "project_not_found", "The requested project does not exist.")
    if link is None:
        return error_response(404, "project_paper_not_found", "The article is not saved in this project.")
    paper = session.get(Paper, paper_id)
    session.commit()
    return saved_paper_response(paper, link)


@router.get("/{project_id}/export.csv", response_model=None)
def export_project_csv(project_id: UUID, session: Session = Depends(get_session)) -> Response | JSONResponse:
    try:
        list_project_papers(session, project_id)
    except ProjectNotFoundError:
        return error_response(404, "project_not_found", "The requested project does not exist.")
    output = StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["title", "year", "doi", "source_url", "status", "notes", "abstract"])
    for paper, link in project_paper_rows(session, project_id):
        writer.writerow([paper.title, paper.publication_year or "", paper.doi or "", paper.landing_url, link.status, link.notes or "", paper.abstract_text or ""])
    return Response(output.getvalue().encode("utf-8-sig"), media_type="text/csv; charset=utf-8", headers={"Content-Disposition": f'attachment; filename="researchflow-{project_id}.csv"'})
