# Copyright 2025 CamptoCamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models


class AccountInvoice(models.Model):
    _inherit = "account.move"

    def mass_sending(self, template=None, exclude_followers=False, **kwargs):
        invoices = self.filtered(lambda i: not i.sending_in_progress)

        if kwargs.get("is_email"):
            invoices = invoices.filtered(lambda i: i.partner_id.email)
        if invoices:
            invoices.write(
                {
                    "sending_in_progress": True,
                }
            )
            for invoice in invoices:
                if kwargs.get("is_email"):
                    description = _("Send invoice %(name)s by email", name=invoice.name)
                else:
                    description = _("Print invoice %(name)s", name=invoice.name)

                if not kwargs.get("is_direct_print"):
                    kwargs = {}

                invoice.with_delay(
                    description=description,
                    channel="root.account_invoice_mass_sending_channel",
                )._send_invoice_individually(
                    template=template, exclude_followers=exclude_followers, **kwargs
                )
        return invoices

    def _send_invoice_individually(
        self, template=None, exclude_followers=False, **kwargs
    ):
        self.ensure_one()

        if not kwargs.get("is_direct_print"):
            return super()._send_invoice_individually(
                template=template, exclude_followers=exclude_followers
            )

        res = self.action_invoice_sent()
        wiz_ctx = res["context"] or {}
        wiz_ctx.update(
            {
                "active_model": self._name,
                "active_ids": self.ids,
                "active_id": self.id,
                "discard_logo_check": True,
                "account_invoice_mass_sending": True,
                "exclude_followers": exclude_followers,
            }
        )
        wiz = self.env["account.invoice.send"].with_context(**wiz_ctx).create({})
        wiz.write(
            {
                "is_print": kwargs.get("is_print"),
                "is_email": kwargs.get("is_email"),
                "is_direct_print": kwargs.get("is_direct_print"),
                "template_id": template.id if template else None,
                "composition_mode": "comment",
            }
        )
        wiz.onchange_template_id()
        self.write(
            {
                "sending_in_progress": False,
            }
        )
        return wiz.send_and_print_action()
