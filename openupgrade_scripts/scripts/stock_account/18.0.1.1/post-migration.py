# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade, openupgrade_180


def convert_company_dependent(env):
    openupgrade_180.convert_company_dependent(
        env, "product.category", "property_cost_method"
    )
    openupgrade_180.convert_company_dependent(
        env, "product.category", "property_stock_account_input_categ_id"
    )
    openupgrade_180.convert_company_dependent(
        env, "product.category", "property_stock_account_output_categ_id"
    )
    openupgrade_180.convert_company_dependent(
        env, "product.category", "property_stock_journal"
    )
    openupgrade_180.convert_company_dependent(
        env, "product.category", "property_stock_valuation_account_id"
    )
    openupgrade_180.convert_company_dependent(
        env, "product.category", "property_valuation"
    )


@openupgrade.migrate()
def migrate(env, version):
    convert_company_dependent(env)
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            "stock_account.default_category_cost_method",
            "stock_account.default_category_valuation",
        ],
    )
