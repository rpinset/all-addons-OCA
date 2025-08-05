# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    alternative_pricelist_ids = fields.Many2many(
        comodel_name="product.pricelist",
        string="Alternative pricelists",
        relation="product_pricelist_alternative_rel",
        column1="origin_id",
        column2="alternative_id",
        domain="[('id', '!=', id)]",
    )
    is_alternative_to_pricelist_ids = fields.Many2many(
        comodel_name="product.pricelist",
        string="Is alternative to pricelists",
        relation="product_pricelist_alternative_rel",
        column1="alternative_id",
        column2="origin_id",
    )
    is_alternative_to_pricelist_count = fields.Integer(
        compute="_compute_is_alternative_to_pricelist_count"
    )

    @api.depends("is_alternative_to_pricelist_ids")
    def _compute_is_alternative_to_pricelist_count(self):
        groups = self.read_group(
            [("alternative_pricelist_ids", "in", self.ids)],
            ["alternative_pricelist_ids"],
            "alternative_pricelist_ids",
            lazy=False,
        )
        data = {
            group["alternative_pricelist_ids"][0]: group["__count"] for group in groups
        }
        for pricelist in self:
            pricelist.is_alternative_to_pricelist_count = data.get(pricelist.id, 0)

    def action_view_is_alternative_to_pricelist(self):
        self.ensure_one()
        action = {
            "type": "ir.actions.act_window",
            "name": _("Is Alternative to Pricelist"),
            "res_model": "product.pricelist",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.is_alternative_to_pricelist_ids.ids)],
            "context": dict(self.env.context, create=False),
        }
        if self.is_alternative_to_pricelist_count == 1:
            action.update(
                {"view_mode": "form", "res_id": self.is_alternative_to_pricelist_ids.id}
            )
        return action

    def _compute_price_rule(self, products, qty, uom=None, date=False, **kwargs):
        res = super()._compute_price_rule(products, qty, uom=uom, date=date, **kwargs)

        # In some contexts we want to ignore alternative pricelists
        # and return the original price
        if self.env.context.get(
            "skip_alternative_pricelist", False
        ) or self.env.context.get("based_on_other_pricelist", False):
            return res
        pricelist_items_ids = [val[1] for val in res.values()]
        use_lower_price_item = (
            self.env["product.pricelist.item"]
            .browse(pricelist_items_ids)
            .filtered(lambda rec: rec.alternative_pricelist_policy == "use_lower_price")
        )
        use_lower_price_item_ids = set(use_lower_price_item.ids)

        products_with_use_lower_price = products.filtered(
            lambda rec: res[rec.id][1] in use_lower_price_item_ids
        )
        for alternative_pricelist in self.alternative_pricelist_ids:
            alternative_res = alternative_pricelist._compute_price_rule(
                products_with_use_lower_price, qty, uom, date, **kwargs
            )
            for product_id, (
                alternative_price,
                alternative_item_id,
            ) in alternative_res.items():
                if alternative_price < res[product_id][0]:
                    res[product_id] = (alternative_price, alternative_item_id)
        return res

    @api.constrains("alternative_pricelist_ids")
    def _check_pricelist_alternative_items_based_on_other_pricelist(self):
        """Alternative pricelists can not contain items based on other pricelist"""
        for pricelist in self:
            if pricelist.alternative_pricelist_ids.item_ids.filtered(
                lambda item: item.compute_price == "formula"
                and item.base == "pricelist"
            ):
                raise ValidationError(
                    _(
                        "Formulas based on another pricelist are not allowed "
                        "on alternative pricelists."
                    )
                )
