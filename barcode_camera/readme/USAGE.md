Install ``barcode_camera`` next to a feature module such as ``barcode_stock``.

A camera button appears in the bottom-right corner of every screen that reads a
scan, whichever module it comes from: the home screen, the picking list and
picking, the move wizard, the selectors, and so on. Tap it, point the camera at
a barcode, and the scan is processed as if it came from a hardware scanner. The
codes read are the ones Odoo's scanner dialog reads: EAN, UPC, Code 128, Code
39, ITF, QR, Data Matrix and the like.

There is nothing to register for that: a screen reads scans through the hooks of
``barcode_scanner`` (``useBarcodeHandler``), which counts the screens doing so,
and the button shows whenever one does.

The browser only gives access to the camera in a secure context (HTTPS or
localhost). Without it, like Odoo's own camera buttons, the button is not
shown, and hardware or manual scanning remain available.
