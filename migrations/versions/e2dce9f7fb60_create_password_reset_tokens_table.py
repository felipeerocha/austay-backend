"""create password_reset_tokens table

Revision ID: e2dce9f7fb60
Revises: 45dd098e0b25
Create Date: 2025-09-07 23:38:53.168321

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2dce9f7fb60'
down_revision: Union[str, Sequence[str], None] = '45dd098e0b25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'password_reset_tokens',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.UUID, nullable=False),
        sa.Column('token', sa.String(length=10), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('expires_at', sa.DateTime, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('password_reset_tokens')
