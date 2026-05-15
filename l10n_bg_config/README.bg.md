# Българска локализация — Конфигурационен гръбнак (OCA)

> Основният модул на българската локализация. Издърпва core стека,
> скрива BG-специфичния UI за не-български фирми, валидира
> идентификатори и деривира криптирани API credentials.

**Модул:** `l10n_bg_config` | **Версия:** 18.0.8.0.5 | **Лиценз:** LGPL-3 | **Категория:** Localization

## Описание

`l10n_bg_config` е крайъгълният камък, от който зависи всеки друг
модул на българската локализация. Има три задачи:

1. **Еднократна инсталация на локализацията.** Авто-инсталира с
   `l10n_bg` (`auto_install: ["l10n_bg"]`) и зависи от `l10n_bg_ledger`
   + `l10n_bg_tariff_code`, така че нова база става готова за България
   без ръчно търсене на зависимости. `pre_init_hook` /
   `post_init_hook` свързват chart-of-accounts шаблоните
   (`data/template/`).
2. **Мултифирмена UI дисциплина.** В база, която смесва български и
   небългарски фирми, BG-специфичните полета и групи биха задръствали
   всяка форма за небългарските субекти. Mixin-ът ги премахва
   автоматично спрямо активната фирма.
3. **Деривация на credentials.** API ключовете за НАП интеграциите
   никога не се валидират срещу съхранен plaintext — модулът доставя
   XOR-базираната деривация на ключове, ползвана в цялата локализация.

## Архитектура

### `l10n.bg.config.mixin` (AbstractModel)

Сърцето на модула (`models/l10n_bg_config_mixin.py`). Всеки модел,
който го наследи, получава:

- `is_l10n_bg_record` — computed boolean, истина когато фирмата на
  записа (или активната фирма) е маркирана като българска чрез
  `res.company._check_is_l10n_bg_record()`.
- Override-нат `get_view()`, който за **небългарски фирми**
  пренаписва върнатата arch, слагайки `column_invisible` / `invisible`
  на всяко `l10n_bg_*` поле и всяка `l10n_bg`-именувана група, и
  скрива search филтри рефериращи `l10n_bg`. Локализационен модул може
  свободно да добавя `l10n_bg_*` полета — те изчезват за фирмите, които
  не се нуждаят от тях, без ръчни `invisible` атрибути.

### Разширени core модели

| Модел | Защо е разширен |
|---|---|
| `res.company` | `_check_is_l10n_bg_record()` gate; chart-template binding; съхранение на BG API ключ |
| `res.partner` | BG ЕИК/БУЛСТАТ, `generate_encryption_keys(...)` crypt key |
| `account.move` / `account.move.line` | наследяват mixin → авто-скриване на BG полета за не-BG фирми |
| `account.chart.template` | hook points за БГ сметкоплан |
| `account.account.tag` | база за НАП клетъчно тагване |
| `res.country` | hooks за преводими области/региони |
| `ir.module.module` | помощници за оркестрация на инсталацията |

### Помощници за сигурност на credentials

`models/l10n_bg_config_mixin.py` предоставя:

- `generate_encryption_keys(key1, key2)` / `decrypt_key(encrypted,
  key1, key2)` — XOR-базирана деривация на ключове.
- `is_valid_api_key(uic, api_key, crypt_key)` — валидира тройката
  НАП submission credentials без пряка проверка за равенство.
- `prepare_zip_payload(files_report, company)` — обвива файловете на
  НАП отчетите; инжектира случайна еднократна парола когато тройката
  API ключове е невалидна, така че експортите деградират безопасно.

> OCA build-ът само деривира/валидира credentials; Fernet-криптираният
> company-blacklist контролер + OWL service на l10n-bulgaria CE build-а
> **не** е част от този модул.

## Помощници (wizards)

| Wizard | Предназначение |
|---|---|
| `account_account_tag_bulk_edit_wizard` | bulk-тагване на сметки за НАП клетки |
| `account_settings_preview_xml_file` | preview на генериран settings XML |
| `account_chart_template_plugins` | enable/disable chart-template plugins |

## Заредени данни

`data/res_lang_data.xml` (BG language конфиг) + `data/template/`
сметкоплан CSV-та (`account.account-bg.csv`, `account.group-bg.csv`,
`account.tax-bg.csv`).

## Зависимости

| Odoo базови | Българска локализация | Python пакет |
|---|---|---|
| `base`, `account`, `base_vat` | `l10n_bg`, `l10n_bg_ledger`, `l10n_bg_tariff_code` | `xmltodict` |

## Конфигурация

1. Apps → инсталирайте **l10n_bg_config** (зависимостите се авто-инсталират).
2. Settings → Localization → преглед на активните модули + chart template.
3. Задайте ЕИК/БУЛСТАТ и НАП API credentials на фирмения партньор;
   модулът деривира и съхранява криптирания crypt key.

## Конвенция за именуване на полета (валидна за цялата екосистема)

Всяко поле, което локализационен модул добавя към Odoo core модел
(`account.move`, `res.partner`, `res.company`, `pos.*`, …) **трябва**
да е с префикс `l10n_bg_`. View пренаписването на mixin-а разчита на
този префикс — непрефиксирани полета ще изтекат във форми на не-BG фирми.

## Известни ограничения

- `get_view` arch пренаписването е per-call; много големи views
  добавят минимален parse overhead за не-BG фирми.

## Свързани

- Преглед на репозиторията: [`../OVERVIEW.bg.md`](../OVERVIEW.bg.md)
- `readme/` — DESCRIPTION / CONTEXT / CONFIGURE изходни бележки
- Downstream consumers: практически всеки `l10n_bg_*` модул
