# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def message_post_with_template(
        self, template_id, email_layout_xmlid=None, **kwargs
    ):
        # OVERRIDE to force the email_layout_xmlid defined on the mail.template
        template = self.env["mail.template"].sudo().browse(template_id)
        if template.force_email_layout_id:
            email_layout_xmlid = template.force_email_layout_id.xml_id
        return super().message_post_with_template(
            template_id, email_layout_xmlid=email_layout_xmlid, **kwargs
        )

    def _notify_record_by_email(
        self,
        message,
        recipients_data,
        msg_vals=False,
        model_description=False,
        mail_auto_delete=True,
        check_existing=False,
        force_send=True,
        send_after_commit=True,
        **kwargs
    ):
        msg_vals = msg_vals or {}
        layout_xmlid = (
            msg_vals.get("email_layout_xmlid")
            or message.email_layout_xmlid
            or "mail.message_notification_email"
        )
        layout = self.env.ref(layout_xmlid, raise_if_not_found=True)
        res_model = (
            self.env["ir.model"].sudo().search([("model", "=", self._name)], limit=1)
        )
        mapping = self.env["email.layout.mapping"].search(
            [("layout_id", "=", layout.id), ("model_ids", "in", res_model.ids)],
            limit=1,
        )
        if not mapping:
            mapping = self.env["email.layout.mapping"].search(
                [("layout_id", "=", layout.id), ("model_ids", "=", False)], limit=1
            )
        if mapping:
            substitute_layout = mapping.substitute_layout_id
            if not substitute_layout.xml_id:
                substitute_layout._export_rows([["id"]])
            msg_vals["email_layout_xmlid"] = mapping.substitute_layout_id.xml_id
        return super()._notify_record_by_email(
            message,
            recipients_data,
            msg_vals=msg_vals,
            model_description=model_description,
            mail_auto_delete=mail_auto_delete,
            check_existing=check_existing,
            force_send=force_send,
            send_after_commit=send_after_commit,
            **kwargs
        )
