# Copyright 2026 Weboffice IT-Service und Marketing GmbH & Co KG <https://weboffice.at>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import base64
import uuid
from unittest import mock

from odoo import fields
from odoo.tests.common import TransactionCase

from .common import TestAsignCommonMixin

# Fake JWS result; only the base64url signature part is decoded by
# _asign_create_signature.
JWS_FAKE = "eyJhbGciOiJFUzI1NiJ9.cGF5bG9hZA.c2lnbmF0dXJl"


class TestAsignRefund(TransactionCase, TestAsignCommonMixin):
    """Backend refunds must not duplicate RKSV signature data."""

    def setUp(self):
        super().setUp()
        self.open_session(
            {
                "name": "Refund Test",
                "asign_enabled": True,
                "asign_pid": "K91",
                "asign_serial_hex": "abc123",
                "asign_key": base64.b64encode(b"0" * 32).decode(),
                "asign_cert": base64.b64encode(b"dummy").decode(),
                "asign_fid": "ATU12345675",
                "asign_user": "test",
                "asign_password": "test",
                "asign_method": "online",
            }
        )

    def _mock_sign(self):
        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = {"result": JWS_FAKE}
        return mock.patch("requests.post", return_value=response)

    def _sync_order(self, seq, amount=0.0):
        """Sync an order from a faked frontend with mocked online signing."""
        date_order = fields.Datetime.to_string(fields.Datetime.now())
        lines = []
        if amount:
            lines.append(
                (
                    0,
                    0,
                    {
                        "name": "Test Line",
                        "price_unit": amount,
                        "price_subtotal": amount,
                        "price_subtotal_incl": amount,
                        "discount": 0,
                        "product_id": self.product.id,
                        "full_product_name": "Test Line",
                        "qty": 1,
                        "refunded_orderline_id": False,
                        "tax_ids": [(6, 0, [])],
                    },
                )
            )

        order_data = {
            "uuid": str(uuid.uuid4()),
            "access_token": str(uuid.uuid4()),
            "session_id": self.pos_session.id,
            "name": "/",
            "date_order": date_order,
            "partner_id": None,
            "fiscal_position_id": None,
            "amount_return": 0.0,
            "to_invoice": False,
            "shipping_date": None,
            "asign_state": "u",
            "user_id": self.env.uid,
            "amount_paid": amount,
            "amount_total": amount,
            "amount_tax": 0.0,
            "sequence_number": seq,
            "payment_ids": [
                (
                    0,
                    0,
                    {
                        "name": False,
                        "payment_method_id": self.cash_payment_method.id,
                        "amount": amount,
                        "uuid": uuid.uuid4().hex,
                        "payment_date": date_order,
                    },
                )
            ],
            "lines": lines,
        }

        with self._mock_sign():
            result = self.env["pos.order"].sync_from_ui([order_data])
        order_ids = [row["id"] for row in result["pos.order"]]
        order = self.env["pos.order"].browse(order_ids)
        self.assertEqual(len(order), 1, "There should be one order created")
        return order

    def test_backend_refund_signed_with_own_seq(self):
        """A backend refund draws its own receipt number and gets signed."""
        start = self._sync_order(1)
        self.assertEqual(start.asign_seq, 1)
        order = self._sync_order(2, amount=10.0)
        self.assertEqual(order.asign_state, "s")
        self.assertEqual(order.asign_seq, 2)

        action = order.refund()
        refund = self.env["pos.order"].browse(action["res_id"])

        # No signature data may be copied from the original order.
        self.assertEqual(refund.name, "/")
        self.assertEqual(refund.asign_state, "u")
        self.assertEqual(refund.asign_seq, 0)
        self.assertFalse(refund.asign_qrcode)
        self.assertFalse(refund.asign_dep)
        self.assertFalse(refund.asign_counter)
        self.assertFalse(refund.asign_type)

        wizard = (
            self.env["pos.make.payment"]
            .with_context(active_ids=refund.ids, active_id=refund.id)
            .create({"payment_method_id": self.cash_payment_method.id})
        )
        with self._mock_sign():
            wizard.check()

        self.assertEqual(refund.state, "paid")
        self.assertEqual(refund.asign_state, "s")
        self.assertEqual(refund.asign_type, "c")
        # The refund consumed the next gapless receipt number.
        self.assertEqual(refund.asign_seq, 3)
        self.assertNotEqual(refund.asign_seq, order.asign_seq)
        # The QR payload must be the refund's own signature, not a copy
        # (asign_dep is the raw JWS response and identical under the mock).
        self.assertNotEqual(refund.asign_qrcode, order.asign_qrcode)
        self.assertTrue(refund.asign_dep)
        # The name is the receipt number without any REFUND suffix.
        self.assertEqual(
            refund.name, self.pos_config.order_seq_id.get_next_char(refund.asign_seq)
        )
        self.assertNotIn("REFUND", refund.name)
        # The negative refund amount reverses the turnover counter.
        self.assertEqual(refund.asign_counter, "0")

        # The original order stays untouched.
        self.assertEqual(order.asign_seq, 2)
        self.assertEqual(order.asign_state, "s")
