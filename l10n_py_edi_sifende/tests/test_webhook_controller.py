# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import base64
import hashlib
import hmac
import json
import time
import uuid
from datetime import timedelta
from unittest.mock import patch

import requests

from odoo import fields
from odoo.tests import HttpCase, tagged

from .common import CDC, FakeResponse, SifendeCommon
from .test_edi_flow import PDF, XML

SECRET = "whsec_8Kq2m5N0vXrT1bYc3LdWz9AeJfHpU4sG"
OTHER_CDC = "01800123451001001000000132026042710000000007"


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestWebhookController(SifendeCommon, HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.connector.sifende_webhook_secret = SECRET

    def setUp(self):
        super().setUp()
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
        self.route_status("APROBADO")

    def route_status(self, *states, **extra):
        self.fake.add(
            "GET",
            rf"/documento-electronico/status/{CDC}$",
            *(self.status_response(state, **extra) for state in states),
        )

    def processing_move(self, **vals):
        move = self.make_move("fe", **vals)
        self.route_emission(self.emission_response())
        move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "processing")
        return move

    @staticmethod
    def sign(body, secret=SECRET, event_id="e", delivery_id="d", timestamp=None):
        message = f"{event_id}.{delivery_id}.{timestamp}.".encode() + body
        digest = hmac.new(secret.encode(), message, hashlib.sha256).digest()
        return "v1=" + base64.b64encode(digest).decode()

    def post(
        self,
        event_type="documento.aprobado",
        connector=None,
        secret=SECRET,
        event_id=None,
        timestamp=None,
        signature=None,
        body=None,
        headers=None,
        **data,
    ):
        connector = connector or self.connector
        event_id = event_id or str(uuid.uuid4())
        delivery_id = str(uuid.uuid4())
        timestamp = str(int(time.time()) if timestamp is None else timestamp)
        if body is None:
            body = json.dumps(
                {
                    "id": event_id,
                    "tipo": event_type,
                    "version": "1",
                    "data": {
                        "cdc": CDC,
                        "estado": "APROBADO",
                        "resultados": [],
                        **data,
                    },
                }
            ).encode()
        request_headers = {
            "Content-Type": "application/json",
            "X-Sifende-Event-Id": event_id,
            "X-Sifende-Event-Type": event_type,
            "X-Sifende-Delivery-Id": delivery_id,
            "X-Sifende-Timestamp": timestamp,
            "X-Sifende-Signature": signature
            or self.sign(body, secret, event_id, delivery_id, timestamp),
            **(headers or {}),
        }
        return self.url_open(
            f"/l10n_py_edi_sifende/webhook/{connector.id}",
            data=body,
            headers={k: v for k, v in request_headers.items() if v is not None},
        )

    def events(self):
        return self.env["l10n_py.sifende.webhook.event"].search([])

    # === Eventos de documento ===

    def test_aprobado_acepta_y_descarga_xml_y_kude(self):
        move = self.processing_move()
        response = self.post("documento.aprobado")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        self.assertEqual(base64.b64decode(move.l10n_py_edi_xml), XML)
        self.assertEqual(base64.b64decode(move.l10n_py_kude_pdf), PDF)
        mimetypes = self.env["ir.attachment"].search(
            [("res_model", "=", "account.move"), ("res_id", "=", move.id)]
        )
        self.assertEqual(
            {a.name: a.mimetype for a in mimetypes}[f"{CDC}.xml"], "application/xml"
        )
        self.assertFalse(move.l10n_py_sifende_archivos_pendientes)
        self.assertEqual(len(self.fake.calls_to("GET", "/status/")), 1)

    def test_aprobado_con_observacion_guarda_los_mensajes(self):
        move = self.processing_move()
        self.route_status("APROBADO_OBSERVACION")
        self.post(
            estado="APROBADO_OBSERVACION",
            resultados=[{"codigo": "0301", "mensaje": "Observación de SIFEN"}],
        )
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        self.assertEqual(move.l10n_py_edi_message, "0301: Observación de SIFEN")

    def test_rechazado_deja_los_mensajes_de_sifen(self):
        move = self.processing_move()
        self.route_status("RECHAZADO")
        response = self.post(
            "documento.rechazado",
            estado="RECHAZADO",
            resultados=[
                {"codigo": "1001", "mensaje": "CDC duplicado"},
                {"codigo": "1002", "mensaje": "Otro error"},
            ],
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(move.l10n_py_edi_status, "rejected")
        self.assertTrue(
            move.l10n_py_edi_message.startswith("1001: CDC duplicado\n1002: Otro error")
        )
        self.assertIn("Inutilización de números", move.l10n_py_edi_message)
        self.assertFalse(move.l10n_py_kude_pdf)

    def test_cancelado_cancela_un_documento_aceptado(self):
        move = self.processing_move()
        self.post("documento.aprobado")
        self.route_status("CANCELADO")
        response = self.post("documento.cancelado", estado="CANCELADO")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(move.l10n_py_edi_status, "cancelled")

    def test_aprobado_tras_un_error_de_sifende_acepta_el_documento(self):
        move = self.processing_move()
        move.write(
            {"l10n_py_edi_status": "error", "l10n_py_sifende_envio_fallido": True}
        )
        response = self.post("documento.aprobado")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        self.assertFalse(move.l10n_py_sifende_envio_fallido)
        self.assertTrue(move.l10n_py_kude_pdf)

    def test_un_aviso_sobre_un_error_local_no_consulta_a_sifende(self):
        move = self.processing_move()
        move.l10n_py_edi_status = "error"
        self.post("documento.aprobado")
        self.assertEqual(move.l10n_py_edi_status, "error")
        self.assertFalse(self.fake.calls_to("GET", "/status/"))

    def test_un_rechazo_tardio_no_pisa_un_documento_aceptado(self):
        move = self.processing_move()
        self.post("documento.aprobado")
        self.post("documento.rechazado", estado="RECHAZADO")
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        self.assertEqual(len(self.fake.calls_to("GET", "/status/")), 1)

    def test_un_aviso_que_contradice_a_la_consulta_manda_la_consulta(self):
        move = self.processing_move()
        self.route_status("APROBADO")
        self.post("documento.rechazado", estado="RECHAZADO")
        self.assertEqual(move.l10n_py_edi_status, "accepted")

    def test_un_cancelado_antiguo_no_cancela_un_documento_vigente(self):
        move = self.processing_move()
        self.post("documento.aprobado")
        self.post("documento.cancelado", estado="CANCELADO")
        self.assertEqual(move.l10n_py_edi_status, "accepted")

    def test_sin_respuesta_a_la_consulta_el_documento_queda_para_el_cron(self):
        move = self.processing_move()
        self.fake.add(
            "GET", rf"/documento-electronico/status/{CDC}$", requests.Timeout()
        )
        self.assertEqual(self.post("documento.rechazado").status_code, 200)
        self.assertEqual(move.l10n_py_edi_status, "processing")
        self.route_status("RECHAZADO")
        self.env["account.move"]._cron_sifende_check_status()
        self.assertEqual(move.l10n_py_edi_status, "rejected")

    def test_kude_en_preparacion_queda_pendiente_para_el_cron(self):
        move = self.processing_move()
        self.fake.add(
            "GET",
            rf"/documento-electronico/{CDC}/kude$",
            FakeResponse(202, headers={"Retry-After": "5"}),
        )
        response = self.post("documento.aprobado")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        self.assertTrue(move.l10n_py_edi_xml)
        self.assertFalse(move.l10n_py_kude_pdf)
        self.assertTrue(move.l10n_py_sifende_archivos_pendientes)
        self.sleep.assert_not_called()
        self.fake.add(
            "GET",
            rf"/documento-electronico/{CDC}/kude$",
            FakeResponse(200, content=PDF, headers={"Content-Type": "application/pdf"}),
        )
        self.env["account.move"]._cron_sifende_check_status()
        self.assertTrue(move.l10n_py_kude_pdf)
        self.assertFalse(move.l10n_py_sifende_archivos_pendientes)

    # === Eventos sin acción ===

    def test_lote_procesado_y_tipos_desconocidos_responden_200_sin_accion(self):
        move = self.processing_move()
        for event_type in ("lote.procesado", "documento.inventado"):
            response = self.post(event_type)
            self.assertEqual(response.status_code, 200)
        self.assertEqual(move.l10n_py_edi_status, "processing")
        self.assertFalse(self.events())

    def test_cdc_desconocido_responde_200_sin_accion(self):
        move = self.processing_move()
        response = self.post(cdc=OTHER_CDC)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(move.l10n_py_edi_status, "processing")
        self.assertFalse(self.events())

    def test_el_cdc_de_otra_empresa_no_se_toca(self):
        move = self.processing_move()
        other_company = self.env["res.company"].create({"name": "Otra empresa"})
        other = self.env["l10n_py.edi.connector"].create(
            {
                "name": "Otro Sifende",
                "provider_type": "sifende",
                "company_id": other_company.id,
                "sifende_webhook_secret": "whsec_otra",
            }
        )
        response = self.post(connector=other, secret="whsec_otra")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(move.l10n_py_edi_status, "processing")
        self.assertFalse(self.events())
        self.assertEqual(self.post(connector=other).status_code, 401)

    # === Duplicados ===

    def test_un_evento_repetido_responde_200_y_no_se_reprocesa(self):
        move = self.processing_move()
        event_id = str(uuid.uuid4())
        self.assertEqual(self.post(event_id=event_id).status_code, 200)
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        move.l10n_py_edi_status = "processing"
        self.assertEqual(self.post(event_id=event_id).status_code, 200)
        self.assertEqual(move.l10n_py_edi_status, "processing")
        self.assertEqual(self.events().event_id, event_id)

    def test_eventos_distintos_se_procesan_cada_uno(self):
        move = self.processing_move()
        self.post(estado="APROBADO")
        move.l10n_py_edi_status = "processing"
        self.post(estado="APROBADO")
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        self.assertEqual(len(self.events()), 2)

    def test_los_eventos_viejos_se_limpian(self):
        self.processing_move()
        self.post()
        self.env.cr.execute(
            "UPDATE l10n_py_sifende_webhook_event SET create_date = %s",
            [fields.Datetime.now() - timedelta(days=8)],
        )
        self.events().invalidate_recordset()
        recent = self.env["l10n_py.sifende.webhook.event"].create(
            {"connector_id": self.connector.id, "event_id": "reciente"}
        )
        self.env["l10n_py.sifende.webhook.event"]._gc_processed_events()
        self.assertEqual(self.events(), recent)

    def test_un_error_propio_responde_500_y_el_reintento_se_procesa(self):
        move = self.processing_move()
        event_id = str(uuid.uuid4())
        with (
            patch.object(
                type(move),
                "_l10n_py_sifende_apply_webhook",
                side_effect=RuntimeError("falla transitoria"),
            ),
            self.assertLogs("odoo.addons.l10n_py_edi_sifende", "ERROR"),
        ):
            response = self.post(event_id=event_id)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(move.l10n_py_edi_status, "processing")
        self.assertFalse(self.events())
        self.assertEqual(self.post(event_id=event_id).status_code, 200)
        self.assertEqual(move.l10n_py_edi_status, "accepted")

    # === Autenticidad ===

    def test_firma_valida_con_varias_versiones_en_el_header(self):
        move = self.processing_move()
        event_id, delivery_id, timestamp = "e1", "d1", str(int(time.time()))
        body = json.dumps({"tipo": "documento.aprobado", "data": {"cdc": CDC}}).encode()
        good = self.sign(body, SECRET, event_id, delivery_id, timestamp)
        response = self.url_open(
            f"/l10n_py_edi_sifende/webhook/{self.connector.id}",
            data=body,
            headers={
                "X-Sifende-Event-Id": event_id,
                "X-Sifende-Delivery-Id": delivery_id,
                "X-Sifende-Timestamp": timestamp,
                "X-Sifende-Signature": f"v1=AAAA, {good}",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(move.l10n_py_edi_status, "accepted")

    def assert_rejected(self, move, response):
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"")
        self.assertEqual(move.l10n_py_edi_status, "processing")
        self.assertFalse(self.events())

    def test_firma_invalida_responde_401_sin_detalles(self):
        move = self.processing_move()
        for signature in ("v1=AAAA", "v2=AAAA", "no-es-una-firma", "v1=%%%"):
            with self.subTest(signature=signature):
                self.assert_rejected(move, self.post(signature=signature))

    def test_secreto_equivocado_responde_401(self):
        move = self.processing_move()
        self.assert_rejected(move, self.post(secret="whsec_otro"))

    def test_cuerpo_alterado_responde_401(self):
        move = self.processing_move()
        body = json.dumps({"tipo": "documento.aprobado", "data": {"cdc": CDC}}).encode()
        timestamp = int(time.time())
        response = self.post(
            event_id="e1",
            timestamp=timestamp,
            body=body + b" ",
            signature=self.sign(body, SECRET, "e1", "d1", timestamp),
            headers={"X-Sifende-Delivery-Id": "d1"},
        )
        self.assert_rejected(move, response)

    def test_timestamp_fuera_de_la_ventana_responde_401(self):
        move = self.processing_move()
        for offset in (-301, 301, -3600):
            with self.subTest(offset=offset):
                response = self.post(timestamp=int(time.time()) + offset)
                self.assert_rejected(move, response)

    def test_timestamp_dentro_de_la_ventana_se_acepta(self):
        move = self.processing_move()
        self.assertEqual(self.post(timestamp=int(time.time()) - 240).status_code, 200)
        self.assertEqual(move.l10n_py_edi_status, "accepted")

    def test_headers_faltantes_o_timestamp_invalido_responden_401(self):
        move = self.processing_move()
        for name in (
            "X-Sifende-Event-Id",
            "X-Sifende-Delivery-Id",
            "X-Sifende-Timestamp",
            "X-Sifende-Signature",
        ):
            with self.subTest(missing=name):
                response = self.post(headers={name: None})
                self.assertEqual(response.status_code, 401)
        self.assert_rejected(move, self.post(timestamp="ayer"))

    def test_sin_secreto_configurado_responde_401(self):
        move = self.processing_move()
        self.connector.sifende_webhook_secret = False
        self.assert_rejected(move, self.post())

    def test_json_invalido_con_firma_valida_responde_400(self):
        response = self.post(body=b"no es json")
        self.assertEqual(response.status_code, 400)

    # === Conector ===

    def test_conector_inexistente_responde_404(self):
        response = self.url_open("/l10n_py_edi_sifende/webhook/999999", data=b"{}")
        self.assertEqual(response.status_code, 404)

    def test_conector_de_otro_proveedor_responde_404(self):
        self.env.cr.execute(
            "UPDATE l10n_py_edi_connector SET provider_type = 'otro' WHERE id = %s",
            [self.connector.id],
        )
        self.connector.invalidate_recordset()
        self.assertEqual(self.post().status_code, 404)

    def test_conector_archivado_responde_404(self):
        self.connector.active = False
        self.assertEqual(self.post().status_code, 404)

    def test_solo_acepta_post(self):
        url = f"/l10n_py_edi_sifende/webhook/{self.connector.id}"
        self.assertEqual(self.url_open(url).status_code, 405)
