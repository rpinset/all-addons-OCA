# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class IRModelData(models.Model):
    _inherit = "ir.model.data"

    @api.model
    def xmlid_to_res_model_res_id(self, xmlid, raise_if_not_found=False):
        res_model, res_id = super().xmlid_to_res_model_res_id(
            xmlid,
            raise_if_not_found=raise_if_not_found,
        )
        if res_model == "mail.template" and res_id:
            module, xmlid = xmlid.split(".")
            res_model, res_id = self.check_object_reference(
                module,
                xmlid,
                raise_on_access_error=raise_if_not_found,
            )
        return res_model, res_id
