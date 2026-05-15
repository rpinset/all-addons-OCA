# Markdown Viewer (Locale-aware) (OCA)

> Рендира локализирани Markdown файлове (`README.bg.md` vs
> `README.en.md` / `README.md`) спрямо езика на потребителя — ползва
> се за показване на правилната per-module документация вътре в Odoo.

**Модул:** `markdown_viewer_locale` | **Версия:** 18.0.3.0.4 | **Лиценз:** LGPL-3 | **Категория:** Tools

## Описание

Всеки локализационен модул доставя `README.en.md` + `README.bg.md` (и
някои `README.md`). Този инструмент избира и рендира варианта,
съответстващ на езика на логнатия потребител, така че български
потребител вижда българската документация, а английски — английската
— вътре в Odoo UI, не само на GitHub.

## Какво прави

Backend asset bundle доставя bundled `marked` (Markdown) +
`highlight.js` (syntax highlighting) и малък registry/popup.
`FormController` patch добавя doc бутон, който отваря
locale-съответстващия Markdown файл (`*.bg.md` за `bg_BG`, fallback
към `*.en.md` / `*.md`) в popup, рендиран до HTML в браузъра.

## Assets

| Файл | Роля |
|---|---|
| `static/src/lib/marked.min.js` | Markdown → HTML |
| `static/src/lib/highlight.min.js` | подсветка на код блокове |
| `static/src/js/markdown_registry.js` | registry на doc източници |
| `static/src/js/markdown_popup.js` | popup контролер (след `form_controller.js`) |
| `static/src/xml/form_controller.xml` | doc бутон в form контролера |
| `static/src/css/markdown_popup.css` | стилизиране на popup |

## Зависимости

| Odoo базови | Българска локализация |
|---|---|
| `web` | (инструмент — ползва се в цялата локализация) |

Без външни Python пакети (Markdown/highlight либовете са vendored JS).

## Конфигурация

Няма. Инсталирайте — локализираното README рендиране следва езика на
потребителя.

## Свързани

- Преглед на репозиторията: [`../OVERVIEW.bg.md`](../OVERVIEW.bg.md)
- Документира `README.en.md` / `README.bg.md` на всеки модул
