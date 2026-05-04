# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import logging

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class EDIConnector(models.Model):
    _name = "l10n_py.edi.connector"
    _description = "Conector EDI Paraguay"

    name = fields.Char(required=True)
    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
    )
    provider_type = fields.Selection(
        selection=[],
        string="Proveedor",
        required=True,
    )
    environment = fields.Selection(
        [("test", "Pruebas"), ("prod", "Producción")],
        default="test",
        required=True,
    )
    active = fields.Boolean(default=True)
    timeout = fields.Integer(default=30)

    _sql_constraints = [
        (
            "company_unique",
            "unique(company_id)",
            "Solo un conector EDI por empresa",
        ),
    ]

    # === Public interface (each provider must implement) ===

    def send_document(self, invoice_data):
        """Send document. Returns dict with success, result, error keys."""
        self.ensure_one()
        raise UserError(
            _("El proveedor '%s' no implementa el envío de documentos")
            % self.provider_type
        )

    def check_status(self, document_id):
        """Check document status."""
        self.ensure_one()
        raise UserError(
            _("El proveedor '%s' no implementa la consulta de estado")
            % self.provider_type
        )

    def cancel_document(self, document_id, reason=""):
        """Cancel an approved document."""
        self.ensure_one()
        raise UserError(
            _("El proveedor '%s' no implementa la cancelación") % self.provider_type
        )

    def preview_document(self, invoice_data):
        """Build XML without signing or sending. Returns XML string."""
        self.ensure_one()
        raise UserError(
            _("El proveedor '%s' no implementa la previsualización")
            % self.provider_type
        )

    def inutilize_range(self, data):
        """Inutilize a range of document numbers. Returns dict."""
        self.ensure_one()
        raise UserError(
            _("El proveedor '%s' no implementa la inutilización") % self.provider_type
        )

    def test_connection(self):
        """Test connectivity. Returns notification action."""
        self.ensure_one()
        raise UserError(
            _("El proveedor '%s' no implementa la prueba de conexión")
            % self.provider_type
        )
