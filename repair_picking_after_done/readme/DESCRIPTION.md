This module enhances Odoo's repair process by introducing automatic stock transfers for repaired products.

- **Automatic Transfer:** When a repair order is marked as done, a stock transfer for the remaining repaired products is automatically created and validated if the ***auto_transfer_repair*** parameter is enabled.
- **Manual Transfer:** Users can manually create stock transfers when automatic transfer is disabled.