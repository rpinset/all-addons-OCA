# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import base64

from lxml import etree

from odoo.exceptions import UserError
from odoo.tests import tagged

from .common import CDC, FakeResponse, SifendeCommon
from .test_connector import taxpayer
from .test_edi_flow import PDF, XML


def form_arch(env, model, xmlid):
    return etree.fromstring(env[model].get_view(env.ref(xmlid).id)["arch"])


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestFormDetails(SifendeCommon):
    # === Refresco del formulario del conector ===

    def test_las_acciones_del_conector_refrescan_el_formulario(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "web.base.url", "https://erp.example.com.py"
        )
        self.fake.add("GET", r"^/contribuyente/webhooks$", FakeResponse(200, []))
        self.fake.add(
            "POST",
            r"^/contribuyente/webhooks$",
            FakeResponse(
                201,
                {
                    "endpoint": {"id": 7, "url": "https://x", "eventos": []},
                    "secreto": "whsec_x",
                },
            ),
        )
        action = self.connector.action_sifende_register_webhook()
        self.assertEqual(action["params"]["next"]["tag"], "soft_reload")
        self.fake.add("DELETE", r"^/contribuyente/webhooks/7$", FakeResponse(204, None))
        action = self.connector.action_sifende_remove_webhook()
        self.assertEqual(action["params"]["next"]["tag"], "soft_reload")

    def test_probar_conexion_refresca_el_ambiente_verificado(self):
        self.fake.add("GET", r"^/contribuyente$", taxpayer())
        action = self.connector.test_connection()
        self.assertEqual(action["params"]["next"]["tag"], "soft_reload")

    def test_las_etiquetas_del_conector_estan_en_espanol(self):
        fields = self.env["l10n_py.edi.connector"].fields_get(
            ["environment", "timeout", "active"], ["string"]
        )
        self.assertEqual(
            {name: field["string"] for name, field in fields.items()},
            {
                "environment": "Ambiente",
                "timeout": "Tiempo de espera (segundos)",
                "active": "Activo",
            },
        )
        field = self.env["account.move"].fields_get(["l10n_py_receipt_id"], ["string"])
        self.assertEqual(field["l10n_py_receipt_id"]["string"], "ID de recibo")

    # === Botones ===

    def test_las_vistas_previas_se_ocultan_con_el_conector_de_sifende(self):
        tree = form_arch(self.env, "account.move", "account.view_move_form")
        for name in (
            "action_preview_xml",
            "action_preview_kude",
            "action_l10n_py_preview_qr",
        ):
            button = tree.xpath(f"//button[@name='{name}']")[0]
            self.assertIn("l10n_py_sifende_enabled", button.get("invisible"), name)

    def test_el_id_de_lote_se_oculta_con_el_conector_de_sifende(self):
        tree = form_arch(self.env, "account.move", "account.view_move_form")
        field = tree.xpath("//field[@name='l10n_py_edi_batch_id']")[0]
        self.assertIn("l10n_py_sifende_enabled", field.get("invisible"))

    def test_el_transporte_ofrece_solo_los_libres_o_del_propio_documento(self):
        tree = form_arch(self.env, "account.move", "account.view_move_form")
        for section in ("nre_section", "export_transport_section"):
            field = tree.xpath(
                f"//group[@name='{section}']//field[@name='l10n_py_transport_id']"
            )[0]
            self.assertIn("move_id", field.get("domain"), section)

    def test_el_estado_edi_muestra_el_qr(self):
        tree = form_arch(self.env, "account.move", "account.view_move_form")
        self.assertTrue(tree.xpath("//field[@name='l10n_py_qr_code'][@widget='image']"))


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestButtonsByRole(SifendeCommon):
    def make_user(self, login, group):
        return self.env["res.users"].create(
            {
                "name": login,
                "login": login,
                "company_id": self.company.id,
                "company_ids": [(6, 0, self.company.ids)],
                "groups_id": [
                    (
                        6,
                        0,
                        [self.env.ref("base.group_user").id, self.env.ref(group).id],
                    )
                ],
            }
        )

    def buttons(self, user, model, xmlid):
        env = self.env(user=user)
        tree = form_arch(env, model, xmlid)
        return {button.get("name") for button in tree.xpath("//button")}

    def test_el_usuario_de_solo_lectura_no_ve_enviar_ni_reintentar(self):
        reader = self.make_user("lectura-botones", "account.group_account_readonly")
        names = self.buttons(reader, "account.move", "account.view_move_form")
        self.assertNotIn("action_send_edi", names)
        self.assertNotIn("action_retry_edi", names)

    def test_facturacion_ve_enviar_y_reintentar_pero_no_probar_conexion(self):
        biller = self.make_user("facturador-botones", "account.group_account_invoice")
        names = self.buttons(biller, "account.move", "account.view_move_form")
        self.assertIn("action_send_edi", names)
        self.assertIn("action_retry_edi", names)
        form = "l10n_py_edi_base.view_edi_connector_form"
        self.assertNotIn(
            "test_connection", self.buttons(biller, "l10n_py.edi.connector", form)
        )

    def test_el_administrador_de_contabilidad_ve_probar_conexion(self):
        manager = self.make_user("contador-botones", "account.group_account_manager")
        form = "l10n_py_edi_base.view_edi_connector_form"
        self.assertIn(
            "test_connection", self.buttons(manager, "l10n_py.edi.connector", form)
        )


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestFiscalName(SifendeCommon):
    def test_el_nombre_fiscal_dice_el_tipo_y_el_numero_completo(self):
        for kind, label in (
            ("fe", "Factura"),
            ("nc", "Nota de Crédito"),
            ("nd", "Nota de Débito"),
            ("nr", "Nota de Remisión"),
            ("af", "Autofactura"),
        ):
            with self.subTest(kind=kind):
                move = self.make_move(kind)
                self.assertEqual(
                    move.l10n_py_sifende_document_name, f"{label} 001-001-0000001"
                )
                self.assertEqual(move.display_name, move.l10n_py_sifende_document_name)
                self.assertEqual(move._get_report_base_filename(), move.display_name)

    def test_un_borrador_conserva_su_nombre(self):
        move = self.make_move("nd", posted=False)
        self.assertFalse(move.l10n_py_sifende_document_name)
        self.assertEqual(move.display_name, "Draft Invoice")

    def test_un_documento_de_otra_empresa_conserva_el_nombre_de_odoo(self):
        move = self.make_move("fe")
        self.connector.unlink()
        move.invalidate_recordset()
        self.assertFalse(move.l10n_py_sifende_document_name)
        self.assertIn(move.name, move.display_name)

    def test_el_asunto_del_correo_usa_el_nombre_fiscal(self):
        move = self.make_move("nd")
        subject = self.env["account.move.send"]._get_default_mail_subject(
            move, move._get_mail_template(), "en_US"
        )
        self.assertIn("(Ref Nota de Débito 001-001-0000001)", subject)
        self.assertNotIn(move.name, subject)


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestChequeAndCard(SifendeCommon):
    def cheque(self, number, bank="Banco Continental", **vals):
        return self.make_move(
            "fe",
            l10n_py_payment_type="2",
            l10n_py_sifende_cheque_numero=number,
            l10n_py_sifende_cheque_banco=bank,
            **vals,
        )

    def test_un_cheque_de_mas_de_8_digitos_se_rechaza_en_vez_de_truncarse(self):
        move = self.cheque("123456789")
        self.assertEqual(move.l10n_py_sifende_cheque_numero, "123456789")
        errors = move._l10n_py_sifende_cheque_errors()
        self.assertEqual(len(errors), 1)
        self.assertIn("hasta 8", errors[0])

    def test_un_cheque_de_8_digitos_se_acepta(self):
        self.assertFalse(self.cheque("12345678")._l10n_py_sifende_cheque_errors())

    def test_un_banco_de_mas_de_20_caracteres_se_rechaza_en_vez_de_truncarse(self):
        move = self.cheque("1234", bank="Banco Nacional de Fomento S.A.")
        self.assertEqual(
            move.l10n_py_sifende_cheque_banco, "Banco Nacional de Fomento S.A."
        )
        errors = move._l10n_py_sifende_cheque_errors()
        self.assertEqual(len(errors), 1)
        self.assertIn("banco", errors[0])

    def test_el_envio_con_un_cheque_largo_no_llama_a_sifende(self):
        move = self.cheque("123456789")
        with self.assertRaisesRegex(Exception, "hasta 8"):
            move.action_send_edi()
        self.assertFalse(self.fake.calls_to("POST", ".*"))

    def test_la_marca_de_la_tarjeta_sale_del_catalogo(self):
        for code, name in (("1", "VISA"), ("2", "MASTERCARD"), ("6", "CABAL")):
            with self.subTest(brand=name):
                move = self.make_move(
                    "fe",
                    l10n_py_payment_type="3",
                    l10n_py_sifende_tarjeta_marca=code,
                )
                card = self.sent_payload(move)["pagos"][0]["tarjeta"]
                self.assertEqual(card["tipoTarjeta"], name)
                self.assertNotIn("descripcionTipoTarjeta", card)

    def test_una_linea_sin_producto_dice_cual_es(self):
        move = self.make_move(
            "fe", lines=[self.line(product_id=False, name="Servicio sin código")]
        )
        with self.assertRaisesRegex(
            UserError, 'La línea "Servicio sin código" no tiene producto'
        ) as error:
            move.action_send_edi()
        self.assertNotIn("código NCM", str(error.exception))
        self.assertFalse(self.fake.calls_to("POST", ".*"))

    def test_una_linea_sin_producto_ni_descripcion_se_nombra_por_su_posicion(self):
        move = self.make_move(
            "fe",
            lines=[
                self.line(),
                self.line(),
                self.line(product_id=False, name=False),
            ],
        )
        with self.assertRaisesRegex(
            UserError, "La línea n.º 3 no tiene producto"
        ) as error:
            move.action_send_edi()
        self.assertNotIn('""', str(error.exception))
        self.assertFalse(self.fake.calls_to("POST", ".*"))

    def test_una_tarjeta_sin_marca_se_frena_antes_de_enviar(self):
        move = self.make_move("fe", l10n_py_payment_type="4")
        with self.assertRaisesRegex(UserError, "marca de la tarjeta"):
            move.action_send_edi()
        self.assertFalse(self.fake.calls_to("POST", ".*"))

    def test_la_marca_otra_se_informa_como_otro(self):
        move = self.make_move(
            "fe", l10n_py_payment_type="4", l10n_py_sifende_tarjeta_marca="99"
        )
        card = self.sent_payload(move)["pagos"][0]["tarjeta"]
        self.assertEqual(card["tipoTarjeta"], "OTRO")
        self.assertEqual(card["descripcionTipoTarjeta"], "Otro")

    def test_la_marca_se_congela_con_el_documento_enviado(self):
        move = self.make_move(
            "fe", l10n_py_payment_type="3", l10n_py_sifende_tarjeta_marca="1"
        )
        self.sent_payload(move)
        with self.assertRaisesRegex(Exception, "datos de pago"):
            move.l10n_py_sifende_tarjeta_marca = "2"


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestAttachments(SifendeCommon):
    def accepted(self):
        move = self.make_move("fe")
        self.route_emission(self.emission_response())
        move.action_send_edi()
        self.fake.add(
            "GET",
            rf"/documento-electronico/status/{CDC}$",
            self.status_response("APROBADO"),
        )
        self.fake.add(
            "GET",
            rf"/documento-electronico/{CDC}/xml$",
            FakeResponse(200, content=XML, headers={"Content-Type": "application/xml"}),
        )
        self.fake.add(
            "GET",
            rf"/documento-electronico/{CDC}/kude$",
            FakeResponse(200, content=PDF, headers={"Content-Type": "application/pdf"}),
        )
        self.env["account.move"]._cron_sifende_check_status()
        return move

    def attachments(self, move):
        return self.env["ir.attachment"].search(
            [
                ("res_model", "=", "account.move"),
                ("res_id", "=", move.id),
                ("res_field", "=", False),
            ]
        )

    def test_el_xml_y_el_kude_quedan_como_adjuntos_de_la_factura(self):
        move = self.accepted()
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        files = {att.name: att for att in self.attachments(move)}
        self.assertEqual(set(files), {f"{CDC}.xml", f"KUDE_{CDC}.pdf"})
        self.assertEqual(files[f"{CDC}.xml"].raw, XML)
        self.assertEqual(files[f"KUDE_{CDC}.pdf"].raw, PDF)
        self.assertEqual(files[f"{CDC}.xml"].mimetype, "application/xml")
        self.assertEqual(files[f"KUDE_{CDC}.pdf"].mimetype, "application/pdf")
        self.assertEqual(base64.b64decode(move.l10n_py_edi_xml), XML)

    def test_los_adjuntos_del_webhook_conservan_el_mimetype_del_xml(self):
        move = self.make_move("fe")
        public = self.env.ref("base.public_user")
        move.with_user(public).sudo()._l10n_py_sifende_attach(
            f"{CDC}.xml", XML, "application/xml"
        )
        files = {att.name: att for att in self.attachments(move)}
        self.assertEqual(files[f"{CDC}.xml"].mimetype, "application/xml")

    def test_los_adjuntos_no_se_duplican(self):
        move = self.accepted()
        move._l10n_py_sifende_attach(f"{CDC}.xml", XML, "application/xml")
        move.l10n_py_kude_pdf = False
        move._generate_kude()
        self.assertEqual(len(self.attachments(move)), 2)
