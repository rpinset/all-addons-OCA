# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class HrEmployee(models.Model):
    _name = "hr.employee"
    _inherit = ["hr.employee", "iot.key.mixin"]

    iot_key_id = fields.Many2one(
        "iot.key", compute="_compute_iot_key", search="_search_iot_key"
    )
    iot_key_ids = fields.One2many(context={"active_test": False}, string="IoT Keys")
    rule_ids = fields.Many2many(
        "iot.rule",
        related="iot_key_id.rule_ids",
        readonly=False,
        string="IoT Rules",
    )
    rfid_card_code = fields.Char(
        store=True,
        compute="_compute_rfid_card_code",
        inverse="_inverse_rfid_card_code",
    )

    @api.model
    def _search_iot_key(self, operator, value):
        if operator not in ["=", "!=", "in", "not in"]:
            raise ValueError("Operator not supported for iot_key_id search")
        employees = self.search([("iot_key_ids", operator, value)])
        return [("id", "in", employees.ids)]

    @api.depends("iot_key_ids.unique_virtual_key", "iot_key_ids")
    def _compute_rfid_card_code(self):
        for record in self:
            if record.iot_key_ids:
                record.rfid_card_code = record.iot_key_ids.unique_virtual_key

    def _inverse_rfid_card_code(self):
        for record in self:
            if record.iot_key_ids:
                record.iot_key_ids.unique_virtual_key = record.rfid_card_code

    @api.depends("iot_key_ids")
    def _compute_iot_key(self):
        for record in self:
            record.iot_key_id = record.iot_key_ids[:1] if record.iot_key_ids else False

    def _generate_iot_key_vals(self):
        return {
            "unique_virtual_key": self.rfid_card_code,
            "name": _("%s / RFID") % self.display_name,
            "key_type": "RFID",
            "res_id": self.id,
            "res_model": self._name,
        }

    def generate_iot_key(self):
        self.ensure_one()
        if not self.iot_key_id and self.rfid_card_code:
            self.env["iot.key"].create(self._generate_iot_key_vals())
            self.invalidate_recordset()
            self._compute_rfid_card_code()
        return {}
