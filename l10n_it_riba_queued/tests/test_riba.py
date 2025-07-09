# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import datetime

from odoo.fields import first
from odoo.tests import Form
from odoo.tools import safe_eval

from odoo.addons.l10n_it_ricevute_bancarie.tests import riba_common


class TestRiBa(riba_common.TestRibaCommon):
    def test_async_payment(self):
        """When multiple lines have to be paid asynchronously,
        a job is created.
        """
        # Arrange
        company = self.env.company
        payment_date = datetime.date(2020, month=1, day=1)
        payment_term = self.payment_term2
        riba_configuration = self.riba_config_sbf_immediate
        product = self.product1
        partner = self.partner
        company.due_cost_service_id = self.service_due_cost

        invoice_form = Form(
            self.env["account.move"].with_context(
                default_move_type="out_invoice",
                default_name="Test invoice",
            )
        )
        invoice_form.partner_id = partner
        invoice_form.invoice_payment_term_id = payment_term
        invoice_form.riba_partner_bank_id = first(partner.bank_ids)
        with invoice_form.invoice_line_ids.new() as line:
            line.product_id = product
        invoice = invoice_form.save()
        invoice.action_post()

        to_issue_action = self.env.ref(
            "l10n_it_ricevute_bancarie.action_riba_da_emettere"
        )
        to_issue_records = self.env[to_issue_action.res_model].search(
            safe_eval.safe_eval(to_issue_action.domain)
        )
        invoice_to_issue_records = to_issue_records & invoice.line_ids
        self.assertTrue(invoice_to_issue_records)

        issue_wizard_model = self.env["riba.issue"].with_context(
            active_model=invoice_to_issue_records._name,
            active_ids=invoice_to_issue_records.ids,
        )
        issue_wizard_form = Form(issue_wizard_model)
        issue_wizard_form.configuration_id = riba_configuration
        issue_wizard = issue_wizard_form.save()
        issue_result = issue_wizard.create_list()
        slip = self.env[issue_result["res_model"]].browse(issue_result["res_id"])

        slip.confirm()
        self.assertEqual(slip.state, "accepted")

        credit_wizard_action = self.env.ref(
            "l10n_it_ricevute_bancarie.riba_accreditation_action"
        )
        credit_wizard = (
            self.env[credit_wizard_action["res_model"]]
            .with_context(active_id=slip.id)
            .create(
                {
                    "bank_amount": invoice.amount_total,
                }
            )
        )
        credit_wizard.create_move()
        self.assertEqual(slip.state, "accredited")

        # Act
        payment_wizard_action = slip.settle_all_line()
        payment_wizard_form = Form(
            self.env[payment_wizard_action["res_model"]].with_context(
                **payment_wizard_action["context"]
            )
        )
        payment_wizard_form.payment_date = payment_date
        payment_wizard = payment_wizard_form.save()
        delayed = payment_wizard.pay_async()

        # Assert
        job = self.env["queue.job"].search([("uuid", "=", delayed.uuid)])
        self.assertTrue(job)
