# Partner Multilang — Транслитерация и многоезични имена (OCA)

> Автоматична кирилица→латиница транслитерация (ISO 9 / ΕΛΟΤ 743),
> езиково разпознаване, многоезично търсене на партньори и правилно
> сортиране — инфраструктурата, която прави българските partner данни
> легално съответстващи и използваеми в смесени-script бази.

**Модул:** `partner_multilang` | **Версия:** 18.0.3.0.4 | **Лиценз:** LGPL-3 | **Категория:** Localization

## Описание

Кирилските държави (България, Русия, Сърбия, Македония, Украйна,
Беларус) законово изискват латинска транслитерация на имената в
официални документи. Смесените кирилица/латиница данни също сортират
грешно в Odoo list/kanban. Този модул решава и двете: транслитерира
автоматично, пази всеки превод, търси из всички тях и сортира по
езика на потребителя.

## Архитектура

### `res.transliterate.mixin` (нов AbstractModel — `models/res_transliterate.py`)

Преизползваемият engine. Всеки модел, който го наследи, получава
многоезичен `display_name`: `_compute_display_name()` връща стойността
на езика на потребителя, транслитерирайки on-the-fly при нужда, и
проследява кои полета са авто-транслитерирани, така че ръчните редакции
не се презаписват.

### Езиково разпознаване (двустепенно)

- **Приоритет 1:** `lingua` (`LanguageDetectorBuilder`) — точен.
- **Приоритет 2:** `langdetect` — бърз fallback.

Неанглийските имена се транслитерират (ISO 9 за кирилица, ΕΛΟΤ 743 за
гръцки) чрез библиотеките `transliterate` + `unidecode`.

### `res.partner` (разширен — `models/res_partner.py`)

- `name` (trigram-индексирано), `street`, `street2`, `city`,
  `function`, `company_name`, `commercial_company_name` направени
  `translate=True`.
- `complete_name_multilanguage` — computed преводимо поле, базирано на
  **JSONB колона**, добавена чрез суров SQL `ADD COLUMN IF NOT EXISTS`
  в `init()`, така че техническата колона се материализира **без
  upgrade на модула**.
- `_rec_names_search` разширен да включи
  `complete_name_multilanguage` — търсенето match-ва всеки запазен
  превод, не само активния език. `get_view` hook пренаписва
  `complete_name` field нодовете към многоезичното поле.

### Други разширения

| Модел | Защо |
|---|---|
| `ir.binary` | `download_name` обработка за преводими JSONB имена (избягва счупени filenames) |
| `res.country` / `res.country.state` | hooks за преводими имена |
| `res.lang` | sort/collation hooks (`views/res_lang_views.xml`) |
| `res.company` / `res.config.settings` | `transliterate_names` фирмен toggle (`views/res_config_settings_view.xml`) |

`pre_init_hook` / `post_init_hook` / `uninstall_hook` управляват
жизнения цикъл на JSONB колоната.

## Зависимости

| Odoo базови | Българска локализация | Python пакети |
|---|---|---|
| `base`, `contacts` | — (фундаментален) | `transliterate`, `unidecode`, `lingua` |

## Конфигурация

1. Инсталация.
2. Settings → активирайте **Transliterate Names** (per company).
3. Съществуващите партньори се транслитерират при следващ write;
   новите при create. JSONB колоната се появява автоматично — без `-u`.

## JSONB предупреждение за downstream модули

Понеже преводимите имена живеят в PostgreSQL **JSONB** колони, всеки
модул правещ `regexp_matches` / суров SQL върху partner имена трябва
да обработва JSONB формата. Това е повтарящ се gotcha — виж
`l10n_bg_account_reconcile_patch`, който съществува точно за да
поправи JSONB-name обработката в OCA reconcile engine-а.

## Downstream consumers

`l10n_bg_multilang`, `l10n_bg_mrp_multilang`,
`l10n_bg_project_multilang`, и практически всеки отчет, който печата
partner имена двуезично.

## Известни ограничения

- Транслитерацията е rule-based (ISO 9 / ΕΛΟΤ 743); собствени имена с
  нестандартна романизация изискват ръчен override.
- Езиковото разпознаване на много къси низове (1-2 знака) е ненадеждно
  — fallback към активния език.

## Свързани

- Преглед на репозиторията: [`../OVERVIEW.bg.md`](../OVERVIEW.bg.md)
- JSONB-fix consumer: `l10n_bg_account_reconcile_patch`
- `readme/DESCRIPTION.md` / `readme/USAGE.md` — изходни бележки
