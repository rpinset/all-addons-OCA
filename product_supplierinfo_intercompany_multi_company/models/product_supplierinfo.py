from odoo import api, fields, models


class ProductSupplierinfo(models.Model):
    _inherit = ["multi.company.abstract", "product.supplierinfo"]
    _name = "product.supplierinfo"
    _description = "Supplier Pricelist (Multi-Company)"

    company_ids = fields.Many2many(
        string="Companies",
        comodel_name="res.company",
        compute="_compute_company_ids",
        store=True,
    )

    @api.depends("product_id.company_ids", "product_tmpl_id.company_ids")
    def _compute_company_ids(self):
        for rec in self.with_context(automatic_intercompany_sync=True):
            product = rec.product_id or rec.product_tmpl_id
            rec.company_ids = product.company_ids

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for rec in res:
            # the default value of company_id is automatically set
            # so we need to force the computation on creation
            if rec.intercompany_pricelist_id:
                rec._compute_company_ids()
        return res
