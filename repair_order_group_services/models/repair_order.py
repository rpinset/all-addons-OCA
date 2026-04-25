# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class RepairOrder(models.Model):
    """Bridge module between repair_order_group and repair_service.

    Ensures service lines from all repairs in a group are added to the
    sale order when a quotation is created from a grouped repair.
    """

    _inherit = "repair.order"

    def _post_create_grouped_hook(self):
        """Extend grouped sale order creation with service lines.

        Called by repair_order_group after sale orders are created for
        grouped repairs. Adds service lines from all repairs in the group
        using the `from_group_hook` context to distinguish from standard
        service creation flow.

        Returns:
            The result of the parent method (if any).
        """
        result = super()._post_create_grouped_hook()

        # Add service lines with context flag to indicate grouped repair flow
        self.repair_service_ids.with_context(
            from_group_hook=True
        )._create_repair_sale_order_line()

        return result
