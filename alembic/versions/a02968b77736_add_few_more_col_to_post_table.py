"""add few more col to post table

Revision ID: a02968b77736
Revises: 00aa02c9e764
Create Date: 2026-10-07 23:18:47.859309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a02968b77736'
down_revision: Union[str, Sequence[str], None] = '00aa02c9e764'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('published',sa.Boolean(),nullable=False,server_default='True')
        )
    op.add_column(
        'posts',
        sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False)
        )
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
