# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.exceptions import UserError
from odoo.tests import tagged

from .common import CDC, SifendeCommon


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestResetDraft(SifendeCommon):
    def move_with(self, status, cdc=CDC):
        move = self.make_move("fe")
        move.write({"l10n_py_edi_status": status, "l10n_py_cdc": cdc})
        return move

    def test_un_documento_enviado_no_vuelve_a_borrador(self):
        for status in ("sent", "processing", "accepted"):
            move = self.move_with(status)
            with self.assertRaisesRegex(UserError, "Cancelar EDI.*nota de crédito"):
                move.button_draft()
            self.assertEqual(move.state, "posted", status)

    def test_el_boton_de_borrador_se_oculta_con_el_documento_enviado(self):
        self.assertFalse(self.move_with("accepted").show_reset_to_draft_button)
        self.assertTrue(self.move_with("to_send", False).show_reset_to_draft_button)

    def test_un_documento_rechazado_o_con_error_vuelve_a_borrador(self):
        for status, cdc in (("rejected", CDC), ("rejected", False), ("error", False)):
            move = self.move_with(status, cdc)
            self.assertTrue(move.show_reset_to_draft_button)
            move.button_draft()
            self.assertEqual(move.state, "draft", status)
            move.button_cancel()
            self.assertEqual(move.state, "cancel", status)

    def test_un_documento_sin_conector_vuelve_a_borrador(self):
        self.connector.unlink()
        move = self.move_with("accepted")
        move.button_draft()
        self.assertEqual(move.state, "draft")

    def test_un_documento_cancelado_en_sifen_no_se_reemite(self):
        move = self.move_with("cancelled")
        move.button_draft()
        with self.assertRaisesRegex(UserError, "no se reutiliza"):
            move.action_post()
        move.button_cancel()
        self.assertEqual(move.state, "cancel")
        self.assertEqual(move.l10n_py_edi_status, "cancelled")

    def test_editar_importes_de_un_documento_enviado_avisa_de_los_importes(self):
        move = self.move_with("accepted")
        line = move.line_ids.filtered(lambda line: line.display_type == "payment_term")
        with self.assertRaisesRegex(UserError, "importes"):
            line.date_maturity = line.date_maturity.replace(year=2030)
