# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    is_price_to_weight_tax_included = fields.Boolean(
        related="company_id.is_price_to_weight_tax_included"
    )
