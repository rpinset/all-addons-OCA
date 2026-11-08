A zone is the nearest ancestor location, itself included, whose removal strategy
is zone-based. `stock.location._get_zone_location()` resolves it, and
`_zone_removal_strategies()` lists the strategy methods that define one — a
module adding another zone-based strategy extends that list.

An extension module defining the zones differently overrides
`_get_zone_location` on `stock.location`:

```python
def _get_zone_location(self):
    return <the zone of this location> or super()._get_zone_location()
```

`stock.location._is_same_zone(source_zone, destination_zone)` decides what counts
as staying put: `True` keeps the date of the goods, `False` updates it. A
destination in no zone answers `True`, unless the company setting
`zone_in_date_update_out_of_zone` is on. Override it to change that rule.

When the destination location already holds stock, the returned date competes
with the one already stored and the oldest of the two wins, so arriving goods
never push the ones already there back in the queue. This mirrors the way the
core keeps the oldest `in_date` when it merges stock into an existing quant.
