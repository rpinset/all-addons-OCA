# Partner Multilang — Transliteration & Multilingual Names (OCA)

> Automatic Cyrillic→Latin transliteration (ISO 9 / ΕΛΟΤ 743), language
> detection, multi-language partner search and correct sorting — the
> infrastructure that makes Bulgarian partner data legally compliant
> and usable in mixed-script databases.

**Module:** `partner_multilang` | **Version:** 18.0.3.0.4 | **License:** LGPL-3 | **Category:** Localization

## Overview

Cyrillic-script countries (Bulgaria, Russia, Serbia, Macedonia,
Ukraine, Belarus) legally require a Latin transliteration of names on
official documents. Mixed Cyrillic/Latin data also sorts incorrectly
in Odoo list/kanban views. This module solves both: it transliterates
automatically, stores every translation, searches across all of them,
and sorts by the user's language.

## Architecture

### `res.transliterate.mixin` (new AbstractModel — `models/res_transliterate.py`)

The reusable engine. Any model that inherits it gets a multilingual
`display_name`: `_compute_display_name()` returns the value in the
user's language, transliterating on the fly when needed, and tracks
which fields were auto-transliterated so manual edits aren't
overwritten.

### Language detection (two-tier)

- **Priority 1:** `lingua` (`LanguageDetectorBuilder`) — accurate.
- **Priority 2:** `langdetect` — fast fallback.

Non-English names are transliterated (ISO 9 for Cyrillic, ΕΛΟΤ 743 for
Greek) via the `transliterate` + `unidecode` libraries.

### `res.partner` (extended — `models/res_partner.py`)

- `name` (trigram-indexed), `street`, `street2`, `city`, `function`,
  `company_name`, `commercial_company_name` made `translate=True`.
- `complete_name_multilanguage` — a computed translatable field backed
  by a **JSONB column** added via raw SQL `ADD COLUMN IF NOT EXISTS`
  in `init()`, so the technical column materializes **without a module
  upgrade**.
- `_rec_names_search` extended to include
  `complete_name_multilanguage` — search matches any stored
  translation, not just the active language. A `get_view` hook rewrites
  `complete_name` field nodes to the multilingual field.

### Other extensions

| Model | Why |
|---|---|
| `ir.binary` | `download_name` handling for translated JSONB names (avoids broken filenames) |
| `res.country` / `res.country.state` | translatable name hooks |
| `res.lang` | sort/collation hooks (`views/res_lang_views.xml`) |
| `res.company` / `res.config.settings` | `transliterate_names` company toggle (`views/res_config_settings_view.xml`) |

`pre_init_hook` / `post_init_hook` / `uninstall_hook` manage the JSONB
column lifecycle.

## Dependencies

| Odoo core | Bulgarian-localization | External Python |
|---|---|---|
| `base`, `contacts` | — (foundational) | `transliterate`, `unidecode`, `lingua` |

## Configuration

1. Install.
2. Settings → enable **Transliterate Names** (per company).
3. Existing partners transliterate on next write; new partners on
   create. The JSONB column appears automatically — no `-u` needed.

## JSONB caveat for downstream modules

Because translated names live in PostgreSQL **JSONB** columns, any
module doing `regexp_matches` / raw SQL on partner names must handle
the JSONB shape. This is a recurring gotcha — see
`l10n_bg_account_reconcile_patch`, which exists precisely to fix
JSONB-name handling in the OCA reconcile engine.

## Downstream consumers

`l10n_bg_multilang`, `l10n_bg_mrp_multilang`,
`l10n_bg_project_multilang`, and effectively every report that prints
partner names bilingually.

## Known limitations

- Transliteration is rule-based (ISO 9 / ΕΛΟΤ 743); proper names with
  non-standard romanization need a manual override.
- Language detection on very short strings (1-2 chars) is unreliable —
  falls back to the active language.

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- JSONB-fix consumer: `l10n_bg_account_reconcile_patch`
- `readme/DESCRIPTION.md` / `readme/USAGE.md` — source notes
