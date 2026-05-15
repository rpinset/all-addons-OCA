# Bulgaria — Sale Order Accepted-Delivery Report (OCA)

> A QWeb PDF "accepted delivery" / pro-forma report generated directly
> from a Bulgarian sale order.

**Module:** `l10n_bg_sale_order_delivery_note` | **Version:** 18.0.1.0.0 | **License:** AGPL-3 | **Category:** Sales/Bulgaria

## Overview

Bulgarian sales practice often needs an accepted-delivery / pro-forma
document issued at the **sale-order** stage (before or instead of the
stock-side handover protocol). This module adds that report on
`sale.order`.

## What it provides

- `report/ir_actions_report.xml` — an `ir.actions.report` (qweb-pdf)
  bound to `sale.order`, available from the order's Print menu.
- `report/ir_action_report_templates.xml` — the QWeb template, using
  the Bulgarian section-based report theme.

Report-layer only — no model fields, no seeded data.

## Dependencies

| Odoo core | Bulgarian-localization |
|---|---|
| `sale` | `l10n_bg_report_theme` |

## Configuration

None. Install — the accepted-delivery report appears in the sale-order
Print menu.

## Related modules

`l10n_bg_report_stock` provides the stock-picking-side handover
protocol + accepted-delivery slip; this module is the
sale-order-side counterpart.

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- Stock-side: `l10n_bg_report_stock`
- Report layout: `l10n_bg_report_theme`
