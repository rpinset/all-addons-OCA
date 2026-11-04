From the Barcode app home screen, tap **Inventory Adjustment**.

## Count a location

1. **Pick or scan the location** to count. Scanning a location barcode
   jumps straight into the count; otherwise choose one from the searchable
   list of internal locations.
2. The count screen shows the stock the location holds, one line per
   product and lot. **Count by scanning** each product: a plain barcode
   adds one unit. With `barcode_gs1` installed, a GS1 label also brings
   its **lot/serial** and its **quantity**; without it, the scanner reads
   plain EAN-13 barcodes only. You can also type the counted quantity in
   each line, decimals included, which then shows how far it is from the
   stock.
3. To count something not shown, tap **"+"** and scan or search the
   product. A freshly scanned or added product jumps to the top of the
   list and is highlighted, so you always see what the scan just changed.
   Only storable products can be counted: services and non-storable
   consumables are not offered, and scanning one says why it is refused.
4. Tap **Apply Adjustment** to record the count. If the stock of a
   counted product changed while you counted — goods came in or went out —
   nothing is applied yet: the lines show the stock as it is now, and you
   choose whether to apply your count anyway or to count again.

## Lots and serial numbers

A lot/serial-tracked product needs its lot/serial before it can be
applied — read from a GS1 label, or typed into the line (the lots a
count at that location can use are suggested; a new name is created on
the server). The name is
matched exactly first, as lots differing only in case are different lots;
in another case it is only taken when it names a single lot. The same
product can appear on **several lines**, one per lot or serial number, so
it stays available in the **"+"** picker even after it already has a line.

A serial number counts one unit: reading it again warns instead of
counting it twice.

## What it records

Each adjustment is applied as a
[stock_inventory](https://github.com/OCA/stock-logistics-warehouse)
adjustment group (draft → in progress → done), scoped to exactly the
counted products at the counted location, using Odoo's native on-hand
adjustment. Every barcode count therefore leaves one traceable, auditable
record with its own move lines. Lots are created in the counted location's
company.

A count covers the stock at the location itself, outside packages and not
owned by a partner: its sublocations are counted on their own, and stock in
a package or owned by someone else is neither shown nor changed.

As in the back office, applying a count requires **Inventory
Administrator** rights. Other users are told so when they open
**Inventory Adjustment**.
