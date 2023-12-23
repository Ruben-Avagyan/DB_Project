"""added extra column for car

Revision ID: b6ed91772356
Revises: 
Create Date: 2023-12-23 21:45:38.688187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6ed91772356'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("car", sa.Column("extra_data", sa.String, nullable=True))


def downgrade() -> None:
    op.drop_column("car", "extra_data")
