# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.component.core import Component
from odoo.addons.shopfloor_base.utils import ensure_model


class DataAction(Component):
    _inherit = "shopfloor.data.action"

    @ensure_model("measuring.device")
    def measuring_device(self, record, **kw):
        return self._jsonify(
            record.with_context(device=record.id), self._measuring_device_parser, **kw
        )

    @property
    def _measuring_device_parser(self):
        return self._simple_record_parser()
