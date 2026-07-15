# Part of the Paraguayan localization. See LICENSE file for full copyright
# and licensing details.
from odoo import _, models

from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = "account.chart.template"

    @template("py")
    def _get_py_template_data(self):
        return {
            "name": _("Plan de Cuentas - Paraguay (Resolución General N° 49/14)"),
            "code_digits": "6",
            "property_account_receivable_id": "account_py_301",
            "property_account_payable_id": "account_py_2001",
            "property_account_expense_categ_id": "account_py_50101_expense",
            "property_account_income_categ_id": "account_py_40101_income",
        }

    @template("py", "res.company")
    def _get_py_res_company(self):
        return {
            self.env.company.id: {
                "account_fiscal_country_id": "base.py",
                "bank_account_code_prefix": "1.01.01.04",
                "cash_account_code_prefix": "1.01.01.02",
                "transfer_account_code_prefix": "1.01.01.03",
                "account_default_pos_receivable_account_id": "account_py_301",
                "income_currency_exchange_account_id": "account_py_805_income",
                "expense_currency_exchange_account_id": "account_py_1304_expense",
                "default_cash_difference_income_account_id": "account_py_802_income",
                "default_cash_difference_expense_account_id": (
                    "account_py_1116_expense"
                ),
                "account_journal_suspense_account_id": "account_py_103",
                "account_journal_payment_debit_account_id": "account_py_301",
                "account_journal_payment_credit_account_id": "account_py_2001",
                "account_sale_tax_id": "py_tax_vat_10_ventas",
                "account_purchase_tax_id": "py_tax_vat_10_compras",
            },
        }
