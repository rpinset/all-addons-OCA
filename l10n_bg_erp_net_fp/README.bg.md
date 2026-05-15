# България — ErpNet.FP фискални принтери (OCA)

> Browser-to-printer печат на фискални бонове за български POS през
> ErpNet.FP сървър, с real-time мониторинг на статуса на устройството и
> автоматичен А/Б/В/Г tax-group мапинг.

**Модул:** `l10n_bg_erp_net_fp` | **Версия:** 18.0.7.0.2 | **Лиценз:** LGPL-3 | **Категория:** Point Of Sale

## Описание

Българското законодателство изисква фискални бонове от регистрирано
фискално устройство. Този модул свързва Odoo POS с български фискални
принтери през **ErpNet.FP** сървъра: бонът се печата **директно от
браузъра към устройството** (заобикаляйки backend bottlenecks), докато
backend-ът управлява административните операции и мониторинга. Българските
ДДС данъчни групи (А, Б, В, Г) се мапват автоматично, а здравето на
устройството се polling-ва, така че касиерът вижда състоянието на
принтера в реално време.

## Модел на данните

| Модел | Роля |
|---|---|
| `fiscal.printer.device` | Регистрирано ErpNet.FP устройство (host URL, `printer_id`, timeout, retry count, SSL verify, connection mode, автоматичен-Z конфиг) |
| `fiscal.printer.status` | Live snapshot на здравето на устройството |
| `fiscal.printer.status.history` | Исторически status записи |
| `fiscal.printer.response` | Per-request response log (по `request_id`) |

### `account.tax.group` (разширен)

`l10n_bg_fiscal_tax_group` — selection, мапващ всяка Odoo данъчна група
към българска фискална буква: **А** (ДДС 0%), **Б** (ДДС 20%),
**В** (ДДС 20%), **Г** (ДДС 9%). Default **Б**. Това прави ДДС редовете
на печатния фискален бон легално коректни.

### POS разширения

`pos.config`, `pos.order`, `pos.session`, `pos.printer` разширени за
фискалния print поток (device binding, фискален бон vs fallback,
session/Z обработка).

## Контролер / endpoints (`controllers/main.py`)

JSON endpoints (`auth="user"`), с които browser-side ErpNet.FP
клиентът комуникира:

| Route | Предназначение |
|---|---|
| `/fiscal_printer/get_printer_config` | взема device конфига за принтер |
| `/fiscal_printer/send_response` | връща фискалния отговор на устройството |
| `/fiscal_printer/update_status` | push на live device статус |
| `/fiscal_printer/browser_ready` | browser handshake |
| `/fiscal_printer/test_notification` | bus notification self-test |

Backend asset bundle управлява status updates; `point_of_sale._assets_pos`
bundle управлява in-POS печата + cash/open-control popups.

## Автоматичен Z отчет

`fiscal.printer.device` носи `auto_z_report` + `z_report_hour` /
`z_report_minute`; cron (`data/fiscal_printer_device_cron.xml`)
тригерира end-of-day Z когато е активиран.

## Зависимости

| Odoo базови | Българска локализация |
|---|---|
| `base`, `bus`, `mail`, `point_of_sale`, `account` | — |

## Конфигурация

1. Вдигнете ErpNet.FP сървър, достъпен от касиерските браузъри.
2. Settings → регистрирайте `fiscal.printer.device` записи (host URL,
   printer ID, timeout/retry).
3. Мапнете Odoo данъчните групи към А/Б/В/Г на `account.tax.group`.
4. Bind-нете POS configs към устройства; опционално включете
   автоматичен Z.

## Sister модули

- `l10n_bg_erp_net_fp_fleet` — централен fleet manager за много
  ErpNet.FP инстанции
- `l10n_bg_erp_net_fp_iot` / `_iot_oca` — Odoo IoT-box bridges

> По-богатият PLU / external-POS-shift / standalone shift-dashboard
> feature set живее в l10n-bulgaria CE build-а на този модул
> (18.0.15.x); този OCA build е fiscal-print + status-monitoring ядрото.

## Известни ограничения

- Директният browser→device печат изисква ErpNet.FP service-ът да е
  достъпен от всяка касиерска машина.

## Свързани

- Преглед на репозиторията: [`../OVERVIEW.bg.md`](../OVERVIEW.bg.md)
- `readme/DESCRIPTION.md` — изходни бележки
