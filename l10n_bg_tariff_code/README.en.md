# Bulgaria — TARIC / HS / CN Code Management (OCA)

> Customs commodity-code management for products and invoice lines,
> with a local cache of EU TARIC tariff rates pulled from the European
> CIRCABC dataset.

**Module:** `l10n_bg_tariff_code` | **Version:** 18.0.3.0.10 | **License:** LGPL-3 | **Category:** Accounting/Localizations

## Overview

Bulgarian customs declarations and Intrastat reporting require each
product to carry its **TARIC / HS / CN** commodity code, and customs
valuation needs the applicable tariff rate. Querying the EU TARIC
system on every line would be slow and rate-limited, so this module
maintains a **local rate cache** keyed by CN code + country + validity
window, refreshed from the official CIRCABC data.

## Data model

### `l10n_bg.taric.cache` (new — `models/l10n_bg_taric_cache.py`)

Local cache of TARIC tariff rates from CIRCABC. `_rec_name = "cn_code"`,
ordered by `cn_code, country_code`.

| Field | Meaning |
|---|---|
| `cn_code` | Combined Nomenclature code (rec name) |
| `country_code` | Origin country the rate applies to |
| `measure_type` | TARIC measure type (e.g. `103` = third-country duty) |
| `duty_rate` | Applicable duty |
| `valid_from` / `valid_to` | Rate validity window |

A SQL `UNIQUE(cn_code, country_code, valid_from, valid_to)` constraint
prevents duplicate overlapping rates. Lookups hit the cache first; a
miss (or stale entry past `valid_to`) triggers a refresh from the
configured TARIC API.

### Extended models

| Model | Addition |
|---|---|
| `product.template` / `product.product` | TARIC/HS/CN code fields |
| `account.move.line` | tariff code propagation for customs valuation |
| `res.company` | `l10n_bg_taric_api_url`, `l10n_bg_taric_api_enabled`, `l10n_bg_taric_cache_duration` (hours) |
| `res.config.settings` | exposes the above as settings |

## Wizard

`l10n_bg_taric_import_wizard` (`wizards/`) — bulk-imports a TARIC/CN
rate set from a CIRCABC export into `l10n_bg.taric.cache` (flexible
column mapping absorbs CIRCABC format drift).

## Seeded data

`data/l10n_bg_tarif_code_data.xml`. `pre_init_hook` prepares the
schema before first install.

## Dependencies

| Odoo core | Bulgarian-localization | External Python |
|---|---|---|
| `account`, `stock_delivery` | — | `requests` |

## Configuration

1. Settings → Bulgarian Localization → TARIC:
   - **Enable TARIC API** + **TARIC API URL** (EU endpoint).
   - **Cache Duration (hours)** — how long a cached rate is trusted.
2. Assign TARIC/CN codes on products (manually or via
   `taric_ai_classifier` for AI-assisted classification), or run the
   import wizard against a CIRCABC export.

## Downstream consumers

`taric_ai_classifier` (AI classification writes codes here),
`l10n_bg_intrastat` (commodity codes on declarations),
`l10n_bg_tax_admin` customs flows.

## Known limitations

- Cache freshness depends on `cache_duration`; a rate that changes
  mid-window is only picked up after expiry (or manual re-import).
- CIRCABC dataset structure changes occasionally — the import wizard's
  column mapping tolerates common shifts but a major EU format change
  needs a code update.

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- AI classifier: `taric_ai_classifier`
- `readme/DESCRIPTION.md` — source notes
