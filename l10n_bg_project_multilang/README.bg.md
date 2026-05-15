# България — Многоезична проектна задача (OCA)

> Прави partner-name полетата на проектната задача преводими, така че
> проектните документи се рендират двуезично, консистентно с multilang
> стека.

**Модул:** `l10n_bg_project_multilang` | **Версия:** 18.0.1.0.0 | **Лиценз:** LGPL-3 | **Категория:** Localization

## Описание

Multilang стекът (`partner_multilang` / `l10n_bg_multilang`) прави
partner/employee/bank имената двуезични. Проектните задачи също носят
partner name полета, които се появяват на проектните документи — този
модул ги прави преводими също, така че проектната документация остава
консистентна с българските двуезични изисквания.

## Какво прави

`project.task` (разширен — `models/`):

| Поле | Третиране |
|---|---|
| `partner_name` | `translate=True` |
| `partner_company_name` | `translate=True` |

Само model-layer — без views (празната `data` в манифеста е по
дизайн), без seed данни, без външни зависимости.

## Зависимости

| Odoo базови | Българска локализация |
|---|---|
| `project` | `partner_multilang` |

Твърда зависимост от `partner_multilang` — той предоставя
transliteration engine-а и JSONB-name инфраструктурата, на които тези
преводими полета разчитат.

## Конфигурация

Няма. Инсталирайте — partner-name полетата на проектната задача приемат
per-език стойности; транслитерацията следва фирмения toggle на
`partner_multilang`.

## Свързани

- Преглед на репозиторията: [`../OVERVIEW.bg.md`](../OVERVIEW.bg.md)
- Multilang ядро: `partner_multilang`, `l10n_bg_multilang`
- Sibling: `l10n_bg_mrp_multilang`
