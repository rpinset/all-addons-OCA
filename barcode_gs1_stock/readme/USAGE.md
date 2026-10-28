Installing ``barcode_gs1`` next to ``barcode_stock`` brings this module in, and
every screen that applies a scanned quantity uses it.

When a scanned GS1 barcode carries a measure, the unit that measure is in comes
from the rule that read it (*Unit of Measure* on the barcode rule — AI 310n is
kilograms, 320n pounds, 311n metres). It is then compared with the unit the
product is stocked in:

- **same kind of unit** — the measure is the quantity, converted into the
  product's own unit: 2.497 kg on the label is 2497 for a product in grams;
- **a different kind** — a weight for a product counted in units, say — the
  measure says nothing about how many to pick, so the piece count on the label
  (AI 30/37) is the quantity, and a single unit when the label states none.

When a label states several measures (a net weight and a net volume, say), the
first one in the product's kind of unit is taken. The gross weight and the other
measures of the pack itself (AI 330n–349n) never are.

The quantity is rounded the way it will be stored, so what the screen shows is
what ends up in stock. With Odoo's defaults that is two decimals: 2.497 kg is
2.50 for a product in kilograms (see Configuration to keep the grams). A measure
that rounds to nothing (4 g, for a product in kilograms kept to two decimals) is
not taken: the scan reads as one without a measure.

When the GTIN is a packaging barcode (a carton of twelve, say), a label without
a count picks the pack's quantity, and a count on the label wins over it. A
measure in the product's own kind of unit wins over both: a carton of cheese
weighing 4.32 kg is 4.32 for a product stocked in kilograms, not twelve.

The units of measure are read when the app opens. Should that fail, they are read
again on the next scan that carries a measure; that one scan reads as if it
carried none.

Without this module GS1 barcodes are still parsed, but a measure is never the
quantity: the warehouse app takes the piece count, or a single unit (the pack's
quantity for a packaging barcode).
