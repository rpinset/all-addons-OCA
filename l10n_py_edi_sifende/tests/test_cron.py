# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from datetime import timedelta
from unittest.mock import patch

from odoo import fields
from odoo.tests import tagged

from odoo.addons.l10n_py_edi_sifende.models import account_move

from .common import API_KEY, FakeResponse, SifendeCommon

PDF = b"%PDF-1.4 kude"
XML = b"<rDE/>"


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestCron(SifendeCommon):
    def make_tracked(self, count, status="processing", days_ago=0, **vals):
        today = fields.Date.context_today(self.env["account.move"])
        today -= timedelta(days=days_ago)
        moves = self.env["account.move"]
        for index in range(count):
            move = self.make_move("fe", invoice_date=today)
            move.write(
                {
                    "l10n_py_edi_status": status,
                    "l10n_py_cdc": f"{index:04d}".rjust(44, "1"),
                    **vals,
                }
            )
            moves |= move
        return moves

    def route_status(self, move, state, **extra):
        self.fake.add(
            "GET",
            rf"/status/{move.l10n_py_cdc}$",
            self.status_response(state, cdc=move.l10n_py_cdc, **extra),
        )

    def route_files(self, move):
        for suffix, content, kind in (("xml", XML, "xml"), ("kude", PDF, "pdf")):
            self.fake.add(
                "GET",
                rf"/documento-electronico/{move.l10n_py_cdc}/{suffix}$",
                FakeResponse(
                    200,
                    content=content,
                    headers={"Content-Type": f"application/{kind}"},
                ),
            )

    def run_cron(self):
        self.env["account.move"]._cron_sifende_check_status()

    def queried(self):
        return [
            c.path.rsplit("/", 1)[-1] for c in self.fake.calls_to("GET", "/status/")
        ]

    # === Lote ===

    def test_el_cron_rota_por_todos_los_documentos_pendientes(self):
        moves = self.make_tracked(3)
        for move in moves:
            self.route_status(move, "PENDIENTE")
        with patch.object(account_move, "CRON_BATCH_SIZE", 2):
            self.run_cron()
            self.run_cron()
        self.assertEqual(set(self.queried()), set(moves.mapped("l10n_py_cdc")))

    def test_un_documento_que_falla_no_ocupa_siempre_su_lugar_en_el_lote(self):
        moves = self.make_tracked(3)
        for move in moves:
            self.route_status(move, "PENDIENTE")
        failing = moves[:2]
        original = type(moves)._l10n_py_sifende_sync

        def sync(record, connector, *args, **kwargs):
            if record in failing:
                raise ValueError("falla persistente")
            return original(record, connector, *args, **kwargs)

        with (
            patch.object(account_move, "CRON_BATCH_SIZE", 2),
            patch.object(type(moves), "_l10n_py_sifende_sync", sync),
            self.assertLogs("odoo.addons.l10n_py_edi_sifende", "ERROR"),
        ):
            self.run_cron()
            self.run_cron()
        self.assertEqual(self.queried(), [moves[2].l10n_py_cdc])
        self.assertTrue(all(moves.mapped("l10n_py_sifende_ultima_consulta")))

    def test_el_cron_para_al_agotar_su_presupuesto_de_tiempo(self):
        moves = self.make_tracked(2)
        with patch.object(account_move, "CRON_TIME_BUDGET", -1):
            self.run_cron()
        self.assertFalse(self.fake.calls)
        self.assertFalse(any(moves.mapped("l10n_py_sifende_ultima_consulta")))

    def test_el_cron_no_espera_el_kude(self):
        (move,) = self.make_tracked(1)
        self.route_status(move, "APROBADO")
        self.fake.add(
            "GET",
            rf"/documento-electronico/{move.l10n_py_cdc}/xml$",
            FakeResponse(200, content=XML, headers={"Content-Type": "application/xml"}),
        )
        self.fake.add(
            "GET",
            rf"/documento-electronico/{move.l10n_py_cdc}/kude$",
            FakeResponse(202, headers={"Retry-After": "5"}),
        )
        self.run_cron()
        self.sleep.assert_not_called()
        self.assertTrue(move.l10n_py_sifende_archivos_pendientes)

    def make_second_connector_move(self):
        company = self.env["res.company"].create(
            {
                "name": "Segunda Empresa Test",
                "country_id": self.country_py.id,
                "currency_id": self.env.ref("base.PYG").id,
            }
        )
        self.env["l10n_py.edi.connector"].create(
            {
                "name": "Sifende 2",
                "provider_type": "sifende",
                "environment": "test",
                "sifende_api_key": API_KEY,
                "company_id": company.id,
            }
        )
        (move,) = self.make_tracked(1)
        move.l10n_py_cdc = "9" * 44
        self.env.cr.execute(
            "UPDATE account_move SET company_id = %s WHERE id = %s",
            (company.id, move.id),
        )
        move.invalidate_recordset()
        return move

    def test_un_conector_con_mucho_trabajo_no_deja_sin_turno_a_los_demas(self):
        first = self.make_tracked(2)
        other = self.make_second_connector_move()
        clock = [0.0]

        def sync(record, connector, *args, **kwargs):
            clock[0] += 30

        with (
            patch.object(account_move.time, "monotonic", lambda: clock[0]),
            patch.object(type(first), "_l10n_py_sifende_sync", sync),
        ):
            self.run_cron()
            self.run_cron()
        self.assertTrue(other.l10n_py_sifende_ultima_consulta)

    def test_el_cron_respeta_el_limite_de_lote_de_cada_conector(self):
        first = self.make_tracked(3)
        other = self.make_second_connector_move()
        synced = []

        def sync(record, connector, *args, **kwargs):
            synced.append(record)

        with (
            patch.object(account_move, "CRON_BATCH_SIZE", 2),
            patch.object(type(first), "_l10n_py_sifende_sync", sync),
        ):
            self.run_cron()
        self.assertEqual(len(synced), 3)
        self.assertIn(other, synced)

    # === Prioridad ===

    def record_syncs(self, moves):
        synced = []

        def sync(record, connector, *args, **kwargs):
            synced.append(record)

        return synced, patch.object(type(moves), "_l10n_py_sifende_sync", sync)

    def test_los_documentos_en_curso_van_antes_que_los_aceptados_vigilados(self):
        # los aceptados nunca se consultaron, así que antes iban primero
        watched = self.make_tracked(2, status="accepted")
        in_flight = self.make_tracked(
            2,
            l10n_py_sifende_ultima_consulta=fields.Datetime.now()
            - timedelta(minutes=5),
        )
        synced, sync = self.record_syncs(watched)
        with patch.object(account_move, "CRON_BATCH_SIZE", 2), sync:
            self.run_cron()
        self.assertEqual(synced, list(in_flight))

    def test_los_aceptados_vigilados_ocupan_el_lugar_libre_del_lote(self):
        watched = self.make_tracked(2, status="accepted")
        (in_flight,) = self.make_tracked(1)
        synced, sync = self.record_syncs(watched)
        with patch.object(account_move, "CRON_BATCH_SIZE", 2), sync:
            self.run_cron()
        self.assertEqual(synced, [in_flight, watched[0]])

    def test_un_aceptado_sin_archivos_va_antes_que_los_vigilados(self):
        watched = self.make_tracked(1, status="accepted")
        # consultado hace un momento: solo entra por los archivos pendientes
        files = self.make_tracked(
            1,
            status="accepted",
            l10n_py_sifende_archivos_pendientes=True,
            l10n_py_sifende_ultima_consulta=fields.Datetime.now(),
        )
        synced, sync = self.record_syncs(watched)
        with patch.object(account_move, "CRON_BATCH_SIZE", 1), sync:
            self.run_cron()
        self.assertEqual(synced, list(files))

    def test_un_cancelado_con_archivos_pendientes_no_ocupa_el_lote(self):
        cancelled = self.make_tracked(
            1, status="cancelled", l10n_py_sifende_archivos_pendientes=True
        )
        synced, sync = self.record_syncs(cancelled)
        with sync:
            self.run_cron()
        self.assertFalse(synced)

    def test_un_error_de_sifende_va_antes_que_los_aceptados_vigilados(self):
        watched = self.make_tracked(1, status="accepted")
        failed = self.make_tracked(
            1, status="error", l10n_py_sifende_envio_fallido=True
        )
        synced, sync = self.record_syncs(watched)
        with patch.object(account_move, "CRON_BATCH_SIZE", 1), sync:
            self.run_cron()
        self.assertEqual(synced, list(failed))

    # === Cancelaciones ===

    def accepted_with_files(self, **vals):
        (move,) = self.make_tracked(1, status="accepted", **vals)
        move.write({"l10n_py_edi_xml": "WE1M", "l10n_py_kude_pdf": "UERG"})
        return move

    def test_el_cron_respalda_un_aviso_de_cancelacion_perdido(self):
        move = self.accepted_with_files()
        self.route_status(move, "CANCELADO")
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "cancelled")

    def test_un_documento_aceptado_se_consulta_una_vez_por_hora(self):
        move = self.accepted_with_files()
        self.route_status(move, "APROBADO")
        self.run_cron()
        self.run_cron()
        self.assertEqual(len(self.queried()), 1)
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        move.l10n_py_sifende_ultima_consulta = fields.Datetime.now() - timedelta(
            hours=2
        )
        self.run_cron()
        self.assertEqual(len(self.queried()), 2)

    def test_un_documento_aceptado_fuera_del_plazo_de_cancelacion_no_se_consulta(self):
        self.accepted_with_files(days_ago=30)
        self.run_cron()
        self.assertFalse(self.fake.calls)

    def test_un_error_de_sifende_se_consulta_una_vez_por_hora(self):
        (move,) = self.make_tracked(
            1, status="error", l10n_py_sifende_envio_fallido=True
        )
        self.route_status(move, "ERROR")
        self.run_cron()
        self.run_cron()
        self.assertEqual(len(self.queried()), 1)
        self.assertEqual(move.l10n_py_edi_status, "error")
        move.l10n_py_sifende_ultima_consulta = fields.Datetime.now() - timedelta(
            hours=2
        )
        self.route_status(move, "EN_LOTE")
        self.run_cron()
        self.assertEqual(len(self.queried()), 2)
        self.assertEqual(move.l10n_py_edi_status, "processing")
        self.assertFalse(move.l10n_py_sifende_envio_fallido)

    def test_un_error_de_sifende_que_pasa_a_enviado_vuelve_a_procesando(self):
        (move,) = self.make_tracked(
            1, status="error", l10n_py_sifende_envio_fallido=True
        )
        self.route_status(move, "ENVIADO")
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "processing")
        self.assertFalse(move.l10n_py_sifende_envio_fallido)

    def test_un_error_de_sifende_aprobado_despues_queda_aceptado(self):
        (move,) = self.make_tracked(
            1, status="error", l10n_py_sifende_envio_fallido=True
        )
        self.route_status(move, "APROBADO")
        self.route_files(move)
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        self.assertFalse(move.l10n_py_sifende_envio_fallido)
        self.assertTrue(move.l10n_py_kude_pdf)

    def test_un_documento_cancelado_o_rechazado_no_se_consulta(self):
        for status in ("cancelled", "rejected", "error"):
            self.make_tracked(1, status=status)
        self.run_cron()
        self.assertFalse(self.fake.calls)

    def test_la_aprobacion_y_los_archivos_siguen_funcionando(self):
        (move,) = self.make_tracked(1)
        self.route_status(move, "APROBADO")
        self.route_files(move)
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        self.assertTrue(move.l10n_py_kude_pdf)
        self.assertFalse(move.l10n_py_sifende_archivos_pendientes)

    # === Registro EDI ===

    def status_logs(self, move):
        return self.env["l10n_py.edi.log"].search(
            [("operation_type", "=", "status"), ("cdc", "=", move.l10n_py_cdc)]
        )

    def test_una_consulta_que_no_cambia_el_estado_no_se_registra(self):
        move = self.accepted_with_files()
        self.route_status(move, "APROBADO")
        self.run_cron()
        self.assertEqual(len(self.queried()), 1)
        self.assertFalse(self.status_logs(move))

    def test_un_documento_que_sigue_en_proceso_no_llena_el_registro(self):
        (move,) = self.make_tracked(1)
        self.route_status(move, "EN_LOTE")
        self.run_cron()
        self.run_cron()
        self.assertEqual(len(self.queried()), 2)
        self.assertEqual(move.l10n_py_edi_status, "processing")
        self.assertFalse(self.status_logs(move))

    def test_una_consulta_que_cambia_el_estado_se_registra(self):
        move = self.accepted_with_files()
        self.route_status(move, "CANCELADO")
        self.run_cron()
        self.assertEqual(move.l10n_py_edi_status, "cancelled")
        self.assertEqual(len(self.status_logs(move)), 1)

    def test_una_respuesta_sin_estado_se_registra(self):
        move = self.accepted_with_files()
        self.fake.add("GET", rf"/status/{move.l10n_py_cdc}$", FakeResponse(200, {}))
        self.run_cron()
        self.assertEqual(len(self.status_logs(move)), 1)
        self.assertEqual(move.l10n_py_edi_status, "accepted")

    def test_una_consulta_fallida_se_registra(self):
        move = self.accepted_with_files()
        self.fake.add(
            "GET",
            rf"/status/{move.l10n_py_cdc}$",
            FakeResponse(500, {"detail": "Servicio no disponible"}),
        )
        self.run_cron()
        log = self.status_logs(move)
        self.assertEqual(len(log), 1)
        self.assertFalse(log.success)
        self.assertEqual(move.l10n_py_edi_status, "accepted")
