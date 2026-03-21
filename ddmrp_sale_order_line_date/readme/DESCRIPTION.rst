Extends *DDMRP Sale* to use the delivery date set on each individual sale
order line (provided by the *Sale Order Line Date* module) instead of the
order-level delivery date when computing qualified demand for DDMRP buffers.

Install this module when different lines of the same sales order may have
different delivery dates and you want buffers to react to the per-line date
rather than the global order date.
