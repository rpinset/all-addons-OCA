# Bulgaria Localization — Configuration Backbone (OCA)

> The foundation module of the Bulgarian localization. Pulls the core
> stack, hides BG-specific UI for non-BG companies, validates
> identifiers, and derives encrypted API credentials.

**Module:** `l10n_bg_config` | **Version:** 18.0.8.0.5 | **License:** LGPL-3 | **Category:** Localization

## Overview

`l10n_bg_config` is the keystone every other Bulgarian-localization
module depends on. It has three jobs:

1. **One-shot localization setup.** It auto-installs with `l10n_bg`
   (`auto_install: ["l10n_bg"]`) and depends on `l10n_bg_ledger` +
   `l10n_bg_tariff_code`, so a fresh database becomes Bulgaria-ready
   without hunting for dependencies. `pre_init_hook` / `post_init_hook`
   wire the chart-of-accounts templates (`data/template/`).
2. **Multi-company UI discipline.** In a database that mixes Bulgarian
   and non-Bulgarian companies, BG-specific fields and groups would
   clutter every form for the non-BG entities. This module's mixin
   strips them out automatically per active company.
3. **Credential derivation.** API keys for the NRA integrations are
   never validated against a stored plaintext — the module ships the
   XOR-based key derivation used across the localization.

## Architecture

### `l10n.bg.config.mixin` (AbstractModel)

The heart of the module (`models/l10n_bg_config_mixin.py`). Any model
that inherits it gains:

- `is_l10n_bg_record` — computed boolean, true when the record's
  company (or the active company) is flagged as Bulgarian via
  `res.company._check_is_l10n_bg_record()`.
- An overridden `get_view()` that, for **non-BG companies**, rewrites
  the returned arch to set `column_invisible` / `invisible` on every
  `l10n_bg_*` field and any `l10n_bg`-named group, and hide search
  filters referencing `l10n_bg`. A localization module can therefore
  add `l10n_bg_*` fields freely — they vanish for companies that don't
  need them, with no manual `invisible` attributes.

### Extended core models

| Model | Why it's extended |
|---|---|
| `res.company` | `_check_is_l10n_bg_record()` gate; chart-template binding; BG API key storage |
| `res.partner` | BG UIC (БУЛСТАТ/ЕИК), `generate_encryption_keys(...)` crypt key |
| `account.move` / `account.move.line` | inherit the mixin → auto-hide BG fields for non-BG companies |
| `account.chart.template` | BG chart-of-accounts hook points |
| `account.account.tag` | NRA cell tagging base |
| `res.country` | translatable state/region support hooks |
| `ir.module.module` | install-orchestration helpers |

### Credential security helpers

`models/l10n_bg_config_mixin.py` provides:

- `generate_encryption_keys(key1, key2)` / `decrypt_key(encrypted,
  key1, key2)` — XOR-based key derivation.
- `is_valid_api_key(uic, api_key, crypt_key)` — validates the NRA
  submission credential triple without a direct equality check.
- `prepare_zip_payload(files_report, company)` — wraps NRA report
  files; injects a random one-time password when the company's API-key
  triple is invalid, so exports degrade safely instead of leaking.

> The OCA build derives/validates credentials only; the Fernet-encrypted
> company-blacklist controller + OWL service of the l10n-bulgaria CE
> build is **not** part of this module.

## Wizards

| Wizard | Purpose |
|---|---|
| `account_account_tag_bulk_edit_wizard` | bulk-tag accounts for NRA cells |
| `account_settings_preview_xml_file` | preview a generated settings XML |
| `account_chart_template_plugins` | enable/disable chart-template plugins |

## Seeded data

`data/res_lang_data.xml` (BG language config) + `data/template/`
chart-of-accounts CSVs (`account.account-bg.csv`,
`account.group-bg.csv`, `account.tax-bg.csv`).

## Dependencies

| Odoo core | Bulgarian-localization | External Python |
|---|---|---|
| `base`, `account`, `base_vat` | `l10n_bg`, `l10n_bg_ledger`, `l10n_bg_tariff_code` | `xmltodict` |

## Configuration

1. Apps → install **l10n_bg_config** (dependencies auto-install).
2. Settings → Localization → review enabled modules + chart template.
3. Set the company's БУЛСТАТ/ЕИК and NRA API credentials on the company
   partner; the module derives and stores the encrypted crypt key.

## Field-naming convention enforced ecosystem-wide

Any field a localization module adds to an Odoo core model
(`account.move`, `res.partner`, `res.company`, `pos.*`, …) **must** be
prefixed `l10n_bg_`. The mixin's view rewriting depends on this prefix
to find and hide fields — non-prefixed fields will leak into non-BG
company forms.

## Known limitations

- `get_view` arch rewriting is per-call; very large views add minor
  parse overhead for non-BG companies.

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- `readme/` — DESCRIPTION / CONTEXT / CONFIGURE source notes
- Downstream consumers: virtually every `l10n_bg_*` module
