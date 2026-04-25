# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade, openupgrade_180


def convert_company_dependent(env):
    openupgrade_180.convert_company_dependent(
        env, "product.category", "property_account_creditor_price_difference_categ"
    )
    openupgrade_180.convert_company_dependent(
        env, "product.template", "property_account_creditor_price_difference"
    )


@openupgrade.migrate()
def migrate(env, version):
    convert_company_dependent(env)
