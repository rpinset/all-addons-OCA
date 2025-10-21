from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    invoice_legal_notes = fields.Html(translate=True)
