Synchronizes all the Shopify product media with the extra product media of the
Odoo eCommerce (`product.image`).

Without this glue module, Shopify Connector only synchronizes the main image of
each product and the images of its variants, and leaves the other Shopify
images untouched. With it, the other Shopify images are imported as extra
product media, and the extra product media managed in Odoo are exported to
Shopify.

The module installs automatically when Shopify Connector and eCommerce are both
installed.
