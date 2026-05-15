# Bulgaria — Accounting Reports Configuration (OCA)

> The UI layer for Bulgarian accounting reports: the Odoo 18 views,
> menus and account-tag wizard that surface the SQL view models from
> `l10n_bg_reports_audit`.

**Module:** `l10n_bg_reports_config` | **Version:** 18.0.9.0.2 | **License:** LGPL-3 | **Category:** Accounting/Localizations/Reporting

## Overview

`l10n_bg_reports_audit` computes the Bulgarian VAT declaration, sales
/ purchase ledgers and VIES as headless SQL view models. This module
is the **configuration + presentation half**: it ships the list/form
views, the accounting menu, the account-tag function seed and the
bulk-tag wizard, so an accountant can actually drive the reports from
the Odoo UI. Splitting UI from the data engine lets the engine version
independently of the Odoo-18-specific views.

## What it provides

### Views (`views/`)

- `account_bg_vat_line_sale_reports.xml` /
  `account_bg_vat_line_purchase_reports.xml` /
  `account_bg_vat_line_vies_reports.xml` — list/pivot views over the
  sales / purchases / VIES line models.
- `account_bg_partner.xml` / `account_bg_products.xml` — partner /
  product trail-balance views.
- `account_account_tag_views.xml` + `account_menuitem.xml` — NRA
  cell-tag maintenance + the Bulgarian-reports menu.
- `res_company_views.xml` / `res_company_history_vat.xml` /
  `res_company_history_intrastat.xml` — VAT-ratio (Art. 73 §2) and
  Intrastat-threshold history on the company.
- `res_config_view.xml`, `res_partner.xml`, `product_view.xml`,
  `account_move_views.xml` — supporting form extensions.

### Model

`l10n.bg.vat.ratio.history` (extended, `models/res_company_history_vat.py`)
— UI-side additions to the VAT-ratio history record.

### Wizard

`account_account_tag_bulk_edit_wizard` (`wizards/`) — bulk-assign NRA
cell tags across many accounts in one pass (the practical way to map a
whole chart of accounts to the declaration cells).

### Seed data

`data/account_account_tag_function.xml` (tag→function mapping) +
`data/settings.xml`.

## Dependencies

| Odoo core | Bulgarian-localization |
|---|---|
| `base`, `account` | `l10n_bg_reports_audit`, `l10n_bg_config`, `l10n_bg_ledger` |

## Configuration

1. Install (pulls `l10n_bg_reports_audit`).
2. Accounting → Bulgaria → review the VAT / sales / purchases / VIES
   report views.
3. Use the account-tag bulk-edit wizard to map the chart of accounts
   to the NRA declaration cells.
4. Set the company VAT ratio (Art. 73 §2) and Intrastat thresholds on
   the company history views.

## Known limitations

- Presentation only — the figures come from the
  `l10n_bg_reports_audit` SQL views; a wrong number is fixed in the
  journal entries / account tags, not here.

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- Data engine: `l10n_bg_reports_audit`
- `readme/DESCRIPTION.md` / `readme/USAGE.md` — source notes
