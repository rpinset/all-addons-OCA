# Copyright 2025 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase

from odoo.addons.edi_oca.tests.common import EDIBackendTestMixin
from odoo.addons.edi_sale_oca.tests.common import OrderMixin


class TestSaleAction(TransactionCase, EDIBackendTestMixin, OrderMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_env()
        cls._setup_records()
        cls.order = cls._setup_order()
        cls.backend = cls._get_backend()
        cls.exchange_type_out.exchange_filename_pattern = "{record.id}"
        cls.record = cls._create_exchange_record(cls.order)

    @classmethod
    def _create_exchange_record(cls, record):
        return cls.backend.create_record(
            cls.exchange_type_out.code,
            {
                "res_id": record.id,
                "model": record._name,
            },
        )

    def test_order_exchange_record_count_without_picking_records(self):
        self.assertEqual(self.order.exchange_record_count, 1)

    def test_order_exchange_record_count_with_picking_records(self):
        self._create_exchange_record(self.order.picking_ids[:1])
        self.assertEqual(self.order.exchange_record_count, 2)
        self._create_exchange_record(self.order.picking_ids[:1])
        self.assertEqual(self.order.exchange_record_count, 3)

    def test_order_action_view_edi_records_without_picking_records(self):
        action = self.order.action_view_edi_records()
        domain = action["domain"]
        records = self.env["edi.exchange.record"].search(domain)
        self.assertEqual(records, self.record)

    def test_order_action_view_edi_records_with_picking_records(self):
        new_rec = self._create_exchange_record(self.order.picking_ids[:1])
        action = self.order.action_view_edi_records()
        domain = action["domain"]
        records = self.env["edi.exchange.record"].search(domain)
        self.assertEqual(records, self.record + new_rec)
