Stock export is two components with usage `stock.exporter`. `_component_match` keeps
the component for the backend version:

- `mercadolibre.product.exporter.stock.legacy` writes `available_quantity` on
  `PUT /items/{id}` when **Versions** is Legacy items.
- `mercadolibre.product.exporter.stock.user_product` writes
  `PUT /user-products/{id}/stock/type/seller_warehouse` (or `selling_address`) when
  **Versions** is User products.

A binding with an empty `user_product_id` uses the legacy call, including when the
backend version is User products. Fulfillment bindings and fulfillment warehouse lines
are skipped. The quantity is `product.with_context(warehouse_id=warehouse).free_qty`
for that mapped warehouse only.

`_apply_on` has to be an Odoo model. The Mercado Libre topic is not a model, so the
handlers set `_topic` to `items` or `stock-location` and `_apply_on` to
`mercadolibre.notification`. The core dispatcher selects the handler by `_topic`.

`mercadolibre.product.binder` resolves a listing with
`to_internal(external_id, variation_id=...)`. An empty variation id is the item that
has no variations. `to_external` returns the Mercado Libre item id.

Publishing a new listing is the component usage `product.publisher`. This module ships
a publisher that raises `UserError` with "Listing publication is not installed." A
localization replaces that component with `POST /items` without changing price or stock
export.

Import and export mappers are separate (`import.mapper` and `export.mapper`). The
export mapper exposes `price_payload`, `legacy_stock_payload`, and
`user_product_stock_payload` so a price body is never merged into a stock body.

Import jobs use the identity key `meli:item:{backend_id}:{item_id}:`. One job imports
every variation of the item. Price jobs use `meli:price:{backend_id}:{binding_id}`.
Stock jobs use `meli:stock:{backend_id}:{binding_id}:{mapping_id}`.
