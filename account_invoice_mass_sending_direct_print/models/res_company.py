from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    invoice_is_direct_print = fields.Boolean(string="Direct Print", default=False)
