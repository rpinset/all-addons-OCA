# България — Приемно-предавателен отчет от поръчка (OCA)

> QWeb PDF "приемно-предавателен" / pro-forma отчет, генериран
> директно от българска поръчка за продажба.

**Модул:** `l10n_bg_sale_order_delivery_note` | **Версия:** 18.0.1.0.0 | **Лиценз:** AGPL-3 | **Категория:** Sales/Bulgaria

## Описание

Българската търговска практика често изисква
приемно-предавателен / pro-forma документ, издаден на ниво
**поръчка за продажба** (преди или вместо stock-side
приемно-предавателния протокол). Този модул добавя този отчет на
`sale.order`.

## Какво предоставя

- `report/ir_actions_report.xml` — `ir.actions.report` (qweb-pdf),
  bind-нат към `sale.order`, достъпен от Print менюто на поръчката.
- `report/ir_action_report_templates.xml` — QWeb template-ът,
  ползващ българския section-based report theme.

Само report-layer — без model полета, без seed данни.

## Зависимости

| Odoo базови | Българска локализация |
|---|---|
| `sale` | `l10n_bg_report_theme` |

## Конфигурация

Няма. Инсталирайте — приемно-предавателният отчет се появява в Print
менюто на поръчката.

## Свързани модули

`l10n_bg_report_stock` предоставя stock-picking-side
приемно-предавателния протокол + документ; този модул е sale-order-side
вариантът.

## Свързани

- Преглед на репозиторията: [`../OVERVIEW.bg.md`](../OVERVIEW.bg.md)
- Stock-side: `l10n_bg_report_stock`
- Report layout: `l10n_bg_report_theme`
