After installing the module, the views defined in
`account_payment_mode` will inherit from the base views provided by
`account_payment_method_base`.

No functional changes are introduced.

The module only ensures a consistent view inheritance chain between
the two addons and keeps compatibility with downstream modules that
inherit the original view XML IDs from `account_payment_mode`.
