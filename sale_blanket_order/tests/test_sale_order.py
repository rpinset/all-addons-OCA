# Copyright (C) 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import date, timedelta

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import Form, tagged

from odoo.addons.sale.tests.common import TestSaleCommon


@tagged("-at_install", "post_install")
class TestSaleOrder(TestSaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.blanket_order_obj = cls.env["sale.blanket.order"]
        cls.blanket_order_line_obj = cls.env["sale.blanket.order.line"]
        cls.sale_order_obj = cls.env["sale.order"]
        cls.sale_order_line_obj = cls.env["sale.order.line"]

        cls.payment_term = cls.env.ref("account.account_payment_term_immediate")
        cls.sale_pricelist = cls._create_pricelist(
            currency_id=cls.env.ref("base.USD").id
        )

        cls.product = cls.env["product.product"].create(
            {
                "name": "Demo",
                "categ_id": cls.product_category.id,
                "standard_price": 40.0,
                "type": "consu",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "default_code": "PROD_DEL01",
                "description_sale": "Demo product sale description",
            }
        )
        cls.product_2 = cls.env["product.product"].create(
            {
                "name": "Demo 2",
                "categ_id": cls.product_category.id,
                "standard_price": 35.0,
                "type": "consu",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "default_code": "PROD_DEL02",
            }
        )
        cls.product_3 = cls.env["product.product"].create(
            {
                "name": "Demo 3",
                "categ_id": cls.product_category.id,
                "standard_price": 50.0,
                "type": "consu",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "default_code": "PROD_DEL03",
            }
        )
        cls.validity = date.today() + timedelta(days=365)
        cls.date_schedule_1 = date.today() + timedelta(days=10)
        cls.date_schedule_2 = date.today() + timedelta(days=20)

    def create_blanket_order_01(self):
        with Form(self.blanket_order_obj) as bo:
            bo.partner_id = self.partner
            bo.validity_date = self.validity
            bo.payment_term_id = self.payment_term
            bo.pricelist_id = self.sale_pricelist
            with bo.line_ids.new() as line_1:
                line_1.product_id = self.product
                line_1.product_uom = self.product.uom_id
                line_1.date_schedule = self.date_schedule_1
                line_1.original_uom_qty = 20.0
                line_1.price_unit = 30.0
            with bo.line_ids.new() as line_2:
                line_2.product_id = self.product
                line_2.product_uom = self.product.uom_id
                line_2.date_schedule = self.date_schedule_2
                line_2.original_uom_qty = 20.0
                line_2.price_unit = 30.0
        blanket_order = bo.save()
        return blanket_order

    def create_blanket_order_02(self):
        with Form(self.blanket_order_obj) as bo:
            bo.partner_id = self.partner
            bo.validity_date = self.validity
            bo.payment_term_id = self.payment_term
            bo.pricelist_id = self.sale_pricelist
            with bo.line_ids.new() as line_1:
                line_1.product_id = self.product
                line_1.product_uom = self.product.uom_id
                line_1.original_uom_qty = 20.0
                line_1.price_unit = 30.0
            with bo.line_ids.new() as line_2:
                line_2.product_id = self.product_2
                line_2.product_uom = self.product.uom_id
                line_2.original_uom_qty = 10.0
                line_2.price_unit = 15.0
        blanket_order = bo.save()
        return blanket_order

    def test_01_create_sale_order(self):
        blanket_order = self.create_blanket_order_01()
        blanket_order.action_confirm()
        bo_lines = self.blanket_order_line_obj.search(
            [("order_id", "=", blanket_order.id)]
        )
        self.assertEqual(len(bo_lines), 2)

        with Form(self.sale_order_obj) as so:
            so.partner_id = self.partner
            with so.order_line.new() as line_1:
                line_1.product_id = self.product
                line_1.product_uom_qty = 5.0
                line_1.price_unit = 10.0
        so = so.save()
        so_line = so.order_line[0]
        self.assertEqual(so_line._get_eligible_bo_lines(), bo_lines)
        bo_line_assigned = self.blanket_order_line_obj.search(
            [("date_schedule", "=", fields.Date.to_string(self.date_schedule_1))]
        )
        self.assertEqual(so_line.blanket_order_line, bo_line_assigned)
        so.action_confirm()

    def test_02_create_sale_order(self):
        blanket_order = self.create_blanket_order_02()
        blanket_order.action_confirm()
        bo_lines = self.blanket_order_line_obj.search(
            [("order_id", "=", blanket_order.id)]
        )
        self.assertEqual(len(bo_lines), 2)

        with Form(self.sale_order_obj) as so:
            so.partner_id = self.partner
            with so.order_line.new() as line_1:
                line_1.product_id = self.product_2
                line_1.product_uom_qty = 5.0
                line_1.price_unit = 10.0
        so = so.save()
        so_line = so.order_line[0]
        self.assertEqual(
            so_line._get_eligible_bo_lines(),
            bo_lines.filtered(lambda bo_line: bo_line.product_id == self.product_2),
        )
        bo_line_assigned = self.blanket_order_line_obj.search(
            [
                ("order_id", "=", blanket_order.id),
                ("product_id", "=", self.product_2.id),
                ("date_schedule", "=", False),
            ]
        )
        self.assertEqual(so_line.blanket_order_line, bo_line_assigned)
        self.assertEqual(so_line.tax_ids, bo_line_assigned.taxes_id)
        self.assertEqual(bo_line_assigned.remaining_qty, 5.0)

    def test_03_create_sale_order(self):
        blanket_order = self.create_blanket_order_02()
        blanket_order.action_confirm()

        with Form(self.sale_order_obj) as so:
            so.partner_id = self.partner
            with so.order_line.new() as line_1:
                line_1.product_id = self.product_2
                line_1.product_uom_qty = 10.0
                line_1.price_unit = 10.0
        so1 = so.save()
        self.assertEqual(
            so1.order_line.blanket_order_line,
            blanket_order.line_ids.filtered(lambda r: r.product_id == self.product_2),
        )

        with Form(self.sale_order_obj) as so:
            so.partner_id = self.partner
            with so.order_line.new() as line_1:
                line_1.product_id = self.product_2
                line_1.product_uom_qty = 10.0
                line_1.price_unit = 10.0
        so2 = so.save()
        self.assertFalse(so2.order_line.blanket_order_line)

    def test_04_create_sale_order(self):
        blanket_order = self.create_blanket_order_02()
        blanket_order.action_confirm()

        with Form(self.sale_order_obj) as so:
            so.partner_id = self.partner
            with so.order_line.new() as line_1:
                line_1.product_id = self.product_2
                line_1.product_uom_qty = 10.0
                line_1.price_unit = 10.0
        so1 = so.save()
        self.assertEqual(
            so1.order_line.blanket_order_line,
            blanket_order.line_ids.filtered(lambda r: r.product_id == self.product_2),
        )

        partner = self._create_partner()
        so1.partner_id = partner
        self.assertFalse(so1.order_line.blanket_order_line)

    def test_05_create_sale_order(self):
        blanket_order = self.create_blanket_order_02()
        blanket_order.action_confirm()

        with Form(self.sale_order_obj) as so:
            so.partner_id = self.partner
            with so.order_line.new() as line_1:
                line_1.product_id = self.product_2
                line_1.product_uom_qty = 10.0
                line_1.price_unit = 10.0
        so1 = so.save()
        self.assertEqual(
            so1.order_line.blanket_order_line,
            blanket_order.line_ids.filtered(lambda r: r.product_id == self.product_2),
        )

        blanket_order.line_ids.filtered(
            lambda r: r.product_id == self.product_2
        ).original_uom_qty = 0

        with self.assertRaisesRegex(
            ValidationError, "order that has no remaining quantity"
        ):
            so1.action_confirm()

    def test_06_create_sale_order(self):
        blanket_order = self.create_blanket_order_02()
        blanket_order.action_confirm()

        with Form(self.sale_order_obj) as so:
            so.partner_id = self.partner
            with so.order_line.new() as line_1:
                line_1.product_id = self.product_2
                line_1.product_uom_qty = 10.0
                line_1.price_unit = 10.0
        so1 = so.save()
        self.assertEqual(
            so1.order_line.blanket_order_line,
            blanket_order.line_ids.filtered(lambda r: r.product_id == self.product_2),
        )

        blanket_order.partner_id = self._create_partner()

        with self.assertRaisesRegex(
            ValidationError,
            "The customer must be equal to the blanket order lines customer",
        ):
            so1.action_confirm()

    def test_07_create_sale_order(self):
        blanket_order = self.create_blanket_order_02()
        blanket_order.action_confirm()

        with Form(self.sale_order_obj) as so:
            so.partner_id = self.partner
            with so.order_line.new() as line_1:
                line_1.product_id = self.product_2
                line_1.product_uom_qty = 10.0
                line_1.price_unit = 10.0
        so1 = so.save()
        self.assertEqual(
            so1.order_line.blanket_order_line,
            blanket_order.line_ids.filtered(lambda r: r.product_id == self.product_2),
        )

        blanket_order.pricelist_id = self._create_pricelist(
            currency_id=self.env.ref("base.EUR").id
        )

        with self.assertRaisesRegex(
            ValidationError,
            "The currency of the blanket order must match with that of the sale order",
        ):
            so1.action_confirm()

    def test_08_create_sale_order(self):
        blanket_order = self.create_blanket_order_02()
        blanket_order.action_confirm()

        with Form(self.sale_order_obj) as so:
            so.partner_id = self.partner
            with so.order_line.new() as line_1:
                line_1.product_id = self.product_2
                line_1.product_uom_qty = 10.0
                line_1.price_unit = 10.0
        so1 = so.save()
        self.assertEqual(
            so1.order_line.blanket_order_line,
            blanket_order.line_ids.filtered(lambda r: r.product_id == self.product_2),
        )

        blanket_order.line_ids.filtered(
            lambda r: r.product_id == self.product_2
        ).product_id = self.product_3

        with self.assertRaisesRegex(
            ValidationError,
            "The product in the blanket order and in the sales order must match",
        ):
            so1.action_confirm()

    def test_09_disable_adding_lines(self):
        blanket_order = self.create_blanket_order_02()
        blanket_order.action_confirm()

        with Form(self.sale_order_obj) as so:
            so.partner_id = self.partner
            with so.order_line.new() as line_1:
                line_1.product_id = self.product_2
                line_1.product_uom_qty = 10.0
                line_1.price_unit = 10.0
        so1 = so.save()
        self.assertFalse(so1.disable_adding_lines)
        self.env.user.group_ids += self.quick_ref(
            "sale_blanket_order.blanket_orders_disable_adding_lines"
        )
        self.assertTrue(so1.disable_adding_lines)

    def test_10_cancel_backorder(self):
        blanket_order = self.create_blanket_order_02()
        blanket_order.action_confirm()

        with Form(self.sale_order_obj) as so:
            so.partner_id = self.partner
            with so.order_line.new() as line_1:
                line_1.product_id = self.product_2
                line_1.product_uom_qty = 10.0
                line_1.price_unit = 10.0

        with self.assertRaisesRegex(
            UserError,
            "You can not delete a blanket order with opened sale orders",
        ):
            blanket_order.action_cancel()

    def test_11_blanket_order_quantities(self):
        blanket_order = self.create_blanket_order_02()
        blanket_order.action_confirm()

        with Form(self.sale_order_obj) as so:
            so.partner_id = self.partner
            with so.order_line.new() as line_1:
                line_1.product_id = self.product
                line_1.product_uom_qty = 5.0
                line_1.price_unit = 10.0
            with so.order_line.new() as line_2:
                line_2.product_id = self.product_2
                line_2.product_uom_qty = 4.0
                line_2.price_unit = 10.0
        so1 = so.save()

        self.assertEqual(blanket_order.original_uom_qty, 30.0)
        self.assertEqual(blanket_order.ordered_uom_qty, 9.0)
        self.assertEqual(blanket_order.invoiced_uom_qty, 0.0)
        self.assertEqual(blanket_order.delivered_uom_qty, 0.0)
        self.assertEqual(blanket_order.remaining_uom_qty, 21.0)
        self.assertEqual(
            self.blanket_order_obj.search([("original_uom_qty", ">", 0)]), blanket_order
        )
        self.assertEqual(
            self.blanket_order_obj.search([("ordered_uom_qty", ">", 0)]), blanket_order
        )
        self.assertFalse(self.blanket_order_obj.search([("invoiced_uom_qty", ">", 0)]))
        self.assertEqual(
            self.blanket_order_obj.search([("invoiced_uom_qty", "=", 0)]), blanket_order
        )
        self.assertFalse(self.blanket_order_obj.search([("delivered_uom_qty", ">", 0)]))
        self.assertEqual(
            self.blanket_order_obj.search([("delivered_uom_qty", "=", 0)]),
            blanket_order,
        )
        self.assertEqual(
            self.blanket_order_obj.search([("remaining_uom_qty", ">", 0)]),
            blanket_order,
        )

        so1.action_confirm()
        so1._create_invoices()

        blanket_order.invalidate_recordset()
        self.assertEqual(blanket_order.original_uom_qty, 30.0)
        self.assertEqual(blanket_order.ordered_uom_qty, 9.0)
        self.assertEqual(blanket_order.invoiced_uom_qty, 9.0)
        self.assertEqual(blanket_order.delivered_uom_qty, 0.0)
        self.assertEqual(blanket_order.remaining_uom_qty, 21.0)
        self.assertEqual(
            self.blanket_order_obj.search([("original_uom_qty", ">", 0)]), blanket_order
        )
        self.assertEqual(
            self.blanket_order_obj.search([("ordered_uom_qty", ">", 0)]), blanket_order
        )
        self.assertEqual(
            self.blanket_order_obj.search([("invoiced_uom_qty", ">", 0)]), blanket_order
        )
        self.assertFalse(self.blanket_order_obj.search([("delivered_uom_qty", ">", 0)]))
        self.assertEqual(
            self.blanket_order_obj.search([("remaining_uom_qty", ">", 0)]),
            blanket_order,
        )

        so1.order_line.filtered(
            lambda r: r.product_id == self.product
        ).qty_delivered = 3.0
        so1.order_line.filtered(
            lambda r: r.product_id == self.product_2
        ).qty_delivered = 2.0

        blanket_order.invalidate_recordset()
        self.assertEqual(blanket_order.original_uom_qty, 30.0)
        self.assertEqual(blanket_order.ordered_uom_qty, 9.0)
        self.assertEqual(blanket_order.invoiced_uom_qty, 9.0)
        self.assertEqual(blanket_order.delivered_uom_qty, 5.0)
        self.assertEqual(blanket_order.remaining_uom_qty, 21.0)
        self.assertEqual(
            self.blanket_order_obj.search([("original_uom_qty", ">", 0)]), blanket_order
        )
        self.assertEqual(
            self.blanket_order_obj.search([("ordered_uom_qty", ">", 0)]), blanket_order
        )
        self.assertEqual(
            self.blanket_order_obj.search([("invoiced_uom_qty", ">", 0)]), blanket_order
        )
        self.assertEqual(
            self.blanket_order_obj.search([("delivered_uom_qty", ">", 0)]),
            blanket_order,
        )
        self.assertEqual(
            self.blanket_order_obj.search([("remaining_uom_qty", ">", 0)]),
            blanket_order,
        )
