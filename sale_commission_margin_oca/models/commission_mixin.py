# Copyright 2025 Dixmit - Luis Rodríguez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CommissionMixin(models.AbstractModel):
    _inherit = "commission.mixin"

    agent_ids = fields.One2many(
        compute="_compute_agent_ids",
        store=True,
        precompute=True,
    )

    commission_free = fields.Boolean(
        compute="_compute_commission_free",
        store=True,
        precompute=True,
    )


class CommissionLineMixin(models.AbstractModel):
    _inherit = "commission.line.mixin"

    commission_id = fields.Many2one(
        compute="_compute_commission_id",
        store=True,
        precompute=True,
    )

    amount = fields.Monetary(
        compute="_compute_amount",
        store=True,
        precompute=True,
    )
