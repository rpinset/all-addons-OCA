# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade, openupgrade_160


@openupgrade.migrate()
def migrate(env, version):
    openupgrade_160.fill_analytic_distribution(env, "mrp_production", m2m_rel=False)
    openupgrade_160.fill_analytic_distribution(
        env,
        "mrp_workcenter",
        m2m_rel=False,
        analytic_account_column="costs_hour_account_id",
    )
