# Copyright 2023 Tecnativa - Víctor Martínez
# Copyright 2025 - APSL-Nagarro - Miquel Alzanillas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    agreement_sign_oca_template_id = fields.Many2one(
        comodel_name="sign.oca.template",
        related="company_id.agreement_sign_oca_template_id",
        string="Default Agreement Sign Template",
        readonly=False,
    )

    agreement_sign_oca_signed_stage_id = fields.Many2one(
        comodel_name="agreement.stage",
        related="company_id.agreement_sign_oca_signed_stage_id",
        string="Signed Agreements Stage",
        readonly=False,
    )
