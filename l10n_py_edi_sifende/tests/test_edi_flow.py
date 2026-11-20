# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import base64
from datetime import timedelta

import requests

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tools import mute_logger

from .common import API_KEY, CDC, QR_URL, STAMP, FakeResponse, SifendeCommon, problem

XML = b'<?xml version="1.0"?><rDE><DE Id="' + CDC.encode() + b'"/></rDE>'
PDF = b"%PDF-1.4 kude"


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestEdiFlow(SifendeCommon):
    def route_files(self, kude=None):
        self.fake.add(
            "GET",
            rf"/documento-electronico/{CDC}/xml$",
            FakeResponse(200, content=XML, headers={"Content-Type": "application/xml"}),
        )
        self.fake.add(
            "GET",
            rf"/documento-electronico/{CDC}/kude$",
            *(
                kude
                or [
                    FakeResponse(
                        200, content=PDF, headers={"Content-Type": "application/pdf"}
                    )
                ]
            ),
        )

    def route_status(self, *responses):
        self.fake.add("GET", rf"/documento-electronico/status/{CDC}$", *responses)

    def sent_move(self, **vals):
        move = self.make_move("fe", **vals)
        self.route_emission(self.emission_response())
        move.action_send_edi()
        return move

    def run_cron(self):
        self.env["account.move"]._cron_sifende_check_status()

    # === Emisión ===

    def test_envio_deja_el_documento_en_procesamiento(self):
        move = self.sent_move()
        self.assertEqual(move.l10n_py_edi_status, "processing")
        self.assertEqual(move.l10n_py_cdc, CDC)
        self.assertEqual(move.l10n_py_qr_string, QR_URL)
        self.assertFalse(move.l10n_py_edi_batch_id)
        self.assertTrue(move.l10n_py_qr_code)
        self.assertFalse(move.l10n_py_kude_pdf)
        self.assertFalse(move.l10n_py_edi_xml)

    def test_envio_usa_api_key_e_idempotency_key(self):
        move = self.sent_move()
        call = self.fake.calls_to("POST", "^/documento-electronico$")[0]
        database = self.env["ir.config_parameter"].sudo().get_param("database.uuid")
        self.assertEqual(call.headers["Authorization"], f"Bearer {API_KEY}")
        self.assertEqual(
            call.headers["Idempotency-Key"], f"odoo:{database}:{move.id}:0"
        )
        self.assertTrue(call.url.startswith("https://api.sifende.com.py/api/v1/"))

    def test_flujo_asincronico_completo(self):
        move = self.sent_move()
        self.route_status(
            self.status_response("PENDIENTE"), self.status_response("EN_LOTE")
        )
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "processing")
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "processing")

        self.route_status(self.status_response("APROBADO", protocoloAutorizacion="987"))
        self.route_files()
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        self.assertEqual(base64.b64decode(move.l10n_py_edi_xml), XML)
        self.assertEqual(move.l10n_py_edi_xml_filename, f"{CDC}.xml")
        self.assertEqual(base64.b64decode(move.l10n_py_kude_pdf), PDF)
        self.assertEqual(move.l10n_py_kude_filename, f"KUDE_{CDC}.pdf")
        self.assertFalse(move.l10n_py_sifende_archivos_pendientes)

    def test_aprobado_con_observacion_guarda_las_observaciones(self):
        move = self.sent_move()
        self.route_status(
            self.status_response(
                "APROBADO_OBSERVACION", mensajeRechazo="1500 - Observación X"
            )
        )
        self.route_files()
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        self.assertIn("Observación X", move.l10n_py_edi_message)

    def test_kude_en_preparacion_respeta_retry_after(self):
        move = self.accepted_move()
        pending = FakeResponse(
            202, {"estado": "PENDIENTE"}, headers={"Retry-After": "7"}
        )
        self.route_files(
            kude=[
                pending,
                FakeResponse(
                    200, content=PDF, headers={"Content-Type": "application/pdf"}
                ),
            ]
        )
        move.action_download_kude()
        self.sleep.assert_called_with(7)
        kude_calls = self.fake.calls_to("GET", "/kude$")
        self.assertEqual(len(kude_calls), 2)
        self.assertIsNone(kude_calls[0].params)
        self.assertEqual(kude_calls[1].params, {"soloConsulta": "true"})
        self.assertEqual(base64.b64decode(move.l10n_py_kude_pdf), PDF)

    def test_kude_que_no_termina_queda_pendiente_y_se_reintenta(self):
        move = self.sent_move()
        self.route_status(self.status_response("APROBADO"))
        pending = FakeResponse(
            202, {"estado": "PENDIENTE"}, headers={"Retry-After": "10"}
        )
        self.route_files(kude=[pending])
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        self.assertTrue(move.l10n_py_edi_xml)
        self.assertFalse(move.l10n_py_kude_pdf)
        self.assertTrue(move.l10n_py_sifende_archivos_pendientes)

        self.route_files()
        self.run_cron()
        self.assertTrue(move.l10n_py_kude_pdf)
        self.assertFalse(move.l10n_py_sifende_archivos_pendientes)

    def test_xml_sin_generar_deja_la_factura_aceptada_y_pendiente(self):
        move = self.sent_move()
        self.route_status(self.status_response("APROBADO"))
        self.fake.add(
            "GET",
            rf"/documento-electronico/{CDC}/xml$",
            problem("documento-electronico-generation-error", 409),
        )
        self.fake.add(
            "GET",
            rf"/documento-electronico/{CDC}/kude$",
            FakeResponse(200, content=PDF, headers={"Content-Type": "application/pdf"}),
        )
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        self.assertFalse(move.l10n_py_edi_xml)
        self.assertTrue(move.l10n_py_sifende_archivos_pendientes)

    def test_rechazo_de_sifen(self):
        move = self.sent_move()
        self.route_status(
            self.status_response("RECHAZADO", mensajeRechazo="1001 - CDC duplicado")
        )
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "rejected")
        self.assertIn("1001 - CDC duplicado", move.l10n_py_edi_message)
        self.assertFalse(move.l10n_py_kude_pdf)

    def test_estado_error_no_reintenta_solo(self):
        move = self.sent_move()
        self.route_status(self.status_response("ERROR"))
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "error")
        self.run_cron()
        self.assertEqual(len(self.fake.calls_to("GET", "/status/")), 1)

    def test_check_status_es_compatible_con_el_cron_base(self):
        self.route_status(
            self.status_response("APROBADO"),
            self.status_response("RECHAZADO", mensajeRechazo="falló"),
            self.status_response("PENDIENTE"),
        )
        approved = self.connector.check_status(CDC)
        self.assertTrue(approved["success"])
        self.assertEqual(approved["result"]["status"], "Aprobado")
        rejected = self.connector.check_status(CDC)
        self.assertFalse(rejected["success"])
        self.assertEqual(rejected["result"]["status"], "Rechazado")
        pending = self.connector.check_status(CDC)
        self.assertFalse(pending["success"])
        self.assertNotIn("status", pending["result"])

    def test_un_fallo_de_consulta_no_cambia_el_estado(self):
        move = self.sent_move()
        self.route_status(requests.Timeout())
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "processing")

    # === Reintentos e idempotencia ===

    def test_timeout_reintenta_con_la_misma_clave(self):
        move = self.make_move("fe")
        self.route_emission(
            requests.Timeout(),
            requests.Timeout(),
            requests.Timeout(),
            self.emission_response(),
        )
        move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "error")
        self.assertTrue(move.l10n_py_sifende_reintento_misma_clave)
        self.assertIn("misma clave", move.l10n_py_edi_message)
        self.assertEqual(len(self.fake.calls_to("POST", "^/documento-electronico$")), 3)

        move.action_retry_edi()
        self.assertEqual(move.l10n_py_edi_status, "processing")
        self.assertEqual(move.l10n_py_sifende_intento, 0)
        keys = {
            c.headers["Idempotency-Key"]
            for c in self.fake.calls_to("POST", "^/documento-electronico$")
        }
        self.assertEqual(len(keys), 1)

    def test_5xx_reintenta_con_la_misma_clave_y_se_recupera(self):
        move = self.make_move("fe")
        self.route_emission(problem("internal-error", 503), self.emission_response())
        move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "processing")
        calls = self.fake.calls_to("POST", "^/documento-electronico$")
        self.assertEqual(len(calls), 2)
        self.assertEqual(
            calls[0].headers["Idempotency-Key"], calls[1].headers["Idempotency-Key"]
        )
        self.sleep.assert_called()

    def test_idempotency_in_progress_se_reintenta(self):
        move = self.make_move("fe")
        self.route_emission(
            FakeResponse(
                409,
                {
                    "type": "https://sifende.com.py/docs/solucion-problemas/idempotency-in-progress"
                },
                headers={"Retry-After": "3"},
            ),
            self.emission_response(),
        )
        move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "processing")
        self.sleep.assert_called_with(3)

    def test_cinco_hundred_persistente_deja_error_transitorio(self):
        move = self.make_move("fe")
        self.route_emission(problem("internal-error", 500))
        move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "error")
        self.assertTrue(move.l10n_py_sifende_reintento_misma_clave)

    def test_correccion_tras_rechazo_usa_clave_nueva(self):
        move = self.make_move("fe")
        self.route_emission(
            problem(
                "validation-error",
                400,
                "La solicitud contiene 1 error(es) de validación",
                errores={"receptor.direccion": "Dirección obligatoria"},
            ),
            self.emission_response(),
        )
        move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "rejected")
        self.assertIn(
            "receptor.direccion: Dirección obligatoria", move.l10n_py_edi_message
        )
        self.assertFalse(move.l10n_py_sifende_reintento_misma_clave)

        move.action_retry_edi()
        self.assertEqual(move.l10n_py_sifende_intento, 1)
        self.assertEqual(move.l10n_py_edi_status, "processing")
        database = self.env["ir.config_parameter"].sudo().get_param("database.uuid")
        keys = [
            c.headers["Idempotency-Key"]
            for c in self.fake.calls_to("POST", "^/documento-electronico$")
        ]
        self.assertEqual(
            keys, [f"odoo:{database}:{move.id}:0", f"odoo:{database}:{move.id}:1"]
        )

    def test_un_rechazo_de_sifen_no_se_reintenta_y_guia_a_la_inutilizacion(self):
        move = self.sent_move()
        self.route_status(
            self.status_response("RECHAZADO", mensajeRechazo="1001 - CDC duplicado")
        )
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "rejected")
        self.assertIn("1001 - CDC duplicado", move.l10n_py_edi_message)
        self.assertIn("Inutilización de números", move.l10n_py_edi_message)
        self.assertIn("Restablecer a borrador", move.l10n_py_edi_message)

        with self.assertRaisesRegex(UserError, "no se puede reenviar"):
            move.action_retry_edi()
        self.assertEqual(move.l10n_py_sifende_intento, 0)
        self.assertEqual(len(self.fake.calls_to("POST", "^/documento-electronico$")), 1)

    def failed_move(self):
        move = self.sent_move()
        self.route_status(self.status_response("ERROR"))
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "error")
        return move

    def test_un_error_de_sifende_no_se_reemite_y_guia_al_panel(self):
        move = self.failed_move()
        self.assertTrue(move.l10n_py_sifende_envio_fallido)
        self.assertIn("panel de Sifende", move.l10n_py_edi_message)
        self.assertIn("mismo CDC", move.l10n_py_edi_message)

        for action in (move.action_retry_edi, move.action_send_edi):
            with self.assertRaisesRegex(UserError, "panel de Sifende"):
                action()
        self.assertEqual(move.l10n_py_sifende_intento, 0)
        self.assertEqual(move.l10n_py_edi_status, "error")
        self.assertEqual(len(self.fake.calls_to("POST", "^/documento-electronico$")), 1)

    def test_un_error_de_sifende_se_recupera_cuando_el_lote_se_reintenta(self):
        move = self.failed_move()
        move.l10n_py_sifende_ultima_consulta = fields.Datetime.now() - timedelta(
            hours=2
        )
        self.route_status(self.status_response("EN_LOTE"))
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "processing")
        self.assertFalse(move.l10n_py_sifende_envio_fallido)

        self.route_status(self.status_response("APROBADO"))
        self.route_files()
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        self.assertFalse(move.l10n_py_sifende_envio_fallido)

    def test_el_error_transitorio_se_reintenta_con_la_misma_clave(self):
        move = self.make_move("fe")
        self.route_emission(
            *[problem("internal-error", 500)] * 3, self.emission_response()
        )
        move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "error")
        self.assertFalse(move.l10n_py_sifende_envio_fallido)

        move.action_retry_edi()
        self.assertEqual(move.l10n_py_edi_status, "processing")
        self.assertEqual(move.l10n_py_sifende_intento, 0)
        keys = {
            c.headers["Idempotency-Key"]
            for c in self.fake.calls_to("POST", "^/documento-electronico$")
        }
        self.assertEqual(len(keys), 1)

    # === Errores del envío ===

    def test_numero_en_uso_informa_el_cdc_existente(self):
        move = self.make_move("fe")
        self.route_emission(
            problem("document-number-in-use", 409, "Número en uso", cdc=CDC)
        )
        move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "error")
        self.assertIn(CDC, move.l10n_py_edi_message)
        self.assertIn("en uso", move.l10n_py_edi_message)
        self.assertFalse(move.l10n_py_sifende_reintento_misma_clave)

    def test_numero_inutilizado(self):
        move = self.make_move("fe")
        self.route_emission(
            problem("document-number-voided", 409, "Número inutilizado")
        )
        move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "error")
        self.assertIn("inutilizado", move.l10n_py_edi_message)

    def test_timbrado_distinto(self):
        move = self.make_move("fe")
        self.route_emission(
            problem("timbrado-mismatch", 422, "Timbrado esperado 87654321")
        )
        move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "error")
        self.assertIn("timbrado", move.l10n_py_edi_message.lower())
        self.assertIn("87654321", move.l10n_py_edi_message)

    def test_los_errores_de_configuracion_de_sifende_no_son_un_rechazo(self):
        for slug, hint in (
            ("configuracion-incompleta", "configuración del contribuyente"),
            ("timbrado-no-vigente", "timbrado no está vigente"),
            ("certificado-no-vigente", "certificado digital"),
            ("idempotency-key-reused", "clave nueva"),
        ):
            with self.subTest(slug=slug):
                move = self.make_move("fe")
                self.route_emission(
                    problem(slug, 422, "Detalle de Sifende"), self.emission_response()
                )
                move.action_send_edi()
                self.assertEqual(move.l10n_py_edi_status, "error")
                self.assertIn(hint, move.l10n_py_edi_message)
                self.assertIn("Detalle de Sifende", move.l10n_py_edi_message)
                move.action_retry_edi()
                self.assertEqual(move.l10n_py_edi_status, "processing")
                self.assertEqual(move.l10n_py_sifende_intento, 1)

    def test_numero_de_un_rechazado_requiere_inutilizar(self):
        move = self.make_move("fe")
        self.route_emission(problem("document-number-requires-voiding", 422))
        move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "rejected")
        self.assertIn("Inutilización de números", move.l10n_py_edi_message)

    def test_cupo_agotado_enlaza_la_facturacion(self):
        move = self.make_move("fe")
        self.route_emission(problem("document-quota-exceeded", 403, "Cupo agotado"))
        move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "error")
        self.assertIn("https://app.sifende.com.py", move.l10n_py_edi_message)

    def test_api_key_invalida(self):
        move = self.make_move("fe")
        self.route_emission(FakeResponse(401, {"error": "Invalid or expired API key"}))
        move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "error")
        self.assertIn("API key", move.l10n_py_edi_message)

    def test_sin_api_key(self):
        self.connector.sifende_api_key = False
        move = self.make_move("fe")
        move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "error")
        self.assertIn("API key", move.l10n_py_edi_message)
        self.assertFalse(self.fake.calls_to("POST", "^/documento-electronico$"))

    def test_asistente_de_envio_avisa_si_sifende_no_acepto(self):
        move = self.make_move("fe")
        self.route_emission(problem("document-number-in-use", 409, cdc=CDC))
        wizard = self.env["account.move.send.edi.wizard"].create(
            {"invoice_id": move.id}
        )
        params = wizard.action_send()["params"]
        self.assertEqual(params["type"], "danger")
        self.assertIn(CDC, params["message"])

    def test_asistente_de_envio_mantiene_el_aviso_de_oca_si_todo_sale_bien(self):
        move = self.make_move("fe")
        self.route_emission(self.emission_response())
        wizard = self.env["account.move.send.edi.wizard"].create(
            {"invoice_id": move.id}
        )
        self.assertEqual(wizard.action_send()["params"]["type"], "success")

    # === Cancelación e inutilización ===

    def accepted_move(self):
        move = self.make_move("fe", invoice_date=fields.Date.today())
        move.write({"l10n_py_edi_status": "accepted", "l10n_py_cdc": CDC})
        return move

    def test_cancelacion_desde_el_asistente_envia_el_motivo(self):
        move = self.accepted_move()
        self.fake.add(
            "POST",
            rf"/documento-electronico/{CDC}/cancelar$",
            FakeResponse(
                200, {"estadoEvento": "APROBADO", "tipoEvento": "CANCELACION"}
            ),
        )
        wizard = self.env["l10n_py.edi.cancel.wizard"].create(
            {"invoice_id": move.id, "motive": "Error en el monto facturado"}
        )
        wizard.action_cancel()
        self.assertEqual(move.l10n_py_edi_status, "cancelled")
        call = self.fake.calls_to("POST", "/cancelar$")[0]
        self.assertEqual(call.json, {"motivo": "Error en el monto facturado"})
        self.assertTrue(call.headers["Idempotency-Key"])

    def test_cancelacion_directa_usa_un_motivo_por_defecto(self):
        move = self.accepted_move()
        self.fake.add(
            "POST", "/cancelar$", FakeResponse(200, {"estadoEvento": "APROBADO"})
        )
        move.action_cancel_edi()
        self.assertEqual(
            self.fake.calls_to("POST", "/cancelar$")[0].json,
            {"motivo": "Cancelación solicitada desde Odoo"},
        )

    def test_cancelacion_rechazada(self):
        move = self.accepted_move()
        self.fake.add(
            "POST",
            "/cancelar$",
            problem("evento-cancelacion-error", 409, "Plazo vencido"),
        )
        with self.assertRaisesRegex(UserError, "Plazo vencido"):
            move.action_cancel_edi()
        self.assertEqual(move.l10n_py_edi_status, "accepted")

    def test_inutilizacion(self):
        inutilization = self.env["l10n_py.number.inutilization"].create(
            {
                "authorization_id": self.auths["fe"].id,
                "number_from": 5,
                "number_to": 7,
                "motive": "Números saltados por error de sistema",
            }
        )
        self.fake.add(
            "POST",
            "/inutilizar$",
            FakeResponse(200, {"estadoEvento": "APROBADO", "codigoRespuesta": "0600"}),
        )
        inutilization.action_send()
        self.assertEqual(inutilization.state, "accepted")
        self.assertEqual(
            self.fake.calls_to("POST", "/inutilizar$")[0].json,
            {
                "numeroTimbrado": int(STAMP),
                "establecimiento": "001",
                "puntoExpedicion": "001",
                "numeroInicio": "0000005",
                "numeroFin": "0000007",
                "tipoDocumento": 1,
                "motivo": "Números saltados por error de sistema",
            },
        )

    def test_inutilizacion_de_notas_de_credito_informa_su_tipo(self):
        inutilization = self.env["l10n_py.number.inutilization"].create(
            {
                "authorization_id": self.auths["nc"].id,
                "number_from": 5,
                "number_to": 5,
                "motive": "Número saltado por error de sistema",
            }
        )
        self.fake.add(
            "POST", "/inutilizar$", FakeResponse(200, {"estadoEvento": "APROBADO"})
        )
        inutilization.action_send()
        self.assertEqual(
            self.fake.calls_to("POST", "/inutilizar$")[0].json["tipoDocumento"], 5
        )

    def test_inutilizacion_rechazada(self):
        inutilization = self.env["l10n_py.number.inutilization"].create(
            {
                "authorization_id": self.auths["fe"].id,
                "number_from": 5,
                "number_to": 7,
                "motive": "Números saltados por error de sistema",
            }
        )
        self.fake.add(
            "POST",
            "/inutilizar$",
            problem("evento-inutilizacion-error", 409, "Rango en uso"),
        )
        with (
            mute_logger(
                "odoo.addons.l10n_py_edi_base.models.l10n_py_number_inutilization"
            ),
            self.assertRaisesRegex(UserError, "Rango en uso"),
        ):
            inutilization.action_send()
        self.assertEqual(inutilization.state, "rejected")

    # === Vista previa ===

    def test_vista_previa_no_esta_disponible(self):
        move = self.make_move("fe")
        with self.assertRaisesRegex(UserError, "vista previa"):
            move.action_preview_xml()
        with self.assertRaisesRegex(UserError, "vista previa"):
            move.action_l10n_py_preview_qr()
        self.assertFalse(self.fake.calls_to("POST", ".*"))
