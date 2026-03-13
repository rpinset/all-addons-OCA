# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    intermediary_bank_id = fields.Many2one(
        string="Intermediary Bank",
        comodel_name="res.bank",
        help="Bank used as intermediary for international payments",
    )
