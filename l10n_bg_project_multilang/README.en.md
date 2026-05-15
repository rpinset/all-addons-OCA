# Bulgaria — Multilingual Project Task (OCA)

> Makes the project-task partner-name fields translatable so project
> documents render bilingually, consistent with the multilang stack.

**Module:** `l10n_bg_project_multilang` | **Version:** 18.0.1.0.0 | **License:** LGPL-3 | **Category:** Localization

## Overview

The multilang stack (`partner_multilang` / `l10n_bg_multilang`) makes
partner/employee/bank names bilingual. Project tasks also carry partner
name fields that surface on project documents — this module makes them
translatable too, so project paperwork stays consistent with Bulgarian
bilingual requirements.

## What it does

`project.task` (extended — `models/`):

| Field | Treatment |
|---|---|
| `partner_name` | `translate=True` |
| `partner_company_name` | `translate=True` |

Model-layer only — no views shipped (the manifest's `data` is empty by
design), no seeded data, no external dependencies.

## Dependencies

| Odoo core | Bulgarian-localization |
|---|---|
| `project` | `partner_multilang` |

Hard dependency on `partner_multilang` — it provides the
transliteration engine and JSONB-name infrastructure these translatable
fields rely on.

## Configuration

None. Install — the project-task partner-name fields accept
per-language values; transliteration follows the `partner_multilang`
company toggle.

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- Multilang core: `partner_multilang`, `l10n_bg_multilang`
- Sibling: `l10n_bg_mrp_multilang`
