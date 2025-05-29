# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

# from odoo.http import controllers_per_module
from odoo.http import Controller

from ..controllers.main import (
    BaseRestDemoJwtApiController,
    BaseRestDemoNewApiController,
    BaseRestDemoPrivateApiController,
    BaseRestDemoPublicApiController,
)
from .common import CommonCase


class TestController(CommonCase):
    def test_controller_registry(self):
        # at the end of the start process, our tow controllers must into the
        # controller registered
        controllers = Controller.children_classes.get("base_rest_demo", [])
        self.assertTrue(
            any([issubclass(x, BaseRestDemoPrivateApiController) for x in controllers])
        )
        self.assertTrue(
            any([issubclass(x, BaseRestDemoPublicApiController) for x in controllers])
        )
        self.assertTrue(
            any([issubclass(x, BaseRestDemoNewApiController) for x in controllers])
        )
        self.assertTrue(
            any([issubclass(x, BaseRestDemoJwtApiController) for x in controllers])
        )
