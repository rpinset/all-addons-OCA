# България — Report Theme Sections (OCA)

> Корпоративен модулен section-based PDF report theme за български
> бизнес документи: конфигурируеми header / article / footer, две
> лога, per-section фонове, portrait + landscape.

**Модул:** `l10n_bg_report_theme` | **Версия:** 18.0.5.0.4 | **Лиценз:** LGPL-3 | **Категория:** Localization

## Описание

Българските фактури, delivery slip-ове, поръчки за доставка и
приемно-предавателни протоколи имат layout очаквания (фирмен branding
блок, легален footer, номерация на страници, място за две лога), които
стоковият Odoo report layout не покрива чисто. Този модул заменя
document layout-а с **триетажна архитектура** — Header / Article /
Footer — всяка независимо стилизирана, налична в portrait и landscape,
и управляваща всеки отчет на българската локализация.

## Архитектура

### Разширени модели (`models/`)

| Модел | Добавка |
|---|---|
| `base.document.layout` | section-based layout полета (header/article/footer стилизиране, фонове, две лога, цветове) |
| `res.company` | per-company layout конфигурация, носеща section настройките |
| `ir.actions.report` | hooks, така че отчетите се рендират през themed templates |

### Templates и assets

- `views/report_templates.xml` — section-based external layout-а
  (portrait + landscape).
- `views/report_invoice.xml`, `views/purchase_order_templates.xml`,
  `views/purchase_quotation_templates.xml` — themed document тела.
- `views/base_document_layout_views.xml` /
  `views/ir_action_report_templates.xml` /
  `views/res_company_views.xml` — конфигурационен UI.
- `data/report_layout.xml` + `data/report_paperformat_data.xml` —
  регистрира layout-а и paper формата.
- `web.report_assets_common` bundle доставя variable-font SCSS, така че
  PDF рендирането ползва правилната типография.

`webcolors` се ползва за парсване/конвертиране на конфигурираните цветове.

## Зависимости

| Odoo базови | Българска локализация | Python пакет |
|---|---|---|
| `web`, `sale`, `account`, `stock`, `purchase` | `l10n_bg_config` | `webcolors` |

## Конфигурация

1. Инсталация.
2. Settings → Companies → Document Layout: изберете българския
   section-based layout, задайте header/footer съдържание, цветове,
   лога и per-section фонове.
3. Всички български отчети (фактура, доставка, PO,
   приемно-предавателен протокол) се рендират през него автоматично.

## Downstream consumers

`l10n_bg_invoice_copy`, `l10n_bg_report_stock`,
`l10n_bg_sale_order_delivery_note` и практически всеки PDF отчет на
българската локализация надграждат този theme.

## Известни ограничения

- Section фоновете и двете лога леко увеличават PDF render тежестта при
  много голям batch печат.

## Свързани

- Преглед на репозиторията: [`../OVERVIEW.bg.md`](../OVERVIEW.bg.md)
- Consumers: `l10n_bg_invoice_copy`, `l10n_bg_report_stock`,
  `l10n_bg_sale_order_delivery_note`
- `readme/` — изходни бележки
