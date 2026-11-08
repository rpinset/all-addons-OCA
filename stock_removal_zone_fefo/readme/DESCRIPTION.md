Glue module between `stock_removal_zone_fifo` and `product_expiry`, installed
automatically when both are.

It adds a **Zone-Level FEFO** removal strategy, the expiry-aware counterpart of
Zone-Level FIFO. Goods closest to their removal date are still taken first; the
zone entry date only breaks ties between lots expiring on the same date:

    removal_date, zone_in_date, in_date, id

The standard FEFO strategy is left untouched.
