from odoo import models


class ProductIntercompanySupplierMixin(models.AbstractModel):
    _inherit = "product.intercompany.supplier.mixin"

    def _condition_supplierinfo_create_or_update(self, pricelist, supplierinfo):
        res = super()._condition_supplierinfo_create_or_update(pricelist, supplierinfo)
        return res and (
            not self.company_ids
            or (
                pricelist.company_id in self.company_ids
                and pricelist.company_id != self.company_ids
            )
        )

    def _prepare_intercompany_supplier_info(self, pricelist):
        """
        Let the compute set the company on the supplierinfo
        """
        res = super()._prepare_intercompany_supplier_info(pricelist)
        if "company_id" in res:
            del res["company_id"]
        return res
