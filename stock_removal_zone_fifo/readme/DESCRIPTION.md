The standard FIFO removal strategy sorts the quants by incoming date
(`in_date`). That date is set when the goods are received and follows them from
location to location, so it cannot tell when they arrived in the zone they are
stored in: a pallet received long ago and only now brought down to a picking
area keeps its old incoming date, and the picker is sent to it before the stock
that has been sitting in that area for weeks.

This module adds a **Zone-Level FIFO** removal strategy. It keeps the FIFO
principle but sorts on a new `Zone Entry Date` (`zone_in_date`) field on the
quant, falling back on the incoming date:

    zone_in_date, in_date, id

`zone_in_date` changes only when the goods enter another zone, unlike `in_date`
which a merge of stock or an inventory adjustment can move. A zone is the nearest
ancestor location carrying the strategy. It is always set, so the sort above
needs no NULL handling.
