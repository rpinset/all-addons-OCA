# Sale Order Blanket Order — Carrier Auto Assign Compatibility

Glue module reconciling
[`sale_order_blanket_order`](https://github.com/OCA/sale-blanket) and
[`sale_order_carrier_auto_assign`](https://github.com/OCA/sale-workflow).

## Problem

When `sale_order_carrier_auto_assign` is installed, both blanket orders and
call-off orders receive an auto-assigned carrier delivery-fee line. Without
this module, the delivery-fee line participates in the blanket-order call-off
matching algorithm: each call-off's delivery line "consumes" capacity from
the blanket order's delivery line. After the first call-off, the blanket's
delivery line has zero remaining capacity, so the second call-off fails
confirmation with:

> The product is not part of linked blanket order

## What this module does

It excludes `is_delivery` sale order lines from the blanket-order line
matching algorithm and from the call-off → blanket stock-rule forwarding,
so delivery-fee lines never participate in blanket call-off accounting.

## Bypass switch

The filter can be turned off by setting the context key
`skip_blanket_carrier_filter=True`. The regression test uses this flag to
demonstrate that the original failure mode reappears when the filter is
disabled.
