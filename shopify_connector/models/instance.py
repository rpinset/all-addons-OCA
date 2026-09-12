import logging
from datetime import timedelta
from urllib.parse import urlparse

import psycopg2

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

from odoo.addons.queue_job.exception import RetryableJobError

from ..graphql import (
    SHOP_QUERY,
    WEBHOOK_SUBSCRIPTION_CREATE,
    WEBHOOK_SUBSCRIPTION_UPDATE,
    WEBHOOK_SUBSCRIPTIONS_QUERY,
)
from ..lib.client import (
    API_VERSION,
    ShopifyClient,
    ShopifyError,
    request_access_token,
)

_logger = logging.getLogger(__name__)

ACCESS_TOKEN_LOCK_TIMEOUT_SECONDS = 45

ACCESS_TOKEN_EXPIRY_MARGIN_SECONDS = 60

ACCESS_TOKEN_CREDENTIAL_FIELDS = ("shop_url", "client_id", "webhook_secret")

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
    client_id = fields.Char(
        string="Shopify App Client ID",
        copy=False,
        help="Client ID of the Shopify app created in the Shopify Dev Dashboard.",
    )
    access_token = fields.Char(
        string="Admin API Access Token",
        copy=False,
        groups="shopify_connector.group_shopify_manager",
    )
    access_token_expires_at = fields.Datetime(
        copy=False,
        readonly=True,
        help="Expiry of the access token issued by the Shopify Dev Dashboard. "
        "Empty for static Admin API tokens, which do not expire.",
    )
    api_version = fields.Char(
        string="API Version",
        required=True,
        default=API_VERSION,
        readonly=True,
    )
    webhook_secret = fields.Char(
        string="Shopify App Client Secret",
        copy=False,
        groups="shopify_connector.group_shopify_manager",
        help="Shopify app client secret, also used to verify webhook HMAC signatures.",
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
        stale = self._instances_with_stale_managed_token(values)
        result = super().write(values)
        if stale:
            stale._clear_managed_access_token(values)
        return result

    def _instances_with_stale_managed_token(self, values):
        """Return the records whose stored token outlives its credentials.

        Only instances taking part in the managed flow, before or after the
        write, give up their token: a legacy instance keeps the static token its
        administrator configured, whichever credential is edited.
        """
        changed = [name for name in ACCESS_TOKEN_CREDENTIAL_FIELDS if name in values]
        if not changed:
            return self.browse()
        stale_ids = []
        for instance in self:
            if not any(
                (values[name] or False) != (instance[name] or False) for name in changed
            ):
                continue
            client_id = values.get("client_id", instance.client_id)
            if not instance.client_id and not client_id:
                continue
            stale_ids.append(instance.id)
        return self.browse(stale_ids)

    def _clear_managed_access_token(self, values):
        """Drop the stored token, so that the next call asks for a fresh one.

        No token is requested here: the managed flow gets one on the next
        Shopify call, with the credentials that were just stored. A token
        written along with the new credentials is no more trustworthy than the
        stored one, so it goes too, unless the instance just left the managed
        flow: that token is the static one to use from now on, and only its
        managed expiry is dropped.
        """
        managed = self.filtered("client_id")
        if managed:
            managed.write({"access_token": False, "access_token_expires_at": False})
        legacy = self - managed
        if legacy:
            cleared = {"access_token_expires_at": False}
            if "access_token" not in values:
                cleared["access_token"] = False
            legacy.write(cleared)

    def _shopify_app_credentials(self):
        """Return the app client credentials, or ``None`` for static tokens.

        The Client ID drives the Shopify Dev Dashboard flow, because the client
        secret is also used by installations that only verify webhook HMAC.
        """
        self.ensure_one()
        client_id = (self.client_id or "").strip()
        client_secret = (self.webhook_secret or "").strip()
        if not client_id:
            return None
        if not client_secret:
            raise UserError(
                self.env._(
                    "The Shopify app credentials of %s are incomplete: set the "
                    "Shopify App Client Secret next to the Client ID.",
                    self.display_name,
                )
            )
        return client_id, client_secret

    def _has_valid_managed_access_token(self):
        """Return whether a token issued for the client credentials is usable.

        A token without a recorded expiry was not issued by this flow, so it is
        never reused when a Client ID asks for managed tokens. Static tokens
        never reach this check.

        A token is given up a safety margin before the expiry Shopify issued,
        so that requests sent with it do not arrive once it has expired. The
        stored expiry stays the one Shopify issued.
        """
        self.ensure_one()
        if not self.access_token or not self.access_token_expires_at:
            return False
        usable_until = self.access_token_expires_at - timedelta(
            seconds=ACCESS_TOKEN_EXPIRY_MARGIN_SECONDS
        )
        return usable_until > fields.Datetime.now()

    def _request_access_token(self):
        """Store and return a token issued for the app client credentials."""
        self.ensure_one()
        credentials = self._shopify_app_credentials()
        if not credentials:
            raise UserError(
                self.env._(
                    "Set the Shopify App Client ID of %s to request an access token.",
                    self.display_name,
                )
            )
        client_id, client_secret = credentials
        token = request_access_token(self.shop_url, client_id, client_secret)
        self.write(
            {
                "access_token": token["access_token"],
                "access_token_expires_at": fields.Datetime.now()
                + timedelta(seconds=token["expires_in"]),
            }
        )
        return token["access_token"]

    def _lock_for_access_token_renewal(self, cr):
        """Take the renewal lock of this instance in the transaction of ``cr``.

        Return whether the row is visible to ``cr``. An instance created by the
        calling transaction is not committed yet, so no other worker can renew
        its token and there is nothing to serialise.

        The lock is an advisory one rather than ``SELECT ... FOR UPDATE``
        because ``cr`` runs in a transaction of its own: a row lock would queue
        behind the one the calling transaction takes when it flushes a pending
        write of the same instance, and wait for our own transaction until the
        timeout elapses. ``action_test_connection`` has exactly that shape, and
        only survives a row lock because Odoo defers the ``UPDATE`` until the
        next flush. An advisory lock never collides with the row locks the ORM
        takes, so the renewal stops depending on when a flush happens.
        """
        self.ensure_one()
        cr.execute(
            "SELECT set_config(%s, %s, true)",
            ["lock_timeout", f"{ACCESS_TOKEN_LOCK_TIMEOUT_SECONDS}s"],
        )
        cr.execute("SELECT id FROM shopify_instance WHERE id = %s", [self.id])
        if not cr.rowcount:
            return False
        cr.execute(
            "SELECT pg_advisory_xact_lock(hashtext('shopify.instance'), %s)",
            [self.id],
        )
        return True

    def _renew_access_token_locked(self):
        """Request an access token, letting a single worker renew at a time.

        The lock lives in a transaction of its own, so a long running job never
        keeps the instance row locked while it works, and the token is durable
        as soon as Shopify issues it. Workers that waited for the lock check the
        token again and reuse the one the first worker just stored.

        Renewing without the lock stays reserved for the state only the calling
        transaction knows about, never for a lock another worker holds.
        """
        self.ensure_one()
        try:
            with self.env.registry.cursor() as cr:
                if not self._lock_for_access_token_renewal(cr):
                    return self._request_access_token()
                instance = self.with_env(
                    api.Environment(cr, self.env.uid, self.env.context, su=self.env.su)
                )
                if self._credentials_differ_from(instance):
                    # The calling transaction changed the credentials without
                    # committing them: only it knows what to authenticate with.
                    return self._request_access_token()
                if instance._has_valid_managed_access_token():
                    token = instance.access_token
                else:
                    token = instance._request_access_token()
        except psycopg2.errors.LockNotAvailable as error:
            raise self._access_token_lock_timeout_error() from error
        self.invalidate_recordset(["access_token", "access_token_expires_at"])
        return token

    def _access_token_lock_timeout_error(self):
        """Return the error to raise when another worker holds the lock.

        Requesting a second token here would defeat the lock, so the caller
        comes back instead: a job retries once the lock window has elapsed, and
        anyone else is told to try again.
        """
        self.ensure_one()
        _logger.warning(
            "Timed out waiting for the Shopify access token lock of %s.",
            self.display_name,
        )
        message = self.env._(
            "Another worker is renewing the Shopify access token of %s. "
            "Try again in a moment.",
            self.display_name,
        )
        if self.env.context.get("job_uuid"):
            return RetryableJobError(message, seconds=ACCESS_TOKEN_LOCK_TIMEOUT_SECONDS)
        return UserError(message)

    def _credentials_differ_from(self, instance):
        """Return whether ``instance`` authenticates against something else."""
        self.ensure_one()
        return any(
            self[name] != instance[name] for name in ACCESS_TOKEN_CREDENTIAL_FIELDS
        )

    def _shopify_access_token(self):
        """Return the access token to use, requesting one when needed."""
        self.ensure_one()
        if not self._shopify_app_credentials():
            return self.access_token
        if self._has_valid_managed_access_token():
            return self.access_token
        return self._renew_access_token_locked()

    def _shopify_client(self):
        self.ensure_one()
        return ShopifyClient(
            self.shop_url,
            self._shopify_access_token(),
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
            "client_id": False,
            "access_token": False,
            "access_token_expires_at": False,
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
