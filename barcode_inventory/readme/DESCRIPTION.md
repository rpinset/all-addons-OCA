Perform inventory adjustments and stock counts directly from the Barcode
scanner app.

The operator picks an internal location, scans the products found there
(with `barcode_gs1` installed, a GS1 label also brings its lot/serial and
quantity), types the counted quantity, and applies. Each adjustment is recorded as a
[stock_inventory](https://github.com/OCA/stock-logistics-warehouse) adjustment
group — draft → in progress → done — so every barcode count leaves a traceable,
auditable record with its own move lines, using Odoo's native on-hand
adjustment mechanism (`stock.quant`).

This is a feature module on top of `barcode_scanner`: it registers its own
screens, scan handling and home-screen tile into the scanner core without
patching it, so you install only what you need.
