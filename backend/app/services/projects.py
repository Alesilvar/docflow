from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Paper, ProjectPaper, ResearchProject
from app.integrations.openalex import PaperSearchItem


class ProjectNotFoundError(Exception):
    pass


def create_project(session: Session, name: str, research_question: str | None) -> ResearchProject:
    project = ResearchProject(name=name.strip(), research_question=research_question)
    session.add(project)
    session.flush()
    return project


def save_paper_to_project(session: Session, project_id: UUID, item: PaperSearchItem) -> tuple[Paper, bool]:
    project = session.get(ResearchProject, project_id)
    if project is None:
        raise ProjectNotFoundError

    paper = session.scalar(select(Paper).where(Paper.openalex_id == item.openalex_id))
    if paper is None:
        paper = Paper(
            openalex_id=item.openalex_id, doi=item.doi, title=item.title,
            publication_year=item.year, landing_url=item.source_url, abstract_text=item.abstract,
            source_payload={},
        )
        session.add(paper)
        session.flush()

    link = session.get(ProjectPaper, {"project_id": project.id, "paper_id": paper.id})
    if link is not None:
        return paper, False
    session.add(ProjectPaper(project_id=project.id, paper_id=paper.id))
    session.flush()
    return paper, True


def list_project_papers(session: Session, project_id: UUID) -> list[Paper]:
    if session.get(ResearchProject, project_id) is None:
        raise ProjectNotFoundError
    statement = select(Paper).join(ProjectPaper).where(ProjectPaper.project_id == project_id).order_by(ProjectPaper.added_at.desc())
    return list(session.scalars(statement))


def remove_paper_from_project(session: Session, project_id: UUID, paper_id: UUID) -> bool:
    if session.get(ResearchProject, project_id) is None:
        raise ProjectNotFoundError
    link = session.get(ProjectPaper, {"project_id": project_id, "paper_id": paper_id})
    if link is None:
        return False
    session.delete(link)
    session.flush()
    return True


def update_project_paper(session: Session, project_id: UUID, paper_id: UUID, *, notes: str | None = None, status: str | None = None) -> ProjectPaper | None:
    if session.get(ResearchProject, project_id) is None:
        raise ProjectNotFoundError
    link = session.get(ProjectPaper, {"project_id": project_id, "paper_id": paper_id})
    if link is None:
        return None
    if notes is not None:
        link.notes = notes
    if status is not None:
        link.status = status
    session.flush()
    return link
