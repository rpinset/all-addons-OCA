# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from datetime import timedelta

from psycopg2 import errors

from odoo import api, fields, models

RETENTION_DAYS = 7


class SifendeWebhookEvent(models.Model):
    _name = "l10n_py.sifende.webhook.event"
    _description = "Evento de webhook de Sifende procesado"

    connector_id = fields.Many2one(
        "l10n_py.edi.connector", required=True, index=True, ondelete="cascade"
    )
    event_id = fields.Char(required=True)
    event_type = fields.Char()

    _sql_constraints = [
        (
            "event_unique",
            "unique(connector_id, event_id)",
            "El evento ya fue procesado para este conector.",
        ),
    ]

    @api.model
    def register(self, connector, event_id, event_type):
        """Devuelve False si el evento ya estaba registrado."""
        if self.sudo().search_count(
            [("connector_id", "=", connector.id), ("event_id", "=", event_id)]
        ):
            return False
        # el índice único cubre la carrera entre dos entregas simultáneas
        try:
            with self.env.cr.savepoint():
                self.sudo().create(
                    {
                        "connector_id": connector.id,
                        "event_id": event_id,
                        "event_type": event_type,
                    }
                )
        except errors.UniqueViolation:
            return False
        return True

    @api.autovacuum
    def _gc_processed_events(self):
        limit = fields.Datetime.now() - timedelta(days=RETENTION_DAYS)
        self.sudo().search([("create_date", "<", limit)]).unlink()
