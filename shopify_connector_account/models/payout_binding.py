from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ShopifyPayout(models.Model):
    _name = "shopify.payout"
    _description = "Shopify Payments Payout"
    _inherit = "shopify.binding.mixin"
    _order = "issued_at desc, id desc"
    _rec_name = "reference"
    _check_company_auto = True

    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    reference = fields.Char(required=True, readonly=True, index=True)
    legacy_resource_id = fields.Char(readonly=True, index=True)
    issued_at = fields.Datetime(readonly=True, index=True)
    payout_status = fields.Char(readonly=True, index=True)
    transaction_type = fields.Char(readonly=True)
    currency_id = fields.Many2one(
        "res.currency",
        required=True,
        readonly=True,
        ondelete="restrict",
    )
    gross_amount = fields.Monetary(currency_field="currency_id", readonly=True)
    fee_amount = fields.Monetary(currency_field="currency_id", readonly=True)
    net_amount = fields.Monetary(currency_field="currency_id", readonly=True)
    gross_exact = fields.Char(required=True, readonly=True)
    fee_exact = fields.Char(required=True, readonly=True)
    net_exact = fields.Char(required=True, readonly=True)
    summary = fields.Json(readonly=True)
    raw_payload = fields.Json(readonly=True)
    transaction_ids = fields.One2many(
        "shopify.payout.transaction",
        "payout_id",
        string="Balance Transactions",
    )
    entry_id = fields.Many2one(
        "account.move",
        string="Generated Journal Entry",
        check_company=True,
        readonly=True,
        copy=False,
        ondelete="set null",
    )
    unmatched_count = fields.Integer(
        compute="_compute_unmatched_count",
        string="Unmatched Transactions",
    )

    @api.depends("transaction_ids.is_unmatched")
    def _compute_unmatched_count(self):
        for payout in self:
            payout.unmatched_count = len(
                payout.transaction_ids.filtered("is_unmatched")
            )

    @api.constrains("instance_id", "currency_id", "entry_id")
    def _check_payout_scope(self):
        for payout in self:
            if payout.entry_id and payout.entry_id.company_id != payout.company_id:
                raise ValidationError(
                    self.env._("The payout entry must belong to the instance company.")
                )

    def action_generate_entry(self):
        for payout in self:
            payout.with_delay(
                description=self.env._(
                    "Generate Shopify payout entry %s", payout.reference
                ),
                identity_key=(
                    f"shopify.payout.entry.{payout.instance_id.id}.{payout.shopify_id}"
                ),
            )._job_generate_entry()
        return True


class ShopifyPayoutTransaction(models.Model):
    _name = "shopify.payout.transaction"
    _description = "Shopify Payments Balance Transaction"
    _order = "transaction_date, id"
    _rec_name = "display_type"
    _check_company_auto = True

    instance_id = fields.Many2one(
        "shopify.instance",
        required=True,
        index=True,
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    payout_id = fields.Many2one(
        "shopify.payout",
        required=True,
        index=True,
        ondelete="cascade",
    )
    shopify_id = fields.Char(required=True, readonly=True, index=True)
    transaction_type = fields.Char(readonly=True, index=True)
    display_type = fields.Char(readonly=True)
    source_type = fields.Char(readonly=True, index=True)
    source_id = fields.Char(readonly=True)
    source_order_transaction_id = fields.Char(readonly=True, index=True)
    transaction_date = fields.Datetime(readonly=True, index=True)
    currency_id = fields.Many2one(
        "res.currency",
        required=True,
        readonly=True,
        ondelete="restrict",
    )
    amount = fields.Monetary(currency_field="currency_id", readonly=True)
    fee = fields.Monetary(currency_field="currency_id", readonly=True)
    net = fields.Monetary(currency_field="currency_id", readonly=True)
    amount_exact = fields.Char(required=True, readonly=True)
    fee_exact = fields.Char(required=True, readonly=True)
    net_exact = fields.Char(required=True, readonly=True)
    order_binding_id = fields.Many2one(
        "shopify.order",
        string="Associated Order",
        index=True,
        readonly=True,
        ondelete="set null",
    )
    reconciliation_account_id = fields.Many2one(
        "account.account",
        check_company=True,
        readonly=True,
        ondelete="restrict",
    )
    route = fields.Selection(
        [
            ("clearing", "Gateway Clearing"),
            ("adjustment", "Adjustment"),
            ("gift_card", "Gift Card Liability"),
            ("fee", "Fee Expense"),
        ],
        readonly=True,
    )
    is_unmatched = fields.Boolean(readonly=True, index=True)
    unmatched_reason = fields.Char(readonly=True)
    adjustment_reason = fields.Char(readonly=True)
    test = fields.Boolean(readonly=True)
    raw_payload = fields.Json(readonly=True)

    _instance_transaction_unique = models.Constraint(
        "UNIQUE(instance_id, shopify_id)",
        "A Shopify Payments transaction can only be imported once.",
    )

    @api.constrains(
        "instance_id",
        "payout_id",
        "order_binding_id",
        "reconciliation_account_id",
    )
    def _check_transaction_scope(self):
        for transaction in self:
            if transaction.payout_id.instance_id != transaction.instance_id:
                raise ValidationError(
                    self.env._(
                        "The transaction and payout must use one Shopify instance."
                    )
                )
            if (
                transaction.order_binding_id
                and transaction.order_binding_id.instance_id != transaction.instance_id
            ):
                raise ValidationError(
                    self.env._(
                        "The associated order must use the transaction instance."
                    )
                )
            account = transaction.reconciliation_account_id
            if (
                account
                and account.company_ids
                and transaction.company_id not in (account.company_ids)
            ):
                raise ValidationError(
                    self.env._(
                        "The reconciliation account must be available to the company."
                    )
                )


class ShopifyDispute(models.Model):
    _name = "shopify.dispute"
    _description = "Shopify Payments Dispute"
    _inherit = "shopify.binding.mixin"
    _order = "initiated_at desc, id desc"
    _rec_name = "shopify_id"
    _check_company_auto = True

    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    order_binding_id = fields.Many2one(
        "shopify.order",
        string="Associated Order",
        readonly=True,
        index=True,
        ondelete="set null",
    )
    currency_id = fields.Many2one(
        "res.currency",
        required=True,
        readonly=True,
        ondelete="restrict",
    )
    amount = fields.Monetary(currency_field="currency_id", readonly=True)
    amount_exact = fields.Char(required=True, readonly=True)
    dispute_status = fields.Char(readonly=True, index=True)
    dispute_type = fields.Char(readonly=True, index=True)
    reason = fields.Char(readonly=True)
    network_reason_code = fields.Char(readonly=True)
    initiated_at = fields.Datetime(readonly=True)
    evidence_due_by = fields.Datetime(readonly=True)
    evidence_sent_on = fields.Datetime(readonly=True)
    finalized_on = fields.Datetime(readonly=True)
    raw_payload = fields.Json(readonly=True)

    @api.constrains("instance_id", "order_binding_id")
    def _check_dispute_scope(self):
        for dispute in self.filtered("order_binding_id"):
            if dispute.order_binding_id.instance_id != dispute.instance_id:
                raise ValidationError(
                    self.env._("The dispute order must use the same Shopify instance.")
                )


class ShopifyInstanceFinancialConfiguration(models.Model):
    _inherit = "shopify.instance"

    shopify_payments_state = fields.Selection(
        [
            ("unknown", "Not Checked"),
            ("enabled", "Enabled"),
            ("unavailable", "Unavailable"),
        ],
        required=True,
        default="unknown",
        readonly=True,
    )
    payout_journal_id = fields.Many2one(
        "account.journal",
        check_company=True,
        domain="[('type', 'in', ('bank', 'cash'))]",
        ondelete="restrict",
    )
    payout_fee_account_id = fields.Many2one(
        "account.account",
        string="Payout Fee Expense Account",
        check_company=True,
        domain="[('account_type', 'in', ('expense', 'expense_direct_cost'))]",
        ondelete="restrict",
    )
    payout_adjustment_account_id = fields.Many2one(
        "account.account",
        check_company=True,
        ondelete="restrict",
    )
    payout_currency_gain_account_id = fields.Many2one(
        "account.account",
        check_company=True,
        ondelete="restrict",
    )
    payout_currency_loss_account_id = fields.Many2one(
        "account.account",
        check_company=True,
        ondelete="restrict",
    )
    payout_auto_post = fields.Boolean(default=False)
    gift_card_liability_account_id = fields.Many2one(
        "account.account",
        compute="_compute_gift_card_liability_account",
        help=(
            "The configured gift-card product's income account, used as a "
            "liability account for sales and redemptions."
        ),
    )
    payout_import_date_from = fields.Date()
    payout_import_date_to = fields.Date()
    payout_ids = fields.One2many("shopify.payout", "instance_id")
    dispute_ids = fields.One2many("shopify.dispute", "instance_id")

    @api.depends(
        "gift_card_product_id",
        "gift_card_product_id.property_account_income_id",
        "gift_card_product_id.categ_id.property_account_income_categ_id",
    )
    def _compute_gift_card_liability_account(self):
        for instance in self:
            product = instance.gift_card_product_id.with_company(instance.company_id)
            instance.gift_card_liability_account_id = (
                (
                    product.property_account_income_id
                    or product.categ_id.property_account_income_categ_id
                )
                if product
                else False
            )

    @api.constrains("gift_card_product_id")
    def _check_gift_card_product_liability_account(self):
        for instance in self.filtered("gift_card_product_id"):
            account = instance.gift_card_liability_account_id
            if not account or account.account_type not in (
                "liability_current",
                "liability_non_current",
            ):
                raise ValidationError(
                    self.env._(
                        "The gift-card product income account must be a "
                        "current or non-current liability account."
                    )
                )

    @api.constrains(
        "company_id",
        "payout_journal_id",
        "payout_fee_account_id",
        "payout_adjustment_account_id",
        "payout_currency_gain_account_id",
        "payout_currency_loss_account_id",
    )
    def _check_financial_configuration_company(self):
        for instance in self:
            if (
                instance.payout_journal_id
                and instance.payout_journal_id.company_id != instance.company_id
            ):
                raise ValidationError(
                    self.env._(
                        "The payout journal must belong to the instance company."
                    )
                )
            accounts = (
                instance.payout_fee_account_id
                | instance.payout_adjustment_account_id
                | instance.payout_currency_gain_account_id
                | instance.payout_currency_loss_account_id
            )
            if accounts.filtered(
                lambda account, instance=instance: (
                    account.company_ids
                    and instance.company_id not in account.company_ids
                )
            ):
                raise ValidationError(
                    self.env._(
                        "Financial accounts must be available to the instance company."
                    )
                )

    def action_import_payouts(self):
        self.ensure_one()
        if (
            self.payout_import_date_from
            and self.payout_import_date_to
            and self.payout_import_date_from > self.payout_import_date_to
        ):
            raise ValidationError(
                self.env._("The payout import start date must precede the end date.")
            )
        self.with_delay(
            description=self.env._("Import Shopify Payments payouts for %s", self.name),
            identity_key=(
                f"shopify.payouts.import.{self.id}."
                f"{self.payout_import_date_from}.{self.payout_import_date_to}"
            ),
        )._job_import_payouts(
            fields.Date.to_string(self.payout_import_date_from),
            fields.Date.to_string(self.payout_import_date_to),
        )
        return True


class ShopifyGatewayPaymentGiftCardEntry(models.Model):
    _inherit = "shopify.gateway.payment"

    gift_card_move_id = fields.Many2one(
        "account.move",
        string="Gift Card Liability Entry",
        readonly=True,
        copy=False,
        ondelete="set null",
    )
