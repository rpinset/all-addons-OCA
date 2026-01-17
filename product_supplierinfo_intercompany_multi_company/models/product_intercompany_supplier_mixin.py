from odoo import models


class ProductIntercompanySupplierMixin(models.AbstractModel):
    _inherit = "product.intercompany.supplier.mixin"

    def _synchronise_supplier_info_for_record(self, pricelist, supplierinfo):
        res = super()._synchronise_supplier_info_for_record(pricelist, supplierinfo)
        if (
            self._has_intercompany_price(pricelist)
            and self.company_id == pricelist.company_id
        ):
            supplierinfo.sudo().unlink()
        return res

    def _condition_supplierinfo_create_or_update(self, pricelist, supplierinfo):
        res = super()._condition_supplierinfo_create_or_update(pricelist, supplierinfo)
        return res and (
            not self.company_ids
            or (
                pricelist.company_id in self.company_ids
                and pricelist.company_id != self.company_ids
            )
        )
