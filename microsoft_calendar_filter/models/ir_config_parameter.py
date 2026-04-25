# Copyright 2026 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
"""Checks on the filter_odoo_events parameter from this module.

We do the check on the underlying model of ir.config_parameter,
rather then on res.config.settings, to make sure no invalid value
enters the database through set_param or direct create/write.
Direct SQL and internal _create or _write are not covered.
"""

from odoo import _, api, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval

from .res_config_settings import FILTER_ODOO_EVENTS


class IrConfigParameter(models.Model):
    _inherit = "ir.config_parameter"

    @api.constrains("key", "value")
    def _check_filter_odoo_events(self):
        """Validate value for filter_odoo_events if present."""
        for record in self.filtered(lambda r: r.key == FILTER_ODOO_EVENTS and r.value):
            domain_text = str(record.value).strip()
            if domain_text not in ("", "[]"):
                try:
                    domain = safe_eval(domain_text)
                    Calendar = self.env["calendar.event"]
                    # Search does not need to return records, but must be valid.
                    Calendar.search(domain, limit=1)
                except Exception as exc:
                    message = exc.msg if hasattr(exc, "msg") else str(exc)
                    raise ValidationError(
                        _(
                            "Domain %(domain_text)s is invalid: %(message)s",
                            domain_text=domain_text,
                            message=message,
                        )
                    ) from exc
