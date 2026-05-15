# България — Отпуски по КТ (OCA)

> Българският каталог типове отпуски по Кодекса на труда (КТ) и
> НЗОК: платен годишен, болнични, майчинство/бащинство, учебни,
> граждански дълг — с НОИ reason кодове и обработка на дни за сметка
> на работодателя.

**Модул:** `l10n_bg_hr_holidays` | **Версия:** 18.0.1.0.4 | **Лиценз:** LGPL-3 | **Категория:** Human Resources/Time Off

## Описание

Odoo доставя generic time-off модел; българската ТРЗ изисква законовите
типове отпуски с техните легални кодове, НЗОК болничните reason кодове
и коректна обработка на дните за сметка на работодателя в рамките на
отпуск. Този модул доставя това като data + model слой, който payroll
модулите консумират.

## Модел на данните

### `hr.leave.type` (разширен — `models/hr_leave_type.py`)

| Поле | Предназначение |
|---|---|
| `l10n_bg_code` | Законов код (напр. `155` платен годишен, `163` майчинство). Управлява display `[код] име` и downstream филтриране |
| `l10n_bg_allow_paid_days` | Computed — истина за типове `time_type == "leave"`, при които важат дни за сметка на работодателя |
| `l10n_bg_paid_days_unpaid_leave` | Конфигуриран праг платени дни за иначе неплатен отпуск |
| `l10n_bg_leave_reason_id` | M2O → `nssi.leave.reason` |

### `nssi.leave.reason` (нов — `models/`)

НЗОК болничните reason кодове — `code` (2-знака, индексиран) + `name`
(преводимо), display `[код] име`. Seed-нати от
`data/nssi.leave.reason.csv`. Класифицират болничните за генериране на
НОИ удостоверения.

### `hr.leave` (разширен — `models/hr_leave.py`)

`l10n_bg_leave_reason_id` (related от типа отпуск),
`l10n_bg_show_paid_days_fields`, `l10n_bg_paid_days_unpaid_leave` и
`l10n_bg_effective_unpaid_days` — показват reason кода и изчисляват
колко дни от неплатен отпуск са все още за сметка на работодателя,
когато типът го позволява.

## Заредени данни

- `data/hr_holidays_data.xml` — българските типове отпуски с техните
  КТ / НЗОК кодове.
- `data/nssi.leave.reason.csv` — НЗОК reason кодове.

## Изгледи

`views/hr_leave_type_views.xml` (код + reason + платени дни на типа),
`views/hr_leave_views.xml` (reason + платени дни на заявката),
`views/l10n_bg_nssi_leave_reason.xml` (поддръжка на reason кодове).

## Връзка с ТРЗ

`l10n_bg_hr_payroll_holidays` (EE) надгражда този: авто-създава НОИ
болнични удостоверения при одобрение и захранва третирането на
майчинство / болнични в `l10n_bg_hr_payroll`. Зададените тук кодове са
ключът на връзката.

## Зависимости

| Odoo базови | Българска локализация |
|---|---|
| `hr_contract`, `hr_holidays` | `l10n_bg` |

## Конфигурация

1. Инсталация → типове отпуски + НЗОК reason кодове се зареждат автоматично.
2. HR → Configuration → Time Off Types: преглед на кодове / правила за платени дни.
3. Създайте allocations за годишните типове.

## Известни ограничения

- OCA build-ът е каталогът типове отпуски + reason кодове; read-only
  `hr.leave.balance` SQL view-ът, pro-rata allocation помощникът и
  Annual Leave Schedule планерът са част от l10n-bulgaria CE build-а,
  не от този модул.

## Свързани

- Преглед на репозиторията: [`../OVERVIEW.bg.md`](../OVERVIEW.bg.md)
- ТРЗ consumer: `l10n-bulgaria-ee/l10n_bg_hr_payroll_holidays`
- `readme/DESCRIPTION.md` — изходни бележки
