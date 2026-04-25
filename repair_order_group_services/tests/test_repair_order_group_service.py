# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestRepairOrderGroupService(TransactionCase):
    """Minimal integration test for bridge module."""

    def setUp(self):
        super().setUp()

        self.RepairOrder = self.env["repair.order"]
        self.RepairService = self.env["repair.service"]
        self.RepairGroup = self.env["repair.order.group"]
        self.Partner = self.env["res.partner"]
        self.Product = self.env["product.product"]

        self.customer = self.Partner.create({"name": "Test Customer"})

        self.service_product = self.Product.create(
            {
                "name": "Repair Service",
                "type": "service",
                "list_price": 100,
            }
        )

        self.repair_product = self.Product.create(
            {
                "name": "Device",
                "type": "consu",
            }
        )

    def test_group_services_added(self):
        """Services from all repairs in the group must be added to the quotation."""

        group = self.RepairGroup.create({"name": "Group 1"})

        r1 = self.RepairOrder.create(
            {
                "name": "R1",
                "partner_id": self.customer.id,
                "product_id": self.repair_product.id,
                "group_id": group.id,
            }
        )

        r2 = self.RepairOrder.create(
            {
                "name": "R2",
                "partner_id": self.customer.id,
                "product_id": self.repair_product.id,
                "group_id": group.id,
            }
        )

        self.RepairService.create(
            {
                "repair_id": r1.id,
                "product_id": self.service_product.id,
                "product_uom_qty": 1,
            }
        )

        self.RepairService.create(
            {
                "repair_id": r2.id,
                "product_id": self.service_product.id,
                "product_uom_qty": 2,
            }
        )

        r1.action_create_sale_order()

        self.assertTrue(r1.sale_order_id)
        self.assertTrue(r2.sale_order_id)

        sale_order = r1.sale_order_id
        self.assertEqual(sale_order, r2.sale_order_id)

        lines = sale_order.order_line.filtered(
            lambda line: line.product_id == self.service_product
            and not line.display_type
        )

        self.assertEqual(len(lines), 2)

        quantities = sorted(lines.mapped("product_uom_qty"))
        self.assertEqual(quantities, [1, 2])
