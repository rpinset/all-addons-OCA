# Bulgaria — MT940 Bank-Statement Import (OCA)

> Adds the SWIFT **MT940** statement format to the OCA bank-statement
> import framework, with the `:28C:` StatementNumber pattern relaxed to
> accept Bulgarian-bank exports.

**Module:** `l10n_bg_account_statement_import_mt940` | **Version:** 18.0.1.0.0 | **License:** LGPL-3 | **Category:** Localization

## Overview

Most Bulgarian banks export account statements in **MT940** (SWIFT).
The OCA `account_statement_import_file` framework doesn't ship MT940 by
default, and the standard `mt-940` Python library's `StatementNumber`
regex is stricter than what some Bulgarian banks emit. This module
registers the format and patches the pattern so those exports parse
cleanly.

## What it does

- `account.journal._get_bank_statements_available_import_formats()`
  extended (`models/account_journal.py`) — appends `"mt940"` to the
  list of supported import formats.
- A wizard binding (`wizard/account_statement_import.xml`) plugs the
  MT940 parser into the OCA `account.statement.import` flow.
- The `mt940.tags.StatementNumber.pattern` is overridden with a
  relaxed regex so the `:28C:` field from Bulgarian banks is accepted
  (validated by the standalone parser test in `tests/`).

## Dependencies

| OCA core | External Python |
|---|---|
| `account_statement_import_file` | `mt-940` |

> Note: the manifest declares the `mt-940` PyPI package
> (`pip install mt-940`); the import name is `mt940`.

## Configuration

1. Install (`pip install mt-940` if not already present).
2. Accounting → Import a bank statement → choose the **MT940** format
   → upload the bank's `.940` / `.sta` file.

## Note vs InfoPay

For Borica InfoPay banks, prefer the live API (`l10n_bg_infopay` +
bridges) over MT940 file import. MT940 is the fallback for banks
without an InfoPay channel.

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- OCA import base: `account_statement_import_file`
- Live alternative: `l10n_bg_infopay`
