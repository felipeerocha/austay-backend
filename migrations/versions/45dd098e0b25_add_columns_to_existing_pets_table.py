"""add columns to existing pets table

Revision ID: 45dd098e0b25
Revises: f759e55081e7
Create Date: 2025-09-07 14:55:13.074580

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "45dd098e0b25"
down_revision: Union[str, Sequence[str], None] = "f759e55081e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: cria a tabela pets completa."""
    op.create_table(
        "pets",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("nome", sa.String(), nullable=False),
        sa.Column("especie", sa.String(), nullable=False),
        sa.Column("raca", sa.String(), nullable=False),
        sa.Column("nascimento", sa.String(), nullable=True),
        sa.Column("sexo", sa.String(), nullable=False),
        sa.Column("vermifugado", sa.Boolean(), nullable=True),
        sa.Column("vacinado", sa.Boolean(), nullable=True),
        sa.Column("tutor_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["tutor_id"], ["tutors.id"], ondelete="CASCADE"),
    )

    # Índices
    op.create_index(op.f("ix_pets_nome"), "pets", ["nome"])
    op.create_index(op.f("ix_pets_especie"), "pets", ["especie"])
    op.create_index(op.f("ix_pets_raca"), "pets", ["raca"])
    op.create_index(op.f("ix_pets_sexo"), "pets", ["sexo"])
    op.create_index(op.f("ix_pets_tutor_id"), "pets", ["tutor_id"])





def downgrade() -> None:
    """Downgrade schema: remove a tabela pets."""
    op.drop_index(op.f("ix_pets_tutor_id"), table_name="pets")
    op.drop_index(op.f("ix_pets_sexo"), table_name="pets")
    op.drop_index(op.f("ix_pets_raca"), table_name="pets")
    op.drop_index(op.f("ix_pets_especie"), table_name="pets")
    op.drop_index(op.f("ix_pets_nome"), table_name="pets")
    op.drop_table("pets")
