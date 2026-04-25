# Copyright 2014 Compassion CH - Cyril Sester <csester@compassion.ch>
# Copyright 2014 Tecnativa - Pedro M. Baeza
# Copyright 2015-2020 Akretion - Alexis de Lattre <alexis.delattre@akretion.com>
# Copyright 2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class AccountBankingMandate(models.Model):
    """The banking mandate is attached to a bank account and represents an
    authorization that the bank account owner gives to a company for a
    specific operation (such as direct debit)
    """

    _name = "account.banking.mandate"
    _description = "A generic banking mandate"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "signature_date desc"
    _check_company_auto = True

    format = fields.Selection(
        [("basic", "Basic Mandate")],
        default="basic",
        required=True,
        string="Mandate Format",
        tracking=20,
    )
    type = fields.Selection(
        [("recurrent", "Recurrent"), ("oneoff", "Single Use")],
        string="Type of Mandate",
        default="recurrent",
        tracking=30,
        required=True,
    )
    # We allow to have a draft mandate without bank account
    partner_bank_id = fields.Many2one(
        comodel_name="res.partner.bank",
        compute="_compute_partner_bank_id",
        precompute=True,
        store=True,
        readonly=False,
        string="Bank Account",
        tracking=40,
        domain="[('partner_id', '=', partner_id)]",
        ondelete="restrict",
        index="btree",
        check_company=True,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        index="btree",
        required=True,
        tracking=35,
        ondelete="restrict",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    unique_mandate_reference = fields.Char(
        tracking=10, copy=False, default=lambda self: _("New")
    )
    signature_date = fields.Date(
        string="Date of Signature",
        tracking=50,
    )
    scan = fields.Binary(string="Scan of the Mandate")
    last_debit_date = fields.Date(string="Date of the Last Debit", readonly=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("valid", "Valid"),
            ("final", "Final Debit"),
            ("expired", "Expired"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        default="draft",
        tracking=60,
        help="Only valid mandates can be used in a payment line. A cancelled "
        "mandate is a mandate that has been cancelled by the customer.",
    )
    payment_line_ids = fields.One2many(
        comodel_name="account.payment.line",
        inverse_name="mandate_id",
        string="Related Payment Lines",
    )
    payment_line_ids_count = fields.Integer(compute="_compute_payment_line_ids_count")

    _sql_constraints = [
        (
            "mandate_ref_company_uniq",
            "unique(unique_mandate_reference, company_id)",
            "A Mandate with the same reference already exists for this company!",
        )
    ]

    @api.depends("partner_id")
    def _compute_partner_bank_id(self):
        for mandate in self:
            if (
                mandate.partner_bank_id
                and mandate.partner_id
                and mandate.partner_id != mandate.partner_bank_id.partner_id
            ):
                mandate.partner_bank_id = False

    @api.depends("unique_mandate_reference", "partner_bank_id", "state")
    def _compute_display_name(self):
        state2label = dict(self.fields_get("state", "selection")["state"]["selection"])
        for mandate in self:
            name = mandate.unique_mandate_reference
            acc_number = mandate.partner_bank_id.sanitized_acc_number
            if acc_number:
                name = f"{name} [...{acc_number[-4:]}]"
            if mandate.state != "valid":
                name = f"{name} ({state2label[mandate.state]})"
            mandate.display_name = name

    @api.depends("payment_line_ids")
    def _compute_payment_line_ids_count(self):
        payment_line_model = self.env["account.payment.line"]
        domain = [("mandate_id", "in", self.ids)]
        res = payment_line_model._read_group(
            domain=domain, groupby=["mandate_id"], aggregates=["__count"]
        )
        payment_line_dict = {mandate.id: line_count for (mandate, line_count) in res}
        for rec in self:
            rec.payment_line_ids_count = payment_line_dict.get(rec.id, 0)

    def show_payment_lines(self):
        self.ensure_one()
        return {
            "name": _("Payment lines"),
            "type": "ir.actions.act_window",
            "view_mode": "list,form",
            "res_model": "account.payment.line",
            "domain": [("mandate_id", "=", self.id)],
        }

    @api.constrains("signature_date", "last_debit_date")
    def _check_dates(self):
        today = fields.Date.context_today(self)
        for mandate in self:
            if mandate.signature_date and mandate.signature_date > today:
                raise ValidationError(
                    _("The date of signature of mandate '%s' is in the future!")
                    % mandate.display_name
                )
            if (
                mandate.signature_date
                and mandate.last_debit_date
                and mandate.signature_date > mandate.last_debit_date
            ):
                raise ValidationError(
                    _(
                        "The mandate '%s' can't have a date of last debit "
                        "before the date of signature."
                    )
                    % mandate.display_name
                )

    @api.constrains("state", "partner_bank_id", "partner_id", "signature_date")
    def _check_valid_state(self):
        for mandate in self:
            if mandate.state in ("valid", "final"):
                if not mandate.signature_date:
                    raise ValidationError(
                        _(
                            "Cannot validate the mandate '%s' without a date of "
                            "signature."
                        )
                        % mandate.display_name
                    )
                if not mandate.partner_bank_id:
                    raise ValidationError(
                        _(
                            "Cannot validate the mandate '%s' because it is not "
                            "attached to a bank account."
                        )
                        % mandate.display_name
                    )
            if (
                mandate.partner_bank_id
                and mandate.partner_id
                and mandate.partner_bank_id.partner_id != mandate.partner_id
            ):
                raise ValidationError(
                    _(
                        "Mandate %(mandate)s is configured with partner %(partner)s "
                        "and bank account %(bank_account)s, but this bank account "
                        "belongs to partner %(partner_bank_account)s.",
                        mandate=mandate.display_name,
                        partner=mandate.partner_id.display_name,
                        bank_account=mandate.partner_bank_id.display_name,
                        partner_bank_account=mandate.partner_bank_id.partner_id.display_name,
                    )
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            unique_mandate_reference = vals.get("unique_mandate_reference", _("New"))
            if unique_mandate_reference == _("New"):
                vals["unique_mandate_reference"] = self.env["ir.sequence"].with_company(
                    vals.get("company_id")
                ).next_by_code("account.banking.mandate") or _("New")
        return super().create(vals_list)

    def validate(self):
        for mandate in self:
            if mandate.state != "draft":
                raise UserError(
                    _("Mandate '%s' should be in draft state.") % mandate.display_name
                )
        self.write({"state": "valid"})

    def cancel(self):
        for mandate in self:
            if mandate.state not in ("draft", "valid", "final"):
                raise UserError(
                    _("Mandate '%s' should be in draft, valid or final debit state.")
                    % mandate.display_name
                )
        self.write({"state": "cancel"})

    def back2draft(self):
        """Allows to set the mandate back to the draft state.
        This is for mandates cancelled by mistake.
        """
        for mandate in self:
            if mandate.state != "cancel":
                raise UserError(
                    _("Mandate '%s' should be in cancel state.") % mandate.display_name
                )
        self.write({"state": "draft"})

    def valid2final(self):
        for mandate in self:
            if mandate.state != "valid":
                raise UserError(
                    _("Mandate '%s' should be in valid state.") % mandate.display_name
                )
        self.write({"state": "final"})

    def final2valid(self):
        """Should never happen. Only for user mistakes."""
        for mandate in self:
            if mandate.state != "final":
                raise UserError(
                    _("Mandate '%s' should be in 'Final Debit' state.")
                    % mandate.display_name
                )
        self.write({"state": "valid"})
