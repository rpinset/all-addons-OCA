# Copyright 2026 Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.connector.exception import ConnectorException


class MauticApiError(ConnectorException):
    """Mautic returned an error response for an API call."""

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code
