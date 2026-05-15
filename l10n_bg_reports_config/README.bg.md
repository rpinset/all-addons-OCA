# България — Конфигурация на счетоводните отчети (OCA)

> UI слоят за българските счетоводни отчети: Odoo 18 views, менютата
> и account-tag wizard-а, които показват SQL view моделите от
> `l10n_bg_reports_audit`.

**Модул:** `l10n_bg_reports_config` | **Версия:** 18.0.9.0.2 | **Лиценз:** LGPL-3 | **Категория:** Accounting/Localizations/Reporting

## Описание

`l10n_bg_reports_audit` изчислява българската ДДС декларация,
дневниците продажби / покупки и VIES като headless SQL view модели.
Този модул е **конфигурационната + презентационна половина**: доставя
list/form views, счетоводното меню, account-tag function seed-а и
bulk-tag wizard-а, така че счетоводител реално да управлява отчетите
от Odoo UI. Разделянето на UI от data engine-а позволява на engine-а
да версионира независимо от Odoo-18-специфичните views.

## Какво предоставя

### Изгледи (`views/`)

- `account_bg_vat_line_sale_reports.xml` /
  `account_bg_vat_line_purchase_reports.xml` /
  `account_bg_vat_line_vies_reports.xml` — list/pivot views върху
  sales / purchases / VIES line моделите.
- `account_bg_partner.xml` / `account_bg_products.xml` — partner /
  product оборотна-ведомост views.
- `account_account_tag_views.xml` + `account_menuitem.xml` — поддръжка
  на НАП cell-tag + менюто за български отчети.
- `res_company_views.xml` / `res_company_history_vat.xml` /
  `res_company_history_intrastat.xml` — ДДС коефициент (чл. 73 §2) и
  история на Intrastat прага на фирмата.
- `res_config_view.xml`, `res_partner.xml`, `product_view.xml`,
  `account_move_views.xml` — поддържащи form разширения.

### Модел

`l10n.bg.vat.ratio.history` (разширен,
`models/res_company_history_vat.py`) — UI-side добавки към записа за
история на ДДС коефициента.

### Помощник (wizard)

`account_account_tag_bulk_edit_wizard` (`wizards/`) — bulk-задаване на
НАП cell tags върху много сметки наведнъж (практичният начин да
мапнеш цял сметкоплан към декларационните клетки).

### Seed данни

`data/account_account_tag_function.xml` (tag→function мапинг) +
`data/settings.xml`.

## Зависимости

| Odoo базови | Българска локализация |
|---|---|
| `base`, `account` | `l10n_bg_reports_audit`, `l10n_bg_config`, `l10n_bg_ledger` |

## Конфигурация

1. Инсталирайте (издърпва `l10n_bg_reports_audit`).
2. Accounting → Bulgaria → преглед на ДДС / продажби / покупки / VIES
   report views.
3. Ползвайте account-tag bulk-edit wizard-а за мапване на сметкоплана
   към НАП декларационните клетки.
4. Задайте фирмения ДДС коефициент (чл. 73 §2) и Intrastat праговете
   на company history views.

## Известни ограничения

- Само презентация — числата идват от `l10n_bg_reports_audit` SQL
  views; грешно число се поправя в счетоводните записи / account tags,
  не тук.

## Свързани

- Преглед на репозиторията: [`../OVERVIEW.bg.md`](../OVERVIEW.bg.md)
- Data engine: `l10n_bg_reports_audit`
- `readme/DESCRIPTION.md` / `readme/USAGE.md` — изходни бележки
