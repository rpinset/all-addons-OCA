1. Go to *Settings → External Systems* (menu provided by ``base_external_system``).
2. Create a new record.
3. Set **System Type** to *External System RPC* (``external.system.odoo``).
4. Fill in the connection parameters:

   * Host (e.g. ``odoo-test.odoo.org``)
   * Port (e.g. ``443`` or ``8069``)
   * Database name
   * Username
   * Password
   * SSL toggle (if applicable)

5. Save the record.

After saving, the adapter interface record is created automatically by
``base_external_system`` and is available via the ``interface`` field.
