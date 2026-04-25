# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.helpdesk_mgmt_fieldservice.tests.test_helpdesk_ticket_fsm_order import (  # noqa: E501
    TestHelpdeskTicketFSMOrder,
)


class TestHelpdeskTicketFSMOrderAgreement(TestHelpdeskTicketFSMOrder):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.agreement = cls.env["agreement"].create({"name": "Test Agreement"})
        cls.ticket_1.write(
            {
                "agreement_id": cls.agreement.id,
            }
        )

    def test_helpdesk_ticket_fsm_order_propagation(self):
        fsm_orders = self._create_ticket_fsm_orders(self.ticket_1, 5)
        self.assertRecordValues(
            fsm_orders,
            [
                {
                    "agreement_id": self.agreement.id,
                }
                for _ in range(5)
            ],
        )
