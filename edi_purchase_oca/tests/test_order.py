# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase

from .common import OrderMixin, PurchaseEDIBackendTestMixin


class TestOrder(TransactionCase, PurchaseEDIBackendTestMixin, OrderMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, edi_framework_action=True))
        cls._setup_records()
        cls.exchange_type_in.exchange_filename_pattern = "{record.id}-{type.code}-{dt}"
        cls.exc_record_in = cls.backend.create_record(
            cls.exchange_type_in.code, {"edi_exchange_state": "input_received"}
        )
        cls._setup_order_records()
        order_vals = {
            "order_line": [
                {
                    "product_id": cls.product.id,
                    "product_qty": 10,
                    "price_unit": 100.0,
                }
            ],
        }
        cls.order = cls._create_purchase_order(
            origin_exchange_record_id=cls.exc_record_in.id,
            **order_vals,
        )

    def test_line_origin(self):
        order = self.order
        self.assertEqual(order.origin_exchange_record_id, self.exc_record_in)
        lines = order.order_line
        self.env["purchase.order.line"].create(
            [
                {
                    "order_id": order.id,
                    "product_id": self.product.id,
                    "product_qty": 20,
                    "price_unit": 100.0,
                    "edi_id": 2000,
                },
                {
                    "order_id": order.id,
                    "product_id": self.product.id,
                    "product_qty": 30,
                    "price_unit": 100.0,
                    "edi_id": 3000,
                },
            ]
        )
        order.invalidate_recordset()
        new_line1, new_line2 = order.order_line - lines
        self.assertEqual(new_line1.origin_exchange_record_id, self.exc_record_in)
        self.assertEqual(new_line2.origin_exchange_record_id, self.exc_record_in)

    def test_line_exchange_ready(self):
        line_model = self.env["purchase.order.line"]

        regular_line = line_model.new({"product_id": self.product.id})
        section_line = line_model.new({"display_type": "line_section"})
        downpayment_line = line_model.new({"is_downpayment": True})

        self.assertTrue(regular_line.edi_exchange_ready)
        self.assertFalse(section_line.edi_exchange_ready)
        self.assertFalse(downpayment_line.edi_exchange_ready)
