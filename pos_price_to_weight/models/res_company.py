# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class ResCompany(models.Model):
    _name = "res.company"
    _inherit = "res.company"

    is_price_to_weight_tax_included = fields.Boolean(
        string="Price (Computed Weight) Barcodes Include Taxes", default=True
    )
