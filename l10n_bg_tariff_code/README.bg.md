# България — Управление на TARIC / HS / CN кодове (OCA)

> Управление на митнически стокови кодове за продукти и фактурни
> редове, с локален кеш на ЕС TARIC тарифни ставки, изтеглени от
> европейския CIRCABC dataset.

**Модул:** `l10n_bg_tariff_code` | **Версия:** 18.0.3.0.10 | **Лиценз:** LGPL-3 | **Категория:** Accounting/Localizations

## Описание

Българските митнически декларации и Intrastat отчетност изискват
всеки продукт да носи своя **TARIC / HS / CN** стоков код, а
митническата оценка се нуждае от приложимата тарифна ставка.
Заявка към ЕС TARIC системата на всеки ред би била бавна и
rate-limited, затова този модул поддържа **локален кеш на ставки** по
ключ CN код + държава + период на валидност, опресняван от
официалните CIRCABC данни.

## Модел на данните

### `l10n_bg.taric.cache` (нов — `models/l10n_bg_taric_cache.py`)

Локален кеш на TARIC тарифни ставки от CIRCABC. `_rec_name = "cn_code"`,
подреден по `cn_code, country_code`.

| Поле | Значение |
|---|---|
| `cn_code` | Combined Nomenclature код (rec name) |
| `country_code` | Държава на произход, за която важи ставката |
| `measure_type` | TARIC measure тип (напр. `103` = мито трета държава) |
| `duty_rate` | Приложимо мито |
| `valid_from` / `valid_to` | Период на валидност на ставката |

SQL constraint `UNIQUE(cn_code, country_code, valid_from, valid_to)`
предотвратява дублирани припокриващи се ставки. Lookup-ите удрят кеша
първо; miss (или stale запис след `valid_to`) тригерира refresh от
конфигурираното TARIC API.

### Разширени модели

| Модел | Добавка |
|---|---|
| `product.template` / `product.product` | TARIC/HS/CN code полета |
| `account.move.line` | tariff code propagation за митническа оценка |
| `res.company` | `l10n_bg_taric_api_url`, `l10n_bg_taric_api_enabled`, `l10n_bg_taric_cache_duration` (часове) |
| `res.config.settings` | излага горните като settings |

## Помощник (wizard)

`l10n_bg_taric_import_wizard` (`wizards/`) — bulk-импортира TARIC/CN
ставки от CIRCABC export в `l10n_bg.taric.cache` (гъвкав column mapping
поема CIRCABC формат drift).

## Заредени данни

`data/l10n_bg_tarif_code_data.xml`. `pre_init_hook` подготвя схемата
преди първа инсталация.

## Зависимости

| Odoo базови | Българска локализация | Python пакет |
|---|---|---|
| `account`, `stock_delivery` | — | `requests` |

## Конфигурация

1. Settings → Bulgarian Localization → TARIC:
   - **Enable TARIC API** + **TARIC API URL** (ЕС endpoint).
   - **Cache Duration (hours)** — колко дълго cached ставка се доверява.
2. Задайте TARIC/CN кодове на продуктите (ръчно или чрез
   `taric_ai_classifier` за AI-подпомогната класификация), или пуснете
   import wizard-а срещу CIRCABC export.

## Downstream consumers

`taric_ai_classifier` (AI класификацията записва кодове тук),
`l10n_bg_intrastat` (стокови кодове на декларации),
`l10n_bg_tax_admin` митнически потоци.

## Известни ограничения

- Свежестта на кеша зависи от `cache_duration`; ставка, която се
  промени в средата на прозореца, се взема едва след изтичане (или
  ръчен re-import).
- CIRCABC dataset структурата се променя понякога — column mapping-ът
  на wizard-а толерира чести промени, но голяма ЕС формат промяна
  изисква code update.

## Свързани

- Преглед на репозиторията: [`../OVERVIEW.bg.md`](../OVERVIEW.bg.md)
- AI класификатор: `taric_ai_classifier`
- `readme/DESCRIPTION.md` — изходни бележки
