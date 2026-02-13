# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"

    is_direct_print = fields.Boolean(
        string="Direct Print",
        default=lambda self: self.env.company.invoice_is_direct_print,
    )

    def enqueue_invoices(self):
        active_ids = self._context.get("active_ids")
        invoices = self.env["account.move"].browse(active_ids)
        params = {
            "is_print": self.is_print,
            "is_email": self.is_email,
            "is_direct_print": self.is_direct_print,
            "exclude_followers": self.exclude_followers,
        }
        invoices_to_send = invoices.mass_sending(self.template_id, **params)
        ineligible_invoices = invoices - invoices_to_send
        title = _("Invoices: Mass sending")
        msg = _(
            "The sending of %(invoices_count)d invoices will be processed "
            "in background.",
            invoices_count=len(invoices_to_send),
        )
        notification = {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": title,
                "message": msg,
                "type": "success",
                "next": {"type": "ir.actions.act_window_close"},
            },
        }
        if ineligible_invoices:
            invoicelist = [invoice.name for invoice in ineligible_invoices]
            warn_msg = _(
                "Invoices %(ineligible_invoices)s were already in "
                "processing or do not have an email address defined.",
                ineligible_invoices=" ".join(invoicelist),
            )
            notification["params"]["next"].update(
                {
                    "type": "ir.actions.client",
                    "tag": "display_notification",
                    "params": {
                        "title": title,
                        "message": warn_msg,
                        "type": "warning",
                        "sticky": True,
                        "next": {"type": "ir.actions.act_window_close"},
                    },
                }
            )
        return notification

    def _print_document(self):
        self.ensure_one()
        res = super()._print_document()
        if self.is_direct_print and "account_invoice_mass_sending" in self._context:
            res = self.generate_pdf_from_action_report(res)
        return res

    def generate_pdf_from_action_report(self, action_report):
        report_ref = action_report["report_name"]
        context = dict(action_report.get("context", {}))

        res_ids = context.get("active_ids") or [context.get("active_id")]
        if not res_ids:
            raise ValueError("No record IDs found in action_report context.")

        report_obj = self.env["ir.actions.report"].with_context(
            context, is_direct_print=True
        )
        report_obj._render_qweb_pdf(report_ref, res_ids)
        return True
