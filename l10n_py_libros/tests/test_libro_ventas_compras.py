from unittest.mock import patch

from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged

from .test_libro_common import LibroCommonCase


@tagged("post_install", "-at_install", "l10n_py", "l10n_py_libros")
class TestLibroVentasCompras(LibroCommonCase):
    def test_ventas_contado_10(self):
        invoice = self._create_invoice(
            "out_invoice", [(self.product, self.tax_10, 1100.0)]
        )
        invoice.action_post()
        libro = self._create_libro("ventas")
        libro.action_generate_lines()
        self.assertEqual(len(libro.line_ids), 1)
        line = libro.line_ids
        self.assertEqual(line.state, "ok", line.error_message)
        self.assertEqual(line.f_condicion, "1")
        self.assertEqual(
            line.f_monto_gravado_10, int(invoice.l10n_py_amount_subtotal_10)
        )
        self.assertEqual(line.f_monto_exento, int(invoice.l10n_py_amount_exempt))
        self.assertEqual(
            line.f_monto_total,
            line.f_monto_gravado_10 + line.f_monto_gravado_5 + line.f_monto_exento,
        )

    def test_compras_credito_5_exento(self):
        invoice = self._create_invoice(
            "in_invoice",
            [
                (self.product, self.tax_5_purchase, 525.0),
                (self.product, False, 100.0),
            ],
            invoice_payment_term_id=self.term_credit.id,
            l10n_py_libro_supplier_timbrado="87654321",
            l10n_py_libro_supplier_number="001-001-0000001",
        )
        invoice.action_post()
        libro = self._create_libro("compras")
        libro.action_generate_lines()
        self.assertEqual(len(libro.line_ids), 1)
        line = libro.line_ids
        self.assertEqual(line.state, "ok", line.error_message)
        self.assertEqual(line.f_condicion, "2")
        self.assertEqual(line.f_monto_gravado_10, 0)
        self.assertEqual(line.f_monto_gravado_5, int(invoice.l10n_py_amount_subtotal_5))
        self.assertEqual(line.f_monto_exento, int(invoice.l10n_py_amount_exempt))

    def test_compras_autofactura_101(self):
        invoice = self._create_invoice(
            "in_invoice",
            [(self.product, self.tax_10_purchase, 1100.0)],
            doc_type=self.doc_type_autofactura,
            l10n_py_libro_supplier_timbrado="87654322",
            l10n_py_libro_supplier_number="001-001-0000002",
        )
        invoice.action_post()
        libro = self._create_libro("compras")
        libro.action_generate_lines()
        line = libro.line_ids
        self.assertEqual(line.f_tipo_comprobante, "101")
        self.assertEqual(line.f_monto_gravado_10, 0)
        self.assertEqual(line.f_monto_gravado_5, 0)
        self.assertEqual(line.f_monto_exento, 0)
        self.assertEqual(line.f_monto_total, int(round(invoice.amount_total)))
        self.assertEqual(line.state, "ok", line.error_message)

    def test_ventas_excluye_aceptado_sifen(self):
        invoice = self._create_invoice(
            "out_invoice", [(self.product, self.tax_10, 1100.0)]
        )
        invoice.action_post()
        invoice.l10n_py_edi_status = "accepted"
        invoice.l10n_py_cdc = "0" * 44
        libro = self._create_libro("ventas")
        libro.action_generate_lines()
        self.assertEqual(len(libro.line_ids), 0)

    def test_compras_excluye_electronico_manual(self):
        invoice = self._create_invoice(
            "in_invoice",
            [(self.product, self.tax_10_purchase, 1100.0)],
            l10n_py_libro_supplier_timbrado="87654323",
            l10n_py_libro_supplier_number="001-001-0000003",
            l10n_py_libro_electronic=True,
        )
        invoice.action_post()
        libro = self._create_libro("compras")
        libro.action_generate_lines()
        self.assertEqual(len(libro.line_ids), 0)

    def test_compras_dedup_flag_copiado_del_partner(self):
        self.supplier.with_company(self.company.id).l10n_py_libro_electronic = True
        invoice = self.env["account.move"].create(
            {
                "move_type": "in_invoice",
                "partner_id": self.supplier.id,
                "journal_id": self.purchase_journal.id,
            }
        )
        self.assertTrue(invoice.l10n_py_libro_electronic)

    def test_nc_emitida_en_compras_direccion_padrao(self):
        original = self._create_invoice(
            "out_invoice", [(self.product, self.tax_10, 1100.0)]
        )
        original.action_post()
        nc = self._create_invoice(
            "out_refund",
            [(self.product, self.tax_10, 1100.0)],
            doc_type=self.doc_type_nc,
            reversed_entry_id=original.id,
        )
        nc.action_post()
        libro = self._create_libro("compras")
        libro.action_generate_lines()
        self.assertEqual(len(libro.line_ids), 1)
        line = libro.line_ids
        self.assertEqual(line.f_tipo_comprobante, "110")
        self.assertTrue(line.f_comprobante_asociado_numero)
        self.assertTrue(line.f_comprobante_asociado_timbrado)
        self.assertGreaterEqual(line.f_monto_total, 0)

    def test_nc_direccion_invertida(self):
        self.company.l10n_py_libro_nc_nd_direction = "invertida"
        original = self._create_invoice(
            "out_invoice", [(self.product, self.tax_10, 1100.0)]
        )
        original.action_post()
        nc = self._create_invoice(
            "out_refund",
            [(self.product, self.tax_10, 1100.0)],
            doc_type=self.doc_type_nc,
            reversed_entry_id=original.id,
        )
        nc.action_post()
        libro = self._create_libro("ventas")
        libro.action_generate_lines()
        # Con dirección invertida, tanto la factura original (siempre Ventas
        # por ser out_invoice) como la NC propia (invertida: NC own -> ventas)
        # aparecen en el registro de Ventas.
        self.assertEqual(len(libro.line_ids), 2)
        nc_line = libro.line_ids.filtered(lambda line: line.f_tipo_comprobante == "110")
        self.assertEqual(len(nc_line), 1)

    def test_troca_direccion_bloqueada_con_libro_generado(self):
        libro = self._create_libro("compras")
        libro.action_generate_lines()
        libro.state = "generated"
        with self.assertRaises(UserError):
            self.company.l10n_py_libro_nc_nd_direction = "invertida"
        libro.action_reopen()
        libro.state = "draft"
        self.company.l10n_py_libro_nc_nd_direction = "invertida"
        self.assertEqual(self.company.l10n_py_libro_nc_nd_direction, "invertida")

    def test_timbrado_fornecedor_formato_invalido(self):
        with self.assertRaises(ValidationError):
            self._create_invoice(
                "in_invoice",
                [(self.product, self.tax_10_purchase, 1100.0)],
                l10n_py_libro_supplier_number="invalido",
            )

    def test_timbrado_fornecedor_vazio_marca_linha_em_erro(self):
        invoice = self._create_invoice(
            "in_invoice", [(self.product, self.tax_10_purchase, 1100.0)]
        )
        invoice.action_post()
        libro = self._create_libro("compras")
        libro.action_generate_lines()
        line = libro.line_ids
        self.assertEqual(line.state, "erro")

    def test_condicion_venta_sem_termino(self):
        invoice = self._create_invoice(
            "out_invoice", [(self.product, self.tax_10, 1100.0)]
        )
        self.assertEqual(invoice.l10n_py_condicion_venta, "1")

    def test_condicion_venta_termino_com_prazo(self):
        invoice = self._create_invoice(
            "out_invoice",
            [(self.product, self.tax_10, 1100.0)],
            invoice_payment_term_id=self.term_credit.id,
        )
        self.assertEqual(invoice.l10n_py_condicion_venta, "2")

    def test_action_confirm_bloqueado_com_linha_em_erro(self):
        invoice = self._create_invoice(
            "in_invoice", [(self.product, self.tax_10_purchase, 1100.0)]
        )
        invoice.action_post()
        libro = self._create_libro("compras")
        libro.action_generate_lines()
        with self.assertRaises(UserError):
            libro.action_confirm()

    def test_action_download_zip_bloqueado_com_linha_em_erro(self):
        invoice = self._create_invoice(
            "in_invoice", [(self.product, self.tax_10_purchase, 1100.0)]
        )
        invoice.action_post()
        libro = self._create_libro("compras")
        libro.action_generate_lines()
        with self.assertRaises(UserError):
            libro.action_download_zip()

    def test_corrigir_documento_e_regenerar_remove_erro(self):
        invoice = self._create_invoice(
            "in_invoice", [(self.product, self.tax_10_purchase, 1100.0)]
        )
        invoice.action_post()
        libro = self._create_libro("compras")
        libro.action_generate_lines()
        self.assertEqual(libro.line_ids.state, "erro")
        invoice.write(
            {
                "l10n_py_libro_supplier_timbrado": "87654324",
                "l10n_py_libro_supplier_number": "001-001-0000004",
            }
        )
        libro.action_generate_lines()
        self.assertEqual(libro.line_ids.state, "ok", libro.line_ids.error_message)

    def test_regenerar_preserva_override_manual(self):
        invoice = self._create_invoice(
            "out_invoice", [(self.product, self.tax_10, 1100.0)]
        )
        invoice.action_post()
        libro = self._create_libro("ventas")
        libro.action_generate_lines()
        line = libro.line_ids
        line.write({"f_imputa_ire": "S"})
        self.assertTrue(line.manual_override)
        libro.action_generate_lines()
        self.assertEqual(line.f_imputa_ire, "S")

    def test_restaurar_valores_gerados_limpa_override(self):
        invoice = self._create_invoice(
            "out_invoice", [(self.product, self.tax_10, 1100.0)]
        )
        invoice.action_post()
        libro = self._create_libro("ventas")
        libro.action_generate_lines()
        line = libro.line_ids
        line.write({"f_imputa_ire": "S"})
        line.action_restore_generated_values()
        self.assertFalse(line.manual_override)
        self.assertEqual(line.f_imputa_ire, "N")

    def _foreign_currency(self):
        """Return a currency different from the company currency."""
        currency = self.env.ref("base.USD")
        if currency == self.company.currency_id:
            currency = self.env.ref("base.EUR")
        currency.active = True
        return currency

    def test_moeda_estrangeira_com_taxa_manual(self):
        currency_usd = self._foreign_currency()
        invoice = self._create_invoice(
            "out_invoice",
            [(self.product, self.tax_10, 100.0)],
            currency_id=currency_usd.id,
            l10n_py_exchange_rate=7300.0,
        )
        invoice.action_post()
        libro = self._create_libro("ventas")
        libro.action_generate_lines()
        line = libro.line_ids
        self.assertEqual(line.f_moneda_extranjera, "S")
        self.assertGreater(line.f_monto_total, 100)

    def test_moeda_estrangeira_conversao_pyg_soma_baldes_igual_total(self):
        # O1 - residual de arredondamento (D1 item 3): cada balde é
        # convertido/arredondado de forma independente, mas o resíduo deve
        # ser absorvido pelo maior balde não-zero para que 9+10+11 == 12
        # exatamente, e o total deve bater com move.amount_total convertido
        # com tolerancia de 1 guaraní.
        currency_usd = self._foreign_currency()
        invoice = self._create_invoice(
            "out_invoice",
            [
                (self.product, self.tax_10, 111.11),
                (self.product, self.tax_5, 33.33),
                (self.product, False, 7.77),
            ],
            currency_id=currency_usd.id,
            l10n_py_exchange_rate=7300.1234,
        )
        invoice.action_post()
        libro = self._create_libro("ventas")
        libro.action_generate_lines()
        line = libro.line_ids
        self.assertEqual(line.state, "ok", line.error_message)
        self.assertEqual(
            line.f_monto_gravado_10 + line.f_monto_gravado_5 + line.f_monto_exento,
            line.f_monto_total,
        )
        target = libro._get_total_in_pyg(invoice)
        self.assertLessEqual(abs(line.f_monto_total - target), 1)

    def test_monto_total_e_soma_dos_baldes_marca_linha_em_erro(self):
        # O1 - a checagem "total vs. baldes" tem que comparar contra
        # move.amount_total (não só consigo mesma): editar manualmente o
        # monto_total sem alterar o comprovante de origem deve marcar erro.
        invoice = self._create_invoice(
            "out_invoice", [(self.product, self.tax_10, 1100.0)]
        )
        invoice.action_post()
        libro = self._create_libro("ventas")
        libro.action_generate_lines()
        line = libro.line_ids
        self.assertEqual(line.state, "ok", line.error_message)
        line.write({"f_monto_total": line.f_monto_total + 5000})
        self.assertEqual(line.state, "erro")
        self.assertIn("monto total", line.error_message.lower())

    def test_documento_alterado_apos_geracao_recalcula_state(self):
        # O2 - @api.depends alargado (move_id.l10n_py_libro_supplier_timbrado
        # /_number/l10n_py_authorization_id/reversed_entry_id/l10n_py_edi_
        # status/l10n_py_cdc, libro_id.company_id.l10n_py_libro_nc_nd_
        # direction): alterar o documento de origem depois da geração, sem
        # chamar action_generate_lines/action_confirm/action_download_zip
        # nem editar a línea diretamente, tem que recalcular o state
        # automaticamente via store=True.
        invoice = self._create_invoice(
            "in_invoice",
            [(self.product, self.tax_10_purchase, 1100.0)],
            l10n_py_libro_supplier_timbrado="87654329",
            l10n_py_libro_supplier_number="001-001-0000009",
        )
        invoice.action_post()
        libro = self._create_libro("compras")
        libro.action_generate_lines()
        line = libro.line_ids
        self.assertEqual(line.state, "ok", line.error_message)
        invoice.l10n_py_libro_supplier_timbrado = False
        self.assertEqual(line.state, "erro")

    def test_ventas_solo_exonerado_va_al_campo_no_gravado(self):
        invoice = self._create_invoice(
            "out_invoice", [(self.product, self.tax_exonerado, 5000.0)]
        )
        invoice.action_post()
        libro = self._create_libro("ventas")
        libro.action_generate_lines()
        line = libro.line_ids
        self.assertEqual(line.state, "ok", line.error_message)
        self.assertEqual(line.f_monto_gravado_10, 0)
        self.assertEqual(line.f_monto_gravado_5, 0)
        self.assertEqual(line.f_monto_exento, 5000)
        self.assertEqual(line.f_monto_total, 5000)

    def test_ventas_mixta_exonerado_no_se_suma_al_gravado_10(self):
        invoice = self._create_invoice(
            "out_invoice",
            [
                (self.product, self.tax_10, 1100.0),
                (self.product, self.tax_exonerado, 900.0),
            ],
        )
        invoice.action_post()
        libro = self._create_libro("ventas")
        libro.action_generate_lines()
        line = libro.line_ids
        self.assertEqual(line.state, "ok", line.error_message)
        self.assertEqual(line.f_monto_gravado_10, 1100)
        self.assertEqual(line.f_monto_exento, 900)
        self.assertEqual(line.f_monto_total, 2000)

    def test_residuo_mayor_que_redondeo_no_se_redistribuye(self):
        invoice = self._create_invoice(
            "out_invoice", [(self.product, self.tax_10, 1100.0)]
        )
        invoice.action_post()
        libro = self._create_libro("ventas")
        with patch.object(type(libro), "_get_total_in_pyg", return_value=1100 + 500):
            libro.action_generate_lines()
        line = libro.line_ids
        self.assertEqual(line.f_monto_gravado_10, 1100)
        self.assertEqual(line.state, "erro")

    def test_wizard_asigna_letra_de_lote_por_tipo(self):
        wizard = self.env["l10n_py.libro.generate.wizard"].create(
            {
                "company_id": self.company.id,
                "year": self.TEST_YEAR,
                "month": self.TEST_MONTH,
                "incluir_ventas": True,
                "incluir_compras": True,
            }
        )
        wizard.action_generate()
        libros = self.env["l10n_py.libro"].search(
            [("company_id", "=", self.company.id), ("year", "=", self.TEST_YEAR)]
        )
        letras = {libro.tipo_registro: libro.lote_letra for libro in libros}
        self.assertEqual(letras.get("ventas"), "V")
        self.assertEqual(letras.get("compras"), "C")
