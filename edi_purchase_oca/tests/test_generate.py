# Copyright 2026 Camptocamp SA
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase

from .common import OrderMixin, PurchaseEDIBackendTestMixin


class TestGenerateViaConf(TransactionCase, PurchaseEDIBackendTestMixin, OrderMixin):
    """Verify that purchase EDI generation is driven by ``edi.configuration``.

    No component / no fake handler: we simply assert that the snippets bound
    to the partner via ``partner_id.edi_purchase_conf_ids`` are executed by
    the state-change event dispatched by ``edi.exchange.consumer.mixin``.

    Each snippet writes a marker on ``conf.description`` so we can verify
    which configurations actually ran.
    """

    # Snippet writes the order's state on the conf description if it matches
    # the expected target state.
    _snippet_tpl = (
        "if record.state == '{state}':\n"
        "    conf.write({{'description': "
        "(conf.description or '') + '|' + record.state}})"
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_env()
        cls._setup_records()

        cls.exc_type = cls._create_exchange_type(
            name="Demo Purchase Order out",
            code="demo_PurchaseOrder_out",
            direction="output",
            exchange_filename_pattern="{record_name}-{type.code}-{dt}",
            exchange_file_ext="xml",
        )
        cls.state_change_trigger = cls.env.ref(
            "edi_purchase_oca.edi_conf_trigger_purchase_order_state_change"
        )
        purchase_model_id = cls.env["ir.model"]._get_id("purchase.order")
        cls.edi_conf_confirmed = cls.env["edi.configuration"].create(
            {
                "name": "Demo Purchase Order - order confirmed",
                "type_id": cls.exc_type.id,
                "backend_id": cls.backend.id,
                "model_id": purchase_model_id,
                "trigger_id": cls.state_change_trigger.id,
                "snippet_do": cls._snippet_tpl.format(state="purchase"),
            }
        )
        cls.edi_conf_cancelled = cls.env["edi.configuration"].create(
            {
                "name": "Demo Purchase Order - order cancelled",
                "type_id": cls.exc_type.id,
                "backend_id": cls.backend.id,
                "model_id": purchase_model_id,
                "trigger_id": cls.state_change_trigger.id,
                "snippet_do": cls._snippet_tpl.format(state="cancel"),
            }
        )
        cls._setup_order_records()

    def test_new_order_no_conf_no_output(self):
        # No conf linked to the vendor -> no snippet executed.
        order = self._create_purchase_order()
        order.button_confirm()
        self.assertFalse(self.edi_conf_confirmed.description)
        self.assertFalse(self.edi_conf_cancelled.description)

    def test_new_order_1conf_output(self):
        self.vendor.edi_purchase_conf_ids = self.edi_conf_confirmed
        order = self._create_purchase_order()
        self.assertFalse(self.edi_conf_confirmed.description)
        order.button_confirm()
        self.assertEqual(self.edi_conf_confirmed.description, "|purchase")
        # The cancelled conf is not even attached to the vendor.
        self.assertFalse(self.edi_conf_cancelled.description)

    def test_new_order_2conf_output(self):
        self.vendor.edi_purchase_conf_ids = (
            self.edi_conf_confirmed | self.edi_conf_cancelled
        )
        order = self._create_purchase_order()
        # Confirm -> only the "confirmed" snippet matches
        order.button_confirm()
        self.assertEqual(self.edi_conf_confirmed.description, "|purchase")
        self.assertFalse(self.edi_conf_cancelled.description)
        # Cancel -> the "cancelled" snippet matches
        order.button_cancel()
        self.assertEqual(self.edi_conf_confirmed.description, "|purchase")
        self.assertEqual(self.edi_conf_cancelled.description, "|cancel")
