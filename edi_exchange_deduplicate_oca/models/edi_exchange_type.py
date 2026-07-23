# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EDIExchangeType(models.Model):
    _inherit = "edi.exchange.type"

    deduplicate_on_send = fields.Boolean(
        string="Deduplicate on Send",
        default=False,
        help="Before sending an exchange record, check if a fresher one does not "
        "exist for same record; if so, mark oldest one as obsolete.",
    )
    delete_obsolete_records = fields.Boolean(
        string="Delete obsolete records",
        default=True,
        help="Delete records marked as obsolete.",
    )

    deduplicate_on_exchange_record_status = fields.Char(
        default="new,output_pending",
        groups="base.group_no_one",
    )

    def _deduplicate_get_exchange_record_states(self):
        self.ensure_one()
        configured_states = self.sudo().deduplicate_on_exchange_record_status or ""
        return {
            state.strip() for state in configured_states.split(",") if state.strip()
        }

    @api.constrains("deduplicate_on_exchange_record_status")
    def _check_deduplicate_on_exchange_record_status(self):
        exchange_state_field = self.env["edi.exchange.record"]._fields[
            "edi_exchange_state"
        ]
        allowed_states = set(exchange_state_field.get_values(self.env))
        for rec in self:
            configured_states = rec._deduplicate_get_exchange_record_states()
            invalid_states = sorted(configured_states - allowed_states)
            if invalid_states:
                raise ValidationError(
                    self.env._(
                        "Invalid exchange state(s): %(invalid_states)s. "
                        "Allowed values are: %(allowed_states)s",
                        invalid_states=", ".join(invalid_states),
                        allowed_states=", ".join(sorted(allowed_states)),
                    )
                )
