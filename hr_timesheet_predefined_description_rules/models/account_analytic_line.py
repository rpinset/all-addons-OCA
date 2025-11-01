# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    free_text = fields.Char(
        string="Additional Description",
        help=(
            "Free text. If the predefined description has 'append_free_text_to_name' enabled, "
            "it will be auto-completed with the predefined description."
        ),
    )
    allow_free_text_related = fields.Boolean(
        related="predefined_description_id.allow_free_text"
    )

    def write(self, vals):
        for rec in self:
            predef_id = vals.get("predefined_description_id") or (
                rec.predefined_description_id.id
                if rec.predefined_description_id
                else False
            )
            predef = (
                self.env["timesheet.predefined.description"].browse(predef_id).exists()
                if predef_id
                else None
            )

            if predef and (rec.task_id or rec.ticket_id):
                user_text = (vals.get("free_text") or rec.free_text or "").strip()

                if predef.free_text_required and not user_text:
                    raise UserError(
                        _(
                            "You must add additional information "
                            "for this predefined description."
                        )
                    )

                if predef.append_free_text_to_name and user_text:
                    vals["name"] = f"{predef.name}. {user_text}"
                else:
                    vals["name"] = predef.name

        return super().write(vals)
