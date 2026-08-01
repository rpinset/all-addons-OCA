from __future__ import annotations

# pylint: disable=consider-merging-classes-inherited
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.fields import Command

from ..graphql.order import (
    DRAFT_ORDER_BY_ID_QUERY,
    DRAFT_ORDERS_QUERY,
    ORDER_BY_ID_QUERY,
    REFUND_BY_ID_QUERY,
    RETURN_BY_ID_QUERY,
    orders_bulk_query,
)
from ..lib.bulk import ShopifyBulkRunner
from ..lib.order import (
    decimal_amount,
    line_diffs,
    normalize_order_payload,
    normalize_refund_payload,
    payload_digest,
    selected_money,
    shopify_gid,
)
from .webhook_event import WEBHOOK_HANDLERS


class ShopifyOrderImportError(UserError):
    """A recoverable Shopify order import error."""

    def __init__(self, message, *, missing_tax=None):
        super().__init__(message)
        self.missing_tax = missing_tax


def _utc_datetime(value):
    if not value:
        return False
    parsed = (
        value
        if isinstance(value, datetime)
        else datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    )
    if parsed.tzinfo:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


def _exact_difference(actual, expected):
    return abs(Decimal(str(actual)) - decimal_amount(expected))


class ShopifyInstanceOrderSync(models.Model):
    _inherit = "shopify.instance"

    def action_import_orders(self):
        self.ensure_one()
        if self.state != "connected":
            raise UserError(
                self.env._("Connect the Shopify instance before importing orders.")
            )
        if (
            self.order_import_date_from
            and self.order_import_date_to
            and self.order_import_date_from > self.order_import_date_to
        ):
            raise UserError(
                self.env._("The order import start date must precede the end date.")
            )
        self.with_delay(
            description=self.env._("Import Shopify orders for %s", self.name),
            identity_key=(
                f"shopify.orders.bulk.{self.id}."
                f"{self.order_import_date_from}.{self.order_import_date_to}"
            ),
        )._job_fetch_orders_bulk(
            fields.Date.to_string(self.order_import_date_from),
            fields.Date.to_string(self.order_import_date_to),
        )
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": self.env._("Order import queued"),
                "message": self.env._(
                    "Orders and draft orders will import in the background."
                ),
                "type": "success",
                "sticky": False,
            },
        }

    @api.model
    def _cron_reconcile_orders(self):
        for instance in self.search(
            [("active", "=", True), ("state", "=", "connected")]
        ):
            instance.with_delay(
                description=self.env._(
                    "Reconcile Shopify orders for %s", instance.name
                ),
                identity_key=f"shopify.orders.reconcile.{instance.id}",
            )._job_fetch_orders_bulk(
                fields.Date.to_string(
                    fields.Date.context_today(instance) - timedelta(days=2)
                ),
                False,
            )
            instance._write_log(
                entity="drift_orders",
                direction="import",
                level="info",
                message=self.env._(
                    "Daily order drift reconciliation queued with a two-day overlap."
                ),
                record=instance,
            )

    def _job_fetch_orders_bulk(self, date_from=False, date_to=False):
        self = self.sudo()
        self.ensure_one()
        if not self.active:
            return 0
        records = ShopifyBulkRunner(self._shopify_client()).run(
            orders_bulk_query(date_from, date_to)
        )
        orders = [
            row
            for row in records
            if not row.get("__parentId")
            and str(row.get("id") or "").startswith("gid://shopify/Order/")
        ]
        for order in orders:
            self.env["shopify.order"].with_delay(
                description=self.env._(
                    "Import Shopify order %s", (order.get("name") or order["id"])
                ),
                identity_key=f"shopify.order.import.{self.id}.{order['id']}",
            )._job_import_order_from_api(self.id, order["id"])
        draft_count = self._queue_draft_orders(date_from, date_to)
        self._write_log(
            entity="order",
            direction="import",
            level="info",
            message=self.env._(
                "%(orders)s orders and %(drafts)s draft orders queued for import.",
                orders=len(orders),
                drafts=draft_count,
            ),
            record=self,
        )
        return len(orders) + draft_count

    def _queue_draft_orders(self, date_from=False, date_to=False):
        query_terms = []
        if date_from:
            query_terms.append(f"created_at:>={str(date_from)[:10]}")
        if date_to:
            query_terms.append(f"created_at:<={str(date_to)[:10]}")
        after = None
        count = 0
        while True:
            data = self._shopify_client().execute(
                DRAFT_ORDERS_QUERY,
                {"after": after, "query": " ".join(query_terms) or None},
            )
            connection = data.get("draftOrders") or {}
            for payload in connection.get("nodes") or []:
                draft = normalize_order_payload(payload, is_draft=True)
                self.env["shopify.order"].with_delay(
                    description=self.env._(
                        "Import Shopify draft order %s", draft["name"]
                    ),
                    identity_key=f"shopify.draft.import.{self.id}.{draft['id']}",
                )._job_import_order(self.id, draft, payload_normalized=True)
                count += 1
            page_info = connection.get("pageInfo") or {}
            if not page_info.get("hasNextPage"):
                break
            after = page_info.get("endCursor")
            if not after:
                raise ShopifyOrderImportError(
                    self.env._("Shopify returned an invalid draft-order page cursor.")
                )
        return count


class ShopifyOrderSync(models.Model):
    _inherit = "shopify.order"

    @api.model
    def _job_import_order_from_api(self, instance_id, order_id, webhook_payload=None):
        instance = self.env["shopify.instance"].sudo().browse(instance_id).exists()
        if not instance or not instance.active:
            return False
        client = instance._shopify_client()
        data = client.execute(ORDER_BY_ID_QUERY, {"id": shopify_gid("Order", order_id)})
        payload = data.get("order")
        if not payload:
            return False
        webhook_payload = webhook_payload or {}
        for key in (
            "exchangeOriginOrder",
            "exchange_origin_order",
            "exchangeOriginalOrder",
            "exchange_original_order",
            "originalOrder",
            "original_order",
            "exchangeOriginalOrderId",
            "exchange_original_order_id",
            "exchange_origin_order_id",
            "originalOrderId",
            "original_order_id",
        ):
            if webhook_payload.get(key):
                payload[key] = webhook_payload[key]
        refund_nodes = payload.get("refunds") or []
        if isinstance(refund_nodes, dict):
            refund_nodes = refund_nodes.get("nodes") or []
        payload["refunds"] = {
            "nodes": [
                detail
                for node in refund_nodes
                if (
                    detail := client.execute(
                        REFUND_BY_ID_QUERY, {"id": node["id"]}
                    ).get("refund")
                )
            ]
        }
        payload["returns"] = {
            "nodes": [
                detail
                for node in (payload.get("returns") or {}).get("nodes") or []
                if (
                    detail := client.execute(
                        RETURN_BY_ID_QUERY, {"id": node["id"]}
                    ).get("return")
                )
            ]
        }
        return self._job_import_order(instance.id, payload)

    @api.model
    def _job_import_draft_from_api(self, instance_id, draft_id):
        instance = self.env["shopify.instance"].sudo().browse(instance_id).exists()
        if not instance or not instance.active:
            return False
        data = instance._shopify_client().execute(
            DRAFT_ORDER_BY_ID_QUERY,
            {"id": shopify_gid("DraftOrder", draft_id)},
        )
        payload = data.get("draftOrder")
        if not payload:
            return False
        return self._job_import_order(instance.id, payload, is_draft=True)

    @api.model
    def _job_import_order(
        self,
        instance_id,
        payload,
        *,
        payload_normalized=False,
        is_draft=False,
    ):
        self = self.sudo()
        instance = self.env["shopify.instance"].browse(instance_id).exists()
        if not instance or not instance.active:
            return False
        order_data = (
            payload
            if payload_normalized
            else normalize_order_payload(payload, is_draft=is_draft)
        )
        digest = payload_digest(order_data)
        self.env.cr.execute(
            "SELECT pg_advisory_xact_lock(%s, hashtext(%s))",
            (instance.id, order_data["id"]),
        )
        if order_data["is_draft"] and order_data["completed_order_id"]:
            self.env.cr.execute(
                "SELECT pg_advisory_xact_lock(%s, hashtext(%s))",
                (instance.id, order_data["completed_order_id"]),
            )
        binding = self.search(
            [
                ("instance_id", "=", instance.id),
                ("shopify_id", "=", order_data["id"]),
            ],
            limit=1,
        )
        if binding and binding.payload_digest == digest and binding.state == "synced":
            return binding.id
        if not binding:
            binding = self.create(
                {
                    "instance_id": instance.id,
                    "shopify_id": order_data["id"],
                    "order_name": order_data["name"],
                    "source": order_data["source"],
                    "is_draft": order_data["is_draft"],
                }
            )
        if order_data["source"] == "pos":
            return self._route_shopify_pos_order(binding, instance, order_data, digest)
        return self._process_shopify_order(binding, instance, order_data, digest)

    def _route_shopify_pos_order(self, binding, instance, order_data, digest):
        """Extension boundary used by the optional POS connector."""
        binding.write(
            {
                "order_name": order_data["name"],
                "order_number": order_data["number"],
                "financial_status": order_data["financial_status"],
                "fulfillment_status": order_data["fulfillment_status"],
                "source": "pos",
                "source_name": order_data["source_name"],
                "source_identifier": order_data["source_identifier"],
                "raw_payload": order_data["raw"],
                "payload_digest": digest,
                "external_updated_at": _utc_datetime(order_data["updated_at"]),
                "state": "pending",
                "error_message": False,
            }
        )
        instance._write_log(
            entity="order",
            direction="import",
            level="info",
            message=self.env._(
                "Shopify POS order %s is pending because POS import is disabled.",
                order_data["name"],
            ),
            record=binding,
        )
        return binding.id

    def _process_shopify_order(self, binding, instance, order_data, digest):
        try:
            with self.env.cr.savepoint():
                sale_order = self._build_order(binding, instance, order_data)
                completed_draft = order_data["is_draft"] and binding.replaced_by_id
                if not completed_draft:
                    self._apply_state(binding, sale_order, order_data)
                    self._apply_invoice_and_payments(binding, order_data)
                    self._apply_returns(binding, order_data)
                    self._apply_refunds(binding, order_data)
                self._write_success(binding, sale_order, order_data, digest)
        except Exception as exc:
            values = {
                "state": "error",
                "error_message": str(exc),
                "raw_payload": order_data.get("raw"),
            }
            missing = getattr(exc, "missing_tax", None)
            if missing:
                values.update(
                    {
                        "missing_tax_rate": missing["rate"],
                        "missing_tax_country_id": missing["country_id"],
                        "missing_tax_included": missing["included"],
                    }
                )
            binding.write(values)
            instance._write_log(
                entity="order",
                direction="import",
                level="error",
                message=self.env._(
                    "Order %(order)s import failed: %(error)s",
                    order=order_data["name"],
                    error=exc,
                ),
                record=binding,
            )
            return False
        instance._write_log(
            entity="order",
            direction="import",
            level="info",
            message=self.env._("Imported Shopify order %s.", order_data["name"]),
            record=binding,
        )
        return binding.id

    def _build_order(self, binding, instance, order_data):
        sale_order = binding.odoo_id
        draft_binding = self.env["shopify.order"]
        completed_binding = self.env["shopify.order"]
        if order_data["is_draft"] and order_data["completed_order_id"]:
            completed_binding = self.search(
                [
                    ("instance_id", "=", instance.id),
                    ("shopify_id", "=", order_data["completed_order_id"]),
                    ("odoo_id", "!=", False),
                ],
                limit=1,
            )
            if completed_binding:
                sale_order = completed_binding.odoo_id
                binding.replaced_by_id = completed_binding
        if not completed_binding and not sale_order and not order_data["is_draft"]:
            draft_binding = self.search(
                [
                    ("instance_id", "=", instance.id),
                    ("is_draft", "=", True),
                    ("completed_order_shopify_id", "=", order_data["id"]),
                    ("odoo_id", "!=", False),
                ],
                limit=1,
            )
            sale_order = draft_binding.odoo_id
        if completed_binding:
            binding.odoo_id = sale_order
            self._verify_total(
                sale_order,
                self._currency(instance, order_data),
                instance,
                order_data,
            )
            return sale_order
        if sale_order and self._is_delivered(sale_order):
            differences = line_diffs(
                self._existing_line_snapshot(binding, sale_order),
                [
                    {"id": line["id"], "quantity": line["quantity"]}
                    for line in order_data["lines"]
                ],
            )
            if any(differences.values()):
                raise ShopifyOrderImportError(
                    self.env._(
                        "Shopify edited order lines after Odoo delivery; "
                        "manual resolution is required."
                    )
                )
        currency = self._currency(instance, order_data)
        partner = self._partner(instance, order_data)
        pricelist = self._pricelist(instance, currency)
        values = {
            "partner_id": partner.id,
            "company_id": instance.company_id.id,
            "pricelist_id": pricelist.id,
            "currency_id": currency.id,
            "origin": order_data["name"],
            "client_order_ref": order_data["name"],
            "date_order": _utc_datetime(order_data["created_at"])
            or fields.Datetime.now(),
            "note": order_data["note"],
            "shopify_discount_codes": ", ".join(order_data["discount_codes"]),
            "shopify_tags": ", ".join(order_data["tags"]),
            "shopify_note": order_data["note"],
            "shopify_risk_level": order_data["risk_level"],
        }
        values.update(self._shopify_order_extra_values(instance, order_data))
        if sale_order:
            if (
                sale_order.state in ("cancel", "done")
                and not order_data["cancelled_at"]
            ):
                raise ShopifyOrderImportError(
                    self.env._(
                        "The existing Odoo order can no longer accept Shopify edits."
                    )
                )
            write_values = values
            if sale_order.state not in ("draft", "sent"):
                # Odoo 19 rejects these commercial fields on confirmed
                # orders even when their values have not changed.
                immutable_fields = {
                    "partner_id",
                    "company_id",
                    "pricelist_id",
                    "currency_id",
                    "date_order",
                }
                write_values = {
                    key: value
                    for key, value in values.items()
                    if key not in immutable_fields
                }
            sale_order.with_context(shopify_order_import=True).write(write_values)
        else:
            sale_order = (
                self.env["sale.order"]
                .with_company(instance.company_id)
                .with_context(shopify_order_import=True)
                .create(values)
            )
        binding.odoo_id = sale_order
        if draft_binding:
            draft_binding.line_binding_ids.mapped("odoo_id").unlink()
            draft_binding.replaced_by_id = binding
        self._apply_lines(binding, sale_order, instance, order_data)
        self._verify_total(sale_order, currency, instance, order_data)
        return sale_order

    def _shopify_order_extra_values(self, instance, order_data):
        """Allow optional modules to supply sale-order routing values."""
        return {}

    def _existing_line_snapshot(self, binding, sale_order):
        result = []
        by_line = {item.odoo_id.id: item for item in binding.line_binding_ids}
        for line in sale_order.order_line:
            line_binding = by_line.get(line.id)
            if line_binding:
                result.append(
                    {
                        "id": line_binding.shopify_id,
                        "quantity": int(line.product_uom_qty),
                    }
                )
        return result

    def _currency(self, instance, order_data):
        side = (
            "presentment" if instance.order_currency_policy == "presentment" else "shop"
        )
        code = order_data["total"][side]["currency"]
        currency = (
            self.env["res.currency"]
            .with_context(active_test=False)
            .search([("name", "=", code)], limit=1)
        )
        if not currency:
            raise ShopifyOrderImportError(
                self.env._("Shopify order currency %s is not configured in Odoo.", code)
            )
        return currency

    def _partner(self, instance, order_data):
        if order_data["customer_id"]:
            customer = self.env["shopify.customer"].search(
                [
                    ("instance_id", "=", instance.id),
                    ("shopify_id", "=", order_data["customer_id"]),
                ],
                limit=1,
            )
            if customer:
                return customer.odoo_id
        if not instance.guest_partner_id:
            raise ShopifyOrderImportError(
                self.env._("The Shopify guest customer is not configured.")
            )
        return instance.guest_partner_id

    def _pricelist(self, instance, currency):
        if instance.product_pricelist_id.currency_id == currency:
            return instance.product_pricelist_id
        pricelist = (
            self.env["product.pricelist"]
            .with_company(instance.company_id)
            .search(
                [
                    ("company_id", "=", instance.company_id.id),
                    ("currency_id", "=", currency.id),
                    ("name", "=", f"Shopify {instance.name} ({currency.name})"),
                ],
                limit=1,
            )
        )
        if not pricelist:
            pricelist = (
                self.env["product.pricelist"]
                .with_company(instance.company_id)
                .create(
                    {
                        "name": f"Shopify {instance.name} ({currency.name})",
                        "currency_id": currency.id,
                        "company_id": instance.company_id.id,
                    }
                )
            )
        return pricelist

    def _apply_lines(self, binding, sale_order, instance, order_data):
        existing = {item.shopify_id: item for item in binding.line_binding_ids}
        incoming_ids = set()
        country = self._tax_country(order_data)
        for line_data in order_data["lines"]:
            incoming_ids.add(line_data["id"])
            line_binding = existing.get(line_data["id"])
            if line_data["quantity"] <= 0:
                if line_binding:
                    line_binding.odoo_id.unlink()
                continue
            product = self._line_product(instance, line_data)
            taxes = self._mapped_taxes(
                instance,
                line_data["tax_lines"],
                country,
                order_data["taxes_included"],
            )
            selected_total = selected_money(
                line_data["discounted_total"],
                instance.order_currency_policy == "presentment",
            )
            selected_unit = selected_money(
                line_data["unit_price"],
                instance.order_currency_policy == "presentment",
            )
            quantity = Decimal(str(line_data["quantity"]))
            discount_amount = decimal_amount(
                selected_unit["amount"]
            ) * quantity - decimal_amount(selected_total["amount"])
            original_total = decimal_amount(selected_unit["amount"]) * quantity
            discount_percent = (
                discount_amount * Decimal("100") / original_total
                if original_total
                else Decimal("0")
            )
            line_values = {
                "order_id": sale_order.id,
                "product_id": product.id,
                "name": line_data["title"] or product.display_name,
                "product_uom_qty": line_data["quantity"],
                "product_uom_id": product.uom_id.id,
                "price_unit": selected_unit["amount"],
                "discount": format(discount_percent, "f"),
                "tax_ids": [Command.set(taxes.ids)],
                "shopify_line_id": line_data["id"],
                "shopify_discount_amount": format(discount_amount, "f"),
                "shopify_expected_total": selected_total["amount"],
                "shopify_is_gift_card": line_data["gift_card"],
            }
            if line_binding:
                line_binding.odoo_id.with_context(shopify_order_import=True).write(
                    line_values
                )
                sale_line = line_binding.odoo_id
            else:
                sale_line = (
                    self.env["sale.order.line"]
                    .with_company(instance.company_id)
                    .with_context(shopify_order_import=True)
                    .create(line_values)
                )
                line_binding = self.env["shopify.order.line"].create(
                    {
                        "instance_id": instance.id,
                        "shopify_id": line_data["id"],
                        "order_binding_id": binding.id,
                        "odoo_id": sale_line.id,
                    }
                )
            line_binding.write(self._line_binding_values(line_data))
        for identifier, line_binding in existing.items():
            if identifier not in incoming_ids and not line_binding.is_shipping:
                line_binding.odoo_id.unlink()
        self._apply_shipping_lines(binding, sale_order, instance, order_data, country)

    def _line_binding_values(self, line_data):
        allocations = line_data["discount_allocations"]
        shop_discount = sum(
            decimal_amount(item["amount"]["shop"]["amount"]) for item in allocations
        )
        presentment_discount = sum(
            decimal_amount(item["amount"]["presentment"]["amount"])
            for item in allocations
        )
        return {
            "variant_shopify_id": line_data["variant_id"],
            "sku": line_data["sku"],
            "current_quantity": line_data["quantity"],
            "refundable_quantity": line_data["refundable_quantity"],
            "shop_unit_price": line_data["unit_price"]["shop"]["amount"],
            "presentment_unit_price": line_data["unit_price"]["presentment"]["amount"],
            "shop_discounted_total": line_data["discounted_total"]["shop"]["amount"],
            "presentment_discounted_total": line_data["discounted_total"][
                "presentment"
            ]["amount"],
            "shop_discount_total": format(shop_discount, "f"),
            "presentment_discount_total": format(presentment_discount, "f"),
            "is_gift_card": line_data["gift_card"],
            "last_sync_date": fields.Datetime.now(),
            "state": "synced",
            "error_message": False,
        }

    def _apply_shipping_lines(self, binding, sale_order, instance, order_data, country):
        instance._ensure_delivery_product()
        existing = {
            item.shopify_id: item
            for item in binding.line_binding_ids.filtered("is_shipping")
        }
        incoming_ids = set()
        for index, shipping in enumerate(order_data["shipping_lines"]):
            identifier = shipping["id"] or (
                f"gid://shopify/ShippingLine/{order_data['id'].rsplit('/', 1)[-1]}"
                f"-{index}"
            )
            incoming_ids.add(identifier)
            selected = selected_money(
                shipping["discounted_total"],
                instance.order_currency_policy == "presentment",
            )
            selected_original = selected_money(
                shipping["original_total"],
                instance.order_currency_policy == "presentment",
            )
            original_amount = decimal_amount(selected_original["amount"])
            discounted_amount = decimal_amount(selected["amount"])
            discount_percent = (
                (original_amount - discounted_amount) * Decimal("100") / original_amount
                if original_amount
                else Decimal("0")
            )
            taxes = self._mapped_taxes(
                instance,
                shipping["tax_lines"],
                country,
                order_data["taxes_included"],
            )
            values = {
                "order_id": sale_order.id,
                "product_id": instance.delivery_product_id.id,
                "name": shipping["title"],
                "product_uom_qty": 1,
                "product_uom_id": instance.delivery_product_id.uom_id.id,
                "price_unit": selected_original["amount"],
                "discount": format(discount_percent, "f"),
                "tax_ids": [Command.set(taxes.ids)],
                "shopify_line_id": identifier,
                "shopify_expected_total": selected["amount"],
                "shopify_is_shipping": True,
            }
            line_binding = existing.get(identifier)
            if line_binding:
                line_binding.odoo_id.with_context(shopify_order_import=True).write(
                    values
                )
            else:
                sale_line = (
                    self.env["sale.order.line"]
                    .with_company(instance.company_id)
                    .with_context(shopify_order_import=True)
                    .create(values)
                )
                self.env["shopify.order.line"].create(
                    {
                        "instance_id": instance.id,
                        "shopify_id": identifier,
                        "order_binding_id": binding.id,
                        "odoo_id": sale_line.id,
                        "is_shipping": True,
                        "current_quantity": 1,
                        "refundable_quantity": 1,
                        "shop_discounted_total": shipping["discounted_total"]["shop"][
                            "amount"
                        ],
                        "presentment_discounted_total": shipping["discounted_total"][
                            "presentment"
                        ]["amount"],
                        "last_sync_date": fields.Datetime.now(),
                        "state": "synced",
                    }
                )
        for identifier, line_binding in existing.items():
            if identifier not in incoming_ids:
                line_binding.odoo_id.unlink()

    def _line_product(self, instance, line_data):
        if line_data["gift_card"]:
            if not instance.gift_card_product_id:
                raise ShopifyOrderImportError(
                    self.env._("Configure the Shopify gift-card liability product.")
                )
            return instance.gift_card_product_id
        variant = self.env["shopify.product.variant"].search(
            [
                ("instance_id", "=", instance.id),
                ("shopify_id", "=", line_data["variant_id"]),
            ],
            limit=1,
        )
        if variant:
            return variant.odoo_id
        if (
            instance.unknown_product_policy == "placeholder"
            and instance.placeholder_product_id
        ):
            return instance.placeholder_product_id
        raise ShopifyOrderImportError(
            self.env._(
                "No product binding exists for Shopify variant %(variant)s "
                "(SKU %(sku)s).",
                variant=line_data["variant_id"] or "-",
                sku=line_data["sku"] or "-",
            )
        )

    def _tax_country(self, order_data):
        country_code = order_data.get("tax_country_code") or ""
        return self.env["res.country"].search([("code", "=", country_code)], limit=1)

    def _mapped_taxes(self, instance, tax_lines, country, included):
        taxes = self.env["account.tax"]
        for line in tax_lines:
            rate = format(decimal_amount(line["rate"]).normalize(), "f")
            line_country = country
            if line.get("country_code"):
                line_country = self.env["res.country"].search(
                    [("code", "=", line["country_code"])], limit=1
                )
            mapping = self.env["shopify.tax.mapping"].search(
                [
                    ("instance_id", "=", instance.id),
                    ("rate", "=", rate),
                    ("country_id", "=", line_country.id),
                    ("price_included", "=", included),
                ],
                limit=1,
            )
            if not mapping:
                raise ShopifyOrderImportError(
                    self.env._(
                        "No Shopify tax mapping exists for rate %(rate)s, "
                        "country %(country)s, included=%(included)s.",
                        rate=rate,
                        country=line_country.code or "-",
                        included=included,
                    ),
                    missing_tax={
                        "rate": rate,
                        "country_id": line_country.id,
                        "included": included,
                    },
                )
            taxes |= mapping.tax_id
        return taxes

    def _verify_total(self, sale_order, currency, instance, order_data):
        sale_order.invalidate_recordset(["amount_total"])
        expected = self._shopify_expected_order_total(instance, order_data)
        difference = _exact_difference(sale_order.amount_total, expected)
        rounding = Decimal(str(currency.rounding))
        if difference >= rounding / Decimal("2"):
            raise ShopifyOrderImportError(
                self.env._(
                    "Order total mismatch: Odoo %(odoo)s, Shopify %(shopify)s, "
                    "difference %(difference)s %(currency)s.",
                    odoo=sale_order.amount_total,
                    shopify=expected,
                    difference=format(difference, "f"),
                    currency=currency.name,
                )
            )

    def _shopify_expected_order_total(self, instance, order_data):
        """Return the exact source total the Odoo order must reproduce."""
        return selected_money(
            order_data["total"],
            instance.order_currency_policy == "presentment",
        )["amount"]

    def _apply_state(self, binding, sale_order, order_data):
        instance = binding.instance_id
        high_risk = (
            instance.high_risk_hold_enabled and order_data["risk_level"] == "HIGH"
        )
        risk_hold = high_risk or sale_order.shopify_risk_hold
        sale_order.write(
            {
                "shopify_risk_hold": risk_hold,
                "shopify_risk_level": order_data["risk_level"],
            }
        )
        if order_data["cancelled_at"]:
            if self._is_delivered(sale_order):
                raise ShopifyOrderImportError(
                    self.env._("Shopify cancelled an order already delivered in Odoo.")
                )
            if sale_order.state != "cancel":
                sale_order.action_cancel()
            return
        if self._should_confirm_shopify_order(instance, order_data, sale_order):
            sale_order.action_confirm()
        if risk_hold:
            sale_order.picking_ids.write({"shopify_risk_hold": True})
        if high_risk:
            if not sale_order.activity_ids.filtered(
                lambda activity: activity.summary
                == self.env._("Shopify high-risk order")
            ):
                sale_order.activity_schedule(
                    "mail.mail_activity_data_todo",
                    summary=self.env._("Shopify high-risk order"),
                    note=self.env._(
                        "Review the Shopify risk assessment and release the "
                        "risk hold before validating delivery."
                    ),
                )

    def _should_confirm_shopify_order(self, instance, order_data, sale_order):
        eligible = (
            order_data["financial_status"] == "PAID" and instance.auto_confirm_paid
        ) or (
            order_data["financial_status"] == "PARTIALLY_PAID"
            and instance.auto_confirm_partially_paid
        )
        return (
            not order_data["is_draft"]
            and instance.order_confirmation_policy == "auto"
            and eligible
            and sale_order.state in ("draft", "sent")
        )

    def _is_delivered(self, sale_order):
        return bool(
            sale_order.picking_ids.filtered(lambda picking: picking.state == "done")
        )

    def _apply_invoice_and_payments(self, binding, order_data):
        instance = binding.instance_id
        sale_order = binding.odoo_id
        should_invoice = (
            instance.order_invoicing_policy == "paid"
            and order_data["financial_status"] == "PAID"
        ) or (
            instance.order_invoicing_policy == "fulfillment"
            and order_data["fulfillment_status"] == "FULFILLED"
        )
        if not should_invoice or sale_order.state == "cancel":
            return
        if sale_order.state in ("draft", "sent"):
            sale_order.action_confirm()
            if sale_order.shopify_risk_hold:
                sale_order.picking_ids.write({"shopify_risk_hold": True})
        invoices = sale_order.invoice_ids.filtered(
            lambda move: move.move_type == "out_invoice" and move.state != "cancel"
        )
        if not invoices:
            invoices = sale_order._create_invoices()
        for invoice in invoices.filtered(lambda move: move.state == "draft"):
            invoice.action_post()
        for transaction in order_data["transactions"]:
            if (
                transaction["status"] != "SUCCESS"
                or transaction["kind"] not in ("SALE", "CAPTURE")
                or self.env["shopify.gateway.payment"].search_count(
                    [
                        ("instance_id", "=", instance.id),
                        (
                            "transaction_shopify_id",
                            "=",
                            transaction["id"],
                        ),
                    ]
                )
            ):
                continue
            invoice = invoices.filtered(lambda move: move.amount_residual > 0)[:1]
            if not invoice:
                break
            gateway = transaction["gateway"].strip().lower()
            journal = (
                instance.gift_card_journal_id
                if gateway in ("gift_card", "gift card")
                else self.env["shopify.gateway.journal"]
                .search(
                    [
                        ("instance_id", "=", instance.id),
                        ("gateway", "=", gateway),
                    ],
                    limit=1,
                )
                .journal_id
            )
            if not journal:
                raise ShopifyOrderImportError(
                    self.env._(
                        "No payment journal is mapped for Shopify gateway %s.",
                        (transaction["gateway"] or "-"),
                    )
                )
            amount = decimal_amount(
                selected_money(
                    transaction["amount"],
                    instance.order_currency_policy == "presentment",
                )["amount"]
            )
            amount = min(amount, Decimal(str(invoice.amount_residual)))
            if amount <= 0:
                continue
            register = (
                self.env["account.payment.register"]
                .with_context(
                    active_model="account.move",
                    active_ids=invoice.ids,
                )
                .create(
                    {
                        "journal_id": journal.id,
                        "amount": format(amount, "f"),
                        "payment_date": fields.Date.context_today(self),
                        "group_payment": False,
                    }
                )
            )
            payments = register._create_payments()
            payment = payments[:1]
            gateway_payment = self.env["shopify.gateway.payment"].create(
                {
                    "instance_id": instance.id,
                    "transaction_shopify_id": transaction["id"],
                    "order_binding_id": binding.id,
                    "payment_id": payment.id,
                    "gateway": transaction["gateway"],
                    "amount": format(amount, "f"),
                }
            )
            self._after_shopify_gateway_payment(gateway_payment, transaction, invoice)

    def _after_shopify_gateway_payment(self, gateway_payment, transaction, invoice):
        """Extension hook for optional financial modules."""
        return None

    def _apply_refunds(self, binding, order_data):
        for refund in order_data["refunds"]:
            self._apply_refund(binding, refund)

    def _apply_returns(self, binding, order_data):
        model = self.env["shopify.return"]
        for return_data in order_data["returns"]:
            return_binding = model.search(
                [
                    ("instance_id", "=", binding.instance_id.id),
                    ("shopify_id", "=", return_data["id"]),
                ],
                limit=1,
            )
            values = {
                "instance_id": binding.instance_id.id,
                "shopify_id": return_data["id"],
                "order_binding_id": binding.id,
                "name": return_data["name"],
                "return_status": return_data["status"],
                "total_quantity": return_data["total_quantity"],
                "created_at": _utc_datetime(return_data["created_at"]),
                "closed_at": _utc_datetime(return_data["closed_at"]),
                "return_lines": return_data["lines"],
                "exchange_lines": return_data["exchange_lines"],
                "raw_payload": return_data["raw"],
                "state": "synced",
                "error_message": False,
                "last_sync_date": fields.Datetime.now(),
            }
            if return_binding:
                return_binding.write(values)
            else:
                model.create(values)

    def _apply_refund(self, binding, refund):
        if not refund["id"]:
            return
        existing = self.env["shopify.refund"].search(
            [
                ("instance_id", "=", binding.instance_id.id),
                ("shopify_id", "=", refund["id"]),
            ],
            limit=1,
        )
        if existing and existing.state == "synced":
            return
        selected_side = binding.instance_id.order_currency_policy == "presentment"
        amount = decimal_amount(
            selected_money(refund["total"], selected_side)["amount"]
        )
        if not amount:
            amount = sum(
                decimal_amount(
                    selected_money(line["subtotal"], selected_side)["amount"]
                )
                + decimal_amount(selected_money(line["tax"], selected_side)["amount"])
                for line in refund["lines"]
            ) + sum(
                decimal_amount(selected_money(item["amount"], selected_side)["amount"])
                + decimal_amount(selected_money(item["tax"], selected_side)["amount"])
                for item in refund["adjustments"]
            )
        if not existing:
            existing = self.env["shopify.refund"].create(
                {
                    "instance_id": binding.instance_id.id,
                    "shopify_id": refund["id"],
                    "order_binding_id": binding.id,
                }
            )
        restock = any(
            line["restock_type"] not in ("", "NO_RESTOCK") for line in refund["lines"]
        )
        existing.write(
            {
                "amount": format(amount, "f"),
                "currency_id": binding.order_currency_id.id
                or binding.odoo_id.currency_id.id,
                "note": refund["note"],
                "created_at": _utc_datetime(refund["created_at"]),
                "restock_requested": restock,
                "raw_payload": refund,
            }
        )
        self._write_refund_lines(existing, binding, refund, selected_side)
        invoices = binding.odoo_id.invoice_ids.filtered(
            lambda move: move.move_type == "out_invoice" and move.state == "posted"
        )
        if invoices and not existing.move_id:
            existing.move_id = self._create_refund_move(
                binding, invoices[0], refund, amount, selected_side
            )
        elif not invoices:
            self._adjust_uninvoiced_refund(binding, refund, amount)
        if restock:
            try:
                self._create_restock_return(binding, refund)
            except Exception as exc:
                binding.instance_id._write_log(
                    entity="refund",
                    direction="import",
                    level="warning",
                    message=self.env._(
                        "Refund imported, but the automatic stock return "
                        "could not be created: %s",
                        exc,
                    ),
                    record=existing,
                )
        existing.write(
            {
                "state": "synced",
                "error_message": False,
                "last_sync_date": fields.Datetime.now(),
            }
        )

    def _write_refund_lines(self, refund_binding, order_binding, refund, selected_side):
        existing = {line.shopify_id: line for line in refund_binding.line_ids}
        for line in refund["lines"]:
            order_line = order_binding.line_binding_ids.filtered(
                lambda item, line=line: item.shopify_id == line["line_id"]
            )[:1]
            values = {
                "refund_id": refund_binding.id,
                "shopify_id": line["id"],
                "order_line_binding_id": order_line.id,
                "quantity": line["quantity"],
                "subtotal": selected_money(line["subtotal"], selected_side)["amount"],
                "tax": selected_money(line["tax"], selected_side)["amount"],
                "restock_type": line["restock_type"],
            }
            if line["id"] in existing:
                existing[line["id"]].write(values)
            else:
                self.env["shopify.refund.line"].create(values)

    def _create_refund_move(
        self, binding, invoice, refund, refund_amount, selected_side
    ):
        commands = []
        for line in refund["lines"]:
            order_line_binding = binding.line_binding_ids.filtered(
                lambda item, line=line: item.shopify_id == line["line_id"]
            )[:1]
            sale_line = order_line_binding.odoo_id
            invoice_line = invoice.invoice_line_ids.filtered(
                lambda item, sale_line=sale_line: sale_line in item.sale_line_ids
            )[:1]
            if not invoice_line:
                continue
            subtotal = decimal_amount(
                selected_money(line["subtotal"], selected_side)["amount"]
            )
            quantity = Decimal(str(line["quantity"] or 1))
            commands.append(
                Command.create(
                    {
                        "product_id": sale_line.product_id.id,
                        "name": sale_line.name,
                        "quantity": line["quantity"] or 1,
                        "price_unit": format(subtotal / quantity, "f"),
                        "account_id": invoice_line.account_id.id,
                        "tax_ids": [Command.set(invoice_line.tax_ids.ids)],
                        "sale_line_ids": [Command.set(sale_line.ids)],
                    }
                )
            )
        shipping_amount = sum(
            decimal_amount(selected_money(item["amount"], selected_side)["amount"])
            for item in refund["shipping"]
        )
        adjustment_amount = sum(
            decimal_amount(selected_money(item["amount"], selected_side)["amount"])
            for item in refund["adjustments"]
        )
        other_amount = shipping_amount + adjustment_amount
        if other_amount:
            shipping_line = binding.line_binding_ids.filtered("is_shipping")[:1]
            invoice_line = invoice.invoice_line_ids.filtered(
                lambda item: shipping_line.odoo_id in item.sale_line_ids
            )[:1]
            account = invoice_line.account_id or invoice.invoice_line_ids[:1].account_id
            commands.append(
                Command.create(
                    {
                        "product_id": shipping_line.odoo_id.product_id.id
                        if shipping_line
                        else False,
                        "name": self.env._("Shopify shipping refund/adjustment"),
                        "quantity": 1,
                        "price_unit": format(other_amount, "f"),
                        "account_id": account.id,
                        "tax_ids": [Command.clear()],
                    }
                )
            )
        allocated = (
            sum(
                decimal_amount(
                    selected_money(line["subtotal"], selected_side)["amount"]
                )
                + decimal_amount(selected_money(line["tax"], selected_side)["amount"])
                for line in refund["lines"]
            )
            + other_amount
        )
        remainder = refund_amount - allocated
        if remainder:
            account = invoice.invoice_line_ids[:1].account_id
            commands.append(
                Command.create(
                    {
                        "name": self.env._("Shopify refund rounding/adjustment"),
                        "quantity": 1,
                        "price_unit": format(remainder, "f"),
                        "account_id": account.id,
                        "tax_ids": [Command.clear()],
                    }
                )
            )
        move = (
            self.env["account.move"]
            .with_company(binding.instance_id.company_id)
            .create(
                {
                    "move_type": "out_refund",
                    "partner_id": invoice.partner_id.id,
                    "currency_id": invoice.currency_id.id,
                    "company_id": invoice.company_id.id,
                    "invoice_origin": binding.order_name,
                    "ref": self.env._(
                        "Shopify refund %s", refund["id"].rsplit("/", 1)[-1]
                    ),
                    "reversed_entry_id": invoice.id,
                    "invoice_line_ids": commands,
                }
            )
        )
        delta = refund_amount - Decimal(str(move.amount_total))
        if delta:
            move.write(
                {
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": self.env._("Shopify tax/rounding adjustment"),
                                "quantity": 1,
                                "price_unit": format(delta, "f"),
                                "account_id": invoice.invoice_line_ids[
                                    :1
                                ].account_id.id,
                                "tax_ids": [Command.clear()],
                            }
                        )
                    ]
                }
            )
        if _exact_difference(move.amount_total, refund_amount) >= Decimal(
            str(move.currency_id.rounding)
        ) / Decimal("2"):
            raise ShopifyOrderImportError(
                self.env._(
                    "Credit-note total does not match Shopify refund %(refund)s.",
                    refund=format(refund_amount, "f"),
                )
            )
        move.action_post()
        return move

    def _adjust_uninvoiced_refund(self, binding, refund, amount):
        sale_order = binding.odoo_id
        if self._is_delivered(sale_order):
            raise ShopifyOrderImportError(
                self.env._(
                    "A refund for a delivered, uninvoiced order needs "
                    "manual resolution."
                )
            )
        expected_total = (
            decimal_amount(
                binding.presentment_money_json["total"]
                if binding.instance_id.order_currency_policy == "presentment"
                else binding.shop_money_json["total"]
            )
            if binding.shop_money_json
            else Decimal(str(sale_order.amount_total))
        )
        if (
            binding.instance_id.refund_uninvoiced_policy == "cancel"
            and amount >= expected_total
        ):
            if sale_order.state != "cancel":
                sale_order.action_cancel()
            return
        for line in refund["lines"]:
            line_binding = binding.line_binding_ids.filtered(
                lambda item, line=line: item.shopify_id == line["line_id"]
            )[:1]
            if line_binding:
                new_quantity = max(
                    line_binding.odoo_id.product_uom_qty - line["quantity"], 0
                )
                line_binding.odoo_id.product_uom_qty = new_quantity

    def _create_restock_return(self, binding, refund):
        picking = binding.odoo_id.picking_ids.filtered(
            lambda item: (
                item.state == "done" and item.picking_type_id.code == "outgoing"
            )
        )[:1]
        if not picking:
            return
        commands = []
        for line in refund["lines"]:
            if line["restock_type"] in ("", "NO_RESTOCK"):
                continue
            order_line = binding.line_binding_ids.filtered(
                lambda item, line=line: item.shopify_id == line["line_id"]
            )[:1].odoo_id
            move = picking.move_ids.filtered(
                lambda item, order_line=order_line: item.sale_line_id == order_line
            )[:1]
            if move:
                commands.append(
                    Command.create(
                        {
                            "move_id": move.id,
                            "quantity": line["quantity"],
                        }
                    )
                )
        if not commands:
            return
        wizard = (
            self.env["stock.return.picking"]
            .with_context(
                active_id=picking.id,
                active_model="stock.picking",
            )
            .create(
                {
                    "picking_id": picking.id,
                    "product_return_moves": commands,
                }
            )
        )
        wizard.action_create_returns()

    def _write_success(self, binding, sale_order, order_data, digest):
        currencies = {}
        for side in ("shop", "presentment"):
            code = order_data["total"][side]["currency"]
            currencies[side] = (
                self.env["res.currency"]
                .with_context(active_test=False)
                .search([("name", "=", code)], limit=1)
            )
        shop_values = {
            "subtotal": order_data["subtotal"]["shop"]["amount"],
            "discount_total": order_data["discount_total"]["shop"]["amount"],
            "shipping_total": order_data["shipping_total"]["shop"]["amount"],
            "tax_total": order_data["tax_total"]["shop"]["amount"],
            "total": order_data["total"]["shop"]["amount"],
        }
        presentment_values = {
            "subtotal": order_data["subtotal"]["presentment"]["amount"],
            "discount_total": order_data["discount_total"]["presentment"]["amount"],
            "shipping_total": order_data["shipping_total"]["presentment"]["amount"],
            "tax_total": order_data["tax_total"]["presentment"]["amount"],
            "total": order_data["total"]["presentment"]["amount"],
        }
        binding.write(
            {
                "odoo_id": sale_order.id,
                "order_name": order_data["name"],
                "order_number": order_data["number"],
                "financial_status": order_data["financial_status"],
                "fulfillment_status": order_data["fulfillment_status"],
                "source": order_data["source"],
                "source_name": order_data["source_name"],
                "source_identifier": order_data["source_identifier"],
                "is_draft": order_data["is_draft"],
                "draft_status": order_data["draft_status"],
                "completed_order_shopify_id": order_data["completed_order_id"],
                "risk_level": order_data["risk_level"],
                "shop_currency_id": currencies["shop"].id,
                "presentment_currency_id": currencies["presentment"].id,
                "order_currency_id": sale_order.currency_id.id,
                "shop_subtotal": shop_values["subtotal"],
                "shop_discount_total": shop_values["discount_total"],
                "shop_shipping_total": shop_values["shipping_total"],
                "shop_tax_total": shop_values["tax_total"],
                "shop_total": shop_values["total"],
                "presentment_subtotal": presentment_values["subtotal"],
                "presentment_discount_total": presentment_values["discount_total"],
                "presentment_shipping_total": presentment_values["shipping_total"],
                "presentment_tax_total": presentment_values["tax_total"],
                "presentment_total": presentment_values["total"],
                "shop_money_json": shop_values,
                "presentment_money_json": presentment_values,
                "discount_codes": ", ".join(order_data["discount_codes"]),
                "raw_payload": order_data["raw"],
                "payload_digest": digest,
                "created_at": _utc_datetime(order_data["created_at"]),
                "cancelled_at": _utc_datetime(order_data["cancelled_at"]),
                "external_updated_at": _utc_datetime(order_data["updated_at"]),
                "last_sync_date": fields.Datetime.now(),
                "state": "synced",
                "error_message": False,
                "missing_tax_rate": False,
                "missing_tax_country_id": False,
                "missing_tax_included": False,
            }
        )


class ShopifyWebhookOrderSync(models.Model):
    _inherit = "shopify.webhook.event"

    def _queue_order_import(self):
        self.ensure_one()
        order_id = shopify_gid(
            "Order",
            self.payload.get("admin_graphql_api_id") or self.payload.get("id"),
        )
        if not order_id:
            raise ShopifyOrderImportError(
                self.env._("Order webhook contains no order ID.")
            )
        self.env["shopify.order"].with_delay(
            description=self.env._("Import webhook order %s", order_id),
            identity_key=(
                f"shopify.order.webhook.{self.instance_id.id}.{order_id}."
                f"{self.webhook_id}"
            ),
        )._job_import_order_from_api(self.instance_id.id, order_id, self.payload)

    def _handle_orders_create(self):
        self._queue_order_import()

    def _handle_orders_updated(self):
        self._queue_order_import()

    def _handle_orders_cancelled(self):
        self._queue_order_import()

    def _handle_refunds_create(self):
        self.ensure_one()
        order_id, _refund = normalize_refund_payload(self.payload)
        self.env["shopify.order"].with_delay(
            description=self.env._("Import Shopify refund for %s", order_id),
            identity_key=(
                f"shopify.refund.webhook.{self.instance_id.id}.{self.webhook_id}"
            ),
        )._job_import_order_from_api(self.instance_id.id, order_id)

    def _handle_draft_orders_create(self):
        self._queue_draft_import()

    def _handle_draft_orders_update(self):
        self._queue_draft_import()

    def _queue_draft_import(self):
        self.ensure_one()
        draft_id = shopify_gid(
            "DraftOrder",
            self.payload.get("admin_graphql_api_id") or self.payload.get("id"),
        )
        if not draft_id:
            raise ShopifyOrderImportError(
                self.env._("Draft-order webhook contains no order ID.")
            )
        self.env["shopify.order"].with_delay(
            description=self.env._("Import Shopify draft order %s", draft_id),
            identity_key=(
                f"shopify.draft.webhook.{self.instance_id.id}.{draft_id}."
                f"{self.webhook_id}"
            ),
        )._job_import_draft_from_api(self.instance_id.id, draft_id)


WEBHOOK_HANDLERS.update(
    {
        "orders/create": "_handle_orders_create",
        "orders/updated": "_handle_orders_updated",
        "orders/cancelled": "_handle_orders_cancelled",
        "refunds/create": "_handle_refunds_create",
        "draft_orders/create": "_handle_draft_orders_create",
        "draft_orders/update": "_handle_draft_orders_update",
    }
)
