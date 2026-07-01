# Copyright 2024 Weboffice IT-Service und Marketing GmbH & Co KG <https://weboffice.at>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError


class AsignCert(models.Model):
    _name = "asign.cert"
    _description = "a.sign Certificate"

    _unique_serial_hex = models.UniqueIndex(
        "(serial_hex) WHERE (serial_hex IS NOT NULL)",
        "Serial number has to be unique",
    )

    name = fields.Char(string="Serial (Hex)", required=True)
    serial_hex = fields.Char(
        string="Serial (Normalized)",
        index=True,
        store=True,
        compute="_compute_serial_hex",
        help="Serial number of the certificate in normalized hex format.",
    )
    cert = fields.Binary(
        string="Certificate",
        help="Public certificate of the signing card or online service.",
    )
    cert_name = fields.Char(compute="_compute_cert_name")
    cert_type = fields.Selection(
        [
            ("online", "Online"),
            ("card", "Card"),
        ],
        default="online",
        required=True,
    )
    user = fields.Char()
    password = fields.Char()
    active = fields.Boolean(default=True)

    @api.depends("serial_hex")
    def _compute_cert_name(self):
        for cert in self:
            cert.cert_name = f"{cert.serial_hex}.cer" if cert.serial_hex else "cert.cer"

    @api.depends("name")
    def _compute_serial_hex(self):
        for cert in self:
            cert.serial_hex = f"{int(cert.name, 16):x}" if cert.name else ""

    @api.model
    def _get_cert(self, serial_hex, raise_if_not_found=True):
        cert = self.search([("serial_hex", "=", serial_hex)], limit=1)
        if not cert and raise_if_not_found:
            raise ValidationError(
                self.env._("No certificate found for serial %s", serial_hex)
            )
        return cert

    @tools.ormcache("serial_hex")
    def _get_login(self, serial_hex):
        cert = self._get_cert(serial_hex)
        return cert.user, cert.password
