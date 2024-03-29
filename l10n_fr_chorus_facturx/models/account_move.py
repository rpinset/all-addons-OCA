# Copyright 2017-2020 Akretion (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _cii_trade_contact_department_name(self, partner):
        if partner.fr_chorus_service_id:
            return partner.name
        return super()._cii_trade_contact_department_name(partner)

    @api.model
    def _cii_trade_agreement_buyer_ref(self, partner):
        if partner.fr_chorus_service_id:
            return partner.fr_chorus_service_id.code
        return super()._cii_trade_agreement_buyer_ref(partner)

    def chorus_get_invoice(self, chorus_invoice_format):
        self.ensure_one()
        if chorus_invoice_format == "xml_cii":
            chorus_file_content = self.with_context(
                fr_chorus_cii16b=True
            ).generate_facturx_xml()[0]
        elif chorus_invoice_format == "pdf_factur-x":
            chorus_file_content, filetype = self.env["ir.actions.report"]._render(
                "account.report_invoice", [self.id]
            )
            assert filetype == "pdf", "wrong filetype"
        else:
            chorus_file_content = super().chorus_get_invoice(chorus_invoice_format)
        return chorus_file_content

    def _prepare_facturx_attachments(self):
        res = super()._prepare_facturx_attachments()
        for attach in self.chorus_attachment_ids:
            res[attach.name] = {
                "filedata": attach.raw,
                "modification_datetime": attach.write_date,
                "creation_datetime": attach.create_date,
            }
        return res
