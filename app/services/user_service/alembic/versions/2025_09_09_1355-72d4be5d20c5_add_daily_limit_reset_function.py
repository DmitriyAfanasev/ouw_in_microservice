"""add_daily_limit_reset_function

Revision ID: 72d4be5d20c5
Revises: 90ae1880f72e
Create Date: 2025-09-09 13:55:39.963511+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "72d4be5d20c5"
down_revision: str | Sequence[str] | None = "90ae1880f72e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade():
    # Включаем расширение pg_cron (если еще не включено)
    op.execute(sa.text("CREATE EXTENSION IF NOT EXISTS pg_cron;"))

    # Создаем функцию для сброса лимитов
    op.execute(
        sa.text(
            """
        CREATE OR REPLACE FUNCTION reset_api_key_limits()
        RETURNS void AS $$
        BEGIN
            UPDATE api_keys
            SET limit_requests = 200
            WHERE is_active = true;
            RAISE NOTICE 'API key limits reset successfully at %', now();
        END;
        $$ LANGUAGE plpgsql;
    """
        )
    )

    # Настраиваем ежедневный запуск в 00:00
    op.execute(
        sa.text(
            """
        SELECT cron.schedule(
            'reset-api-key-limits-daily',  -- имя задания
            '0 0 * * *',                   -- каждый день в 00:00 (cron syntax)
            'SELECT reset_api_key_limits()' -- что выполнять
        );
    """
        )
    )


def downgrade():
    # Удаляем задание из планировщика
    op.execute(
        sa.text(
            """
        SELECT cron.unschedule('reset-api-key-limits-daily');
    """
        )
    )

    # Удаляем функцию
    op.execute(
        sa.text(
            """
        DROP FUNCTION IF EXISTS reset_api_key_limits();
    """
        )
    )

    # Отключаем расширение (опционально)
    op.execute(
        sa.text(
            """
        DROP EXTENSION IF EXISTS pg_cron;
    """
        )
    )
