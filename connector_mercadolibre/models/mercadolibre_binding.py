# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MercadoLibreBinding(models.AbstractModel):
    _name = "mercadolibre.binding"
    _inherit = "external.binding"
    _description = "Mercado Libre Binding"

    state = fields.Selection(
        selection=[
            ("pending", "Pending"),
            ("synced", "Synced"),
            ("error", "Error"),
        ],
        required=True,
        default="pending",
        index=True,
    )
    error_message = fields.Text(readonly=True)

    def mark_synced(self):
        self.write(
            {
                "state": "synced",
                "error_message": False,
                "sync_date": fields.Datetime.now(),
            }
        )

    def mark_error(self, message):
        self.write({"state": "error", "error_message": message})

    def button_retry(self):
        """Reset the binding. Concrete models enqueue the next job."""
        self.write({"state": "pending", "error_message": False})
