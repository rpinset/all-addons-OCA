# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models
from odoo.exceptions import UserError


class Opportunity2Rfq(models.TransientModel):
    _name = "srm.rfq.partner"
    _description = "Create new or use existing Supplier on new RFQ"

    @api.model
    def default_get(self, field_list):
        result = super().default_get(field_list)

        if self.env.context.get("active_model") != "crm.lead":
            raise UserError(self.env._("You can only apply this action from a lead."))

        lead = self.env["crm.lead"]
        lead_id = result.get("lead_id") or (
            self.env.context.get("active_id") if "lead_id" in field_list else False
        )
        if lead_id:
            lead = self.env["crm.lead"].browse(lead_id)
            result["lead_id"] = lead.id

            partner_id = result.get("partner_id") or lead._find_matching_partner().id

            if "action" in field_list and not result.get("action"):
                result["action"] = "exist" if partner_id else "create"
            if "partner_id" in field_list and not result.get("partner_id"):
                result["partner_id"] = partner_id

        return result

    action = fields.Selection(
        selection=[
            ("create", "Create a new vendor"),
            ("exist", "Link to an existing vendor"),
            ("nothing", "Do not link to a vendor"),
        ],
        string="RFQ Vendor",
        required=True,
    )
    lead_id = fields.Many2one(
        comodel_name="crm.lead", string="Associated Lead", required=True
    )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Vendor")

    def action_apply(self):
        """Create/link vendor if requested, then open the RFQ form."""
        self.ensure_one()
        if self.action == "create":
            self.lead_id._handle_partner_assignment(create_missing=True)
        elif self.action == "exist":
            self.lead_id._handle_partner_assignment(
                force_partner_id=self.partner_id.id,
                create_missing=False,
            )
        return self.lead_id.action_rfq_new()
