# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import objectify

from odoo import _, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    def _generate_party_block(self, parent_node, block_level, gen_args, payment=None):
        """Generate the piece of the XML file corresponding to Name+IBAN+BIC
        This code is mutualized between TRF and DD
        In some localization (l10n_ch_sepa for example), they need the
        payment argument"""
        self.ensure_one()
        assert block_level in ("B", "C")
        if gen_args["payment_method"] == "TRF":
            party_type = block_level == "B" and "Dbtr" or "Cdtr"
        elif gen_args["payment_method"] == "DD":
            party_type = block_level == "B" and "Cdtr" or "Dbtr"
        party_type2label = {
            "Dbtr": _("Debtor Name"),
            "Cdtr": _("Creditor Name"),
        }
        partner = self.partner_id
        partner_name = self.acc_holder_name or partner.name
        party_name = self.env["account.payment.order"]._prepare_field(
            party_type2label[party_type],
            partner_name,
            gen_args["name_maxsize"],
            gen_args,
        )
        # At C block level, the order is : BIC, Name, IBAN
        # At B block level, the order is : Name, IBAN, BIC
        if block_level == "C":
            self._generate_party_agent(
                parent_node,
                party_type,
                block_level,
                gen_args,
                payment=payment,
            )
        party = objectify.SubElement(parent_node, party_type)
        party.Nm = party_name

        partner._generate_address_block(party, gen_args)

        partner._generate_party_id(party, party_type)

        self._generate_party_acc_number(
            parent_node, party_type, block_level, gen_args, payment=payment
        )

        if block_level == "B":
            self._generate_party_agent(
                parent_node,
                party_type,
                block_level,
                gen_args,
                payment=payment,
            )

    def _generate_party_agent(
        self, parent_node, party_type, block_level, gen_args, payment=None
    ):
        """Generate the piece of the XML file corresponding to BIC
        This code is mutualized between TRF and DD
        Starting from Feb 1st 2016, we should be able to do
        cross-border SEPA transfers without BIC, cf
        http://www.europeanpaymentscouncil.eu/index.cfm/
        sepa-credit-transfer/iban-and-bic/
        In some localization (l10n_ch_sepa for example), they need the
        payment argument"""
        self.ensure_one()
        assert block_level in ("B", "C")
        if self.bank_bic:
            party_agent = objectify.SubElement(parent_node, f"{party_type}Agt")
            party_agent_institution = objectify.SubElement(party_agent, "FinInstnId")
            setattr(
                party_agent_institution,
                gen_args["bic_xml_tag"],
                self.bank_bic,
            )
        else:
            if block_level == "B" or (
                block_level == "C" and gen_args["payment_method"] == "DD"
            ):
                party_agent = objectify.SubElement(parent_node, f"{party_type}Agt")
                party_agent_institution = objectify.SubElement(
                    party_agent, "FinInstnId"
                )
                party_agent_other = objectify.SubElement(
                    party_agent_institution, "Othr"
                )
                party_agent_other.Id = "NOTPROVIDED"
            # for Credit Transfers, in the 'C' block, if BIC is not provided,
            # we should not put the 'Creditor Agent' block at all,
            # as per the guidelines of the EPC

    def _generate_party_acc_number(
        self, parent_node, party_type, block_level, gen_args, payment=None
    ):
        party_account = objectify.SubElement(parent_node, f"{party_type}Acct")
        party_account_id = objectify.SubElement(party_account, "Id")
        if self.acc_type == "iban":
            party_account_id.IBAN = self.sanitized_acc_number
        else:
            party_account_other = objectify.SubElement(party_account_id, "Othr")
            party_account_other.Id = self.sanitized_acc_number
        if party_type == "Dbtr" and self.currency_id:
            party_account.Ccy = self.currency_id.name
