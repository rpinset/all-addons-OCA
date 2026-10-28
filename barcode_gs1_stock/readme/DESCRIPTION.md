This module is the bridge between **GS1 barcodes** and the **warehouse app**: it
makes the measure a GS1 label carries the quantity picked, expressed in the unit
the product is stocked in.

A GS1 label often states both, and they disagree: a box of cured meat carries
"2 pieces" (AI 30) and "2.497 kg" (AI 310n). Which of the two is the quantity
depends on how the product is stocked, something only the warehouse knows —
kilograms make it the weight, units make it the count.

It installs itself as soon as both ``barcode_gs1`` and ``barcode_stock`` are
installed, and neither needs the other without it.
