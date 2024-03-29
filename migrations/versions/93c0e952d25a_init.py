"""init

Revision ID: 93c0e952d25a
Revises: 
Create Date: 2019-12-14 13:26:58.283323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93c0e952d25a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('anime',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('season', sa.String(length=140), nullable=True),
    sa.Column('year', sa.String(length=140), nullable=True),
    sa.Column('num_episodes', sa.String(length=140), nullable=True),
    sa.Column('esrb', sa.String(length=140), nullable=True),
    sa.Column('description', sa.String(length=5000), nullable=True),
    sa.Column('image', sa.String(length=140), nullable=True),
    sa.Column('url', sa.String(length=140), nullable=True),
    sa.Column('studio', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('anime_genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('anime_name', sa.String(length=140), nullable=True),
    sa.Column('genre', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pending_anime',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('season', sa.String(length=140), nullable=True),
    sa.Column('year', sa.String(length=140), nullable=True),
    sa.Column('num_episodes', sa.String(length=140), nullable=True),
    sa.Column('esrb', sa.String(length=140), nullable=True),
    sa.Column('description', sa.String(length=5000), nullable=True),
    sa.Column('image', sa.String(length=140), nullable=True),
    sa.Column('url', sa.String(length=140), nullable=True),
    sa.Column('studio', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pending_waifu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('description', sa.String(length=5000), nullable=True),
    sa.Column('image', sa.String(length=140), nullable=True),
    sa.Column('url', sa.String(length=140), nullable=True),
    sa.Column('anime_name', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('studio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('admin_flag', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('waifu_tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('waifu_name', sa.String(length=140), nullable=True),
    sa.Column('tag', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    op.create_table('waifu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('description', sa.String(length=5000), nullable=True),
    sa.Column('image', sa.String(length=140), nullable=True),
    sa.Column('url', sa.String(length=140), nullable=True),
    sa.Column('anime_name', sa.String(length=140), nullable=True),
    sa.Column('anime_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['anime_id'], ['anime.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('appearance', sa.String(length=140), nullable=True),
    sa.Column('personality', sa.String(length=140), nullable=True),
    sa.Column('strength', sa.String(length=140), nullable=True),
    sa.Column('intelligence', sa.String(length=140), nullable=True),
    sa.Column('wouldyou', sa.String(length=140), nullable=True),
    sa.Column('body', sa.String(length=5000), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('waifu_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['waifu_id'], ['waifu.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rating_timestamp'), 'rating', ['timestamp'], unique=False)
    op.create_table('waifu_averages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('waifu_id', sa.Integer(), nullable=True),
    sa.Column('appearance_total', sa.String(length=140), nullable=True),
    sa.Column('personality_total', sa.String(length=140), nullable=True),
    sa.Column('strength_total', sa.String(length=140), nullable=True),
    sa.Column('intelligence_total', sa.String(length=140), nullable=True),
    sa.Column('num_ratings', sa.String(length=140), nullable=True),
    sa.ForeignKeyConstraint(['waifu_id'], ['waifu.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('waifu_averages')
    op.drop_index(op.f('ix_rating_timestamp'), table_name='rating')
    op.drop_table('rating')
    op.drop_table('waifu')
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    op.drop_table('followers')
    op.drop_table('waifu_tags')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('studio')
    op.drop_table('pending_waifu')
    op.drop_table('pending_anime')
    op.drop_table('anime_genres')
    op.drop_table('anime')
    # ### end Alembic commands ###
