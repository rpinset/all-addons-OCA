# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo_test_helper import FakeModelLoader

from odoo.tools import mute_logger

from odoo.addons.shopfloor_reception.tests.common import CommonCase


class TestSetPackDimension(CommonCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.menu.sudo().set_packaging_dimension = True
        cls.wh = cls.env.ref("stock.warehouse0")
        cls.setUpClassPackaging()
        cls.setUpComponentRegistry()

    def setUp(self):
        super().setUp()
        self.loader = FakeModelLoader(self.env, self.__module__)
        self.loader.backup_registry()

        from .device_model import MeasuringModel

        self.loader.update_registry((MeasuringModel,))
        self.device_model = self.env["measuring.device"].sudo()
        self.device = self.device_model.create(
            {
                "name": "Test Device",
                "device_type": "testdevice",
                "state": "ready",
                "warehouse_id": self.wh.id,
            }
        )

    def tearDown(self):
        self.loader.restore_registry()
        return super().tearDown()

    @classmethod
    def setup_picking(cls):
        return cls._create_picking(lines=[(cls.product_c, 10)])

    @classmethod
    def setUpComponentRegistry(cls):
        from .device_component import MeasuringComponent

        MeasuringComponent._build_component(cls._components_registry)

    @classmethod
    def setUpClassPackaging(cls):
        cls.packaging1 = cls.product_c.packaging_ids
        cls.packaging2 = (
            cls.env["product.packaging"]
            .sudo()
            .create(
                {
                    "name": "Big Box",
                    "product_id": cls.product_c.id,
                    "barcode": "ProductCBigBox",
                    "qty": 6,
                }
            )
        )

    def _assert_response_set_dimension(
        self, response, picking, line, packaging, message=None
    ):
        data = {
            "picking": self.data.picking(picking),
            "selected_move_line": self.data.move_line(line),
            "packaging": self.data_detail.packaging_detail(packaging),
        }
        self.assert_response(
            response,
            next_state="set_packaging_dimension",
            data=data,
            message=message,
        )

    def test_select_device__no_device(self):
        picking = self.setup_picking()
        line = picking.move_line_ids[0]
        # Unlink device so none is found
        self.device.unlink()
        response = self.service.dispatch(
            "set_packaging_dimension__measuring_device_assign",
            params={
                "picking_id": picking.id,
                "selected_line_id": line.id,
                "packaging_id": self.packaging1.id,
            },
        )
        self._assert_response_set_dimension(
            response,
            picking,
            line,
            self.packaging1,
            message=self.msg_store.no_measuring_device_found(),
        )

    def test_select_device__device_already_assigned(self):
        picking = self.setup_picking()
        line = picking.move_line_ids[0]
        # assign measuring device to packaging2, so it cannot be selected again
        self.packaging2._measuring_device_assign(self.device)
        response = self.service.dispatch(
            "set_packaging_dimension__measuring_device_assign",
            params={
                "picking_id": picking.id,
                "selected_line_id": line.id,
                "packaging_id": self.packaging1.id,
            },
        )
        self._assert_response_set_dimension(
            response,
            picking,
            line,
            self.packaging1,
            message=self.msg_store.measuring_device_already_in_use(self.device),
        )

    @mute_logger("odoo.addons.stock_measuring_device.models.measuring_device")
    def test_select_device__ok(self):
        picking = self.setup_picking()
        line = picking.move_line_ids[0]
        response = self.service.dispatch(
            "set_packaging_dimension__measuring_device_assign",
            params={
                "picking_id": picking.id,
                "selected_line_id": line.id,
                "packaging_id": self.packaging1.id,
            },
        )
        packaging = self.packaging1
        data = {
            "picking": self.data.picking(picking),
            "selected_move_line": self.data.move_line(line),
            "packaging": self.data_detail.packaging_detail(packaging),
            "measuring_device": self.data.measuring_device(
                packaging.measuring_device_id
            ),
        }
        self.assert_response(
            response,
            next_state="use_measuring_device",
            data=data,
        )
        self.assertEqual(self.packaging1.measuring_device_id, self.device)
        measurements = {
            "weight": 42,
            "height": 43,
            "packaging_length": 44,
            "width": 45,
        }
        measured_packaging = self.device._update_packaging_measures(measurements)
        self.assertEqual(measured_packaging, self.packaging1)
        self.assertEqual(measured_packaging.weight, 42)
        self.assertEqual(measured_packaging.height, 43)
        self.assertEqual(measured_packaging.packaging_length, 44)
        self.assertEqual(measured_packaging.width, 45)

    def test_release_device__no_device_assigned(self):
        picking = self.setup_picking()
        line = picking.move_line_ids[0]
        response = self.service.dispatch(
            "set_packaging_dimension__measuring_device_release",
            params={
                "picking_id": picking.id,
                "selected_line_id": line.id,
                "packaging_id": self.packaging1.id,
            },
        )
        self._assert_response_set_dimension(
            response,
            picking,
            line,
            self.packaging1,
            message=self.msg_store.no_measuring_device_to_release(self.packaging1),
        )

    def test_release_device__ok(self):
        picking = self.setup_picking()
        line = picking.move_line_ids[0]
        # Assign device to the packaging so it can be released
        self.packaging1._measuring_device_assign(self.device)
        response = self.service.dispatch(
            "set_packaging_dimension__measuring_device_release",
            params={
                "picking_id": picking.id,
                "selected_line_id": line.id,
                "packaging_id": self.packaging1.id,
            },
        )
        self._assert_response_set_dimension(
            response,
            picking,
            line,
            self.packaging1,
            message=self.msg_store.measuring_device_released(
                self.packaging1, self.device
            ),
        )
        self.assertFalse(self.packaging1.measuring_device_id)
