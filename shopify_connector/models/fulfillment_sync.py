from __future__ import annotations

# pylint: disable=consider-merging-classes-inherited
from collections import defaultdict
from datetime import datetime, timezone

from odoo import fields, models
from odoo.exceptions import UserError
from odoo.fields import Command

from ..graphql.fulfillment import (
    FULFILLMENT_BY_ID_QUERY,
    FULFILLMENT_CANCEL_MUTATION,
    FULFILLMENT_CREATE_MUTATION,
    FULFILLMENT_ORDER_MOVE_MUTATION,
    FULFILLMENT_ORDER_RELEASE_HOLD_MUTATION,
    ORDER_FULFILLMENT_ORDERS_QUERY,
)
from ..lib.client import ShopifyError
from ..lib.fulfillment import (
    FulfillmentAllocationError,
    allocate_fulfillment_lines,
    build_tracking_payload,
)
from ..lib.order import shopify_gid
from .webhook_event import WEBHOOK_HANDLERS


class ShopifyFulfillmentError(UserError):
    """An actionable fulfillment mapping or Shopify API error."""


def _nodes(value):
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        if isinstance(value.get("nodes"), list):
            return _nodes(value["nodes"])
        if isinstance(value.get("edges"), list):
            return _nodes(
                [edge.get("node") for edge in value["edges"] if isinstance(edge, dict)]
            )
    return []


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


def _tracking(payload):
    tracking = payload.get("trackingInfo") or {}
    if isinstance(tracking, list):
        return tracking[0] if tracking else {}
    return tracking if isinstance(tracking, dict) else {}


class ShopifyOrderFulfillmentSync(models.Model):
    _inherit = "shopify.order"

    def _write_success(self, binding, sale_order, order_data, digest):
        result = super()._write_success(binding, sale_order, order_data, digest)
        if not binding.is_draft:
            binding.with_delay(
                description=self.env._(
                    "Import fulfillment orders for %s", binding.order_name
                ),
                identity_key=(
                    f"shopify.fulfillment.orders.refresh."
                    f"{binding.instance_id.id}.{binding.shopify_id}"
                ),
            )._job_refresh_fulfillment_orders()
        return result

    def action_refresh_fulfillment_orders(self):
        for binding in self.filtered(lambda item: not item.is_draft):
            binding.with_delay(
                description=self.env._(
                    "Refresh fulfillment orders for %s", binding.order_name
                ),
                identity_key=(
                    f"shopify.fulfillment.orders.refresh."
                    f"{binding.instance_id.id}.{binding.shopify_id}"
                ),
            )._job_refresh_fulfillment_orders()
        return True

    def _job_refresh_fulfillment_orders(self):
        self = self.sudo()
        self.ensure_one()
        if not self.instance_id.active or self.is_draft:
            return []
        data = self.instance_id._shopify_client().execute(
            ORDER_FULFILLMENT_ORDERS_QUERY,
            {"id": self.shopify_id},
        )
        order = data.get("order")
        if not order:
            raise ShopifyFulfillmentError(
                self.env._("Shopify order %s was not found.", self.shopify_id)
            )
        imported = self.env["shopify.fulfillment.order"]
        seen = set()
        for payload in _nodes(order.get("fulfillmentOrders")):
            binding = self._upsert_fulfillment_order(payload)
            imported |= binding
            seen.add(binding.shopify_id)
        stale = self.fulfillment_order_ids.filtered(
            lambda item: item.shopify_id not in seen
        )
        stale.write(
            {
                "fulfillment_status": "CLOSED",
                "is_held": False,
                "line_ids": [Command.clear()],
                "last_sync_date": fields.Datetime.now(),
            }
        )
        self.instance_id._write_log(
            entity="fulfillment_order",
            direction="import",
            level="info",
            message=self.env._(
                "Refreshed %s Shopify fulfillment order(s).", len(imported)
            ),
            record=self,
        )
        return imported.ids

    def _upsert_fulfillment_order(self, payload):
        fulfillment_order_id = str(payload.get("id") or "")
        if not fulfillment_order_id:
            raise ShopifyFulfillmentError(
                self.env._("Shopify returned a fulfillment order without an ID.")
            )
        assigned = payload.get("assignedLocation") or {}
        location = assigned.get("location") or {}
        location_id = str(location.get("id") or "")
        location_binding = self.env["shopify.location"].search(
            [
                ("instance_id", "=", self.instance_id.id),
                ("shopify_id", "=", location_id),
            ],
            limit=1,
        )
        holds = [
            {
                "id": str(hold.get("id") or ""),
                "reason": str(hold.get("reason") or ""),
                "notes": str(hold.get("reasonNotes") or ""),
                "ours": bool(hold.get("heldByRequestingApp")),
            }
            for hold in (payload.get("fulfillmentHolds") or [])
            if isinstance(hold, dict)
        ]
        actions = [
            str(item.get("action") or "").upper()
            for item in (payload.get("supportedActions") or [])
            if isinstance(item, dict) and item.get("action")
        ]
        values = {
            "instance_id": self.instance_id.id,
            "shopify_id": fulfillment_order_id,
            "order_binding_id": self.id,
            "assigned_location_id": location_binding.id,
            "assigned_location_shopify_id": location_id,
            "assigned_location_name": str(location.get("name") or ""),
            "fulfillment_status": str(payload.get("status") or "").upper(),
            "request_status": str(payload.get("requestStatus") or "").upper(),
            "supported_actions": actions,
            "fulfillment_holds": holds,
            "is_held": bool(holds)
            or str(payload.get("status") or "").upper() == "ON_HOLD",
            "last_sync_date": fields.Datetime.now(),
            "state": "synced",
            "error_message": False,
        }
        binding = self.env["shopify.fulfillment.order"].search(
            [
                ("instance_id", "=", self.instance_id.id),
                ("shopify_id", "=", fulfillment_order_id),
            ],
            limit=1,
        )
        if binding:
            binding.write(values)
        else:
            binding = self.env["shopify.fulfillment.order"].create(values)
        seen_lines = set()
        for line in _nodes(payload.get("lineItems")):
            line_id = str(line.get("id") or "")
            order_line_id = str((line.get("lineItem") or {}).get("id") or "")
            if not line_id:
                continue
            seen_lines.add(line_id)
            order_line_binding = self.line_binding_ids.filtered(
                lambda item, order_line_id=order_line_id: (
                    item.shopify_id == order_line_id
                )
            )[:1]
            line_values = {
                "fulfillment_order_id": binding.id,
                "shopify_id": line_id,
                "order_line_binding_id": order_line_binding.id,
                "order_line_shopify_id": order_line_id,
                "total_quantity": int(line.get("totalQuantity") or 0),
                "remaining_quantity": int(line.get("remainingQuantity") or 0),
            }
            existing = binding.line_ids.filtered(
                lambda item, line_id=line_id: item.shopify_id == line_id
            )[:1]
            if existing:
                existing.write(line_values)
            else:
                self.env["shopify.fulfillment.order.line"].create(line_values)
        binding.line_ids.filtered(
            lambda item: item.shopify_id not in seen_lines
        ).unlink()
        return binding

    def _fulfillment_allocation_input(self, picking):
        moves = []
        for move in picking.move_ids.filtered(
            lambda item: item.state == "done" and item.sale_line_id
        ):
            quantity = getattr(move, "quantity", 0)
            if not quantity:
                quantity = sum(
                    getattr(line, "quantity", 0) for line in move.move_line_ids
                )
            if quantity <= 0:
                continue
            line_binding = self.line_binding_ids.filtered(
                lambda item, move=move: item.odoo_id == move.sale_line_id
            )[:1]
            if not line_binding:
                raise ShopifyFulfillmentError(
                    self.env._(
                        "Delivery move %(move)s has no Shopify order-line binding.",
                        move=move.display_name,
                    )
                )
            variant_binding = self.env["shopify.product.variant"].search(
                [
                    ("instance_id", "=", self.instance_id.id),
                    ("odoo_id", "=", move.product_id.id),
                    ("state", "=", "synced"),
                ],
                limit=1,
            )
            if not variant_binding or (
                line_binding.variant_shopify_id
                and variant_binding.shopify_id != line_binding.variant_shopify_id
            ):
                raise ShopifyFulfillmentError(
                    self.env._(
                        "Delivery move %s has no matching Shopify variant binding.",
                        move.display_name,
                    )
                )
            moves.append(
                {
                    "move_id": move.id,
                    "name": move.display_name,
                    "line_id": line_binding.shopify_id,
                    "variant_id": variant_binding.shopify_id,
                    "quantity": quantity,
                }
            )
        return moves

    def _fulfillment_orders_input(self):
        return [
            {
                "id": fulfillment_order.shopify_id,
                "location_id": (fulfillment_order.assigned_location_shopify_id),
                "status": fulfillment_order.fulfillment_status,
                "held": fulfillment_order.is_held,
                "supported_actions": fulfillment_order.supported_actions or [],
                "line_items": [
                    {
                        "id": line.shopify_id,
                        "line_id": line.order_line_shopify_id,
                        "remaining_quantity": line.remaining_quantity,
                    }
                    for line in fulfillment_order.line_ids
                ],
            }
            for fulfillment_order in self.fulfillment_order_ids
        ]

    def _mapped_source_location(self, picking):
        candidates = self.env["shopify.location"].search(
            [
                ("instance_id", "=", self.instance_id.id),
                ("active", "=", True),
                ("odoo_location_id", "parent_of", picking.location_id.id),
            ]
        )
        if not candidates:
            raise ShopifyFulfillmentError(
                self.env._(
                    "Delivery source location %(location)s is not mapped to a "
                    "Shopify location for %(instance)s.",
                    location=picking.location_id.display_name,
                    instance=self.instance_id.name,
                )
            )
        return max(
            candidates,
            key=lambda item: len(item.odoo_location_id.parent_path or ""),
        )

    def _tracking_info(self, picking):
        carrier = picking.carrier_id
        mapping = (
            self.env["shopify.carrier.mapping"].search(
                [
                    ("instance_id", "=", self.instance_id.id),
                    ("carrier_id", "=", carrier.id),
                ],
                limit=1,
            )
            if carrier
            else self.env["shopify.carrier.mapping"]
        )
        company = mapping.tracking_company or (carrier.name if carrier else "")
        url = getattr(picking, "carrier_tracking_url", False)
        if not url and carrier and hasattr(carrier, "get_tracking_link"):
            try:
                url = carrier.get_tracking_link(picking)
            except (NotImplementedError, UserError):
                url = False
        return build_tracking_payload(
            picking.carrier_tracking_ref,
            company,
            url,
        )

    def _job_push_picking_fulfillment(self, picking_id):  # noqa: C901
        self = self.sudo()
        self.ensure_one()
        if not self.instance_id.active:
            return False
        picking = self.env["stock.picking"].browse(picking_id).exists()
        if (
            not picking
            or picking.state != "done"
            or picking.picking_type_id.code != "outgoing"
        ):
            return False
        if picking.company_id != self.company_id:
            raise ShopifyFulfillmentError(
                self.env._(
                    "The delivery and Shopify order must belong to the same company."
                )
            )
        idempotency_key = f"picking:{picking.id}"
        self.env.cr.execute(
            "SELECT pg_advisory_xact_lock(%s, hashtext(%s))",
            (self.instance_id.id, idempotency_key),
        )
        existing = self.env["shopify.fulfillment"].search(
            [
                ("instance_id", "=", self.instance_id.id),
                ("idempotency_key", "=", idempotency_key),
            ],
            limit=1,
        )
        if existing:
            if existing.shopify_id:
                return existing.id
            raise ShopifyFulfillmentError(
                self.env._(
                    "A previous Shopify fulfillment attempt exists for %(picking)s "
                    "without a confirmed Shopify ID. Resolve binding %(binding)s "
                    "before retrying to avoid a duplicate fulfillment.",
                    picking=picking.name,
                    binding=existing.display_name,
                )
            )

        self._job_refresh_fulfillment_orders()
        location = self._mapped_source_location(picking)
        moves = self._fulfillment_allocation_input(picking)
        if not moves:
            self.instance_id._write_log(
                entity="fulfillment",
                direction="export",
                level="info",
                message=self.env._(
                    "Delivery %s has no Shopify-bound delivered moves.", picking.name
                ),
                record=picking,
            )
            return False
        held_line_ids = {
            line.order_line_shopify_id
            for fulfillment_order in self.fulfillment_order_ids.filtered("is_held")
            for line in fulfillment_order.line_ids
            if line.remaining_quantity
        }
        delivered_line_ids = {move["line_id"] for move in moves}
        try:
            allocation = allocate_fulfillment_lines(
                moves,
                self._fulfillment_orders_input(),
                target_location_id=location.shopify_id,
            )
        except FulfillmentAllocationError as exc:
            if held_line_ids.intersection(delivered_line_ids):
                raise ShopifyFulfillmentError(
                    self.env._(
                        "Shopify has a fulfillment hold on one or more "
                        "unallocated delivered items. Release the hold before "
                        "pushing %(picking)s.",
                        picking=picking.name,
                    )
                ) from exc
            raise ShopifyFulfillmentError(str(exc)) from exc
        if allocation["warnings"] and held_line_ids.intersection(delivered_line_ids):
            raise ShopifyFulfillmentError(
                self.env._(
                    "Shopify has a fulfillment hold on delivered quantities "
                    "that could not be allocated. Release the hold before "
                    "pushing %(picking)s.",
                    picking=picking.name,
                )
            )

        if allocation["move_fulfillment_order_ids"]:
            client = self.instance_id._shopify_client()
            for fulfillment_order_id in allocation["move_fulfillment_order_ids"]:
                client.execute(
                    FULFILLMENT_ORDER_MOVE_MUTATION,
                    {
                        "id": fulfillment_order_id,
                        "newLocationId": location.shopify_id,
                    },
                )
            self._job_refresh_fulfillment_orders()
            try:
                allocation = allocate_fulfillment_lines(
                    moves,
                    self._fulfillment_orders_input(),
                    target_location_id=location.shopify_id,
                )
            except FulfillmentAllocationError as exc:
                if held_line_ids.intersection(delivered_line_ids):
                    raise ShopifyFulfillmentError(
                        self.env._(
                            "Shopify has a fulfillment hold on one or more "
                            "unallocated delivered items. Release the hold "
                            "before pushing %(picking)s.",
                            picking=picking.name,
                        )
                    ) from exc
                raise ShopifyFulfillmentError(str(exc)) from exc
            if allocation["warnings"] and held_line_ids.intersection(
                delivered_line_ids
            ):
                raise ShopifyFulfillmentError(
                    self.env._(
                        "Shopify has a fulfillment hold on delivered "
                        "quantities that could not be allocated. Release the "
                        "hold before pushing %(picking)s.",
                        picking=picking.name,
                    )
                )
            if allocation["move_fulfillment_order_ids"]:
                raise ShopifyFulfillmentError(
                    self.env._(
                        "Shopify did not reassign the fulfillment order to "
                        "location %s.",
                        location.name,
                    )
                )
        groups = allocation["groups"]
        if not groups:
            return False
        fulfillment_orders = self.fulfillment_order_ids.filtered(
            lambda item: (
                item.shopify_id in {group["fulfillment_order_id"] for group in groups}
            )
        )
        binding = self.env["shopify.fulfillment"].create(
            {
                "instance_id": self.instance_id.id,
                "order_binding_id": self.id,
                "fulfillment_order_ids": [Command.set(fulfillment_orders.ids)],
                "picking_id": picking.id,
                "idempotency_key": idempotency_key,
                "origin": "odoo",
                "location_shopify_id": location.shopify_id,
                "state": "pending",
            }
        )
        fulfillment_input = {
            "lineItemsByFulfillmentOrder": [
                {
                    "fulfillmentOrderId": group["fulfillment_order_id"],
                    "fulfillmentOrderLineItems": group["line_items"],
                }
                for group in groups
            ],
            "notifyCustomer": bool(self.instance_id.fulfillment_notify_customer),
        }
        tracking = self._tracking_info(picking)
        if tracking:
            fulfillment_input["trackingInfo"] = tracking
        try:
            data = self.instance_id._shopify_client().execute(
                FULFILLMENT_CREATE_MUTATION,
                {"fulfillment": fulfillment_input},
            )
            payload = (data.get("fulfillmentCreate") or {}).get("fulfillment") or {}
            if not payload.get("id"):
                raise ShopifyFulfillmentError(
                    self.env._("Shopify did not return the created fulfillment ID.")
                )
        except (ShopifyError, ShopifyFulfillmentError) as exc:
            binding.write({"state": "error", "error_message": str(exc)})
            self.instance_id._write_log(
                entity="fulfillment",
                direction="export",
                level="error",
                message=self.env._(
                    "Failed to fulfill %(picking)s: %(error)s",
                    picking=picking.name,
                    error=exc,
                ),
                record=binding,
            )
            return False
        tracking_payload = _tracking(payload) or tracking
        binding.write(
            {
                "shopify_id": payload["id"],
                "fulfillment_status": str(payload.get("status") or "").upper(),
                "tracking_company": tracking_payload.get("company"),
                "tracking_number": tracking_payload.get("number"),
                "tracking_url": tracking_payload.get("url"),
                "raw_payload": payload,
                "external_updated_at": _utc_datetime(payload.get("updatedAt")),
                "last_sync_date": fields.Datetime.now(),
                "state": "synced",
                "error_message": False,
            }
        )
        for warning in allocation["warnings"]:
            self.instance_id._write_log(
                entity="fulfillment",
                direction="export",
                level="error",
                message=warning,
                record=binding,
            )
        self.instance_id._write_log(
            entity="fulfillment",
            direction="export",
            level="info",
            message=self.env._(
                "Created Shopify fulfillment %(fulfillment)s for delivery "
                "%(delivery)s.",
                fulfillment=binding.shopify_id,
                delivery=picking.name,
            ),
            record=binding,
        )
        try:
            self._job_refresh_fulfillment_orders()
        except ShopifyError as exc:
            self.instance_id._write_log(
                entity="fulfillment_order",
                direction="import",
                level="warning",
                message=self.env._(
                    "Fulfillment was created, but the follow-up fulfillment "
                    "order refresh failed: %s",
                    exc,
                ),
                record=binding,
            )
        return binding.id


class ShopifyFulfillmentOrderActions(models.Model):
    _inherit = "shopify.fulfillment.order"

    def _job_release_hold(self):
        self = self.sudo()
        self.ensure_one()
        if not self.instance_id.active:
            return False
        hold_ids = [
            hold["id"] for hold in (self.fulfillment_holds or []) if hold.get("id")
        ]
        self.instance_id._shopify_client().execute(
            FULFILLMENT_ORDER_RELEASE_HOLD_MUTATION,
            {"id": self.shopify_id, "holdIds": hold_ids or None},
        )
        try:
            self.order_binding_id._job_refresh_fulfillment_orders()
        except ShopifyError as exc:
            self.instance_id._write_log(
                entity="fulfillment_order",
                direction="import",
                level="warning",
                message=self.env._("Hold released; refresh failed: %s", exc),
                record=self,
            )
        self.instance_id._write_log(
            entity="fulfillment_order",
            direction="export",
            level="info",
            message=self.env._(
                "Released Shopify fulfillment hold %s.", self.shopify_id
            ),
            record=self,
        )
        return True


class ShopifyFulfillmentActions(models.Model):
    _inherit = "shopify.fulfillment"

    def _job_cancel_shopify(self):
        self = self.sudo()
        self.ensure_one()
        if not self.instance_id.active:
            return False
        if not self.shopify_id:
            raise ShopifyFulfillmentError(
                self.env._("This fulfillment has no Shopify ID to cancel.")
            )
        data = self.instance_id._shopify_client().execute(
            FULFILLMENT_CANCEL_MUTATION,
            {"id": self.shopify_id},
        )
        payload = (data.get("fulfillmentCancel") or {}).get("fulfillment") or {}
        self.write(
            {
                "fulfillment_status": str(payload.get("status") or "CANCELLED").upper(),
                "raw_payload": payload or self.raw_payload,
                "last_sync_date": fields.Datetime.now(),
                "state": "synced",
                "error_message": False,
            }
        )
        try:
            self.order_binding_id._job_refresh_fulfillment_orders()
        except ShopifyError as exc:
            self.instance_id._write_log(
                entity="fulfillment_order",
                direction="import",
                level="warning",
                message=self.env._("Fulfillment cancelled; refresh failed: %s", exc),
                record=self,
            )
        self.instance_id._write_log(
            entity="fulfillment",
            direction="export",
            level="warning",
            message=self.env._(
                "Manually cancelled Shopify fulfillment %s.", self.shopify_id
            ),
            record=self,
        )
        return True


class StockPickingShopifyFulfillmentSync(models.Model):
    _inherit = "stock.picking"

    def _action_done(self, *args, **kwargs):
        result = super()._action_done(*args, **kwargs)
        if self.env.context.get("skip_shopify_fulfillment_push"):
            return result
        completed = result if getattr(result, "_name", "") == self._name else self
        for picking in completed.filtered(
            lambda item: (
                item.state == "done" and item.picking_type_id.code == "outgoing"
            )
        ):
            bindings = picking.sale_id.shopify_binding_ids.filtered(
                lambda item: not item.is_draft and item.state == "synced"
            )
            for binding in bindings:
                binding.with_delay(
                    description=self.env._(
                        "Push Shopify fulfillment for %s", picking.name
                    ),
                    identity_key=(
                        f"shopify.fulfillment.push."
                        f"{binding.instance_id.id}.{binding.id}.{picking.id}"
                    ),
                )._job_push_picking_fulfillment(picking.id)
        return result

    def action_cancel(self):
        result = super().action_cancel()
        for picking in self:
            for fulfillment in picking.shopify_fulfillment_ids.filtered("shopify_id"):
                base_url = (
                    self.env["ir.config_parameter"].sudo().get_param("web.base.url")
                )
                link = (
                    f"{(base_url or '').rstrip('/')}/web#id={fulfillment.id}"
                    "&model=shopify.fulfillment&view_type=form"
                )
                fulfillment.instance_id._write_log(
                    entity="fulfillment",
                    direction="export",
                    level="warning",
                    message=self.env._(
                        "Odoo delivery %(picking)s was cancelled after Shopify "
                        "fulfillment %(fulfillment)s was created. Shopify was "
                        "not cancelled automatically. Review and use the manual "
                        "Cancel in Shopify action: %(link)s",
                        picking=picking.name,
                        fulfillment=fulfillment.shopify_id,
                        link=link,
                    ),
                    record=fulfillment,
                )
        return result


class ShopifyWebhookFulfillmentSync(models.Model):
    _inherit = "shopify.webhook.event"

    def _queue_fulfillment_import(self):
        self.ensure_one()
        fulfillment_id = shopify_gid(
            "Fulfillment",
            self.payload.get("admin_graphql_api_id") or self.payload.get("id"),
        )
        if not fulfillment_id:
            raise ShopifyFulfillmentError(
                self.env._("Fulfillment webhook contains no fulfillment ID.")
            )
        self.env["shopify.fulfillment"].with_delay(
            description=self.env._("Import Shopify fulfillment %s", fulfillment_id),
            identity_key=(
                f"shopify.fulfillment.webhook.{self.instance_id.id}.{self.webhook_id}"
            ),
        )._job_import_from_shopify(
            self.instance_id.id,
            fulfillment_id,
            self.payload,
        )

    def _handle_fulfillments_create(self):
        self._queue_fulfillment_import()

    def _handle_fulfillments_update(self):
        self._queue_fulfillment_import()


class ShopifyExternalFulfillmentImport(models.Model):
    _inherit = "shopify.fulfillment"

    def _job_import_from_shopify(
        self, instance_id, fulfillment_id, webhook_payload=None
    ):
        self = self.sudo()
        instance = self.env["shopify.instance"].browse(instance_id).exists()
        if not instance or not instance.active:
            return False
        webhook_payload = webhook_payload or {}
        try:
            data = instance._shopify_client().execute(
                FULFILLMENT_BY_ID_QUERY,
                {"id": fulfillment_id},
            )
            payload = data.get("fulfillment") or {}
        except ShopifyError:
            payload = {}
        if not payload:
            payload = dict(webhook_payload)
            payload["id"] = fulfillment_id
        order_id = shopify_gid(
            "Order",
            (payload.get("order") or {}).get("id") or webhook_payload.get("order_id"),
        )
        order_binding = self.env["shopify.order"].search(
            [
                ("instance_id", "=", instance.id),
                ("shopify_id", "=", order_id),
            ],
            limit=1,
        )
        if not order_binding:
            raise ShopifyFulfillmentError(
                self.env._(
                    "No synchronized Odoo order matches Shopify order %s.", order_id
                )
            )
        binding = self.search(
            [
                ("instance_id", "=", instance.id),
                ("shopify_id", "=", fulfillment_id),
            ],
            limit=1,
        )
        tracking = _tracking(payload)
        values = {
            "instance_id": instance.id,
            "shopify_id": fulfillment_id,
            "order_binding_id": order_binding.id,
            "fulfillment_status": str(
                payload.get("status") or webhook_payload.get("status") or ""
            ).upper(),
            "location_shopify_id": shopify_gid(
                "Location",
                (payload.get("location") or {}).get("id")
                or webhook_payload.get("location_id"),
            ),
            "tracking_company": (
                tracking.get("company") or webhook_payload.get("tracking_company")
            ),
            "tracking_number": (
                tracking.get("number") or webhook_payload.get("tracking_number")
            ),
            "tracking_url": (
                tracking.get("url") or webhook_payload.get("tracking_url")
            ),
            "raw_payload": payload,
            "external_updated_at": _utc_datetime(payload.get("updatedAt")),
            "last_sync_date": fields.Datetime.now(),
            "state": "synced",
            "error_message": False,
        }
        echo = bool(binding and binding.origin == "odoo")
        if binding:
            binding.write(values)
        else:
            values["origin"] = "shopify"
            binding = self.create(values)
        fulfillment_order_ids = {
            str(item.get("id") or "")
            for item in _nodes(payload.get("fulfillmentOrders"))
            if item.get("id")
        }
        fulfillment_order_ids.update(
            {
                shopify_gid(
                    "FulfillmentOrder",
                    line.get("fulfillment_order_id"),
                )
                for line in (webhook_payload.get("line_items") or [])
                if line.get("fulfillment_order_id")
            }
        )
        if fulfillment_order_ids:
            fulfillment_orders = self.env["shopify.fulfillment.order"].search(
                [
                    ("instance_id", "=", instance.id),
                    ("shopify_id", "in", list(fulfillment_order_ids)),
                ]
            )
            binding.fulfillment_order_ids = [Command.set(fulfillment_orders.ids)]
        if echo:
            instance._write_log(
                entity="fulfillment",
                direction="import",
                level="info",
                message=self.env._(
                    "Ignored connector fulfillment webhook echo %s.", fulfillment_id
                ),
                record=binding,
            )
            return binding.id
        instance._write_log(
            entity="fulfillment",
            direction="import",
            level="info",
            message=self.env._(
                "Imported external Shopify fulfillment %s.", fulfillment_id
            ),
            record=binding,
        )
        if instance.fulfillment_auto_validate_webhook:
            binding._auto_validate_external(payload, webhook_payload)
        else:
            instance._write_log(
                entity="fulfillment",
                direction="import",
                level="info",
                message=self.env._(
                    "External fulfillment is log-only; Odoo delivery was not validated."
                ),
                record=binding,
            )
        return binding.id

    def _auto_validate_external(self, payload, webhook_payload):
        self.ensure_one()
        if self.fulfillment_status != "SUCCESS":
            return False
        quantities = defaultdict(int)
        for line in _nodes(payload.get("fulfillmentLineItems")):
            line_id = str((line.get("lineItem") or {}).get("id") or "")
            if line_id:
                quantities[line_id] += int(line.get("quantity") or 0)
        if not quantities:
            for line in webhook_payload.get("line_items") or []:
                line_id = shopify_gid("LineItem", line.get("id"))
                if line_id:
                    quantities[line_id] += int(line.get("quantity") or 0)
        if not quantities:
            self.instance_id._write_log(
                entity="fulfillment",
                direction="import",
                level="warning",
                message=self.env._(
                    "External fulfillment had no line quantities; Odoo "
                    "delivery was not validated."
                ),
                record=self,
            )
            return False
        pickings = self.order_binding_id.odoo_id.picking_ids.filtered(
            lambda item: (
                item.state not in ("done", "cancel")
                and item.picking_type_id.code == "outgoing"
            )
        )
        location = self.env["shopify.location"].search(
            [
                ("instance_id", "=", self.instance_id.id),
                ("shopify_id", "=", self.location_shopify_id),
            ],
            limit=1,
        )
        if location:
            at_location = pickings.filtered(
                lambda item: (
                    location.odoo_location_id
                    and location.odoo_location_id.parent_path
                    in item.location_id.parent_path
                )
            )
            pickings = at_location or pickings
        picking = pickings[:1]
        if not picking or picking.shopify_risk_hold:
            self.instance_id._write_log(
                entity="fulfillment",
                direction="import",
                level="warning",
                message=self.env._(
                    "No eligible Odoo delivery could be validated for external "
                    "fulfillment %s.",
                    self.shopify_id,
                ),
                record=self,
            )
            return False
        picking.action_assign()
        changed = False
        partial = False
        for line_id, quantity in quantities.items():
            line_binding = self.order_binding_id.line_binding_ids.filtered(
                lambda item, line_id=line_id: item.shopify_id == line_id
            )[:1]
            move = picking.move_ids.filtered(
                lambda item, line_binding=line_binding: (
                    item.sale_line_id == line_binding.odoo_id
                )
            )[:1]
            if not move:
                continue
            done_quantity = min(quantity, int(move.product_uom_qty))
            move.quantity = done_quantity
            partial |= done_quantity < move.product_uom_qty
            changed = True
        if not changed:
            return False
        picking = picking.with_context(skip_shopify_fulfillment_push=True)
        if partial:
            picking._action_done()
        else:
            picking.button_validate()
        if picking.state == "done":
            self.picking_id = picking
            return True
        self.instance_id._write_log(
            entity="fulfillment",
            direction="import",
            level="warning",
            message=self.env._(
                "Odoo delivery %s still requires manual validation.", picking.name
            ),
            record=self,
        )
        return False


WEBHOOK_HANDLERS.update(
    {
        "fulfillments/create": "_handle_fulfillments_create",
        "fulfillments/update": "_handle_fulfillments_update",
    }
)
