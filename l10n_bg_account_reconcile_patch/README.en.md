# Bulgaria — Account Reconcile JSONB-Name Fix (OCA)

> Patches OCA bank-statement reconciliation so partner matching works
> when partner names are stored as translatable JSONB (the
> `partner_multilang` side-effect).

**Module:** `l10n_bg_account_reconcile_patch` | **Version:** 18.0.1.0.0 | **License:** LGPL-3 | **Category:** Localization

## Overview

When `partner_multilang` makes `res.partner.name` a translatable
**JSONB** column, the OCA reconciliation engine's partner-matching runs
`regexp_matches(...)` against the raw JSONB and fails to find the
partner. This module monkey-patches the matching logic to resolve the
JSONB name first, so auto-reconciliation keeps working in a
multilingual database.

This is the **OCA-stack variant**: it patches
`account.bank.statement.line` matching as wired by
`account_reconcile_model_oca`, not the Enterprise `account_accountant`
reconcile widget.

## What it does

Via a `post_load_hook` (monkey-patch in `hooks.py`, no model changes):

- `_retrieve_partner_patch` — replaces `AccountBankStatementLineBase
  ._retrieve_partner`; the SQL `regexp_matches(...)` now operates on
  the resolved name text instead of the JSONB blob.
- `_get_st_line_strings_for_matching(allowed_fields=None)` — adjusted
  so statement-line strings compare against the proper name
  representation.

The hook is registered through the manifest's `post_load`
(`post_load_hook`) so it activates without an explicit model upgrade.

## Dependencies

| Odoo core / OCA | Bulgarian-localization |
|---|---|
| `account_reconcile_model_oca` | effective with `partner_multilang` |

No external Python packages.

## Configuration

None. Install — OCA reconciliation partner matching tolerates JSONB
names.

## Related JSONB-fix modules

Companion to the org-chart / multilang JSONB-name fixes. Root cause is
documented in `partner_multilang` (translated names are PostgreSQL
JSONB columns; any raw SQL on `res.partner.name` must handle that
shape).

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- Root cause: `partner_multilang`
- OCA reconcile base: `account_reconcile_model_oca`
