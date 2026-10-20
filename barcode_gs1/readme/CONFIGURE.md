No configuration is needed: once installed, GS1 barcodes are parsed wherever
the app reads a scan. Two things can be adjusted.

## Application identifiers

The application identifiers are read from a GS1 ``barcode.nomenclature``: the
one set on the company when it is a GS1 nomenclature, otherwise the first GS1
nomenclature found (the *Default GS1 Nomenclature* Odoo ships). Its GS1-128
rules are fetched once, when the barcode app opens.

To teach the scanner a new application identifier, add a rule under
*Inventory → Configuration → Barcode Nomenclatures* — no code change. A rule
whose *Type* is one the app understands (product, lot, quantity, weighted
product, priced product, package, package type, expiration date, best before
date, pack date, location, destination location) lands on the matching field of
the parsed scan (see Usage); the value of any other rule is still available in
``ais``.

Identifiers the nomenclature does not define keep working through the ones built
into the module, and if the nomenclature cannot be read at all the module falls
back to them entirely.

## Scanners that cannot send FNC1

GS1 ends a variable-length value with FNC1 unless it is the last element of the
barcode, and a keyboard-wedge scanner often sends nothing in its place. Odoo has
a field for exactly that — *FNC1 Separator* on the nomenclature — so configure
the scanner to send one of those characters (``#`` out of the box) and the scan
is read as printed.
