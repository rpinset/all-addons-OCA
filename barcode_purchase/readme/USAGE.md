From the Barcode app home screen, tap **Purchase Orders**.

## Raise an order

1. **Pick the vendor.** Scanning a partner barcode selects it straight away;
   otherwise choose one from the searchable list of suppliers.
2. Optionally set the **destination location** (the destinations of the
   receipt operations are offered, and scanning a location picks it), the
   **buyer** (Odoo's native purchase-order responsible user) and a **vendor
   reference**.
3. **Add the products.** Each line is ordered in the product's **purchase unit**,
   shown under its quantity. Scanning a product adds one purchase unit. With a
   GS1 parser installed, a GS1 label also gives its **lot/serial** and its
   **piece count** (AI 30/37), which is converted from the product's unit into
   the purchase unit (24 pieces of a product bought by the dozen are 2 Dozens);
   a net weight on the label is not taken as the quantity. Scanning the same
   product and lot again adds to its line; a serial number stands for a single
   unit and is listed once. You can also tap **"+"** to search and add a
   product, and edit the quantity on each line. Only goods that can be purchased
   are offered.
4. The **price** shown on each line is the one the order will take, as in the
   back office: the vendor's price, in the purchase unit and the order's
   currency. Type a price to use another one instead, 0 included.
5. Tap **Confirm Order** to create and confirm the purchase order, or **Save
   Draft** to create it without confirming.

## Destination and lots

The destination and the lots read are kept on the order, so they hold however
the order is confirmed: from the scanner, or later in the back office (a draft,
or an order approved in two steps). The destination picks the receipt
operation of its warehouse and becomes the final location of each line, which
the stock moves follow: straight into it with a reception in one step, through
the input and the steps after it with a reception in several. The lots read are
kept on their lines (*Lot/Serial Read*) and written on the receipt when it is
created.

## Automatic validation

With **Validate automatically** ticked, **Confirm Order** confirms the order on
create, which raises the receipt. **Save Draft** always keeps it as a draft.

A lot/serial-tracked product does not hold the order back: only a GS1 label
carries a lot, and a vendor's lot is usually unknown until the goods turn up, so
the order is confirmed either way and the message names the products whose
lot/serial still has to be entered on the receipt.

That message names the order and the state it ended in, because a confirmation
does not always confirm: with two-step validation the order lands on **To
Approve** and raises no receipt until somebody approves it in the back office.

Creating and confirming a purchase order requires the **Purchase** user rights,
as in the back office.

## Reading more from a label

The quantity a scan stands for comes from ``PurchaseScreen.scannedQuantity(scan,
product)``, in the purchase unit: the pieces the label counts, converted, or one
purchase unit. A module that reads more from a label (a GS1 net weight, say) can
patch it to convert that into the purchase unit.
