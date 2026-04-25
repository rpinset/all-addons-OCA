# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade, openupgrade_180


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env, "analytic", "18.0.1.2/noupdate_changes.xml")
    openupgrade_180.convert_company_dependent(
        env, "account.analytic.plan", "default_applicability"
    )
