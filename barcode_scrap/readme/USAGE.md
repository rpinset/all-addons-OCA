From the Barcode app home screen, tap **Scrap Products**.

## Scrap goods

1. **Pick or scan the location** the goods are written off from. Scanning a
   location barcode jumps straight to the scrap lines; otherwise choose one
   from the searchable list of internal locations.
2. **Scan each product** to scrap: a plain barcode adds one unit. With a GS1
   parser installed, a GS1 label also gives its **lot/serial** and its **piece
   count** (AI 30/37); a net weight on the label is not taken as the quantity.
   Scanning the same product and lot again adds to its line. Tap **"+"** to add
   a product by hand; with no search it lists what the location holds. Only
   goods can be scrapped, as in the back office: services are not offered.
3. Each line shows how much of it the location holds. Adjust the quantity
   if needed.
4. Choose the **scrap reasons** and tap **Scrap**. A reason that does not
   exist yet can be created on the spot with **New reason**, as the back
   office's reason field allows; typing the name of an existing one (in any
   case) picks that one instead of creating a duplicate.

## Lots and serial numbers

A lot is found by its exact name: lots whose names differ only in case are
different lots. A name typed in another case finds its lot only when it names a
single one.

A lot/serial-tracked product needs its lot/serial: read from the GS1 label,
or typed into the line, which suggests the lots stored in that location. When
the location holds a single lot of the product, it is filled in. A serial
number is scrapped one unit at a time and can only appear once.

## Stock shown and not enough stock

The quantity each line shows is what a scrap made from the scanner can take:
the net quantity at the location itself, outside packages and not owned by a
partner, as validating the scrap counts it. Goods in a package or owned by a
partner are scrapped from the back office, where the scrap takes a package and
an owner.

When a line asks for more than that, nothing is scrapped yet: the scanner lists
what is short and asks whether to **scrap anyway** — the same choice the back
office offers through its insufficient-quantity wizard. Confirming scraps the
lines it was asked about; lines changed in between are checked again.

## Destination

The goods go to the scrap location the back office preselects for the company,
and can be sent to any scrap location of the company or a shared one instead.
When the company has none of its own, the first shared one is taken; with no
scrap location at all, scrapping waits until one is created.

## Reading more from a label

The quantity a scan stands for comes from ``ScrapScreen.scannedQuantity(scan,
productUomId)``: the piece count, or one unit. A module that reads more from a
label (a GS1 net weight, say) can patch it to convert that into the product's
unit, as ``barcode_stock`` offers with its own ``scannedQuantity``.
