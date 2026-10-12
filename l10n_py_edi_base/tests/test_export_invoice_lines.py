from odoo import Command
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "l10n_py")
class TestExportInvoiceLines(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.ref("base.main_company")
        cls.company.country_id = cls.env.ref("base.py")
        cls.tax_exonerado = cls.env["account.tax"].create(
            {
                "name": "IVA Exonerado",
                "amount": 0,
                "amount_type": "percent",
                "type_tax_use": "sale",
                "l10n_py_iva_affectation": "2",
            }
        )
        cls.tax_exento = cls.env["account.tax"].create(
            {
                "name": "IVA Exento",
                "amount": 0,
                "amount_type": "percent",
                "type_tax_use": "sale",
                "l10n_py_iva_affectation": "3",
            }
        )
        cls.product = cls.env["product.product"].create({"name": "Prod export"})

    def _invoice_with_tax(self, tax):
        return self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.env["res.partner"].create({"name": "X"}).id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "quantity": 1,
                            "price_unit": 100,
                            "tax_ids": [Command.set(tax.ids)],
                        }
                    )
                ],
            }
        )

    def test_exonerado_line_emits_ivatipo_2(self):
        inv = self._invoice_with_tax(self.tax_exonerado)
        items = inv._prepare_invoice_lines()
        self.assertEqual(items[0]["ivaTipo"], 2)
        self.assertEqual(items[0]["iva"], 0)
        self.assertEqual(items[0]["ivaBase"], 0)

    def test_exento_still_3(self):
        inv = self._invoice_with_tax(self.tax_exento)
        items = inv._prepare_invoice_lines()
        self.assertEqual(items[0]["ivaTipo"], 3)

    def test_fallback_no_field(self):
        # Retrocompat: força o campo vazio (False) p/ exercitar de verdade o
        # helper _l10n_py_infer_affectation — impostos legados sem afetação.
        tax5 = self.env["account.tax"].create(
            {
                "name": "IVA 5 legacy",
                "amount": 5,
                "amount_type": "percent",
                "type_tax_use": "sale",
            }
        )
        tax5.l10n_py_iva_affectation = False  # simula legado sem o campo
        inv = self._invoice_with_tax(tax5)
        items = inv._prepare_invoice_lines()
        self.assertEqual(items[0]["ivaTipo"], 1)  # fallback: amount 5 -> '1'
        self.assertEqual(items[0]["iva"], 5)

    def test_fallback_no_field_amount_zero(self):
        # Retrocompat: campo vazio + amount 0 cai no fallback -> Exento '3'.
        tax0 = self.env["account.tax"].create(
            {
                "name": "IVA 0 legacy",
                "amount": 0,
                "amount_type": "percent",
                "type_tax_use": "sale",
            }
        )
        tax0.l10n_py_iva_affectation = False  # simula legado sem o campo
        inv = self._invoice_with_tax(tax0)
        items = inv._prepare_invoice_lines()
        self.assertEqual(items[0]["ivaTipo"], 3)  # fallback: amount 0 -> '3'
        self.assertEqual(items[0]["iva"], 0)

    def test_upgrade_path_exento_without_default(self):
        # Camino de upgrade: al agregar la columna en una base existente el
        # campo debe quedar falsy (sin default), de modo que el impuesto
        # Exento preexistente pase por el fallback y NO salga como gravado
        # (ivaTipo=1 con alícuota 0, inconsistente para el SIFEN).
        tax_legacy = self.env["account.tax"].create(
            {
                "name": "IVA Exento legacy",
                "amount": 0,
                "amount_type": "percent",
                "type_tax_use": "sale",
            }
        )
        self.assertFalse(
            tax_legacy.l10n_py_iva_affectation,
            "Sin default: el impuesto creado sin afectación debe quedar falsy",
        )
        inv = self._invoice_with_tax(tax_legacy)
        items = inv._prepare_invoice_lines()
        self.assertEqual(items[0]["ivaTipo"], 3)
        self.assertEqual(items[0]["ivaBase"], 0)

    def test_line_without_tax_raises(self):
        # Una línea sin ningún impuesto no puede caer en el default gravado
        # 10%: debe fallar explícito en la preparación del DE.
        from odoo.exceptions import UserError

        inv = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.env["res.partner"].create({"name": "Y"}).id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "quantity": 1,
                            "price_unit": 100,
                            "tax_ids": [Command.clear()],
                        }
                    )
                ],
            }
        )
        with self.assertRaises(UserError):
            inv._prepare_invoice_lines()

    def _invoice_with_transport(self, doc_type_xmlid, partner_country_xmlid):
        """Fatura (out_invoice) com um l10n_py.transport anexado."""
        doc_type = self.env.ref(doc_type_xmlid)
        partner = self.env["res.partner"].create(
            {
                "name": "Cliente Transporte",
                "country_id": self.env.ref(partner_country_xmlid).id,
            }
        )
        inv = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": partner.id,
                "l10n_latam_document_type_id": doc_type.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "quantity": 1,
                            "price_unit": 100,
                        }
                    )
                ],
            }
        )
        transport = self.env["l10n_py.transport"].create(
            {
                "move_id": inv.id,
                "transport_mode": "1",
                "incoterm": "FOB",
            }
        )
        inv.l10n_py_transport_id = transport.id
        return inv

    def test_export_invoice_emits_transport(self):
        # Factura de Exportación (tipo 1) a parceiro do exterior + transporte
        # com incoterm deve emitir "transporte" no payload EDI.
        inv = self._invoice_with_transport("l10n_py_account.dc_py_f", "base.br")
        data = inv._prepare_edi_document_data()
        self.assertIn("transporte", data)
        self.assertEqual(data["transporte"]["condicionNegociacion"], "FOB")

    def test_nre_transport_regression(self):
        # NRE (tipo 7) continua emitindo "transporte" como antes (regressão).
        nre = self._invoice_with_transport("l10n_py_account.dc_py_nr", "base.py")
        data = nre._prepare_edi_document_data()
        self.assertIn("transporte", data)
        self.assertEqual(data["transporte"]["condicionNegociacion"], "FOB")

    def test_transport_default_incoterm_from_invoice(self):
        # Al crear l10n_py.transport en el contexto de una factura con
        # invoice_incoterm_id, el incoterm se precompleta (evita redigitar
        # el dato que ya llegó del pedido de venta vía sale_stock).
        inv = self._invoice_with_transport("l10n_py_account.dc_py_f", "base.br")
        inv.invoice_incoterm_id = self.env.ref("account.incoterm_FOB")
        transport = (
            self.env["l10n_py.transport"]
            .with_context(default_move_id=inv.id)
            .new({"transport_mode": "3"})
        )
        self.assertEqual(transport.incoterm, "FOB")
