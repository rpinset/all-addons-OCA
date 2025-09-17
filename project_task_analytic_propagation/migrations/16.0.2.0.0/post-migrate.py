# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/LGPL-3.0)

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    analytic_lines = env["account.analytic.line"].search(
        [("task_id.analytic_account_id", "!=", False)]
    )

    analytic_lines.filtered(lambda t: not t._is_not_billed())._compute_account_id()
