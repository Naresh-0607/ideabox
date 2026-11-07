"""add ideas table

Revision ID: 8c3a2f1e4b7d
Revises: 1fb6376ef537
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "8c3a2f1e4b7d"
down_revision: Union[str, Sequence[str], None] = "1fb6376ef537"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ideas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ideas_id", "ideas", ["id"], unique=False)
    op.create_index("ix_ideas_user_id", "ideas", ["user_id"], unique=False)
    op.create_index("ix_ideas_status", "ideas", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_ideas_status", table_name="ideas")
    op.drop_index("ix_ideas_user_id", table_name="ideas")
    op.drop_index("ix_ideas_id", table_name="ideas")
    op.drop_table("ideas")
