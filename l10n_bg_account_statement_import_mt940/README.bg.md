# България — MT940 импорт на банкови извлечения (OCA)

> Добавя SWIFT **MT940** формат към OCA framework-а за импорт на
> банкови извлечения, с разхлабен `:28C:` StatementNumber pattern за
> приемане на експорти от български банки.

**Модул:** `l10n_bg_account_statement_import_mt940` | **Версия:** 18.0.1.0.0 | **Лиценз:** LGPL-3 | **Категория:** Localization

## Описание

Повечето български банки експортират извлечения в **MT940** (SWIFT).
OCA framework-ът `account_statement_import_file` не доставя MT940 по
подразбиране, а `StatementNumber` regex-ът на стандартната `mt-940`
Python библиотека е по-строг от това, което някои български банки
емитват. Този модул регистрира формата и patch-ва pattern-а, така че
тези експорти се парсват чисто.

## Какво прави

- `account.journal._get_bank_statements_available_import_formats()`
  разширен (`models/account_journal.py`) — добавя `"mt940"` към
  списъка с поддържани формати за импорт.
- Wizard binding (`wizard/account_statement_import.xml`) включва MT940
  парсера в OCA `account.statement.import` потока.
- `mt940.tags.StatementNumber.pattern` е override-нат с разхлабен
  regex, така че `:28C:` полето от български банки се приема
  (валидирано от standalone parser теста в `tests/`).

## Зависимости

| OCA core | Python пакет |
|---|---|
| `account_statement_import_file` | `mt-940` |

> Бележка: манифестът декларира PyPI пакета `mt-940`
> (`pip install mt-940`); import името е `mt940`.

## Конфигурация

1. Инсталация (`pip install mt-940` ако още не е наличен).
2. Accounting → импорт на банково извлечение → изберете **MT940**
   формат → качете `.940` / `.sta` файла на банката.

## Бележка vs InfoPay

За Borica InfoPay банки предпочитайте live API (`l10n_bg_infopay` +
bridges) пред MT940 файлов импорт. MT940 е fallback за банки без
InfoPay канал.

## Свързани

- Преглед на репозиторията: [`../OVERVIEW.bg.md`](../OVERVIEW.bg.md)
- OCA import база: `account_statement_import_file`
- Live алтернатива: `l10n_bg_infopay`
