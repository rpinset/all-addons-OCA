from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    invoice_is_direct_print = fields.Boolean(
        string="Invoice Is Direct Print",
        related="company_id.invoice_is_direct_print",
        readonly=False,
        help=(
            "Allows the invoice to be printed automatically via a background job "
            "when using the `Send & Print` wizard."
        ),
    )
