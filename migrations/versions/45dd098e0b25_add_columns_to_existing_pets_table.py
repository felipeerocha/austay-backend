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
    """Upgrade schema."""
    op.add_column("pets", sa.Column("nome", sa.String(), nullable=False))
    op.add_column("pets", sa.Column("especie", sa.String(), nullable=False))
    op.add_column("pets", sa.Column("raca", sa.String(), nullable=False))
    op.add_column("pets", sa.Column("nascimento", sa.String(), nullable=True))
    op.add_column("pets", sa.Column("sexo", sa.String(), nullable=False))
    op.add_column("pets", sa.Column("vermifugado", sa.Boolean(), nullable=True))
    op.add_column("pets", sa.Column("vacinado", sa.Boolean(), nullable=True))
    op.add_column("pets", sa.Column("tutor_id", sa.UUID(), nullable=False))

    op.create_index(op.f("ix_pets_nome"), "pets", ["nome"])
    op.create_index(op.f("ix_pets_especie"), "pets", ["especie"])
    op.create_index(op.f("ix_pets_raca"), "pets", ["raca"])
    op.create_index(op.f("ix_pets_sexo"), "pets", ["sexo"])
    op.create_index(op.f("ix_pets_tutor_id"), "pets", ["tutor_id"])

    op.create_foreign_key("fk_pet_tutor", "pets", "tutors", ["tutor_id"], ["id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_pet_tutor", "pets", type_="foreignkey")

    op.drop_index(op.f("ix_pets_tutor_id"), table_name="pets")
    op.drop_index(op.f("ix_pets_sexo"), table_name="pets")
    op.drop_index(op.f("ix_pets_raca"), table_name="pets")
    op.drop_index(op.f("ix_pets_especie"), table_name="pets")
    op.drop_index(op.f("ix_pets_nome"), table_name="pets")

    op.drop_column("pets", "tutor_id")
    op.drop_column("pets", "vacinado")
    op.drop_column("pets", "vermifugado")
    op.drop_column("pets", "sexo")
    op.drop_column("pets", "nascimento")
    op.drop_column("pets", "raca")
    op.drop_column("pets", "especie")
    op.drop_column("pets", "nome")
