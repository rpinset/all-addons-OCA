# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, models

from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = "account.chart.template"

    @template("by")
    def _get_by_template_data(self):
        return {
            "name": _("Belarus - Accounting"),
            "visible": True,
            "code_digits": "4",
            "property_account_receivable_id": "by_acc_6210",
            "property_account_payable_id": "by_acc_6010",
            "property_account_expense_categ_id": "by_acc_9020",
            "property_account_income_categ_id": "by_acc_9010",
        }

    @template("by", "res.company")
    def _get_by_res_company(self):
        return {
            self.env.company.id: {
                "account_fiscal_country_id": "base.by",
                "bank_account_code_prefix": "51",
                "cash_account_code_prefix": "50",
                "transfer_account_code_prefix": "57",
                "account_sale_tax_id": "sale_vat_20",
                "account_purchase_tax_id": "purchase_vat_20",
            }
        }
