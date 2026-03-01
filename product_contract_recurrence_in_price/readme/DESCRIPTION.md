This module extends the functionality of ``product_contract`` to add an option to compute
the total amounts on "contract" Sale Order lines, including every invoicing planned.

For instance, a product worth 10€ invoiced every month for one year would have a total
of 120€ (unit_price * #invoices) instead of 10€ (unit_price * quantity).
