Since Odoo 18.0, `product_expiry` prevents the reservation of expired lots.

This module adds an option on Shopfloor menus to reserve goods whatever their
expiration date, relying on `product_expiry_assign`.

The option is available for the following scenarios:

- Location content transfer: when moves are created to move the whole content
  of a location, goods from expired lots are reserved too.
