Scrap damaged or lost goods directly from the Barcode scanner app.

The operator picks the internal location the goods are written off from, scans
them (with a GS1 parser installed, a GS1 label also gives its lot/serial and
piece count), sets
the quantities, chooses the scrap reasons and scraps. Each line becomes a
native `stock.scrap`, created and validated on the spot, so the stock leaves the
location for the scrap location exactly as it does from the back office.

This is a feature module on top of `barcode_scanner`: it registers its own
screens, scan handling and home-screen tile into the scanner core without
patching it, so you install only what you need.
