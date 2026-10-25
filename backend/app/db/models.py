from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ResearchProject(Base):
    __tablename__ = "research_projects"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(200))
    research_question: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Paper(Base):
    __tablename__ = "papers"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    openalex_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    doi: Mapped[str | None] = mapped_column(String(300), nullable=True, index=True)
    title: Mapped[str] = mapped_column(Text)
    publication_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    landing_url: Mapped[str] = mapped_column(Text)
    abstract_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_payload: Mapped[dict] = mapped_column(JSON().with_variant(JSONB, "postgresql"), default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ProjectPaper(Base):
    __tablename__ = "project_papers"
    __table_args__ = (UniqueConstraint("project_id", "paper_id", name="uq_project_papers_project_paper"),)

    project_id: Mapped[UUID] = mapped_column(ForeignKey("research_projects.id", ondelete="CASCADE"), primary_key=True)
    paper_id: Mapped[UUID] = mapped_column(ForeignKey("papers.id", ondelete="CASCADE"), primary_key=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="saved")
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
