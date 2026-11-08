Bind Mercado Libre listings to Odoo products and keep price and seller stock aligned.

Listings are matched by the `SELLER_SKU` attribute, then by `seller_custom_field`,
then by the product internal reference. A listing that does not match stays unbound.
**Create missing products** is off by default.

Price export uses the Mercado Libre Prices API. Stock export sends `available_quantity`
for legacy items and `PUT /user-products/{id}/stock/type/seller_warehouse` when the
backend version is User products. Fulfillment stock is read-only.
