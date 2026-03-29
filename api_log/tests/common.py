# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import contextlib

from odoo.http import Response
from odoo.tests.common import HttpCase

from odoo.addons.website.tools import MockRequest


class Common(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.log_model = cls.env["api.log"]

    @contextlib.contextmanager
    def _mock_request_exc_handling(self, *args, **kwargs):
        """Enhance the standard mock of a request with exception handling."""
        with MockRequest(*args, **kwargs) as mock_request:
            mock_request.dispatcher.handle_error = lambda exc: Response()
            yield mock_request
