# Bulgaria — Sale Line Description on Pickings (OCA)

> Shows the sale-order line description on stock pickings and delivery
> slips, so the delivered item text matches what the customer ordered.

**Module:** `l10n_bg_stock_sale_line_description` | **Version:** 18.0.1.0.1 | **License:** LGPL-3 | **Category:** Localization

## Overview

By default a delivery slip shows the product name, not the descriptive
text the salesperson entered on the sale-order line. Bulgarian
customers expect the delivery document to carry the same wording as
the order. This module surfaces the SO line description on the picking
form and the delivery-slip report.

## What it does

- `views/stock_picking_views.xml` inherits the picking form — adds the
  SO line description next to `description_picking` in the operations
  page.
- `report/report_deliveryslip.xml` inherits the delivery-slip report
  (and the serial-move-line variant) — prints the description in the
  move table.
- `security/res_groups.xml` ships a group gating whether the extra
  description column is shown.

Report/view-layer only — no model fields.

## Dependencies

| Odoo core | Bulgarian-localization |
|---|---|
| `stock`, `sale_stock` | — |

## Configuration

None (other than optionally assigning the visibility group). Install —
the description follows from the sale order onto the picking and its
printed delivery slip.

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- Related: `l10n_bg_report_stock`
