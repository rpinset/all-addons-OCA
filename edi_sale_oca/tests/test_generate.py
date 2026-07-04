# Copyright 2024 Camptocamp SA
# @author: Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase

from .common import SaleEDIBackendTestMixin


class TestGenerateViaConf(TransactionCase, SaleEDIBackendTestMixin):
    """Verify that sale EDI generation is driven by ``edi.configuration``.

    No component / no fake handler: we simply assert that the snippets bound
    to the partner via ``partner_id.edi_sale_conf_ids`` are executed by
    the state-change event dispatched by ``edi.exchange.consumer.mixin``.

    Each snippet writes a marker on ``conf.description`` so we can verify
    which configurations actually ran.
    """

    _snippet_tpl = (
        "if record.state == '{state}':\n"
        "    conf.write({{'description': "
        "(conf.description or '') + '|' + record.state}})"
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls._setup_env()
        cls._setup_records()

        cls.exc_type = cls._create_exchange_type(
            name="Demo Sale Order out",
            code="demo_SaleOrder_out",
            direction="output",
            exchange_filename_pattern="{record_name}-{type.code}-{dt}",
            exchange_file_ext="xml",
        )
        cls.state_change_trigger = cls.env.ref(
            "edi_sale_oca.edi_conf_trigger_sale_order_state_change"
        )
        sale_model_id = cls.env["ir.model"]._get_id("sale.order")
        cls.edi_conf_confirmed = cls.env["edi.configuration"].create(
            {
                "name": "Demo Sale Order - order confirmed",
                "type_id": cls.exc_type.id,
                "backend_id": cls.backend.id,
                "model_id": sale_model_id,
                "trigger_id": cls.state_change_trigger.id,
                "snippet_do": cls._snippet_tpl.format(state="sale"),
            }
        )
        cls.edi_conf_done = cls.env["edi.configuration"].create(
            {
                "name": "Demo Sale Order - order cancelled",
                "type_id": cls.exc_type.id,
                "backend_id": cls.backend.id,
                "model_id": sale_model_id,
                "trigger_id": cls.state_change_trigger.id,
                "snippet_do": cls._snippet_tpl.format(state="cancel"),
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "John Doe"})

    def test_new_order_no_conf_no_output(self):
        order = self.env["sale.order"].create({"partner_id": self.partner.id})
        order.action_confirm()
        self.assertFalse(self.edi_conf_confirmed.description)
        self.assertFalse(self.edi_conf_done.description)

    def test_new_order_1conf_output(self):
        self.partner.edi_sale_conf_ids = self.edi_conf_confirmed
        order = self.env["sale.order"].create({"partner_id": self.partner.id})
        self.assertFalse(self.edi_conf_confirmed.description)
        order.action_confirm()
        self.assertEqual(self.edi_conf_confirmed.description, "|sale")
        self.assertFalse(self.edi_conf_done.description)

    def test_new_order_2conf_output(self):
        self.partner.edi_sale_conf_ids = self.edi_conf_confirmed | self.edi_conf_done
        order = self.env["sale.order"].create({"partner_id": self.partner.id})
        order.action_confirm()
        self.assertEqual(self.edi_conf_confirmed.description, "|sale")
        self.assertFalse(self.edi_conf_done.description)
        order._action_cancel()
        self.assertEqual(self.edi_conf_confirmed.description, "|sale")
        self.assertEqual(self.edi_conf_done.description, "|cancel")
