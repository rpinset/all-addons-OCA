# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import api, fields, models


class CrowdfundingInvoicingWizard(models.TransientModel):
    _name = "crowdfunding.invoicing.wizard"
    _description = "Crowdfunding Invoicing Wizard"

    percentage = fields.Float(default=1)
    percentage_paid = fields.Float(compute="_compute_percentage_paid", readonly=True)
    challenge_ids = fields.Many2many("crowdfunding.challenge")
    vendor_bill_ids = fields.Many2many(
        "account.move",
        compute="_compute_vendor_bill_ids",
        string="Existing vendor bills",
    )

    def default_get(self, fields_list):
        result = super().default_get(fields_list)
        if "challenge_ids" in fields_list and "challenge_ids" not in result:
            result["challenge_ids"] = [(6, 0, self.env.context.get("active_ids", []))]
        return result

    @api.depends("challenge_ids")
    def _compute_percentage_paid(self):
        for this in self:
            this.percentage_paid = sum(
                this.mapped("challenge_ids.vendor_amount")
            ) / sum(this.mapped("challenge_ids.claimed_partner_amount"))

    @api.depends("challenge_ids")
    def _compute_vendor_bill_ids(self):
        for this in self:
            this.vendor_bill_ids = this.challenge_ids.vendor_bill_ids.filtered(
                lambda x: x.state != "cancel"
            )

    def action_invoice(self):
        invoices = self.challenge_ids._in_invoice(self.percentage)
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "account.action_move_in_invoice_type",
        )
        action["domain"] = [("id", "in", invoices.ids)]
        return action

    @api.onchange("vendor_bill_ids")
    def _onchange_vendor_bill_ids(self):
        if self.vendor_bill_ids:
            self.percentage = 0
