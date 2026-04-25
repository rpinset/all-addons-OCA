# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def _fill_microsoft_calendar_credentials_res_users(env):
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO microsoft_calendar_credentials (
            create_uid, write_uid, create_date, write_date,
            calendar_sync_token, synchronization_stopped
        )
        SELECT id, id, create_date, write_date,
            microsoft_calendar_sync_token, microsoft_synchronization_stopped
        FROM res_users
        WHERE microsoft_calendar_sync_token IS NOT NULL
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE res_users ru
        SET microsoft_calendar_account_id = mc.id
        FROM microsoft_calendar_credentials mc
        WHERE mc.calendar_sync_token = ru.microsoft_calendar_sync_token
            AND ru.microsoft_calendar_account_id IS NULL
        """,
    )


@openupgrade.migrate()
def migrate(env, version=None):
    _fill_microsoft_calendar_credentials_res_users(env)
