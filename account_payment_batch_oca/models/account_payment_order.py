# © 2009 EduSense BV (<http://www.edusense.nl>)
# © 2011-2013 Therp BV (<https://therp.nl>)
# © 2016 Akretion (Alexis de Lattre - alexis.delattre@akretion.com)
# Copyright 2016-2022 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from collections import defaultdict

from markupsafe import Markup

from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import format_date

logger = logging.getLogger(__name__)


class AccountPaymentOrder(models.Model):
    _name = "account.payment.order"
    _description = "Payment/Debit Order"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"
    _check_company_auto = True

    name = fields.Char(
        string="Reference", readonly=True, copy=False, default=lambda self: _("New")
    )
    payment_method_line_id = fields.Many2one(
        comodel_name="account.payment.method.line",
        required=True,
        ondelete="restrict",
        tracking=True,
        check_company=True,
        index=True,
        domain="[('payment_order_ok', '=', True), "
        "('payment_type', '=', payment_type), ('company_id', '=', company_id)]",
        string="Payment Method",
    )
    payment_type = fields.Selection(
        selection=[("inbound", "Inbound"), ("outbound", "Outbound")],
        readonly=True,
        required=True,
    )
    payment_method_id = fields.Many2one(
        comodel_name="account.payment.method",
        related="payment_method_line_id.payment_method_id",
        store=True,
    )
    payment_method_code = fields.Char(
        related="payment_method_line_id.payment_method_id.code", store=True
    )
    mail_notif = fields.Boolean(related="payment_method_line_id.mail_notif")
    company_id = fields.Many2one(
        "res.company",
        ondelete="cascade",
        required=True,
        index=True,
        default=lambda self: self.env.company,
    )
    company_currency_id = fields.Many2one(related="company_id.currency_id", store=True)
    bank_account_link = fields.Selection(
        related="payment_method_line_id.bank_account_link",
    )
    allowed_journal_ids = fields.Many2many(
        comodel_name="account.journal",
        compute="_compute_allowed_journal_ids",
        string="Allowed journals",
    )
    journal_id = fields.Many2one(
        comodel_name="account.journal",
        compute="_compute_journal_id",
        store=True,
        precompute=True,
        string="Bank Journal",
        ondelete="restrict",
        tracking=True,
        check_company=True,
        domain="[('id', 'in', allowed_journal_ids)]",
    )
    # The journal_id field is only required at confirm step, to
    # allow auto-creation of payment order from invoice
    company_partner_bank_id = fields.Many2one(
        related="journal_id.bank_account_id",
        string="Company Bank Account",
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("open", "Confirmed"),
            ("generated", "File Generated"),
            ("uploaded", "File Uploaded"),
            ("cancel", "Cancel"),
        ],
        string="Status",
        readonly=True,
        copy=False,
        default="draft",
        tracking=True,
        index=True,
    )
    date_prefered = fields.Selection(
        selection=[
            ("now", "Immediately"),
            ("due", "Due Date"),
            ("fixed", "Fixed Date"),
        ],
        compute="_compute_date_prefered",
        store=True,
        precompute=True,
        string="Payment Execution Date Type",
        required=True,
        tracking=True,
    )
    date_scheduled = fields.Date(
        string="Payment Execution Date",
        tracking=True,
        help="Select a requested date of execution if you selected 'Due Date' "
        "as the Payment Execution Date Type.",
    )
    date_generated = fields.Date(string="File Generation Date", readonly=True)
    date_uploaded = fields.Date(string="File Upload Date", readonly=True)
    payment_line_ids = fields.One2many(
        comodel_name="account.payment.line",
        inverse_name="order_id",
        string="Transactions",
    )
    payment_ids = fields.One2many(
        comodel_name="account.payment",
        inverse_name="payment_order_id",
        string="Payment Transactions",
        readonly=True,
    )
    payment_lot_ids = fields.One2many(
        comodel_name="account.payment.lot", inverse_name="order_id", readonly=True
    )
    payment_lot_count = fields.Integer(
        compute="_compute_payment_lot_count", string="Number of Lots", store=True
    )
    payment_count = fields.Integer(
        compute="_compute_payment_count",
        store=True,
        string="Number of Payment Transactions",
    )
    untrusted_bank_account_count = fields.Integer(
        compute="_compute_untrusted_bank_accounts"
    )
    untrusted_bank_account_ids = fields.Many2many(
        "res.partner.bank", compute="_compute_untrusted_bank_accounts"
    )
    total_company_currency = fields.Monetary(
        compute="_compute_total", store=True, currency_field="company_currency_id"
    )
    description = fields.Char()
    payment_file_id = fields.Many2one("ir.attachment", string="Payment File Attachment")
    payment_file_datas = fields.Binary(
        related="payment_file_id.datas", string="Payment File"
    )
    payment_file_name = fields.Char(
        related="payment_file_id.name", string="Payment Filename"
    )
    search_partner_id = fields.Many2one(
        related="payment_line_ids.partner_id", string="Partner"
    )

    _sql_constraints = [
        (
            "name_company_unique",
            "unique(name, company_id)",
            "A payment/debit order with the same reference already exists "
            "in this company.",
        )
    ]

    @api.depends("payment_method_line_id")
    def _compute_allowed_journal_ids(self):
        for record in self:
            allowed_journals = False
            if record.payment_method_line_id:
                allowed_journals = record.payment_method_line_id.journal_id
                if (
                    record.payment_method_line_id.bank_account_link == "variable"
                    and record.payment_method_line_id.variable_journal_ids
                ):
                    allowed_journals |= (
                        record.payment_method_line_id.variable_journal_ids
                    )
            record.allowed_journal_ids = allowed_journals

    @api.depends("payment_lot_ids")
    def _compute_payment_lot_count(self):
        rg_res = self.env["account.payment.lot"]._read_group(
            [("order_id", "in", self.ids)], groupby=["order_id"], aggregates=["__count"]
        )
        mapped_data = {order.id: count for (order, count) in rg_res}
        for order in self:
            order.payment_lot_count = mapped_data.get(order.id, 0)

    @api.depends(
        "payment_line_ids.partner_bank_id.allow_out_payment", "payment_method_line_id"
    )
    def _compute_untrusted_bank_accounts(self):
        rpbo = self.env["res.partner.bank"]
        for order in self:
            bank_accounts = rpbo
            if (
                order.payment_type == "outbound"
                and order.payment_method_line_id
                and order.payment_method_line_id.payment_method_id.bank_account_required
            ):
                for line in order.payment_line_ids:
                    if (
                        line.partner_bank_id
                        and not line.partner_bank_id.allow_out_payment
                    ):
                        bank_accounts |= line.partner_bank_id
            order.untrusted_bank_account_count = len(bank_accounts)
            order.untrusted_bank_account_ids = [Command.set(bank_accounts.ids)]

    def unlink(self):
        for order in self:
            if order.state == "uploaded":
                raise UserError(
                    _(
                        "You cannot delete an uploaded payment/debit order "
                        "(but you can cancel it)."
                    )
                )
            if order.payment_file_id:
                order.payment_file_id.unlink()
        return super().unlink()

    @api.constrains("payment_type", "payment_method_line_id")
    def _payment_order_constraints(self):
        for order in self:
            if (
                order.payment_method_line_id
                and order.payment_method_line_id.payment_type != order.payment_type
            ):
                payment_type2label = dict(
                    self.env["account.payment.method"].fields_get(
                        "payment_type", "selection"
                    )["payment_type"]["selection"]
                )
                raise ValidationError(
                    _(
                        "On payment/debit order %(order)s, the payment type is "
                        "%(order_ptype)s, but the payment method %(method)s "
                        "is configured with payment type %(method_ptype)s.",
                        order=order.display_name,
                        order_ptype=payment_type2label[order.payment_type],
                        method=order.payment_method_line_id.display_name,
                        method_ptype=payment_type2label[
                            order.payment_method_line_id.payment_type
                        ],
                    )
                )

    @api.constrains("date_scheduled")
    def _check_date_scheduled(self):
        today = fields.Date.context_today(self)
        for order in self:
            if order.date_scheduled:
                if order.date_scheduled < today:
                    raise ValidationError(
                        _(
                            "On payment/debit order %(porder)s, the payment "
                            "execution date is in the past (%(exedate)s).",
                            porder=order.name,
                            exedate=format_date(self.env, order.date_scheduled),
                        )
                    )

    @api.depends("payment_line_ids", "payment_line_ids.amount_company_currency")
    def _compute_total(self):
        rg_res = self.env["account.payment.line"]._read_group(
            [("order_id", "in", self.ids)],
            groupby=["order_id"],
            aggregates=["amount_company_currency:sum"],
        )
        mapped_data = {order.id: total for (order, total) in rg_res}
        for order in self:
            order.total_company_currency = mapped_data.get(order.id, 0)

    @api.depends("payment_ids")
    def _compute_payment_count(self):
        rg_res = self.env["account.payment"]._read_group(
            [("payment_order_id", "in", self.ids)],
            groupby=["payment_order_id"],
            aggregates=["__count"],
        )
        mapped_data = {order.id: pay_count for (order, pay_count) in rg_res}
        for order in self:
            order.payment_count = mapped_data.get(order.id, 0)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "company_id" in vals:
                self = self.with_company(vals["company_id"])
            payment_method_line = False
            if vals.get("payment_method_line_id"):
                payment_method_line = self.env["account.payment.method.line"].browse(
                    vals["payment_method_line_id"]
                )
            if vals.get("name", _("New")) == _("New"):
                if payment_method_line and payment_method_line.specific_sequence_id:
                    vals["name"] = payment_method_line.specific_sequence_id.next_by_id()
                elif payment_method_line.payment_method_id.payment_type == "inbound":
                    vals["name"] = self.env["ir.sequence"].next_by_code(
                        "account.payment.order.inbound"
                    ) or _("New")
                else:
                    vals["name"] = self.env["ir.sequence"].next_by_code(
                        "account.payment.order"
                    ) or _("New")
        return super().create(vals_list)

    @api.depends("payment_method_line_id")
    def _compute_date_prefered(self):
        for order in self:
            if order.payment_method_line_id.default_date_prefered:
                order.date_prefered = order.payment_method_line_id.default_date_prefered
            else:
                order.date_prefered = "due"

    @api.depends("payment_method_line_id")
    def _compute_journal_id(self):
        for order in self:
            if order.payment_method_line_id.journal_id:
                order.journal_id = order.payment_method_line_id.journal_id
            else:
                order.journal_id = False

    def cancel2draft(self):
        # Delete existing payments
        self.payment_ids.unlink()
        # Delete existing lots
        self.payment_lot_ids.unlink()
        self.write({"state": "draft"})

    def action_cancel(self):
        # Unreconcile and cancel payments
        self.payment_ids.action_draft()
        self.payment_ids.action_cancel()
        if self.payment_file_id:
            self.payment_file_id.unlink()
        self.write(
            {
                "state": "cancel",
                "date_generated": False,
            }
        )

    def _enforce_allow_out_payment(self):
        """Inherit this method if you don't want to enfore 'allow_out_payment' boolean
        on bank accounts"""
        return True

    def draft2open(self):
        """
        Called when you click on the 'Confirm' button
        Set the 'date' on payment line depending on the 'date_prefered' of the order
        Generate the account payments and lots
        """
        for order in self:
            if not order.journal_id:
                raise UserError(
                    _("Missing Bank Journal on payment order %s.") % order.name
                )
            if (
                order.payment_method_id.bank_account_required
                and not order.journal_id.bank_account_id
            ):
                raise UserError(
                    _("Missing bank account on bank journal '%s'.")
                    % order.journal_id.display_name
                )
            if not order.payment_line_ids:
                raise UserError(
                    _("There are no transactions on payment order %s.") % order.name
                )
            if order.payment_ids:
                raise UserError(
                    _("%s is linked to existing payments. This should never happen.")
                    % order.name
                )
            if order.payment_lot_ids:
                raise UserError(
                    _("%s is linked to existing lots. This should never happen.")
                    % order.name
                )
            # Prepare account payments from the payment lines
            payline_err_text = set()
            group_paylines = {}  # key = pay_key
            pay_key2lot = {}  # key = pay_key, value = payment_lot
            lot_key2lot = {}  # key = lot_key, value = payment_lot
            for payline in order.payment_line_ids:
                payline.write(payline._prepare_write_draft2open())
                for error in payline._draft2open_payment_line_check():
                    payline_err_text.add(error)
                # Group options
                pay_key = (
                    payline._payment_line_grouping_key()
                    if order.payment_method_line_id.group_lines
                    else payline.id
                )
                lot_key = payline._lot_grouping_key()
                if pay_key in group_paylines:
                    group_paylines[pay_key]["paylines"] |= payline
                    group_paylines[pay_key]["total"] += payline.amount_currency
                else:
                    group_paylines[pay_key] = {
                        "paylines": payline,
                        "total": payline.amount_currency,
                        "currency": payline.currency_id,
                    }
                if lot_key not in lot_key2lot:
                    lot_key2lot[lot_key] = self.env["account.payment.lot"].create(
                        payline._prepare_account_payment_lot_vals(len(lot_key2lot) + 1)
                    )
                pay_key2lot[pay_key] = lot_key2lot[lot_key]
            # Raise errors that happened on the validation process
            if payline_err_text:
                raise UserError("\n".join(payline_err_text))

            # Create account payments
            lot2pay_seq = defaultdict(int)
            payment_vals = []
            for pay_key, paydict in group_paylines.items():
                # Block generation of negative account.payment
                if paydict["currency"].compare_amounts(paydict["total"], 0) <= 0:
                    raise UserError(
                        _(
                            "The amount for Partner '%(partner)s' is negative "
                            "or null (%(amount).2f) !",
                            partner=paydict["paylines"][0].partner_id.name,
                            amount=paydict["total"],
                        )
                    )
                lot = pay_key2lot[pay_key]
                lot2pay_seq[lot] += 1
                payment_vals.append(
                    paydict["paylines"]._prepare_account_payment_vals(
                        lot, lot2pay_seq[lot]
                    )
                )
            self.env["account.payment"].create(payment_vals)
        self.write({"state": "open"})

    def generate_payment_file(self):
        """Returns (payment file as bytes, filename extension without the dot)"""
        self.ensure_one()
        if self.payment_method_id.code in ("manual", "test_manual"):
            return (False, False)
        else:
            raise UserError(
                _(
                    "No handler for payment method code '%s'. Maybe you haven't "
                    "installed the related Odoo module."
                )
                % self.payment_method_id.code
            )

    def _prepare_filename(self):
        """Returns filename without extension"""
        self.ensure_one()
        return self.name.replace("/", "-")

    def open2generated(self):
        self.ensure_one()
        action = {}
        payment_file_bytes, filename_ext = self.generate_payment_file()
        vals = {
            "state": "generated",
            "date_generated": fields.Date.context_today(self),
        }
        if payment_file_bytes and filename_ext:
            filename = ".".join([self._prepare_filename(), filename_ext])
            attachment = self.env["ir.attachment"].create(
                {
                    "name": filename,
                    "raw": payment_file_bytes,
                }
            )
            vals["payment_file_id"] = attachment.id
            action = {
                "name": filename,
                "type": "ir.actions.act_url",
                "url": f"web/content/?model={self._name}&id={self.id}&"
                f"filename_field=payment_file_name&field=payment_file_datas&"
                f"download=true&filename={filename}",
                "target": "new",
                # target: "new" and NOT "self", otherwise you get the following bug:
                # after this action, all UserError won't show a pop-up to the user
                # but will only show a warning message in the logs until the web
                # page is reloaded
            }
        self.write(vals)
        return action

    def generated2uploaded(self):
        self.ensure_one()
        self.payment_ids.action_post()
        method_line = self.payment_method_line_id
        mail_notif = method_line.mail_notif
        partner2mail = {}
        # Perform the reconciliation of payments and source journal items
        # Reminder : in v18, account.payment doesn't always have a move_id
        for payment in self.payment_ids:
            if payment.move_id:
                lines_to_rec = self.env["account.move.line"]
                for line in (
                    payment.payment_line_ids.move_line_id + payment.move_id.line_ids
                ):
                    if line.account_id.id == payment.destination_account_id.id:
                        lines_to_rec |= line
                lines_to_rec.reconcile()
            if mail_notif:
                if payment.partner_id not in partner2mail:
                    partner2mail[payment.partner_id] = {
                        "payments": payment,
                        "dest_partners": self.env["res.partner"],
                    }
                else:
                    partner2mail[payment.partner_id]["payments"] |= payment
                for line in payment.payment_line_ids:
                    if line.mail_notif_partner_id:
                        partner2mail[payment.partner_id]["dest_partners"] |= (
                            line.mail_notif_partner_id
                        )
        if mail_notif:
            account_number_scrambled_ctx = {
                "show_bank_account_chars": method_line.show_bank_account_chars,
                "show_bank_account": method_line.show_bank_account,
            }
            for partner, mail_dict in partner2mail.items():
                if mail_dict["dest_partners"]:
                    payments, detail_col = mail_dict[
                        "payments"
                    ]._prepare_payment_order_mail(
                        partner.lang, account_number_scrambled_ctx
                    )
                    partner_to = ",".join(
                        [str(p.id) for p in mail_dict["dest_partners"]]
                    )
                    try:
                        self.env.ref(
                            "account_payment_batch_oca.payment_order_mail_notif"
                        ).with_context(
                            payments=payments,
                            detail_col=detail_col,
                            partner_lang=partner.lang,
                            partner_to=partner_to,
                            partner_display_name=partner.display_name,
                            partner_name=partner.name,
                        ).send_mail(self.id)
                        logger.info(
                            "mail generated for partner %s", partner.display_name
                        )
                    except Exception as e:
                        logger.warning(
                            "Error in the generation of the payment notif mail "
                            "for partner %s: %s",
                            partner.display_name,
                            e,
                        )
                        self.message_post(
                            body=Markup(
                                _(
                                    "Odoo <strong>failed to generate the email"
                                    "</strong> for partner <a href=# "
                                    "data-oe-model=res.partner "
                                    "data-oe-id=%(partner_id)d> "
                                    "%(partner_name)s</a>: %(error)s",
                                    partner_id=partner.id,
                                    partner_name=partner.display_name,
                                    error=e,
                                )
                            )
                        )
        self.write(
            {"state": "uploaded", "date_uploaded": fields.Date.context_today(self)}
        )

    def action_open_payments(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "account.action_account_all_payments"
        )
        if self.payment_count == 1:
            action.update(
                {
                    "view_mode": "form,list,kanban,graph,activity",
                    "views": False,
                    "view_id": False,
                    "res_id": self.payment_ids[0].id,
                }
            )
        else:
            action["domain"] = [("id", "in", self.payment_ids.ids)]
        return action

    def action_open_invoices(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "account.action_move_journal_line"
        )
        move_ids = set()
        for line in self.payment_line_ids:
            if line.move_line_id:
                move_ids.add(line.move_line_id.move_id.id)
        if not move_ids:
            raise UserError(
                _("None of the payment lines are linked to a journal item.")
            )
        if len(move_ids) == 1:
            action.update(
                {
                    "view_mode": "form,list,kanban,activity",
                    "views": False,
                    "view_id": False,
                    "res_id": list(move_ids)[0],
                }
            )
        else:
            action["domain"] = [("id", "in", list(move_ids))]
        return action

    def action_open_untrusted_accounts(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "base.action_res_partner_bank_account_form"
        )
        if len(self.untrusted_bank_account_ids) == 1:
            action.update(
                {
                    "view_mode": "form,list",
                    "views": False,
                    "view_id": False,
                    "res_id": self.untrusted_bank_account_ids.id,
                }
            )
        else:
            action["domain"] = [("id", "in", self.untrusted_bank_account_ids.ids)]
        return action
