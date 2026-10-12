# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaquilaVanWizard(models.TransientModel):
    _name = "l10n_py.maquila.van.wizard"
    _description = "VAN (National Added Value) Calculation Wizard"

    program_id = fields.Many2one(
        "l10n_py.maquila.program",
        required=True,
        domain="[('state', '=', 'active')]",
    )
    period_start = fields.Date(required=True)
    period_end = fields.Date(required=True)
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.ref("base.USD"),
    )
    total_cost = fields.Monetary(
        readonly=True,
    )
    national_cost = fields.Monetary(
        string="National Cost (PY)",
        readonly=True,
    )
    mercosul_cost = fields.Monetary(
        readonly=True,
    )
    imported_cost = fields.Monetary(
        readonly=True,
    )
    van_amount = fields.Monetary(
        string="VAN Amount",
        compute="_compute_van",
    )
    van_percentage = fields.Float(
        string="VAN %",
        compute="_compute_van",
    )
    mercosul_content = fields.Float(
        string="Mercosul Content %",
        compute="_compute_van",
    )

    @api.depends("total_cost", "mercosul_cost", "imported_cost")
    def _compute_van(self):
        for wiz in self:
            # National added value = total cost minus foreign-origin inputs
            # (imported + Mercosul), so VAN and total_cost share the same base.
            foreign_cost = wiz.mercosul_cost + wiz.imported_cost
            wiz.van_amount = wiz.total_cost - foreign_cost
            if wiz.total_cost:
                wiz.van_percentage = (wiz.van_amount / wiz.total_cost) * 100
                wiz.mercosul_content = (
                    (wiz.van_amount + wiz.mercosul_cost) / wiz.total_cost
                ) * 100
            else:
                wiz.van_percentage = 0.0
                wiz.mercosul_content = 0.0

    def action_compute(self):
        """Compute the VAN via the shared program method so the wizard and the
        CNIME report always report the same figure."""
        self.ensure_one()
        vals = self.program_id._maquila_van_for_period(
            self.period_start, self.period_end
        )
        self.total_cost = vals["total_cost"]
        self.national_cost = vals["national_cost"]
        self.mercosul_cost = vals["mercosul_cost"]
        self.imported_cost = vals["imported_cost"]
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }
