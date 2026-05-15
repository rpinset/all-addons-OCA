# Markdown Viewer (Locale-aware) (OCA)

> Renders localized Markdown files (`README.bg.md` vs `README.en.md` /
> `README.md`) based on the user's language — used to show the right
> per-module documentation inside Odoo.

**Module:** `markdown_viewer_locale` | **Version:** 18.0.3.0.4 | **License:** LGPL-3 | **Category:** Tools

## Overview

Every localization module ships `README.en.md` + `README.bg.md` (and
some `README.md`). This utility picks and renders the variant matching
the logged-in user's language, so a Bulgarian user sees the Bulgarian
documentation and an English user sees English — inside the Odoo UI,
not just on GitHub.

## What it does

A backend asset bundle ships a bundled `marked` (Markdown) + `highlight.js`
(syntax highlighting) and a small registry/popup. A `FormController`
patch adds a doc button that opens the locale-appropriate Markdown
file (`*.bg.md` for `bg_BG`, falling back to `*.en.md` / `*.md`) in a
popup, rendered to HTML in the browser.

## Assets

| File | Role |
|---|---|
| `static/src/lib/marked.min.js` | Markdown → HTML |
| `static/src/lib/highlight.min.js` | code-block highlighting |
| `static/src/js/markdown_registry.js` | registry of doc sources |
| `static/src/js/markdown_popup.js` | popup controller (after `form_controller.js`) |
| `static/src/xml/form_controller.xml` | doc button injected into the form controller |
| `static/src/css/markdown_popup.css` | popup styling |

## Dependencies

| Odoo core | Bulgarian-localization |
|---|---|
| `web` | (utility — used across the localization) |

No external Python packages (the Markdown/highlight libs are vendored
JS).

## Configuration

None. Install — localized README rendering follows the user language.

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- Documents every module's `README.en.md` / `README.bg.md`
