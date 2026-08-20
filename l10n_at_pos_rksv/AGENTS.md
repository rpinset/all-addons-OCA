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
- `pos.config.asign_seq_id` – dedicated `no_gap` `ir.sequence` per POS for the RKSV
  receipt number (`asign_seq`). Created at `action_asign_assign` (lazily via
  `_asign_seq`) and decoupled from the order number (`sequence_number`).
- `pos.order.asign_seq` – gapless RKSV receipt number, drawn from `asign_seq_id` only
  when a receipt is signed (`_asign_next_seq`), so cancelled/skipped orders never create
  a gap.
- `pos.order._compute_order_name()` – for RKSV the final name is built from `asign_seq`
  via `order_seq_id.get_next_char`; until signed the order keeps the `'/'` placeholder.
- `pos.order._asign_add_signature()` – core chained signing flow; called from
  `action_pos_order_paid` and able to back-fill missed paid/done orders (signed strictly
  in `sequence_number` order). Each receipt draws its `asign_seq` inside a per-order
  savepoint, so a signing failure releases the consumed number and leaves no gap. A
  defensive guard (`AsignSequenceError`) aborts if the drawn number is not exactly
  `last signed asign_seq + 1` (tampered sequence / concurrent signer). Cancelled orders
  are never signed.
- All `pos.order.asign_*` fields carry `copy=False` and `_prepare_refund_values` resets
  `name`/`asign_state` – backend refunds (`refund()` uses `copy()`) must not inherit the
  original signature; they draw their own gapless `asign_seq` and are signed as `STO`
  when paid.
- `pos.config._asign_create_zero_receipt()` – produces start/zero receipts required by
  the RKSV (`asign_type` `s` for the very first one, `0` afterwards).
- `pos.config._asign_repair_signed_names()` – restores names of already signed receipts
  whose name was reset to `'/'` by a concurrent cancel (lost-update race); the signature
  stays valid, only the name is recomputed from `asign_seq`. Runs inside
  `_asign_sign_missed`.
- Cron `pos_config_ir_cron` – daily run of `_cron_asign_sign_missed`; back-fills
  unsigned paid/done receipts (cancelled orders are skipped). Processes all matching POS
  regardless of session state; additionally triggered asynchronously by
  `pos.session.action_pos_session_close()`.

## Views & Menus

- POS settings inherit (`res_config_settings_views.xml`) – RKSV section.
- POS list/form inherits (`pos_order_views.xml`) – RKSV signature fields.
- POS receipt inherit (`static/src/overrides/order_receipt.xml`) – prints the RKSV
  receipt number (`order.name`), the QR code, serial and STARTBELEG/NULLBELEG/STORNO
  markers.
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
├── migrations/19.0.1.5.0/post-migration.py   # asign_seq sequence setup
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
│   ├── test_refund.py     # backend refund flow, no copied signature data (mocked)
│   ├── test_dep.py        # gated by `pos_config_id` config
│   ├── test_asign_online.py # gated by `test_asign` config
│   └── regcheck/          # Python wrapper + Java jars (tests-only)
└── views/
```

## Known Pitfalls / Notes

- License is **LGPL-3** to match the other OCA `l10n_at_*` modules.
- In Odoo 19 every order consumes `sequence_number` at create. The RKSV receipt number
  (`asign_seq`) is intentionally a **separate** `no_gap` sequence (`asign_seq_id`)
  consumed only at signing, so a cancelled order – which never gets signed – leaves no
  gap and does not need a zeroed-receipt signature. Existing installs are migrated by
  `migrations/19.0.1.5.0/post-migration.py`, which creates the sequence and continues
  its `number_next` after the highest already signed `asign_seq` (existing signatures
  are kept).
- `test_asign_online.py` and `test_dep.py` carry the `integration` / `-standard` tags
  and additionally check `config.get('test_asign')` / `config.get('pos_config_id')`.
  They are skipped in normal CI runs.
- The `tests/regcheck/regkassen-verification-1.1.1/` folder ships the upstream Java jars
  (~19 MB) needed for DEP verification; they are not loaded at module install but must
  be excluded from any size-sensitive packaging step.
- Anything sent to the A-Trust JWS endpoint requires a configured `asign.cert` with
  `cert_type='online'`, `user`, `password`.
- Neutralized/test databases deactivate all crons (`ir.cron.active = False`), and
  `ir.cron._trigger_list()` silently drops immediate triggers of inactive crons.
  `test_close_session_triggers_cron` therefore re-activates `pos_config_ir_cron` before
  asserting that closing a session creates a trigger.
- `test_rksv_pid` deliberately provokes the per-company unique-index on
  `pos.config.asign_pid` and uses `@mute_logger("odoo.sql_db")` so the expected
  `UniqueViolation` does not leave an `ERROR` line in the log (which would otherwise
  break OCA's `checklog-odoo` CI step).
