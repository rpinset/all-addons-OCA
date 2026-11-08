Glue module between `stock_removal_zone_fifo` and `stock_location_zone`,
installed automatically when both are.

`stock_removal_zone_fifo` takes a zone to be the nearest ancestor location
carrying the Zone-Level FIFO strategy. This module overrides
`stock.location._get_zone_location` to use the zones of `stock_location_zone`
instead, so the goods keep their zone entry date while they stay under the same
location flagged `Is a Zone Location?`.

Install it when the zones of your warehouse do not line up with the locations you
set the removal strategy on. It takes the definition over entirely: a location
under nothing flagged `Is a Zone Location?` is then in no zone, whatever removal
strategy its ancestors carry. Flag your zones before installing it.
