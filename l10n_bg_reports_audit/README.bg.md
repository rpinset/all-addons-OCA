# България — База на счетоводните отчети (OCA)

> Техническата база за българската счетоводна/данъчна отчетност: SQL
> view моделите зад ДДС декларацията, дневниците продажби/покупки и
> VIES, плюс НАП конфигурацията на account tags. Без собствен UI —
> data engine-ът, върху който report модулите надграждат.

**Модул:** `l10n_bg_reports_audit` | **Версия:** 18.0.12.0.3 | **Лиценз:** LGPL-3 | **Категория:** Accounting/Localizations/Reporting

## Описание

Българската ДДС отчетност (ДДС декларация, дневник на
продажбите/покупките, VIES) се изчислява от счетоводни записи,
таг-нати срещу НАП клетъчните кодове. Правенето на това в Python per
отчет би било бавно и неконсистентно. Този модул го доставя като слой
от **PostgreSQL view модели**, които строят SQL-а си динамично
(`_select()` / `_from()` / `_where()` / `_group()`), така че всеки
отчет чете същите авторитетни числа. Не доставя менюта или форми —
`l10n_bg_reports_config` (sibling) предоставя UI.

## SQL view модели (`report/`, `_auto=False`)

### ДДС декларационна верига

| Модел | Роля |
|---|---|
| `account.bg.vat.calc.declar` | Детайлно ДДС изчисление per ред (клетки 10-82) |
| `account.bg.vat.info.declar` | Агрегирана ДДС декларация per фирма/период |
| `account.bg.vat.result.declar` | Salda: tag_50 (внасяне), tag_60 (възстановяване), 70-82 (чл. 92) |

### Дневници продажби / покупки

`account.bg.info.sale.line` / `account.bg.calc.sales.line` /
`account.bg.total.sales.line` и тройката покупки
(`account.bg.info.purchases.line` / `.calc.purchases.line` /
`.total.purchases.line`) — редовете на дневника на продажбите /
покупките с НАП `info_tag_*` / `account_tag_*` колони. `calc`
вариантите са persistent PG views с custom `init()` (нужен е module
`-u` след промяна на заявка); `info` вариантите са dynamic
`_table_query` (restart е достатъчен).

### VIES

`account.bg.calc.vies.line` (вътреобщностни доставки per партньор —
стоки / триъгълни / услуги), `account.bg.vies.info.declar`,
`account.bg.vies.total.declar`.

### Оборотна ведомост

`account.bg.calc.partner.line` (вземания/задължения per партньор с
рекурсивно CTE: начално → движение → крайно),
`account.bg.calc.product.line`.

## Разширени модели

| Модел | Добавка |
|---|---|
| `account.account.tag` | `+ l10n.bg.config.mixin`; базата на НАП cell-tag |
| `account.move` / `account.move.line` | reporting metadata за view-овете |
| `account.journal` | класификация на журнали за дневниците |
| `res.company` | `l10n_bg_vat_ratio` (чл. 73 §2), Intrastat-threshold + VAT-ratio history връзки, audit config флагове |
| `res.company.history.vat` (`l10n.bg.vat.ratio.history`) | история на ДДС коефициента (mail.thread) |
| `res.company.history.intrastat` (`l10n.bg.intrastat.threshold`) | история на Intrastat прага |
| `res.partner` / продукти | reporting помощници (`report/account_bg_partner.py`, `account_bg_products.py`) |
| `ir.actions.report` / `res.config.settings` | report + settings hooks |

`l10n_bg_file_helper` пакетира файловете на отчетите за НАП експорт.

## Зависимости

| Odoo базови | Българска локализация |
|---|---|
| `base`, `account` | `l10n_bg`, `l10n_bg_ledger`, `l10n_bg_config` |

## Конфигурация

Инсталирайте (издърпва се автоматично от `l10n_bg_config`). Не излага
UI самостоятелно — инсталирайте `l10n_bg_reports_config` за views,
менюта и account-tag bulk-edit wizard-а. Таг-нете сметкоплана срещу
НАП клетките; view моделите тогава изчисляват декларациите.

## Restart vs upgrade (операционна бележка)

След редакция на `*.info.*` заявка (dynamic `_table_query`) сървърен
**restart** е достатъчен. След редакция на `*.calc.*` / `*.total.*` /
`*.declar` persistent PG view (custom `init()`) е нужен module **`-u`**
(или ръчен `DROP VIEW` + пресъздаване).

## Downstream consumers

`l10n_bg_reports_config` (UI), `l10n_bg_vat_reports` /
`l10n_bg_tax_admin` и НАП submission модулите четат тези views.

## Известни ограничения

- View моделите са read-only; корекциите се правят върху подлежащите
  счетоводни записи / account tags, не върху редовете на отчета.
- Двойната `init()` vs `_table_query` семантика означава, че промяна в
  заявка може тихо да не влезе в сила без правилния reload (виж по-горе).

## Свързани

- Преглед на репозиторията: [`../OVERVIEW.bg.md`](../OVERVIEW.bg.md)
- UI sibling: `l10n_bg_reports_config`
- `readme/` — DESCRIPTION / CONTEXT / CONFIGURE / USAGE изходни бележки
