# Copyright 2024 Weboffice IT-Service und Marketing GmbH & Co KG <https://weboffice.at>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import base64
import hashlib
import logging
import re
import secrets
import uuid

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

AES_KEY_SIZE = 32
CRC_N = 3


def next_sequence(records, field):
    """Return the next sequence value following the highest one in ``records``.

    The sequence is incremented numerically, preserving any non-numeric prefix
    and suffix as well as the original zero-padding width.
    """
    if not records:
        return None
    sequences = [v for v in records.mapped(field) if v]
    if not sequences:
        return None
    last_sequence = max(sequences)
    match = re.match(r"([^0-9]*)([0-9]+)(.*)", last_sequence)
    if not match:
        return None
    next_no = str(int(match.group(2)) + 1)
    next_no = next_no.zfill(len(match.group(2)))
    return f"{match.group(1)}{next_no}{match.group(3)}"


class PosConfig(models.Model):
    _inherit = "pos.config"

    _unique_asign_pid = models.UniqueIndex(
        "(company_id, asign_pid) WHERE (asign_pid IS NOT NULL)",
        "Fiscal POS-ID has to be unique for the company",
    )

    asign_enabled = fields.Boolean(
        string="a.sign Enabled",
        help="Enable Austrian RKSV (a.sign) signing for this POS.",
    )
    asign_method = fields.Selection(
        [
            ("card", "Card"),
            ("online", "Online"),
        ],
        string="a.sign Method",
        default="online",
    )
    asign_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("assigned", "Assigned"),
            ("active", "Active"),
        ],
        string="a.sign State",
        default="draft",
        readonly=True,
        copy=False,
    )
    asign_serial_hex = fields.Char(
        string="a.sign Serial",
        help="Serial number of the certificate in hex format.",
    )
    asign_fid = fields.Char(
        string="a.sign Fiscal ID",
        help="VAT or tax number of the company for the POS.",
    )
    asign_pid = fields.Char(
        string="a.sign POS ID",
        help=(
            "Fiscal ID of the POS system inside the company, used as "
            "prefix of the order number."
        ),
        copy=False,
    )
    asign_key = fields.Char(
        string="a.sign Encryption Key",
        help="The AES encryption key of the journal.",
        copy=False,
    )
    asign_crc = fields.Char(
        string="a.sign Checksum",
        compute="_compute_asign_crc",
        help="Checksum of the encryption key.",
        copy=False,
        store=True,
    )
    asign_start_order_id = fields.Many2one(
        "pos.order",
        string="Start Order",
        compute="_compute_asign_start_order_id",
        store=False,
    )
    asign_seq_id = fields.Many2one(
        "ir.sequence",
        string="a.sign Sequence",
        help=(
            "Dedicated gapless sequence for the RKSV receipt number "
            "(asign_seq). It is consumed only when a receipt is signed, so "
            "signed receipts stay consecutive regardless of cancelled orders."
        ),
        readonly=True,
        copy=False,
    )

    def _default_asign_fid(self):
        return self.env.company.vat

    def _default_asign_pid(self):
        configs = self.env["pos.config"].search(
            [("company_id", "=", self.env.company.id)]
        )
        return next_sequence(configs, "asign_pid") or "K01"

    def _default_asign_key(self):
        return base64.b64encode(secrets.token_bytes(AES_KEY_SIZE)).decode()

    def _get_asign_start_order(self):
        return self.env["pos.order"].search(
            [
                ("config_id", "=", self.id),
                ("asign_state", "=", "s"),
                ("asign_type", "=", "s"),
            ]
        )

    def _compute_asign_start_order_id(self):
        for config in self:
            config.asign_start_order_id = config._get_asign_start_order()

    def _asign_seq(self):
        """Return the dedicated gapless RKSV receipt sequence, creating it once.

        The receipt number (``asign_seq``) is drawn from this no-gap sequence
        only at signing time, so it is independent from the POS order number
        (``sequence_number``) that every order consumes at creation.
        """
        self.ensure_one()
        if not self.asign_seq_id:
            self.asign_seq_id = (
                self.env["ir.sequence"]
                .sudo()
                .create(
                    {
                        "name": f"RKSV {self.asign_pid or self.name}",
                        "implementation": "no_gap",
                        "padding": 0,
                        "number_increment": 1,
                        "number_next": 1,
                        "company_id": self.company_id.id,
                    }
                )
            )
        return self.asign_seq_id

    @api.model
    def _set_asign_defaults(self, record):
        record.ensure_one()
        if not record.asign_enabled:
            return
        if not record.asign_fid:
            record.asign_fid = self._default_asign_fid()
        if not record.asign_pid:
            record.asign_pid = self._default_asign_pid()
        if not record.asign_key:
            record.asign_key = self._default_asign_key()

    @api.constrains("asign_enabled")
    def _check_asign_config(self):
        for config in self:
            if not config.asign_enabled:
                continue

            self._set_asign_defaults(config)

            if not config.asign_method:
                raise ValidationError(
                    self.env._(
                        "Austrian RKSV activated but method is empty for POS %s",
                        config.name,
                    )
                )
            if not config.asign_state:
                raise ValidationError(
                    self.env._(
                        "Austrian RKSV activated but state is invalid for POS %s",
                        config.name,
                    )
                )
            if not config.asign_serial_hex:
                raise ValidationError(
                    self.env._(
                        "Austrian RKSV activated but serial is empty for POS %s",
                        config.name,
                    )
                )
            if not config.asign_fid:
                raise ValidationError(
                    self.env._(
                        "Austrian RKSV activated but fiscal ID is empty for POS %s",
                        config.name,
                    )
                )
            if not config.asign_pid:
                raise ValidationError(
                    self.env._(
                        "Austrian RKSV activated but POS ID is empty for POS %s",
                        config.name,
                    )
                )
            if not config.asign_key:
                raise ValidationError(
                    self.env._(
                        "Austrian RKSV activated but encryption key is empty "
                        "for POS %s",
                        config.name,
                    )
                )
            if len(base64.b64decode(config.asign_key)) != AES_KEY_SIZE:
                raise ValidationError(
                    self.env._(
                        "Austrian RKSV activated but encryption key has invalid "
                        "length (%(length)s != %(expected)s) for POS %(name)s",
                        length=len(config.asign_key),
                        expected=AES_KEY_SIZE,
                        name=config.name,
                    )
                )

            if config.asign_method == "online":
                self.env["asign.cert"]._get_cert(config.asign_serial_hex)

    @api.depends("asign_key")
    def _compute_asign_crc(self):
        for config in self:
            if not config.asign_key:
                config.asign_crc = ""
                continue
            checksum = hashlib.sha256(config.asign_key.encode()).digest()[:CRC_N]
            config.asign_crc = base64.b64encode(checksum).decode().rstrip("=")

    def action_asign_assign(self):
        configs = self.filtered(lambda c: c.asign_enabled and c.asign_state == "draft")
        with_open = configs.filtered("has_active_session")
        if with_open:
            raise UserError(
                self.env._(
                    "POS %s has open sessions. Close them first.",
                    with_open[0].name,
                )
            )
        configs.write({"asign_state": "assigned"})
        for config in configs:
            config._asign_seq()

    def action_asign_reset(self):
        configs = self.filtered(
            lambda c: c.asign_enabled and c.asign_state in ("assigned", "active")
        )
        with_open = configs.filtered("has_active_session")
        if with_open:
            raise UserError(
                self.env._(
                    "POS %s has open sessions. Close them first.",
                    with_open[0].name,
                )
            )
        configs.write({"asign_state": "draft"})

    def _load_pos_data_fields(self, config):
        res = super()._load_pos_data_fields(config)
        if not res:
            return res
        res += [
            "asign_enabled",
            "asign_state",
            "asign_method",
            "asign_pid",
            "asign_fid",
        ]
        return res

    def _asign_dep_create(self, dep_export):
        return {
            "Belege-Gruppe": [
                {
                    "Signaturzertifikat": "",
                    "Zertifizierungsstellen": [],
                    "Belege-kompakt": dep_export,
                }
            ]
        }

    def _asign_dep_export(self):
        self.ensure_one()
        dep_export = [
            row["asign_dep"]
            for row in self.env["pos.order"].search_read(
                [
                    ("config_id", "=", self.id),
                    ("asign_state", "=", "s"),
                ],
                ["asign_dep"],
                order="asign_seq asc",
            )
        ]
        return self._asign_dep_create(dep_export)

    def _check_asign_before_creating_new_session(self):
        if self.asign_enabled and self.asign_state == "draft":
            raise ValidationError(
                self.env._(
                    "POS %s has enabled a.sign but certificate is not assigned.",
                    self.name,
                )
            )

    def _check_before_creating_new_session(self):
        res = super()._check_before_creating_new_session()
        self._check_asign_before_creating_new_session()
        return res

    def _asign_create_zero_receipt(self):
        self.ensure_one()

        if self.has_active_session:
            raise UserError(
                self.env._("POS %s has open sessions. Close them first.", self.name)
            )

        if not self.asign_enabled:
            raise UserError(self.env._("POS %s has a.sign disabled.", self.name))

        self._check_asign_before_creating_new_session()

        cash_register_balance_start = 0.0
        cash_register_balance_end_real = 0.0
        last_session = self.env["pos.session"].search(
            [("config_id", "=", self.id)], order="id desc", limit=1
        )
        if last_session:
            cash_register_balance_start = last_session.cash_register_balance_end_real
            cash_register_balance_end_real = last_session.cash_register_balance_end_real

        session = self.env["pos.session"].create(
            {
                "name": "/",
                "user_id": self.env.uid,
                "config_id": self.id,
            }
        )

        session.set_opening_control(
            cash_register_balance_start, self.env._("Zero Receipt")
        )
        session.cash_register_balance_end_real = cash_register_balance_end_real

        date_order = fields.Datetime.to_string(fields.Datetime.now())
        order_data = {
            "uuid": str(uuid.uuid4()),
            "name": "/",
            "date_order": date_order,
            "partner_id": None,
            "fiscal_position_id": None,
            "amount_return": 0.0,
            "to_invoice": False,
            "shipping_date": None,
            "asign_state": "u",
            "asign_type": "0",
            "session_id": session.id,
            "user_id": self.env.uid,
            "amount_paid": 0.0,
            "amount_total": 0.0,
            "amount_tax": 0.0,
            "lines": [],
        }

        pos_order_model = self.env["pos.order"]
        result = pos_order_model.sync_from_ui([order_data])["pos.order"]
        session.close_session_from_ui()

        zero_order = pos_order_model.browse([row["id"] for row in result])
        zero_order.ensure_one()
        if zero_order.asign_state != "s":
            raise ValidationError(self.env._("Created zero-receipt was not signed."))
        return zero_order

    def _asign_repair_signed_names(self):
        """Restore names of signed receipts overwritten by a concurrent cancel.

        A lost-update race can reset the name of an already signed receipt to
        ``'/'``. The signature already covers the receipt, so only the name is
        restored from its RKSV sequence number (``asign_seq``). Cancelled
        orders never receive an ``asign_seq`` and therefore need no repair.
        """
        self.ensure_one()

        orders = self.env["pos.order"].search(
            [
                ("config_id", "=", self.id),
                ("asign_state", "=", "s"),
                ("asign_seq", ">", 0),
                ("name", "=", "/"),
            ]
        )
        for order in orders:
            order.name = order._compute_order_name()
            _logger.warning(
                "**RKSV** restored name %s of signed receipt for POS %s",
                order.name,
                self.name,
            )

    def _asign_sign_missed(self):
        """Sign paid/done receipts that were created but not signed yet.

        Cancelled orders are skipped on purpose: they do not consume a receipt
        number, so they cannot create a gap in the signed range.
        """
        self.ensure_one()
        pos_order_model = self.env["pos.order"]

        self._asign_repair_signed_names()

        while True:
            order = pos_order_model.search(
                [
                    ("config_id", "=", self.id),
                    ("state", "in", ("paid", "done")),
                    ("asign_state", "=", "u"),
                ],
                order="sequence_number desc",
                limit=1,
            )
            if not order:
                return

            signed_orders = order._asign_add_signature()
            if not signed_orders:
                _logger.warning(
                    "**RKSV** unable to sign missed order %s for POS %s",
                    order.name,
                    self.name,
                )
                return

            _logger.warning(
                "**RKSV** signed %s missed receipt(s) up to %s for POS %s",
                len(signed_orders),
                signed_orders[-1].name,
                self.name,
            )

    def _cron_asign_sign_missed(self):
        configs = self
        if not configs:
            configs = self.search(
                [
                    ("asign_enabled", "=", True),
                    ("asign_state", "in", ["assigned", "active"]),
                ]
            )
        for config in configs:
            _logger.info("**RKSV** Check missed orders for POS %s", config.name)
            config._asign_sign_missed()

    def action_asign_zero_receipt(self):
        self._asign_create_zero_receipt()
