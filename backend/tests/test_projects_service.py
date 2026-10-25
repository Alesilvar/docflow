from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.models import Base, Paper, ProjectPaper
from app.integrations.openalex import PaperSearchItem
from app.services.projects import create_project, save_paper_to_project


def test_project_save_is_idempotent_and_reuses_global_paper() -> None:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    item = PaperSearchItem("https://openalex.org/W1", "Example", 2024, ["Ada"], None, None, "https://example.org")
    with Session(engine) as session:
        first = create_project(session, "First", None)
        second = create_project(session, "Second", None)
        _, created = save_paper_to_project(session, first.id, item)
        _, duplicate = save_paper_to_project(session, first.id, item)
        _, reused = save_paper_to_project(session, second.id, item)
        assert created is True
        assert duplicate is False
        assert reused is True
        assert session.query(Paper).count() == 1
        assert session.query(ProjectPaper).count() == 2
