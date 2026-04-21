# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from contextlib import contextmanager
from unittest.mock import MagicMock

from odoo.tests.common import TransactionCase


class Common(TransactionCase):
    @contextmanager
    def _mock_method(self, method_name, method_obj=None):
        if method_obj is None:
            method_obj = self.record
        magic = MagicMock()
        self.patch(type(self.record), method_name, magic)
        yield magic
