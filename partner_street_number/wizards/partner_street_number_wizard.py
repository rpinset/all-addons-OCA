# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class PartnerStreetNumberWizard(models.TransientModel):
    _name = "partner.street.number.wizard"
    _description = "Update street components/street"

    direction = fields.Selection(
        [
            (
                "_compute_street_data",
                "Set street_name, street_number, street_number2 from street",
            ),
            ("_inverse_street_data", "Set street from component fields"),
        ],
        default="_compute_street_data",
        required=True,
    )

    def action_set(self):
        partners = self.env["res.partner"].browse(
            self.env.context.get("active_ids", [])
        )
        getattr(partners, self.direction)()
