"""add user table

Revision ID: 85982eeb2db7
Revises: bc6860243d04
Create Date: 2024-07-19 09:35:42.290365

"""
from sqlalchemy.sql.sqltypes import TIMESTAMP
from typing import Sequence, Union
from sqlalchemy.sql.expression import text

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85982eeb2db7'
down_revision: Union[str, None] = 'bc6860243d04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column("id", sa.Integer(), nullable=False, primary_key=True), sa.Column("email", sa.String(), nullable=False, unique=True), sa.Column("password", sa.String(), nullable=False), sa.Column("registered_on", sa.TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False))


def downgrade() -> None:
    op.drop_table("users")
    pass
