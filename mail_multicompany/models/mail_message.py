# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MailMessage(models.Model):

    _inherit = "mail.message"

    company_id = fields.Many2one("res.company", "Company")

    @api.model_create_multi
    def create(self, values_list):
        context = self.env.context
        for vals in values_list:
            # When using mail.message.composer model and res_id are not defined but
            # they are in the context.
            if not vals.get("model") and context.get("active_model"):
                vals["model"] = context.get("active_model")
            if not vals.get("res_id") and context.get("active_id"):
                vals["res_id"] = context.get("active_id")
            if vals.get("model") and vals.get("res_id"):
                current_object = self.env[vals["model"]].browse(vals["res_id"])
                if hasattr(current_object, "company_id") and current_object.company_id:
                    vals["company_id"] = current_object.company_id.id
                # when the object has no company, we try with the user,
                # e.g. portal.wizard.user
                elif (hasattr(current_object, "user_id") and
                      current_object.user_id.company_id):
                    vals["company_id"] = current_object.user_id.company_id.id
            if not vals.get("company_id"):
                vals["company_id"] = self.env.user.company_id.id
            # Search SMTP server with company_id or shared SMTP server
            if not vals.get("mail_server_id"):
                vals["mail_server_id"] = (
                    self.sudo()
                    .env["ir.mail_server"]
                    .search(
                        ['|', ("company_id", "=", vals.get("company_id", False)),
                            ("company_id", "=", False)],
                        order="sequence",
                        limit=1,
                    )
                    .id
                )
        return super(MailMessage, self).create(values_list)
