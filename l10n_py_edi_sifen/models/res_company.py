# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import base64
import logging

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_py_certificate = fields.Binary("Certificado PKCS12 (.pfx)")
    l10n_py_certificate_filename = fields.Char()
    l10n_py_certificate_password = fields.Char("Contraseña del Certificado")
    l10n_py_certificate_expiry = fields.Date("Expiración", readonly=True)

    def _get_pkcs12_data(self):
        """Return (cert_bytes, password) for SIFEN mTLS."""
        self.ensure_one()
        if not self.l10n_py_certificate:
            raise UserError(
                _("Configure el certificado PKCS12 en la empresa %s") % self.name
            )
        cert_bytes = base64.b64decode(self.l10n_py_certificate)
        return cert_bytes, self.l10n_py_certificate_password or ""
