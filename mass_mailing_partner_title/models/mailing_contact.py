from odoo import api, fields, models


class MailingContact(models.Model):
    _inherit = "mailing.contact"

    title_id = fields.Many2one(comodel_name="res.partner.title", string="Title")

    @api.onchange("partner_id")
    def _onchange_partner_mass_mailing_partner(self):
        res = super()._onchange_partner_mass_mailing_partner()
        if self.partner_id:
            self.title_id = self.partner_id.title_id
        return res

    def _prepare_partner(self):
        vals = super()._prepare_partner()
        vals["title_id"] = self.title_id.id
        return vals

    def write(self, vals):
        # If partner_id is changing, sync dependent fields from partner
        # to ensure consistency
        if "partner_id" in vals and vals["partner_id"]:
            partner = self.env["res.partner"].browse(vals["partner_id"])
            vals["title_id"] = partner.title_id.id
        return super().write(vals)
