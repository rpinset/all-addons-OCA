The standard is_shipped field shows information about the status
of the shipments and invoices related to a Purchase Order.

However, it can happen that the field is_shipped is marked as True while some of the shipments
were cancelled. Because of this, this module introduces a new field that will show
wether a purchase order is fully shipped or not.
