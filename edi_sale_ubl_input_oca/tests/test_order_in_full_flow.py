# Copyright 2022 Camptocamp SA
# @author: Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest import mock

from odoo.addons.edi_oca.tests.common import EDIBackendCommonComponentTestCase
from odoo.addons.edi_sale_ubl_oca.tests.common import OrderInboundTestMixin

# TODO: split in different tests w/ SingleTransaction


class TestOrderInboundFull(EDIBackendCommonComponentTestCase, OrderInboundTestMixin):

    _schema_path = "base_ubl:data/xsd-2.2/maindoc/UBL-OrderResponse-2.2.xsd"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_env()
        cls.backend = cls._get_backend()
        cls.exc_type_out = cls.env.ref(
            "edi_sale_ubl_input_oca.demo_edi_sale_ubl_input_so_out"
        )
        cls.exc_type_in = cls.env.ref(
            "edi_sale_ubl_input_oca.demo_edi_sale_ubl_input_so_in"
        )
        cls._setup_inbound_order(cls.backend, cls.exc_type_in)
        cls.edi_conf = cls.env.ref(
            "edi_sale_oca.demo_edi_configuration_confirmed"
        ).copy(
            {
                "name": "UBL IN EDI Conf",
                "type_id": cls.exc_type_out.id,
                "backend_id": cls.backend.id,
            }
        )

    @classmethod
    def _get_backend(cls):
        return cls.env.ref("edi_ubl_oca.edi_backend_ubl_demo")

    # No need to test sending data
    @mock.patch("odoo.addons.edi_oca.models.edi_backend.EDIBackend._exchange_send")
    def test_new_order(self, mock_send):
        order = self._find_order()
        self.backend._check_input_exchange_sync()
        self.assertEqual(self.exc_record_in.edi_exchange_state, "input_processed")
        order = self._find_order()
        order.partner_id.edi_sale_conf_ids = self.edi_conf
        self.assertEqual(self.exc_record_in.record, order)
        order_msg = order.message_ids[0]
        self.assertIn("Exchange processed successfully", order_msg.body)
        self.assertIn(self.exc_record_in.identifier, order_msg.body)
        order.invalidate_cache()
        # Test relations
        self.assertEqual(len(order.exchange_record_ids), 1)
        exc_record = order.exchange_record_ids.filtered(
            lambda x: x.type_id == self.exc_type_in
        )
        self.assertEqual(exc_record, self.exc_record_in)
        # Confirm the order
        with mock.patch.object(
            type(self.backend), "_exchange_generate"
        ) as mock_generate:
            mock_generate.return_value = "<xml>fake</xml>"
            order.action_confirm()
        # Should give us a valid order response ack record
        ack_exc_record = order.exchange_record_ids.filtered(
            lambda x: x.type_id == self.exc_type_out
        )
        file_content = ack_exc_record._get_file_content()
        self.assertEqual(file_content, "<xml>fake</xml>")
        self.assertEqual(ack_exc_record.edi_exchange_state, "output_sent")
