# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo.tests import Form

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


class WithholdingTaxReportCommon(AccountTestInvoicingCommon):
    @classmethod
    def setup_withholding_tax(cls, company_data):
        return cls.env["withholding.tax"].create(
            {
                "name": "Test withholding tax",
                "code": "TWHT",
                "company_id": company_data["company"].id,
                "account_receivable_id": company_data["default_account_receivable"].id,
                "account_payable_id": company_data["default_account_payable"].id,
                "journal_id": company_data["default_journal_misc"].id,
                "payment_term": cls.pay_terms_a.id,
                "rate_ids": [
                    (
                        0,
                        0,
                        {
                            "tax": 20,
                            "base": 1,
                        },
                    )
                ],
            }
        )

    @classmethod
    def setup_withholding_data(cls, company_data):
        """
        Create an invoice with a withholding tax for current company.
        """
        cls.set_allowed_companies(company_data["company"])
        wh_tax = cls.setup_withholding_tax(company_data)
        invoice = cls.init_invoice("in_invoice", amounts=[100])
        invoice_form = Form(invoice)
        with invoice_form.invoice_line_ids.edit(0) as line_form:
            line_form.invoice_line_tax_wt_ids.clear()
            line_form.invoice_line_tax_wt_ids.add(wh_tax)
        invoice = invoice_form.save()
        return invoice

    @classmethod
    def set_allowed_companies(cls, company):
        """
        Set company for current user.
        Note that user.company_id would not be the current company
        but only the default company for the user.
        """
        context = {"allowed_company_ids": company.ids}
        if "allowed_company_ids" in cls.env.context:
            cls.env.context.pop("allowed_company_ids")
        cls.env.context = dict(**cls.env.context, **context)

    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.invoice = cls.setup_withholding_data(cls.company_data)
        cls.invoice.action_post()

        receivable_account_code = cls.company_data["default_account_receivable"].code
        payable_account_code = cls.company_data["default_account_payable"].code
        cls.report_template = cls.env["mis.report"].create(
            {
                "name": "Test report",
                "kpi_ids": [
                    (
                        0,
                        0,
                        {
                            "description": "Balance receivable",
                            "name": "rec_bal",
                            "expression": f"bal[{receivable_account_code}]",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "description": "Balance payable",
                            "name": "pay_bal",
                            "expression": f"bal[{payable_account_code}]",
                        },
                    ),
                ],
            }
        )
        cls.report_instance = cls.env["mis.report.instance"].create(
            {
                "name": "Test report instance",
                "report_id": cls.report_template.id,
                "comparison_mode": False,
                "date_from": cls.invoice.date - timedelta(days=1),
                "date_to": cls.invoice.date + timedelta(days=1),
            }
        )
