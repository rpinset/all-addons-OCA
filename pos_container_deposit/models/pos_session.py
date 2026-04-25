from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_product_product(self):
        """
        Load all deposit products and add deposit related fields
        """
        result = super()._loader_params_product_product()
        result["search_params"]["fields"] += ["deposit_product_id", "is_deposit"]
        return result
