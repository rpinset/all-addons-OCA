Use **Shopify > Dashboard** to monitor binding states, queue backlog, recent
errors, webhook health, drift schedules, and operational table sizes.

Normal changes flow through webhooks and idempotent jobs. Use the entity import
or reconcile actions for manual catch-up. For failures, correct the underlying
configuration or data, select error bindings, and choose **Retry Failed
Shopify Bindings**. Resetting to pending clears the state without scheduling
work.

Tax lines with the same rate on one order line are added together before the
tax mapping lookup. For example, an order line with a 1% city tax and a 1%
transit tax needs a tax mapping for 0.02. If you mapped 0.01 to a 2% tax as a
workaround, map 0.02 to that tax instead.

With **Validate Deliveries from Webhooks** enabled on the instance, a
fulfillment made in Shopify or by a fulfillment app validates the fulfilled
items on the Odoo deliveries of the order:

- A sale order that is not confirmed yet is confirmed first.
- Each delivery step is validated for the fulfilled items, including the pick
  and pack steps. Items not fulfilled yet stay on a backorder.
- Kits ship their components.
- The carrier and tracking numbers of the fulfillment are copied to the
  delivery. The carrier comes from the carrier mappings of the instance, or
  else from a delivery carrier with the same name.
- A fulfillment validates deliveries only once. Later updates only refresh its
  carrier and tracking numbers.
- A fulfillment that Odoo missed, because its webhook was lost or arrived before
  the order, is applied the next time the order is imported.

The fulfilled items need reserved stock, so lots and serial numbers come from
the reservation. Enable **Ship Unreserved Stock** to also ship the items that
Odoo could not reserve. Products tracked by lot or serial number still need
reserved stock.

When a delivery cannot be validated, for example because of missing stock or a
risk hold, the fulfillment goes to error with the reason. Fix the cause and
retry it. Releasing the risk hold of an order retries its fulfillments
automatically.

The **Shopify Drift: Updated Orders** scheduled action imports again the orders
updated in Shopify since the **Sync Orders Updated Since** date of each
instance, then moves that date forward. It recovers the order changes whose
webhook was missed, and skips the orders whose latest version Odoo already
imported. To import older updated orders on the next run, set an earlier date on
the **Orders** tab of the instance.

Run **Check Webhooks** after changing domains or credentials and repair any
missing or misrouted subscriptions. Never edit Shopify IDs or raw payloads.
