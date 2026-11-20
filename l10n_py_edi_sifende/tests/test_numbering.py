# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.exceptions import UserError
from odoo.tests import tagged

from .common import SECURITY_CODE, SifendeCommon, problem


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestNumbering(SifendeCommon):
    def in_use(self, **extra):
        return problem("document-number-in-use", 409, "Número en uso", **extra)

    def stuck_move(self):
        move = self.make_move("fe")
        self.route_emission(self.in_use())
        move.action_send_edi()
        return move

    def sent_number(self):
        return self.fake.calls_to("POST", r"^/documento-electronico$")[-1].json[
            "numeroDocumento"
        ]

    # === Número Desde ===

    def test_la_numeracion_respeta_numero_desde_si_es_mayor_que_el_maximo(self):
        self.auths["fe"].invoice_number_from = 101
        self.assertEqual(self.make_move("fe").l10n_py_invoice_number, 101)
        self.assertEqual(self.make_move("fe").l10n_py_invoice_number, 102)

    def test_subir_numero_desde_con_facturas_previas_salta_al_nuevo_inicio(self):
        self.make_move("fe")
        self.make_move("fe")
        self.auths["fe"].invoice_number_from = 50
        self.assertEqual(self.auths["fe"].next_number, 50)
        self.assertEqual(self.make_move("fe").l10n_py_invoice_number, 50)

    def test_si_el_maximo_supera_numero_desde_sigue_la_secuencia(self):
        self.make_move("fe")
        self.make_move("fe")
        self.assertEqual(self.make_move("fe").l10n_py_invoice_number, 3)

    def test_la_faja_agotada_se_informa(self):
        self.auths["fe"].invoice_number_to = 2
        self.make_move("fe")
        self.make_move("fe")
        with self.assertRaisesRegex(UserError, "agotada"):
            self.make_move("fe")

    # === Número en uso ===

    def test_un_numero_en_uso_deja_la_factura_marcada_con_instrucciones(self):
        move = self.stuck_move()
        self.assertEqual(move.l10n_py_edi_status, "error")
        self.assertTrue(move.l10n_py_sifende_numero_ocupado)
        self.assertIn("Renumerar", move.l10n_py_edi_message)
        self.assertIn("Número Desde", move.l10n_py_edi_message)
        self.assertEqual(self.auths["fe"].l10n_py_sifende_ultimo_numero_en_uso, 1)

    def test_reintentar_un_numero_en_uso_indica_renumerar(self):
        move = self.stuck_move()
        with self.assertRaisesRegex(UserError, "Renumerar"):
            move.action_retry_edi()
        self.assertEqual(move.l10n_py_sifende_intento, 0)

    def test_renumerar_toma_el_siguiente_numero_y_no_reutiliza_el_ocupado(self):
        move = self.stuck_move()
        move.action_l10n_py_sifende_renumber()
        self.assertEqual(move.l10n_py_invoice_number, 2)
        self.assertEqual(move.l10n_py_full_invoice_number, "001-001-0000002")
        self.assertEqual(move.l10n_py_edi_status, "to_send")
        self.assertFalse(move.l10n_py_sifende_numero_ocupado)
        self.assertEqual(move.l10n_py_sifende_intento, 1)
        self.assertIn("2", move.l10n_py_edi_message)

    def test_la_factura_renumerada_se_emite_con_el_numero_nuevo_y_clave_nueva(self):
        move = self.stuck_move()
        first_key = self.fake.calls_to("POST", r"^/documento-electronico$")[-1].headers[
            "Idempotency-Key"
        ]
        move.action_l10n_py_sifende_renumber()
        self.route_emission(self.emission_response())
        move.action_send_edi()
        call = self.fake.calls_to("POST", r"^/documento-electronico$")[-1]
        self.assertEqual(call.json["numeroDocumento"], 2)
        self.assertNotEqual(call.headers["Idempotency-Key"], first_key)
        self.assertEqual(move.l10n_py_edi_status, "processing")

    def test_renumerar_respeta_numero_desde(self):
        move = self.stuck_move()
        self.auths["fe"].invoice_number_from = 101
        move.action_l10n_py_sifende_renumber()
        self.assertEqual(move.l10n_py_invoice_number, 101)

    def test_cada_numero_en_uso_avanza_el_siguiente(self):
        move = self.stuck_move()
        for expected in (2, 3, 4):
            move.action_l10n_py_sifende_renumber()
            self.assertEqual(move.l10n_py_invoice_number, expected)
            self.route_emission(self.in_use())
            move.action_send_edi()
        self.assertEqual(self.auths["fe"].l10n_py_sifende_ultimo_numero_en_uso, 4)
        self.assertEqual(self.make_move("fe").l10n_py_invoice_number, 5)

    def test_un_numero_inutilizado_tambien_se_renumera(self):
        move = self.make_move("fe")
        self.route_emission(problem("document-number-voided", 409, "Inutilizado"))
        move.action_send_edi()
        self.assertTrue(move.l10n_py_sifende_numero_ocupado)
        move.action_l10n_py_sifende_renumber()
        self.assertEqual(move.l10n_py_invoice_number, 2)

    def test_las_otras_facturas_tampoco_reutilizan_el_numero_ocupado(self):
        self.stuck_move().action_l10n_py_sifende_renumber()
        self.assertEqual(self.make_move("fe").l10n_py_invoice_number, 3)

    def test_no_se_renumera_un_documento_sin_el_error(self):
        move = self.make_move("fe")
        with self.assertRaisesRegex(UserError, "ya usado"):
            move.action_l10n_py_sifende_renumber()

    def test_no_se_renumera_un_documento_con_cdc(self):
        move = self.stuck_move()
        move.l10n_py_cdc = "0" * 44
        with self.assertRaisesRegex(UserError, "Sifende ya lo emitió"):
            move.action_l10n_py_sifende_renumber()
        self.assertEqual(move.l10n_py_invoice_number, 1)

    def test_si_el_cdc_existente_es_el_de_este_documento_no_se_renumera(self):
        move = self.make_move("fe")
        cdc = f"01800123451001001{1:07d}120261020{1}{SECURITY_CODE}0"
        self.assertEqual(len(cdc), 44)
        self.route_emission(self.in_use(cdc=cdc))
        move.action_send_edi()
        self.assertTrue(move.l10n_py_sifende_numero_ocupado)
        self.assertEqual(self.auths["fe"].l10n_py_sifende_ultimo_numero_en_uso, 0)
        with self.assertRaisesRegex(UserError, "este mismo documento"):
            move.action_l10n_py_sifende_renumber()
        self.assertEqual(move.l10n_py_invoice_number, 1)

    def test_renumerar_con_la_faja_agotada_avisa(self):
        self.auths["fe"].invoice_number_to = 2
        move = self.stuck_move()
        move.action_l10n_py_sifende_renumber()
        self.route_emission(self.in_use())
        move.action_send_edi()
        with self.assertRaisesRegex(UserError, "agotada"):
            move.action_l10n_py_sifende_renumber()
        self.assertEqual(move.l10n_py_invoice_number, 2)
