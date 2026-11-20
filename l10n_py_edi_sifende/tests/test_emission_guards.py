# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from lxml import etree

from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged

from .common import CDC, SifendeCommon


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestEmissionGuards(SifendeCommon):
    def test_un_borrador_no_se_envia(self):
        move = self.make_move("fe", posted=False)
        with self.assertRaisesRegex(UserError, "Confirme la factura"):
            move.action_send_edi()
        self.assertFalse(self.fake.calls_to("POST", ".*"))
        self.assertNotEqual(move.l10n_py_edi_status, "sent")

    def test_un_borrador_sin_fecha_no_salta_un_type_error(self):
        move = self.make_move("fe", posted=False)
        move.invoice_date = False
        with self.assertRaisesRegex(UserError, "Confirme la factura"):
            move.action_send_edi()
        errors = move._validate_edi_document_type()
        self.assertTrue(any("fecha" in error for error in errors))

    def test_un_borrador_no_se_reintenta(self):
        move = self.make_move("fe", posted=False)
        move.l10n_py_edi_status = "error"
        with self.assertRaisesRegex(UserError, "Confirme la factura"):
            move.action_retry_edi()
        self.assertEqual(move.l10n_py_sifende_intento, 0)
        self.assertFalse(self.fake.calls_to("POST", ".*"))

    def test_una_factura_cancelada_no_se_envia(self):
        move = self.make_move("fe")
        move.button_draft()
        move.button_cancel()
        with self.assertRaisesRegex(UserError, "Confirme la factura"):
            move.action_send_edi()

    def test_una_factura_publicada_se_envia(self):
        move = self.make_move("fe")
        self.route_emission(self.emission_response())
        move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "processing")

    def test_los_botones_de_envio_se_ocultan_en_borrador(self):
        arch = self.env["account.move"].get_view(
            self.env.ref("account.view_move_form").id
        )["arch"]
        tree = etree.fromstring(arch)
        for name in ("action_send_edi", "action_retry_edi"):
            button = tree.xpath(f"//button[@name='{name}']")[0]
            self.assertIn("state", button.get("invisible"), name)


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestKeyEnvironment(SifendeCommon):
    def test_no_se_guarda_un_conector_de_pruebas_con_clave_de_produccion(self):
        with self.assertRaisesRegex(ValidationError, "sk_live_"):
            self.connector.sifende_api_key = "sk_live_clave-ficticia"

    def test_no_se_guarda_un_conector_de_produccion_con_clave_de_pruebas(self):
        with self.assertRaisesRegex(ValidationError, "Producción"):
            self.connector.environment = "prod"

    def test_las_claves_sandbox_y_test_son_de_pruebas(self):
        for key in ("sk_sandbox_clave-ficticia", "sk_test_clave-ficticia"):
            self.connector.sifende_api_key = key
        self.connector.write(
            {"environment": "prod", "sifende_api_key": "sk_live_clave-ficticia"}
        )
        self.assertEqual(self.connector.environment, "prod")

    def test_una_clave_sin_prefijo_conocido_no_se_valida_localmente(self):
        self.connector.sifende_api_key = "clave-sin-prefijo"
        self.connector.environment = "prod"

    def break_environment(self):
        # una clave guardada antes de la validación o editada por SQL
        self.env.cr.execute(
            "UPDATE l10n_py_edi_connector SET environment = 'prod' WHERE id = %s",
            (self.connector.id,),
        )
        self.connector.invalidate_recordset()

    def test_el_envio_valida_el_ambiente_antes_de_llamar_a_sifende(self):
        move = self.make_move("fe")
        self.break_environment()
        with self.assertRaisesRegex(UserError, "ambiente"):
            move.action_send_edi()
        self.assertFalse(self.fake.calls)
        self.assertNotEqual(move.l10n_py_edi_status, "sent")

    def test_reintentar_valida_el_ambiente(self):
        move = self.make_move("fe")
        move.write({"l10n_py_edi_status": "error"})
        self.break_environment()
        with self.assertRaisesRegex(UserError, "ambiente"):
            move.action_retry_edi()
        self.assertFalse(self.fake.calls_to("POST", ".*"))

    def test_cancelar_valida_el_ambiente(self):
        move = self.make_move("fe")
        move.write({"l10n_py_edi_status": "accepted", "l10n_py_cdc": CDC})
        self.break_environment()
        with self.assertRaisesRegex(UserError, "ambiente"):
            move.action_cancel_edi()
        self.assertFalse(self.fake.calls_to("POST", ".*"))

    def test_inutilizar_valida_el_ambiente(self):
        self.break_environment()
        with self.assertRaisesRegex(UserError, "ambiente"):
            self.connector.inutilize_range({})
        self.assertFalse(self.fake.calls_to("POST", ".*"))
