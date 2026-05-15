# Bulgaria — HR Holidays (Labor-Code leave types) (OCA)

> The Bulgarian leave-type catalogue per the Labor Code (КТ) and NHIF
> (НЗОК): annual paid leave, sick leave, maternity/paternity,
> educational, civic-duty — with NSSI reason codes and employer-paid-day
> handling.

**Module:** `l10n_bg_hr_holidays` | **Version:** 18.0.1.0.4 | **License:** LGPL-3 | **Category:** Human Resources/Time Off

## Overview

Odoo ships a generic time-off model; Bulgarian payroll needs the
statutory leave types with their legal codes, the NHIF sick-leave
reason codes, and correct handling of employer-paid days within a leave.
This module supplies that as the data + model layer the payroll modules
consume.

## Data model

### `hr.leave.type` (extended — `models/hr_leave_type.py`)

| Field | Purpose |
|---|---|
| `l10n_bg_code` | Statutory code (e.g. `155` paid annual, `163` maternity). Drives the `[code] name` display and downstream filtering |
| `l10n_bg_allow_paid_days` | Computed — true for `time_type == "leave"` types where employer-paid days apply |
| `l10n_bg_paid_days_unpaid_leave` | Configured paid-days threshold for an otherwise-unpaid leave |
| `l10n_bg_leave_reason_id` | M2O → `nssi.leave.reason` |

### `nssi.leave.reason` (new — `models/`)

The NHIF/НЗОК sick-leave reason codes — `code` (2-char, indexed) +
`name` (translatable), display `[code] name`. Seeded from
`data/nssi.leave.reason.csv`. Used to classify sick leaves for NSSI
certificate generation.

### `hr.leave` (extended — `models/hr_leave.py`)

`l10n_bg_leave_reason_id` (related from the leave type),
`l10n_bg_show_paid_days_fields`, `l10n_bg_paid_days_unpaid_leave` and
`l10n_bg_effective_unpaid_days` — surface the reason code and compute
how many days of an unpaid leave are still employer-paid, when the
type allows it.

## Seeded data

- `data/hr_holidays_data.xml` — the Bulgarian leave types with their
  КТ / NHIF codes.
- `data/nssi.leave.reason.csv` — NHIF reason codes.

## Views

`views/hr_leave_type_views.xml` (code + reason + paid-days on the
type), `views/hr_leave_views.xml` (reason + paid-days on the request),
`views/l10n_bg_nssi_leave_reason.xml` (reason-code maintenance).

## Relationship to payroll

`l10n_bg_hr_payroll_holidays` (EE) builds on this: it auto-creates
NSSI sick certificates on approval and feeds the maternity / sick-leave
treatment into `l10n_bg_hr_payroll`. The leave codes set here are the
join key.

## Dependencies

| Odoo core | Bulgarian-localization |
|---|---|
| `hr_contract`, `hr_holidays` | `l10n_bg` |

## Configuration

1. Install → leave types + NHIF reason codes load automatically.
2. HR → Configuration → Time Off Types: review codes / paid-day rules.
3. Create allocations for annual-leave types.

## Known limitations

- The OCA build is the core leave-type + reason-code catalogue; the
  read-only `hr.leave.balance` SQL view, pro-rata allocation helper and
  Annual Leave Schedule planner are part of the l10n-bulgaria CE build,
  not this module.

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- Payroll consumer: `l10n-bulgaria-ee/l10n_bg_hr_payroll_holidays`
- `readme/DESCRIPTION.md` — source notes
