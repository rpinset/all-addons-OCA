# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.rma.tests.test_rma import TestRma as TestRmaBase


class TestRma(TestRmaBase):
    @classmethod
    def setUpClass(cls):
        res = super().setUpClass()
        cls.rma_operation_allowed_for_reason = cls.env["rma.operation"].create(
            {"name": "Allowed"}
        )
        cls.rma_operation_forbidden_for_reason = cls.env["rma.operation"].create(
            {"name": "Forbidden"}
        )
        cls.rma_reason = cls.env["rma.reason"].create(
            {
                "name": "Reason",
                "allowed_operation_ids": [(4, cls.rma_operation_allowed_for_reason.id)],
            }
        )
        return res

    def test_allowed_operations_on_rma(self):
        rma = self._create_rma(partner=self.partner, product=self.product)
        # No reason -> all are allowed
        self.assertEqual(
            self.env["rma.operation"].search(rma.operation_domain),
            self.env["rma.operation"].search([]),
        )
        # Set a reason -> take only the operations allowed on the reason
        rma.reason_id = self.rma_reason
        self.assertEqual(
            self.env["rma.operation"].search(rma.operation_domain).ids,
            [self.rma_operation_allowed_for_reason.id],
        )

    def test_allowed_operations_on_stock_return_picking_wizard(self):
        # Create a stock picking
        picking = self._create_delivery()
        wiz = self.env["stock.return.picking"].create(
            {
                "picking_id": picking.id,
                "create_rma": True,
            }
        )
        self.assertEqual(
            self.env["rma.operation"].search(wiz.rma_operation_domain),
            self.env["rma.operation"].search([]),
        )
        wiz.rma_reason_id = self.rma_reason
        self.assertEqual(
            self.env["rma.operation"].search(wiz.rma_operation_domain).ids,
            [self.rma_operation_allowed_for_reason.id],
        )

    def test_allowed_operations_on_stock_return_picking_wizard_line(self):
        # Create a stock picking
        picking = self._create_delivery()
        wiz = self.env["stock.return.picking"].create(
            {
                "picking_id": picking.id,
                "create_rma": True,
                "product_return_moves": [
                    (0, 0, {"product_id": picking.move_ids[0].product_id.id})
                ],
            }
        )
        # Ensure that the reason is propagated on the wizard lines.
        wiz.rma_reason_id = self.rma_reason
        self.assertEqual(wiz.product_return_moves.rma_reason_id, self.rma_reason)
        # Ensure that the operation domain is propagated on the lines
        self.assertEqual(
            self.env["rma.operation"]
            .search(wiz.product_return_moves.rma_operation_domain)
            .ids,
            [self.rma_operation_allowed_for_reason.id],
        )
