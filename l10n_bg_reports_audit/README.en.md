# Bulgaria — Accounting Reports Base (OCA)

> The technical base for Bulgarian accounting/tax reporting: the SQL
> view models behind the VAT declaration, sales/purchase ledgers and
> VIES, plus the NRA account-tag configuration. No UI of its own — the
> data engine the report modules build on.

**Module:** `l10n_bg_reports_audit` | **Version:** 18.0.12.0.3 | **License:** LGPL-3 | **Category:** Accounting/Localizations/Reporting

## Overview

Bulgarian VAT reporting (ДДС декларация, дневник на продажбите/покупките,
VIES) is computed from journal entries tagged against the NRA cell
codes. Doing this in Python per report would be slow and inconsistent.
This module supplies it as a layer of **PostgreSQL view models** that
build their SQL dynamically (`_select()` / `_from()` / `_where()` /
`_group()`), so every report reads the same authoritative figures. It
ships no menus or forms — `l10n_bg_reports_config` (sibling) provides
the UI.

## SQL view models (`report/`, `_auto=False`)

### VAT declaration chain

| Model | Role |
|---|---|
| `account.bg.vat.calc.declar` | Detailed VAT calculation per line (cells 10-82) |
| `account.bg.vat.info.declar` | Aggregated VAT declaration per company/period |
| `account.bg.vat.result.declar` | Settlement: tag_50 (pay), tag_60 (refund), 70-82 (Art. 92) |

### Sales / purchases ledgers

`account.bg.info.sale.line` / `account.bg.calc.sales.line` /
`account.bg.total.sales.line` and the purchases triple
(`account.bg.info.purchases.line` / `.calc.purchases.line` /
`.total.purchases.line`) — the дневник на продажбите / покупките lines
with the NRA `info_tag_*` / `account_tag_*` columns. The `calc`
variants are persistent PG views built with a custom `init()` (need a
module `-u` after a query change); the `info` variants are dynamic
`_table_query` (a restart suffices).

### VIES

`account.bg.calc.vies.line` (intra-EU supplies per partner — goods /
triangular / services), `account.bg.vies.info.declar`,
`account.bg.vies.total.declar`.

### Trail balance

`account.bg.calc.partner.line` (partner receivable/payable with a
recursive CTE: initial → movement → final), `account.bg.calc.product.line`.

## Extended models

| Model | Addition |
|---|---|
| `account.account.tag` | `+ l10n.bg.config.mixin`; the NRA cell-tag base |
| `account.move` / `account.move.line` | reporting metadata used by the views |
| `account.journal` | journal classification for ledgers |
| `res.company` | `l10n_bg_vat_ratio` (Art. 73 §2), Intrastat-threshold + VAT-ratio history links, audit config flags |
| `res.company.history.vat` (`l10n.bg.vat.ratio.history`) | VAT-ratio history (mail.thread) |
| `res.company.history.intrastat` (`l10n.bg.intrastat.threshold`) | Intrastat-threshold history |
| `res.partner` / products | reporting helpers (`report/account_bg_partner.py`, `account_bg_products.py`) |
| `ir.actions.report` / `res.config.settings` | report + settings hooks |

`l10n_bg_file_helper` packages report files for NRA export.

## Dependencies

| Odoo core | Bulgarian-localization |
|---|---|
| `base`, `account` | `l10n_bg`, `l10n_bg_ledger`, `l10n_bg_config` |

## Configuration

Install (pulled automatically by `l10n_bg_config`). It exposes no UI on
its own — install `l10n_bg_reports_config` for the views, menus and the
account-tag bulk-edit wizard. Tag the chart of accounts against the NRA
cells; the view models then compute the declarations.

## Restart vs upgrade (operational note)

After editing a `*.info.*` query (dynamic `_table_query`) a server
**restart** is enough. After editing a `*.calc.*` / `*.total.*` /
`*.declar` persistent PG view (custom `init()`), a module **`-u`** (or
a manual `DROP VIEW` + recreate) is required.

## Downstream consumers

`l10n_bg_reports_config` (UI), `l10n_bg_vat_reports` /
`l10n_bg_tax_admin` and the NRA submission modules read these views.

## Known limitations

- View models are read-only; corrections are made on the underlying
  journal entries / account tags, not the report rows.
- The dual `init()` vs `_table_query` semantics mean a query change can
  silently not take effect without the right reload (see note above).

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- UI sibling: `l10n_bg_reports_config`
- `readme/` — DESCRIPTION / CONTEXT / CONFIGURE / USAGE source notes
