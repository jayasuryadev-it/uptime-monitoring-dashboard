"""initial_schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-09-17 16:10:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # 2. monitors table
    op.create_table(
        'monitors',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('url', sa.String(length=2048), nullable=False),
        sa.Column('interval', sa.Integer(), nullable=False, server_default='60'),
        sa.Column('timeout', sa.Integer(), nullable=False, server_default='10'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_monitors_user_id'), 'monitors', ['user_id'], unique=False)

    # 3. health_checks table
    op.create_table(
        'health_checks',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('monitor_id', sa.String(length=36), nullable=False),
        sa.Column('status', sa.String(length=10), nullable=False),
        sa.Column('status_code', sa.Integer(), nullable=True),
        sa.Column('response_time', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('checked_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['monitor_id'], ['monitors.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_health_checks_monitor_id'), 'health_checks', ['monitor_id'], unique=False)
    op.create_index(op.f('ix_health_checks_checked_at'), 'health_checks', ['checked_at'], unique=False)

    # 4. incidents table
    op.create_table(
        'incidents',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('monitor_id', sa.String(length=36), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['monitor_id'], ['monitors.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_incidents_monitor_id'), 'incidents', ['monitor_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_incidents_monitor_id'), table_name='incidents')
    op.drop_table('incidents')
    op.drop_index(op.f('ix_health_checks_checked_at'), table_name='health_checks')
    op.drop_index(op.f('ix_health_checks_monitor_id'), table_name='health_checks')
    op.drop_table('health_checks')
    op.drop_index(op.f('ix_monitors_user_id'), table_name='monitors')
    op.drop_table('monitors')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
