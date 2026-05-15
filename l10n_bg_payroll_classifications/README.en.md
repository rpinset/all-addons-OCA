# Bulgaria — Payroll Classifications (НКПД + КИД) (OCA)

> The two official Bulgarian taxonomies payroll depends on: НКПД-2011
> occupational codes (required on Declaration 1) and КИД economic
> activities (which drive the МОД insurance floor and ТЗПБ rate).

**Module:** `l10n_bg_payroll_classifications` | **Version:** 18.0.5.0.2 | **License:** LGPL-3 | **Category:** Human Resources/Localization

## Overview

Bulgarian payroll cannot compute social-security correctly without two
state classifiers:

- **НКПД-2011** (Национална класификация на професиите и длъжностите)
  — the 8-digit occupational code that must appear on every employee's
  Declaration 1 (Декларация Образец 1).
- **КИД** (Класификация на икономическите дейности) — the economic
  activity that determines the **МОД** (minimum insurance income) floor
  for the position and the **ТЗПБ** (work-accident) contribution rate.

This module ships both as hierarchical reference data so the payroll
modules can reference real codes instead of free text.

## Data model

### `bg.hr.payroll.ncop.classification` (new)

НКПД-2011 occupational catalogue. `code` (8-digit, indexed) + `name`
(translatable) + `parent_id`/`child_ids` tree (class → group → unit →
position). Displays as `[code] name`.

### `bg.hr.payroll.economic.activity` (new)

КИД economic-activity catalogue used for МОД. `code` (КИД code,
indexed) + `name` (translatable) + `level` selection + `parent_id`/
`child_ids` tree. Displays as `[code] name`.

### `hr.job` (extended)

Links a job position to its НКПД code, so an employee's contract
inherits the correct occupational classification for declarations
(`views/hr_job_views.xml`, menus in `views/hr_menus.xml`).

## Seeded data

The full official hierarchies, each split into per-level CSVs:

- `data/bg_hr_payroll_economic_activity/` — `parent` / `div` / `grp` /
  `cls` КИД levels.
- `data/bg_hr_payroll_ncop_classification/` — `major` / `sub_major` /
  `minor` / `unit` / `occupation` НКПД levels.

## Dependencies

| Odoo core | Bulgarian-localization |
|---|---|
| `base`, `hr` | — |

## Configuration

Install — both catalogues load automatically. Assign the НКПД code on
job positions; set the company/contract КИД activity so payroll picks
the right МОД floor and ТЗПБ band.

## Downstream consumers

`l10n_bg_hr_payroll` (МОД floor + ТЗПБ rate from КИД; НКПД on payslip),
`l10n_bg_api_nra_dec1` / `l10n_bg_hr_payroll_nra_dec1` (НКПД code on
Declaration 1), `l10n_bg_self_insured` (economic activity for the
self-insured ТЗПБ band).

## Known limitations

- Classifications are static reference data; when НСИ revises НКПД/КИД
  the seed files must be refreshed via a module upgrade.

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- Payroll consumer: `l10n-bulgaria-ee/l10n_bg_hr_payroll`
