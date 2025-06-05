# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class WizardAuthPartnerForceSetPassword(models.TransientModel):
    _name = "wizard.auth.partner.force.set.password"
    _description = "Wizard Partner Auth Reset Password"

    password = fields.Char(required=True)
    password_confirm = fields.Char(string="Confirm Password", required=True)

    @api.constrains("password", "password_confirm")
    def _check_password(self):
        for wizard in self:
            if wizard.password != wizard.password_confirm:
                raise ValidationError(
                    _("Password and Confirm Password must be the same")
                )

    def action_force_set_password(self):
        self.ensure_one()
        if self.env.context.get("active_model") != "auth.partner":
            raise UserError(_("This wizard can only be used on auth.partner"))
        auth_partner_id = self.env.context.get("active_id")
        if not auth_partner_id:
            raise UserError(_("No active_id in context"))

        auth_partner = self.env["auth.partner"].browse(auth_partner_id)

        auth_partner.write({"password": self.password})

        return {"type": "ir.actions.act_window_close"}
