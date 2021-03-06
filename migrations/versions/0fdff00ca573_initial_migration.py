"""Initial migration.

Revision ID: 0fdff00ca573
Revises: 
Create Date: 2021-09-11 19:36:26.345025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fdff00ca573'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('actor')
    op.drop_table('movie')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actor',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('gender', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('movie_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], name='actor_movie_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='actor_pkey')
    )
    op.create_table('movie',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('release_date', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='movie_pkey')
    )
    # ### end Alembic commands ###
