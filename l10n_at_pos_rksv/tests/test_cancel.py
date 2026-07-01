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


class TestAsignCancel(TransactionCase, TestAsignCommonMixin):
    """Cancelled orders holding a receipt number."""

    def setUp(self):
        super().setUp()
        self.open_session(
            {
                "name": "Cancel Test",
                "asign_enabled": True,
                "asign_pid": "K90",
                "asign_serial_hex": "abc123",
                "asign_key": base64.b64encode(b"0" * 32).decode(),
                "asign_cert": base64.b64encode(b"dummy").decode(),
                "asign_fid": "ATU12345675",
                "asign_user": "test",
                "asign_password": "test",
                "asign_method": "online",
            }
        )

    def _sync_order(self, seq, amount=0.0, state=None, with_payment=True):
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

        payment_ids = []
        if with_payment:
            payment_ids.append(
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
            "amount_paid": amount if with_payment else 0.0,
            "amount_total": amount,
            "amount_tax": 0.0,
            "sequence_number": seq,
            "payment_ids": payment_ids,
            "lines": lines,
        }
        if state:
            order_data["state"] = state

        with self._mock_sign():
            result = self.env["pos.order"].sync_from_ui([order_data])
        order_ids = [row["id"] for row in result["pos.order"]]
        order = self.env["pos.order"].browse(order_ids)
        self.assertEqual(len(order), 1, "There should be one order created")
        return order

    def _mock_sign(self):
        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = {"result": JWS_FAKE}
        return mock.patch("requests.post", return_value=response)

    def _create_signed_start_order(self):
        order = self._sync_order(1)
        self.assertEqual(order.state, "paid")
        self.assertEqual(order.asign_state, "s")
        self.assertEqual(order.asign_type, "s")
        self.assertNotEqual(order.name, "/")
        return order

    def _create_cancelled_order(self, seq, amount):
        order = self._sync_order(seq, amount=amount, state="draft", with_payment=False)
        self.assertEqual(order.state, "draft")
        self.assertEqual(order.name, "/")
        order.action_pos_order_cancel()
        self.assertEqual(order.state, "cancel")
        self.assertEqual(order.sequence_number, seq)
        return order

    def test_cancelled_order_signed_in_batch(self):
        """A cancelled order is signed as zeroed receipt by the batch loop."""
        self._create_signed_start_order()
        cancelled = self._create_cancelled_order(2, 39.9)

        order = self._sync_order(3, amount=5.0)
        self.assertEqual(order.state, "paid")
        self.assertEqual(order.asign_state, "s")
        self.assertEqual(order.asign_type, "o")
        self.assertEqual(order.asign_counter, "500")

        self.assertEqual(cancelled.state, "cancel")
        self.assertEqual(cancelled.asign_state, "s")
        self.assertEqual(cancelled.asign_type, "0")
        self.assertEqual(cancelled.asign_seq, 2)
        self.assertEqual(cancelled.asign_counter, "0")
        self.assertNotEqual(cancelled.name, "/")
        self.assertFalse(any(cancelled.lines.mapped("qty")))
        self.assertEqual(cancelled.amount_total, 0.0)

    def test_cancelled_order_signed_by_cron(self):
        """A cancelled order is signed as zeroed receipt by the cron."""
        self._create_signed_start_order()
        cancelled = self._create_cancelled_order(2, 39.9)

        with self._mock_sign():
            self.pos_config._cron_asign_sign_missed()

        self.assertEqual(cancelled.state, "cancel")
        self.assertEqual(cancelled.asign_state, "s")
        self.assertEqual(cancelled.asign_type, "0")
        self.assertNotEqual(cancelled.name, "/")
        self.assertFalse(any(cancelled.lines.mapped("qty")))
        self.assertEqual(cancelled.amount_total, 0.0)
        self.assertEqual(cancelled.amount_tax, 0.0)

    def test_close_session_triggers_cron(self):
        """Closing a session triggers the sign-missed cron."""
        self._create_signed_start_order()
        self._create_cancelled_order(2, 39.9)

        cron = self.env.ref("l10n_at_pos_rksv.pos_config_ir_cron")
        trigger_model = self.env["ir.cron.trigger"]
        before = trigger_model.search_count([("cron_id", "=", cron.id)])

        self.pos_session.set_opening_control(0, "")
        with self._mock_sign():
            self.pos_session.close_session_from_ui()

        self.assertEqual(self.pos_session.state, "closed")
        self.assertGreater(
            trigger_model.search_count([("cron_id", "=", cron.id)]),
            before,
            "Closing the session must trigger the sign-missed cron",
        )

    def test_cron_skips_open_session(self):
        """The cron skips POS with a session in opened state."""
        self._create_signed_start_order()
        cancelled = self._create_cancelled_order(2, 39.9)

        self.pos_session.set_opening_control(0, "")
        self.assertEqual(self.pos_session.state, "opened")

        with self._mock_sign():
            self.pos_config._cron_asign_sign_missed()
        self.assertEqual(cancelled.asign_state, "u", "POS in use must be skipped")

        with self._mock_sign():
            self.pos_session.close_session_from_ui()
            self.pos_config._cron_asign_sign_missed()

        self.assertEqual(cancelled.asign_state, "s")
        self.assertEqual(cancelled.asign_type, "0")
        self.assertNotEqual(cancelled.name, "/")

    def test_repair_signed_cancelled_name(self):
        """The cron restores the name of an overwritten signed order."""
        order = self._create_signed_start_order()
        name = order.name

        # simulate the lost-update race overwriting the signed order
        self.env.cr.execute(
            "UPDATE pos_order SET state = 'cancel', name = '/' WHERE id = %s",
            (order.id,),
        )
        self.env["pos.order"].invalidate_model()
        self.assertEqual(order.state, "cancel")
        self.assertEqual(order.name, "/")

        with self._mock_sign():
            self.pos_config._cron_asign_sign_missed()

        self.assertEqual(order.name, name, "Only the name is restored")
        self.assertEqual(order.state, "cancel")
        self.assertEqual(order.asign_state, "s")
