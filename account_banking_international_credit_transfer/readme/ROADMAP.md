- Add support for additional PAIN versions
- Extract common parts of `account_banking_international_credit_transfer`
  and `account_banking_sepa_credit_transfer` into a dedicated base module
  (e.g. `account_banking_base_credit_transfer`), or
- Add overridable hooks in `account_banking_sepa_credit_transfer` so that
  `account_banking_international_credit_transfer` can simply inherit
  and extend it instead of duplicating the implementation.

