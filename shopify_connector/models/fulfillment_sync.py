from __future__ import annotations

# pylint: disable=consider-merging-classes-inherited
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from odoo import fields, models
from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.tools import float_compare, float_is_zero, float_round

from odoo.addons.queue_job.exception import RetryableJobError

from ..graphql.fulfillment import (
    FULFILLMENT_BY_ID_QUERY,
    FULFILLMENT_CANCEL_MUTATION,
    FULFILLMENT_CREATE_MUTATION,
    FULFILLMENT_ORDER_MOVE_MUTATION,
    FULFILLMENT_ORDER_RELEASE_HOLD_MUTATION,
    ORDER_FULFILLMENT_ORDERS_QUERY,
    ORDER_FULFILLMENTS_QUERY,
)
from ..lib.client import ShopifyError
from ..lib.fulfillment import (
    FulfillmentAllocationError,
    allocate_fulfillment_lines,
    build_tracking_payload,
)
from ..lib.order import shopify_gid
from .webhook_event import WEBHOOK_HANDLERS

# Delivery steps are validated one at a time, because Odoo creates each step
# when the previous one is done. Stop after this many in case a route loops back.
MAX_DELIVERY_STEPS = 10

# Shopify and Odoo clocks may drift; a fulfillment created by an unconfirmed
# push can carry a Shopify timestamp slightly before the Odoo attempt record.
UNCONFIRMED_PUSH_CLOCK_SKEW = timedelta(minutes=5)
FAILED_FULFILLMENT_STATUSES = ("CANCELLED", "ERROR", "FAILURE")


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
        self._queue_missing_fulfillments(order)
        return imported.ids

    def _queue_missing_fulfillments(self, order):
        fulfillment_ids = [
            str(item["id"])
            for item in _nodes(order.get("fulfillments"))
            if item.get("id")
        ]
        known = set(
            self.env["shopify.fulfillment"]
            .search(
                [
                    ("instance_id", "=", self.instance_id.id),
                    ("shopify_id", "in", fulfillment_ids),
                ]
            )
            .mapped("shopify_id")
        )
        for fulfillment_id in fulfillment_ids:
            if fulfillment_id in known:
                continue
            self.env["shopify.fulfillment"].with_delay(
                description=self.env._("Import Shopify fulfillment %s", fulfillment_id),
                identity_key=(
                    f"shopify.fulfillment.import.{self.instance_id.id}.{fulfillment_id}"
                ),
            )._job_import_from_shopify(self.instance_id.id, fulfillment_id)

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
            recovered = self._recover_unconfirmed_push(existing, picking)
            if recovered:
                return recovered.id
            # Shopify holds no fulfillment from that attempt: send it again.
            existing.unlink()

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
        binding.write(self._pushed_fulfillment_values(payload, tracking))
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
        self._refresh_after_push(binding)
        return binding.id

    def _pushed_fulfillment_values(self, payload, tracking):
        tracking_payload = _tracking(payload) or tracking
        return {
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

    def _refresh_after_push(self, binding):
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

    def _unconfirmed_push_matches(self, attempt, picking, payloads):
        """Return the Shopify fulfillments an unconfirmed push may have created.

        ``attempt`` is a connector fulfillment that never received its Shopify
        ID, so Shopify may or may not have created it. A fulfillment matches
        when Shopify created it at the attempt's location, no earlier than the
        attempt, and it only holds items of the delivery, in quantities the
        delivery covers.
        """
        self.ensure_one()
        delivered = defaultdict(float)
        for move in self._fulfillment_allocation_input(picking):
            delivered[move["line_id"]] += move["quantity"]
        not_before = attempt.create_date - UNCONFIRMED_PUSH_CLOCK_SKEW
        matches = []
        for payload in payloads:
            if not payload.get("id"):
                continue
            status = str(payload.get("status") or "").upper()
            if status in FAILED_FULFILLMENT_STATUSES:
                continue
            location_id = (payload.get("location") or {}).get("id")
            if (
                attempt.location_shopify_id
                and location_id != attempt.location_shopify_id
            ):
                continue
            created_at = _utc_datetime(payload.get("createdAt"))
            if not created_at or created_at < not_before:
                continue
            quantities = defaultdict(float)
            for line in _nodes(payload.get("fulfillmentLineItems")):
                line_id = str((line.get("lineItem") or {}).get("id") or "")
                quantities[line_id] += float(line.get("quantity") or 0)
            if not quantities or any(
                not line_id or quantity > delivered.get(line_id, 0)
                for line_id, quantity in quantities.items()
            ):
                continue
            matches.append(payload)
        return matches

    def _recover_unconfirmed_push(self, attempt, picking):
        """Bind the Shopify fulfillment an unconfirmed push created, if any.

        Returns the confirmed binding, or an empty recordset when Shopify holds
        no fulfillment from that attempt and the delivery can be sent again.
        """
        self.ensure_one()
        fulfillment_model = self.env["shopify.fulfillment"]
        data = self.instance_id._shopify_client().execute(
            ORDER_FULFILLMENTS_QUERY,
            {"id": self.shopify_id},
        )
        order = data.get("order")
        if not order:
            raise ShopifyFulfillmentError(
                self.env._("Shopify order %s was not found.", self.shopify_id)
            )
        payloads = _nodes(order.get("fulfillments"))
        known = fulfillment_model.search(
            [
                ("instance_id", "=", self.instance_id.id),
                (
                    "shopify_id",
                    "in",
                    [payload["id"] for payload in payloads if payload.get("id")],
                ),
            ]
        )
        # Fulfillments the connector pushed for other deliveries are not
        # candidates; external ones may be this attempt imported by webhook.
        pushed_ids = set(
            known.filtered(lambda item: item.origin == "odoo").mapped("shopify_id")
        )
        matches = [
            payload
            for payload in self._unconfirmed_push_matches(attempt, picking, payloads)
            if payload["id"] not in pushed_ids
        ]
        if not matches:
            return fulfillment_model
        if len(matches) > 1:
            raise ShopifyFulfillmentError(
                self.env._(
                    "A previous Shopify fulfillment attempt for %(picking)s was not "
                    "confirmed, and several Shopify fulfillments could be the one "
                    "it created: %(fulfillments)s. Bind the right one manually.",
                    picking=picking.name,
                    fulfillments=", ".join(payload["id"] for payload in matches),
                )
            )
        payload = matches[0]
        binding = attempt
        imported = known.filtered(lambda item: item.shopify_id == payload["id"])
        if imported:
            if imported.picking_id:
                raise ShopifyFulfillmentError(
                    self.env._(
                        "Shopify fulfillment %(fulfillment)s, created by an "
                        "unconfirmed attempt for %(picking)s, was imported as an "
                        "external fulfillment that validated %(other)s. Review "
                        "both deliveries before binding it.",
                        fulfillment=payload["id"],
                        picking=picking.name,
                        other=imported.picking_id.name,
                    )
                )
            fulfillment_orders = attempt.fulfillment_order_ids | (
                imported.fulfillment_order_ids
            )
            attempt.unlink()
            imported.write(
                {
                    "origin": "odoo",
                    "picking_id": picking.id,
                    "idempotency_key": f"picking:{picking.id}",
                    "fulfillment_order_ids": [Command.set(fulfillment_orders.ids)],
                }
            )
            binding = imported
        binding.write(
            self._pushed_fulfillment_values(payload, self._tracking_info(picking))
        )
        self.instance_id._write_log(
            entity="fulfillment",
            direction="export",
            level="info",
            message=self.env._(
                "Bound Shopify fulfillment %(fulfillment)s, created by an "
                "unconfirmed attempt, to delivery %(delivery)s.",
                fulfillment=binding.shopify_id,
                delivery=picking.name,
            ),
            record=binding,
        )
        self._refresh_after_push(binding)
        return binding

    def _unconfirmed_push_for(self, payload):
        """Return the single unconfirmed connector push matching ``payload``."""
        self.ensure_one()
        attempts = self.env["shopify.fulfillment"].search(
            [
                ("instance_id", "=", self.instance_id.id),
                ("order_binding_id", "=", self.id),
                ("origin", "=", "odoo"),
                ("shopify_id", "=", False),
                ("picking_id", "!=", False),
            ]
        )
        found = self.env["shopify.fulfillment"]
        for attempt in attempts:
            try:
                if self._unconfirmed_push_matches(
                    attempt, attempt.picking_id, [payload]
                ):
                    found |= attempt
            except ShopifyFulfillmentError:
                continue
        return found if len(found) == 1 else self.env["shopify.fulfillment"]


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
            # Any stock user may validate a delivery; only the lookup of the
            # order bindings needs Shopify access.
            bindings = picking.sale_id.sudo().shopify_binding_ids.filtered(
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
            # Any stock or purchase user may cancel a picking; only the lookup
            # of its fulfillments needs Shopify access.
            fulfillments = picking.sudo().shopify_fulfillment_ids.filtered("shopify_id")
            for fulfillment in fulfillments:
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
        self.env.cr.execute(
            "SELECT pg_try_advisory_xact_lock(%s, hashtext(%s))",
            (instance.id, fulfillment_id),
        )
        if not self.env.cr.fetchone()[0]:
            raise RetryableJobError(
                self.env._(
                    "Another job is importing Shopify fulfillment %s.", fulfillment_id
                ),
                seconds=5,
            )
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
            instance._write_log(
                entity="fulfillment",
                direction="import",
                level="info",
                message=self.env._(
                    "Shopify order %s is not imported yet. Its fulfillment is "
                    "applied when the order is imported.",
                    order_id,
                ),
            )
            return False
        binding = self.search(
            [
                ("instance_id", "=", instance.id),
                ("shopify_id", "=", fulfillment_id),
            ],
            limit=1,
        )
        if not binding:
            # A connector push whose response was lost: this is its echo, not
            # an external fulfillment that should validate another delivery.
            binding = order_binding._unconfirmed_push_for(payload)
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
        if self.picking_id:
            # Deliveries are validated only once; later updates of the
            # fulfillment only refresh the carrier and tracking.
            self._apply_external_tracking(self.picking_id, payload, webhook_payload)
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
        location = self.env["shopify.location"].search(
            [
                ("instance_id", "=", self.instance_id.id),
                ("shopify_id", "=", self.location_shopify_id),
            ],
            limit=1,
        )
        try:
            # Separate savepoints: the order stays confirmed even when its
            # deliveries cannot be validated yet.
            with self.env.cr.savepoint():
                self._confirm_external_order()
            with self.env.cr.savepoint():
                pickings = self._validate_external_deliveries(
                    quantities, location.odoo_location_id, payload, webhook_payload
                )
        except UserError as error:
            message = self.env._(
                "Shopify fulfillment %(fulfillment)s did not validate the Odoo "
                "delivery: %(error)s",
                fulfillment=self.shopify_id,
                error=str(error),
            )
            self.write({"state": "error", "error_message": message})
            self.instance_id._write_log(
                entity="fulfillment",
                direction="import",
                level="error",
                message=message,
                record=self,
            )
            return False
        if not pickings:
            return False
        self.picking_id = pickings[:1]
        self.instance_id._write_log(
            entity="fulfillment",
            direction="import",
            level="info",
            message=self.env._(
                "Validated Odoo delivery %(pickings)s from Shopify fulfillment "
                "%(fulfillment)s.",
                pickings=", ".join(pickings.mapped("name")),
                fulfillment=self.shopify_id,
            ),
            record=self,
        )
        return True

    def _confirm_external_order(self):
        sale_order = self.order_binding_id.odoo_id
        if sale_order.state not in ("draft", "sent"):
            return
        # Shopify shipped the items, so the quotation is confirmed to get its
        # deliveries, which keep the risk hold of the order.
        sale_order.action_confirm()
        if sale_order.shopify_risk_hold:
            sale_order.picking_ids.write({"shopify_risk_hold": True})
        self.instance_id._write_log(
            entity="fulfillment",
            direction="import",
            level="info",
            message=self.env._(
                "Confirmed sale order %(order)s because Shopify fulfillment "
                "%(fulfillment)s shipped its items.",
                order=sale_order.name,
                fulfillment=self.shopify_id,
            ),
            record=self,
        )

    def _validate_external_deliveries(
        self, quantities, location, payload, webhook_payload
    ):
        # Quantity to ship per sale line and product: a kit line needs its
        # components, not the kit product.
        needed = {}
        sale_lines = self.env["sale.order.line"]
        for line_id, quantity in quantities.items():
            line_binding = self.order_binding_id.line_binding_ids.filtered(
                lambda item, line_id=line_id: item.shopify_id == line_id
            )[:1]
            sale_line = line_binding.odoo_id
            # Services, and lines without an Odoo sale line, ship nothing.
            if not quantity or sale_line.product_id.type != "consu":
                continue
            sale_lines |= sale_line
            for product, product_quantity in self._external_line_needs(
                sale_line, quantity
            ).items():
                needed[(sale_line, product)] = product_quantity
        if not sale_lines:
            return self.env["stock.picking"]
        # Odoo creates each delivery step when the previous one is done, so the
        # last step may not exist yet, or may not hold all the items. Each pass
        # validates the earlier steps for the items that the last step does not
        # have reserved, until it has them all. Steps already done in Odoo,
        # such as a pick validated by hand, are skipped.
        for _step in range(MAX_DELIVERY_STEPS):
            allocation = self._external_allocation(needed, "outgoing", location)
            if allocation:
                self._external_moves(allocation).picking_id.action_assign()
            upstream = self._external_allocation(
                self._external_missing(needed, allocation), "internal", location
            )
            if not upstream:
                break
            self._ship_external_moves(upstream)
        allocation = self._external_allocation(needed, "outgoing", location)
        if not allocation:
            # Items already delivered by hand in Odoo are not an error.
            moves = self._external_chain_moves(sale_lines)
            if moves and all(move.state == "done" for move in moves):
                self.instance_id._write_log(
                    entity="fulfillment",
                    direction="import",
                    level="info",
                    message=self.env._(
                        "The items of Shopify fulfillment %s were already "
                        "delivered in Odoo.",
                        self.shopify_id,
                    ),
                    record=self,
                )
                return self.env["stock.picking"]
            raise ShopifyFulfillmentError(
                self.env._(
                    "No open Odoo delivery contains its items. Check the "
                    "deliveries of the sale order, then retry."
                )
            )
        pickings = self._external_moves(allocation).picking_id
        # Copy the tracking first: when a delivery without tracking number is
        # validated, Odoo books a shipment with an integrated carrier.
        self._apply_external_tracking(pickings, payload, webhook_payload)
        self._ship_external_moves(allocation)
        return pickings.sorted(lambda picking: (picking.date_done, picking.id))

    def _external_line_needs(self, sale_line, quantity):
        ordered = sale_line.product_uom_qty
        if float_is_zero(ordered, precision_rounding=sale_line.product_uom_id.rounding):
            return {}
        moves = self._external_chain_moves(sale_line)
        # The first step holds the whole quantity of each product, even once
        # done, so a kit line gets the share of each of its components.
        first_moves = moves.filtered(lambda move: not move.move_orig_ids & moves)
        needs = {}
        for product in first_moves.product_id:
            total = sum(
                first_moves.filtered(
                    lambda move, product=product: move.product_id == product
                ).mapped("product_qty")
            )
            needs[product] = float_round(
                quantity * total / ordered,
                precision_rounding=product.uom_id.rounding,
            )
        return needs

    def _external_chain_moves(self, sale_lines):
        # The delivery and its pick and pack steps, without returns. Scrap
        # moves have no outgoing or internal operation type, so they are left
        # out as well.
        return sale_lines.move_ids.filtered(
            lambda move: (
                move.state != "cancel"
                and not move.origin_returned_move_id
                and (
                    move.picking_code == "outgoing"
                    or (
                        move.picking_code == "internal"
                        and move.location_final_id.usage == "customer"
                    )
                )
            )
        )

    def _external_allocation(self, needed, picking_code, location):
        def sort_key(move):
            # Moves whose previous step is done first, then the moves at the
            # fulfillment location, then the oldest transfers.
            at_location = bool(
                location.parent_path
                and (move.location_id.parent_path or "").startswith(
                    location.parent_path
                )
            )
            advanced = any(previous.state == "done" for previous in move.move_orig_ids)
            return (
                not advanced,
                not at_location,
                move.picking_id.scheduled_date or datetime.max,
                move.picking_id.id,
                move.id,
            )

        allocation = {}
        for (sale_line, product), quantity in needed.items():
            rounding = product.uom_id.rounding
            moves = (
                self._external_chain_moves(sale_line)
                .filtered(
                    lambda move, product=product: (
                        move.product_id == product
                        and move.state != "done"
                        and move.picking_id
                        and move.picking_code == picking_code
                    )
                )
                .sorted(sort_key)
            )
            for move in moves:
                if float_compare(quantity, 0, precision_rounding=rounding) <= 0:
                    break
                taken = min(quantity, move.product_qty - allocation.get(move, 0.0))
                if float_compare(taken, 0, precision_rounding=rounding) > 0:
                    allocation[move] = allocation.get(move, 0.0) + taken
                    quantity = float_round(
                        quantity - taken, precision_rounding=rounding
                    )
        return allocation

    def _external_missing(self, needed, allocation):
        # The quantity the allocated moves do not have reserved yet is still
        # in an earlier step.
        missing = {}
        for (sale_line, product), quantity in needed.items():
            covered = sum(
                min(self._external_reserved_quantity(move), allocated)
                for move, allocated in allocation.items()
                if move.sale_line_id == sale_line and move.product_id == product
            )
            rest = float_round(
                quantity - covered, precision_rounding=product.uom_id.rounding
            )
            if float_compare(rest, 0, precision_rounding=product.uom_id.rounding) > 0:
                missing[(sale_line, product)] = rest
        return missing

    def _external_moves(self, allocation):
        return self.env["stock.move"].browse([move.id for move in allocation])

    def _external_reserved_quantity(self, move):
        return move.product_uom._compute_quantity(move.quantity, move.product_id.uom_id)

    def _ship_external_moves(self, allocation):
        pickings = self._external_moves(allocation).picking_id
        pickings.action_assign()
        # Without Ship Unreserved Stock, the fulfilled items must be reserved,
        # so lots and serial numbers come from the reservation.
        if not self.instance_id.fulfillment_validate_unreserved:
            for move, quantity in allocation.items():
                if (
                    float_compare(
                        self._external_reserved_quantity(move),
                        quantity,
                        precision_rounding=move.product_id.uom_id.rounding,
                    )
                    < 0
                ):
                    raise ShopifyFulfillmentError(
                        self.env._(
                            "Odoo could not reserve %(product)s on %(transfer)s. "
                            "Add the stock, or enable Ship Unreserved Stock on "
                            "the Shopify instance, then retry.",
                            product=move.product_id.display_name,
                            transfer=move.picking_id.name,
                        )
                    )
        # Ship only the fulfilled quantities; with skip_backorder, the rest of
        # each transfer goes to a backorder without asking.
        for move in pickings.move_ids.filtered(
            lambda item: item.state not in ("done", "cancel")
        ):
            quantity = allocation.get(move)
            if quantity:
                move.quantity = move.product_id.uom_id._compute_quantity(
                    quantity, move.product_uom
                )
                move.picked = True
            else:
                move.picked = False
        # Shopify already has this fulfillment, so it is not sent back.
        pickings.with_context(
            skip_backorder=True,
            skip_sms=True,
            skip_shopify_fulfillment_push=True,
        ).button_validate()
        not_done = pickings.filtered(lambda picking: picking.state != "done")
        if not_done:
            raise ShopifyFulfillmentError(
                self.env._(
                    "Odoo transfer %s could not be validated.",
                    ", ".join(not_done.mapped("name")),
                )
            )

    def _external_tracking_values(self, payload, webhook_payload):
        tracking = payload.get("trackingInfo") or []
        if isinstance(tracking, dict):
            tracking = [tracking]
        tracking = [item for item in tracking if isinstance(item, dict)]
        # A fulfillment can have one tracking number per package; all are kept.
        numbers = [str(item.get("number") or "").strip() for item in tracking]
        company = next(
            (
                str(item["company"]).strip()
                for item in tracking
                if str(item.get("company") or "").strip()
            ),
            "",
        )
        if not any(numbers):
            # Fall back on the webhook payload when the fulfillment has none.
            numbers = [
                str(number).strip()
                for number in (
                    webhook_payload.get("tracking_numbers")
                    or [webhook_payload.get("tracking_number")]
                )
                if number
            ]
        company = company or str(webhook_payload.get("tracking_company") or "").strip()
        values = {}
        numbers = list(dict.fromkeys(number for number in numbers if number))
        if numbers:
            values["carrier_tracking_ref"] = ",".join(numbers)
        carrier = self._external_carrier(company)
        if carrier:
            values["carrier_id"] = carrier.id
        return values

    def _external_carrier(self, company):
        carrier = self.env["delivery.carrier"]
        if not company:
            return carrier
        mapping = self.instance_id.carrier_mapping_ids.filtered(
            lambda item: (
                (item.tracking_company or "").strip().casefold() == company.casefold()
            )
        )[:1]
        if mapping:
            return mapping.carrier_id
        return carrier.search(
            [
                ("name", "=ilike", company),
                ("company_id", "in", [False, self.company_id.id]),
            ],
            limit=1,
        )

    def _apply_external_tracking(self, pickings, payload, webhook_payload):
        values = self._external_tracking_values(payload, webhook_payload)
        for picking in pickings:
            changes = {}
            if values.get("carrier_tracking_ref") and (
                picking.carrier_tracking_ref != values["carrier_tracking_ref"]
            ):
                changes["carrier_tracking_ref"] = values["carrier_tracking_ref"]
            if (
                values.get("carrier_id")
                and picking.carrier_id.id != values["carrier_id"]
            ):
                changes["carrier_id"] = values["carrier_id"]
            if changes:
                picking.write(changes)


class SaleOrderShopifyFulfillmentRetry(models.Model):
    _inherit = "sale.order"

    def action_release_shopify_risk_hold(self):
        result = super().action_release_shopify_risk_hold()
        # Fulfillments that failed on the risk hold can now validate their
        # deliveries.
        fulfillments = self.sudo().shopify_binding_ids.fulfillment_ids.filtered(
            lambda item: (
                item.origin == "shopify"
                and item.state == "error"
                and item.shopify_id
                and not item.picking_id
            )
        )
        if fulfillments:
            fulfillments.action_retry_sync()
        return result


WEBHOOK_HANDLERS.update(
    {
        "fulfillments/create": "_handle_fulfillments_create",
        "fulfillments/update": "_handle_fulfillments_update",
    }
)
