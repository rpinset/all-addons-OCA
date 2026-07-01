# Copyright 2024 Weboffice IT-Service und Marketing GmbH & Co KG <https://weboffice.at>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import base64
import hashlib
import logging
import struct
import urllib.parse

import pytz
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

try:
    TIMEZONE_AT = pytz.timezone("Europe/Vienna")
except pytz.UnknownTimeZoneError:
    _logger.error("Timezone Europe/Vienna not found.")
    TIMEZONE_AT = None

B64_STO = base64.b64encode(b"STO").decode()
B64_TRA = base64.b64encode(b"TRA").decode()

ASIGN_SUITE_ID = "R1-AT1"
ASIGN_ENDPOINT = "https://www.a-trust.at/asignrkonline/v2"
ASIGN_TIMEOUT = 30


def asign_b64urldecode_nopadding(value):
    """Decode a base64 URL-safe string that has no padding."""
    missing = len(value) % 4
    if missing:
        value += "=" * (4 - missing)
    return base64.urlsafe_b64decode(value)


def asign_float(value):
    """Format a monetary amount in the Austrian RKSV decimal notation."""
    return f"{value:0.2f}".replace(".", ",")


def asign_datetime(value):
    """Format a datetime as required by the RKSV signature payload."""
    utc_dt = pytz.utc.localize(value, is_dst=False)
    local_dt = utc_dt.astimezone(TIMEZONE_AT) if TIMEZONE_AT else utc_dt
    return local_dt.strftime("%Y-%m-%dT%H:%M:%S")


class PosOrder(models.Model):
    _inherit = "pos.order"

    asign_type = fields.Selection(
        [
            ("o", "Order"),
            ("s", "Start"),
            ("0", "Null"),
            ("c", "Cancel"),
            ("m", "Mixed"),
            ("t", "Training"),
        ],
        string="a.sign Type",
        index=True,
        readonly=True,
    )
    asign_state = fields.Selection(
        [
            ("u", "Unsigned"),
            ("s", "Signed"),
        ],
        string="a.sign State",
        help=(
            "State of the RKSV signature: unsigned means the signature is "
            "missing, signed means the signature is present. If empty, no "
            "signing is needed."
        ),
        index=True,
        readonly=True,
    )
    asign_counter = fields.Char(
        string="a.sign Counter",
        help="The turnover counter of the RKSV signature.",
        readonly=True,
    )
    asign_qrcode = fields.Char(
        string="a.sign QR-Code",
        help="The QR code of the RKSV signature.",
        index=True,
        readonly=True,
    )
    asign_dep = fields.Text(
        string="a.sign DEP",
        help="The DEP entry of the RKSV signature export.",
        readonly=True,
    )
    asign_serial = fields.Char(
        string="a.sign Serial",
        help="The serial number of the RKSV signing component.",
        readonly=True,
    )
    asign_seq = fields.Integer(
        string="a.sign Sequence",
        help="The sequence number of the RKSV signature export.",
        readonly=True,
        index=True,
    )
    asign_qrcode_quoted = fields.Char(
        string="a.sign QR-Code Quoted",
        compute="_compute_qrcode",
    )

    sign_qrcode = fields.Char(compute="_compute_qrcode")
    sign_qrcode_name = fields.Char(compute="_compute_qrcode")

    @api.depends("asign_qrcode", "asign_serial")
    def _compute_qrcode(self):
        for order in self:
            qrcode = (
                urllib.parse.quote(order.asign_qrcode) if order.asign_qrcode else ""
            )
            order.asign_qrcode_quoted = qrcode
            order.sign_qrcode = qrcode
            order.sign_qrcode_name = order.asign_serial or ""

    def _load_pos_data_fields(self, config):
        res = super()._load_pos_data_fields(config)
        if not res:
            return res
        res += [
            "asign_type",
            "asign_state",
            "asign_qrcode",
            "asign_serial",
            "asign_ref",
        ]
        return res

    def _compute_order_name(self, session=None):
        if self.asign_state or self.config_id.asign_enabled:
            session = session or self.session_id
            config = session.config_id
            return config.order_seq_id.get_next_char(self.sequence_number or 0)
        return super()._compute_order_name()

    def _compute_asign_seq(self):
        for order in self:
            order.asign_seq = order.sequence_number

    def _asign_tax_amounts(self):
        """Return the tax amounts of the order grouped by RKSV tax category."""
        amount_total = self.currency_id.round(self.amount_total)
        res = {
            "normal": 0.0,
            "reduced1": 0.0,
            "reduced2": 0.0,
            "special": 0.0,
            "null": 0.0,
            "amount": amount_total,
            # round to int to avoid float comparison issues with the turnover
            "turnover": round(amount_total * 100),
        }

        for line in self.lines:
            asign_type = "normal"
            if not line.tax_ids:
                asign_type = "null"
            else:
                tax_group = line.tax_ids.tax_group_id[:1]
                if tax_group.asign_type:
                    asign_type = tax_group.asign_type

            res[asign_type] += self.currency_id.round(line.price_subtotal_incl)

        # never trust float; recompute the bucket sum and add any rounding
        # difference to the first bucket that contributed to it.
        correction_type = None
        calc_total = 0.0
        for amount_type in ("normal", "reduced1", "reduced2", "special", "null"):
            bucket_total = res[amount_type]
            if amount_total and not correction_type:
                correction_type = amount_type
            calc_total += bucket_total
        calc_total = self.currency_id.round(calc_total)
        diff = amount_total - calc_total
        if diff and correction_type:
            res[correction_type] += diff
        return res

    def _asign_prepare_signature(self, last_order):
        """Build the RKSV signature payload for the chained signing step."""
        config = self.session_id.config_id
        amounts = self._asign_tax_amounts()

        asign_counter = amounts["turnover"]
        if last_order:
            asign_counter += int(last_order.asign_counter)

        asign_type = "o"
        if self.asign_type == "c" or self.refunded_order_id:
            asign_type = "c"
            encoded_turnover = B64_STO
        elif self.asign_type == "t":
            asign_type = "t"
            encoded_turnover = B64_TRA
        else:
            if not amounts["amount"]:
                asign_type = "0"
                if not last_order:
                    asign_type = "s"

            receipt_id = f"{config.asign_pid}{self.asign_seq}"
            turnover_ctr = hashlib.sha256(receipt_id.encode()).digest()[:16]
            turnover_bin = struct.pack(">qq", asign_counter, 0)
            cipher = Cipher(
                algorithms.AES(base64.b64decode(config.asign_key)),
                modes.CTR(turnover_ctr),
            )
            encryptor = cipher.encryptor()
            encrypted_turnover = encryptor.update(turnover_bin) + encryptor.finalize()
            encoded_turnover = base64.b64encode(encrypted_turnover[:8]).decode()

        # If there is a previous order use its DEP for the chain hash, else
        # use the POS-ID as defined by the RKSV specification.
        last_hash = last_order.asign_dep if last_order else config.asign_pid
        last_hash = hashlib.sha256(last_hash.encode()).digest()[:8]
        last_hash = base64.b64encode(last_hash).decode()

        asign_data = [
            ASIGN_SUITE_ID,
            config.asign_pid,
            str(self.asign_seq),
            asign_datetime(self.date_order),
            asign_float(amounts["normal"]),
            asign_float(amounts["reduced1"]),
            asign_float(amounts["reduced2"]),
            asign_float(amounts["null"]),
            asign_float(amounts["special"]),
            encoded_turnover,
            config.asign_serial_hex,
            last_hash,
        ]
        return {
            "asign_serial": config.asign_serial_hex,
            "asign_counter": str(asign_counter),
            "asign_qrcode": f"_{'_'.join(asign_data)}",
            "asign_type": asign_type,
        }

    def _asign_create_signature(self, last_order):
        """Sign the prepared payload and return the full signature data."""
        data = self._asign_prepare_signature(last_order)
        user, password = self.env["asign.cert"]._get_login(data["asign_serial"])

        url = f"{ASIGN_ENDPOINT}/{user}/Sign/JWS"
        payload = {
            "password": password,
            "jws_payload": data["asign_qrcode"],
        }
        headers = {
            "Content-type": "application/json",
            "Accept": "text/plain",
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=ASIGN_TIMEOUT)
        resp.raise_for_status()
        resp_data = resp.json()

        error = resp_data.get("error")
        if error:
            raise ValidationError(self.env._("Online RKSV signing error: %s", error))

        result = resp_data.get("result")
        if not result:
            raise ValidationError(self.env._("Online RKSV signing has no result"))

        signation = asign_b64urldecode_nopadding(result.split(".")[-1])
        signation = base64.b64encode(signation).decode()

        data.update(
            {
                "asign_state": "s",
                "asign_qrcode": f"{data['asign_qrcode']}_{signation}",
                "asign_dep": result,
            }
        )
        return data

    def _asign_prepare_cancel(self):
        """Prepare a cancelled order holding a receipt number for signing.

        In Odoo 19 every order consumes a sequence number at creation, so a
        cancelled order has to show up as a signed receipt in the DEP to keep
        the receipt range gapless. Orders without any payment are zeroed
        first; the missing name is restored from the sequence number.
        """
        self.ensure_one()
        if self.currency_id.is_zero(self.amount_paid):
            self.lines.write(
                {
                    "qty": 0,
                    "price_unit": 0,
                    "price_subtotal": 0,
                    "price_subtotal_incl": 0,
                }
            )
            self.write({"amount_total": 0.0, "amount_tax": 0.0})
        vals = {"asign_state": "u"}
        if self.name == "/":
            vals["name"] = self._compute_order_name()
        self.write(vals)

    def _asign_add_signature(self, limit=10):
        """Sign this order, including missed previous unsigned orders."""
        self.ensure_one()
        self._compute_asign_seq()

        cr = self.env.cr
        cr.execute(
            """
            SELECT asign_seq, o.id
              FROM pos_order o
              JOIN pos_session s ON s.id = o.session_id
             WHERE s.config_id = %s
               AND o.asign_state = 's'
               AND o.asign_seq < %s
             ORDER BY o.asign_seq DESC
             LIMIT 1
            """,
            (self.session_id.config_id.id, self.asign_seq),
        )

        rows = cr.fetchall()
        last_seq, last_order_id = rows[0] if rows else (0, None)
        last_order = self.browse(last_order_id) if last_order_id else self.browse()

        if last_seq + 1 == self.asign_seq or not last_order:
            orders = self
        else:
            # Make sure new orders are flushed before searching, so the search
            # below picks up everything.
            self.flush_model()

            unsigned_orders = self.search(
                [
                    ("session_id.config_id", "=", self.session_id.config_id.id),
                    ("sequence_number", ">", last_seq),
                    ("state", "in", ("paid", "done", "cancel")),
                    ("asign_state", "!=", "s"),
                ],
                order="sequence_number ASC",
                limit=limit,
            )

            if not unsigned_orders:
                _logger.error(
                    "**RKSV** #0 No unsigned order found before %s, "
                    "but sequence does not match",
                    self.name,
                )
                return self.browse()

            if unsigned_orders[0].sequence_number == last_seq + 1:
                orders = unsigned_orders
            else:
                _logger.error(
                    "**RKSV** #1 Sequence number mismatch! "
                    "Last signed order: %s, current order: %s",
                    last_order.name,
                    self.name,
                )
                return self.browse()

        orders._compute_asign_seq()
        signed_orders = self.browse()
        for order in orders:
            if signed_orders and order.asign_seq != last_order.asign_seq + 1:
                _logger.error(
                    "**RKSV** #2 Sequence number mismatch! "
                    "Last signed order: %s, current order: %s",
                    last_order.name,
                    order.name,
                )
                return signed_orders

            if order.state == "cancel":
                order._asign_prepare_cancel()

            try:
                signature = order._asign_create_signature(last_order)
                order.write(signature)
                order.flush_model()
                signed_orders += order
            except (UserError, requests.exceptions.RequestException):
                _logger.exception("**RKSV** Error during signing order %s", order.name)
                return signed_orders

            last_order = order

        return signed_orders

    def action_pos_order_paid(self):
        res = super().action_pos_order_paid()

        if self.source != "pos":
            config = self.config_id
            if (
                not self.asign_state
                and config.asign_enabled
                and config.asign_state != "draft"
            ):
                self.asign_state = "u"
                self.asign_serial = ""
                self.asign_qrcode = ""
                self.asign_type = ""

        if self.state == "paid" and self.asign_state == "u":
            self._asign_add_signature()

        return res

    def _asign_sign_and_check_one(self):
        self.ensure_one()
        # cancelled orders are accepted as well; they are prepared as zeroed
        # receipts by _asign_prepare_cancel() inside the signing loop
        if self.state not in ("paid", "done", "cancel"):
            raise UserError(
                self.env._(
                    "Order %s is not paid, done or cancelled, cannot be signed",
                    self.name,
                )
            )
        signed_orders = self._asign_add_signature(limit=1)
        if signed_orders != self:
            raise UserError(self.env._("Order %s is not signed", self.name))
