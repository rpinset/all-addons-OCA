A change to a product list price enqueues one price export for each binding of that
product. A done stock move enqueues one stock export per binding and mapped warehouse.
Both jobs use an identity key, so a burst of moves becomes a single pending job.

**Mercado Libre / Catalog / Categories** shows the cached category tree and the
attribute schema used when a publisher component creates a listing. **Refresh
categories** on the backend reloads that tree.

The notification topics `items` and `stock-location` update the binding.
`stock-location` writes the last marketplace quantity on the binding and does not
create `stock.quant` rows.
