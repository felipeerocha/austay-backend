"""Refatora logica de pagamento e estadia

Revision ID: 4f60da275a93
Revises: 24c8d45059b5
Create Date: 2025-11-12 09:21:00.686552

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql # Import necessário

# revision identifiers, used by Alembic.
revision: str = '4f60da275a93'
down_revision: Union[str, Sequence[str], None] = '24c8d45059b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### Comandos ajustados manualmente ###
    
    # --- Alterações na tabela ESTADIA ---
    op.add_column('estadia', sa.Column('valor_total', sa.Float(), nullable=True))
    op.alter_column('estadia', 'pago',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               server_default=sa.text('false')) # Boa prática adicionar o default no DB

    # --- Alterações na tabela PAGAMENTO ---
    op.add_column('pagamento', sa.Column('valor_total', sa.Float(), nullable=True))
    op.alter_column('pagamento', 'valor',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('pagamento', 'meio_pagamento',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('pagamento', 'data_pagamento',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # --- CORREÇÃO 1: Conversão de String para Boolean ---
    # O 'postgresql_using' ensina o Postgres a converter os dados
    op.alter_column('pagamento', 'status',
               existing_type=sa.VARCHAR(),
               type_=sa.Boolean(),
               nullable=False,
               server_default=sa.text('false'),
               # ASSUMINDO que seu status 'pago' era a string 'pago'. Ajuste se for diferente.
               postgresql_using="(status = 'pago')")

    # --- Alterações de Constraint (FK e Unique) ---
    op.create_unique_constraint('uq_pagamento_estadia_id', 'pagamento', ['estadia_id'])
    
    # O nome da FK pode ser diferente, 'pagamento_estadia_id_fkey' é um chute comum.
    # Se der erro aqui, verifique o nome da constraint no seu DB.
    try:
        op.drop_constraint('pagamento_estadia_id_fkey', 'pagamento', type_='foreignkey')
    except Exception:
        print("Aviso: Não foi possível dropar a constraint 'pagamento_estadia_id_fkey'. "
              "Verifique o nome no seu banco de dados se a migração falhar.")

    op.create_foreign_key(
        'pagamento_estadia_id_fkey', # Dando um nome explícito
        'pagamento', 'estadia', 
        ['estadia_id'], ['id'], 
        ondelete='CASCADE'
    )
    
    # --- CORREÇÃO 2: Lógica de Backfill de Dados ---
    # Cria os registros de 'pagamento' faltantes para 'estadia' antigas
    op.execute("""
        INSERT INTO pagamento (id, estadia_id, status, valor, valor_total, meio_pagamento, data_pagamento)
        SELECT 
            gen_random_uuid(),  -- Gera um novo UUID para o pagamento
            e.id,               -- ID da estadia
            e.pago,             -- Sincroniza o status com a estadia (que já é boolean)
            NULL,               -- Valor (será preenchido no pagamento)
            NULL,               -- Valor Total (será preenchido no pagamento)
            NULL,               -- Meio (será preenchido no pagamento)
            NULL                -- Data (será preenchido no pagamento)
        FROM estadia e
        WHERE e.id NOT IN (SELECT p.estadia_id FROM pagamento p WHERE p.estadia_id IS NOT NULL)
    """)
    # ### Fim dos comandos ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### Comandos ajustados manualmente ###
    
    # Reverter o downgrade é complexo e perigoso
    
    op.drop_constraint('pagamento_estadia_id_fkey', 'pagamento', type_='foreignkey')
    op.create_foreign_key('pagamento_estadia_id_fkey', 'pagamento', 'estadia', ['estadia_id'], ['id'])
    op.drop_constraint('uq_pagamento_estadia_id', 'pagamento', type_='unique')
    op.alter_column('pagamento', 'data_pagamento',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('pagamento', 'meio_pagamento',
               existing_type=sa.VARCHAR(),
               nullable=False)
    
    # --- Revertendo Boolean para String ---
    op.alter_column('pagamento', 'status',
               existing_type=sa.Boolean(),
               type_=sa.VARCHAR(),
               nullable=False,
               server_default=None,
               postgresql_using="CASE WHEN status THEN 'pago' ELSE 'nao_pago' END")

    op.alter_column('pagamento', 'valor',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.drop_column('pagamento', 'valor_total')
    op.alter_column('estadia', 'pago',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               server_default=None)
    op.drop_column('estadia', 'valor_total')
    # ### Fim dos comandos ###