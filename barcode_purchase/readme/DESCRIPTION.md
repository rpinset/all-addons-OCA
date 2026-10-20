Create purchase orders directly from the Barcode scanner app.

The operator picks a vendor, a destination location and a buyer, then scans or
adds the products to order (with a GS1 parser installed, a GS1 label also gives
its lot/serial and piece count) and confirms. The module creates a
`purchase.order` and, when asked, confirms it — which raises the incoming
picking — so a purchase can be raised on the warehouse floor without opening the
back office. The server does it all in one call: a failure leaves no half-made
order behind.

This is a feature module on top of `barcode_scanner`: it registers its own
screens and home-screen tile into the scanner core without patching it, so you
install only what you need.
