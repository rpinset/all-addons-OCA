# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
from unittest.mock import patch

from odoo import Command
from odoo.exceptions import AccessError, UserError
from odoo.tests.common import TransactionCase, new_test_user

# A 1x1 transparent PNG.
PNG = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA"
    "60e6kgAAAABJRU5ErkJggg=="
)


class TestBarcodeStockQuality(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Inspection = cls.env["qc.inspection"]
        unit = cls.env.ref("uom.product_uom_unit")
        cls.test = cls.env["qc.test"].create(
            {
                "name": "Reception check",
                "test_lines": [
                    Command.create(
                        {
                            "name": "Packaging intact",
                            "type": "qualitative",
                            "ql_values": [
                                Command.create({"name": "Yes", "ok": True}),
                                Command.create({"name": "No", "ok": False}),
                            ],
                        }
                    ),
                    Command.create(
                        {
                            "name": "Temperature",
                            "type": "quantitative",
                            "min_value": 0,
                            "max_value": 5,
                            "uom_id": unit.id,
                        }
                    ),
                ],
            }
        )
        cls.yes, cls.no = cls.test.test_lines[0].ql_values
        cls.other_value = cls.env["qc.test.question.value"].create(
            {"name": "Elsewhere", "ok": True}
        )
        product = cls.env["product.product"].create(
            {"name": "Chilled goods", "is_storable": True}
        )
        receipts = cls.env.ref("stock.picking_type_in")
        cls.picking = cls.env["stock.picking"].create(
            {
                "picking_type_id": receipts.id,
                "location_id": receipts.default_location_src_id.id,
                "location_dest_id": receipts.default_location_dest_id.id,
                "move_ids": [
                    Command.create(
                        {
                            "name": product.name,
                            "product_id": product.id,
                            "product_uom_qty": 1,
                            "location_id": receipts.default_location_src_id.id,
                            "location_dest_id": receipts.default_location_dest_id.id,
                        }
                    )
                ],
            }
        )
        cls.inspection = cls._inspection(cls.picking, cls.test)
        cls.user = new_test_user(
            cls.env,
            login="barcode_quality_user",
            groups="stock.group_stock_user,"
            "quality_control_oca.group_quality_control_user",
        )

    @classmethod
    def _inspection(cls, picking, test):
        inspection = cls.env["qc.inspection"].create(
            {
                "name": "Barcode reception check",
                "object_id": f"stock.picking,{picking.id}",
                "test": test.id,
                "inspection_lines": cls.env["qc.inspection"]._prepare_inspection_lines(
                    test
                ),
            }
        )
        inspection.action_todo()
        return inspection

    def _answers(self, value, measure):
        qualitative, quantitative = self.inspection.inspection_lines
        return [
            {"line_id": qualitative.id, "qualitative_value_id": value.id},
            {"line_id": quantitative.id, "quantitative_value": measure},
        ]

    # --- reading --------------------------------------------------------------

    def test_inspections_of_a_reception(self):
        canceled = self._inspection(self.picking, self.test)
        canceled.action_cancel()
        result = self.env["stock.picking"].action_barcode_scanner_quality_inspections(
            self.picking.id
        )
        self.assertEqual(result["picking_id"], self.picking.id)
        # The canceled inspection is left out.
        self.assertEqual(
            [i["inspection_id"] for i in result["inspections"]], [self.inspection.id]
        )
        data = result["inspections"][0]
        self.assertEqual(data["state"], "ready")
        self.assertFalse(data["can_reset"])
        self.assertEqual(data["test_name"], "Reception check")
        self.assertEqual(data["photo_count"], 0)
        qualitative, quantitative = data["lines"]
        self.assertEqual(qualitative["question_type"], "qualitative")
        self.assertFalse(qualitative["qualitative_value_id"])
        self.assertEqual(
            [value["name"] for value in qualitative["possible_values"]], ["Yes", "No"]
        )
        self.assertEqual(quantitative["question_type"], "quantitative")
        self.assertEqual(quantitative["uom_name"], "Units")
        self.assertEqual(quantitative["max_value"], 5)

    def test_reception_gone(self):
        with self.assertRaises(UserError):
            self.env["stock.picking"].action_barcode_scanner_quality_inspections(0)

    def test_only_quality_users_read_inspections(self):
        clerk = new_test_user(
            self.env, login="barcode_quality_clerk", groups="stock.group_stock_user"
        )
        with self.assertRaises(AccessError):
            self.env["stock.picking"].with_user(
                clerk
            ).action_barcode_scanner_quality_inspections(self.picking.id)

    # --- answering ------------------------------------------------------------

    def test_answers_that_pass(self):
        result = self.Inspection.with_user(self.user).action_barcode_scanner_submit(
            self.inspection.id, self._answers(self.yes, 3.5)
        )
        self.assertEqual(result["state"], "success")
        self.assertTrue(result["success"])
        quantitative = self.inspection.inspection_lines[1]
        self.assertEqual(quantitative.quantitative_value, 3.5)
        self.assertEqual(quantitative.uom_id, quantitative.test_uom_id)

    def test_answers_that_fail_wait_for_a_supervisor(self):
        result = self.Inspection.action_barcode_scanner_submit(
            self.inspection.id, self._answers(self.no, 3)
        )
        self.assertEqual(result["state"], "waiting")
        self.assertFalse(result["success"])

    def test_answers_that_cannot_be_taken(self):
        qualitative, quantitative = self.inspection.inspection_lines
        cases = [
            # A question left without an answer.
            [{"line_id": qualitative.id, "qualitative_value_id": self.yes.id}],
            # A measure that is not a number.
            self._answers(self.yes, "warm"),
            self._answers(self.yes, "inf"),
            # A choice the question does not offer.
            self._answers(self.other_value, 3),
            [{"line_id": quantitative.id, "quantitative_value": 3}],
        ]
        for answers in cases:
            with self.subTest(answers=answers), self.assertRaises(UserError):
                self.Inspection.action_barcode_scanner_submit(
                    self.inspection.id, answers
                )
        self.assertEqual(self.inspection.state, "ready")

    def test_only_a_ready_inspection_is_answered(self):
        with self.assertRaises(UserError):
            self.Inspection.action_barcode_scanner_submit(0, [])
        self.Inspection.action_barcode_scanner_submit(
            self.inspection.id, self._answers(self.yes, 1)
        )
        with self.assertRaises(UserError):
            self.Inspection.action_barcode_scanner_submit(
                self.inspection.id, self._answers(self.no, 9)
            )

    def test_reset_a_confirmed_inspection(self):
        with self.assertRaises(UserError):
            self.Inspection.action_barcode_scanner_reset(self.inspection.id)
        result = self.Inspection.action_barcode_scanner_submit(
            self.inspection.id, self._answers(self.yes, 1)
        )
        self.assertTrue(result["can_reset"])
        self.assertTrue(self.inspection.barcode_scanner_confirmed)
        result = self.Inspection.action_barcode_scanner_reset(self.inspection.id)
        self.assertEqual(result["state"], "ready")
        self.assertFalse(result["can_reset"])
        self.assertFalse(self.inspection.barcode_scanner_confirmed)
        # The answers are kept, for the operator to correct them.
        qualitative, quantitative = result["lines"]
        self.assertEqual(qualitative["qualitative_value_id"], self.yes.id)
        self.assertEqual(quantitative["quantitative_value"], 1)
        # Failed and waiting for a supervisor: still the operator's to redo.
        self.Inspection.action_barcode_scanner_submit(
            self.inspection.id, self._answers(self.no, 1)
        )
        self.assertEqual(self.inspection.state, "waiting")
        self.Inspection.action_barcode_scanner_reset(self.inspection.id)
        self.assertEqual(self.inspection.state, "ready")

    def test_a_supervisor_rejection_is_not_reopened(self):
        self.Inspection.action_barcode_scanner_submit(
            self.inspection.id, self._answers(self.no, 1)
        )
        self.inspection.action_approve()
        self.assertEqual(self.inspection.state, "failed")
        with self.assertRaises(UserError):
            self.Inspection.action_barcode_scanner_reset(self.inspection.id)
        self.assertEqual(self.inspection.state, "failed")

    def test_back_office_confirmations_are_not_reopened(self):
        qualitative, quantitative = self.inspection.inspection_lines
        qualitative.qualitative_value = self.yes
        quantitative.quantitative_value = 1
        self.inspection.action_confirm()
        self.assertEqual(self.inspection.state, "success")
        data = self.inspection._barcode_scanner_read()
        self.assertFalse(data["can_reset"])
        with self.assertRaises(UserError):
            self.Inspection.action_barcode_scanner_reset(self.inspection.id)

    def test_closed_receptions_are_not_reopened(self):
        self.Inspection.action_barcode_scanner_submit(
            self.inspection.id, self._answers(self.yes, 1)
        )
        self.picking.action_cancel()
        self.assertFalse(self.inspection._barcode_scanner_read()["can_reset"])
        with self.assertRaises(UserError):
            self.Inspection.action_barcode_scanner_reset(self.inspection.id)

    # --- photos ---------------------------------------------------------------

    def test_attach_a_photo(self):
        result = self.Inspection.with_user(
            self.user
        ).action_barcode_scanner_attach_photo(self.inspection.id, "box.png", PNG)
        self.assertEqual(
            result, {"inspection_id": self.inspection.id, "photo_count": 1}
        )
        attachment = self.env["ir.attachment"].search(
            [("res_model", "=", "qc.inspection"), ("res_id", "=", self.inspection.id)]
        )
        self.assertEqual(attachment.name, "box.png")
        # Only photos are counted.
        self.env["ir.attachment"].create(
            {
                "name": "notes.txt",
                "raw": b"not a photo",
                "res_model": "qc.inspection",
                "res_id": self.inspection.id,
            }
        )
        data = self.Inspection.browse(self.inspection.id)._barcode_scanner_read()
        self.assertEqual(data["photo_count"], 1)
        # Without a name, it is named as evidence.
        self.Inspection.action_barcode_scanner_attach_photo(self.inspection.id, "", PNG)
        self.assertTrue(
            self.env["ir.attachment"].search_count(
                [("res_id", "=", self.inspection.id), ("name", "=", "Quality evidence")]
            )
        )

    def test_photos_that_cannot_be_attached(self):
        attach = self.Inspection.action_barcode_scanner_attach_photo
        cases = [
            (0, PNG),
            (self.inspection.id, "not base64!"),
            (self.inspection.id, base64.b64encode(b"plain text").decode()),
        ]
        for inspection_id, datas in cases:
            with self.subTest(datas=datas[:12]), self.assertRaises(UserError):
                attach(inspection_id, "photo.png", datas)
        # An image Odoo cannot process.
        Attachment = type(self.env["ir.attachment"])
        with (
            patch.object(Attachment, "create", side_effect=OSError("truncated")),
            self.assertRaises(UserError),
        ):
            attach(self.inspection.id, "photo.png", PNG)
