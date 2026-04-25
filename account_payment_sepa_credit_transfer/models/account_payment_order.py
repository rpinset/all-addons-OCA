# Copyright 2010-2020 Akretion (www.akretion.com)
# Copyright 2014-2022 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from lxml import objectify

from odoo import models
from odoo.exceptions import UserError


class AccountPaymentOrder(models.Model):
    _inherit = "account.payment.order"

    def generate_payment_file(self):
        """Creates the SEPA Credit Transfer file. That's the important code!"""
        self.ensure_one()
        if self.payment_method_id.code != "sepa_credit_transfer":
            return super().generate_payment_file()

        pain_flavor = self.payment_method_id.pain_version
        # We use pain_flavor.startswith('pain.001.001.xx')
        # to support country-specific extensions such as
        # pain.001.001.03.ch.02 (cf l10n_ch_sepa)
        if not pain_flavor:
            raise UserError(
                self.env._("PAIN version '%s' is not supported.", pain_flavor)
            )
        elif pain_flavor.startswith(("pain.001.001.03", "pain.001.003.03")):
            # pain.001.003.03 is for German Banks
            # it is not in the offical ISO 20022 documentations, but nearly all
            # german banks are working with this instead 001.001.03
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
        elif pain_flavor.startswith("pain.001.001.09"):
            bic_xml_tag = "BICFI"
            name_maxsize = 140
        else:
            raise UserError(
                self.env._("PAIN version '%s' is not supported.", pain_flavor)
            )
        xsd_file = self.payment_method_id._get_xsd_file_path()
        gen_args = {
            "bic_xml_tag": bic_xml_tag,
            "name_maxsize": name_maxsize,
            "convert_to_ascii": self._convert_to_ascii(),
            "payment_method": "TRF",
            "pain_flavor": pain_flavor,
            "pain_xsd_file": xsd_file,
            "date_fmt": "%Y-%m-%d",
        }
        nsmap = self._generate_pain_nsmap()
        attrib = self._generate_pain_attrib()
        xml_root = objectify.Element("Document", nsmap=nsmap, attrib=attrib)
        pain_root = objectify.SubElement(xml_root, "CstmrCdtTrfInitn")
        # A. Group header
        group_header = self._generate_group_header_block(pain_root, gen_args)
        transactions_count_a = 0
        amount_control_sum_a = 0.0
        for lot in self.payment_lot_ids:
            # B. Payment info
            payment_info = lot._generate_start_payment_info_block(pain_root, gen_args)
            self.company_partner_bank_id._generate_party_block(
                payment_info, "B", gen_args
            )
            self._generate_charge_bearer(payment_info)
            for payment in lot.payment_ids:
                # C. Credit Transfer Transaction Info
                transactions_count_a += 1
                trf_transaction_info = objectify.SubElement(payment_info, "CdtTrfTxInf")
                payment._generate_payment_identification_block(
                    trf_transaction_info, gen_args
                )
                amount_node = objectify.SubElement(trf_transaction_info, "Amt")
                amount_control_sum_a = payment._generate_amount_block(
                    amount_node, amount_control_sum_a
                )
                if not payment.partner_bank_id:
                    raise UserError(
                        self.env._(
                            "Bank account is missing on the payment {payment} "
                            "of partner '{partner}'."
                        ).format(
                            partner=payment.partner_id.display_name,
                            payment=payment.display_name,
                        )
                    )

                payment.partner_bank_id._generate_party_block(
                    trf_transaction_info,
                    "C",
                    gen_args,
                    payment,
                )
                payment._generate_purpose(trf_transaction_info)
                payment._generate_regulatory_reporting(trf_transaction_info, gen_args)
                payment._generate_remittance_info_block(trf_transaction_info, gen_args)
        group_header.NbOfTxs = str(transactions_count_a)
        group_header.CtrlSum = self._format_control_sum(amount_control_sum_a)
        return self._finalize_sepa_file_creation(xml_root, gen_args)
