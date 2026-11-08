# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    zone_in_date_update_out_of_zone = fields.Boolean(
        string="Update Zone Entry Date out of Zones",
        help="Update the zone entry date when goods are moved to a location"
        " that is in no zone. Off by default, as no zone-based removal"
        " strategy sorts them there.",
    )
