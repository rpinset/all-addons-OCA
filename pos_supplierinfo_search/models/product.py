import json

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    supplier_data_json = fields.Char(
        "Supplier data dict",
        help="Technical field: Used in POS frontend to search products by supplierinfo",
        compute="_compute_supplier_data_json",
    )

    def _compute_supplier_data_json(self):
        for rec in self:
            rec.supplier_data_json = json.dumps(
                [
                    {
                        "supplier_name": s.partner_id.display_name,
                        "supplier_product_code": s.product_code or "",
                        "supplier_product_name": s.product_name or "",
                    }
                    for s in rec.product_tmpl_id.seller_ids
                ]
            )

    @api.model
    def _load_pos_data_fields(self, config_id):
        res = super()._load_pos_data_fields(config_id)
        res.append("supplier_data_json")
        return res
