# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import json
from unittest.mock import patch

import requests

from odoo.exceptions import AccessError, UserError
from odoo.tests import tagged

from odoo.addons.l10n_py_edi_sifende.models import edi_connector
from odoo.addons.l10n_py_edi_sifende.services import client

from .common import API_KEY, CDC, STAMP, FakeResponse, SifendeCommon


def taxpayer(**overrides):
    body = {
        "ruc": "80009401",
        "digitoVerificador": "0",
        "razonSocial": "Ejemplo S.A.",
        "ambiente": "DEV",
        "timbrado": {"numero": int(STAMP), "fechaInicioVigencia": "2026-01-15"},
        "establecimientos": [
            {
                "numeroEstablecimiento": 1,
                "nombreSucursal": "Casa central",
                "activo": True,
                "puntosExpedicion": [{"puntoExpedicion": 1, "activo": True}],
            }
        ],
        "estadoConfiguracion": {"listoParaEmitir": True},
    }
    body.update(overrides)
    return FakeResponse(200, body)


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestConnector(SifendeCommon):
    def route_taxpayer(self, response):
        self.fake.add("GET", r"^/contribuyente$", response)

    def message(self, action):
        self.assertEqual(action["tag"], "display_notification")
        return action["params"]

    def test_las_etiquetas_del_conector_estan_en_espanol(self):
        fields = self.connector._fields
        self.assertEqual(fields["company_id"].string, "Empresa")
        self.assertEqual(fields["environment"].string, "Ambiente")

    def test_test_connection_correcta(self):
        self.route_taxpayer(taxpayer())
        params = self.message(self.connector.test_connection())
        self.assertEqual(params["type"], "success")
        self.assertIn("Ejemplo S.A.", params["message"])
        self.assertIn("DEV", params["message"])
        self.assertIn("Listo para emitir: Sí", params["message"])
        self.assertEqual(self.connector.sifende_ambiente, "DEV")

    def test_test_connection_advierte_timbrado_distinto(self):
        self.route_taxpayer(
            taxpayer(timbrado={"numero": 87654321, "fechaInicioVigencia": "2026-01-15"})
        )
        params = self.message(self.connector.test_connection())
        self.assertEqual(params["type"], "warning")
        self.assertIn(
            f"El timbrado {STAMP} de Odoo no coincide con el de SIFENDE (87654321)",
            params["message"],
        )
        self.assertTrue(params["sticky"])

    def test_test_connection_advierte_establecimiento_y_punto_desconocidos(self):
        self.auths["fe"].write({"establishment": "002", "expedition_point": "003"})
        self.route_taxpayer(taxpayer())
        message = self.message(self.connector.test_connection())["message"]
        self.assertIn("establecimiento 002 / punto 003", message)

    def test_test_connection_advierte_un_punto_inactivo(self):
        establishment = taxpayer().json()["establecimientos"][0]
        establishment["puntosExpedicion"][0]["activo"] = False
        self.route_taxpayer(taxpayer(establecimientos=[establishment]))
        message = self.message(self.connector.test_connection())["message"]
        self.assertIn("establecimiento 001 / punto 001", message)
        self.assertIn("inactivo en SIFENDE", message)
        self.assertNotIn("no existe", message)

    def test_test_connection_advierte_un_establecimiento_inactivo(self):
        establishment = taxpayer().json()["establecimientos"][0]
        establishment["activo"] = False
        self.route_taxpayer(taxpayer(establecimientos=[establishment]))
        message = self.message(self.connector.test_connection())["message"]
        self.assertIn("inactivo en SIFENDE", message)

    def test_test_connection_avisa_si_no_esta_listo_para_emitir(self):
        self.route_taxpayer(taxpayer(estadoConfiguracion={"listoParaEmitir": False}))
        params = self.message(self.connector.test_connection())
        self.assertEqual(params["type"], "warning")
        self.assertIn("Listo para emitir: No", params["message"])

    def test_test_connection_falla_si_la_clave_es_de_otro_ambiente(self):
        self.connector.write(
            {"environment": "prod", "sifende_api_key": "sk_live_clave-ficticia"}
        )
        self.route_taxpayer(taxpayer(ambiente="DEV"))
        with self.assertRaisesRegex(UserError, "ambiente DEV"):
            self.connector.test_connection()

    def test_test_connection_prod_con_clave_prod(self):
        self.connector.write(
            {"environment": "prod", "sifende_api_key": "sk_live_clave-ficticia"}
        )
        self.route_taxpayer(taxpayer(ambiente="PROD"))
        self.assertEqual(
            self.message(self.connector.test_connection())["type"], "success"
        )

    def test_test_connection_en_pruebas_acepta_sandbox(self):
        self.route_taxpayer(taxpayer(ambiente="SANDBOX", timbrado=None))
        self.assertEqual(
            self.message(self.connector.test_connection())["type"], "success"
        )

    def test_test_connection_sandbox_no_compara_el_timbrado_sintetico(self):
        self.route_taxpayer(
            taxpayer(
                ambiente="SANDBOX",
                timbrado={"numero": -1, "fechaInicioVigencia": "2000-01-01"},
            )
        )
        message = self.message(self.connector.test_connection())
        self.assertEqual(message["type"], "success")
        self.assertNotIn("timbrado", message["message"])
        self.assertNotIn("\n", message["message"])

    def test_cambiar_la_api_key_borra_el_ambiente_verificado(self):
        self.route_taxpayer(taxpayer(ambiente="SANDBOX"))
        self.connector.test_connection()
        self.assertEqual(self.connector.sifende_ambiente, "SANDBOX")
        self.connector.sifende_api_key = "sk_test_otra-clave-ficticia"
        self.assertFalse(self.connector.sifende_ambiente)

    def test_test_connection_clave_invalida(self):
        self.route_taxpayer(FakeResponse(401, {"error": "Invalid or expired API key"}))
        with self.assertRaisesRegex(UserError, "API key"):
            self.connector.test_connection()

    def test_test_connection_sin_conexion(self):
        self.route_taxpayer(requests.ConnectionError("boom"))
        with self.assertRaisesRegex(UserError, "No se pudo contactar"):
            self.connector.test_connection()

    def test_url_base_configurable(self):
        self.connector.sifende_base_url = "http://localhost:8080/"
        self.route_taxpayer(taxpayer())
        self.connector.test_connection()
        self.assertEqual(
            self.fake.calls_to("GET", "^/contribuyente$")[0].url,
            "http://localhost:8080/api/v1/contribuyente",
        )

    # === Seguridad ===

    def test_la_api_key_solo_la_leen_los_administradores(self):
        self.assertEqual(
            self.connector._fields["sifende_api_key"].groups, "base.group_system"
        )
        manager = self.env["res.users"].create(
            {
                "name": "Contador",
                "login": "contador_sifende",
                "groups_id": [
                    (6, 0, [self.env.ref("account.group_account_manager").id])
                ],
            }
        )
        with self.assertRaises(AccessError):
            self.connector.with_user(manager).sifende_api_key  # noqa: B018

    def test_la_vista_oculta_la_api_key_y_la_enmascara(self):
        arch = self.env["l10n_py.edi.connector"].get_view(view_type="form")["arch"]
        self.assertRegex(arch, r'name="sifende_api_key"[^>]*password="True"')
        manager = self.env["res.users"].create(
            {
                "name": "Contador vista",
                "login": "contador_vista_sifende",
                "groups_id": [
                    (6, 0, [self.env.ref("account.group_account_manager").id])
                ],
            }
        )
        arch = (
            self.env["l10n_py.edi.connector"]
            .with_user(manager)
            .get_view(view_type="form")["arch"]
        )
        self.assertNotIn("sifende_api_key", arch)

    def test_la_api_key_no_aparece_en_los_logs(self):
        self.route_taxpayer(taxpayer())
        self.connector.test_connection()
        move = self.make_move("fe")
        self.route_emission(self.emission_response())
        move.action_send_edi()
        logs = self.env["l10n_py.edi.log"].search([("provider", "=", "sifende")])
        self.assertTrue(logs)
        for log in logs:
            for name in (
                "request_headers",
                "request_data",
                "response_data",
                "error_message",
                "endpoint",
            ):
                self.assertNotIn(API_KEY, log[name] or "")
        headers = json.loads(logs.filtered("request_headers")[0].request_headers)
        self.assertEqual(headers["Authorization"], "Bearer sk_test_****")

    def test_el_envio_queda_registrado_en_el_log_edi(self):
        move = self.make_move("fe")
        self.route_emission(self.emission_response())
        move.action_send_edi()
        log = self.env["l10n_py.edi.log"].search(
            [("document_id", "=", move.id), ("operation_type", "=", "send")]
        )
        self.assertEqual(len(log), 1)
        self.assertEqual(log.status_code, 202)
        self.assertEqual(log.cdc, CDC)
        self.assertTrue(log.success)

    def test_los_fallos_http_quedan_registrados_como_error(self):
        move = self.make_move("fe")
        self.route_emission(FakeResponse(401, {"error": "Invalid or expired API key"}))
        move.action_send_edi()
        log = self.env["l10n_py.edi.log"].search([("document_id", "=", move.id)])
        self.assertFalse(log.success)
        self.assertTrue(log.error)

    # === Catálogo de enumeraciones ===

    def test_el_catalogo_se_cachea_entre_documentos(self):
        self.route_emission(self.emission_response())
        self.make_move("fe").action_send_edi()
        self.make_move("fe").action_send_edi()
        self.assertEqual(len(self.fake.calls_to("GET", "/public/enums$")), 1)

    def test_el_catalogo_se_renueva_a_las_24_horas(self):
        self.route_emission(self.emission_response())
        now = [1000.0]
        with patch.object(edi_connector.time, "monotonic", side_effect=lambda: now[0]):
            self.make_move("fe").action_send_edi()
            now[0] += client.ENUM_CACHE_TTL - 1
            self.make_move("fe").action_send_edi()
            self.assertEqual(len(self.fake.calls_to("GET", "/public/enums$")), 1)
            now[0] += 2
            self.make_move("fe").action_send_edi()
        self.assertEqual(len(self.fake.calls_to("GET", "/public/enums$")), 2)

    def test_el_catalogo_no_lleva_credenciales(self):
        self.connector._sifende_client().enums()
        call = self.fake.calls_to("GET", "/public/enums$")[0]
        self.assertNotIn("Authorization", call.headers)

    def test_valor_ausente_del_catalogo(self):
        self.enums["unidadMedida"] = []
        move = self.make_move("fe")
        self.route_emission(self.emission_response())
        move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "error")
        self.assertIn("unidadMedida", move.l10n_py_edi_message)

    # === Instalación ===

    def test_cron_de_estado_cada_cinco_minutos(self):
        cron = self.env.ref("l10n_py_edi_sifende.ir_cron_sifende_check_status")
        self.assertEqual((cron.interval_number, cron.interval_type), (5, "minutes"))
        self.assertEqual(cron.code, "model._cron_sifende_check_status()")

    def test_mask_key(self):
        self.assertEqual(edi_connector.mask_key(API_KEY), "sk_test_****")
        self.assertEqual(edi_connector.mask_key("sinprefijo"), "****")
        self.assertEqual(edi_connector.mask_key(False), "")
