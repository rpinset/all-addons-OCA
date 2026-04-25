# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


def _setup_property_downpayment_account(env):
    # "Copy" of sale _setup_property_downpayment_account
    for company in env.companies:
        if not company.chart_template or env["product.category"].with_company(
            company
        ).search_count(
            [("property_account_downpayment_categ_id", "!=", False)], limit=1
        ):
            continue
        # begin patch: avoid having errors for not loading l10n modules
        if not company.country_id.code:
            continue
        module_name = "l10n_" + company.country_id.code.lower()
        l10n_module = env["ir.module.module"].search(
            [
                ("name", "=", module_name),
                ("state", "=", "installed"),
            ]
        )
        if not l10n_module:
            continue
        # end patch
        template_data = (
            env["account.chart.template"]
            ._get_chart_template_data(company.chart_template)
            .get("template_data")
        )
        if template_data and template_data.get("property_account_downpayment_categ_id"):
            property_downpayment_account = env.ref(
                f'account.{company.id}_{template_data["property_account_downpayment_categ_id"]}',
                raise_if_not_found=False,
            )
            if property_downpayment_account:
                env["ir.default"].set(
                    "product.category",
                    "property_account_downpayment_categ_id",
                    property_downpayment_account.id,
                    company_id=company.id,
                )


@openupgrade.migrate()
def migrate(env, version):
    _setup_property_downpayment_account(env)
