In many business flows, a returned product must be linked back to the original
sale in order to validate warranty conditions, refunds or exchanges.

Manually searching the correct sale order for each RMA is error-prone and time
consuming, especially when:

- the customer has multiple past orders
- the product was delivered in several partial shipments
- the return period depends on the type of RMA operation (refund, warranty, lifetime, etc.)

This module introduces an **automatic matching engine** that links RMA records
to the correct delivery moves of the original sale order, based on delivered
quantities and eligibility period.

It avoids manual reconciliation and provides a deterministic, auditable match.