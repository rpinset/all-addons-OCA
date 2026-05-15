# Bulgaria — ErpNet.FP Fiscal Printers (OCA)

> Browser-to-printer fiscal-receipt printing for Bulgarian POS via the
> ErpNet.FP server, with real-time device status monitoring and
> automatic А/Б/В/Г tax-group mapping.

**Module:** `l10n_bg_erp_net_fp` | **Version:** 18.0.7.0.2 | **License:** LGPL-3 | **Category:** Point Of Sale

## Overview

Bulgarian law requires fiscal receipts from a registered fiscal device.
This module connects Odoo POS to Bulgarian fiscal printers through the
**ErpNet.FP** server: the receipt is printed **directly from the
browser to the device** (bypassing backend bottlenecks), while the
backend drives administrative operations and status monitoring.
Bulgarian VAT tax groups (А, Б, В, Г) are mapped automatically, and
device health is polled so a cashier sees the printer state in real
time.

## Data model

| Model | Role |
|---|---|
| `fiscal.printer.device` | A registered ErpNet.FP device (host URL, `printer_id`, timeout, retry count, SSL verify, connection mode, automatic-Z config) |
| `fiscal.printer.status` | Live device health snapshot |
| `fiscal.printer.status.history` | Historical status records |
| `fiscal.printer.response` | Per-request response log (keyed by `request_id`) |

### `account.tax.group` (extended)

`l10n_bg_fiscal_tax_group` — selection mapping each Odoo tax group to a
Bulgarian fiscal letter: **А** (VAT 0%), **Б** (VAT 20%), **В** (VAT
20%), **Г** (VAT 9%). Default **Б**. This is what makes the printed
fiscal receipt's VAT lines legally correct.

### POS extensions

`pos.config`, `pos.order`, `pos.session`, `pos.printer` extended for
the fiscal print flow (device binding, fiscal receipt vs fallback,
session/Z handling).

## Controller / endpoints (`controllers/main.py`)

JSON endpoints (`auth="user"`) the browser-side ErpNet.FP client
talks to:

| Route | Purpose |
|---|---|
| `/fiscal_printer/get_printer_config` | fetch the device config for a printer |
| `/fiscal_printer/send_response` | post the device's fiscal response back |
| `/fiscal_printer/update_status` | push live device status |
| `/fiscal_printer/browser_ready` | browser handshake |
| `/fiscal_printer/test_notification` | bus notification self-test |

A backend asset bundle drives status updates; a `point_of_sale._assets_pos`
bundle drives the in-POS print + cash/open-control popups.

## Automatic Z report

`fiscal.printer.device` carries `auto_z_report` + `z_report_hour` /
`z_report_minute`; a cron (`data/fiscal_printer_device_cron.xml`)
triggers the end-of-day Z when enabled.

## Dependencies

| Odoo core | Bulgarian-localization |
|---|---|
| `base`, `bus`, `mail`, `point_of_sale`, `account` | — |

## Configuration

1. Stand up an ErpNet.FP server reachable from the cashier browsers.
2. Settings → register `fiscal.printer.device` entries (host URL,
   printer ID, timeout/retry).
3. Map Odoo tax groups to А/Б/В/Г on `account.tax.group`.
4. Bind POS configs to devices; optionally enable automatic Z.

## Sister modules

- `l10n_bg_erp_net_fp_fleet` — central fleet manager for many
  ErpNet.FP instances
- `l10n_bg_erp_net_fp_iot` / `_iot_oca` — Odoo IoT-box bridges

> The richer PLU / external-POS-shift / standalone shift-dashboard
> feature set lives in the l10n-bulgaria CE build of this module
> (18.0.15.x); this OCA build is the fiscal-print + status-monitoring
> core.

## Known limitations

- Direct browser→device printing needs the ErpNet.FP service reachable
  from each cashier machine.

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- `readme/DESCRIPTION.md` — source notes
