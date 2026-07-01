# l10n_at_pos_rksv

> Austrian RKSV (a.sign) integration for the Point of Sale: signs every receipt with a
> chained AES turnover counter and prints the QR code required by the Austrian fiscal
> authority.

## Dependencies

- Odoo: `l10n_at`, `point_of_sale` (+ implicit `account`).
- Python: `cryptography`, `pytz`, `requests`.
- Optional (tests only): a JRE plus the Java `regkassen-verification` tool shipped under
  `tests/regcheck/`.

## Models

| Model                 | Purpose                                                                                                       |
| --------------------- | ------------------------------------------------------------------------------------------------------------- |
| `asign.cert`          | A-Trust signing certificate plus online API credentials.                                                      |
| `pos.config`          | Adds the RKSV configuration: enabled flag, method, serial, fiscal/POS-ID, encryption key, CRC, state machine. |
| `pos.order`           | Adds RKSV fields and the chained signature implementation.                                                    |
| `pos.session`         | Triggers the sign-missed cron after closing a session.                                                        |
| `account.tax.group`   | Adds `asign_type` (RKSV tax category).                                                                        |
| `res.config.settings` | Settings UI surface for `pos.config` RKSV fields.                                                             |

## Key Fields & Logic

- `pos.config.asign_state` (`draft → assigned → active`) – locks the RKSV parameters so
  they cannot accidentally change after signing started.
- `pos.config.asign_pid` – auto-incremented per company (`K01`, `K02`, …) with a
  unique-index per company.
- `pos.config.asign_key` – random 32-byte AES key (base64); CRC is the truncated SHA-256
  hash, also rendered on the configuration report.
- `pos.order._asign_add_signature()` – core chained signing flow; called from
  `action_pos_order_paid` and able to back-fill missed orders (paid, done and cancelled
  ones).
- `pos.order._asign_prepare_cancel()` – prepares a cancelled order holding a receipt
  number for signing: zeroes the lines when nothing was paid and restores the name.
- `pos.config._asign_create_zero_receipt()` – produces start/zero receipts required by
  the RKSV (`asign_type` `s` for the very first one, `0` afterwards).
- `pos.config._asign_repair_cancelled_names()` – restores names of signed orders that
  were overwritten with `cancel`/`'/'`; runs idempotently inside `_asign_sign_missed`.
- Cron `pos_config_ir_cron` – daily run of `_cron_asign_sign_missed`; also signs
  cancelled orders as zeroed receipts to keep the receipt range gapless. Skips POS with
  a session in `opened` state; additionally triggered asynchronously by
  `pos.session.action_pos_session_close()`.

## Views & Menus

- POS settings inherit (`res_config_settings_views.xml`) – RKSV section.
- POS list/form inherits (`pos_order_views.xml`) – RKSV signature fields.
- POS configuration form (`pos_config_views.xml`) – _Create Zero-Receipt_.
- Tax-group inherits (`account_tax_views.xml`) – RKSV tax category.
- Certificate views and menu (`asign_views.xml`) under _Point of Sale > Configuration >
  a.sign RKSV_.
- PDF reports for `asign.cert` and `pos.config` (`pos_report.xml` plus
  `report_certificate.xml`, `report_pos_config.xml`).

## Configuration

Hook `post_init_hook` pre-fills `account.tax.group.asign_type` for the standard Austrian
VAT rates (`0%`, `10%`, `13%`, `19%`, `12%`).

## File Layout

```
l10n_at_pos_rksv/
├── data/asign_cron.xml
├── hooks.py
├── i18n/de.po
├── models/
│   ├── account_tax.py, asign.py, pos_config.py, pos_order.py,
│   └── pos_session.py, res_config_settings.py
├── readme/                # OCA fragments (DESCRIPTION, USAGE, CONFIGURE…)
├── security/ir.model.access.csv
├── static/src/...         # POS frontend overrides + receipt CSS/QWeb
├── tests/
│   ├── common.py          # local TestDownload / TestAsignCommon mixins
│   ├── test_res_config_settings.py
│   ├── test_cancel.py     # cancelled orders, write guard, name repair (mocked)
│   ├── test_dep.py        # gated by `pos_config_id` config
│   ├── test_asign_online.py # gated by `test_asign` config
│   └── regcheck/          # Python wrapper + Java jars (tests-only)
└── views/
```

## Known Pitfalls / Notes

- License is **LGPL-3** to match the other OCA `l10n_at_*` modules.
- In Odoo 19 every order consumes `sequence_number` at create. Cancelled orders
  therefore hold a receipt number and must be signed as zeroed receipts (handled by the
  signing loop / cron), otherwise the gapless receipt range breaks and all following
  orders stay unsigned.
- `test_asign_online.py` and `test_dep.py` carry the `integration` / `-standard` tags
  and additionally check `config.get('test_asign')` / `config.get('pos_config_id')`.
  They are skipped in normal CI runs.
- The `tests/regcheck/regkassen-verification-1.1.1/` folder ships the upstream Java jars
  (~19 MB) needed for DEP verification; they are not loaded at module install but must
  be excluded from any size-sensitive packaging step.
- Anything sent to the A-Trust JWS endpoint requires a configured `asign.cert` with
  `cert_type='online'`, `user`, `password`.
- `test_rksv_pid` deliberately provokes the per-company unique-index on
  `pos.config.asign_pid` and uses `@mute_logger("odoo.sql_db")` so the expected
  `UniqueViolation` does not leave an `ERROR` line in the log (which would otherwise
  break OCA's `checklog-odoo` CI step).
