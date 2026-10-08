"""create posts table

Revision ID: d5d172f521a1
Revises: 
Create Date: 2026-10-07 00:06:19.889027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5d172f521a1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'posts',
        sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
        sa.Column('title',sa.String(),nullable=False)
    )
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    
