# Copyright 2022 Camptocamp SA
# @author: Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest import mock

from odoo import fields

from odoo.addons.edi_component_oca.tests.common import EDIBackendCommonComponentTestCase
from odoo.addons.edi_xml_oca.tests.common import (
    get_xml_handler,
)

# TODO: split in different tests w/ SingleTransaction


class TestOrderInboundFull(EDIBackendCommonComponentTestCase):
    _schema_path = "base_ubl:data/xsd-2.2/maindoc/UBL-OrderResponse-2.2.xsd"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_env()
        cls.backend = cls._get_backend()
        cls.exc_type_out = cls.env.ref(
            "edi_sale_ubl_output_oca.demo_edi_sale_ubl_output_so_out"
        )
        cls.exc_type_in = cls.env.ref(
            "edi_sale_ubl_output_oca.demo_edi_sale_ubl_output_so_in"
        )
        cls.edi_conf = cls.env.ref(
            "edi_sale_oca.demo_edi_configuration_confirmed"
        ).copy(
            {
                "name": "UBL IN EDI Conf",
                "type_id": cls.exc_type_out.id,
                "backend_id": cls.backend.id,
            }
        )
        # setup inbound record
        cls.exc_type_in = cls.exc_type_in
        cls.exc_type_in.backend_id = cls.backend
        cls.exc_record_in = cls.backend.create_record(
            cls.exc_type_in.code, {"edi_exchange_state": "input_received"}
        )

    @classmethod
    def _get_backend(cls):
        return cls.env.ref("edi_ubl_oca.edi_backend_ubl_demo")

    def _create_order(self):
        # Simulate order creation via incoming EDI exchange
        partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
                "edi_sale_conf_ids": [(4, self.edi_conf.id)],
            }
        )
        order = self.env["sale.order"].create(
            {
                "client_order_ref": "12345",
                "partner_id": partner.id,
                "origin_exchange_record_id": self.exc_record_in.id,
                "commitment_date": fields.Date.today(),
            }
        )
        self.exc_record_in._set_related_record(order)
        self.exc_record_in.edi_exchange_state = "input_processed"
        order.invalidate_recordset()
        return order

    # No need to test sending data
    @mock.patch("odoo.addons.edi_core_oca.models.edi_backend.EDIBackend._exchange_send")
    def test_new_order(self, mock_send):
        order = self._create_order()
        self.assertEqual(len(order.exchange_record_ids), 1)
        order.action_confirm()
        # Should give us a valid order response ack record
        ack_exc_record = order.exchange_record_ids.filtered(
            lambda x: x.type_id == self.exc_type_out
        )
        file_content = ack_exc_record._get_file_content()
        self.assertEqual(ack_exc_record.edi_exchange_state, "output_sent")
        handler = get_xml_handler(self.backend, self._schema_path)
        err = handler.validate(file_content)
        self.assertEqual(err, None, err)
        data = handler.parse_xml(file_content)
        # TODO: test all main data
        self.assertEqual(data["cbc:OrderResponseCode"], "AP")
