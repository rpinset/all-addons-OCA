from urllib.parse import urlparse

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

from ..graphql import (
    SHOP_QUERY,
    WEBHOOK_SUBSCRIPTION_CREATE,
    WEBHOOK_SUBSCRIPTION_UPDATE,
    WEBHOOK_SUBSCRIPTIONS_QUERY,
)
from ..lib.client import API_VERSION, ShopifyClient, ShopifyError

REQUIRED_WEBHOOK_TOPICS = (
    "APP_UNINSTALLED",
    "CUSTOMERS_CREATE",
    "CUSTOMERS_UPDATE",
    "DRAFT_ORDERS_CREATE",
    "DRAFT_ORDERS_UPDATE",
    "FULFILLMENTS_CREATE",
    "FULFILLMENTS_UPDATE",
    "INVENTORY_LEVELS_UPDATE",
    "ORDERS_CANCELLED",
    "ORDERS_CREATE",
    "ORDERS_UPDATED",
    "PRODUCTS_CREATE",
    "PRODUCTS_DELETE",
    "PRODUCTS_UPDATE",
    "REFUNDS_CREATE",
)


class ShopifyInstance(models.Model):
    _name = "shopify.instance"
    _description = "Shopify Instance"
    _order = "name"
    _check_company_auto = True

    name = fields.Char(required=True)
    shop_url = fields.Char(
        string="Shop Domain",
        required=True,
        help="Shopify myshopify.com domain, without an Admin API path.",
    )
    access_token = fields.Char(
        string="Admin API Access Token",
        copy=False,
        groups="shopify_connector.group_shopify_manager",
    )
    api_version = fields.Char(
        string="API Version",
        required=True,
        default=API_VERSION,
        readonly=True,
    )
    webhook_secret = fields.Char(
        copy=False,
        groups="shopify_connector.group_shopify_manager",
    )
    accept_webhooks = fields.Boolean(
        default=True,
        help="Disable to reject webhook delivery for this instance.",
    )
    webhook_max_payload_bytes = fields.Integer(
        string="Maximum Webhook Payload",
        required=True,
        default=2 * 1024 * 1024,
        help="Reject larger webhook request bodies before HMAC verification.",
    )
    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("connected", "Connected"),
            ("error", "Error"),
        ],
        required=True,
        default="draft",
        readonly=True,
        copy=False,
    )

    _company_url_unique = models.Constraint(
        "UNIQUE(company_id, shop_url)",
        "A shop domain can only be configured once per company.",
    )

    @api.constrains("shop_url")
    def _check_shop_url(self):
        for record in self:
            value = (record.shop_url or "").strip()
            parsed = urlparse(value if "://" in value else f"https://{value}")
            if (
                parsed.scheme not in ("http", "https")
                or not parsed.hostname
                or parsed.path not in ("", "/")
                or parsed.query
                or parsed.fragment
            ):
                raise ValidationError(
                    self.env._("Enter a shop domain such as example.myshopify.com.")
                )

    @api.constrains("webhook_max_payload_bytes")
    def _check_webhook_max_payload_bytes(self):
        for instance in self:
            if instance.webhook_max_payload_bytes <= 0:
                raise ValidationError(
                    self.env._("The maximum webhook payload must be greater than zero.")
                )

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get("shop_url"):
                values["shop_url"] = ShopifyClient._normalise_shop_url(
                    values["shop_url"]
                )
        return super().create(vals_list)

    def write(self, values):
        if values.get("shop_url"):
            values["shop_url"] = ShopifyClient._normalise_shop_url(values["shop_url"])
        return super().write(values)

    def _shopify_client(self):
        self.ensure_one()
        return ShopifyClient(
            self.shop_url,
            self.access_token,
            api_version=self.api_version,
        )

    def action_duplicate_configuration(self):
        self.ensure_one()
        base_url = f"copy-{self.id}.{self.shop_url}"
        shop_url = base_url
        suffix = 2
        instances = self.with_context(active_test=False)
        while instances.search_count(
            [
                ("company_id", "=", self.company_id.id),
                ("shop_url", "=", shop_url),
            ],
            limit=1,
        ):
            shop_url = f"copy-{self.id}-{suffix}.{self.shop_url}"
            suffix += 1
        defaults = {
            "name": self.env._("%s (Copy)", self.name),
            "shop_url": shop_url,
            "access_token": False,
            "webhook_secret": False,
            "state": "draft",
            "active": True,
            "product_pricelist_id": False,
            "guest_partner_id": False,
            "delivery_product_id": False,
            "shopify_plus_state": "unknown",
            "webhook_health_checked_at": False,
            "webhook_missing_topics": False,
        }
        if "shopify_payments_state" in self._fields:
            defaults["shopify_payments_state"] = "unknown"
        duplicate = self.copy(default=defaults)
        for field_name in (
            "tax_mapping_ids",
            "gateway_journal_ids",
            "carrier_mapping_ids",
        ):
            for configuration in self[field_name]:
                configuration.copy(default={"instance_id": duplicate.id})
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Shopify Instance Copy"),
            "res_model": "shopify.instance",
            "res_id": duplicate.id,
            "view_mode": "form",
            "target": "current",
        }

    def _write_log(
        self,
        *,
        entity,
        direction,
        level,
        message,
        record=None,
    ):
        self.ensure_one()
        values = {
            "instance_id": self.id,
            "entity": entity,
            "direction": direction,
            "level": level,
            "message": message,
        }
        if record:
            values.update({"res_model": record._name, "res_id": record.id})
        return self.env["shopify.log"].sudo().create(values)

    def action_test_connection(self):
        self.ensure_one()
        try:
            data = self._shopify_client().execute(SHOP_QUERY)
            shop = data.get("shop", {})
            shop_name = shop.get("name")
            currency_code = shop.get("currencyCode")
            currency = (
                self.env["res.currency"]
                .with_context(active_test=False)
                .search([("name", "=", currency_code)], limit=1)
            )
            if not shop_name or not currency:
                raise ShopifyError(
                    self.env._("Shopify did not return a supported shop identity.")
                )
        except ShopifyError as exc:
            self.state = "error"
            self._write_log(
                entity="instance",
                direction="import",
                level="error",
                message=self.env._("Connection test failed: %s", exc),
                record=self,
            )
            raise UserError(
                self.env._("Shopify connection test failed: %s", exc)
            ) from exc

        self.shop_currency_id = currency
        self.product_pricelist_id.sudo().currency_id = currency
        self.state = "connected"
        self._write_log(
            entity="instance",
            direction="import",
            level="info",
            message=self.env._("Connected to Shopify shop %s.", shop_name),
            record=self,
        )
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": self.env._("Connection successful"),
                "message": self.env._("Connected to Shopify shop %s.", shop_name),
                "type": "success",
                "sticky": False,
            },
        }

    def _webhook_callback_url(self):
        self.ensure_one()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        if not base_url:
            raise UserError(self.env._("Configure the Odoo web base URL first."))
        return f"{base_url.rstrip('/')}/shopify/webhook/{self.id}"

    def action_repair_webhook_subscriptions(self):
        self.ensure_one()
        client = self._shopify_client()
        callback_url = self._webhook_callback_url()
        subscription_input = {"callbackUrl": callback_url, "format": "JSON"}
        created = 0
        repaired = 0
        try:
            data = client.execute(WEBHOOK_SUBSCRIPTIONS_QUERY)
            nodes = data.get("webhookSubscriptions", {}).get("nodes", [])
            subscriptions = {
                node.get("topic"): node
                for node in nodes
                if isinstance(node, dict) and node.get("topic")
            }
            for topic in REQUIRED_WEBHOOK_TOPICS:
                existing = subscriptions.get(topic)
                current_url = (
                    existing.get("endpoint", {}).get("callbackUrl")
                    if existing
                    else None
                )
                if not existing:
                    client.execute(
                        WEBHOOK_SUBSCRIPTION_CREATE,
                        {
                            "topic": topic,
                            "subscription": subscription_input,
                        },
                    )
                    created += 1
                elif current_url != callback_url:
                    client.execute(
                        WEBHOOK_SUBSCRIPTION_UPDATE,
                        {
                            "id": existing["id"],
                            "subscription": subscription_input,
                        },
                    )
                    repaired += 1
        except ShopifyError as exc:
            self.state = "error"
            self._write_log(
                entity="webhook_subscription",
                direction="export",
                level="error",
                message=self.env._("Webhook subscription repair failed: %s", exc),
                record=self,
            )
            raise UserError(
                self.env._("Could not repair Shopify webhook subscriptions: %s", exc)
            ) from exc

        self.state = "connected"
        if "webhook_health_checked_at" in self._fields:
            self.write(
                {
                    "webhook_health_checked_at": fields.Datetime.now(),
                    "webhook_missing_topics": False,
                }
            )
        self._write_log(
            entity="webhook_subscription",
            direction="export",
            level="info",
            message=self.env._(
                "Webhook subscriptions checked: %(created)s created, "
                "%(repaired)s repaired.",
                created=created,
                repaired=repaired,
            ),
            record=self,
        )
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": self.env._("Webhook subscriptions ready"),
                "message": self.env._(
                    "%(created)s created and %(repaired)s repaired.",
                    created=created,
                    repaired=repaired,
                ),
                "type": "success",
                "sticky": False,
            },
        }
