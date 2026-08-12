# Copyright 2026 Camptocamp SA
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase

from odoo.addons.purchase_order_ubl.tests.common import PurchaseOrderUblMixin


class TestPurchaseUBLOutputGenerate(PurchaseOrderUblMixin, TransactionCase):
    """Ensure ``edi.output.ubl.purchase.order`` produces a valid UBL XML file."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context, tracking_disable=True, edi__skip_quick_exec=True
            )
        )
        cls._setup_purchase_ubl_records()
        cls.backend_type = cls.env.ref("edi_ubl_oca.edi_backend_type_ubl")
        cls.backend = cls.env["edi.backend"].create(
            {
                "name": "UBL purchase test backend",
                "backend_type_id": cls.backend_type.id,
            }
        )
        generator_model = cls.env["ir.model"]._get("edi.output.ubl.purchase.order")
        cls.exc_type = cls.env["edi.exchange.type"].create(
            {
                "name": "Test UBL PO out",
                "code": "test_ubl_po_out",
                "direction": "output",
                "exchange_file_ext": "xml",
                "exchange_filename_pattern": "{record.id}-{type.code}-{dt}",
                "backend_id": cls.backend.id,
                "backend_type_id": cls.backend_type.id,
                "generate_model_id": generator_model.id,
            }
        )

    def _create_exchange_record(self):
        return self.backend.create_record(
            self.exc_type.code,
            {"model": self.order._name, "res_id": self.order.id},
        )

    def _generate_xml(self, version):
        record = self._create_exchange_record()
        record.with_context(ubl_version=version).action_exchange_generate()
        self.assertTrue(record.exchange_file)
        return record._get_file_content()

    def test_generate_order_confirmed(self):
        self.order.button_confirm()
        self.assertEqual(self.order.state, "purchase")
        for version in ("2.1", "2.2"):
            with self.subTest(version=version):
                xml_string = self._generate_xml(version)
                self._assert_valid_ubl_xml(xml_string, "Order", version)

    def test_generate_rfq(self):
        self.assertIn(self.order.state, self.order.get_rfq_states())
        for version in ("2.1", "2.2"):
            with self.subTest(version=version):
                xml_string = self._generate_xml(version)
                self._assert_valid_ubl_xml(xml_string, "RequestForQuotation", version)

    def test_generate_skip_taxes_via_advanced_settings(self):
        """``advanced_settings_edit`` must propagate ``env_ctx`` to generate.

        Setting ``ubl_add_item__skip_taxes: true`` on the ``generate``
        component env_ctx must result in no ``ClassifiedTaxCategory``
        nodes in the produced UBL XML.
        """
        self.exc_type.advanced_settings_edit = (
            "execution_model:\n"
            "  generate:\n"
            "    env_ctx:\n"
            "      ubl_add_item__skip_taxes: true\n"
        )
        self.order.button_confirm()
        xml_string = self._generate_xml("2.1")
        parsed = self._assert_valid_ubl_xml(xml_string, "Order", "2.1")
        tax_nodes = self._classified_tax_categories(parsed)
        self.assertFalse(
            tax_nodes,
            "ClassifiedTaxCategory must be skipped when "
            "ubl_add_item__skip_taxes is set via advanced_settings_edit",
        )

    def test_generate_taxes_included_by_default(self):
        """Without any env_ctx, ClassifiedTaxCategory must be present."""
        self.order.button_confirm()
        xml_string = self._generate_xml("2.1")
        parsed = self._assert_valid_ubl_xml(xml_string, "Order", "2.1")
        self.assertTrue(self._classified_tax_categories(parsed))
