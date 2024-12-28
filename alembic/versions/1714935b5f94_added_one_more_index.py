"""Added one more index

Revision ID: 1714935b5f94
Revises: c3d7159fe22e
Create Date: 2024-12-28 14:12:33.992630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1714935b5f94'
down_revision: Union[str, None] = 'c3d7159fe22e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gang_members', sa.Column('height', sa.DECIMAL(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('gang_members', 'height')
    # ### end Alembic commands ###