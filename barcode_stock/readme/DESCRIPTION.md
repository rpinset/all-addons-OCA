This module is the **warehouse application** of the Barcode suite. It builds on
the `barcode_scanner` base framework and registers the stock operation screens,
scan handlers and menu tiles into it.

It covers the following operations:

- Receipts (incoming shipments)
- Deliveries (outgoing shipments)
- Internal transfers
- Quick product and location information

Only EAN13 barcodes are supported. Real-time validation and audio/vibration
feedback are provided on each scan.
