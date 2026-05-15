# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TierDefinition(models.Model):
    _inherit = "tier.definition"

    require_authentication = fields.Boolean(
        help="If enabled, the user will be asked to authenticate "
        "himself in order to validate or reject the tier.",
        default=False,
    )
