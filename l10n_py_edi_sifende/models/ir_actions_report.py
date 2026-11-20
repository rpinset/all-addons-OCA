# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import io

from odoo import models

KUDE_REPORTS = (
    "account.report_invoice",
    "l10n_py_edi_base.kude_report_template",
)


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _render_qweb_pdf_prepare_streams(self, report_ref, data, res_ids=None):
        report = self._get_report(report_ref)
        if (
            report.model != "account.move"
            or not res_ids
            or not (report.is_invoice_report or report.report_name in KUDE_REPORTS)
        ):
            return super()._render_qweb_pdf_prepare_streams(
                report_ref, data, res_ids=res_ids
            )
        moves = self.env["account.move"].browse(res_ids)
        with_kude = moves.filtered(lambda m: m._l10n_py_sifende_has_kude())
        if not with_kude:
            return super()._render_qweb_pdf_prepare_streams(
                report_ref, data, res_ids=res_ids
            )
        others = [res_id for res_id in res_ids if res_id not in with_kude.ids]
        streams = (
            super()._render_qweb_pdf_prepare_streams(report_ref, data, res_ids=others)
            if others
            else {}
        )
        for move in with_kude:
            streams[move.id] = {
                "stream": io.BytesIO(move._l10n_py_sifende_kude_content()),
                "attachment": None,
            }
        ordered = {
            res_id: streams.pop(res_id) for res_id in res_ids if res_id in streams
        }
        ordered.update(streams)
        return ordered
