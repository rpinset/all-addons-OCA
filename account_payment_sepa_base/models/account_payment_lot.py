# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import objectify

from odoo import api, fields, models


class AccountPaymentLot(models.Model):
    _inherit = "account.payment.lot"

    priority = fields.Selection("_priority_selection", readonly=True)
    local_instrument = fields.Selection("_local_instrument_selection", readonly=True)
    category_purpose = fields.Selection("_category_purpose_selection", readonly=True)

    @api.model
    def _priority_selection(self):
        return self._prepare_selection("priority")

    @api.model
    def _local_instrument_selection(self):
        return self._prepare_selection("local_instrument")

    @api.model
    def _category_purpose_selection(self):
        return self._prepare_selection("category_purpose")

    @api.model
    def _prepare_selection(self, field):
        res = self.env["account.payment.line"].fields_get(field, "selection")[field][
            "selection"
        ]
        return res

    def _generate_start_payment_info_block(
        self,
        parent_node,
        gen_args,
    ):
        self.ensure_one()
        order = self.order_id
        payment_info = objectify.SubElement(parent_node, "PmtInf")
        payment_info.PmtInfId = order._prepare_field(
            "Payment Information Identification",
            self.name,
            35,
            gen_args,
            raise_if_oversized=True,
        )
        payment_info.PmtMtd = gen_args["payment_method"]
        payment_info.BtchBookg = str(order.batch_booking).lower()
        # The "SEPA Customer-to-bank
        # Implementation guidelines" for SCT and SDD says that control sum
        # and nb_of_transactions should be present
        # at both "group header" level and "payment info" level
        payment_info.NbOfTxs = str(self.payment_count)
        payment_info.CtrlSum = self.currency_id._pain_format(self.amount)
        payment_type_info = objectify.SubElement(payment_info, "PmtTpInf")
        if self.priority and gen_args["payment_method"] != "DD":
            payment_type_info.InstrPrty = self.priority
        if order.sepa:
            service_level = objectify.SubElement(payment_type_info, "SvcLvl")
            service_level.Cd = "SEPA"
        if self.local_instrument:
            local_instrument_root = objectify.SubElement(payment_type_info, "LclInstrm")
            if gen_args.get("local_instrument_type") == "proprietary":
                local_instrument_root.Prtry = self.local_instrument
            else:
                local_instrument_root.Cd = self.local_instrument
        if gen_args["payment_method"] == "DD" and self.sequence_type:
            payment_type_info.SeqTp = self.sequence_type
        if self.category_purpose:
            category_purpose_node = objectify.SubElement(payment_type_info, "CtgyPurp")
            category_purpose_node.Cd = self.category_purpose
        if gen_args["payment_method"] == "DD":
            payment_info.ReqdColltnDt = self.date.strftime(gen_args["date_fmt"])
        else:
            if gen_args["pain_flavor"].startswith("pain.001.001.09"):
                requested_exec_date = objectify.SubElement(payment_info, "ReqdExctnDt")
                requested_exec_date.Dt = self.date.strftime(gen_args["date_fmt"])
            else:
                payment_info.ReqdExctnDt = self.date.strftime(gen_args["date_fmt"])
        return payment_info
