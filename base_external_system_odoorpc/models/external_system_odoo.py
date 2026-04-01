# Copyright 2026 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from urllib.error import URLError

import odoorpc

from odoo import _, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ExternalSystemOdoo(models.Model):
    """This is an Interface implementing the RPC module."""

    _name = "external.system.odoo"
    _inherit = "external.system.adapter"
    _description = "External System RPC"

    def external_get_client(self):
        """Return a usable client representing the remote system."""
        self.ensure_one()
        return self._connect()

    def external_destroy_client(self, client):
        """Cleanup the client connection"""
        self.ensure_one()
        try:
            if client:
                client.logout()
        except Exception as exc:
            _logger.debug(
                "Failed to logout OdooRPC client for %s: %s", self.display_name, exc
            )
        return super().external_destroy_client(client)

    def external_test_connection(self):
        """Test connection in the UI."""
        self.ensure_one()
        try:
            with self.client() as odoo:
                model_data_model = odoo.env["ir.model.data"]
                # search_read actually gives us fewer
                # RPC calls here.
                # better than search() + browse()
                res = model_data_model.search_read(
                    [
                        ("module", "=", "base"),
                        ("name", "=", "user_admin"),
                    ],
                    ["res_id"],
                    limit=1,
                )
                if not res or not res[0].get("res_id"):
                    raise ValidationError(
                        _("Connected, but could not find admin user.")
                    )
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(_("Connection failed.\n\nDETAIL: %s") % e) from e
        return super().external_test_connection()

    def _connect(self):
        """Return connection object"""
        self.ensure_one()
        if not all([self.host, self.port, self.db_name, self.username, self.password]):
            raise ValidationError(
                _(
                    "Connection failed. Please make sure that all fields "
                    "are filled: Database, Host, Port, Username, Password."
                )
            )
        try:
            odoo = odoorpc.ODOO(
                self.host,
                port=self.port,
                protocol="jsonrpc+ssl" if self.is_ssl else "jsonrpc",
            )
        except URLError as exc:
            raise ValidationError(
                _("Could not connect the Odoo server at %(host)s:%(port)s")
                % {"host": self.host, "port": self.port}
            ) from exc
        odoo.login(self.db_name, self.username, self.password)
        return odoo
