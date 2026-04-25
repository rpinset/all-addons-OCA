# Copyright 2023-2024 Tecnativa - Víctor Martínez
# Copyright 2025 - APSL-Nagarro - Miquel Alzanillas
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import base64

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Agreement(models.Model):
    _inherit = "agreement"

    # Disable log to avoid 'Not implemented...' errors on ORM write operations
    signed_contract = fields.Binary(string="Signed Document", tracking=False)
    # This field is stored as a help to filter by.
    sign_request_ids = fields.One2many(
        comodel_name="sign.oca.request",
        inverse_name="agreement_id",
        string="Sign Requests",
    )
    sign_request_count = fields.Integer(
        string="Sign request count",
        compute="_compute_sign_request_count",
        compute_sudo=True,
        store=True,
    )

    @api.depends("sign_request_ids")
    def _compute_sign_request_count(self):
        request_data = self.env["sign.oca.request"].read_group(
            [("agreement_id", "in", self.ids)],
            ["agreement_id"],
            ["agreement_id"],
        )
        mapped_data = {
            x["agreement_id"][0]: x["agreement_id_count"] for x in request_data
        }
        for item in self:
            item.sign_request_count = mapped_data.get(item.id, 0)

    def action_send_for_signature(self):
        self.ensure_one()
        signers_list = []
        if not self.partner_contact_id:
            raise ValidationError(
                _("The agreement must have an assigned contact (counterparty).")
            )
        if not self.partner_contact_id.email:
            raise ValidationError(
                _(
                    """The agreement's counterparty contact
                    does not have an email configured."""
                )
            )
        report = self.env.ref("agreement_legal.partner_agreement_contract_document")
        pdf_document, content_type = self.env["ir.actions.report"]._render_qweb_pdf(
            report.report_name, self.ids
        )
        customer_role = self.env.ref(
            "sign_oca.sign_role_customer", raise_if_not_found=False
        )
        if not customer_role:
            raise ValidationError(
                _(
                    """The 'Customer' role for the signature
                    was not found. Please update 'agreement' module."""
                )
            )
        company_signer_role = self.env.ref(
            "agreement_sign_oca.role_agreement_signer", raise_if_not_found=False
        )
        if not company_signer_role:
            raise ValidationError(
                _(
                    """The 'Agreement Company Signatory Person' role for the signature
                    was not found. Please update 'agreement_sign_oca' module."""
                )
            )
        if self.partner_contact_id:
            signers_list.append(
                (
                    0,
                    0,
                    {
                        "role_id": customer_role.id,
                        "partner_id": self.partner_contact_id.id,
                    },
                )
            )
        else:
            raise ValidationError(
                _(
                    """Please set a Primary Contact in order to set the
                    signatory person of the counterpart in this document"""
                )
            )

        if not self.company_contact_id:
            raise ValidationError(
                _(
                    """Please set a Company Primary Contact in order to set
                    the signatory person of the company in this document"""
                )
            )
        if not self.company_contact_id.user_ids:
            raise ValidationError(
                _("Please create a user for ther company signatory person")
            )
        else:
            signers_list.append(
                (
                    0,
                    0,
                    {
                        "role_id": company_signer_role.id,
                        "partner_id": self.company_contact_id.id,
                    },
                )
            )

        sign_request_vals = {
            "name": self.name,
            "user_id": self.env.user.id,
            "data": base64.b64encode(pdf_document),
            "record_ref": f"agreement,{self.id}",
            "signer_ids": signers_list,
        }
        sign_request = self.env["sign.oca.request"].create(sign_request_vals)
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "sign_oca.sign_oca_request_act_window"
        )
        action.update(
            {
                "views": [
                    [self.env.ref("sign_oca.sign_oca_request_form_view").id, "form"]
                ],
                "res_id": sign_request.id,
            }
        )
        return action

    def action_view_sign_requests(self):
        self.ensure_one()
        result = self.env["ir.actions.act_window"]._for_xml_id(
            "sign_oca.sign_oca_request_act_window"
        )
        result["domain"] = [("id", "in", self.sign_request_ids.ids)]
        ctx = dict(self.env.context)
        ctx.update(
            {
                "default_agreement_id": self.id,
                "search_default_agreement_id": self.id,
            }
        )
        result["context"] = ctx
        return result
