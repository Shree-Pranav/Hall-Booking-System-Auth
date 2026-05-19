"""add server defaults for users timestamps

Revision ID: 20260519_add_user_timestamps_defaults
Revises: 1372cb775cc5
Create Date: 2026-05-19 05:54:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260519a'
down_revision = '1372cb775cc5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # backfill any NULLs to avoid NOT NULL violations
    # asyncpg (used by SQLAlchemy asyncpg dialect) does not allow multiple
    # SQL statements in a single prepared statement. Execute them separately.
    op.execute("UPDATE users SET created_at = now() WHERE created_at IS NULL;")
    op.execute("UPDATE users SET updated_at = now() WHERE updated_at IS NULL;")

    # set server defaults for users.created_at and users.updated_at
    op.alter_column(
        'users',
        'created_at',
        existing_type=sa.DateTime(),
        server_default=sa.text('now()'),
        existing_nullable=False,
    )
    op.alter_column(
        'users',
        'updated_at',
        existing_type=sa.DateTime(),
        server_default=sa.text('now()'),
        existing_nullable=False,
    )


def downgrade() -> None:
    # revert server defaults
    op.alter_column(
        'users',
        'created_at',
        existing_type=sa.DateTime(),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        'users',
        'updated_at',
        existing_type=sa.DateTime(),
        server_default=None,
        existing_nullable=False,
    )
