# Copyright 2024 Weboffice IT-Service und Marketing GmbH & Co KG <https://weboffice.at>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import logging
import shutil

from odoo.tests.common import TransactionCase, tagged
from odoo.tools import config

from .common import TestAsignCommonMixin, TestDownloadMixin
from .regcheck.regcheck import RegChecker

_logger = logging.getLogger(__name__)


# Online integration test against the live a-trust signing service.
# It is intentionally hidden behind the ``test_asign`` config flag so it is
# never collected during the standard CI run.
if config.get("test_asign"):

    @tagged("integration", "-standard", "-at_install", "post_install")
    class TestAsignOnline(TransactionCase, TestAsignCommonMixin, TestDownloadMixin):
        """End-to-end test of the RKSV online signing flow."""

        def setUp(self):
            super().setUp()
            self.test_config = {
                "name": "Test",
                "asign_enabled": True,
                "asign_pid": config["test_asign_pid"],
                "asign_serial_hex": config["test_asign_serial_hex"],
                "asign_key": config["test_asign_key"],
                "asign_cert": config["test_asign_cert"],
                "asign_fid": config["test_asign_fid"],
                "asign_user": config["test_asign_user"],
                "asign_password": config["test_asign_password"],
                "asign_method": "online",
            }

        def test_asign_receipts_online(self):
            test_data = [
                {
                    "date_order": "2024-08-06 15:28:52",
                    "asign_seq": 1,
                    "asign_type": "s",
                },
                {
                    "date_order": "2024-08-06 15:40:40",
                    "asign_seq": 2,
                    "asign_type": "o",
                    "amount_total": 2.60,
                    "amount_tax": 0.43,
                    "lines": [
                        {
                            "name": "Apfelsaft",
                            "tax": 0.20,
                            "amount": 2.60,
                        },
                    ],
                },
                {
                    "date_order": "2024-08-06 15:43:44",
                    "asign_seq": 3,
                    "asign_type": "o",
                    "amount_total": 3.0,
                    "amount_tax": 0.27,
                    "lines": [
                        {
                            "name": "Leberaustrich",
                            "tax": 0.10,
                            "amount": 3.0,
                        },
                    ],
                },
                {
                    "date_order": "2024-08-06 15:46:07",
                    "asign_seq": 4,
                    "asign_type": "c",
                    "amount_total": -3.0,
                    "amount_tax": -0.27,
                    "lines": [
                        {
                            "name": "Leberaustrich",
                            "tax": 0.10,
                            "amount": -3.0,
                        },
                    ],
                },
                {
                    "date_order": "2024-08-06 16:00:10",
                    "asign_seq": 5,
                    "asign_type": "0",
                },
                {
                    "date_order": "2024-08-06 16:15:39",
                    "asign_seq": 6,
                    "asign_type": "o",
                    "amount_total": 2.20,
                    "amount_tax": 0.37,
                    "lines": [
                        {
                            "name": "Birnensaft",
                            "tax": 0.20,
                            "amount": 2.60,
                        },
                        {
                            "name": "Minus Pfand",
                            "tax": 0.20,
                            "amount": -0.40,
                        },
                    ],
                },
                {
                    "date_order": "2024-08-06 17:00:48",
                    "asign_seq": 7,
                    "asign_type": "o",
                    "amount_total": -4.80,
                    "lines": [
                        {
                            "name": "Auszahlung",
                            "amount": -4.80,
                        },
                    ],
                },
            ]

            self.open_session(self.test_config)

            orders = self.env["pos.order"]
            for order in test_data:
                orders += self._create_order(order)

            regcheck_dir = self.get_download_path("asign_test")
            shutil.rmtree(regcheck_dir, ignore_errors=True)

            dep_export = self.pos_config._asign_dep_export()
            self.save_test_data("asign_test/dep.json", dep_export)

            regcheck = RegChecker(
                regcheck_dir,
                crypto_config={
                    "base64AESKey": self.pos_config.asign_key,
                    "certificateOrPublicKeyMap": {
                        self.pos_config.asign_serial_hex: {
                            "id": self.asign_cert.serial_hex,
                            "signatureDeviceType": "CERTIFICATE",
                            "signatureCertificateOrPublicKey": (
                                self.asign_cert.cert.decode()
                            ),
                        },
                    },
                },
            )

            self.assertTrue(regcheck.check(), "DEP must be valid")

            for order in orders:
                _logger.info(
                    "Processed Order %s\nDEP: %s\nQR Code: %s",
                    order.name,
                    order.asign_dep,
                    order.asign_qrcode,
                )

        def test_create_zero_receipt(self):
            self.create_config(self.test_config)
            zero_order = self.pos_config._asign_create_zero_receipt()
            self.assertTrue(zero_order, "Zero receipt should be created")
            self.assertEqual(len(zero_order), 1, "Only one order is expected")

            self.assertEqual(zero_order.asign_state, "s")
            self.assertEqual(zero_order.asign_type, "s")
            self.assertEqual(zero_order.state, "paid")

            first_session = self.env["pos.session"].search(
                [("config_id", "=", self.pos_config.id)],
                order="id desc",
                limit=1,
            )
            self.assertTrue(first_session)
            first_session.cash_register_balance_end_real = 100.0
            self.env.flush_all()

            zero_order = self.pos_config._asign_create_zero_receipt()
            self.assertEqual(zero_order.asign_state, "s")
            self.assertEqual(zero_order.asign_type, "0")
            self.assertEqual(zero_order.state, "paid")
            self.assertEqual(zero_order.asign_seq, 2)
            self.env.flush_all()

            last_session = self.env["pos.session"].search(
                [("config_id", "=", self.pos_config.id)],
                order="id desc",
                limit=1,
            )
            self.assertNotEqual(last_session, first_session)
            self.assertEqual(last_session.cash_register_balance_end_real, 100.0)
