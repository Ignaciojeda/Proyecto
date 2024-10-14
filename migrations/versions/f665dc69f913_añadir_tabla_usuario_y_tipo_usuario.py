"""Añadir tabla usuario y tipo usuario

Revision ID: f665dc69f913
Revises: 
Create Date: 2024-10-14 00:07:47.445010

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f665dc69f913'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tipo_usuario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nombre', sa.String(length=50), nullable=False))
        batch_op.drop_column('descripcion')

    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.alter_column('contraseña',
               existing_type=mysql.VARCHAR(length=45),
               type_=sa.String(length=128),
               existing_nullable=False)
        batch_op.create_unique_constraint(None, ['correo_usuario'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('contraseña',
               existing_type=sa.String(length=128),
               type_=mysql.VARCHAR(length=45),
               existing_nullable=False)

    with op.batch_alter_table('tipo_usuario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('descripcion', mysql.VARCHAR(length=45), nullable=False))
        batch_op.drop_column('nombre')

    # ### end Alembic commands ###
