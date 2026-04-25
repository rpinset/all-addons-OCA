# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class RepairService(models.Model):
    """Override service line creation to support grouped repairs.

    When services belong to grouped repairs, they are created exclusively
    through the `_post_create_grouped_hook()` in repair_order_group_service.
    This prevents duplicate service lines in sale orders.
    """

    _inherit = "repair.service"

    def _create_repair_sale_order_line(self):
        """Create sale order lines for repair services.

        Behavior depends on the call context:
        - When called with `from_group_hook=True` (from grouped repair hook):
          Creates lines for ALL services, including those from grouped repairs.
        - When called normally (from repair_service module):
          Creates lines ONLY for services belonging to UNGROUPED repairs.
          Services from grouped repairs are skipped to avoid duplicates,
          as they are already handled by the grouped repair hook.
        """
        # Call from grouped repair hook: process all services
        if self.env.context.get("from_group_hook"):
            return super()._create_repair_sale_order_line()

        # Standard call from repair_service: process only ungrouped repairs
        ungrouped_services = self.filtered(lambda s: not s.repair_id.group_id)
        if ungrouped_services:
            return super(
                RepairService, ungrouped_services
            )._create_repair_sale_order_line()
