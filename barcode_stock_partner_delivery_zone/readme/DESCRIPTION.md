This module is the bridge between **delivery zones**
([partner_delivery_zone](https://github.com/OCA/delivery-carrier)) and the
**warehouse app** of the Barcode suite: the operations to process can be
grouped and filtered by the delivery zone of the customer they go to, and an
operation's zone can be changed from the scanner.

`partner_delivery_zone` gives each contact a delivery zone and carries it onto
the transfers made for it. This module brings that zone into `barcode_stock`'s
operation lists and into the operation's Information tab, without changing
either module.

It installs itself as soon as both ``barcode_stock`` and
``partner_delivery_zone`` are installed.
