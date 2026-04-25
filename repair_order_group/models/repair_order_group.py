# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class RepairOrderGroup(models.Model):
    """Model representing a group of related repair orders.

    The group allows multiple repairs for the same customer to be
    managed together — for example, confirmed simultaneously or
    merged into one sales quotation.

    Automatically assigned a unique sequence-based name.
    """

    _name = "repair.order.group"
    _description = "Repair Order Group"

    name = fields.Char(default="New", required=True, index=True)
    partner_id = fields.Many2one(
        "res.partner", compute="_compute_partner_company", store=True
    )
    company_id = fields.Many2one(
        "res.company", compute="_compute_partner_company", store=True
    )
    repair_ids = fields.One2many("repair.order", "group_id")
    repair_count = fields.Integer(compute="_compute_repair_count", store=True)

    @api.depends("repair_ids.partner_id", "repair_ids.company_id")
    def _compute_partner_company(self):
        for g in self:
            r = g.repair_ids[:1]
            g.partner_id = r.partner_id if r else False
            g.company_id = r.company_id if r else False

    @api.depends("repair_ids")
    def _compute_repair_count(self):
        for group in self:
            group.repair_count = len(group.repair_ids)

    @api.model_create_multi
    def create(self, vals_list):
        """Assign sequence when records are created programmatically."""
        seq_env = self.env["ir.sequence"]
        for vals in vals_list:
            if vals.get("name", "New") in (False, "New"):
                vals["name"] = seq_env.next_by_code("repair.order.group") or "New"
        return super().create(vals_list)
