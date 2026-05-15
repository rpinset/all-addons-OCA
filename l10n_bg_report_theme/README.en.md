# Bulgaria — Report Theme Sections (OCA)

> A professional, modular section-based PDF report theme for Bulgarian
> business documents: configurable header / article / footer, dual
> logos, per-section backgrounds, portrait + landscape.

**Module:** `l10n_bg_report_theme` | **Version:** 18.0.5.0.4 | **License:** LGPL-3 | **Category:** Localization

## Overview

Bulgarian invoices, delivery slips, purchase orders and handover
protocols have layout expectations (company branding block, legal
footer, page numbering, room for two logos) that the stock Odoo report
layout doesn't cover cleanly. This module replaces the document layout
with a **three-section architecture** — Header / Article / Footer —
each independently styled, available in portrait and landscape, and
driving every Bulgarian-localization report.

## Architecture

### Extended models (`models/`)

| Model | Addition |
|---|---|
| `base.document.layout` | section-based layout fields (header/article/footer styling, backgrounds, dual logo, colors) |
| `res.company` | per-company layout configuration carrying the section settings |
| `ir.actions.report` | hooks so reports render through the themed templates |

### Templates & assets

- `views/report_templates.xml` — the section-based external layout
  (portrait + landscape).
- `views/report_invoice.xml`, `views/purchase_order_templates.xml`,
  `views/purchase_quotation_templates.xml` — themed document bodies.
- `views/base_document_layout_views.xml` /
  `views/ir_action_report_templates.xml` /
  `views/res_company_views.xml` — configuration UI.
- `data/report_layout.xml` + `data/report_paperformat_data.xml` —
  registers the layout and paper format.
- `web.report_assets_common` bundle ships the variable-font SCSS so PDF
  rendering uses the correct typography.

`webcolors` is used to parse/convert the configured colors.

## Dependencies

| Odoo core | Bulgarian-localization | External Python |
|---|---|---|
| `web`, `sale`, `account`, `stock`, `purchase` | `l10n_bg_config` | `webcolors` |

## Configuration

1. Install.
2. Settings → Companies → Document Layout: pick the Bulgarian
   section-based layout, set header/footer content, colors, logos and
   per-section backgrounds.
3. All Bulgarian reports (invoice, delivery, PO, handover protocol)
   render through it automatically.

## Downstream consumers

`l10n_bg_invoice_copy`, `l10n_bg_report_stock`,
`l10n_bg_sale_order_delivery_note` and effectively every
Bulgarian-localization PDF report build on this theme.

## Known limitations

- Section backgrounds and dual logos increase PDF render weight
  slightly on very high-volume batch printing.

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- Consumers: `l10n_bg_invoice_copy`, `l10n_bg_report_stock`,
  `l10n_bg_sale_order_delivery_note`
- `readme/` — source notes
