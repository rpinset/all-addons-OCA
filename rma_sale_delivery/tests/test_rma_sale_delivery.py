# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import Form

from odoo.addons.rma_delivery.tests.test_rma_delivery import TestRmaDeliveryBase


class TestRmaSaleDelivery(TestRmaDeliveryBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.res_partner.create({"name": "Test partner"})
        cls.product = cls.product_product.create(
            {"name": "Product test", "type": "consu", "is_storable": True}
        )
        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.env.company.id)], limit=1
        )
        cls.env["stock.quant"]._update_available_quantity(
            cls.product, cls.warehouse.lot_stock_id, 1
        )
        cls.operation = cls.env.ref("rma.rma_operation_replace")
        order_form = Form(cls.env["sale.order"])
        order_form.partner_id = cls.partner
        with order_form.order_line.new() as line_form:
            line_form.product_id = cls.product
        cls.sale_order = order_form.save()

    @classmethod
    def _rma_sale_wizard(cls, order):
        wizard_id = order.action_create_rma()["res_id"]
        wizard = cls.env["sale.order.rma.wizard"].browse(wizard_id)
        wizard.operation_id = cls.operation
        return wizard

    def test_sale_oder_rma_wizard_01(self):
        self.sale_order.action_confirm()
        order_picking = self.sale_order.picking_ids
        order_picking.button_validate()
        wizard = self._rma_sale_wizard(self.sale_order)
        rma = self.env["rma"].browse(wizard.create_and_open_rma()["res_id"])
        self.assertFalse(rma.reception_carrier_id)

    def test_sale_oder_rma_wizard_02(self):
        self.sale_order.action_confirm()
        order_picking = self.sale_order.picking_ids
        order_picking.button_validate()
        wizard = self._rma_sale_wizard(self.sale_order)
        wizard.reception_carrier_id = self.carrier
        rma = self.env["rma"].browse(wizard.create_and_open_rma()["res_id"])
        self.assertEqual(rma.reception_carrier_id, self.carrier)
