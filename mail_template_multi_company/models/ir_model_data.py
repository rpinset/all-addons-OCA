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
        if (
            res_model == "mail.template"
            and res_id
            and self.env["ir.model.access"].check(
                res_model,
                "read",
                raise_exception=False,
            )
        ):
            original_res_id = res_id
            module, xmlid = xmlid.split(".")
            res_model, res_id = self.check_object_reference(
                module,
                xmlid,
                raise_on_access_error=raise_if_not_found,
            )
            if not res_id:
                # Fallback on the first substitute that can be accessed
                template_sudo = self.env["mail.template"].sudo().browse(original_res_id)
                substitutes = template_sudo.substitute_xmlid_mail_template_ids
                accessible_substitute = self.env["mail.template"].search(
                    [
                        ("id", "in", substitutes.ids),
                    ],
                    limit=1,
                )
                res_id = accessible_substitute.id
        return res_model, res_id
