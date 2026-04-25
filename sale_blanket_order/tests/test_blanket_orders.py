# Copyright (C) 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import date, timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import Form

from odoo.addons.sale.tests.common import SaleCommon


class TestSaleBlanketOrders(SaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.blanket_order_obj = cls.env["sale.blanket.order"]
        cls.blanket_order_line_obj = cls.env["sale.blanket.order.line"]
        cls.blanket_order_wiz_obj = cls.env["sale.blanket.order.wizard"]
        cls.so_obj = cls.env["sale.order"]
        cls.product_pricelist_item_obj = cls.env["product.pricelist.item"]

        cls._enable_discounts()
        cls.payment_term = cls.env.ref("account.account_payment_term_immediate")
        cls.sale_pricelist = cls._create_pricelist(
            currency_id=cls.env.ref("base.USD").id
        )

        # Taxes
        company_partner = cls.env["res.partner"].create(
            {
                "name": __name__,
                "country_id": cls.env.company.country_id.id,
            }
        )
        company2 = cls.env["res.company"].create(
            {
                "name": __name__,
                "partner_id": company_partner.id,
            },
        )
        cls.env.user.company_ids += company2
        cls.env = cls.env(
            context=dict(
                cls.env.context, allowed_company_ids=[cls.env.company.id, company2.id]
            )
        )
        tax_group1 = cls.env["account.tax.group"].create(
            {
                "name": cls.env.company.name,
                "company_id": cls.env.company.id,
            }
        )
        tax_group2 = cls.env["account.tax.group"].create(
            {
                "name": company2.name,
                "company_id": company2.id,
            }
        )
        cls.tax1, cls.tax2 = cls.env["account.tax"].create(
            [
                {
                    "name": cls.env.company.name,
                    "company_id": cls.env.company.id,
                    "amount": 10,
                    "tax_group_id": tax_group1.id,
                },
                {
                    "name": company2.name,
                    "company_id": company2.id,
                    "amount": 20,
                    "tax_group_id": tax_group2.id,
                },
            ]
        )

        # UoM
        cls.product1, cls.product2 = cls.env["product.product"].create(
            [
                {
                    "name": "Demo 1",
                    "categ_id": cls.product_category.id,
                    "standard_price": 35.0,
                    "type": "consu",
                    "uom_id": cls.env.ref("uom.product_uom_unit").id,
                    "default_code": "PROD_DEL01",
                    "taxes_id": [fields.Command.set([cls.tax1.id, cls.tax2.id])],
                },
                {
                    "name": "Demo 2",
                    "categ_id": cls.product_category.id,
                    "standard_price": 50.0,
                    "type": "consu",
                    "uom_id": cls.env.ref("uom.product_uom_unit").id,
                    "default_code": "PROD_DEL02",
                },
            ]
        )

        cls.yesterday = date.today() - timedelta(days=1)
        cls.tomorrow = date.today() + timedelta(days=1)
        cls.analytic_plan_1 = cls.env["account.analytic.plan"].create(
            [
                {
                    "name": "Plan 1",
                    "default_applicability": "unavailable",
                },
            ]
        )
        cls.analytic_account_1 = cls.env["account.analytic.account"].create(
            [
                {
                    "name": "Account 1",
                    "plan_id": cls.analytic_plan_1.id,
                    "company_id": False,
                },
            ]
        )
        cls.analytic_distribution = {
            str(cls.analytic_account_1.id): 100,
        }

    @classmethod
    def setup_independent_user(cls):
        return None

    def test_01_create_blanket_order(self):
        """We create a blanket order and check constrains to confirm BO"""
        with Form(self.blanket_order_obj) as bo:
            bo.partner_id = self.partner
            bo.validity_date = fields.Date.to_string(self.yesterday)
            bo.payment_term_id = self.payment_term
            bo.pricelist_id = self.sale_pricelist
            with bo.line_ids.new() as line_1:
                line_1.product_id = self.product1
                line_1.product_uom = self.product1.uom_id
                line_1.original_uom_qty = 20.0
                line_1.price_unit = 0.0  # will be updated later
            with bo.line_ids.new() as line_2:
                line_2.name = "My section"
                line_2.display_type = "line_section"
        blanket_order = bo.save()

        pricelist_item = self.product_pricelist_item_obj.search(
            [("pricelist_id", "=", blanket_order.pricelist_id.id)], limit=1
        )
        if not pricelist_item:
            pricelist_item = self.product_pricelist_item_obj.create(
                {
                    "pricelist_id": blanket_order.pricelist_id.id,
                    "fixed_price": 10.0,
                }
            )
        self.assertEqual(blanket_order.line_ids[0].taxes_id, self.tax1)

        pricelist_item.write({"compute_price": "percentage"})
        self.assertEqual(blanket_order.state, "draft")

        # date in the past
        with self.assertRaises(UserError):
            blanket_order.action_confirm()

        blanket_order.validity_date = fields.Date.to_string(self.tomorrow)
        blanket_order.action_confirm()
        self.assertEqual(blanket_order.state, "open")

        blanket_order.action_cancel()
        self.assertEqual(blanket_order.state, "expired")

        blanket_order.set_to_draft()
        self.assertEqual(blanket_order.state, "draft")

        blanket_order.action_confirm()

    def test_02_create_sale_orders_from_blanket_order(self):
        """We create a blanket order and create two sale orders"""
        with Form(self.blanket_order_obj) as bo:
            bo.partner_id = self.partner
            bo.validity_date = self.tomorrow
            bo.payment_term_id = self.payment_term
            bo.pricelist_id = self.sale_pricelist
            with bo.line_ids.new() as line_1:
                line_1.name = "My section"
                line_1.display_type = "line_section"
            with bo.line_ids.new() as line_2:
                line_2.product_id = self.product1
                line_2.product_uom = self.product1.uom_id
                line_2.original_uom_qty = 20.0
                line_2.price_unit = 30.0
        blanket_order = bo.save()
        blanket_order.line_ids.filtered(
            lambda r: r.product_id == self.product1
        ).analytic_distribution = self.analytic_distribution
        blanket_order.action_confirm()

        with Form(
            self.blanket_order_wiz_obj.with_context(
                active_id=blanket_order.id, active_model="sale.blanket.order"
            )
        ) as wizard:
            with wizard.line_ids.edit(0) as line:
                self.assertEqual(line.product_id, self.product1)
                line.qty = 10.0
        wizard1 = wizard.save()
        wizard1.create_sale_order()

        with Form(
            self.blanket_order_wiz_obj.with_context(
                active_id=blanket_order.id, active_model="sale.blanket.order"
            )
        ) as wizard:
            with wizard.line_ids.edit(0) as line:
                self.assertEqual(line.product_id, self.product1)
                line.qty = 10.0
        wizard2 = wizard.save()
        wizard2.create_sale_order()

        self.assertEqual(blanket_order.state, "done")

        self.assertEqual(blanket_order.sale_count, 2)

        view_action = blanket_order.action_view_sale_orders()
        domain_ids = view_action["domain"][0][2]
        self.assertEqual(len(domain_ids), 2)

        sos = self.so_obj.browse(domain_ids)
        for so in sos:
            self.assertEqual(so.origin, blanket_order.name)

        # Analytic distribution is propagated to the sale line
        self.assertEqual(
            sos[0].order_line.filtered("product_id").analytic_distribution,
            self.analytic_distribution,
        )

    def test_03_create_sale_orders_from_blanket_order_line(self):
        """We create a blanket order and create two sale orders
        from the blanket order lines"""
        with Form(self.blanket_order_obj) as bo:
            bo.partner_id = self.partner
            bo.validity_date = self.tomorrow
            bo.payment_term_id = self.payment_term
            bo.pricelist_id = self.sale_pricelist
            with bo.line_ids.new() as line_1:
                line_1.product_id = self.product1
                line_1.product_uom = self.product1.uom_id
                line_1.original_uom_qty = 20.0
                line_1.price_unit = 30.0
            with bo.line_ids.new() as line_2:
                line_2.product_id = self.product2
                line_2.product_uom = self.product2.uom_id
                line_2.original_uom_qty = 50.0
                line_2.price_unit = 60.0
        blanket_order = bo.save()
        blanket_order.action_confirm()
        bo_lines = blanket_order.line_ids
        self.assertEqual(len(bo_lines), 2)

        wizard1 = self.blanket_order_wiz_obj.with_context(
            active_ids=[bo_lines[0].id, bo_lines[1].id]
        ).create({})
        self.assertEqual(len(wizard1.line_ids), 2)
        wizard1.line_ids[0].write({"qty": 10.0})
        wizard1.line_ids[1].write({"qty": 20.0})
        wizard1.create_sale_order()

        self.assertEqual(bo_lines[0].remaining_uom_qty, 10.0)
        self.assertEqual(bo_lines[1].remaining_uom_qty, 30.0)

    def test_04_create_sale_order_add_blanket_order_line(self):
        """We create a blanket order and the separately we create
        a sale order and see if blanket order lines have been
        correctly assigned"""
        with Form(self.blanket_order_obj) as bo:
            bo.partner_id = self.partner
            bo.validity_date = self.tomorrow
            bo.payment_term_id = self.payment_term
            bo.pricelist_id = self.sale_pricelist
            with bo.line_ids.new() as line_1:
                line_1.product_id = self.product1
                line_1.product_uom = self.product1.uom_id
                line_1.original_uom_qty = 20.0
                line_1.price_unit = 30.0
            with bo.line_ids.new() as line_2:
                line_2.product_id = self.product2
                line_2.product_uom = self.product2.uom_id
                line_2.original_uom_qty = 50.0
                line_2.price_unit = 60.0
        blanket_order = bo.save()
        blanket_order.action_confirm()

        bo_lines = blanket_order.line_ids

        with Form(self.so_obj) as so:
            so.partner_id = self.partner
            so.payment_term_id = self.payment_term
            so.pricelist_id = self.sale_pricelist
            with so.order_line.new() as line_1:
                line_1.product_id = self.product1
                line_1.product_uom_qty = 10.0
                line_1.price_unit = 30.0
            with so.order_line.new() as line_2:
                line_2.product_id = self.product2
                line_2.product_uom_qty = 50.0
                line_2.price_unit = 60.0
        self.assertEqual(bo_lines[0].remaining_uom_qty, 10.0)

    def test_05_create_sale_order_blanket_order_with_different_uom(self):
        """We create a blanket order and the separately we create
        a sale order with different uom and see if blanket order
        lines have been correctly assigned"""
        with Form(self.blanket_order_obj) as bo:
            bo.partner_id = self.partner
            bo.validity_date = self.tomorrow
            bo.payment_term_id = self.payment_term
            bo.pricelist_id = self.sale_pricelist
            with bo.line_ids.new() as line_1:
                line_1.product_id = self.product1
                line_1.product_uom = self.uom_dozen
                line_1.original_uom_qty = 2.0  # 2 dozens = 24 units
                line_1.price_unit = 240.0  # price for dozen
        blanket_order = bo.save()
        blanket_order.action_confirm()

        with Form(self.so_obj) as so:
            so.partner_id = self.partner
            so.payment_term_id = self.payment_term
            so.pricelist_id = self.sale_pricelist
            with so.order_line.new() as line_1:
                line_1.product_id = self.product1
                line_1.product_uom_qty = 12.0  # 12 units
        sale_order = so.save()

        self.assertEqual(blanket_order.line_ids[0].remaining_qty, 12.0)
        self.assertEqual(sale_order.order_line[0].price_unit, 20.0)

    def test_06_create_sale_orders_from_blanket_order(self):
        """We create a blanket order and create three sale orders
        where the first two consume the first blanket order line
        """
        with Form(self.blanket_order_obj) as bo:
            bo.partner_id = self.partner
            bo.validity_date = self.tomorrow
            bo.payment_term_id = self.payment_term
            bo.pricelist_id = self.sale_pricelist
            with bo.line_ids.new() as line_1:
                line_1.product_id = self.product1
                line_1.product_uom = self.product1.uom_id
                line_1.original_uom_qty = 30.0
                line_1.price_unit = 30.0
            with bo.line_ids.new() as line_2:
                line_2.product_id = self.product2
                line_2.product_uom = self.product2.uom_id
                line_2.original_uom_qty = 20.0
                line_2.price_unit = 60.0
        blanket_order = bo.save()
        blanket_order.action_confirm()

        with Form(
            self.blanket_order_wiz_obj.with_context(
                active_id=blanket_order.id, active_model="sale.blanket.order"
            )
        ) as wizard:
            with wizard.line_ids.edit(0) as line:
                self.assertEqual(line.product_id, self.product1)
                line.qty = 10.0
            with wizard.line_ids.edit(1) as line:
                self.assertEqual(line.product_id, self.product2)
                line.qty = 10.0
        wizard1 = wizard.save()
        wizard1.create_sale_order()

        with Form(
            self.blanket_order_wiz_obj.with_context(
                active_id=blanket_order.id, active_model="sale.blanket.order"
            )
        ) as wizard:
            with wizard.line_ids.edit(0) as line:
                self.assertEqual(line.product_id, self.product1)
                line.qty = 20.0
            with wizard.line_ids.edit(1) as line:
                self.assertEqual(line.product_id, self.product2)
                line.qty = 0
        wizard2 = wizard.save()
        wizard2.create_sale_order()

        with Form(
            self.blanket_order_wiz_obj.with_context(
                active_id=blanket_order.id, active_model="sale.blanket.order"
            )
        ) as wizard:
            with wizard.line_ids.edit(0) as line:
                self.assertEqual(line.product_id, self.product2)
                line.qty = 10.0
        wizard3 = wizard.save()
        wizard3.create_sale_order()

        self.assertEqual(blanket_order.state, "done")

        self.assertEqual(blanket_order.sale_count, 3)

        view_action = blanket_order.action_view_sale_orders()
        domain_ids = view_action["domain"][0][2]
        self.assertEqual(len(domain_ids), 3)

        view_action = blanket_order.action_view_sale_blanket_order_line()
        domain_ids = view_action["domain"][0][2]
        self.assertEqual(len(domain_ids), 2)

    def test_07_unlink_different_states(self):
        with Form(self.blanket_order_obj) as bo:
            bo.partner_id = self.partner
            bo.validity_date = self.tomorrow
            bo.payment_term_id = self.payment_term
            bo.pricelist_id = self.sale_pricelist
            with bo.line_ids.new() as line_1:
                line_1.product_id = self.product1
                line_1.product_uom = self.product1.uom_id
                line_1.original_uom_qty = 30.0
                line_1.price_unit = 30.0
            with bo.line_ids.new() as line_2:
                line_2.product_id = self.product2
                line_2.product_uom = self.product2.uom_id
                line_2.original_uom_qty = 20.0
                line_2.price_unit = 60.0
        blanket_order = bo.save()

        # draft: should be allowed
        self.assertEqual(blanket_order.state, "draft")
        blanket_order.unlink()

        # Recreate since it was deleted
        with Form(self.blanket_order_obj) as bo:
            bo.partner_id = self.partner
            bo.validity_date = self.tomorrow
            bo.payment_term_id = self.payment_term
            bo.pricelist_id = self.sale_pricelist
            with bo.line_ids.new() as line_1:
                line_1.product_id = self.product1
                line_1.product_uom = self.product1.uom_id
                line_1.original_uom_qty = 30.0
                line_1.price_unit = 30.0
            with bo.line_ids.new() as line_2:
                line_2.product_id = self.product2
                line_2.product_uom = self.product2.uom_id
                line_2.original_uom_qty = 20.0
                line_2.price_unit = 60.0
        blanket_order = bo.save()

        # confirm it
        blanket_order.validity_date = fields.Date.to_string(self.tomorrow)
        blanket_order.action_confirm()
        self.assertEqual(blanket_order.state, "open")

        # open: should NOT be allowed
        with self.assertRaisesRegex(UserError, "You can not delete an open blanket"):
            blanket_order.unlink()

        # cancel: should be allowed again
        blanket_order.action_cancel()
        self.assertEqual(blanket_order.state, "expired")
        blanket_order.unlink()  # should succeed

    def test_08_change_display_type(self):
        with Form(self.blanket_order_obj) as bo:
            bo.partner_id = self.partner
            bo.validity_date = fields.Date.to_string(self.yesterday)
            bo.payment_term_id = self.payment_term
            bo.pricelist_id = self.sale_pricelist
            with bo.line_ids.new() as line_1:
                line_1.name = "My section"
                line_1.display_type = "line_section"
        blanket_order = bo.save()
        section = blanket_order.line_ids.filtered(
            lambda r: r.display_type == "line_section"
        )
        with self.assertRaisesRegex(
            UserError, "You cannot change the type of a sale order line"
        ):
            section.display_type = False
