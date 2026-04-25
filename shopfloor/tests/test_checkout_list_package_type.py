# Copyright 2021 Camptocamp SA (http://www.camptocamp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo_test_helper import FakeModelLoader

from .test_checkout_base import CheckoutCommonCase
from .test_checkout_select_package_base import CheckoutSelectPackageMixin


# pylint: disable=missing-return
class CheckoutListDeliveryPackagingCase(CheckoutCommonCase, CheckoutSelectPackageMixin):
    def setUp(self):
        super().setUp()
        self.loader = FakeModelLoader(self.env, self.__module__)
        self.loader.backup_registry()

        from .models import DeliveryCarrierTest, StockPackageType

        self.loader.update_registry((DeliveryCarrierTest, StockPackageType))

        self.carrier = self.env["delivery.carrier"].search([], limit=1)
        self.carrier.sudo().delivery_type = "test"
        self.picking = self._create_picking(
            lines=[
                (self.product_a, 10),
                (self.product_b, 10),
                (self.product_c, 10),
                (self.product_d, 10),
            ]
        )
        self.picking.carrier_id = self.carrier
        self.packaging_type = (
            self.env["product.packaging.level"]
            .sudo()
            .create({"name": "Transport Box", "code": "TB", "sequence": 0})
        )
        self.package_type1 = (
            self.env["stock.package.type"]
            .sudo()
            .create(
                {
                    "name": "Box 1",
                    "package_carrier_type": "test",
                    "barcode": "BOX1",
                }
            )
        )
        self.package_type2 = (
            self.env["stock.package.type"]
            .sudo()
            .create(
                {
                    "name": "Box 2",
                    "package_carrier_type": "test",
                    "barcode": "BOX2",
                }
            )
        )
        self.package_type = (self.package_type1 | self.package_type2).sorted("name")

    def tearDown(self):
        self.loader.restore_registry()
        super().tearDown()

    def test_list_package_type_available(self):
        self._fill_stock_for_moves(self.picking.move_ids, in_package=True)
        self.picking.action_assign()
        selected_lines = self.picking.move_line_ids
        response = self.service.dispatch(
            "list_package_type",
            params={
                "picking_id": self.picking.id,
                "selected_line_ids": selected_lines.ids,
            },
        )
        self.assert_response(
            response,
            next_state="select_package_type",
            data={
                "package_type": self.service.data.package_type_list(self.package_type),
            },
        )

    def test_list_package_type_not_available(self):
        self.package_type.package_carrier_type = False
        self._fill_stock_for_moves(self.picking.move_ids, in_package=True)
        self.picking.action_assign()
        selected_lines = self.picking.move_line_ids
        response = self.service.dispatch(
            "list_package_type",
            params={
                "picking_id": self.picking.id,
                "selected_line_ids": selected_lines.ids,
            },
        )
        self.assert_response(
            response,
            next_state="select_package",
            data={
                "picking": self._picking_summary_data(self.picking),
                "selected_move_lines": [
                    self._move_line_data(ml) for ml in selected_lines.sorted()
                ],
                "packing_info": self.service._data_for_packing_info(self.picking),
                "no_package_enabled": not self.service.options.get(
                    "checkout__disable_no_package"
                ),
                "package_allowed": True,
            },
            message=self.service.msg_store.no_package_type_available(),
        )
