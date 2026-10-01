Scan EAN13 barcodes to quickly process warehouse operations.

## Receipts

From the main menu, select **Warehouse Operations**, then choose
**Receipts** to validate incoming goods. Scan product barcodes to
register quantities.

## Deliveries

From **Warehouse Operations**, select **Delivery Orders** to pick and
ship items. Scan product barcodes to confirm each item.

## Internal Transfers

Use the **Internal Transfer** screen from the main menu to move stock
between locations. Select the origin and destination locations, then
scan or search products to add transfer lines.

## Quantities from the barcode

A scan normally counts as one unit. When the barcode states a quantity — as a
GS1 label does, with ``barcode_gs1`` installed — that quantity is taken instead,
in the product's own unit of measure:

- a label that states a **measure** (a net weight, for instance) is the quantity
  when the product is stocked in that kind of unit, converted if needed: 2.497 kg
  on the label becomes 2.497 for a product in kilograms and 2497 for one in
  grams;
- when the product is *not* stocked that way — a box counted in units — the
  **piece count** on the label is the quantity, and a single unit when the label
  states no count. A weight never turns into a number of units.

## Quick Info

Select **Quick Info** from the main menu, then scan any product or
location barcode to view information. Alternatively, search by barcode
or browse the product and location lists.
