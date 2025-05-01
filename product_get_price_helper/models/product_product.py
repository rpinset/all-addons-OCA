# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# Copyright 2021 Camptocamp (http://www.camptocamp.com).
# @author Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.tools import float_compare, float_is_zero

from ..utils import float_round


class ProductProduct(models.Model):

    _inherit = "product.product"

    def _get_price(
        self, qty=1.0, pricelist=None, fposition=None, company=None, date=None
    ):
        """Computes the product prices

        :param qty:         The product quantity, used to apply pricelist rules.
        :param pricelist:   Optional. Get prices for a specific pricelist.
        :param fposition:   Optional. Apply fiscal position to product taxes.
        :param company:     Optional.
        :param date:        Optional.

        :returns: A dictionary where keys are product IDs and values are dictionaries with:

            <value>                 The product unitary price
            <tax_included>          True if product taxes are included in <price>.

            If the pricelist.discount_policy is "without_discount":
            <original_value>        The original price (before pricelist is applied).
            <discount>              The discounted percentage.
        """
        AccountTax = self.env["account.tax"]
        DecimalPrecision = self.env["decimal.precision"]
        price_dp = DecimalPrecision.precision_get("Product Price")
        discount_dp = DecimalPrecision.precision_get("Discount")

        company = company or self.env.company
        product_context = dict(
            self.env.context,
            quantity=qty,
            pricelist=pricelist.id if pricelist else None,
            fiscal_position=fposition,
            date=date,
        )

        # Prefetch related fields to avoid N+1
        self = self.with_company(company).with_context(**product_context)
        self.read(["lst_price", "taxes_id"])

        # Apply fiscal position + filter by company
        taxes_map = {}
        for product in self:
            taxes = product.taxes_id.filtered(lambda tax: tax.company_id == company)
            if fposition:
                taxes = fposition.map_tax(taxes)
            taxes_map[product.id] = taxes

        result = {}

        price_unit_list = []
        if pricelist:
            price_unit_list = pricelist.with_context(
                **product_context
            )._compute_price_rule(self, qty, date=date)

        for product in self:
            taxes = taxes_map[product.id]
            tax_included = any(t.price_include for t in taxes)

            if price_unit_list:
                price_unit = price_unit_list[product.id][0]
            else:
                price_unit = product.lst_price

            price_unit = AccountTax._fix_tax_included_price_company(
                price_unit, product.taxes_id, taxes, company
            )
            price_unit = float_round(price_unit, price_dp)

            res = {
                "value": price_unit,
                "tax_included": tax_included,
                "original_value": price_unit,
                "discount": 0.0,
            }

            # Handle pricelists with "without_discount" policy
            if pricelist and pricelist.discount_policy == "without_discount":
                price_unit = price_unit_list[product.id][0]
                original_price = product.lst_price

                if not float_is_zero(
                    original_price, precision_digits=price_dp
                ) and float_compare(
                    original_price, price_unit, precision_digits=price_dp
                ):
                    discount = (original_price - price_unit) / original_price * 100
                    discount = float_round(discount, discount_dp)
                else:
                    discount = 0.0

                original_price_fixed = AccountTax._fix_tax_included_price_company(
                    original_price, product.taxes_id, taxes, company
                )
                original_price_fixed = float_round(original_price_fixed, price_dp)

                res.update(
                    {
                        "original_value": original_price_fixed,
                        "discount": discount,
                    }
                )

            result[product.id] = res

        return result
