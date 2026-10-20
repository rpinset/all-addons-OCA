This module adds the **device camera** as a scan source to the Barcode app, so
operators can scan without a dedicated hardware scanner.

A floating button opens the camera with Odoo's own barcode scanner dialog. The
code it reads is fed into the same event bus a hardware scanner uses, so the
active screen handles it exactly like any other scan. The button is plugged in
through the `barcode_app_widgets` registry of `barcode_scanner`, without
patching the app.
