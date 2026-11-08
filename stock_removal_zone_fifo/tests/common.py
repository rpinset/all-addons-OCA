# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields

from odoo.addons.base.tests.common import BaseCommon


class ZoneFifoCommon(BaseCommon):
    """Two picking zones of two bins each, on a Zone-Level FIFO warehouse."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wh = cls.env["stock.warehouse"].create(
            {"name": "Zone FIFO Warehouse", "code": "ZFIFO"}
        )
        cls.stock_loc = cls.wh.lot_stock_id
        cls.customer_loc = cls.env.ref("stock.stock_location_customers")
        cls.zone_fifo = cls.env.ref("stock_removal_zone_fifo.removal_zone_fifo")

        Location = cls.env["stock.location"]
        cls.zone_a = Location.create(
            {"name": "Zone A", "location_id": cls.stock_loc.id}
        )
        cls.bin_a1 = Location.create({"name": "A1", "location_id": cls.zone_a.id})
        cls.bin_a2 = Location.create({"name": "A2", "location_id": cls.zone_a.id})
        cls.zone_b = Location.create(
            {"name": "Zone B", "location_id": cls.stock_loc.id}
        )
        cls.bin_b1 = Location.create({"name": "B1", "location_id": cls.zone_b.id})
        cls.loc_outside = Location.create(
            {"name": "Outside any zone", "location_id": cls.stock_loc.id}
        )

        # Each of these two locations carries the strategy, so each is a zone.
        # stock_loc stays without one, which leaves loc_outside in no zone.
        (cls.zone_a | cls.zone_b).write({"removal_strategy_id": cls.zone_fifo.id})
        if "is_zone" in Location._fields:
            # stock_removal_zone_fifo_location_zone may be installed, and it
            # then governs the zones. Keep both definitions in agreement.
            (cls.zone_a | cls.zone_b).write({"is_zone": True})

        # On the category, so a reservation over the whole stock sorts with the
        # strategy whatever the bin the goods sit in.
        cls.categ = cls.env["product.category"].create(
            {"name": "Zone FIFO Category", "removal_strategy_id": cls.zone_fifo.id}
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Zone FIFO Product",
                "type": "consu",
                "is_storable": True,
                "categ_id": cls.categ.id,
            }
        )

    @classmethod
    def _make_quant(cls, location, quantity, in_date, zone_in_date=None):
        """Put ``quantity`` in ``location`` with a controlled set of dates."""
        return cls.env["stock.quant"].create(
            {
                "product_id": cls.product.id,
                "location_id": location.id,
                "quantity": quantity,
                "in_date": in_date,
                "zone_in_date": zone_in_date or in_date,
            }
        )

    def _move(self, source, dest, quantity, done=True):
        """Move ``quantity`` from ``source`` to ``dest`` and validate it."""
        move = self.env["stock.move"].create(
            {
                "name": self.product.name,
                "product_id": self.product.id,
                "product_uom_qty": quantity,
                "product_uom": self.product.uom_id.id,
                "location_id": source.id,
                "location_dest_id": dest.id,
            }
        )
        move._action_confirm()
        move._action_assign()
        if done:
            move.move_line_ids.quantity = quantity
            move.picked = True
            move._action_done()
        return move

    def _quant(self, location):
        return self.env["stock.quant"].search(
            [
                ("product_id", "=", self.product.id),
                ("location_id", "=", location.id),
            ]
        )

    @staticmethod
    def _dt(value):
        return fields.Datetime.to_datetime(value)
