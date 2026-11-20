# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.exceptions import UserError
from odoo.tests import tagged

from .common import CDC, FIXED_DATE, SifendeCommon

ORIGIN_CDC = "01800123451001001000000122026042710000000006"


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestNotesAndStamps(SifendeCommon):
    def accepted_invoice(self):
        invoice = self.make_move("fe")
        invoice.write({"l10n_py_edi_status": "accepted", "l10n_py_cdc": ORIGIN_CDC})
        return invoice

    def credit_note_of(self, invoice):
        wizard = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create(
                {
                    "journal_id": self.journals["nc"].id,
                    "reason": "Devolución",
                    "date": FIXED_DATE,
                }
            )
        )
        return self.env["account.move"].browse(wizard.refund_moves()["res_id"])

    def debit_note_of(self, invoice):
        wizard = (
            self.env["account.debit.note"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create(
                {
                    "journal_id": self.journals["nd"].id,
                    "reason": "Ajuste",
                    "date": FIXED_DATE,
                    "copy_lines": True,
                }
            )
        )
        return self.env["account.move"].browse(wizard.create_debit()["res_id"])

    def associated_cdcs(self, move):
        return move.l10n_py_associated_document_ids.mapped("cdc")

    # === Documento asociado ===

    def test_la_nota_de_credito_toma_el_cdc_de_la_factura_revertida(self):
        credit_note = self.credit_note_of(self.accepted_invoice())
        credit_note.action_post()
        self.assertEqual(self.associated_cdcs(credit_note), [ORIGIN_CDC])
        self.assertEqual(
            credit_note.l10n_py_associated_document_ids.association_type, "1"
        )

    def test_la_nota_de_credito_se_envia_sin_cargar_el_asociado_a_mano(self):
        credit_note = self.credit_note_of(self.accepted_invoice())
        credit_note.action_post()
        self.route_emission(self.emission_response(cdc=CDC))
        credit_note.action_send_edi()
        payload = self.fake.calls_to("POST", r"^/documento-electronico$")[0].json
        self.assertEqual(
            payload["documentoAsociado"],
            {"tipoDocumento": "ELECTRONICO", "cdc": ORIGIN_CDC},
        )

    def test_la_nota_de_debito_toma_el_cdc_de_la_factura_de_origen(self):
        debit_note = self.debit_note_of(self.accepted_invoice())
        debit_note.action_post()
        self.assertEqual(debit_note.debit_origin_id.l10n_py_cdc, ORIGIN_CDC)
        self.assertEqual(self.associated_cdcs(debit_note), [ORIGIN_CDC])

    def test_el_asociado_se_completa_al_enviar_si_el_cdc_llego_despues(self):
        invoice = self.make_move("fe")
        credit_note = self.credit_note_of(invoice)
        credit_note.action_post()
        self.assertFalse(credit_note.l10n_py_associated_document_ids)
        invoice.l10n_py_cdc = ORIGIN_CDC
        self.route_emission(self.emission_response(cdc=CDC))
        credit_note.action_send_edi()
        self.assertEqual(self.associated_cdcs(credit_note), [ORIGIN_CDC])

    def test_un_asociado_cargado_a_mano_no_se_duplica(self):
        credit_note = self.credit_note_of(self.accepted_invoice())
        credit_note.action_post()
        credit_note.l10n_py_associated_document_ids.unlink()
        other = "01800123451001001000000012026010112345678901"
        self.associate(credit_note, other)
        credit_note._l10n_py_sifende_link_origin_document()
        self.assertEqual(self.associated_cdcs(credit_note), [other])

    def test_una_nota_sin_origen_con_cdc_pide_el_asociado(self):
        credit_note = self.credit_note_of(self.make_move("fe"))
        credit_note.action_post()
        with self.assertRaisesRegex(UserError, "documento asociado"):
            credit_note.action_send_edi()
        self.assertFalse(self.fake.calls_to("POST", ".*"))

    # === Timbrado por defecto ===

    def draft_without_stamp(self, kind, **vals):
        return self.env["account.move"].create(
            {
                "move_type": "out_refund" if kind == "nc" else "out_invoice",
                "partner_id": self.partner.id,
                "journal_id": self.journals[kind].id,
                "l10n_latam_document_type_id": self.doc_types[kind].id,
                "invoice_date": FIXED_DATE,
                "invoice_line_ids": [(0, 0, self.line())],
                **vals,
            }
        )

    def test_la_factura_toma_el_timbrado_del_diario(self):
        move = self.draft_without_stamp("fe")
        self.assertEqual(move.l10n_py_authorization_id, self.auths["fe"])

    def test_la_nota_de_credito_toma_el_timbrado_de_su_tipo(self):
        move = self.draft_without_stamp("nc")
        self.assertEqual(move.l10n_py_authorization_id, self.auths["nc"])

    def test_la_nota_de_debito_toma_el_timbrado_de_su_tipo(self):
        move = self.draft_without_stamp("nd")
        self.assertEqual(move.l10n_py_authorization_id, self.auths["nd"])

    def test_un_timbrado_elegido_a_mano_se_respeta(self):
        other = self.auths["fe"].copy({"name": "87654321"})
        move = self.make_move("fe", posted=False, l10n_py_authorization_id=other.id)
        self.assertEqual(move.l10n_py_authorization_id, other)

    def test_la_nota_de_debito_se_confirma_sin_elegir_timbrado(self):
        debit_note = self.debit_note_of(self.accepted_invoice())
        self.assertEqual(debit_note.l10n_py_authorization_id, self.auths["nd"])

    def test_al_cambiar_el_tipo_de_documento_cambia_el_timbrado(self):
        move = self.draft_without_stamp("fe")
        move.l10n_latam_document_type_id = self.doc_types["nd"]
        self.assertEqual(move.l10n_py_authorization_id, self.auths["nd"])
