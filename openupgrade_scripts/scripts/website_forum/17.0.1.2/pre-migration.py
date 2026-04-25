# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def _forum_default_order_last_activity_date(env):
    """The criteria "write_date desc" of forums order has been removed, while
    "last_activity_date desc" has been added. We can switch them, and more
    initializing the field with the same value.
    """
    openupgrade.add_columns(
        env, [(False, "last_activity_date", "datetime", None, "forum_forum")]
    )
    openupgrade.logged_query(
        env.cr, "UPDATE forum_forum SET last_activity_date = write_date"
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE forum_forum
        SET default_order = 'last_activity_date desc'
        WHERE default_order = 'write_date desc'
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    _forum_default_order_last_activity_date(env)
    openupgrade.rename_fields(
        env, [("website", "website", "forums_count", "forum_count")]
    )
