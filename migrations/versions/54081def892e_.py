"""empty message

Revision ID: 54081def892e
Revises: 
Create Date: 2024-11-04 18:58:14.860132

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '54081def892e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('historial',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('correo', sa.String(length=100), nullable=False),
    sa.Column('carrera', sa.String(length=100), nullable=False),
    sa.Column('objeto_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['objeto_id'], ['objetos_perdidos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('objetos_perdidos', schema=None) as batch_op:
        batch_op.alter_column('activo',
               existing_type=mysql.TINYINT(),
               nullable=True)
        batch_op.alter_column('fecha_creacion',
               existing_type=mysql.DATETIME(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('objetos_perdidos', schema=None) as batch_op:
        batch_op.alter_column('fecha_creacion',
               existing_type=mysql.DATETIME(),
               nullable=False)
        batch_op.alter_column('activo',
               existing_type=mysql.TINYINT(),
               nullable=False)

    op.drop_table('historial')
    # ### end Alembic commands ###
