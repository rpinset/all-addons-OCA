# България — Интеграция с Търговския регистър (OCA)

> Real-time обогатяване на партньори от официалния български Търговски
> регистър (portal.registryagency.bg): извличане и попълване на фирмени
> данни по ЕИК с един клик.

**Модул:** `l10n_bg_company_registry` | **Версия:** 18.0.2.0.1 | **Лиценз:** LGPL-3 | **Категория:** Localization

## Описание

Ръчното преписване на легалните данни на български контрагент (точно
име, структуриран адрес, правна форма, NACE/КИД дейност, съд по
регистрация, управители) е грешкоопасно и остарява. Този модул заявява
официалното API на Търговския регистър live, парсва отговора и записва
данните директно върху `res.partner` — без offline база за поддръжка,
винаги свежи данни.

## Архитектура

### `res.partner` (разширен — `models/res_partner.py`)

Нови полета, попълвани от регистъра:

| Поле | Значение |
|---|---|
| `l10n_bg_legal_form` | ООД / ЕООД / АД / ЕТ … |
| `l10n_bg_registration_date` | Дата на регистрация |
| `l10n_bg_registration_court` | Съд по регистрация |
| `l10n_bg_activity_code` | NACE/КИД код на икономическа дейност |
| `l10n_bg_activity_description` | Описание на дейността |

`action_fetch_from_registry()` — извлича ЕИК от ДДС номера на
партньора (`BG…` премахнато), вика регистъра и попълва партньора.
Умен address parsing обработва българските формати: ул./бул., ж.к.,
к.к., м., кв., р-н, плюс извличане на email/телефон от свободен текст.

### `bg.company.search.wizard` (`wizard/`)

Search-by-ЕИК wizard: връща резултата от регистъра в preview полета
(`display_name_bg` / `display_name_en`, `display_legal_form_bg`,
`display_vat`, `display_address_bg`, `display_country_id`,
`display_state_id`, `display_city_id` → `res.city`,
`display_postal_code`), така че потребителят преглежда преди да го
приложи към партньора.

### `data/ir_actions_server.xml`

`action_populate_bg_registry_data` — контекстуален `res.partner`
server action ("Populate BG Registry Data"), така че fetch-ът може да
се тригерира от action менюто на partner list/form.

## Зависимости

| Odoo базови | Българска локализация | Python пакет |
|---|---|---|
| `base`, `contacts` | `l10n_bg_config`, `l10n_bg_city` | `requests` |

`l10n_bg_city` доставя ЕКАТТЕ населеното място, към което се свързва
парснатият адрес (`res.city`).

## Конфигурация

Инсталация. Отворете партньор с български ДДС/ЕИК → пуснете **Populate
BG Registry Data** (или ползвайте search wizard-а). Структурираният
адрес се свързва с `l10n_bg_city` базата населени места.

## Известни ограничения

- Зависи от достъпността и формата на portal.registryagency.bg;
  голяма промяна в API изисква обновяване на парсера.
- Address parsing-ът е евристичен за свободен текст — верифицирайте
  парснатия град/улица след fetch за необичайни формати.

## Свързани

- Преглед на репозиторията: [`../OVERVIEW.bg.md`](../OVERVIEW.bg.md)
- Източник на населени места: `l10n_bg_city`
- `readme/DESCRIPTION.md` / `readme/CHANGELOG.md` — изходни бележки
