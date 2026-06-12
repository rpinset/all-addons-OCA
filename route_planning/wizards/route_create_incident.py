# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RouteCreateIncident(models.TransientModel):
    _name = "route.create.incident"
    _description = "Create Route Incident"

    checkpoint_id = fields.Many2one("route.checkpoint", string="Checkpoint")
    incident_type_id = fields.Many2one("route.incident.type", required=True)
    note = fields.Text()

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self._context.get("active_ids") or []
        active_model = self._context.get("active_model")
        if active_model == "route.checkpoint" and len(active_ids) == 1:
            res["checkpoint_id"] = active_ids[0]
        return res

    def action_create_incident(self):
        self.checkpoint_id._action_create_incident(self.incident_type_id, self.note)
        return {"type": "ir.actions.act_window_close"}
