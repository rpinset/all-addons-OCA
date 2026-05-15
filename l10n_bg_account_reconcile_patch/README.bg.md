# България — Account Reconcile JSONB-Name поправка (OCA)

> Patch-ва OCA bank-statement reconciliation, така че partner
> matching-ът работи когато partner имената са съхранени като преводим
> JSONB (страничен ефект от `partner_multilang`).

**Модул:** `l10n_bg_account_reconcile_patch` | **Версия:** 18.0.1.0.0 | **Лиценз:** LGPL-3 | **Категория:** Localization

## Описание

Когато `partner_multilang` направи `res.partner.name` преводима
**JSONB** колона, OCA reconciliation engine-ът изпълнява
`regexp_matches(...)` срещу суровия JSONB и не намира партньора. Този
модул monkey-patch-ва matching логиката да резолва JSONB името първо,
така че auto-reconciliation продължава да работи в многоезична база.

Това е **OCA-stack вариантът**: patch-ва matching-а на
`account.bank.statement.line`, както е свързан от
`account_reconcile_model_oca`, не Enterprise `account_accountant`
reconcile widget-а.

## Какво прави

Чрез `post_load_hook` (monkey-patch в `hooks.py`, без model промени):

- `_retrieve_partner_patch` — заменя `AccountBankStatementLineBase
  ._retrieve_partner`; SQL `regexp_matches(...)` сега оперира върху
  резолвнатия текст на името вместо JSONB blob-а.
- `_get_st_line_strings_for_matching(allowed_fields=None)` — настроен,
  така че statement-line низовете сравняват срещу правилната name
  репрезентация.

Hook-ът се регистрира през `post_load` в манифеста
(`post_load_hook`), така че активира без изричен upgrade на модела.

## Зависимости

| Odoo / OCA | Българска локализация |
|---|---|
| `account_reconcile_model_oca` | ефективен с `partner_multilang` |

Без външни Python пакети.

## Конфигурация

Няма. Инсталирайте — OCA reconciliation partner matching-ът толерира
JSONB имена.

## Свързани JSONB-fix модули

Companion на org-chart / multilang JSONB-name поправките. Root cause-ът
е документиран в `partner_multilang` (преводимите имена са PostgreSQL
JSONB колони; всеки суров SQL върху `res.partner.name` трябва да
обработва този формат).

## Свързани

- Преглед на репозиторията: [`../OVERVIEW.bg.md`](../OVERVIEW.bg.md)
- Root cause: `partner_multilang`
- OCA reconcile база: `account_reconcile_model_oca`
