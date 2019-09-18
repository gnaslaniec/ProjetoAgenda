"""Adicionando a tabela de Contatos

Revision ID: cf0d3aebebde
Revises: 
Create Date: 2019-09-18 10:55:45.158024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf0d3aebebde'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contatos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.Text(), nullable=True),
    sa.Column('data_nascimento', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contatos')
    # ### end Alembic commands ###
