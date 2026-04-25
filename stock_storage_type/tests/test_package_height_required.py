# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.exceptions import ValidationError

from .common import TestStorageTypeCommon


class TestStorageTypeMove(TestStorageTypeCommon):
    def test_package_storage_type_height_not_required(self):
        packaging = self.product_lot_pallets_product_packaging
        storage_type = packaging.package_type_id
        storage_type.height = 0
        self.env["stock.quant.package"].create(
            {"name": "TEST1", "product_packaging_id": packaging.id}
        )

    def test_package_storage_type_height_required(self):
        packaging = self.product_lot_pallets_product_packaging
        storage_type = packaging.package_type_id
        storage_type.height_required = True
        with self.assertRaises(ValidationError):
            self.env["stock.quant.package"].create(
                {"name": "TEST2", "product_packaging_id": packaging.id}
            )

    def test_package_height_copied_from_package_type(self):
        packaging = self.product_lot_pallets_product_packaging
        packaging.height = 0
        storage_type = packaging.package_type_id
        storage_type.height_required = True
        storage_type.height = 333
        package = self.env["stock.quant.package"].create(
            {"name": "TEST1", "product_packaging_id": packaging.id}
        )
        self.assertEqual(package.height, 333)

    def test_package_height_copied_from_packaging(self):
        packaging = self.product_lot_pallets_product_packaging
        packaging.height = 444
        storage_type = packaging.package_type_id
        storage_type.height_required = True
        storage_type.height = 333
        package = self.env["stock.quant.package"].create(
            {"name": "TEST1", "product_packaging_id": packaging.id}
        )
        self.assertEqual(package.height, 444)
