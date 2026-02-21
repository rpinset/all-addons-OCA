# Copyright 2020 Akretion Mourad EL HADJ MIMOUNE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import Command
from odoo.tests import tagged

from .common import CommonBaseSubstate


@tagged("post_install", "-at_install", "mi_tag")
class TestBaseSubstate(CommonBaseSubstate):
    def setUp(self):
        super().setUp()

        self.substate_type = self.env["base.substate.type"]
        self.base_substate = self.env["base.substate"]

        self.mail_template = self.env["mail.template"].create(
            {
                "name": "Waiting for legal documents",
                "model_id": self.env["ir.model"]._get(self.sale_test_model._name).id,
                "subject": "Test Email Substate",
            }
        )
        self.sale_test_substate_type = self.substate_type.create(
            {
                "name": "Sale",
                "model": "base.substate.test.sale",
                "target_state_field": "state",
            }
        )

        self.substate_val_quotation = self.env["target.state.value"].create(
            {
                "name": "Quotation",
                "base_substate_type_id": self.sale_test_substate_type.id,
                "target_state_value": "draft",
            }
        )

        self.substate_val_sale = self.env["target.state.value"].create(
            {
                "name": "Sale order",
                "base_substate_type_id": self.sale_test_substate_type.id,
                "target_state_value": "sale",
            }
        )
        self.substate_under_negotiation = self.base_substate.create(
            {
                "name": "Under negotiation",
                "sequence": 1,
                "target_state_value_id": self.substate_val_quotation.id,
            }
        )

        self.substate_won = self.base_substate.create(
            {
                "name": "Won",
                "sequence": 1,
                "target_state_value_id": self.substate_val_quotation.id,
            }
        )

        self.substate_wait_docs = self.base_substate.create(
            {
                "name": "Waiting for legal documents",
                "sequence": 2,
                "target_state_value_id": self.substate_val_sale.id,
                "mail_template_id": self.mail_template.id,
            }
        )

        self.substate_valid_docs = self.base_substate.create(
            {
                "name": "To validate legal documents",
                "sequence": 3,
                "target_state_value_id": self.substate_val_sale.id,
            }
        )

        self.substate_in_delivering = self.base_substate.create(
            {
                "name": "In delivering",
                "sequence": 4,
                "target_state_value_id": self.substate_val_sale.id,
            }
        )

    def test_sale_order_substate(self):
        partner = self.env.ref("base.res_partner_1")
        so_test1 = self.sale_test_model.create(
            {
                "name": "Test base substate to basic sale",
                "partner_id": partner.id,
                "line_ids": [
                    Command.create({"name": "line test", "amount": 120.0, "qty": 1.5})
                ],
            }
        )
        self.assertTrue(so_test1.state == "draft")
        self.assertTrue(so_test1.substate_id == self.substate_under_negotiation)
        self.assertNotIn(
            self.mail_template.subject, so_test1.message_ids.mapped("subject")
        )
        # Test that validation of sale order change substate_id
        so_test1.button_confirm()
        self.assertTrue(so_test1.state == "sale")
        self.assertTrue(so_test1.substate_id == self.substate_wait_docs)
        # Check some message_ids are created and sent email
        self.assertIn(
            self.mail_template.subject, so_test1.message_ids.mapped("subject")
        )
        # Test that substate_id is set to false if
        # there is not substate corresponding to state
        so_test1.button_cancel()
        self.assertTrue(so_test1.state == "cancel")
        self.assertTrue(not so_test1.substate_id)
