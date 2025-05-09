# @author: Valerio Paretta <valerioparetta@innovyou.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _post(self, soft=True):
        edited_products = []
        if self.env.context.get("skip_must_have_dates"):
            product_ids = self.mapped("line_ids.product_id")
            for product in product_ids:
                if product.must_have_dates:
                    edited_products.append(product)
                    product.must_have_dates = False

        res = super()._post(soft=soft)

        for product in edited_products:
            if not product.must_have_dates:
                product.must_have_dates = True

        return res

    def generate_supplier_self_invoice(self):
        self.ensure_one()
        self = self.with_context(skip_must_have_dates=True)
        res = super().generate_supplier_self_invoice()
        for line in self.rc_self_purchase_invoice_id.invoice_line_ids:
            line.write(
                {
                    "start_date": False,
                    "end_date": False,
                }
            )
        return res

    def generate_self_invoice(self):
        self.ensure_one()
        self = self.with_context(skip_must_have_dates=True)
        return super().generate_self_invoice()
