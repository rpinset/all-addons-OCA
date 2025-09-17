# Copyright 2023 ForgeFlow, S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    default_property_product_pricelist_id = fields.Many2one(
        "product.pricelist",
        string="Default Account Pricelist",
        help="Default pricelist for this company for new partners.",
    )

    def _update_partner_pricelist_generic_property(self):
        ir_property_obj = self.env["ir.property"].sudo()
        field = self.env["ir.model.fields"]._get(
            "res.partner", "property_product_pricelist"
        )
        for record in self:
            default_property_pp = record.default_property_product_pricelist_id

            ppty = ir_property_obj.search(
                [
                    ("name", "=", "property_product_pricelist"),
                    ("company_id", "=", record.id),
                    ("fields_id", "=", field.id),
                    ("res_id", "=", False),
                ],
                limit=1,
            )
            if ppty:
                if not default_property_pp:
                    ppty.unlink()
                else:
                    ppty.write(
                        {
                            "value_reference": "product.pricelist,%s"
                            % default_property_pp.id
                        }
                    )
            elif default_property_pp:
                ir_property_obj.create(
                    {
                        "name": "property_product_pricelist",
                        "value_reference": "product.pricelist,%s"
                        % default_property_pp.id,
                        "fields_id": field.id,
                        "company_id": record.id,
                    }
                )

    @api.model_create_multi
    def create(self, vals_list):
        records = super(ResCompany, self).create(vals_list)
        records_with_props = records.filtered("default_property_product_pricelist_id")
        if records_with_props:
            records_with_props._update_partner_pricelist_generic_property()
        return records

    def write(self, vals):
        res = super(ResCompany, self).write(vals)
        if "default_property_product_pricelist_id" in vals:
            for rec in self:
                rec._update_partner_pricelist_generic_property()
        return res
