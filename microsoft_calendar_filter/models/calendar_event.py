# Copyright 2026 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models
from odoo.osv.expression import AND
from odoo.tools.safe_eval import safe_eval

from .res_config_settings import FILTER_ODOO_EVENTS


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    def _extend_microsoft_domain(self, domain):
        """Only need this for simple calendar.event.

        Recurrent events are not sent to Outlook anyway.
        """
        extended_domain = super()._extend_microsoft_domain(domain)
        ICP = self.env["ir.config_parameter"].sudo()
        extra_filter = ICP.get_param(FILTER_ODOO_EVENTS)
        domain_text = extra_filter.strip() if extra_filter else ""
        if domain_text in ("", "[]"):
            return extended_domain
        filter_domain = safe_eval(domain_text)
        return AND([extended_domain, filter_domain])
