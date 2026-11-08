1.  Open the Mercado Libre backend and the page **Catalog**.
2.  Enable **Import listings**, **Export prices**, and **Export stock** as needed.
3.  Add a line per Odoo warehouse: Mercado Libre store id, network node id, and stock
    type (`seller_warehouse`, `selling_address`, or `fulfillment`).
4.  Set **Versions** on the backend. After connect, the core fills this from the
    `user_product_seller` tag on `/users/me`. Keep **User products** for sellers already
    migrated.
5.  Run **Import listings** on the backend. Review unmatched rows under **Mercado Libre /
    Catalog / Listings**.
6.  Open a product and use the **Mercado Libre** smart button to see its bindings. Set
    the internal reference to the seller SKU before the next import if the first pass
    did not match.
