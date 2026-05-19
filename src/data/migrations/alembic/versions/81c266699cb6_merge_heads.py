"""merge heads

Revision ID: 81c266699cb6
Revises: 20260519_add_user_timestamps_defaults, 8495c23c6eb9
Create Date: 2026-05-19 06:05:36.652262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81c266699cb6'
down_revision: Union[str, Sequence[str], None] = ('20260519a', '8495c23c6eb9')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
