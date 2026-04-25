from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def write(self, vals):
        result = super().write(vals)
        if "title_id" in vals:
            self.env["mailing.contact"].sudo().search(
                [("partner_id", "in", self.ids)]
            ).write({"title_id": vals["title_id"]})
        return result
