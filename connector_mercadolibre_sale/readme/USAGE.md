Paid orders import as draft sales orders and take the automatic workflow from the
backend. A cart is several sales orders with the same pack id. The **Pack** smart
button opens the other orders.

A missing SKU is a note on the sales order. The exception **Mercado Libre missing
SKU** blocks confirmation until the listing is matched and the order is imported
again.

Cancelling a Mercado Libre order cancels that sales order when no delivery is done.
The other orders in the pack are left as they are.

Shipment notifications update the shipment binding. A done delivery on a `custom` or
`me1` shipment enqueues one tracking export. `me2` and fulfillment shipments store
the tracking number and do not send one.

A payments notification updates the payment status of the existing order. It does
not create a second sales order.

The reconciliation cron and a repeated `orders_v2` notification share one import job
per order.
