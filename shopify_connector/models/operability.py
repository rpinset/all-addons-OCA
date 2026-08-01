# pylint: disable=consider-merging-classes-inherited

from datetime import timedelta
from uuid import uuid4

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

from ..graphql import WEBHOOK_SUBSCRIPTIONS_QUERY
from ..lib.operability import state_count_label
from .instance import REQUIRED_WEBHOOK_TOPICS

BINDING_DASHBOARD_MODELS = (
    ("Products", "shopify.product.template"),
    ("Variants", "shopify.product.variant"),
    ("Collections", "shopify.collection"),
    ("Locations", "shopify.location"),
    ("Customers", "shopify.customer"),
    ("B2B Companies", "shopify.company"),
    ("Orders", "shopify.order"),
    ("Fulfillments", "shopify.fulfillment"),
)

DRIFT_CRONS = (
    (
        "shopify_connector.ir_cron_reconcile_shopify_products",
        "drift_products",
    ),
    (
        "shopify_connector.ir_cron_reconcile_shopify_inventory",
        "drift_inventory",
    ),
    (
        "shopify_connector.ir_cron_reconcile_shopify_orders",
        "drift_orders",
    ),
    (
        "shopify_connector.ir_cron_reconcile_shopify_customers",
        "drift_customers",
    ),
    (
        "shopify_connector_account.ir_cron_import_shopify_payouts",
        "drift_payouts",
    ),
)


class ShopifyBindingOperations(models.AbstractModel):
    _inherit = "shopify.binding.mixin"

    def action_reset_to_pending(self):
        self.write({"state": "pending", "error_message": False})
        return True

    def action_retry_sync(self):
        failed = self.filtered(lambda binding: binding.state == "error")
        failed.write({"state": "pending", "error_message": False})
        for binding in failed:
            binding._shopify_enqueue_fresh_retry()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": self.env._("Shopify retries queued"),
                "message": self.env._(
                    "%s failed bindings were reset and queued.", len(failed)
                ),
                "type": "success",
                "sticky": False,
            },
        }

    def _shopify_retry_options(self, channel="root.shopify.import"):
        self.ensure_one()
        return {
            "channel": channel,
            "description": self.env._(
                "Retry %(model)s %(record)s",
                model=self._description,
                record=self.display_name,
            ),
            "identity_key": (f"shopify.retry.{self._name}.{self.id}.{uuid4().hex}"),
        }

    def _shopify_enqueue_fresh_retry(self):  # noqa: C901
        self.ensure_one()
        instance = self.instance_id
        if not instance.active:
            return False
        product_binding = False
        customer_binding = False
        order_binding = False
        if self._name == "shopify.product.template":
            product_binding = self
        elif self._name in (
            "shopify.product.variant",
            "shopify.product.image",
        ):
            product_binding = self.template_binding_id
        elif self._name == "shopify.customer":
            customer_binding = self
        elif self._name == "shopify.customer.address":
            customer_binding = self.customer_binding_id
        elif self._name == "shopify.order":
            order_binding = self
        elif self._name in (
            "shopify.order.line",
            "shopify.refund",
            "shopify.return",
        ):
            order_binding = self.order_binding_id

        if product_binding:
            self.env["shopify.product.template"].with_delay(
                **self._shopify_retry_options()
            )._job_import_product_from_api(instance.id, product_binding.shopify_id)
        elif self._name in ("shopify.collection",):
            instance.with_delay(
                **self._shopify_retry_options()
            )._job_fetch_products_bulk()
        elif self._name == "shopify.location":
            instance.with_delay(**self._shopify_retry_options())._job_import_locations()
        elif customer_binding:
            self.env["shopify.customer"].with_delay(
                **self._shopify_retry_options()
            )._job_import_customer_from_api(instance.id, customer_binding.shopify_id)
        elif self._name in (
            "shopify.company",
            "shopify.company.location",
            "shopify.company.contact",
            "shopify.catalog",
        ):
            instance.with_delay(**self._shopify_retry_options())._job_import_b2b()
        elif order_binding:
            if order_binding.is_draft:
                self.env["shopify.order"].with_delay(
                    **self._shopify_retry_options()
                )._job_import_draft_from_api(instance.id, order_binding.shopify_id)
            else:
                self.env["shopify.order"].with_delay(
                    **self._shopify_retry_options()
                )._job_import_order_from_api(instance.id, order_binding.shopify_id)
        elif self._name == "shopify.fulfillment.order":
            self.order_binding_id.with_delay(
                **self._shopify_retry_options()
            )._job_refresh_fulfillment_orders()
        elif self._name == "shopify.fulfillment":
            if self.shopify_id:
                self.env["shopify.fulfillment"].with_delay(
                    **self._shopify_retry_options()
                )._job_import_from_shopify(instance.id, self.shopify_id)
            else:
                self.order_binding_id.with_delay(
                    **self._shopify_retry_options()
                )._job_refresh_fulfillment_orders()
        else:
            raise UserError(
                self.env._(
                    "No safe automatic retry route is configured for %s.",
                    self._description,
                )
            )
        return True


class ShopifyInstanceOperability(models.Model):
    _inherit = "shopify.instance"

    log_retention_days = fields.Integer(
        required=True,
        default=30,
    )
    webhook_retention_days = fields.Integer(
        required=True,
        default=30,
    )
    webhook_health_checked_at = fields.Datetime(readonly=True)
    webhook_missing_topics = fields.Text(readonly=True)
    dashboard_products = fields.Char(compute="_compute_operability_dashboard")
    dashboard_variants = fields.Char(compute="_compute_operability_dashboard")
    dashboard_collections = fields.Char(compute="_compute_operability_dashboard")
    dashboard_locations = fields.Char(compute="_compute_operability_dashboard")
    dashboard_customers = fields.Char(compute="_compute_operability_dashboard")
    dashboard_companies = fields.Char(compute="_compute_operability_dashboard")
    dashboard_orders = fields.Char(compute="_compute_operability_dashboard")
    dashboard_fulfillments = fields.Char(compute="_compute_operability_dashboard")
    dashboard_financial = fields.Char(compute="_compute_operability_dashboard")
    dashboard_queue_backlog = fields.Integer(compute="_compute_operability_dashboard")
    dashboard_recent_errors = fields.Text(compute="_compute_operability_dashboard")
    dashboard_webhooks = fields.Text(compute="_compute_operability_dashboard")
    dashboard_drift_crons = fields.Text(compute="_compute_operability_dashboard")
    dashboard_table_sizes = fields.Text(compute="_compute_operability_dashboard")

    @api.constrains("log_retention_days", "webhook_retention_days")
    def _check_operability_retention(self):
        for instance in self:
            if instance.log_retention_days <= 0 or instance.webhook_retention_days <= 0:
                raise ValidationError(
                    self.env._("Retention periods must be greater than zero.")
                )

    def _dashboard_state_label(self, model_name):
        self.ensure_one()
        groups = (
            self.env[model_name]
            .sudo()
            ._read_group(
                [("instance_id", "=", self.id)],
                groupby=["state"],
                aggregates=["__count"],
            )
        )
        return state_count_label({state: count for state, count in groups if state})

    def _dashboard_queue_domain(self):
        self.ensure_one()
        return [
            ("channel", "=like", "root.shopify%"),
            (
                "state",
                "in",
                ("pending", "enqueued", "started", "wait_dependencies"),
            ),
            ("company_id", "in", (False, self.company_id.id)),
            "|",
            ("identity_key", "=like", f"%.{self.id}"),
            ("identity_key", "=like", f"%.{self.id}.%"),
        ]

    @api.depends("active")
    def _compute_operability_dashboard(self):
        table_sizes = self._shopify_table_sizes()
        cron_model = self.env["ir.cron"].sudo()
        crons = [
            (self.env.ref(xmlid, raise_if_not_found=False), entity)
            for xmlid, entity in DRIFT_CRONS
        ]
        crons = [(cron, entity) for cron, entity in crons if cron and cron.exists()]
        for instance in self:
            labels = {
                model_name: instance._dashboard_state_label(model_name)
                for _label, model_name in BINDING_DASHBOARD_MODELS
            }
            instance.dashboard_products = labels["shopify.product.template"]
            instance.dashboard_variants = labels["shopify.product.variant"]
            instance.dashboard_collections = labels["shopify.collection"]
            instance.dashboard_locations = labels["shopify.location"]
            instance.dashboard_customers = labels["shopify.customer"]
            instance.dashboard_companies = labels["shopify.company"]
            instance.dashboard_orders = labels["shopify.order"]
            instance.dashboard_fulfillments = labels["shopify.fulfillment"]
            if "shopify.payout" in self.env.registry:
                payout = instance._dashboard_state_label("shopify.payout")
                dispute = instance._dashboard_state_label("shopify.dispute")
                instance.dashboard_financial = f"Payouts: {payout}\nDisputes: {dispute}"
            else:
                instance.dashboard_financial = self.env._("Module not installed")
            instance.dashboard_queue_backlog = (
                self.env["queue.job"]
                .sudo()
                .search_count(instance._dashboard_queue_domain())
            )
            errors = (
                self.env["shopify.log"]
                .sudo()
                .search(
                    [
                        ("instance_id", "=", instance.id),
                        ("level", "=", "error"),
                    ],
                    order="create_date desc",
                    limit=3,
                )
            )
            instance.dashboard_recent_errors = "\n".join(
                f"{fields.Datetime.to_string(log.create_date)} · "
                f"{log.entity}: {(log.message or '')[:120]}"
                for log in errors
            ) or self.env._("No recent errors")
            instance.dashboard_webhooks = instance._dashboard_webhook_summary()
            lastcall_field = "lastcall" if "lastcall" in cron_model._fields else False
            drift_lines = []
            for cron, entity in crons:
                last_run = (
                    fields.Datetime.to_string(cron[lastcall_field])
                    if lastcall_field and cron[lastcall_field]
                    else self.env._("not run yet")
                )
                result = (
                    self.env["shopify.log"]
                    .sudo()
                    .search(
                        [
                            ("instance_id", "=", instance.id),
                            ("entity", "=", entity),
                        ],
                        order="create_date desc",
                        limit=1,
                    )
                )
                result_line = (
                    (
                        f"{fields.Datetime.to_string(result.create_date)} "
                        f"[{result.level}] {result.message}"
                    )
                    if result
                    else self.env._("no result log")
                )
                drift_lines.append(f"{cron.name}: {last_run}\n  {result_line}")
            instance.dashboard_drift_crons = "\n".join(drift_lines) or self.env._(
                "No drift crons installed"
            )
            instance.dashboard_table_sizes = table_sizes

    @api.model
    def _shopify_table_sizes(self):
        tables = (
            ("Logs", "shopify_log"),
            ("Webhooks", "shopify_webhook_event"),
            ("Queue", "queue_job"),
        )
        values = []
        for label, table in tables:
            self.env.cr.execute(
                """
                SELECT CASE
                    WHEN to_regclass(%s) IS NULL THEN 'not installed'
                    ELSE pg_size_pretty(
                        pg_total_relation_size(to_regclass(%s))
                    )
                END
                """,
                (table, table),
            )
            values.append(f"{label}: {self.env.cr.fetchone()[0]}")
        return "\n".join(values)

    def _dashboard_webhook_summary(self):
        self.ensure_one()
        event_model = self.env["shopify.webhook.event"].sudo()
        if not self.webhook_health_checked_at:
            remote = self.env._("Remote subscriptions: not checked")
        elif self.webhook_missing_topics:
            remote = self.env._("Remote subscriptions: repair required")
        else:
            remote = self.env._("Remote subscriptions: healthy")
        lines = [remote]
        for topic in REQUIRED_WEBHOOK_TOPICS:
            event = event_model.search(
                [
                    ("instance_id", "=", self.id),
                    ("topic", "=", topic),
                ],
                order="create_date desc",
                limit=1,
            )
            received = (
                fields.Datetime.to_string(event.create_date)
                if event
                else self.env._("never")
            )
            lines.append(f"{topic}: {received}")
        return "\n".join(lines)

    def action_check_webhook_health(self):
        self.ensure_one()
        data = self._shopify_client().execute(WEBHOOK_SUBSCRIPTIONS_QUERY)
        callback_url = self._webhook_callback_url()
        subscriptions = {
            node.get("topic"): ((node.get("endpoint") or {}).get("callbackUrl"))
            for node in (data.get("webhookSubscriptions", {}).get("nodes", []))
            if isinstance(node, dict) and node.get("topic")
        }
        missing = [
            topic
            for topic in REQUIRED_WEBHOOK_TOPICS
            if subscriptions.get(topic) != callback_url
        ]
        self.write(
            {
                "webhook_health_checked_at": fields.Datetime.now(),
                "webhook_missing_topics": "\n".join(missing),
            }
        )
        self._write_log(
            entity="webhook_health",
            direction="import",
            level="warning" if missing else "info",
            message=(
                self.env._(
                    "%s webhook subscriptions are missing or misrouted.", len(missing)
                )
                if missing
                else self.env._("All required webhook subscriptions are healthy.")
            ),
            record=self,
        )
        return True

    def action_open_binding_errors(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Shopify Binding Errors"),
            "res_model": "shopify.log",
            "view_mode": "list",
            "domain": [
                ("instance_id", "=", self.id),
                ("level", "=", "error"),
            ],
            "context": {"search_default_group_entity": 1},
        }


class ShopifyLogOperations(models.Model):
    _inherit = "shopify.log"

    def action_open_related_record(self):
        self.ensure_one()
        if (
            not self.res_model
            or not self.res_id
            or self.res_model not in self.env.registry
        ):
            raise UserError(self.env._("This log has no related record."))
        record = self.env[self.res_model].browse(self.res_id).exists()
        if not record:
            raise UserError(self.env._("The related record no longer exists."))
        return {
            "type": "ir.actions.act_window",
            "name": record.display_name,
            "res_model": record._name,
            "res_id": record.id,
            "view_mode": "form",
            "target": "current",
        }


class ShopifyWebhookRetention(models.Model):
    _inherit = "shopify.webhook.event"

    @api.autovacuum
    def _gc_shopify_webhook_events(self):
        self._prune_done_events()

    @api.model
    def _cron_prune(self):
        return self._prune_done_events()

    @api.model
    def _prune_done_events(self):
        count = 0
        instances = (
            self.env["shopify.instance"]
            .sudo()
            .with_context(active_test=False)
            .search([("id", "!=", False)])
        )
        for instance in instances:
            cutoff = fields.Datetime.now() - timedelta(
                days=instance.webhook_retention_days
            )
            events = self.sudo().search(
                [
                    ("instance_id", "=", instance.id),
                    ("state", "=", "done"),
                    ("create_date", "<", cutoff),
                ]
            )
            count += len(events)
            events.unlink()
        return count
