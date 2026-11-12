# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

try:
    from odoo.upgrade.util.pg import explode_execute

    def _execute(cr, query):
        return explode_execute(
            cr,
            query,
            table="account_move",
            alias="am",
        )
except ImportError:

    def _execute(cr, query):
        cr.execute(query)
        return cr.rowcount


def optimize__init_fields_on_account_move(env):
    env.cr.execute(
        """
        ALTER TABLE account_move ADD COLUMN IF NOT EXISTS payment_method_code VARCHAR;
    """,
    )

    _execute(
        env.cr,
        """
        UPDATE account_move AS am
        SET payment_method_code = apm.code
        FROM
            account_payment_method_line AS apml
            LEFT JOIN account_payment_method AS apm ON apml.payment_method_id = apm.id
        WHERE
            am.preferred_payment_method_line_id = apml.id
            AND am.preferred_payment_method_line_id IS NOT NULL
    """,
    )


def pre_init_hook(env):
    optimize__init_fields_on_account_move(env)
