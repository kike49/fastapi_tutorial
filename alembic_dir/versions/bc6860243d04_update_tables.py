"""update tables

Revision ID: bc6860243d04
Revises: 
Create Date: 2024-07-10 19:02:26.709872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc6860243d04'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# To modify tables
def upgrade() -> None:
    op.create_table('posts', sa.Column("id", sa.Integer(), nullable=False, primary_key=True), sa.Column("title", sa.String(), nullable=False), sa.Column("content", sa.String(), nullable=False), sa.Column("published", sa.Boolean(), nullable=False))
    pass

# To delete tables
def downgrade() -> None:
    op.drop_table("posts")
    pass
