# Copyright 2023 Tecnativa - Víctor Martínez
# Copyright 2025 - APSL-Nagarro - Miquel Alzanillas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    def _default_signed_stage(self):
        default_active_stage = self.env.ref(
            "agreement_legal.agreement_stage_active", raise_if_not_found=False
        )
        return default_active_stage

    agreement_sign_oca_template_id = fields.Many2one(
        comodel_name="sign.oca.template",
        domain="[('model_id.model', '=', 'agreement')]",
        string="Default Agreement Sign Template",
    )
    agreement_sign_oca_signed_stage_id = fields.Many2one(
        comodel_name="agreement.stage",
        default=_default_signed_stage,
        string="Signed Agreements Stage",
        required=True,
    )
