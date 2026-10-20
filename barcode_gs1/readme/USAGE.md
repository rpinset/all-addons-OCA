Install ``barcode_gs1`` alongside ``barcode_scanner`` (and a feature module such
as ``barcode_stock``). Once installed, GS1 barcodes are parsed automatically
wherever the app reads a scan.

A scanned GS1 barcode produces a parsed object such as:

    {
        type: "gs1",
        value: "<product code>",  // GTIN (AI 01), in the form products store
        gtin: "<GTIN>",           // the GTIN exactly as scanned (14 digits)
        productCodes: [...],      // every form the GTIN may be stored as
        lot: "<batch/lot>",       // AI 10 (falls back to the serial, AI 21)
        serial: "<serial>",       // AI 21
        expiry: "YYYY-MM-DD",     // AI 17, or 15/16 when no 17 is present
        useDate: "YYYY-MM-DD",    // AI 15 / 16 (best before, sell by)
        packDate: "YYYY-MM-DD",   // AI 13
        productionDate: "...",    // AI 11
        qty: <number>,            // AI 30 / 37; null when the label states no count
        count: <number>,          // AI 30 / 37 (pieces), kept next to the weight
        weight: <number>,         // AI 31xx–36xx, the measure of the goods
        weightUom: {id, name},    // the unit that measure is in, per the rule
        measures: [{ai, value, uom}, ...], // every measure, gross weight included
        price: <number>,          // AI 390n–393n (amount payable)
        currency: "<ISO 4217>",   // the numeric code AI 391n / 393n carries
        sscc: "<SSCC>",           // AI 00 (logistic unit)
        location: "<GLN>",        // AI 414
        locationDest: "<GLN>",    // AI 410 / 413
        ais: {"01": "...", "10": "...", ...},
        errors: [...],            // what could not be read, e.g. a bad check digit
    }

Both parenthesised barcodes — ``(01)09501101020917(10)LOT123(17)261231`` — and
raw FNC1-separated scans are supported.

GS1 always carries the GTIN zero-padded to 14 digits, while a product stores the
short code printed on the item. ``value`` therefore holds the padding-free form
Odoo stores (13 digits, as ``sanitize_ean`` produces), which is what the screens
match the product against; ``productCodes`` lists the other lengths a barcode may
have been stored as, longest-standing form first.

## Variable-length values

GS1 ends a variable-length value (a lot, a serial…) with FNC1, except when it is
the last element of the barcode, where none is needed. The parser reads it that
way: up to the next separator, or to the end of the barcode (see Configuration
for scanners that cannot send FNC1).

Only when that reading is impossible — a value longer than its rule allows —
was a separator clearly dropped. The value then ends at the next element that
reads cleanly: a specific numeric identifier (never an alphanumeric one, nor a
catch-all range) with a value, a real date or a right check digit. Anything
short of that is ambiguous — ``21 5830192`` is the serial 5830192, or the serial
58 followed by a count of 192 — and is read as GS1 says, as one value.

## Misreads are refused

A GTIN, SSCC or GLN is only accepted when its check digit (GS1 modulo 10)
matches. A misread identifier is left empty and reported in ``errors`` instead
of resolving to the wrong product or pallet.

## In the warehouse app

What the warehouse app does with it (with ``barcode_stock`` installed):

- the quantity picked is the piece count the label states (AI 30/37). A label
  without one picks a single unit, or the pack's quantity when its GTIN is a
  packaging barcode. A measure such as a net weight is decoded but not taken as
  the quantity: that depends on the unit the product is stocked in;
- the lot or serial is looked up for the scanned product and preselected in the
  move wizard; on a receipt an unknown lot opens the create-lot flow with the
  name and, when ``product_expiry`` is installed, the expiry date prefilled;
- on a delivery or an internal transfer, a lot that is not available is reported
  instead of silently picking another one.
