"""Cria tabelas jogadores, pontos e jogadas

Revision ID: 3371e7c4b1a2
Revises: 
Create Date: 2025-05-23 14:45:51.155746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3371e7c4b1a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jogadores',
    sa.Column('cpf', sa.String(length=11), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('cpf')
    )
    op.create_table('jogadas',
    sa.Column('cpf', sa.String(length=11), nullable=False),
    sa.Column('jogadas', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cpf'], ['jogadores.cpf'], ),
    sa.PrimaryKeyConstraint('cpf')
    )
    op.create_table('pontos',
    sa.Column('cpf', sa.String(length=11), nullable=False),
    sa.Column('pontos', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cpf'], ['jogadores.cpf'], ),
    sa.PrimaryKeyConstraint('cpf')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pontos')
    op.drop_table('jogadas')
    op.drop_table('jogadores')
    # ### end Alembic commands ###
