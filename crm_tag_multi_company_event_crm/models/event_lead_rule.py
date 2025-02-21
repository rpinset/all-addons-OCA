# Copyright 2025 ForgeFlow (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventLeadRule(models.Model):
    _inherit = "event.lead.rule"

    lead_tag_ids = fields.Many2many(check_company=True)
