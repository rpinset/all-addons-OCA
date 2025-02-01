# Copyright 2025 Patryk Pyczko (APSL-Nagarro)<ppyczko@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestWebsiteSaleStockOrderCancel(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sale_order = cls.env.ref("website_sale.website_sale_order_2")
        cls.sale_order.write({"commitment_date": datetime.now() + timedelta(days=4)})

    def _set_cancel_restrict_days(self, days):
        """Helper method to set the cancel restriction period."""
        self.env["ir.config_parameter"].sudo().set_param(
            "sale.cancel_restrict_days", str(days)
        )

    def test_can_cancel_no_done_pickings(self):
        self._set_cancel_restrict_days(0)
        self.sale_order._compute_can_cancel()
        self.assertTrue(
            self.sale_order.can_cancel,
            "Order should be cancellable without 'done' pickings.",
        )

    def test_cannot_cancel_with_done_picking(self):
        self._set_cancel_restrict_days(0)
        self.sale_order.picking_ids.action_set_quantities_to_reservation()
        self.sale_order.picking_ids.button_validate()
        self.sale_order._compute_can_cancel()
        self.assertFalse(
            self.sale_order.can_cancel,
            "Order should not be cancellable with 'done' pickings.",
        )
