# Copyright 2022 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = [
        "purchase.order",
        "edi.exchange.consumer.mixin",
    ]

    def _edi_config_field_relation(self):
        return self.partner_id.edi_purchase_conf_ids

    # edi_record_metadata api
    def _edi_get_metadata_to_store(self, orig_vals):
        data = super()._edi_get_metadata_to_store(orig_vals)
        line_vals_by_edi_id = {}
        for line_vals in orig_vals.get("order_line", []):
            vals = line_vals[-1]
            edi_id = vals.get("edi_id")
            if edi_id:
                line_vals_by_edi_id[edi_id] = vals
        data.update({"orig_values": {"lines": line_vals_by_edi_id}})
        return data
