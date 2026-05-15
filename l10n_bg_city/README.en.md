# Bulgaria — Cities & ЕКАТТЕ Geographic Database (OCA)

> The authoritative Bulgarian settlement database: 28 regions, 265
> municipalities, ~3000 city halls, 5000+ settlements — all carrying
> their official ЕКАТТЕ codes.

**Module:** `l10n_bg_city` | **Version:** 18.0.1.0.0 | **License:** LGPL-3 | **Category:** Localization

## Overview

Bulgarian official documents, NRA declarations, Intrastat filings and
NSI statistical reports all require the **ЕКАТТЕ** code (Единен
класификатор на административно-териториалните и териториалните
единици — the national settlement classifier). This module preloads
the full hierarchy so addresses are picked from a standardized list
rather than typed free-form, eliminating the typos that break legal
filings.

## Data model

### `res.city.types` (new — via `data/res_city_types.xml`)

Settlement-type taxonomy: град (city), село (village), градче, квартал,
манастир (monastery), жп гара (railway station), … Each row carries a
`code` and a translatable `name`.

### `res.city` (extended — `models/res_city.py`)

| Field | Meaning |
|---|---|
| `l10n_bg_ecattu` | The 5-digit ЕКАТТЕ code — the join key for all official reporting |
| `l10n_bg_type_settlement_id` | M2O → `res.city.types` |
| `l10n_bg_city_hall_id` / `l10n_bg_city_hall_code` | Parent кметство |
| `l10n_bg_municipality_id` | Parent община |
| `l10n_bg_has_tax_office` | Marks settlements hosting an NRA office (consumed by `l10n_bg_tax_offices`) |
| `l10n_bg_structure_type` | `normal` / `cityhall` / `municipality` — drives the three-level hierarchy + domain filtering |

The hierarchy is **Settlement → City Hall → Municipality → Region**,
with smart domains preventing circular references and scoping
selection lists by country + structure type.

### `res.country.state` (extended — `models/res_country.py`)

`name` made translatable — full support for the 28 Bulgarian области
in both Bulgarian and English.

## Data loading

`post_init_hook` bulk-imports four CSVs shipped with the module:

- `res.country.state.csv` — 28 regions
- `res.city.municipality.csv` — 265 municipalities
- `res.city.cityhall.csv` — city halls
- `res.city.csv` — 5000+ settlements

Plus `res_city_types.xml` (taxonomy) and `res_country_data.xml`. The
`data/src` directory carries the raw source/derivation files.

> The OCA build is the **static dataset variant**: it ships the full
> ЕКАТТЕ hierarchy as data with a one-time post-init load. (The
> l10n-bulgaria CE build additionally carries a quarterly НСИ
> `l10n.bg.ekatte.sync` cron; that auto-sync model is not part of this
> OCA module — refresh here is by upgrading the data files.)

## Dependencies

| Odoo core | Bulgarian-localization |
|---|---|
| `base_address_extended`, `contacts` | — (foundational; sits low) |

## Configuration

Install — `post_init_hook` loads the full dataset (one-time, sizeable
on first install). No further configuration.

## Downstream consumers

`l10n_bg_tax_offices` (office settlement marking),
`l10n_bg_company_registry`, address-completion across the
localization.

## Known limitations

- Initial post-init import is sizeable; expect a one-time delay on
  first install.
- Static dataset — when НСИ revises ЕКАТТЕ the seed CSVs must be
  refreshed by a module upgrade (no auto-sync cron in the OCA build).

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- `readme/DESCRIPTION.md` / `readme/CONTEXT.md` — source notes
- Office directory consumer: `l10n_bg_tax_offices`
