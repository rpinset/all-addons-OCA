from odoo import fields, models


class PackageType(models.Model):
    _inherit = "stock.package.type"

    package_carrier_type = fields.Selection(
        selection_add=[("laposte_fr", "La Poste")],
        ondelete={"laposte_fr": "set default"},
    )
