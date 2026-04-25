# Copyright 2023 Tecnativa - Víctor Martínez
# Copyright 2025 - APSL-Nagarro - Miquel Alzanillas
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class SignOcaRequest(models.Model):
    _inherit = "sign.oca.request"

    # This field is required for the inverse of maintenance.equipment.
    agreement_id = fields.Many2one(
        comodel_name="agreement",
        compute="_compute_agreement_id",
        string="Agreement",
        readonly=True,
        store=True,
    )

    @api.depends("record_ref")
    def _compute_agreement_id(self):
        for item in self.filtered(
            lambda x: x.record_ref and x.record_ref._name == "agreement"
        ):
            item.agreement_id = item.record_ref.id

    def action_send_signed_request(self):
        res = super().action_send_signed_request()
        customer_role = self.env.ref(
            "sign_oca.sign_role_customer", raise_if_not_found=False
        )
        company_signer_role = self.env.ref(
            "agreement_sign_oca.role_agreement_signer", raise_if_not_found=False
        )

        for request in self:
            if request.state == "2_signed" and request.agreement_id and request.data:
                signed_stage_id = (
                    request.env.company.agreement_sign_oca_signed_stage_id.id
                )
                signed_partner_on = False
                signer_partner_contact_id = False
                signed_company_on = False
                signer_company_contact_id = False
                for signer in request.signer_ids:
                    if signer.role_id == customer_role:
                        signer_partner_contact_id = signer.partner_id.id
                        signed_partner_on = signer.signed_on
                    elif signer.role_id == company_signer_role:
                        if signer.partner_id.user_ids:
                            signer_company_contact_id = signer.partner_id.user_ids[0].id
                        signed_company_on = signer.signed_on
                vals = {
                    "partner_signed_date": signed_partner_on,
                    "partner_signed_user_id": signer_partner_contact_id,
                    "company_signed_date": signed_company_on,
                    "company_signed_user_id": signer_company_contact_id,
                    "stage_id": signed_stage_id,
                    "signed_contract": request.data,
                    "signed_contract_filename": request.name,
                }
                vals = {k: v for k, v in vals.items() if v}
                if vals:
                    request.agreement_id.sudo().write(vals)
        return res
