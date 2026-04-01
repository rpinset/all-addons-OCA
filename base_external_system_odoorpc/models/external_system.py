# Copyright 2026 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ExternalSystem(models.Model):
    """Extend base external system"""

    _inherit = "external.system"

    db_name = fields.Char(
        string="Database",
        help="Input database name",
    )
    is_ssl = fields.Boolean(
        string="SSL",
        help="Change protocol if SSL",
    )
