This module is a glue module between **account_payment_method_base**
and **account_payment_mode**.

In Odoo 18 the module `account_payment_method_base` introduces the
canonical user interface for the model `account.payment.method`,
including:

- form view
- list view
- search view
- menu entry

However `account_payment_mode` historically defined its own base
views for the same model.

This results in two competing base view definitions.

This module rewires the views from `account_payment_mode`
so they inherit from the views provided by
`account_payment_method_base`.

This preserves compatibility with existing modules that inherit:

- `account_payment_mode.account_payment_method_form`
- `account_payment_mode.account_payment_method_tree`
- `account_payment_mode.account_payment_method_search`

while ensuring that `account_payment_method_base` remains the
canonical provider of the payment method UI.
