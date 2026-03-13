# Copyright 2010-2020 Akretion (www.akretion.com)
# Copyright 2014-2022 Tecnativa - Pedro M. Baeza
# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from lxml import etree

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools.xml_utils import create_xml_node_chain


class AccountPaymentOrder(models.Model):
    _inherit = "account.payment.order"

    def generate_payment_file(self):  # noqa: C901
        """Creates the International Transfer file. That's the important code!"""
        # Code very similar to https://github.com/OCA/bank-payment/blob/17.0/account_banking_sepa_credit_transfer/models/account_payment_order.py#L14
        # but with intermediary bank support
        self.ensure_one()
        if self.payment_method_id.code != "international_credit_transfer":
            return super().generate_payment_file()

        pain_flavor = self.payment_method_id.pain_version
        # We use pain_flavor.startswith('pain.001.001.xx')
        # to support country-specific extensions such as
        # pain.001.001.03.ch.02 (cf l10n_ch_sepa)
        if not pain_flavor:
            raise UserError(_("PAIN version must be set on the payment method."))
        elif pain_flavor.startswith("pain.001.001.03"):
            bic_xml_tag = "BIC"
            # size 70 -> 140 for <Nm> with pain.001.001.03
            # BUT the European Payment Council, in the document
            # "SEPA Credit Transfer Scheme Customer-to-bank
            # Implementation guidelines" v6.0 available on
            # http://www.europeanpaymentscouncil.eu/knowledge_bank.cfm
            # says that 'Nm' should be limited to 70
            # so we follow the "European Payment Council"
            # and we put 70 and not 140
            name_maxsize = 70
            root_xml_tag = "CstmrCdtTrfInitn"
        else:
            raise UserError(
                _(
                    "PAIN version '%s' is not supported for international credit "
                    "transfers.",
                    pain_flavor,
                )
            )
        xsd_file = self.payment_method_id.get_xsd_file_path()
        gen_args = {
            "bic_xml_tag": bic_xml_tag,
            "name_maxsize": name_maxsize,
            "convert_to_ascii": self.payment_method_id.convert_to_ascii,
            "payment_method": "TRF",
            "file_prefix": "sct_",
            "pain_flavor": pain_flavor,
            "pain_xsd_file": xsd_file,
        }
        nsmap = self.generate_pain_nsmap()
        attrib = self.generate_pain_attrib()
        xml_root = etree.Element("Document", nsmap=nsmap, attrib=attrib)
        pain_root = etree.SubElement(xml_root, root_xml_tag)
        # A. Group header
        header = self.generate_group_header_block(pain_root, gen_args)
        group_header, nb_of_transactions_a, control_sum_a = header
        transactions_count_a = 0
        amount_control_sum_a = 0.0
        lines_per_group = {}
        # key = (requested_date, priority, local_instrument, categ_purpose)
        # values = list of lines as object
        for line in self.payment_ids:
            payment_line = line.payment_line_ids[:1]
            priority = payment_line.priority
            local_instrument = payment_line.local_instrument
            categ_purpose = payment_line.category_purpose
            # The field line.payment_line_date is the requested payment date
            key = (line.payment_line_date, priority, local_instrument, categ_purpose)
            if key in lines_per_group:
                lines_per_group[key].append(line)
            else:
                lines_per_group[key] = [line]
        for (requested_date, priority, local_instrument, categ_purpose), lines in list(
            lines_per_group.items()
        ):
            # B. Payment info
            requested_date = fields.Date.to_string(requested_date)
            (
                payment_info,
                nb_of_transactions_b,
                control_sum_b,
            ) = self.generate_start_payment_info_block(
                pain_root,
                "self.name + '-' "
                "+ requested_date.replace('-', '')  + '-' + priority + "
                "'-' + local_instrument + '-' + category_purpose",
                priority,
                local_instrument,
                categ_purpose,
                False,
                requested_date,
                {
                    "self": self,
                    "priority": priority,
                    "requested_date": requested_date,
                    "local_instrument": local_instrument or "NOinstr",
                    "category_purpose": categ_purpose or "NOcateg",
                },
                gen_args,
            )
            self.generate_party_block(
                payment_info, "Dbtr", "B", self.company_partner_bank_id, gen_args
            )
            charge_bearer = etree.SubElement(payment_info, "ChrgBr")
            if self.sepa:
                charge_bearer_text = "SLEV"
            else:
                charge_bearer_text = self.charge_bearer
            charge_bearer.text = charge_bearer_text
            transactions_count_b = 0
            amount_control_sum_b = 0.0
            for line in lines:
                transactions_count_a += 1
                transactions_count_b += 1
                # C. Credit Transfer Transaction Info
                credit_transfer_transaction_info = etree.SubElement(
                    payment_info, "CdtTrfTxInf"
                )
                payment_identification = etree.SubElement(
                    credit_transfer_transaction_info, "PmtId"
                )
                instruction_identification = etree.SubElement(
                    payment_identification, "InstrId"
                )
                instruction_identification.text = self._prepare_field(
                    "Instruction Identification",
                    "str(line.move_id.id)",
                    {"line": line},
                    35,
                    gen_args=gen_args,
                )
                end2end_identification = etree.SubElement(
                    payment_identification, "EndToEndId"
                )
                end2end_identification.text = self._prepare_field(
                    "End to End Identification",
                    "str(line.move_id.id)",
                    {"line": line},
                    35,
                    gen_args=gen_args,
                )
                currency_name = self._prepare_field(
                    "Currency Code",
                    "line.currency_id.name",
                    {"line": line},
                    3,
                    gen_args=gen_args,
                )
                amount = etree.SubElement(credit_transfer_transaction_info, "Amt")
                instructed_amount = etree.SubElement(
                    amount, "InstdAmt", Ccy=currency_name
                )
                instructed_amount.text = "%.2f" % line.amount
                amount_control_sum_a += line.amount
                amount_control_sum_b += line.amount
                if not (line_partner_bank := line.partner_bank_id):
                    raise UserError(
                        _(
                            "Bank account is missing on the bank payment line "
                            "of partner '%(partner)s' (reference '%(reference)s').",
                            partner=line.partner_id.name,
                            reference=line.name,
                        )
                    )
                # Intermediary bank, specific to international credit transfers
                if not (intermediary_bank := line_partner_bank.intermediary_bank_id):
                    raise UserError(
                        _(
                            "Intermediary bank is missing on the recipient bank "
                            "account of partner '%(partner)s' "
                            "(reference '%(reference)s').",
                            partner=line.partner_id.name,
                            reference=line.name,
                        )
                    )
                financial_institution = create_xml_node_chain(
                    credit_transfer_transaction_info, ["IntrmyAgt1", "FinInstnId"]
                )[-1]
                intermediary_bic = etree.SubElement(financial_institution, bic_xml_tag)
                intermediary_bic.text = intermediary_bank.bic
                intermediary_name = etree.SubElement(financial_institution, "Nm")
                intermediary_name.text = intermediary_bank.name[:name_maxsize]
                self.generate_party_block(
                    credit_transfer_transaction_info,
                    "Cdtr",
                    "C",
                    line_partner_bank,
                    gen_args,
                    line,
                    bank_name=line_partner_bank.bank_id.name
                    if line_partner_bank.bank_id
                    else None,
                )
                line_purpose = line.payment_line_ids[:1].purpose
                if line_purpose:
                    purpose = etree.SubElement(credit_transfer_transaction_info, "Purp")
                    etree.SubElement(purpose, "Cd").text = line_purpose
                self.generate_remittance_info_block(
                    credit_transfer_transaction_info, line, gen_args
                )

                nb_of_transactions_b.text = str(transactions_count_b)
                control_sum_b.text = "%.2f" % amount_control_sum_b
            nb_of_transactions_a.text = str(transactions_count_a)
            control_sum_a.text = "%.2f" % amount_control_sum_a
        return self.finalize_pain_file_creation(xml_root, gen_args)
