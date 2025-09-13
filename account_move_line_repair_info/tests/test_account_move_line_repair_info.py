# Copyright 2022 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# flake8: noqa: B950

from odoo import fields
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestAccountMoveLineRepairInfo(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.aml_model = cls.env["account.move.line"]
        cls.am_model = cls.env["account.move"]
        cls.chart_template = cls.env["account.chart.template"].create(
            {
                "name": "Test chart",
                "currency_id": cls.env.ref("base.EUR").id,
                "code_digits": 6,
                "cash_account_code_prefix": "570",
                "bank_account_code_prefix": "572",
                "transfer_account_code_prefix": "100000",
                "use_anglo_saxon": True,
            }
        )
        cls.asset_type = cls.env.ref("account.data_account_type_current_assets")
        cls.expense_type = cls.env.ref("account.data_account_type_expenses")
        cls.liability_type = cls.env.ref(
            "account.data_account_type_current_liabilities"
        )
        cls.revenue_type = cls.env.ref("account.data_account_type_other_income")
        cls.equity_type = cls.env.ref("account.data_account_type_equity")
        cls.receivable_type = cls.env.ref("account.data_account_type_receivable")
        cls.payable_type = cls.env.ref("account.data_account_type_payable")

        cls.valuation_account = cls.env["account.account"].create(
            {
                "name": "Test stock valuation",
                "code": "tv",
                "user_type_id": cls.asset_type.id,
                "reconcile": True,
                "company_id": cls.env.ref("base.main_company").id,
            }
        )
        cls.payable_account = cls.env["account.account"].create(
            {
                "name": "Test Payable",
                "code": "tpayable",
                "user_type_id": cls.payable_type.id,
                "reconcile": True,
                "company_id": cls.env.ref("base.main_company").id,
            }
        )
        cls.receivable_account = cls.env["account.account"].create(
            {
                "name": "Test Receivable",
                "code": "treceivable",
                "user_type_id": cls.receivable_type.id,
                "reconcile": True,
                "company_id": cls.env.ref("base.main_company").id,
            }
        )

        cls.stock_input_account = cls.env["account.account"].create(
            {
                "name": "Test stock input",
                "code": "tsti",
                "user_type_id": cls.revenue_type.id,
                "reconcile": True,
                "company_id": cls.env.ref("base.main_company").id,
            }
        )
        cls.stock_output_account = cls.env["account.account"].create(
            {
                "name": "Test stock output",
                "code": "tout",
                "user_type_id": cls.liability_type.id,
                "reconcile": True,
                "company_id": cls.env.ref("base.main_company").id,
            }
        )
        cls.stock_income_account = cls.env["account.account"].create(
            {
                "name": "Test stock income",
                "code": "tincome",
                "user_type_id": cls.revenue_type.id,
                "reconcile": True,
                "company_id": cls.env.ref("base.main_company").id,
            }
        )
        cls.stock_expense_account = cls.env["account.account"].create(
            {
                "name": "Test stock outcome",
                "code": "texpense",
                "user_type_id": cls.expense_type.id,
                "reconcile": True,
                "company_id": cls.env.ref("base.main_company").id,
            }
        )
        cls.stock_journal = cls.env["account.journal"].create(
            {"name": "Stock Journal", "code": "STJTEST", "type": "general"}
        )
        cls.categ_real = cls.env["product.category"].create(
            {
                "name": "REAL",
                "property_cost_method": "fifo",
                "property_valuation": "real_time",
                "property_stock_valuation_account_id": cls.valuation_account.id,
                "property_stock_account_input_categ_id": cls.stock_input_account.id,
                "property_stock_account_output_categ_id": cls.stock_output_account.id,
                "property_account_expense_categ_id": cls.stock_expense_account.id,
                "property_account_income_categ_id": cls.stock_income_account.id,
                "property_stock_journal": cls.stock_journal.id,
            }
        )
        cls.res_partner_1 = cls.env["res.partner"].create(
            {
                "name": "Wood Corner",
                "property_account_payable_id": cls.payable_account.id,
                "property_account_receivable_id": cls.receivable_account.id,
            }
        )
        cls.res_partner_address_1 = cls.env["res.partner"].create(
            {"name": "Willie Burke", "parent_id": cls.res_partner_1.id}
        )
        cls.res_partner_12 = cls.env["res.partner"].create(
            {
                "name": "Partner 12",
                "property_account_payable_id": cls.payable_account.id,
                "property_account_receivable_id": cls.receivable_account.id,
            }
        )

        # Products
        cls.product_product_3 = cls.env["product.product"].create(
            {
                "name": "Desk Combination",
                "categ_id": cls.categ_real.id,
                "standard_price": 1.0,
                "type": "product",
            }
        )
        cls.product_product_11 = cls.env["product.product"].create(
            {
                "name": "Conference Chair",
                "categ_id": cls.categ_real.id,
                "standard_price": 1.0,
                "type": "product",
            }
        )
        cls.product_product_5 = cls.env["product.product"].create(
            {
                "name": "Product 5",
                "categ_id": cls.categ_real.id,
                "standard_price": 1.0,
                "type": "product",
            }
        )
        cls.product_product_6 = cls.env["product.product"].create(
            {
                "name": "Large Cabinet",
                "categ_id": cls.categ_real.id,
                "standard_price": 1.0,
                "type": "product",
            }
        )
        cls.product_product_12 = cls.env["product.product"].create(
            {
                "name": "Office Chair Black",
                "categ_id": cls.categ_real.id,
                "standard_price": 1.0,
                "type": "product",
            }
        )
        cls.product_product_13 = cls.env["product.product"].create(
            {
                "name": "Corner Desk Left Sit",
                "categ_id": cls.categ_real.id,
                "standard_price": 1.0,
                "type": "product",
            }
        )
        cls.product_product_2 = cls.env["product.product"].create(
            {
                "name": "Virtual Home Staging",
                "categ_id": cls.categ_real.id,
                "standard_price": 1.0,
                "type": "product",
            }
        )
        cls.product_service_order_repair = cls.env["product.product"].create(
            {
                "name": "Repair Services",
                "type": "service",
                "categ_id": cls.categ_real.id,
            }
        )

        # Location
        cls.stock_warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.env.company.id)], limit=1
        )
        cls.stock_location_14 = cls.env["stock.location"].create(
            {
                "name": "Shelf 2",
                "location_id": cls.stock_warehouse.lot_stock_id.id,
            }
        )

        # Repair Orders
        cls.repair1 = cls.env["repair.order"].create(
            {
                "address_id": cls.res_partner_address_1.id,
                "guarantee_limit": fields.Date.today(),
                "invoice_method": "none",
                "user_id": False,
                "product_id": cls.product_product_3.id,
                "product_uom": cls.env.ref("uom.product_uom_unit").id,
                "partner_invoice_id": cls.res_partner_address_1.id,
                "location_id": cls.stock_warehouse.lot_stock_id.id,
                "operations": [
                    (
                        0,
                        0,
                        {
                            "location_dest_id": cls.product_product_11.property_stock_production.id,
                            "location_id": cls.stock_warehouse.lot_stock_id.id,
                            "name": cls.product_product_11.get_product_multiline_description_sale(),
                            "product_id": cls.product_product_11.id,
                            "product_uom": cls.env.ref("uom.product_uom_unit").id,
                            "product_uom_qty": 1.0,
                            "price_unit": 50.0,
                            "state": "draft",
                            "type": "add",
                            "company_id": cls.env.company.id,
                        },
                    )
                ],
                "fees_lines": [
                    (
                        0,
                        0,
                        {
                            "name": cls.product_service_order_repair.get_product_multiline_description_sale(),
                            "product_id": cls.product_service_order_repair.id,
                            "product_uom_qty": 1.0,
                            "product_uom": cls.env.ref("uom.product_uom_unit").id,
                            "price_unit": 50.0,
                            "company_id": cls.env.company.id,
                        },
                    )
                ],
                "partner_id": cls.res_partner_12.id,
            }
        )

        cls.repair0 = cls.env["repair.order"].create(
            {
                "product_id": cls.product_product_5.id,
                "product_uom": cls.env.ref("uom.product_uom_unit").id,
                "address_id": cls.res_partner_address_1.id,
                "guarantee_limit": fields.Date.today(),
                "invoice_method": "after_repair",
                "user_id": False,
                "partner_invoice_id": cls.res_partner_address_1.id,
                "location_id": cls.stock_warehouse.lot_stock_id.id,
                "operations": [
                    (
                        0,
                        0,
                        {
                            "location_dest_id": cls.product_product_12.property_stock_production.id,
                            "location_id": cls.stock_warehouse.lot_stock_id.id,
                            "name": cls.product_product_12.get_product_multiline_description_sale(),
                            "price_unit": 50.0,
                            "product_id": cls.product_product_12.id,
                            "product_uom": cls.env.ref("uom.product_uom_unit").id,
                            "product_uom_qty": 1.0,
                            "state": "draft",
                            "type": "add",
                            "company_id": cls.env.company.id,
                        },
                    )
                ],
                "fees_lines": [
                    (
                        0,
                        0,
                        {
                            "name": cls.product_service_order_repair.get_product_multiline_description_sale(),
                            "product_id": cls.product_service_order_repair.id,
                            "product_uom_qty": 1.0,
                            "product_uom": cls.env.ref("uom.product_uom_unit").id,
                            "price_unit": 50.0,
                            "company_id": cls.env.company.id,
                        },
                    )
                ],
                "partner_id": cls.res_partner_12.id,
            }
        )

        cls.repair2 = cls.env["repair.order"].create(
            {
                "product_id": cls.product_product_6.id,
                "product_uom": cls.env.ref("uom.product_uom_unit").id,
                "address_id": cls.res_partner_address_1.id,
                "guarantee_limit": fields.Date.today(),
                "invoice_method": "b4repair",
                "user_id": False,
                "partner_invoice_id": cls.res_partner_address_1.id,
                "location_id": cls.stock_location_14.id,
                "operations": [
                    (
                        0,
                        0,
                        {
                            "location_dest_id": cls.product_product_13.property_stock_production.id,
                            "location_id": cls.stock_warehouse.lot_stock_id.id,
                            "name": cls.product_product_13.get_product_multiline_description_sale(),
                            "price_unit": 50.0,
                            "product_id": cls.product_product_13.id,
                            "product_uom": cls.env.ref("uom.product_uom_unit").id,
                            "product_uom_qty": 1.0,
                            "state": "draft",
                            "type": "add",
                            "company_id": cls.env.company.id,
                        },
                    )
                ],
                "fees_lines": [
                    (
                        0,
                        0,
                        {
                            "name": cls.product_service_order_repair.get_product_multiline_description_sale(),
                            "product_id": cls.product_service_order_repair.id,
                            "product_uom_qty": 1.0,
                            "product_uom": cls.env.ref("uom.product_uom_unit").id,
                            "price_unit": 50.0,
                            "company_id": cls.env.company.id,
                        },
                    )
                ],
                "partner_id": cls.res_partner_12.id,
            }
        )

        cls.env.user.groups_id |= cls.env.ref("stock.group_stock_user")

    def test_move_line_repair_info(self):
        self.product_product_3.write({"categ_id": self.categ_real.id})
        self.product_product_11.write({"categ_id": self.categ_real.id})
        self.product_product_5.write({"categ_id": self.categ_real.id})
        self.product_product_6.write({"categ_id": self.categ_real.id})
        self.product_product_12.write({"categ_id": self.categ_real.id})
        self.product_product_13.write({"categ_id": self.categ_real.id})
        self.product_product_2.write({"categ_id": self.categ_real.id})
        repairs = self.repair0 + self.repair1 + self.repair2
        for repair in repairs:
            repair.action_repair_confirm()
            if repair.state != "2binvoiced":
                repair.action_repair_start()
                repair.action_repair_end()
        for operation in repairs.filtered(
            lambda x: x.state == "done" and x.move_id
        ).mapped("operations"):
            aml = self.aml_model.search(
                [("move_id.stock_move_id", "=", operation.move_id.id)]
            )
            if aml:
                self.assertEqual(
                    aml.mapped("repair_order_id").ids, operation.repair_id.ids
                )
        make_invoice = self.env["repair.order.make_invoice"].create({"group": True})
        context = {
            "active_model": "repair.order",
            "active_ids": repairs.ids,
        }
        res = make_invoice.with_context(**context).make_invoices()
        invoices = res.get("domain", []) and self.am_model.browse(
            res.get("domain", [])[0][2]
        )
        for invoice in invoices:
            if invoice.state == "draft":
                invoice.action_post()
        for fee in repairs.mapped("fees_lines"):
            invoice_lines = fee.repair_id.invoice_id.invoice_line_ids.filtered(
                lambda x: fee.id in x.repair_fee_ids.ids
            )
            if invoice_lines:
                self.assertEqual(fee.repair_id.id, invoice_lines.repair_order_id.id)
        for operation in repairs.mapped("operations"):
            invoice_lines = operation.repair_id.invoice_id.invoice_line_ids.filtered(
                lambda x: operation.id in x.repair_line_ids.ids
            )
            if invoice_lines:
                self.assertEqual(
                    operation.repair_id.id, invoice_lines.repair_order_id.id
                )
