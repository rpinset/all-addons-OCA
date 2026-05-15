# Bulgaria — Tax / Social-Security Office Directory (OCA)

> Preloaded `res.partner` directory of NRA territorial offices (and
> related authorities) — so documents and partners can reference the
> correct tax authority.

**Module:** `l10n_bg_tax_offices` | **Version:** 18.0.1.0.0 | **License:** LGPL-3 | **Category:** Localization

## Overview

Bulgarian businesses correspond with the **NRA** (НАП — taxes) by
region: a central office, executive director, Territorial Directorates
(ТД) and oblast offices. This module ships that directory as
`res.partner` records in a parent → office hierarchy so a company can
be linked to the right office for reporting and document automation.

## Data

### `data/res_tax_offices.xml` — NRA / НАП

`res.partner` records (`noupdate="0"`): the National Revenue Agency
central record, the executive director, the central office, the
Territorial Directorates and their oblast offices — each parented to
its ТД, carrying address, phone, email, VAT and `city_id` linking to
the `l10n_bg_city` ЕКАТТЕ settlement.

### `data/res_tax_offices_pre_functions.xml` / `_post_functions.xml`

`ir.actions.server` records that run before/after the directory load —
they reconcile/clean the office partners on (re)install so the
hierarchy stays consistent.

## Dependencies

| Odoo core | Bulgarian-localization |
|---|---|
| (contacts base) | `l10n_bg`, `l10n_bg_city` |

`l10n_bg_city` provides the settlement records the offices reference
(`city_id`, `l10n_bg_has_tax_office`).

## Configuration

Install — the directory loads as partners (hierarchical: NRA →
TD → oblast office). Link a company's tax office on its partner for
report/automation use.

## Maintenance

Contact data drifts (directors change, offices relocate). The data is
`noupdate="0"` — a module upgrade re-applies the XML, so refresh by
editing the data file and bumping the version; manual edits to these
partners are overwritten on `-u`.

## Known limitations

- `noupdate="0"` data — a module upgrade re-applies the XML; manual
  edits to these partners are overwritten on `-u`.

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- Settlement source: `l10n_bg_city`
- `readme/DESCRIPTION.md` — source notes
