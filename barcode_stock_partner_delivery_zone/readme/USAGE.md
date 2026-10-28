Configure the delivery zones in **Contacts > Configuration > Delivery Zones**
and set them on the customers (or their delivery addresses); their transfers get
the zone automatically.

## In the operation lists

- **Delivery orders open grouped by zone**, so the operator works through one
  zone at a time. Operations without a zone are grouped under **No zone**.
  Receipts and internal transfers open as before; the grouping can be turned on
  or off for any list from the **Group** menu, and it is kept during the
  session.
- The **Filters** menu has a **Delivery Zone** section: pick a zone, or
  **No zone**, to see only those operations. Like the status and date filters,
  it can be saved as the list's default with the ★.
- Each operation shows its zone, and typing a zone name in the search narrows
  the list to it.

## In an operation

The **Information** tab shows the operation's delivery zone and lets the
operator change it from the list of zones; the change is saved at once, as in
the back office (and reaches the sale order, through `partner_delivery_zone`).
