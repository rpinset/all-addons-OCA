# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import Form

from odoo.addons.rma.tests.test_rma import TestRma


class TestRmaLotAutocreate(TestRma):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.op_lot_seq = cls.env.ref("rma_lot_autocreate.seq_rma_lot_number")
        cls.operation.lot_sequence_id = cls.op_lot_seq
        cls.operation.auto_create_lot = True
        cls.product_tracked_lot = cls.env["product.product"].create(
            {
                "name": "Tracked by lot",
                "type": "product",
                "tracking": "lot",
                "use_expiration_date": True,
            }
        )
        cls.product_tracked_serial = cls.env["product.product"].create(
            {
                "name": "Tracked by serial",
                "type": "product",
                "tracking": "serial",
            }
        )
        cls.product_untracked = cls.env["product.product"].create(
            {
                "name": "Untracked",
                "type": "product",
                "tracking": "none",
            }
        )

    def test_auto_creates_lot_on_confirm_for_lot_tracked(self):
        rma = self._create_rma(self.partner, self.product_tracked_lot)
        self.assertFalse(rma.lot_id)
        rma.action_confirm()
        self.assertTrue(rma.lot_id)
        self.assertEqual(rma.lot_id.product_id, self.product_tracked_lot)
        self.assertIn("RMA", rma.lot_id.name)

    def test_auto_creates_lot_on_confirm_for_serial_tracked(self):
        rma = self._create_rma(self.partner, self.product_tracked_serial)
        rma.action_confirm()
        self.assertTrue(rma.lot_id)
        self.assertIn("RMA", rma.lot_id.name)

    def test_does_nothing_if_flag_disabled(self):
        self.operation.auto_create_lot = False
        rma = self._create_rma(self.partner, self.product_tracked_lot)
        rma.action_confirm()
        self.assertFalse(rma.lot_id)

    def test_does_nothing_if_untracked(self):
        rma = self._create_rma(self.partner, self.product_untracked)
        rma.action_confirm()
        self.assertFalse(rma.lot_id)

    def test_does_nothing_if_existing_lot(self):
        existing_lot = self.env["stock.lot"].create(
            {"name": "EXISTING", "product_id": self.product_tracked_lot.id}
        )
        rma = self._create_rma(self.partner, self.product_tracked_lot)
        rma.lot_id = existing_lot
        rma.action_confirm()
        self.assertEqual(rma.lot_id, existing_lot)

    def test_operation_require_sequence(self):
        operation_form = Form(self.env["rma.operation"])
        operation_form.name = "OP"
        operation_form.auto_create_lot = True
        with self.assertRaisesRegexp(
            AssertionError, "lot_sequence_id is a required field.*"
        ):
            operation_form.save()
        operation = self.env["rma.operation"].create(
            {"name": "op", "auto_create_lot": False}
        )
        with self.assertRaisesRegexp(
            ValidationError,
            "You must set a Lot/Serial Name Sequence.*",
        ):
            operation.auto_create_lot = True
        with self.assertRaisesRegexp(
            ValidationError,
            "You must set a Lot/Serial Name Sequence.*",
        ):
            self.env["rma.operation"].create({"name": "op 2", "auto_create_lot": True})

    def test_removal_relative_to_expiration(self):
        """removal_date = expiration_date - N days when both are configured."""
        today = fields.Date.context_today(self.env.user)
        op = self.env["rma.operation"].create(
            {
                "name": "Exp + removal",
                "auto_create_lot": True,
                "lot_sequence_id": self.op_lot_seq.id,
                "lot_expiration_days": 90,
                "lot_removal_days_before_expiration": 15,
            }
        )
        rma = self._create_rma(self.partner, self.product_tracked_lot, operation=op)
        rma.action_confirm()
        self.assertTrue(rma.lot_id)
        expected_expiration = today + relativedelta(days=90)
        expected_removal = expected_expiration - relativedelta(days=15)
        self.assertEqual(rma.lot_id.expiration_date.date(), expected_expiration)
        self.assertEqual(rma.lot_id.removal_date.date(), expected_removal)

    def test_removal_requires_expiration(self):
        """Configuring a before-expiration removal without positive expiration should fail."""
        with self.assertRaisesRegexp(
            ValidationError,
            "To set a removal date before expiration, you must configure a positive expiration",
        ):
            self.env["rma.operation"].create(
                {
                    "name": "Removal but no exp",
                    "auto_create_lot": True,
                    "lot_sequence_id": self.op_lot_seq.id,
                    "lot_removal_days_before_expiration": 10,
                    # lot_expiration_days missing/zero
                }
            )
        op = self.env["rma.operation"].create(
            {
                "name": "Zero exp invalid",
                "auto_create_lot": True,
                "lot_sequence_id": self.op_lot_seq.id,
                "lot_expiration_days": 0,
            }
        )
        with self.assertRaisesRegexp(
            ValidationError,
            "To set a removal date before expiration, you must configure a positive expiration",
        ):
            op.write({"lot_removal_days_before_expiration": 5})

    def test_negative_removal_not_allowed(self):
        with self.assertRaisesRegexp(
            ValidationError, "Expiration days must be greater than or equal to 0."
        ):
            self.env["rma.operation"].create(
                {
                    "name": "Invalid expiration",
                    "auto_create_lot": True,
                    "lot_sequence_id": self.op_lot_seq.id,
                    "lot_expiration_days": -30,
                }
            )
        with self.assertRaisesRegexp(
            ValidationError,
            "Removal days before expiration must be greater than or equal to 0.",
        ):
            self.env["rma.operation"].create(
                {
                    "name": "Invalid removal",
                    "auto_create_lot": True,
                    "lot_sequence_id": self.op_lot_seq.id,
                    "lot_expiration_days": 30,
                    "lot_removal_days_before_expiration": -1,
                }
            )

    def test_no_removal_when_not_configured(self):
        today = fields.Date.context_today(self.env.user)
        op = self.env["rma.operation"].create(
            {
                "name": "Only expiration",
                "auto_create_lot": True,
                "lot_sequence_id": self.op_lot_seq.id,
                "lot_expiration_days": 30,
            }
        )
        rma = self._create_rma(self.partner, self.product_tracked_lot, operation=op)
        rma.action_confirm()
        self.assertTrue(rma.lot_id)
        expected_expiration = today + relativedelta(days=30)
        self.assertEqual(rma.lot_id.expiration_date.date(), expected_expiration)
        self.assertEqual(rma.lot_id.removal_date.date(), expected_expiration)

    def test_product_no_use_expiration_date(self):
        self.product_tracked_lot.use_expiration_date = False
        op = self.env["rma.operation"].create(
            {
                "name": "Only expiration",
                "auto_create_lot": True,
                "lot_sequence_id": self.op_lot_seq.id,
                "lot_expiration_days": 30,
            }
        )
        rma = self._create_rma(self.partner, self.product_tracked_lot, operation=op)
        rma.action_confirm()
        self.assertTrue(rma.lot_id)
        self.assertFalse(rma.lot_id.expiration_date)
        self.assertFalse(rma.lot_id.removal_date)
