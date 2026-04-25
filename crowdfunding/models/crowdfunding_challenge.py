# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import _, api, exceptions, fields, models, tools

from odoo.addons.http_routing.models.ir_http import slug


def _extend_context_str(context_str, **kwargs):
    context_str = context_str.strip() or "{}"
    return (
        context_str[:-1]
        + ("," if len(context_str) > 2 else "")
        + (",".join(f"'{key}': {repr(value)}" for key, value in kwargs.items()))
        + "}"
    )


class CrowdfundingChallenge(models.Model):
    _name = "crowdfunding.challenge"
    _description = "Crowdfunding challenge"
    _inherit = [
        "mail.thread",
        "website.published.mixin",
        "website.seo.metadata",
        "website.cover_properties.mixin",
    ]
    _mail_post_access = "read"
    _mail_flat_thread = False

    name = fields.Char(required=True, tracking=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("open", "Open"),
            ("claimed", "Claimed"),
            ("submitted", "Submitted"),
            ("done", "Done"),
        ],
        default="draft",
        tracking=True,
        help="Draft: The challenge is in preparation\n"
        "Open: The challenge is visible for users, payments can be done\n"
        "Claimed: Somebody has been assigned to work on the challenge, "
        "payments can be done\n"
        "Submitted: Work is submitted, no further payments possible\n"
        "Done: Work is done, all payments done",
    )
    description = fields.Html()
    description_url = fields.Char(
        "Description URL", help="URL for more information about this challenge"
    )
    description_image = fields.Binary(
        help="Image that will be displayed on the challenge description"
    )
    claimed_partner_id = fields.Many2one("res.partner", string="Vendor", tracking=True)
    target_amount = fields.Monetary(tracking=True)
    fee_amount = fields.Monetary(
        compute="_compute_amounts",
        store=True,
        readonly=True,
        string="Commission Fee Amount",
        help="When a challenge is claimed, this amount will be deducted "
        "from the total amount pledged to cover overhead costs",
    )
    fee_percentage = fields.Float(
        default=lambda self: self._default_fee_percentage(),
        string="Commission Fee %",
    )
    claimed_partner_amount = fields.Monetary(
        compute="_compute_amounts",
        store=True,
        readonly=True,
        string="Unposted Vendor Amount",
        help="The amount to be paid out",
    )
    funding_state = fields.Selection(
        [
            ("needs_funding", "Needs funding"),
            ("funded", "Funded"),
        ],
        compute="_compute_funding_state",
        store=True,
        readonly=True,
        tracking=True,
    )
    pledged_percentage = fields.Float(
        string="Pledged %",
        compute="_compute_funding_state",
        readonly=True,
        store=True,
        tracking=True,
    )
    pledged_amount = fields.Monetary(
        compute="_compute_invoices",
        readonly=True,
        store=True,
        tracking=True,
    )
    pledged_amount_total = fields.Monetary(
        string="Pledges Total",
        compute="_compute_invoices",
        readonly=True,
        store=True,
        tracking=True,
    )
    pledged_amount_unpaid = fields.Monetary(
        string="Unposted Pledges",
        compute="_compute_invoices",
        readonly=True,
        store=True,
        tracking=True,
    )
    pledge_default_amount = fields.Monetary(
        "Default Pledge Amount",
        help="Fill in a proposed amount pledgers can modify",
    )
    invoice_count = fields.Integer(compute="_compute_invoices", store=True)
    invoice_ids = fields.One2many(
        "account.move",
        "crowdfunding_challenge_id",
        domain=[("move_type", "in", ["out_invoice", "out_refund"])],
    )
    vendor_amount = fields.Monetary(
        "Vendor Amount",
        compute="_compute_vendor_bills",
        readonly=True,
        store=True,
        tracking=True,
    )
    vendor_amount_unpaid = fields.Monetary(
        "Vendor Amount Unposted",
        compute="_compute_vendor_bills",
        readonly=True,
        store=True,
        tracking=True,
    )
    vendor_amount_total = fields.Monetary(
        "Vendor Amount Total",
        compute="_compute_vendor_bills",
        readonly=True,
        store=True,
        tracking=True,
    )
    vendor_bill_count = fields.Integer(compute="_compute_vendor_bills", store=True)
    vendor_bill_ids = fields.One2many(
        "account.move",
        "crowdfunding_challenge_id",
        domain=[("move_type", "in", ["in_invoice", "in_refund"])],
    )
    currency_id = fields.Many2one(related="company_id.currency_id")
    website_meta_title = fields.Char(related="name")
    website_meta_description = fields.Text(compute="_compute_website_meta_description")
    website_meta_og_img = fields.Char(compute="_compute_website_meta_og_img")
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company
    )

    def _default_fee_percentage(self):
        company = (
            self.env["res.company"].browse(
                self.default_get(["company_id"]).get("company_id") or []
            )
            or self.env.user.company
        )
        return company.crowdfunding_default_fee_percentage

    @api.depends("fee_percentage", "target_amount")
    def _compute_amounts(self):
        for this in self:
            amount_used = max(this.target_amount, this.pledged_amount)
            this.fee_amount = this.currency_id.round(amount_used * this.fee_percentage)
            this.claimed_partner_amount = amount_used - this.fee_amount

    @api.depends("pledged_amount", "target_amount")
    def _compute_funding_state(self):
        for this in self:
            this.pledged_percentage = (
                this.target_amount
                and (this.pledged_amount / this.target_amount * 100)
                or 0
            )
            this.funding_state = (
                "needs_funding" if this.pledged_percentage < 100 else "funded"
            )

    @api.depends(
        "invoice_ids.amount_total", "invoice_ids.amount_residual", "invoice_ids.state"
    )
    def _compute_invoices(self):
        for this in self:
            invoices = this.invoice_ids.filtered(lambda x: x.state != "cancel")
            this.invoice_count = len(invoices)
            this.pledged_amount = sum(
                invoices.filtered(lambda x: x.state == "posted").mapped(
                    "amount_total_signed"
                )
            )
            this.pledged_amount_unpaid = (
                sum(invoices.mapped("amount_total_signed")) - this.pledged_amount
            )
            this.pledged_amount_total = this.pledged_amount + this.pledged_amount_unpaid

    @api.depends(
        "vendor_bill_ids.amount_total",
        "vendor_bill_ids.amount_residual",
        "vendor_bill_ids.state",
    )
    def _compute_vendor_bills(self):
        for this in self:
            vendor_bills = this.vendor_bill_ids.filtered(lambda x: x.state != "cancel")
            this.vendor_bill_count = len(vendor_bills)
            this.vendor_amount = sum(
                vendor_bills.filtered(lambda x: x.state == "posted").mapped(
                    "amount_total_signed"
                )
            )
            this.vendor_amount_unpaid = (
                sum(vendor_bills.mapped("amount_total_signed")) - this.vendor_amount
            )
            this.vendor_amount_total = this.vendor_amount + this.vendor_amount_unpaid

    def _compute_website_url(self):
        for this in self:
            this.website_url = f"/crowdfunding/{slug(this)}"

    def _compute_website_meta_description(self):
        for this in self:
            this.website_meta_description = tools.html2plaintext(this.description)

    def _compute_website_meta_og_img(self):
        for this in self:
            this.website_meta_og_img = (
                f"/web/image/crowdfunding.challenge/{slug(this)}/description_image"
                if this.description_image
                else None
            )

    def action_open(self):
        self.filtered(lambda x: x.state == "draft").write(
            {"state": "open", "is_published": True}
        )

    def action_claimed(self):
        self.write({"state": "claimed"})

    def action_submitted(self):
        self.write({"state": "submitted"})

    def action_done(self):
        for this in self:
            if (
                this.currency_id.compare_amounts(
                    sum(
                        this.vendor_bill_ids.filtered(
                            lambda x: x.payment_state == "paid"
                        ).mapped("amount_total_signed")
                    ),
                    this.claimed_partner_amount,
                )
                != 0
            ):
                raise exceptions.UserError(
                    _(
                        "Challenge %(name)s cannot be marked as done as the amount "
                        "paid differs from the amount to be paid"
                    )
                    % this
                )
        self.write({"state": "done"})

    def action_cancel(self):
        self.write(
            {"state": "draft", "is_published": False, "claimed_partner_id": False}
        )

    def action_invoices(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "account.action_move_out_invoice_type"
        )
        return dict(
            action,
            domain=[
                ("crowdfunding_challenge_id", "in", self.ids),
                ("move_type", "in", ["out_invoice", "out_refund"]),
            ],
            context=_extend_context_str(
                action["context"],
                search_default_posted=True,
                search_default_draft=True,
            ),
        )

    def action_vendor_bills(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "account.action_move_in_invoice_type",
        )
        return dict(
            action,
            domain=[
                ("crowdfunding_challenge_id", "in", self.ids),
                ("move_type", "in", ["in_invoice", "in_refund"]),
            ],
            context=_extend_context_str(
                action["context"],
                search_default_posted=True,
                search_default_draft=True,
            ),
        )

    def action_invoice_wizard(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "crowdfunding.action_crowdfunding_invoicing_wizard"
        )
        # workaround for weird bug in v14 not displaying correct status for vendor_bill_ids
        # in not yet saved wizard, in newer versions just returning the action should work
        wizard = (
            self.env[action["res_model"]].with_context(active_ids=self.ids).create({})
        )
        wizard._onchange_vendor_bill_ids()
        action["res_id"] = wizard.id
        return action

    def _in_invoice(self, percentage=None, **kwargs):
        invoices = self.env["account.move"].create(
            [this._in_invoice_vals(percentage, **kwargs) for this in self]
        )
        return invoices

    def _in_invoice_vals(self, percentage=None, **kwargs):
        self.ensure_one()
        invoice_vals = self.env["account.move"].play_onchanges(
            {
                "move_type": "in_invoice",
                "crowdfunding_challenge_id": self.id,
                "partner_id": self.claimed_partner_id.id,
            },
            ["partner_id"],
        )
        invoice_line_vals = self.env["account.move.line"].play_onchanges(
            {
                "move_id": self.env["account.move"].new(invoice_vals),
                "product_id": self.company_id.crowdfunding_product_id.id,
            },
            ["product_id"],
        )
        invoice_line_vals["price_unit"] = self.claimed_partner_amount * (
            percentage or 1
        )
        return dict(
            invoice_vals,
            invoice_line_ids=[(0, 0, invoice_line_vals)],
        )

    def _out_invoice(self, partner, amount, **kwargs):
        return self.env["account.move"].create(
            [this._out_invoice_vals(partner, amount, **kwargs) for this in self]
        )

    def _out_invoice_vals(self, partner, amount, **kwargs):
        self.ensure_one()
        invoice_vals = self.env["account.move"].play_onchanges(
            {
                "move_type": "out_invoice",
                "ref": self.name,
                "crowdfunding_challenge_id": self.id,
                "partner_id": partner.id,
            },
            ["partner_id"],
        )
        invoice_line_vals = self.env["account.move.line"].play_onchanges(
            {
                "move_id": self.env["account.move"].new(invoice_vals),
                "product_id": self.company_id.crowdfunding_product_id.id,
            },
            ["product_id"],
        )
        invoice_line_vals["price_unit"] = amount
        return dict(
            invoice_vals,
            invoice_line_ids=[(0, 0, invoice_line_vals)],
        )

    @api.model
    def _domain_portal_access(self):
        return [("is_published", "=", True)]

    @api.model
    def _domain_website_access(self):
        return [("is_published", "=", True)]

    def _can_pay(self, partner=None):
        self.ensure_one()
        return self.state in ("open", "claimed")
