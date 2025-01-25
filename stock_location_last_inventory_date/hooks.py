# Copyright 2024 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
import logging

logger = logging.getLogger(__name__)


def set_initial_last_inventory_date(cr):
    cr.execute(
        """
    Update
        stock_location
    set
        last_inventory_date = sub.date
    from (
        Select
            line.location_id,
            max(inventory.date) as date
        from
            stock_inventory_line as line
        join
            stock_inventory as inventory
        on
            inventory.id = line.inventory_id
        group by
            line.location_id
    ) as sub
    where
        stock_location.id = sub.location_id;
    """
    )


def post_init_hook(cr, registry):
    logger.info("Calculate last inventory date for locations")
    set_initial_last_inventory_date(cr)
