# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.m2o_to_x2m(
        env.cr,
        env["account.analytic.account"],
        "account_analytic_account",
        "department_ids",
        "department_id",
    )
    openupgrade.m2o_to_x2m(
        env.cr,
        env["account.analytic.plan"],
        "account_analytic_plan",
        "department_ids",
        "department_id",
    )
