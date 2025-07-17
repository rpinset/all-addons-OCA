Add method to get source location of Inventory Routes
--
This technical module extends the `stock.route` model to add the method
`_get_source_location(dest_location)`. It recursively traces upstream
rules (`pull` or `pull_push`) from a destination location, and returns
the ultimate source location — stopping at a rule with `procure_method='make_to_stock'`
or when no applicable pull rules remain.

Useful for multi-hop route setups (e.g., warehouse → packing → output),
to programmatically determine the actual stock source. No UI changes are made —
it's purely for custom logic or other technical modules.

**Example usage:**

```python
route = env.ref("stock.route_warehouse0_mto")
dest = env.ref("stock.stock_location_customers")
src = route._get_source_location(dest)
print(src.display_name)
