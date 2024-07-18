"""fixed author name

Revision ID: 05c50ad62d54
Revises: 1ed8ef099557
Create Date: 2024-06-04 18:35:39.860413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05c50ad62d54'
down_revision: Union[str, None] = '1ed8ef099557'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('author', sa.String(), nullable=False))
    op.drop_constraint('posts_author_id_fkey', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'users', ['author'], ['username'])
    op.drop_column('posts', 'author_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key('posts_author_id_fkey', 'posts', 'users', ['author_id'], ['id'])
    op.drop_column('posts', 'author')
    # ### end Alembic commands ###