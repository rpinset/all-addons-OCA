# Copyright 2025 Moduon Team S.L. <info@moduon.team>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from datetime import timedelta

from odoo import fields, models


class MailComposer(models.TransientModel):
    _inherit = "mail.compose.message"

    def _prepare_mail_values_rendered(self, res_ids):
        result = super()._prepare_mail_values_rendered(res_ids)
        for res_id in res_ids:
            if not result[res_id].get("scheduled_date"):
                result[res_id]["scheduled_date"] = fields.Datetime.now() + timedelta(
                    seconds=30
                )
        return result
