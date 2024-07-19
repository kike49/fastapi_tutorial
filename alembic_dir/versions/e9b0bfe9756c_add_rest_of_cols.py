"""add rest of cols

Revision ID: e9b0bfe9756c
Revises: 287187425729
Create Date: 2024-07-19 10:05:44.800634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision: str = 'e9b0bfe9756c'
down_revision: Union[str, None] = '287187425729'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('posts', 'published', existing_type=sa.Boolean(), server_default="TRUE", nullable=False)
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")))


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass