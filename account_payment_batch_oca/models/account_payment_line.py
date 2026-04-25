# © 2015-2016 Akretion - Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import format_date


class AccountPaymentLine(models.Model):
    _name = "account.payment.line"
    _description = "Payment Lines"
    _check_company_auto = True

    name = fields.Char(string="Payment Reference", readonly=True, copy=False)
    order_id = fields.Many2one(
        comodel_name="account.payment.order",
        string="Payment Order",
        ondelete="cascade",
        index=True,
        check_company=True,
    )
    company_id = fields.Many2one(
        related="order_id.company_id",
        store=True,
    )
    company_currency_id = fields.Many2one(
        related="order_id.company_currency_id",
        store=True,
    )
    payment_type = fields.Selection(
        related="order_id.payment_type",
        store=True,
    )
    bank_account_required = fields.Boolean(
        related="order_id.payment_method_id.bank_account_required",
    )
    mail_notif = fields.Boolean(related="order_id.payment_method_line_id.mail_notif")
    state = fields.Selection(related="order_id.state", store=True)
    move_line_id = fields.Many2one(
        comodel_name="account.move.line",
        string="Journal Item",
        ondelete="restrict",
        check_company=True,
        domain="[('reconciled','=', False), ('account_id.reconcile', '=', True), "
        "('partner_id', '!=', False)]",
    )
    ml_maturity_date = fields.Date(related="move_line_id.date_maturity")
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        compute="_compute_payment_line",
        store=True,
        readonly=False,
        precompute=True,
        string="Currency of the Payment Transaction",
        required=True,
    )
    amount_currency = fields.Monetary(
        compute="_compute_payment_line",
        store=True,
        readonly=False,
        precompute=True,
        string="Amount",
        currency_field="currency_id",
    )
    amount_company_currency = fields.Monetary(
        compute="_compute_amount_company_currency",
        string="Amount in Company Currency",
        currency_field="company_currency_id",
        store=True,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        compute="_compute_payment_line",
        store=True,
        readonly=False,
        precompute=True,
        required=True,
        domain=[("parent_id", "=", False)],
        check_company=True,
    )
    partner_bank_id = fields.Many2one(
        comodel_name="res.partner.bank",
        compute="_compute_partner_bank_id",
        store=True,
        readonly=False,
        precompute=True,
        string="Partner Bank Account",
        required=False,
        ondelete="restrict",
        check_company=True,
    )
    partner_bank_acc_type = fields.Selection(
        related="partner_bank_id.acc_type", string="Bank Account Type"
    )
    partner_bank_allow_out_payment = fields.Boolean(
        related="partner_bank_id.allow_out_payment", store=True
    )
    date = fields.Date(string="Payment Date")
    # communication field is required=False because we don't want to block
    # the creation of lines from move/invoices when communication is empty
    # This field is required in the form view and there is an error message
    # when going from draft to confirm if the field is empty
    communication = fields.Char(
        compute="_compute_payment_line",
        store=True,
        readonly=False,
        precompute=True,
        required=False,
        help="Label of the payment that will be seen by the destinee",
    )
    communication_type = fields.Selection(
        compute="_compute_payment_line",
        store=True,
        readonly=False,
        precompute=True,
        selection=[("free", "Free"), ("structured", "Structured")],
        required=True,
    )
    payment_ids = fields.Many2many(
        comodel_name="account.payment",
        string="Payment transaction",
        readonly=True,
    )
    mail_notif_partner_id = fields.Many2one(
        "res.partner",
        compute="_compute_mail_notif_partner_id",
        store=True,
        precompute=True,
        readonly=False,
        string="Partner to Notify",
        domain="[('email', '!=', False), "
        "'|', ('parent_id', '=', partner_id), ('id', '=', partner_id)]",
    )

    _sql_constraints = [
        (
            "name_company_unique",
            "unique(name, company_id)",
            "A payment line already exists with this reference in the same company!",
        )
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("account.payment.line")
                    or "New"
                )
        return super().create(vals_list)

    @api.depends("amount_currency", "currency_id", "company_currency_id", "date")
    def _compute_amount_company_currency(self):
        for line in self:
            if line.currency_id and line.company_currency_id:
                line.amount_company_currency = line.currency_id._convert(
                    line.amount_currency,
                    line.company_currency_id,
                    line.company_id,
                    line.date or fields.Date.today(),
                )
            else:
                line.amount_company_currency = 0

    @api.depends("partner_id", "order_id.payment_method_line_id")
    def _compute_mail_notif_partner_id(self):
        for line in self:
            mail_notif_partner = False
            if line.partner_id and line.order_id.payment_method_line_id.mail_notif:
                mail_partner_policy = (
                    line.order_id.payment_method_line_id.mail_partner_policy
                )
                if mail_partner_policy == "parent":
                    mail_notif_partner = line.partner_id
                elif mail_partner_policy == "invoice_partner":
                    if line.move_line_id and line.move_line_id.move_id.partner_id:
                        mail_notif_partner = line.move_line_id.move_id.partner_id
                elif mail_partner_policy == "invoice_contact":
                    mail_notif_partner_id = line.partner_id.address_get(["invoice"])[
                        "invoice"
                    ]
                    mail_notif_partner = self.env["res.partner"].browse(
                        mail_notif_partner_id
                    )
                elif mail_partner_policy == "last_payment":
                    last_pay_line = self.search(
                        [
                            ("mail_notif_partner_id", "!=", False),
                            ("order_id", "!=", line.order_id.id),
                            ("state", "!=", "cancel"),
                            ("company_id", "=", line.company_id.id),
                        ],
                        order="id desc",
                        limit=1,
                    )
                    if last_pay_line:
                        mail_notif_partner = last_pay_line.mail_notif_partner_id
                if mail_notif_partner and not mail_notif_partner.email:
                    mail_notif_partner = False
            line.mail_notif_partner_id = mail_notif_partner

    @api.model
    def _lot_grouping_fields(self):
        """This list of fields is used to compute the grouping hashcode for lots.
        This method is inherited in account_payment_sepa_base to add several fields.
        The fields in this list MUST also be present in _payment_grouping_fields()
        """
        return [
            "date",
            "currency_id",
        ]

    @api.model
    def _payment_grouping_fields(self):
        """This list of fields is used o compute the grouping hashcode."""
        res = self._lot_grouping_fields()
        res += [
            "partner_id",
            "partner_bank_id",
            "communication_type",
        ]
        return res

    def _payment_line_grouping_key(self):
        self.ensure_one()
        key = []
        for field in self._payment_grouping_fields():
            key.append(str(self[field]))
        # Don't group the payment lines that are attached to the same supplier
        # but to move lines with different accounts (very unlikely),
        # for easier generation/comprehension of the transfer move
        key.append(self.move_line_id and self.move_line_id.account_id.id or False)
        # Don't group the payment lines that use a structured communication
        # otherwise it would break the structured communication system !
        if self.communication_type != "free":
            key.append(self.id)
        else:
            key.append(None)
        return tuple(key)

    def _lot_grouping_key(self):
        self.ensure_one()
        key = []
        for field in self._lot_grouping_fields():
            key.append(str(self[field]))
        return tuple(key)

    @api.depends("move_line_id")
    def _compute_payment_line(self):
        for line in self:
            communication = False
            communication_type = "free"
            currency_id = line.company_id.currency_id.id
            amount_currency = 0.0
            move_line = line.move_line_id
            partner_id = False
            if move_line and move_line.partner_id:
                partner_id = move_line.partner_id.id
                communication_type = move_line.move_id.reference_type
                communication = (
                    move_line.move_id._get_payment_order_communication_full()
                )
                currency_id = move_line.currency_id.id
                amount_currency = move_line.amount_residual_currency
                if line.order_id.payment_type == "outbound":
                    amount_currency *= -1
            line.communication = communication
            line.communication_type = communication_type
            line.currency_id = currency_id
            line.amount_currency = amount_currency
            line.partner_id = partner_id

    @api.depends(
        "partner_id",
        "move_line_id",
        "order_id.journal_id",
        "order_id.company_id",
        "order_id.payment_method_id",
    )
    def _compute_partner_bank_id(self):
        for line in self:
            partner_bank = False
            partner = line.partner_id
            order = line.order_id
            move = line.move_line_id.move_id
            if order.payment_method_id.bank_account_required:
                if (
                    move
                    and move.move_type in ("in_invoice", "in_refund")
                    and order.payment_type == "outbound"
                ):
                    partner_bank = move.partner_bank_id
                elif partner:
                    if partner == order.company_id.partner_id:  # internal transfer
                        for bank_account in partner.bank_ids:
                            if bank_account != order.journal_id.bank_account_id:
                                partner_bank = bank_account
                                break
                    elif partner.bank_ids:
                        partner_bank = partner.bank_ids[0]
            line.partner_bank_id = partner_bank

    def _draft2open_payment_line_check(self):
        self.ensure_one()
        order = self.order_id
        errors = []
        if self.bank_account_required:
            if not self.partner_bank_id:
                errors.append(
                    _("Missing Partner Bank Account on payment line %s") % self.name
                )
            else:
                if self.partner_bank_id.partner_id != self.partner_id:
                    errors.append(
                        _(
                            "On payment line %(name)s with partner '%(partner)s', "
                            "the bank account '%(bank_account)s' belongs to partner "
                            "'%(bank_account_partner)s'.",
                            name=self.name,
                            partner=self.partner_id.display_name,
                            bank_account=self.partner_bank_id.display_name,
                            bank_account_partner=self.partner_bank_id.partner_id.display_name,
                        )
                    )

                if (
                    order.payment_type == "outbound"
                    and order._enforce_allow_out_payment()
                    and not self.partner_bank_id.allow_out_payment
                ):
                    errors.append(
                        _(
                            "Bank account '%(bank_account)s' of partner '%(partner)s' "
                            "is untrusted. Check that this bank account can be trusted "
                            "and activate the option 'Send Money' on it.",
                            bank_account=self.partner_bank_id.display_name,
                            partner=self.partner_id.display_name,
                        )
                    )
                # internal transfers: check source account != dest account
                if self.partner_bank_id == order.company_partner_bank_id:
                    errors.append(
                        _(
                            "On payment line %(name)s, the bank account "
                            "'%(bank_account)s' is the same as the company "
                            "bank account of the payment order.",
                            name=self.name,
                            bank_account=self.partner_bank_id.display_name,
                        )
                    )
        if not self.communication:
            errors.append(_("Communication is empty on payment line %s.") % self.name)
        if (
            order.payment_method_line_id.mail_notif
            and self.mail_notif_partner_id
            and not self.mail_notif_partner_id.email
        ):
            errors.append(
                _("Missing email on notification partner '%s'.")
                % self.mail_notif_partner_id.display_name
            )
        # inbound: check option no_debit_before_maturity
        if (
            order.payment_type == "inbound"
            and order.payment_method_line_id.no_debit_before_maturity
            and self.ml_maturity_date
            and self.date < self.ml_maturity_date
        ):
            errors.append(
                _(
                    "The payment method '%(method)s' has the option "
                    "'Disallow Debit Before Maturity Date'. The "
                    "payment line %(pline)s has a maturity date %(mdate)s "
                    "which is after the computed payment date %(pdate)s.",
                    method=order.payment_method_line_id.display_name,
                    pline=self.name,
                    mdate=format_date(self.env, self.ml_maturity_date),
                    pdate=format_date(self.env, self.date),
                )
            )
        return errors

    def _prepare_account_payment_vals(self, payment_lot, pay_sequence):
        """Prepare the dictionary to create an account payment record from a set of
        payment lines.
        """
        order = self.order_id
        journal = order.journal_id
        if order.payment_method_line_id.bank_account_link == "fixed":
            method_line_id = order.payment_method_line_id.id
        else:
            method_line = self.env["account.payment.method.line"].search(
                [
                    ("company_id", "=", order.company_id.id),
                    ("journal_id", "=", order.journal_id.id),
                    ("payment_method_id", "=", order.payment_method_id.id),
                    ("bank_account_link", "=", "fixed"),
                ],
                limit=1,
            )
            if not method_line:
                raise UserError(
                    _(
                        "No payment method with a fixed link to journal '%(journal)s' "
                        "with technical payment method '%(payment_method)s'. "
                        "You must create one.",
                        journal=journal.display_name,
                        payment_method=order.payment_method_id.display_name,
                    )
                )
            method_line_id = method_line.id
        vals = {
            "payment_type": order.payment_type,
            "partner_id": self.partner_id.id,
            "destination_account_id": self.move_line_id.account_id.id or False,
            "company_id": order.company_id.id,
            "amount": sum(self.mapped("amount_currency")),
            "date": self[:1].date,
            "currency_id": self.currency_id.id,
            # memo is used as 'Instruction Identification' and
            # 'End to End Identification' in ISO 20022 XML files, so it must be unique
            "memo": f"{payment_lot.name}/{pay_sequence}",
            "payment_reference": " - ".join([line.communication for line in self]),
            "journal_id": journal.id,
            "partner_bank_id": self.partner_bank_id.id,
            "payment_order_id": order.id,
            "payment_lot_id": payment_lot.id,
            "payment_line_ids": [Command.set(self.ids)],
            "payment_method_line_id": method_line_id,
            "invoice_ids": [
                Command.set(
                    [
                        pline.move_line_id.move_id.id
                        for pline in self
                        if pline.move_line_id
                    ]
                )
            ],
        }
        # Determine partner_type
        move_type = self[:1].move_line_id.move_id.move_type
        if move_type in {"out_invoice", "out_refund"}:
            vals["partner_type"] = "customer"
        elif move_type in {"in_invoice", "in_refund"}:
            vals["partner_type"] = "supplier"
        else:
            p_type = "customer" if vals["payment_type"] == "inbound" else "supplier"
            vals["partner_type"] = p_type
        # Fill destination account if manual payment line with no linked journal item
        if not vals["destination_account_id"]:
            if vals["partner_type"] == "customer":
                vals["destination_account_id"] = (
                    self.partner_id.property_account_receivable_id.id
                )
            else:
                vals["destination_account_id"] = (
                    self.partner_id.property_account_payable_id.id
                )
        return vals

    def _prepare_account_payment_lot_vals(self, lot_sequence):
        """This method should only use fields listed in self._lot_grouping_fields()"""
        self.ensure_one()
        vals = {
            "order_id": self.order_id.id,
            "currency_id": self.currency_id.id,
            "date": self.date,
            "name": f"{self.order_id.name}/LOT{lot_sequence}",
        }
        return vals

    def _prepare_write_draft2open(self):
        self.ensure_one()
        today = fields.Date.context_today(self)
        order = self.order_id
        # Compute requested payment date
        if order.date_prefered == "due":
            requested_date = self.ml_maturity_date or self.date or today
        elif order.date_prefered == "fixed":
            requested_date = order.date_scheduled or today
        else:
            requested_date = today
        # No payment date in the past
        requested_date = max(today, requested_date)
        vals = {"date": requested_date}
        return vals

    def action_open_related_move(self):
        self.ensure_one()
        if not self.move_line_id:
            raise UserError(
                _("Payment line %s is not linked to a journal item.")
                % self.display_name
            )
        return self.move_line_id.action_open_business_doc()
