# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import requests

from odoo.exceptions import UserError
from odoo.tests import tagged

from .common import FakeResponse, SifendeCommon, problem

SECRET = "whsec_8Kq2m5N0vXrT1bYc3LdWz9AeJfHpU4sG"
NEW_SECRET = "whsec_Zx9y8W7v6U5t4S3r2Q1p0O9n8M7l6K5j"
EVENTS = ["documento.aprobado", "documento.rechazado", "documento.cancelado"]


def endpoint(
    webhook_id=42, url="https://erp.example.com.py/l10n_py_edi_sifende/webhook/1"
):
    return {
        "id": webhook_id,
        "url": url,
        "ambiente": "DEV",
        "eventos": EVENTS,
        "activo": True,
    }


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestWebhookAdmin(SifendeCommon):
    def setUp(self):
        super().setUp()
        self.env["ir.config_parameter"].sudo().set_param(
            "web.base.url", "https://erp.example.com.py"
        )
        self.url = f"https://erp.example.com.py/l10n_py_edi_sifende/webhook/{self.connector.id}"
        self.fake.add("GET", r"^/contribuyente/webhooks$", FakeResponse(200, []))

    def notification(self, action):
        self.assertEqual(action["tag"], "display_notification")
        return action["params"]

    def registered(self, secret=SECRET):
        self.connector.write(
            {"sifende_webhook_id": 42, "sifende_webhook_secret": secret}
        )

    def test_la_url_publica_se_arma_con_la_url_base(self):
        self.assertEqual(self.connector.sifende_webhook_url, self.url)

    def test_registrar_crea_el_webhook_y_guarda_el_secreto(self):
        self.fake.add(
            "POST",
            r"^/contribuyente/webhooks$",
            FakeResponse(201, {"endpoint": endpoint(url=self.url), "secreto": SECRET}),
        )
        params = self.notification(self.connector.action_sifende_register_webhook())
        self.assertEqual(params["type"], "success")
        self.assertEqual(self.connector.sifende_webhook_id, 42)
        self.assertEqual(self.connector.sifende_webhook_secret, SECRET)
        call = self.fake.calls_to("POST", r"^/contribuyente/webhooks$")[0]
        self.assertEqual(call.json, {"url": self.url, "eventos": EVENTS})
        self.assertNotIn("Idempotency-Key", call.headers)

    def test_el_secreto_no_queda_en_el_log(self):
        self.fake.add(
            "POST",
            r"^/contribuyente/webhooks$",
            FakeResponse(201, {"endpoint": endpoint(url=self.url), "secreto": SECRET}),
        )
        self.connector.action_sifende_register_webhook()
        logs = self.env["l10n_py.edi.log"].search([("operation_type", "=", "event")])
        self.assertTrue(logs)
        for log in logs:
            self.assertNotIn(SECRET, log.response_data or "")
            self.assertNotIn(SECRET, log.request_data or "")

    def test_registrar_exige_https_y_un_host_publico(self):
        for base_url in (
            "http://erp.example.com.py",
            "https://localhost:8069",
            "https://127.0.0.1",
            "http://localhost:8069",
            "",
        ):
            with self.subTest(base_url=base_url):
                self.env["ir.config_parameter"].sudo().set_param(
                    "web.base.url", base_url
                )
                with self.assertRaisesRegex(UserError, "HTTPS"):
                    self.connector.action_sifende_register_webhook()
        self.assertFalse(self.fake.calls)

    def test_registrar_informa_si_la_url_ya_esta_registrada_sin_secreto(self):
        self.fake.add(
            "GET",
            r"^/contribuyente/webhooks$",
            FakeResponse(
                200,
                [endpoint(7, "https://otra.example.com/hook"), endpoint(9, self.url)],
            ),
        )
        params = self.notification(self.connector.action_sifende_register_webhook())
        self.assertEqual(params["type"], "warning")
        self.assertIn("Rotar secreto", params["message"])
        self.assertEqual(self.connector.sifende_webhook_id, 9)
        self.assertFalse(self.connector.sifende_webhook_secret)
        self.assertFalse(self.fake.calls_to("POST", r"^/contribuyente/webhooks$"))

    def test_registrar_informa_si_ya_esta_registrado_con_secreto(self):
        self.registered()
        self.fake.add(
            "GET",
            r"^/contribuyente/webhooks$",
            FakeResponse(200, [endpoint(url=self.url)]),
        )
        params = self.notification(self.connector.action_sifende_register_webhook())
        self.assertIn("ya está registrado", params["message"])
        self.assertEqual(self.connector.sifende_webhook_secret, SECRET)
        self.assertFalse(self.fake.calls_to("POST", r"^/contribuyente/webhooks$"))

    def test_registrar_avisa_si_el_webhook_esta_desactivado_en_sifende(self):
        self.registered()
        self.fake.add(
            "GET",
            r"^/contribuyente/webhooks$",
            FakeResponse(200, [{**endpoint(url=self.url), "activo": False}]),
        )
        params = self.notification(self.connector.action_sifende_register_webhook())
        self.assertEqual(params["type"], "warning")
        self.assertTrue(params["sticky"])
        self.assertIn("desactivado", params["message"])
        self.assertNotIn("ya está registrado", params["message"])
        self.assertFalse(self.fake.calls_to("POST", r"^/contribuyente/webhooks$"))

    def test_registrar_muestra_el_error_de_la_api(self):
        self.fake.add(
            "POST",
            r"^/contribuyente/webhooks$",
            problem("validation-error", 400, "Ya hay cinco webhooks activos"),
        )
        with self.assertRaisesRegex(UserError, "cinco webhooks"):
            self.connector.action_sifende_register_webhook()
        self.assertFalse(self.connector.sifende_webhook_id)

    def test_registrar_sin_conexion_avisa(self):
        self.fake.add("GET", r"^/contribuyente/webhooks$", requests.ConnectionError())
        with self.assertRaisesRegex(UserError, "No se pudo contactar"):
            self.connector.action_sifende_register_webhook()

    def test_rotar_guarda_el_secreto_nuevo(self):
        self.registered()
        self.fake.add(
            "POST",
            r"^/contribuyente/webhooks/42/rotar$",
            FakeResponse(
                200, {"endpoint": endpoint(url=self.url), "secreto": NEW_SECRET}
            ),
        )
        params = self.notification(
            self.connector.action_sifende_rotate_webhook_secret()
        )
        self.assertEqual(params["type"], "success")
        self.assertEqual(self.connector.sifende_webhook_secret, NEW_SECRET)
        self.assertEqual(self.connector.sifende_webhook_id, 42)
        call = self.fake.calls_to("POST", "/rotar")[0]
        self.assertNotIn("Idempotency-Key", call.headers)

    def test_rotar_sin_webhook_registrado_falla(self):
        with self.assertRaisesRegex(UserError, "no tiene un webhook"):
            self.connector.action_sifende_rotate_webhook_secret()

    def test_rotar_un_webhook_inexistente_limpia_el_conector_sin_excepcion(self):
        self.registered()
        self.fake.add(
            "POST", r"/rotar$", problem("webhook-not-found", 404, "No existe")
        )
        params = self.notification(
            self.connector.action_sifende_rotate_webhook_secret()
        )
        self.assertEqual(params["type"], "warning")
        self.assertIn("ya no existe", params["message"])
        self.assertFalse(self.connector.sifende_webhook_id)
        self.assertFalse(self.connector.sifende_webhook_secret)

    def test_quitar_elimina_el_webhook_y_limpia_el_conector(self):
        self.registered()
        self.fake.add("DELETE", r"^/contribuyente/webhooks/42$", FakeResponse(204))
        params = self.notification(self.connector.action_sifende_remove_webhook())
        self.assertEqual(params["type"], "success")
        self.assertFalse(self.connector.sifende_webhook_id)
        self.assertFalse(self.connector.sifende_webhook_secret)
        call = self.fake.calls_to("DELETE", "/webhooks/42")[0]
        self.assertNotIn("Idempotency-Key", call.headers)

    def test_quitar_un_webhook_ya_eliminado_limpia_el_conector(self):
        self.registered()
        self.fake.add("DELETE", r"/webhooks/42$", problem("webhook-not-found", 404))
        self.connector.action_sifende_remove_webhook()
        self.assertFalse(self.connector.sifende_webhook_id)

    def test_quitar_conserva_el_webhook_si_la_api_falla(self):
        self.registered()
        self.fake.add(
            "DELETE", r"/webhooks/42$", problem("internal-error", 500, "Falló")
        )
        with self.assertRaisesRegex(UserError, "Falló"):
            self.connector.action_sifende_remove_webhook()
        self.assertEqual(self.connector.sifende_webhook_id, 42)
        self.assertEqual(self.connector.sifende_webhook_secret, SECRET)

    def test_las_acciones_exigen_un_conector_de_sifende(self):
        self.env.cr.execute(
            "UPDATE l10n_py_edi_connector SET provider_type = 'otro' WHERE id = %s",
            [self.connector.id],
        )
        self.connector.invalidate_recordset()
        with self.assertRaisesRegex(UserError, "no es de Sifende"):
            self.connector.action_sifende_register_webhook()
