# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import objectify

from odoo import models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def _generate_payment_identification_block(self, parent_node, gen_args):
        self.ensure_one()
        order_obj = self.env["account.payment.order"]
        payment_identification = objectify.SubElement(parent_node, "PmtId")
        payment_ident_val = self.memo or str(self.id)
        payment_identification.InstrId = order_obj._prepare_field(
            "Instruction Identification",
            payment_ident_val,
            35,
            gen_args,
            raise_if_oversized=True,
        )
        payment_identification.EndToEndId = order_obj._prepare_field(
            "End to End Identification",
            payment_ident_val,
            35,
            gen_args,
            raise_if_oversized=True,
        )

    def _generate_amount_block(self, parent_node, amount_control_sum_a):
        self.ensure_one()
        parent_node.InstdAmt = self.currency_id._pain_format(self.amount)
        parent_node.InstdAmt.set("Ccy", self.currency_id.name)
        amount_control_sum_a += self.amount
        return amount_control_sum_a

    def _generate_remittance_info_block(self, parent_node, gen_args):
        self.ensure_one()
        order_obj = self.env["account.payment.order"]
        remittance_info = objectify.SubElement(parent_node, "RmtInf")
        communication_type = self.payment_line_ids[:1].communication_type
        if communication_type == "free":
            remittance_info.Ustrd = order_obj._prepare_field(
                "Remittance Unstructured Information",
                self.payment_reference,
                140,
                gen_args,
            )
        elif communication_type == "structured":
            remittance_info_structured = objectify.SubElement(remittance_info, "Strd")
            creditor_ref_information = objectify.SubElement(
                remittance_info_structured, "CdtrRefInf"
            )
            if gen_args.get("structured_remittance_issuer", True):
                creditor_ref_info_type = objectify.SubElement(
                    creditor_ref_information, "Tp"
                )
                creditor_ref_info_type_or = objectify.SubElement(
                    creditor_ref_info_type, "CdOrPrtry"
                )
                creditor_ref_info_type_or.Cd = "SCOR"
                creditor_ref_info_type.Issr = "ISO"

            creditor_ref_information.Ref = order_obj._prepare_field(
                "Creditor Structured Reference",
                self.payment_reference,
                35,
                gen_args,
                raise_if_oversized=True,
            )

    def _generate_purpose(self, parent_node):
        self.ensure_one()
        payment_line = self.payment_line_ids[:1]
        if payment_line.purpose:
            purpose = objectify.SubElement(parent_node, "Purp")
            purpose.Cd = payment_line.purpose

    def _generate_regulatory_reporting(self, parent_node, gen_args):
        self.ensure_one()
        order_obj = self.env["account.payment.order"]
        payment_line = self.payment_line_ids[:1]
        if payment_line.regulatory_reporting_id:
            regulatory_reporting = objectify.SubElement(parent_node, "RgltryRptg")
            regulatory_reporting_details = objectify.SubElement(
                regulatory_reporting, "Dtls"
            )
            regulatory_reporting_details.Cd = order_obj._prepare_field(
                "Regulatory Details Code",
                payment_line.regulatory_reporting_id.code,
                10,
                gen_args,
                raise_if_oversized=True,
            )
