# Copyright 2020 Camptocamp SA (http://www.camptocamp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from .test_checkout_base import CheckoutCommonCase


# pylint: disable=missing-return
class CheckoutListSetPackageTypeCase(CheckoutCommonCase):
    @classmethod
    def setUpClassBaseData(cls):
        super().setUpClassBaseData()
        cls.env["stock.package.type"].sudo().search([]).active = False
        cls.package_type_pallet = (
            cls.env["stock.package.type"]
            .sudo()
            .create(
                {
                    "name": "Pallet",
                    "barcode": "PPP",
                    "height": 100,
                    "width": 100,
                    "packaging_length": 100,
                    "sequence": 2,
                    "package_carrier_type": False,  # no carrier set on picking
                }
            )
        )
        cls.package_type_box = (
            cls.env["stock.package.type"]
            .sudo()
            .create(
                {
                    "name": "Box",
                    "barcode": "BBB",
                    "height": 20,
                    "width": 20,
                    "packaging_length": 20,
                    "sequence": 1,
                    "package_carrier_type": False,  # no carrier set on picking
                }
            )
        )
        cls.package_type_inner_box = (
            cls.env["stock.package.type"]
            .sudo()
            .create(
                {
                    "name": "Inner Box",
                    "barcode": "III",
                    "height": 10,
                    "width": 10,
                    "packaging_length": 10,
                    "sequence": 0,
                    "package_carrier_type": False,  # no carrier set on picking
                }
            )
        )
        cls.picking = cls._create_picking(lines=[(cls.product_a, 10)])
        cls._fill_stock_for_moves(cls.picking.move_ids, in_package=True)
        cls.picking.action_assign()
        cls.package = cls.picking.move_line_ids.result_package_id
        cls.package.package_type_id = cls.package_type_pallet
        cls.package_types = cls.env["stock.package.type"].search([]).sorted()

    def test_list_package_type_ok(self):
        response = self.service.dispatch(
            "change_list_package_type",
            params={"picking_id": self.picking.id, "package_id": self.package.id},
        )

        self.assert_response(
            response,
            next_state="change_package_type",
            data={
                "picking": self._picking_summary_data(self.picking),
                "package": self._package_data(self.package, self.picking),
                "package_type": [
                    self._package_type_data(package_type)
                    for package_type in self.package_type_inner_box
                    + self.package_type_box
                    + self.package_type_pallet
                ],
            },
        )

    def test_list_package_type_error_package_not_found(self):
        response = self.service.dispatch(
            "change_list_package_type",
            params={"picking_id": self.picking.id, "package_id": 0},
        )
        self.assert_response(
            response,
            next_state="summary",
            data={
                "picking": self._stock_picking_data(self.picking, done=True),
                "all_processed": False,
            },
            message={
                "message_type": "error",
                "body": "The record you were working on does not exist anymore.",
            },
        )

    def test_set_package_type_ok(self):
        response = self.service.dispatch(
            "change_set_package_type",
            params={
                "picking_id": self.picking.id,
                "package_id": self.package.id,
                "package_type_id": self.package_type_inner_box.id,
            },
        )
        self.assertRecordValues(
            self.package, [{"package_type_id": self.package_type_inner_box.id}]
        )
        self.assert_response(
            response,
            next_state="summary",
            data={
                "picking": self._stock_picking_data(self.picking, done=True),
                "all_processed": False,
            },
            message={
                "message_type": "success",
                "body": f"Package type changed on package {self.package.name}",
            },
        )

    def test_set_package_type_error_package_not_found(self):
        response = self.service.dispatch(
            "change_set_package_type",
            params={
                "picking_id": self.picking.id,
                "package_id": 0,
                "package_type_id": self.package_type_inner_box.id,
            },
        )
        self.assert_response(
            response,
            next_state="summary",
            data={
                "picking": self._stock_picking_data(self.picking, done=True),
                "all_processed": False,
            },
            message={
                "message_type": "error",
                "body": "The record you were working on does not exist anymore.",
            },
        )

    def test_set_package_type_error_package_type_not_found(self):
        response = self.service.dispatch(
            "change_set_package_type",
            params={
                "picking_id": self.picking.id,
                "package_id": self.package.id,
                "package_type_id": 0,
            },
        )
        self.assert_response(
            response,
            next_state="summary",
            data={
                "picking": self._stock_picking_data(self.picking, done=True),
                "all_processed": False,
            },
            message={
                "message_type": "error",
                "body": "The record you were working on does not exist anymore.",
            },
        )
