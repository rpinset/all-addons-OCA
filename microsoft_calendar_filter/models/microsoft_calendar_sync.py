# Copyright 2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models

from odoo.addons.microsoft_calendar.utils.microsoft_event import MicrosoftEvent

from .res_config_settings import FILTER_PRIVATE_EVENTS


class MicrosoftCalendarSync(models.AbstractModel):
    _inherit = "microsoft.calendar.sync"

    @api.model
    def _sync_microsoft2odoo(self, microsoft_events: MicrosoftEvent):
        ICP = self.env["ir.config_parameter"].sudo()
        filter_private = ICP.get_param(FILTER_PRIVATE_EVENTS)
        # If ICP param set to False or None set_param will delete record.
        if not filter_private:
            return super()._sync_microsoft2odoo(microsoft_events)
        self._remove_private_events(microsoft_events)
        filtered_events = self._filter_microsoft_events(microsoft_events)
        return super()._sync_microsoft2odoo(filtered_events)

    def _remove_private_events(self, microsoft_events):
        """This is to remove events that where public before but now private."""
        private_events = microsoft_events.filter(lambda e: e.sensitivity == "private")
        simple_events = private_events.filter(lambda e: not e.is_recurrence())
        self._remove_events(simple_events)
        recurrent_events = private_events.filter(lambda e: e.is_recurrence())
        self._remove_events(recurrent_events)

    def _remove_events(self, microsoft_events):
        """We need this because _load_odoo_ids_from_db does not accept mixed types."""
        mapped_events = microsoft_events._load_odoo_ids_from_db(self.env)
        for mevent in mapped_events:
            odoo_event = self.browse(mevent.odoo_id(self.env)).exists()
            if odoo_event:
                odoo_event.unlink()

    def _filter_microsoft_events(self, microsoft_events):
        return microsoft_events.filter(lambda e: e.sensitivity != "private")
