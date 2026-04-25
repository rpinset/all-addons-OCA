# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT


class TestAgreementHelpdeskTicketSale(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))

        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.agreement1 = cls.env["agreement"].create({"name": "Agreement 1"})
        cls.agreement2 = cls.env["agreement"].create({"name": "Agreement 2"})
        cls.sale_order1 = cls.env["sale.order"].create(
            {"partner_id": cls.partner.id, "agreement_id": cls.agreement1.id}
        )
        cls.sale_order2 = cls.env["sale.order"].create(
            {"partner_id": cls.partner.id, "agreement_id": cls.agreement2.id}
        )
        cls.ticket = cls.env["helpdesk.ticket"].create(
            {"name": "Ticket", "description": "Ticket Description"}
        )

    def test_helpdesk_ticket_compute_agreement_id(self):
        self.ticket.sale_order_ids = [Command.set([self.sale_order1.id])]
        self.assertEqual(self.ticket.agreement_id, self.agreement1)

    def test_helpdesk_ticket_check_unique_agreement(self):
        with self.assertRaises(ValidationError) as error:
            self.ticket.sale_order_ids = [
                Command.set([self.sale_order1.id, self.sale_order2.id])
            ]
        self.assertEqual(
            error.exception.args[0],
            "Ticket 'Ticket' cannot have multiple different agreements.",
        )
        self.assertFalse(self.ticket.agreement_id)
