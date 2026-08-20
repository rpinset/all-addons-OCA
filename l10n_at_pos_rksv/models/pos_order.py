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


class AsignSequenceError(Exception):
    """Receipt numbers would not be strictly consecutive; abort signing."""


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
        copy=False,
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
        copy=False,
    )
    asign_counter = fields.Char(
        string="a.sign Counter",
        help="The turnover counter of the RKSV signature.",
        readonly=True,
        copy=False,
    )
    asign_qrcode = fields.Char(
        string="a.sign QR-Code",
        help="The QR code of the RKSV signature.",
        index=True,
        readonly=True,
        copy=False,
    )
    asign_dep = fields.Text(
        string="a.sign DEP",
        help="The DEP entry of the RKSV signature export.",
        readonly=True,
        copy=False,
    )
    asign_serial = fields.Char(
        string="a.sign Serial",
        help="The serial number of the RKSV signing component.",
        readonly=True,
        copy=False,
    )
    asign_seq = fields.Integer(
        string="a.sign Sequence",
        help="The sequence number of the RKSV signature export.",
        readonly=True,
        index=True,
        copy=False,
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
        session = session or self.session_id
        config = session.config_id if session else self.config_id
        if self.asign_state or config.asign_enabled:
            # The receipt number is only known once the order is signed; until
            # then keep the placeholder name so the order is not numbered.
            if not self.asign_seq:
                return self.name or "/"
            return config.order_seq_id.get_next_char(self.asign_seq)
        return super()._compute_order_name(session)

    def _prepare_refund_values(self, current_session):
        """Make backend refunds go through the regular RKSV signing flow.

        The base implementation names the refund "<original> REFUND"; with
        RKSV enabled the refund must instead draw its own gapless receipt
        number at signing time, so keep the placeholder name and mark the
        order as unsigned.
        """
        vals = super()._prepare_refund_values(current_session)
        config = current_session.config_id
        if config.asign_enabled and config.asign_state != "draft":
            vals["name"] = "/"
            vals["asign_state"] = "u"
        return vals

    def _asign_next_seq(self):
        """Assign the next gapless RKSV receipt number and the final name.

        The receipt number is drawn from the dedicated per-POS sequence and is
        independent from ``sequence_number`` (the order number consumed at
        creation), so it stays gapless across cancelled or skipped orders.
        """
        self.ensure_one()
        sequence = self.session_id.config_id._asign_seq()
        self.asign_seq = int(sequence.next_by_id())
        self.name = self._compute_order_name()

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

    def _asign_add_signature(self, limit=10):
        """Sign this order, including earlier unsigned receipts of the POS.

        Receipts are signed in creation order (``sequence_number``) and each
        one draws the next gapless ``asign_seq`` from the dedicated POS
        sequence. Cancelled orders are not signed and do not consume a receipt
        number, so the signed range stays gapless without any repair.
        """
        self.ensure_one()
        config = self.session_id.config_id

        # Ensure the dedicated sequence exists outside the per-order savepoint
        # so it is not recreated on a signing rollback.
        config._asign_seq()

        # Flush new orders so the searches below pick up everything.
        self.flush_model()

        # The chain continues from the last signed receipt of this POS.
        last_order = self.search(
            [
                ("config_id", "=", config.id),
                ("asign_state", "=", "s"),
            ],
            order="asign_seq desc",
            limit=1,
        )

        orders = self.search(
            [
                ("config_id", "=", config.id),
                ("state", "in", ("paid", "done")),
                ("asign_state", "=", "u"),
                ("sequence_number", "<=", self.sequence_number),
            ],
            order="sequence_number asc",
            limit=limit,
        )

        signed_orders = self.browse()
        for order in orders:
            try:
                # Draw the receipt number and sign atomically: on failure the
                # savepoint rollback releases the consumed sequence number, so
                # no gap is created in the signed range.
                with self.env.cr.savepoint():
                    order._asign_next_seq()
                    # Defensive guard: the dedicated no-gap sequence must yield
                    # strictly consecutive receipt numbers. A mismatch points to
                    # a tampered sequence or a concurrent signer; abort before
                    # writing a broken chain (the savepoint releases the number).
                    if last_order and order.asign_seq != last_order.asign_seq + 1:
                        raise AsignSequenceError(order.id, order.asign_seq)
                    signature = order._asign_create_signature(last_order)
                    order.write(signature)
                    order.flush_model()
            except AsignSequenceError as err:
                order_id, drawn_seq = err.args
                last_seq = last_order.asign_seq
                order.invalidate_recordset()
                _logger.error(
                    "**RKSV** Receipt sequence mismatch for POS %s: order #%s "
                    "drew asign_seq %s but last signed receipt was %s; aborting.",
                    config.name,
                    order_id,
                    drawn_seq,
                    last_seq,
                )
                return signed_orders
            except (UserError, requests.exceptions.RequestException):
                order.invalidate_recordset()
                _logger.exception("**RKSV** Error during signing order %s", order.name)
                return signed_orders

            signed_orders += order
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
