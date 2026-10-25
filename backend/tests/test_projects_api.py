from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.api.projects import ProjectCreateRequest, SavePaperRequest, create_project_route, export_project_csv, list_projects, save_project_paper
from app.db.models import Base


def test_project_routes_create_list_and_save_idempotently() -> None:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        project = create_project_route(ProjectCreateRequest(name="Thesis"), session)
        assert list_projects(session) == [project]
        payload = SavePaperRequest(openalex_id="https://openalex.org/W1", title="Paper", source_url="https://example.org")
        saved = save_project_paper(project.id, payload, session)
        duplicate = save_project_paper(project.id, payload, session)
        assert saved.saved is True
        assert duplicate.saved is False
        export = export_project_csv(project.id, session)
        assert export.media_type.startswith("text/csv")
        assert export.body.decode("utf-8-sig").startswith("title,year,doi,source_url,status,notes,abstract")
