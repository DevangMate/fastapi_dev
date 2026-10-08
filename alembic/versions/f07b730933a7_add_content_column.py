"""add_content_column

Revision ID: f07b730933a7
Revises: d5d172f521a1
Create Date: 2026-10-07 20:52:30.747471

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f07b730933a7'
down_revision: Union[str, Sequence[str], None] = 'd5d172f521a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
    "posts",
    sa.Column('content',sa.String(),nullable=False)
    )
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    
