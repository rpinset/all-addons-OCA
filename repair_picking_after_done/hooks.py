# Copyright 2024 Patryk Pyczko (APSL-Nagarro)<ppyczko@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.repair.models.stock_move import StockMove


def post_load_hook():
    """
    This hook modifies the stock move splitting logic to:
    - Allow splitting stock moves related to repair
    orders that are marked as "done", which is prevented
    by the core Odoo logic.
    - This change enables the creation of backorders for
    these split stock moves when the associated repair is completed.
    """

    def _split_for_repair_custom(self, qty, restrict_partner_id=False):
        if self.repair_id and self.repair_id.state != "done":
            return []

        return super(StockMove, self)._split(qty, restrict_partner_id)

    if not hasattr(StockMove, "_split_original"):
        StockMove._split_original = StockMove._split
    StockMove._split = _split_for_repair_custom
