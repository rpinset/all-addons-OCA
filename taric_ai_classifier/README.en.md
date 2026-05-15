# Bulgaria — AI TARIC & INTRASTAT Classifier (OCA)

> Claude-AI-powered automatic TARIC / INTRASTAT commodity-code
> classification for products: describe the product, get ranked code
> suggestions with reasoning, apply with one click — single or batch.

**Module:** `taric_ai_classifier` | **Version:** 18.0.1.0.3 | **License:** LGPL-3 | **Category:** Accounting/Localizations

> A curated `README.md` (bilingual, vendor-maintained) exists for this
> module — this file is the developer-handbook companion.

## Overview

Assigning the correct 8-10 digit TARIC / CN code to every product is
tedious and error-prone, yet customs declarations and Intrastat depend
on it. This module sends the product description to the **Anthropic
Claude API**, parses the model's ranked suggestions (code + EN/BG
description + supplementary unit + reasoning + confidence) and lets the
user accept one — for a single product or a whole batch.

## Data model

### `taric.code` (new — `models/taric_code.py`)

The local catalogue of TARIC/CN codes. `_rec_names_search = ["code",
"description"]`, computed `display_name` = `"<code> - <description>"`.
Methods: `action_view_products()`, `action_verify_code()` (validates a
code against the external source via `requests`), plus the AI call to
`https://api.anthropic.com/v1/messages`
(`model="claude-sonnet-4-20250514"`).

### `taric.classification.history` (new)

Audit log of every classification: the product, the chosen code, the
`ai_model` used, timestamp — so a classification decision is traceable.

### `product.template` (extended — `models/product.py`)

`action_classify_with_ai()` (builds the prompt from name + category +
description and calls the AI), `action_verify_taric_code()`,
`action_view_classification_history()`.

### `res.config.settings` (extended)

| Setting | `ir.config_parameter` |
|---|---|
| `anthropic_api_key` | `taric_ai.anthropic_api_key` |
| `auto_classify_enabled` | auto-classify on product create |
| `auto_apply_high_confidence` | auto-apply when confidence is high |

## Wizards (`wizard/`)

| Model | Role |
|---|---|
| `taric.classify.wizard` (+ `.suggestion`) | single-product: shows ranked `taric.classify.suggestion` rows (code, description_en/bg, supplementary_unit, reasoning); `action_apply_classification()` writes the chosen code + a history row |
| `batch.classify.wizard` (+ `.result`) | many products at once: filter unclassified / by category, optional auto-apply of high-confidence results, status feedback |

## Dependencies

| Odoo core | Bulgarian-localization | External Python |
|---|---|---|
| `base`, `product`, `stock`, `stock_delivery`, `account` | — | `requests` |

## Configuration

1. Settings → set the **Anthropic API key** (stored as
   `ir.config_parameter` `taric_ai.anthropic_api_key`).
2. (Optional) enable auto-classify on create and auto-apply for
   high-confidence results.
3. From a product → **Classify with AI**, or run the batch wizard
   over a filtered product set.

## Relationship to `l10n_bg_tariff_code`

`l10n_bg_tariff_code` is the customs-rate cache + TARIC/CN fields on
products; this module is the AI front-end that *fills* those codes.
Use them together: AI proposes the code, `l10n_bg_tariff_code` resolves
the duty rate.

## Known limitations

- Requires an Anthropic API key and outbound HTTPS; AI suggestions
  must still be reviewed for customs-critical products.
- Suggestion quality depends on how descriptive the product data is.

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- Companion: `l10n_bg_tariff_code`
- Curated overview: `README.md`
