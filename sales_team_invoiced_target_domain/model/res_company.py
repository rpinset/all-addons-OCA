from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    crm_team_invoiced_domain = fields.Char(
        default="['|', '|', "
        "['payment_state', '=', 'in_payment'], "
        "['payment_state', '=', 'paid'], "
        "['payment_state', '=', 'reversed']]"
    )
