This module works around some issues of the localization. Each workaround can be removed
once the issue is fixed upstream:

- The asynchronous provider contract: this module overrides `_process_edi_response` and runs
  its own status cron ([#97](https://github.com/OCA/l10n-paraguay/issues/97), see also
  [#33](https://github.com/OCA/l10n-paraguay/pull/33)).
- Receiver ID type and delivery note motive are translated to the SIFEN codes here
  ([#89](https://github.com/OCA/l10n-paraguay/issues/89),
  [#92](https://github.com/OCA/l10n-paraguay/issues/92)). When those are fixed upstream, the
  translation tables must go in the same release.
- Department and city are resolved by name against the SIFEN catalog shipped with this module
  ([#85](https://github.com/OCA/l10n-paraguay/issues/85),
  [#86](https://github.com/OCA/l10n-paraguay/issues/86)).
- The partner form shows the identity document fields
  ([#87](https://github.com/OCA/l10n-paraguay/issues/87)).
- Transport: carrier fields, freight responsibility 5 and creation from the invoice
  ([#93](https://github.com/OCA/l10n-paraguay/issues/93),
  [#94](https://github.com/OCA/l10n-paraguay/issues/94)).
- Payment terms, item prices with VAT and discount, unit of measure code, and number voiding
  ([#95](https://github.com/OCA/l10n-paraguay/issues/95),
  [#96](https://github.com/OCA/l10n-paraguay/issues/96),
  [#98](https://github.com/OCA/l10n-paraguay/issues/98)).
- The extra keys this module adds to the document dict under `sifende` (issuance motive, unit
  of measure, discounts, email and customer code) should become part of the
  `l10n_py_edi_base` contract, so every provider shares them.
