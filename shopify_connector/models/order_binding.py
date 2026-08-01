# pylint: disable=consider-merging-classes-inherited

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class ShopifyOrder(models.Model):
    _name = "shopify.order"
    _description = "Shopify Order Binding"
    _inherit = "shopify.binding.mixin"
    _order = "created_at desc, id desc"
    _check_company_auto = True

    odoo_id = fields.Many2one(
        "sale.order",
        string="Odoo Sales Order",
        index=True,
        check_company=True,
        ondelete="set null",
        help="Empty when an atomic order build failed before creating a sale order.",
    )
    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    order_name = fields.Char(string="Shopify Order", readonly=True, index=True)
    order_number = fields.Char(readonly=True, index=True)
    financial_status = fields.Char(readonly=True, index=True)
    fulfillment_status = fields.Char(readonly=True, index=True)
    source = fields.Selection(
        [
            ("online", "Online Store"),
            ("pos", "Point of Sale"),
            ("draft", "Draft Order"),
        ],
        required=True,
        default="online",
        readonly=True,
        index=True,
    )
    source_name = fields.Char(readonly=True)
    source_identifier = fields.Char(readonly=True)
    is_draft = fields.Boolean(readonly=True, index=True)
    draft_status = fields.Char(readonly=True)
    completed_order_shopify_id = fields.Char(readonly=True, index=True)
    replaced_by_id = fields.Many2one(
        "shopify.order",
        string="Completed Order Binding",
        readonly=True,
        ondelete="set null",
    )
    risk_level = fields.Selection(
        [
            ("UNKNOWN", "Unknown"),
            ("NONE", "None"),
            ("LOW", "Low"),
            ("MEDIUM", "Medium"),
            ("HIGH", "High"),
        ],
        required=True,
        default="UNKNOWN",
        readonly=True,
        index=True,
    )
    shop_currency_id = fields.Many2one(
        "res.currency", readonly=True, ondelete="restrict"
    )
    presentment_currency_id = fields.Many2one(
        "res.currency", readonly=True, ondelete="restrict"
    )
    order_currency_id = fields.Many2one(
        "res.currency", readonly=True, ondelete="restrict"
    )
    shop_subtotal = fields.Monetary(currency_field="shop_currency_id", readonly=True)
    shop_discount_total = fields.Monetary(
        currency_field="shop_currency_id", readonly=True
    )
    shop_shipping_total = fields.Monetary(
        currency_field="shop_currency_id", readonly=True
    )
    shop_tax_total = fields.Monetary(currency_field="shop_currency_id", readonly=True)
    shop_total = fields.Monetary(currency_field="shop_currency_id", readonly=True)
    presentment_subtotal = fields.Monetary(
        currency_field="presentment_currency_id", readonly=True
    )
    presentment_discount_total = fields.Monetary(
        currency_field="presentment_currency_id", readonly=True
    )
    presentment_shipping_total = fields.Monetary(
        currency_field="presentment_currency_id", readonly=True
    )
    presentment_tax_total = fields.Monetary(
        currency_field="presentment_currency_id", readonly=True
    )
    presentment_total = fields.Monetary(
        currency_field="presentment_currency_id", readonly=True
    )
    shop_money_json = fields.Json(readonly=True)
    presentment_money_json = fields.Json(readonly=True)
    discount_codes = fields.Text(readonly=True)
    raw_payload = fields.Json(string="Raw Shopify Payload", readonly=True)
    payload_digest = fields.Char(readonly=True, index=True)
    missing_tax_rate = fields.Char(readonly=True)
    missing_tax_country_id = fields.Many2one(
        "res.country", readonly=True, ondelete="set null"
    )
    missing_tax_included = fields.Boolean(readonly=True)
    created_at = fields.Datetime(string="Shopify Created At", readonly=True)
    cancelled_at = fields.Datetime(string="Shopify Cancelled At", readonly=True)
    line_binding_ids = fields.One2many(
        "shopify.order.line", "order_binding_id", string="Shopify Lines"
    )
    refund_binding_ids = fields.One2many(
        "shopify.refund", "order_binding_id", string="Shopify Refunds"
    )
    return_binding_ids = fields.One2many(
        "shopify.return", "order_binding_id", string="Shopify Returns"
    )

    @api.constrains("instance_id", "odoo_id")
    def _check_order_company(self):
        for binding in self.filtered("odoo_id"):
            if binding.odoo_id.company_id != binding.instance_id.company_id:
                raise ValidationError(
                    self.env._(
                        "The sales order and Shopify instance must share a company."
                    )
                )

    def action_create_tax_mapping(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Create Shopify Tax Mapping"),
            "res_model": "shopify.tax.mapping",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_instance_id": self.instance_id.id,
                "default_rate": self.missing_tax_rate,
                "default_country_id": self.missing_tax_country_id.id,
                "default_price_included": self.missing_tax_included,
            },
        }


class ShopifyOrderLine(models.Model):
    _name = "shopify.order.line"
    _description = "Shopify Order Line Binding"
    _inherit = "shopify.binding.mixin"
    _order = "id"
    _check_company_auto = True

    order_binding_id = fields.Many2one(
        "shopify.order", required=True, index=True, ondelete="cascade"
    )
    odoo_id = fields.Many2one(
        "sale.order.line",
        string="Odoo Sales Line",
        required=True,
        index=True,
        check_company=True,
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
    )
    variant_shopify_id = fields.Char(readonly=True, index=True)
    sku = fields.Char(readonly=True)
    current_quantity = fields.Float(readonly=True)
    refundable_quantity = fields.Float(readonly=True)
    shop_unit_price = fields.Char(readonly=True)
    presentment_unit_price = fields.Char(readonly=True)
    shop_discounted_total = fields.Char(readonly=True)
    presentment_discounted_total = fields.Char(readonly=True)
    shop_discount_total = fields.Char(readonly=True)
    presentment_discount_total = fields.Char(readonly=True)
    is_shipping = fields.Boolean(readonly=True)
    is_gift_card = fields.Boolean(readonly=True)

    _instance_sale_line_unique = models.Constraint(
        "UNIQUE(instance_id, odoo_id)",
        "An Odoo order line can only be linked once per Shopify instance.",
    )

    @api.constrains("instance_id", "order_binding_id", "odoo_id")
    def _check_line_scope(self):
        for binding in self:
            if (
                binding.order_binding_id.instance_id != binding.instance_id
                or binding.odoo_id.order_id != binding.order_binding_id.odoo_id
            ):
                raise ValidationError(
                    self.env._("The Shopify order line must belong to its bound order.")
                )


class ShopifyRefund(models.Model):
    _name = "shopify.refund"
    _description = "Shopify Refund Binding"
    _inherit = "shopify.binding.mixin"
    _order = "created_at desc, id desc"
    _check_company_auto = True

    order_binding_id = fields.Many2one(
        "shopify.order", required=True, index=True, ondelete="cascade"
    )
    move_id = fields.Many2one(
        "account.move",
        string="Credit Note",
        check_company=True,
        readonly=True,
        ondelete="set null",
    )
    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
    )
    amount = fields.Char(
        readonly=True, help="Exact refund amount in the imported order currency."
    )
    currency_id = fields.Many2one("res.currency", readonly=True, ondelete="restrict")
    note = fields.Text(readonly=True)
    created_at = fields.Datetime(readonly=True)
    restock_requested = fields.Boolean(readonly=True)
    raw_payload = fields.Json(readonly=True)
    line_ids = fields.One2many(
        "shopify.refund.line", "refund_id", string="Refund Lines"
    )

    @api.constrains("instance_id", "order_binding_id", "move_id")
    def _check_refund_scope(self):
        for refund in self:
            if refund.order_binding_id.instance_id != refund.instance_id:
                raise ValidationError(
                    self.env._(
                        "The refund and order must use the same Shopify instance."
                    )
                )
            if (
                refund.move_id
                and refund.move_id.company_id != refund.instance_id.company_id
            ):
                raise ValidationError(
                    self.env._("The refund credit note must use the instance company.")
                )


class ShopifyRefundLine(models.Model):
    _name = "shopify.refund.line"
    _description = "Shopify Refund Line"
    _order = "id"

    refund_id = fields.Many2one(
        "shopify.refund", required=True, index=True, ondelete="cascade"
    )
    shopify_id = fields.Char(required=True, index=True)
    order_line_binding_id = fields.Many2one("shopify.order.line", ondelete="set null")
    quantity = fields.Float(readonly=True)
    subtotal = fields.Char(readonly=True)
    tax = fields.Char(readonly=True)
    restock_type = fields.Char(readonly=True)

    _refund_line_unique = models.Constraint(
        "UNIQUE(refund_id, shopify_id)",
        "A refund line can only be imported once.",
    )


class ShopifyReturn(models.Model):
    _name = "shopify.return"
    _description = "Shopify Return and Exchange Binding"
    _inherit = "shopify.binding.mixin"
    _order = "created_at desc, id desc"
    _check_company_auto = True

    order_binding_id = fields.Many2one(
        "shopify.order", required=True, index=True, ondelete="cascade"
    )
    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    name = fields.Char(readonly=True)
    return_status = fields.Char(readonly=True, index=True)
    total_quantity = fields.Float(readonly=True)
    created_at = fields.Datetime(readonly=True)
    closed_at = fields.Datetime(readonly=True)
    return_lines = fields.Json(readonly=True)
    exchange_lines = fields.Json(readonly=True)
    raw_payload = fields.Json(readonly=True)

    @api.constrains("instance_id", "order_binding_id")
    def _check_return_scope(self):
        for return_binding in self:
            if (
                return_binding.order_binding_id.instance_id
                != return_binding.instance_id
            ):
                raise ValidationError(
                    self.env._(
                        "The return and order must use the same Shopify instance."
                    )
                )


class ShopifyTaxMapping(models.Model):
    _name = "shopify.tax.mapping"
    _description = "Shopify Tax Mapping"
    _order = "instance_id, country_id, rate"
    _check_company_auto = True

    instance_id = fields.Many2one(
        "shopify.instance", required=True, index=True, ondelete="cascade"
    )
    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    rate = fields.Char(
        required=True,
        help="Exact Shopify tax rate as a decimal fraction, for example 0.11.",
    )
    country_id = fields.Many2one("res.country", required=True, ondelete="restrict")
    price_included = fields.Boolean(required=True)
    tax_id = fields.Many2one(
        "account.tax",
        required=True,
        check_company=True,
        domain="[('type_tax_use', '=', 'sale')]",
        ondelete="restrict",
    )

    _mapping_unique = models.Constraint(
        "UNIQUE(instance_id, rate, country_id, price_included)",
        "This Shopify tax combination is already mapped.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get("rate") not in (None, ""):
                from decimal import Decimal

                values["rate"] = format(Decimal(str(values["rate"])).normalize(), "f")
        return super().create(vals_list)

    def write(self, values):
        if values.get("rate") not in (None, ""):
            from decimal import Decimal

            values["rate"] = format(Decimal(str(values["rate"])).normalize(), "f")
        return super().write(values)

    @api.constrains("company_id", "tax_id", "price_included")
    def _check_tax_scope(self):
        for mapping in self:
            if mapping.tax_id.company_id != mapping.company_id:
                raise ValidationError(
                    self.env._("The mapped tax must belong to the instance company.")
                )
            if bool(mapping.tax_id.price_include) != mapping.price_included:
                raise ValidationError(
                    self.env._(
                        "The mapped tax price-included setting must match Shopify."
                    )
                )


class ShopifyGatewayJournal(models.Model):
    _name = "shopify.gateway.journal"
    _description = "Shopify Gateway Journal Mapping"
    _order = "instance_id, gateway"
    _check_company_auto = True

    instance_id = fields.Many2one(
        "shopify.instance", required=True, index=True, ondelete="cascade"
    )
    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    gateway = fields.Char(required=True, index=True)
    journal_id = fields.Many2one(
        "account.journal",
        required=True,
        check_company=True,
        domain="[('type', 'in', ('bank', 'cash'))]",
        ondelete="restrict",
    )

    _gateway_unique = models.Constraint(
        "UNIQUE(instance_id, gateway)",
        "This Shopify gateway already has a journal mapping.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            values["gateway"] = str(values.get("gateway") or "").strip().lower()
        return super().create(vals_list)

    def write(self, values):
        if "gateway" in values:
            values["gateway"] = str(values["gateway"] or "").strip().lower()
        return super().write(values)


class ShopifyGatewayPayment(models.Model):
    _name = "shopify.gateway.payment"
    _description = "Shopify Imported Gateway Payment"
    _order = "id desc"

    instance_id = fields.Many2one(
        "shopify.instance", required=True, index=True, ondelete="cascade"
    )
    transaction_shopify_id = fields.Char(required=True, index=True)
    order_binding_id = fields.Many2one(
        "shopify.order", required=True, ondelete="cascade"
    )
    payment_id = fields.Many2one("account.payment", required=True, ondelete="restrict")
    gateway = fields.Char(required=True)
    amount = fields.Char(required=True)

    _transaction_unique = models.Constraint(
        "UNIQUE(instance_id, transaction_shopify_id)",
        "This Shopify payment transaction has already been registered.",
    )

    @api.constrains("instance_id", "order_binding_id", "payment_id")
    def _check_payment_scope(self):
        for payment in self:
            if (
                payment.order_binding_id.instance_id != payment.instance_id
                or payment.payment_id.company_id != payment.instance_id.company_id
            ):
                raise ValidationError(
                    self.env._(
                        "The gateway payment must use the order's instance company."
                    )
                )


class ShopifyInstanceOrderConfig(models.Model):
    _inherit = "shopify.instance"

    order_currency_policy = fields.Selection(
        [
            ("presentment", "Presentment Currency"),
            ("shop", "Shop Currency"),
        ],
        required=True,
        default="presentment",
    )
    unknown_product_policy = fields.Selection(
        [
            ("block", "Block With Error"),
            ("placeholder", "Use Placeholder Product"),
        ],
        required=True,
        default="block",
    )
    order_confirmation_policy = fields.Selection(
        [("quotation", "Import as Quotation"), ("auto", "Auto-confirm Eligible")],
        required=True,
        default="quotation",
    )
    auto_confirm_paid = fields.Boolean(default=True)
    auto_confirm_partially_paid = fields.Boolean(default=True)
    refund_uninvoiced_policy = fields.Selection(
        [("adjust", "Adjust Order"), ("cancel", "Cancel Fully Refunded Order")],
        required=True,
        default="adjust",
    )
    order_invoicing_policy = fields.Selection(
        [
            ("manual", "Manual"),
            ("paid", "Invoice on Paid"),
            ("fulfillment", "Invoice on Fulfillment"),
        ],
        required=True,
        default="manual",
    )
    high_risk_hold_enabled = fields.Boolean(default=True)
    placeholder_product_id = fields.Many2one(
        "product.product", check_company=True, ondelete="restrict"
    )
    delivery_product_id = fields.Many2one(
        "product.product", check_company=True, ondelete="restrict", readonly=True
    )
    gift_card_product_id = fields.Many2one(
        "product.product", check_company=True, ondelete="restrict"
    )
    gift_card_journal_id = fields.Many2one(
        "account.journal",
        check_company=True,
        domain="[('type', 'in', ('bank', 'cash'))]",
        ondelete="restrict",
    )
    order_import_date_from = fields.Date()
    order_import_date_to = fields.Date()
    order_binding_ids = fields.One2many("shopify.order", "instance_id", string="Orders")
    tax_mapping_ids = fields.One2many(
        "shopify.tax.mapping", "instance_id", string="Tax Mappings"
    )
    gateway_journal_ids = fields.One2many(
        "shopify.gateway.journal", "instance_id", string="Gateway Journals"
    )

    @api.model_create_multi
    def create(self, vals_list):
        instances = super().create(vals_list)
        instances._ensure_delivery_product()
        return instances

    def write(self, values):
        company_changed = "company_id" in values and any(
            instance.company_id.id != values["company_id"] for instance in self
        )
        if company_changed and not values.get("delivery_product_id"):
            self.ensure_one()
            company = self.env["res.company"].browse(values["company_id"])
            product = self._create_delivery_product(
                company, values.get("name") or self.name
            )
            values = {**values, "delivery_product_id": product.id}
        return super().write(values)

    def _create_delivery_product(self, company, instance_name):
        return (
            self.env["product.product"]
            .sudo()
            .with_company(company)
            .create(
                {
                    "name": self.env._("Shopify Delivery - %s", instance_name),
                    "type": "service",
                    "sale_ok": True,
                    "purchase_ok": False,
                    "company_id": company.id,
                }
            )
        )

    def _ensure_delivery_product(self):
        for instance in self:
            if instance.delivery_product_id:
                continue
            product = instance._create_delivery_product(
                instance.company_id, instance.name
            )
            instance.sudo().delivery_product_id = product
        return self.mapped("delivery_product_id")

    @api.constrains(
        "company_id",
        "placeholder_product_id",
        "delivery_product_id",
        "gift_card_product_id",
        "gift_card_journal_id",
    )
    def _check_order_configuration_company(self):
        for instance in self:
            records = (
                instance.placeholder_product_id
                | instance.delivery_product_id
                | instance.gift_card_product_id
            )
            if records.filtered(
                lambda product, instance=instance: (
                    product.company_id and product.company_id != instance.company_id
                )
            ):
                raise ValidationError(
                    self.env._(
                        "Configured order products must belong to the instance company."
                    )
                )
            if (
                instance.gift_card_journal_id
                and instance.gift_card_journal_id.company_id != instance.company_id
            ):
                raise ValidationError(
                    self.env._(
                        "The gift-card journal must belong to the instance company."
                    )
                )


class SaleOrderShopify(models.Model):
    _inherit = "sale.order"

    shopify_binding_ids = fields.One2many(
        "shopify.order", "odoo_id", string="Shopify Bindings"
    )
    shopify_risk_hold = fields.Boolean(readonly=True, copy=False, index=True)
    shopify_risk_level = fields.Selection(
        [
            ("UNKNOWN", "Unknown"),
            ("NONE", "None"),
            ("LOW", "Low"),
            ("MEDIUM", "Medium"),
            ("HIGH", "High"),
        ],
        readonly=True,
        copy=False,
    )
    shopify_discount_codes = fields.Char(readonly=True, copy=False)
    shopify_tags = fields.Char(readonly=True, copy=False)
    shopify_note = fields.Text(readonly=True, copy=False)

    def action_release_shopify_risk_hold(self):
        risk_summary = self.env._("Shopify high-risk order")
        for order in self:
            order.write({"shopify_risk_hold": False})
            order.picking_ids.write({"shopify_risk_hold": False})
            order.activity_ids.filtered(
                lambda activity: activity.summary == risk_summary
            ).action_done()
        return True


class SaleOrderLineShopify(models.Model):
    _inherit = "sale.order.line"

    shopify_line_id = fields.Char(readonly=True, copy=False, index=True)
    shopify_discount_amount = fields.Char(readonly=True, copy=False)
    shopify_expected_total = fields.Char(readonly=True, copy=False)
    shopify_is_shipping = fields.Boolean(readonly=True, copy=False)
    shopify_is_gift_card = fields.Boolean(readonly=True, copy=False)


class StockPickingShopifyRisk(models.Model):
    _inherit = "stock.picking"

    shopify_risk_hold = fields.Boolean(readonly=True, copy=False, index=True)

    def button_validate(self):
        held = self.filtered("shopify_risk_hold")
        if held:
            raise UserError(
                self.env._(
                    "Release the Shopify high-risk hold before validating delivery."
                )
            )
        return super().button_validate()
