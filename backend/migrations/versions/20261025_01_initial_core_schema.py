"""initial core schema

Revision ID: 20261025_01
Revises:
Create Date: 2026-10-25
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20261025_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("research_projects", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("name", sa.String(200), nullable=False), sa.Column("research_question", sa.Text(), nullable=True), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False))
    op.create_table("papers", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("openalex_id", sa.String(100), nullable=False), sa.Column("doi", sa.String(300), nullable=True), sa.Column("title", sa.Text(), nullable=False), sa.Column("publication_year", sa.Integer(), nullable=True), sa.Column("landing_url", sa.Text(), nullable=False), sa.Column("abstract_text", sa.Text(), nullable=True), sa.Column("source_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False), sa.UniqueConstraint("openalex_id"))
    op.create_index("ix_papers_openalex_id", "papers", ["openalex_id"])
    op.create_index("ix_papers_doi", "papers", ["doi"])
    op.create_table("project_papers", sa.Column("project_id", sa.Uuid(), sa.ForeignKey("research_projects.id", ondelete="CASCADE"), primary_key=True), sa.Column("paper_id", sa.Uuid(), sa.ForeignKey("papers.id", ondelete="CASCADE"), primary_key=True), sa.Column("notes", sa.Text(), nullable=True), sa.Column("status", sa.String(30), nullable=False), sa.Column("added_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False), sa.UniqueConstraint("project_id", "paper_id", name="uq_project_papers_project_paper"))


def downgrade() -> None:
    op.drop_table("project_papers")
    op.drop_index("ix_papers_doi", table_name="papers")
    op.drop_index("ix_papers_openalex_id", table_name="papers")
    op.drop_table("papers")
    op.drop_table("research_projects")
