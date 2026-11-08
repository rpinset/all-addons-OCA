Import Mercado Libre orders, cart packs, and shipments into Odoo.

One Mercado Libre order becomes one sales order. Orders that share a pack id stay
linked. Shipment status is stored on its own binding and linked to the delivery
when one exists. Paid orders stay in draft and enter the automatic workflow
configured on the backend.
