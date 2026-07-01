# Copyright 2024 Weboffice IT-Service und Marketing GmbH & Co KG <https://weboffice.at>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import json
import logging
import os
import uuid
from datetime import datetime
from unittest import mock

import pytz

from odoo import fields
from odoo.tools import config

_logger = logging.getLogger(__name__)


class TestDownloadMixin:
    """Local helpers to dump test artefacts to a configurable folder.

    Replaces the previous dependency on the proprietary ``oerp_util``
    helpers so the module can be released through OCA without external
    runtime requirements.
    """

    def get_download_path(self, path):
        download_path = config.get("test_download")
        if not download_path:
            _logger.warning(
                "No download path configured. Set 'test_download' in odoo.conf."
            )
            return None

        parent_path = os.path.dirname(path)
        if parent_path:
            parent_path = os.path.join(download_path, parent_path)
            os.makedirs(parent_path, exist_ok=True)
            path = os.path.basename(path)
        else:
            parent_path = download_path
        return os.path.join(parent_path, path)

    def save_test_data(self, name, data):
        path = self.get_download_path(name)
        if not path:
            return
        if isinstance(data, dict | list):
            if not path.endswith(".json"):
                path = f"{path}.json"
            with open(path, "w", encoding="utf-8") as fp:
                json.dump(data, fp, indent=2)
        elif isinstance(data, str):
            with open(path, "w", encoding="utf-8") as fp:
                fp.write(data)
        else:
            with open(path, "wb") as fp:
                fp.write(data)


class TestAsignCommonMixin:
    """Common helpers for tests dealing with the a.sign integration."""

    def _to_utc(self, value):
        date_dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        date_dt = self.austrian_tz.localize(date_dt)
        return fields.Datetime.to_string(date_dt.astimezone(pytz.utc))

    def create_config(self, test_config):
        self.last_order = None
        self.austrian_tz = pytz.timezone("Europe/Berlin")

        self.product = self.env["product.product"].create(
            {"name": "Test Product", "lst_price": 0.0}
        )

        self.cash_journal = (
            self.env["account.journal"].search([("type", "=", "cash")], limit=1).copy()
        )
        self.cash_payment_method = self.env["pos.payment.method"].create(
            {
                "name": "Cash Test",
                "journal_id": self.cash_journal.id,
            }
        )

        asign_cert = test_config.pop("asign_cert", None)
        asign_user = test_config.pop("asign_user", None)
        asign_password = test_config.pop("asign_password", None)
        if asign_cert:
            cert_model = self.env["asign.cert"]
            self.asign_cert = cert_model.search(
                [("serial_hex", "=", test_config["asign_serial_hex"])], limit=1
            )
            if not self.asign_cert:
                self.asign_cert = cert_model.create(
                    {
                        "name": test_config["asign_serial_hex"],
                        "cert": asign_cert,
                        "user": asign_user,
                        "password": asign_password,
                    }
                )

        config_data = {
            "module_pos_restaurant": False,
            "payment_method_ids": [(6, 0, [self.cash_payment_method.id])],
        }
        config_data.update(test_config)
        self.pos_config = self.env["pos.config"].create(config_data)
        self.pos_config.action_asign_assign()
        self.assertTrue(self.pos_config.asign_enabled)

    def open_session(self, test_config):
        self.create_config(test_config)

        self.tax_20 = self.env["account.tax"].search([("amount", "=", 20.0)], limit=1)
        self.tax_10 = self.env["account.tax"].search([("amount", "=", 10.0)], limit=1)

        self.pos_session = self.env["pos.session"].create(
            {"user_id": self.env.uid, "config_id": self.pos_config.id}
        )
        self.pos_seq = 1

    def _create_order(self, order_values):
        date_order = self._to_utc(order_values["date_order"])
        lines = []
        order_data = {
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
            "asign_type": order_values["asign_type"],
            "user_id": self.env.uid,
            "amount_paid": order_values.get("amount_total", 0.0),
            "amount_total": order_values.get("amount_total", 0.0),
            "amount_tax": order_values.get("amount_tax", 0.0),
            "sequence_number": self.pos_seq,
            "payment_ids": [
                (
                    0,
                    0,
                    {
                        "name": False,
                        "payment_method_id": self.cash_payment_method.id,
                        "amount": order_values.get("amount_total", 0.0),
                        "uuid": uuid.uuid4().hex,
                        "payment_date": date_order,
                        "card_type": False,
                        "card_brand": False,
                        "card_no": False,
                        "cardholder_name": False,
                        "payment_ref_no": False,
                        "payment_method_authcode": False,
                        "payment_method_issuer_bank": False,
                        "payment_method_payment_mode": False,
                        "transaction_id": False,
                        "payment_status": False,
                        "ticket": "",
                        "is_change": False,
                        "account_move_id": False,
                    },
                )
            ],
            "lines": lines,
        }

        for line in order_values.get("lines", []):
            line_amount = line.get("amount", 0.0)
            tax = line.get("tax", 0.0)
            tax_amount = round(line_amount * tax, 2)
            tax_ids = []
            if tax == 0.10:
                tax_ids.append(self.tax_10.id)
            elif tax == 0.20:
                tax_ids.append(self.tax_20.id)

            lines.append(
                (
                    0,
                    0,
                    {
                        "id": str(uuid.uuid4()),
                        "name": line["name"],
                        "price_unit": line_amount,
                        "price_subtotal": line_amount - tax_amount,
                        "price_subtotal_incl": line_amount,
                        "discount": 0,
                        "product_id": self.product.id,
                        "full_product_name": line.get("name", "Test"),
                        "qty": 1,
                        "refunded_orderline_id": False,
                        "tax_ids": [(6, 0, tax_ids)],
                    },
                )
            )

        result = self.env["pos.order"].sync_from_ui([order_data])
        order_ids = [order["id"] for order in result["pos.order"]]
        order = self.env["pos.order"].browse(order_ids)
        self.pos_seq += 1

        self.assertEqual(len(order), 1, "There should be one order created")
        self.assertEqual(order.asign_state, "s", "The order should be signed")
        self.assertEqual(
            order.asign_serial,
            self.asign_cert.serial_hex,
            "The serial should be set",
        )

        last_counter = int(self.last_order.asign_counter) if self.last_order else 0
        self.assertEqual(
            order.asign_counter,
            str(last_counter + int(order.amount_total * 100)),
            "Check the turnover",
        )

        self.last_order = order
        return order

    def create_order(self, order_values):
        with mock.patch("requests.post") as post:
            response = mock.Mock()
            response.status_code = 200
            response.json.return_value = {"result": order_values["asign_dep"]}
            post.return_value = response
            order = self._create_order(order_values)
            self.assertEqual(
                order.asign_qrcode,
                order_values["asign_qrcode"],
                "The QR code should be correct",
            )
