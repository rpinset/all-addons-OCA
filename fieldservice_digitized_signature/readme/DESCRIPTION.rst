This module adds a digitized signature to Field Service orders.

Field Service does not provide a native signature field on its orders. This
module fills that gap by adding, on ``fsm.order``:

* a **Signature** field captured through Odoo's web sign widget,
* the name of the person who signed (**Signed By**),
* the date and time the order was signed (**Signed On**).

The captured signature is also printed on the Field Service order report.
