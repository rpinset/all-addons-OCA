# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, models
from odoo.exceptions import UserError


class AccountMoveSend(models.AbstractModel):
    _inherit = "account.move.send"

    @api.model
    def _get_invoice_extra_attachments(self, move):
        attachments = super()._get_invoice_extra_attachments(move)
        if move._l10n_py_sifende_has_kude():
            attachments |= move._l10n_py_sifende_xml_attachment()
        return attachments

    @api.model
    def _get_default_mail_subject(self, move, mail_template, mail_lang):
        subject = super()._get_default_mail_subject(move, mail_template, mail_lang)
        fiscal = move.l10n_py_sifende_document_name
        if subject and fiscal and move.name:
            subject = subject.replace(move.name, fiscal)
        return subject

    @api.model
    def _link_invoice_documents(self, invoices_data):
        # account_edi_ubl_cii embeds a factur-x.xml in the PDF: the KuDE goes untouched
        for invoice, invoice_data in invoices_data.items():
            values = invoice_data.get("pdf_attachment_values")
            if values and invoice._l10n_py_sifende_has_kude():
                values["raw"] = invoice._l10n_py_sifende_kude_content()
        return super()._link_invoice_documents(invoices_data)

    @api.model
    def _hook_invoice_document_before_pdf_report_render(self, invoice, invoice_data):
        super()._hook_invoice_document_before_pdf_report_render(invoice, invoice_data)
        if not invoice._l10n_py_sifende_is_document():
            return
        error = invoice._l10n_py_sifende_send_error()
        if not error:
            try:
                invoice._l10n_py_sifende_prepare_send()
            except UserError as e:
                error = str(e)
        if error:
            invoice_data["error"] = {
                "error_title": self.env._("No se puede enviar el comprobante fiscal:"),
                "errors": [error],
            }

    @api.model
    def _generate_invoice_fallback_documents(self, invoices_data):
        # sin comprobante fiscal no hay proforma de respaldo: el error se conserva
        blocked = {
            invoice
            for invoice in invoices_data
            if invoice._l10n_py_sifende_send_error()
        }
        return super()._generate_invoice_fallback_documents(
            {
                invoice: data
                for invoice, data in invoices_data.items()
                if invoice not in blocked
            }
        )
