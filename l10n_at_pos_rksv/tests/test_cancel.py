# Copyright 2026 Weboffice IT-Service und Marketing GmbH & Co KG <https://weboffice.at>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import base64
import uuid
from unittest import mock

import requests

from odoo import fields
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger

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

    def _sync_order(self, seq, amount=0.0, state=None, with_payment=True, sign_cm=None):
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

        with sign_cm or self._mock_sign():
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

    def test_cancelled_order_not_signed(self):
        """A cancelled order keeps no receipt number; the range stays gapless."""
        start = self._create_signed_start_order()
        self.assertEqual(start.asign_seq, 1)
        cancelled = self._create_cancelled_order(2, 39.9)

        order = self._sync_order(3, amount=5.0)
        self.assertEqual(order.state, "paid")
        self.assertEqual(order.asign_state, "s")
        self.assertEqual(order.asign_type, "o")
        self.assertEqual(order.asign_counter, "500")
        # the cancelled order in between consumed no receipt number
        self.assertEqual(order.asign_seq, 2)

        self.assertEqual(cancelled.state, "cancel")
        self.assertNotEqual(cancelled.asign_state, "s")
        self.assertEqual(cancelled.asign_seq, 0)
        self.assertEqual(cancelled.name, "/")

    def test_cancelled_order_not_signed_by_cron(self):
        """The cron does not sign cancelled orders."""
        self._create_signed_start_order()
        cancelled = self._create_cancelled_order(2, 39.9)

        with self._mock_sign():
            self.pos_config._cron_asign_sign_missed()

        self.assertEqual(cancelled.state, "cancel")
        self.assertNotEqual(cancelled.asign_state, "s")
        self.assertEqual(cancelled.asign_seq, 0)
        self.assertEqual(cancelled.name, "/")

    # The provoked ConnectionError is logged via _logger.exception; mute it so
    # the expected traceback does not leave an ERROR line in the log (which
    # would otherwise break OCA's checklog-odoo CI step).
    @mute_logger("odoo.addons.l10n_at_pos_rksv.models.pos_order")
    def test_missed_paid_order_signed_by_cron(self):
        """A paid order whose signing failed is signed gaplessly by the cron."""
        start = self._create_signed_start_order()
        self.assertEqual(start.asign_seq, 1)
        self._create_cancelled_order(2, 39.9)

        # signing fails on creation, so the order stays paid but unsigned
        fail = mock.patch(
            "requests.post", side_effect=requests.exceptions.ConnectionError()
        )
        order = self._sync_order(3, amount=5.0, sign_cm=fail)
        self.assertEqual(order.state, "paid")
        self.assertEqual(order.asign_state, "u")
        self.assertEqual(order.asign_seq, 0)
        self.assertEqual(order.name, "/")

        with self._mock_sign():
            self.pos_config._cron_asign_sign_missed()

        self.assertEqual(order.asign_state, "s")
        self.assertEqual(order.asign_type, "o")
        self.assertEqual(order.asign_seq, 2)
        self.assertNotEqual(order.name, "/")

    def test_close_session_triggers_cron(self):
        """Closing a session triggers the sign-missed cron."""
        self._create_signed_start_order()
        self._create_cancelled_order(2, 39.9)

        cron = self.env.ref("l10n_at_pos_rksv.pos_config_ir_cron")
        # Neutralized test databases deactivate all crons; an inactive cron
        # silently drops immediate triggers, so activate it for this test.
        cron.active = True
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

    # See test_missed_paid_order_signed_by_cron for why the logger is muted.
    @mute_logger("odoo.addons.l10n_at_pos_rksv.models.pos_order")
    def test_cron_signs_open_session(self):
        """The cron signs missed paid orders even with an opened session."""
        self._create_signed_start_order()
        self._create_cancelled_order(2, 39.9)

        fail = mock.patch(
            "requests.post", side_effect=requests.exceptions.ConnectionError()
        )
        order = self._sync_order(3, amount=5.0, sign_cm=fail)
        self.assertEqual(order.asign_state, "u")

        self.pos_session.set_opening_control(0, "")
        self.assertEqual(self.pos_session.state, "opened")

        with self._mock_sign():
            self.pos_config._cron_asign_sign_missed()

        self.assertEqual(order.asign_state, "s")
        self.assertEqual(order.asign_seq, 2)
        self.assertNotEqual(order.name, "/")

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
