This module allows to force the reservation of expired lots with:

- a configuration option (at the company level)
- a context key

## Configuration option (global)

Open Inventory settings (*Inventory/Configuration/Settings*), section *Traceability*, and enable option *Ignore Expiration Date*.

## With context key (code)

Before calling `<stock.move>._action_confirm()` or `<stock.move>._action_assign()`,
one could set the `ignore_expiration_date` context key:

```python
move_expired_lot._action_assign()
assert move_expired_lot.state == "confirmed"
move_expired_lot.with_context(ignore_expiration_date=True)._action_assign()
assert move_expired_lot.state == "assigned"
```
