# Common methods for migrations
from openupgradelib import openupgrade


def _remove_module(env, module_name):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_module_module
        SET
            state = 'to remove'
        WHERE
            name = %(module_name)s
            AND state NOT IN ('to remove', 'uninstalled')
        """,
        dict(
            module_name=module_name,
        ),
    )
