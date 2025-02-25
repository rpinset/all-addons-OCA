# Copyright 2016-Today: GRAP (http://www.grap.coop)
# Copyright Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _is_matching_supplierinfo(self, supplierinfo):
        res = super()._is_matching_supplierinfo(supplierinfo)
        discount = self.discount1 if "discount1" in self._fields else self.discount
        return res and (discount == supplierinfo.discount)

    def _prepare_supplier_wizard_line(self, supplierinfo):
        res = super()._prepare_supplier_wizard_line(supplierinfo)
        discount = self.discount1 if "discount1" in self._fields else self.discount
        res.update(
            {
                "current_discount": supplierinfo and supplierinfo.discount,
                "new_discount": discount,
            }
        )
        return res
