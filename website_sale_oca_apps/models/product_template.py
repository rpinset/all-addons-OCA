from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    was_odoo_app = fields.Boolean()
