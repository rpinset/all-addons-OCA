Handlers set `_topic` to `orders_v2`, `shipments`, or `payments` and `_apply_on` to
`mercadolibre.notification`. The core dispatcher matches `_topic`. `_apply_on` has
to be an Odoo model, so the topic name is not stored there.

Line builders share the usage `sale.order.line.builder`. The importer loads them
with `many_components` and sorts by `_sequence` (product 10, shipping 20, fee 30).
Add another builder for a coupon or a local tax without changing the importer.

Odoo 19 rejects a sales order line that has neither a product nor a display type.
An unmatched item is a `line_note` with `mercadolibre_unmatched` set. The exception
rule `exception_missing_sku` reads that flag and blocks confirmation.

The status mapper usage is `status.mapper`. Override `apply` for a different
confirmation or cancellation rule. This module leaves paid orders in draft.

Tracking export is the stock picking listener, not the shipment importer. The
identity keys are:

- `meli:orders:{backend_id}` for the batch
- `meli:order:{backend_id}:{order_id}` for one order
- `meli:shipment:{backend_id}:{shipment_id}` for one shipment
- `meli:payment:{backend_id}:{resource}` for a payment notification
- `meli:tracking:{backend_id}:{shipment_id}` for a tracking export

Buyers are matched only through `mercadolibre.res.partner`. The binder does not
search `res.partner` by name.
