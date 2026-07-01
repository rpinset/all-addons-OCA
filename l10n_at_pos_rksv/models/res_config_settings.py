# Copyright 2024 Weboffice IT-Service und Marketing GmbH & Co KG <https://weboffice.at>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import re

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    asign_state = fields.Selection(
        related="pos_config_id.asign_state",
        compute="_compute_asign",
        readonly=True,
    )
    asign_enabled = fields.Boolean(compute="_compute_asign", inverse="_inverse_asign")
    asign_method = fields.Selection(
        [
            ("card", "Card"),
            ("online", "Online"),
        ],
        compute="_compute_asign",
        inverse="_inverse_asign",
    )
    asign_serial_hex = fields.Char(
        string="a.sign Serial",
        help="Serial number of the certificate in hex format.",
        compute="_compute_asign",
        inverse="_inverse_asign",
    )
    asign_fid = fields.Char(compute="_compute_asign", inverse="_inverse_asign")
    asign_pid = fields.Char(compute="_compute_asign", inverse="_inverse_asign")
    asign_key = fields.Char(compute="_compute_asign", inverse="_inverse_asign")
    asign_crc = fields.Char(compute="_compute_asign", readonly=True)

    @api.onchange("asign_enabled")
    def _onchange_asign_enabled(self):
        self.env["pos.config"]._set_asign_defaults(self)

    @api.depends("pos_config_id")
    def _compute_asign(self):
        for record in self:
            config = record.pos_config_id
            record.asign_enabled = config.asign_enabled
            record.asign_method = config.asign_method
            record.asign_serial_hex = config.asign_serial_hex
            record.asign_fid = config.asign_fid
            record.asign_pid = config.asign_pid
            record.asign_key = config.asign_key
            record.asign_crc = config.asign_crc

    def _inverse_asign(self):
        """Persist the wizard values back into ``pos.config``."""
        for record in self:
            config = record.pos_config_id
            if not config:
                continue

            update = {"asign_enabled": record.asign_enabled}

            if not config.asign_state or config.asign_state == "draft":
                update.update(
                    {
                        "asign_enabled": record.asign_enabled,
                        "asign_method": record.asign_method,
                        "asign_fid": record.asign_fid,
                        "asign_key": record.asign_key,
                    }
                )

                if record.asign_serial_hex:
                    update["asign_serial_hex"] = f"{int(record.asign_serial_hex, 16):x}"

                fiscal_pid = record.asign_pid
                if fiscal_pid:
                    fiscal_pid = re.sub(r"[^0-9A-Za-z]", "", fiscal_pid)

                if fiscal_pid:
                    update["asign_pid"] = fiscal_pid
                    config.order_seq_id.implementation = "no_gap"
                    config.order_seq_id.name = fiscal_pid.replace("/", "")
                    config.order_seq_id.prefix = f"{fiscal_pid}/"
                    config.order_seq_id.suffix = None

            if update:
                config.write(update)

    def action_asign_assign(self):
        self.ensure_one()
        self.pos_config_id.action_asign_assign()

    def action_asign_reset(self):
        self.ensure_one()
        self.pos_config_id.action_asign_reset()
