#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    prepayment_account_type = env.ref("account.data_account_type_prepayments")
    prepayment_account_type.financial_statements_report_section = "assets"
