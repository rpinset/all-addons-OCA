Set `Zone-Level FIFO` as the removal strategy of the parent location of each
picking zone. That location *is* the zone: every location under it belongs to it,
up to the next descendant carrying the strategy.

Do not set a removal strategy on the locations inside a zone: the nearest one
carrying it wins, so such a location would become a zone of its own.

Setting the strategy on a **product category** only chooses how the quants are
sorted, it never defines a zone. A category-level Zone-Level FIFO is therefore
pointless on its own: without the strategy on at least one location, no zone
exists, `zone_in_date` is never updated and the sort falls back on `in_date`.
Use the category to apply the strategy warehouse-wide, and the locations to draw
the zones.

Goods moved to a location that is in no zone keep their zone entry date, since
no zone sorts them there. Tick `Update Zone Entry Date out of Zones` in the
Inventory settings to give them the move date instead.

Goods entering a zone from a location in no zone always get a fresh date: once
out of every zone, nothing tells which zone they came from, so Zone A -> Packing
-> Zone B must count as a change of zone.
