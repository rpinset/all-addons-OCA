# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.tools.safe_eval import safe_eval


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = "product.template"

    def action_see_product_variant_attachments(self):
        domain = [
            ("res_model", "=", "product.product"),
            ("res_id", "in", self.product_variant_ids.ids),
        ]
        action = self.env["ir.actions.actions"]._for_xml_id("base.action_attachment")
        context = action.get("context", "{}")
        context = safe_eval(context)
        context["create"] = False
        context["edit"] = False
        action.update({"domain": domain, "context": context})
        return action
