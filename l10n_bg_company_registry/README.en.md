# Bulgaria — Trade Registry Integration (OCA)

> Real-time partner enrichment from the official Bulgarian Trade
> Registry (portal.registryagency.bg): fetch and populate company data
> by EIK with one click.

**Module:** `l10n_bg_company_registry` | **Version:** 18.0.2.0.1 | **License:** LGPL-3 | **Category:** Localization

## Overview

Manually re-typing a Bulgarian counterparty's legal data (exact name,
structured address, legal form, NACE/КИД activity, court of
registration, managers) is error-prone and goes stale. This module
queries the official Trade Registry API live, parses the response and
writes the data straight onto `res.partner` — no offline database to
maintain, always fresh data.

## Architecture

### `res.partner` (extended — `models/res_partner.py`)

New fields populated from the registry:

| Field | Meaning |
|---|---|
| `l10n_bg_legal_form` | ООД / ЕООД / АД / ЕТ … |
| `l10n_bg_registration_date` | Registration date |
| `l10n_bg_registration_court` | Court of registration |
| `l10n_bg_activity_code` | NACE/КИД economic-activity code |
| `l10n_bg_activity_description` | Activity description |

`action_fetch_from_registry()` — extracts the EIK from the partner's
VAT (`BG…` stripped), calls the registry and fills the partner. Smart
address parsing handles Bulgarian formats: ул./бул., ж.к., к.к., м.,
кв., р-н, plus email/phone extraction from free-text addresses.

### `bg.company.search.wizard` (`wizard/`)

Search-by-EIK wizard: returns the registry result in preview fields
(`display_name_bg` / `display_name_en`, `display_legal_form_bg`,
`display_vat`, `display_address_bg`, `display_country_id`,
`display_state_id`, `display_city_id` → `res.city`,
`display_postal_code`) so the user reviews before applying it to the
partner.

### `data/ir_actions_server.xml`

`action_populate_bg_registry_data` — a contextual `res.partner` server
action ("Populate BG Registry Data") so the fetch can be triggered from
the partner list/form action menu.

## Dependencies

| Odoo core | Bulgarian-localization | External Python |
|---|---|---|
| `base`, `contacts` | `l10n_bg_config`, `l10n_bg_city` | `requests` |

`l10n_bg_city` provides the ЕКАТТЕ settlement the parsed address links
to (`res.city`).

## Configuration

Install. Open a partner with a Bulgarian VAT/EIK → run **Populate BG
Registry Data** (or use the search wizard). The structured address
binds to the `l10n_bg_city` settlement database.

## Known limitations

- Depends on portal.registryagency.bg availability and response
  format; a major registry API change needs a parser update.
- Address parsing is heuristic for free-text Bulgarian address strings
  — verify the parsed city/street after fetch for unusual formats.

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- Settlement source: `l10n_bg_city`
- `readme/DESCRIPTION.md` / `readme/CHANGELOG.md` — source notes
