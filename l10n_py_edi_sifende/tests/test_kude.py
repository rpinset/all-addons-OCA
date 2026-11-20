# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import base64
from unittest.mock import patch

from odoo.exceptions import UserError
from odoo.tests import tagged

from odoo.addons.account.models.account_move_send import AccountMoveSend
from odoo.addons.base.models.ir_actions_report import IrActionsReport

from .common import CDC, FakeResponse, SifendeCommon

XML = b'<?xml version="1.0"?><rDE><DE Id="' + CDC.encode() + b'"/></rDE>'
PDF = b"%PDF-1.4 kude"
ODOO_PDF = b"%PDF-1.4 odoo"
NOT_ACCEPTED = ("to_send", "processing", "rejected", "error")


class KudeCommon(SifendeCommon):
    def setUp(self):
        super().setUp()
        patcher = patch.object(
            IrActionsReport, "_run_wkhtmltopdf", return_value=ODOO_PDF
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        self.company.external_report_layout_id = self.env.ref(
            "web.external_layout_standard"
        )

    def accepted_move(self, files=True, **vals):
        move = self.make_move("fe")
        move.write({"l10n_py_edi_status": "accepted", "l10n_py_cdc": CDC, **vals})
        if files:
            move.write(
                {
                    "l10n_py_kude_pdf": base64.b64encode(PDF),
                    "l10n_py_kude_filename": f"KUDE_{CDC}.pdf",
                    "l10n_py_edi_xml": base64.b64encode(XML),
                    "l10n_py_edi_xml_filename": f"{CDC}.xml",
                }
            )
        return move

    def route_files(self, kude=None):
        self.fake.add(
            "GET",
            rf"/documento-electronico/{CDC}/xml$",
            FakeResponse(200, content=XML, headers={"Content-Type": "application/xml"}),
        )
        self.fake.add(
            "GET",
            rf"/documento-electronico/{CDC}/kude$",
            kude
            or FakeResponse(
                200, content=PDF, headers={"Content-Type": "application/pdf"}
            ),
        )

    def render_pdf(self, moves, report="account.account_invoices"):
        report = self.env.ref(report).with_context(force_report_rendering=True)
        return report._render_qweb_pdf(report, moves.ids)[0]

    def send(self, move):
        wizard = (
            self.env["account.move.send.wizard"]
            .with_context(
                active_model="account.move",
                active_ids=move.ids,
                force_report_rendering=True,
            )
            .create({"move_id": move.id})
        )
        return wizard.action_send_and_print()

    def sent_attachments(self, move):
        messages = move.message_ids.filtered(lambda m: m.message_type == "comment")
        return messages[:1].attachment_ids

    def move_files(self, move):
        return self.env["ir.attachment"].search(
            [
                ("res_model", "=", "account.move"),
                ("res_id", "=", move.id),
                ("res_field", "!=", False),
            ]
        )


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestKudeImprimir(KudeCommon):
    def test_imprimir_un_documento_aceptado_devuelve_el_kude(self):
        move = self.accepted_move()
        self.assertEqual(self.render_pdf(move), PDF)
        self.assertEqual(
            self.render_pdf(move, "account.account_invoices_without_payment"), PDF
        )
        self.assertEqual(
            self.render_pdf(move, "l10n_py_edi_base.action_kude_report"), PDF
        )
        self.assertFalse(self.fake.calls_to("GET", "/kude$"))

    def test_el_boton_imprimir_nombra_el_archivo_con_el_cdc(self):
        move = self.accepted_move()
        action = move.action_print_pdf()
        self.assertEqual(action["type"], "ir.actions.report")
        self.assertEqual(move._get_report_base_filename(), f"KUDE_{CDC}")

    def test_imprimir_trae_el_kude_si_todavia_no_esta_descargado(self):
        move = self.accepted_move(files=False)
        self.route_files()
        move.action_print_pdf()
        self.assertEqual(self.render_pdf(move), PDF)
        self.assertEqual(base64.b64decode(move.l10n_py_kude_pdf), PDF)
        self.assertEqual(len(self.fake.calls_to("GET", "/kude$")), 1)

    def test_imprimir_avisa_si_sifende_no_entrega_el_kude(self):
        move = self.accepted_move(files=False)
        self.route_files(
            kude=FakeResponse(
                202, {"estado": "PENDIENTE"}, headers={"Retry-After": "10"}
            )
        )
        with self.assertRaisesRegex(UserError, "todavía no entregó el KuDE"):
            move.action_print_pdf()
        self.assertFalse(move.l10n_py_kude_pdf)

    def test_imprimir_un_documento_no_aceptado_lleva_el_aviso_sin_validez_fiscal(self):
        for status in NOT_ACCEPTED:
            with self.subTest(status=status):
                move = self.accepted_move(files=False, l10n_py_edi_status=status)
                self.assertEqual(move.action_print_pdf()["type"], "ir.actions.report")
                self.assertEqual(self.render_pdf(move), ODOO_PDF)
                self.assertIn("Sin validez fiscal", move.l10n_py_sifende_aviso_fiscal)
        self.assertFalse(self.fake.calls)

    def test_el_html_del_pdf_estandar_muestra_el_aviso_solo_si_no_esta_aceptado(self):
        report = self.env.ref("account.account_invoices")
        pending = self.accepted_move(files=False, l10n_py_edi_status="processing")
        html = report._render_qweb_html(report, pending.ids)[0].decode()
        self.assertIn("SIFEN todavía no aceptó este documento", html)
        cancelled = self.accepted_move(files=False, l10n_py_edi_status="cancelled")
        html = report._render_qweb_html(report, cancelled.ids)[0].decode()
        self.assertIn("cancelado en SIFEN", html)
        accepted = self.accepted_move()
        html = report._render_qweb_html(report, accepted.ids)[0].decode()
        self.assertNotIn("sin validez fiscal", html.lower())

    def test_imprimir_varios_mezcla_el_kude_con_el_pdf_de_odoo(self):
        accepted = self.accepted_move()
        pending = self.accepted_move(files=False, l10n_py_edi_status="processing")
        report = self.env.ref("account.account_invoices")
        streams = report.with_context(
            force_report_rendering=True
        )._render_qweb_pdf_prepare_streams(
            report, {}, res_ids=[pending.id, accepted.id]
        )
        self.assertEqual(list(streams), [pending.id, accepted.id])
        self.assertEqual(streams[accepted.id]["stream"].getvalue(), PDF)
        self.assertEqual(streams[pending.id]["stream"].getvalue(), ODOO_PDF)

    def test_documentos_legales_del_portal_y_del_zip(self):
        move = self.accepted_move()
        pdf = move._get_invoice_legal_documents("pdf")
        self.assertEqual(pdf["content"], PDF)
        self.assertEqual(pdf["filename"], f"KUDE_{CDC}.pdf")
        everything = move._get_invoice_legal_documents_all()
        self.assertEqual(
            [(d["filename"], d["content"]) for d in everything],
            [(f"KUDE_{CDC}.pdf", PDF), (f"{CDC}.xml", XML)],
        )

    def test_el_portal_y_el_menu_pdf_de_un_cancelado_no_entregan_el_kude_aprobado(self):
        move = self.accepted_move()
        self.send(move)
        move._l10n_py_sifende_apply_state("CANCELADO")
        self.assertEqual(move.l10n_py_edi_status, "cancelled")
        move = move.with_context(force_report_rendering=True)
        documents = move._get_invoice_legal_documents_all(allow_fallback=True)
        single = move._get_invoice_legal_documents("pdf", allow_fallback=True)
        for document in [*documents, single]:
            self.assertEqual(document["content"], ODOO_PDF)
            self.assertFalse(document["filename"].startswith("KUDE_"))
        self.assertEqual(len(documents), 1)
        self.assertEqual(base64.b64decode(move.l10n_py_kude_pdf), PDF)
        self.assertEqual(base64.b64decode(move.l10n_py_edi_xml), XML)
        self.assertEqual(move.invoice_pdf_report_id.raw, PDF)

    def test_el_pdf_de_un_cancelado_lleva_el_aviso_de_cancelacion(self):
        move = self.accepted_move(l10n_py_edi_status="cancelled")
        html = (
            self.env.ref("account.account_invoices")
            ._render_qweb_html("account.account_invoices", move.ids)[0]
            .decode()
        )
        self.assertIn("cancelado en SIFEN", html)
        self.assertTrue(move._get_invoice_legal_documents("pdf", allow_fallback=True))

    def test_los_documentos_legales_no_consultan_a_sifende_sin_pedir_el_respaldo(self):
        move = self.accepted_move(files=False)
        self.assertFalse(move._get_invoice_legal_documents_all())
        self.assertFalse(self.fake.calls)


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestKudeEnviar(KudeCommon):
    def test_enviar_un_documento_aceptado_adjunta_el_kude_y_el_xml(self):
        move = self.accepted_move()
        self.send(move)
        attachments = self.sent_attachments(move)
        self.assertEqual(
            {a.name: a.raw for a in attachments},
            {f"KUDE_{CDC}.pdf": PDF, f"{CDC}.xml": XML},
        )
        self.assertEqual(move.invoice_pdf_report_id.name, f"KUDE_{CDC}.pdf")
        self.assertTrue(move.is_move_sent)
        self.assertEqual(
            {a.name: a.mimetype for a in attachments},
            {f"KUDE_{CDC}.pdf": "application/pdf", f"{CDC}.xml": "application/xml"},
        )

    def test_el_xml_firmado_del_documento_es_application_xml(self):
        move = self.accepted_move()
        attachment = move._l10n_py_sifende_xml_attachment()
        self.assertEqual(attachment.name, f"{CDC}.xml")
        self.assertEqual(attachment.mimetype, "application/xml")

    def test_enviar_adjunta_el_kude_sin_el_factur_x_que_incrusta_odoo(self):
        def embed(_self, invoice, invoice_data):
            invoice_data["pdf_attachment_values"]["raw"] += b"/factur-x.xml"

        move = self.accepted_move()
        with patch.object(
            AccountMoveSend, "_hook_invoice_document_after_pdf_report_render", embed
        ):
            self.send(move)
        self.assertEqual(move.invoice_pdf_report_id.raw, PDF)
        self.assertEqual(
            {a.name: a.raw for a in self.sent_attachments(move)},
            {f"KUDE_{CDC}.pdf": PDF, f"{CDC}.xml": XML},
        )

    def test_enviar_dos_veces_no_duplica_los_adjuntos_del_documento(self):
        move = self.accepted_move()
        self.send(move)
        stored = self.move_files(move)
        pdf = move.invoice_pdf_report_id
        self.send(move)
        self.assertEqual(self.move_files(move), stored)
        self.assertEqual(move.invoice_pdf_report_id, pdf)
        self.assertEqual(
            {a.name for a in self.sent_attachments(move)},
            {f"KUDE_{CDC}.pdf", f"{CDC}.xml"},
        )

    def test_enviar_reemplaza_el_pdf_de_odoo_guardado_antes_de_la_aceptacion(self):
        move = self.accepted_move()
        move.invoice_pdf_report_file = base64.b64encode(ODOO_PDF)
        self.assertEqual(move.invoice_pdf_report_id.raw, ODOO_PDF)
        self.send(move)
        self.assertEqual(move.invoice_pdf_report_id.raw, PDF)
        self.assertEqual({a.raw for a in self.sent_attachments(move)}, {PDF, XML})

    def test_el_asistente_no_ofrece_elegir_otro_reporte(self):
        move = self.accepted_move()
        wizard = (
            self.env["account.move.send.wizard"]
            .with_context(active_model="account.move", active_ids=move.ids)
            .create({"move_id": move.id})
        )
        self.assertFalse(wizard.display_pdf_report_id)

    def test_enviar_trae_los_archivos_que_faltan(self):
        move = self.accepted_move(files=False)
        self.route_files()
        self.send(move)
        self.assertEqual({a.raw for a in self.sent_attachments(move)}, {PDF, XML})

    def test_enviar_avisa_si_sifende_no_entrega_los_archivos(self):
        move = self.accepted_move(files=False)
        self.route_files(
            kude=FakeResponse(
                202, {"estado": "PENDIENTE"}, headers={"Retry-After": "10"}
            )
        )
        with self.assertRaisesRegex(UserError, "todavía no entregó el KuDE"):
            move.action_send_and_print()
        self.assertFalse(self.sent_attachments(move))

    def test_enviar_un_documento_no_aceptado_avisa_que_falta_el_comprobante(self):
        for status in NOT_ACCEPTED:
            with self.subTest(status=status):
                move = self.accepted_move(files=False, l10n_py_edi_status=status)
                with self.assertRaisesRegex(
                    UserError, "todavía no tiene comprobante fiscal"
                ):
                    move.action_send_and_print()
                with self.assertRaisesRegex(
                    UserError, "todavía no tiene comprobante fiscal"
                ):
                    self.env["account.move.send"]._generate_and_send_invoices(move)
                self.assertFalse(self.sent_attachments(move))
                self.assertFalse(move.invoice_pdf_report_id)

    def test_enviar_un_documento_cancelado_dice_que_el_kude_no_vale(self):
        move = self.accepted_move(l10n_py_edi_status="cancelled")
        with self.assertRaisesRegex(UserError, "cancelado en SIFEN"):
            move.action_send_and_print()
        self.assertFalse(self.sent_attachments(move))

    def test_el_envio_con_respaldo_no_manda_una_proforma_de_un_no_aceptado(self):
        service = self.env["account.move.send"].with_context(
            force_report_rendering=True
        )
        for status in (*NOT_ACCEPTED, "cancelled"):
            with self.subTest(status=status):
                move = self.accepted_move(files=False, l10n_py_edi_status=status)
                for from_cron in (False, True):
                    move.sending_data = {"author_user_id": self.env.uid}
                    attachments = service._generate_and_send_invoices(
                        move,
                        from_cron=from_cron,
                        allow_raising=False,
                        allow_fallback_pdf=True,
                    )
                    self.assertFalse(attachments)
                    self.assertFalse(self.sent_attachments(move))
                    self.assertFalse(move.invoice_pdf_report_id)
                self.assertFalse(move.is_move_sent)

    def test_un_documento_se_considera_listo_para_enviar_solo_si_esta_aceptado(self):
        for status in (*NOT_ACCEPTED, "cancelled"):
            with self.subTest(status=status):
                move = self.accepted_move(files=False, l10n_py_edi_status=status)
                self.assertFalse(move._is_ready_to_be_sent())
        self.assertTrue(self.accepted_move()._is_ready_to_be_sent())

    def test_enviar_varios_nombra_los_que_no_estan_aceptados(self):
        accepted = self.accepted_move()
        pending = self.accepted_move(files=False, l10n_py_edi_status="processing")
        with self.assertRaisesRegex(UserError, pending.name):
            (accepted | pending).action_send_and_print()

    def test_el_envio_en_lote_deja_el_error_en_el_documento_no_aceptado(self):
        accepted = self.accepted_move()
        pending = self.accepted_move(files=False, l10n_py_edi_status="processing")
        pending.sending_data = {"author_user_id": self.env.uid}
        accepted.sending_data = {"author_user_id": self.env.uid}
        self.env["account.move.send"].with_context(
            force_report_rendering=True
        )._generate_and_send_invoices(
            accepted | pending, from_cron=True, allow_raising=False
        )
        self.assertEqual({a.raw for a in self.sent_attachments(accepted)}, {PDF, XML})
        self.assertFalse(self.sent_attachments(pending))
        self.assertIn(
            "todavía no tiene comprobante fiscal", pending.message_ids[0].body
        )


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestKudeSinSifende(KudeCommon):
    """Sin el conector de Sifende, Odoo se comporta como siempre."""

    def setUp(self):
        super().setUp()
        field = self.env["l10n_py.edi.connector"]._fields["provider_type"]
        for attribute, value in (
            ("selection", [*field.selection, ("otro", "Otro")]),
            ("_selection", {**field._selection, "otro": "Otro"}),
        ):
            patcher = patch.object(field, attribute, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.connector.provider_type = "otro"

    def test_imprimir_sigue_usando_el_pdf_de_odoo(self):
        for status in ("accepted", "processing"):
            with self.subTest(status=status):
                move = self.accepted_move(l10n_py_edi_status=status)
                self.assertEqual(self.render_pdf(move), ODOO_PDF)
                self.assertFalse(move.l10n_py_sifende_aviso_fiscal)
                self.assertNotEqual(move._get_report_base_filename(), f"KUDE_{CDC}")
        self.assertFalse(self.fake.calls)

    def test_enviar_sigue_usando_el_pdf_de_odoo(self):
        for status in ("accepted", "processing"):
            with self.subTest(status=status):
                move = self.accepted_move(l10n_py_edi_status=status)
                self.send(move)
                attachments = self.sent_attachments(move)
                self.assertEqual(attachments.mapped("raw"), [ODOO_PDF])
                self.assertNotIn("KUDE", attachments.name)
        self.assertFalse(self.fake.calls)

    def test_el_envio_con_respaldo_sigue_mandando_la_proforma(self):
        move = self.accepted_move(files=False, l10n_py_edi_status="processing")
        self.assertTrue(move._is_ready_to_be_sent())
        attachments = (
            self.env["account.move.send"]
            .with_context(force_report_rendering=True)
            ._generate_and_send_invoices(
                move, allow_raising=False, allow_fallback_pdf=True
            )
        )
        self.assertTrue(attachments)

    def test_los_documentos_legales_de_un_cancelado_no_cambian(self):
        move = self.accepted_move(l10n_py_edi_status="cancelled")
        self.assertFalse(move._get_invoice_legal_documents("pdf"))
        self.assertFalse(move._get_invoice_legal_documents_all())

    def test_los_documentos_legales_no_cambian(self):
        move = self.accepted_move()
        self.assertFalse(move._get_invoice_legal_documents("pdf"))
        self.assertFalse(move._get_invoice_legal_documents_all())
        self.assertFalse(
            self.env["account.move.send"]._get_invoice_extra_attachments(move)
        )
