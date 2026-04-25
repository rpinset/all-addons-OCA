# Copyright 2013-2016 Akretion - Alexis de Lattre <alexis.delattre@akretion.com>
# Copyright 2016 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2021 Tecnativa - Carlos Roca
# Copyright 2014-2022 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
import re

from lxml import etree, objectify

from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError

try:
    from unidecode import unidecode
except ImportError:
    unidecode = None

logger = logging.getLogger(__name__)


class AccountPaymentOrder(models.Model):
    _inherit = "account.payment.order"

    sepa = fields.Boolean(compute="_compute_sepa", string="SEPA Payment")
    show_warning_not_sepa = fields.Boolean(compute="_compute_sepa")
    charge_bearer = fields.Selection(
        [
            ("SLEV", "Following Service Level"),
            ("SHAR", "Shared"),
            ("CRED", "Borne by Creditor"),
            ("DEBT", "Borne by Debtor"),
        ],
        default="SLEV",
        tracking=True,
        help="Following service level : transaction charges are to be "
        "applied following the rules agreed in the service level "
        "and/or scheme (SEPA Core messages must use this). Shared : "
        "transaction charges on the debtor side are to be borne by "
        "the debtor, transaction charges on the creditor side are to "
        "be borne by the creditor. Borne by creditor : all "
        "transaction charges are to be borne by the creditor. Borne "
        "by debtor : all transaction charges are to be borne by the "
        "debtor.",
    )
    batch_booking = fields.Boolean(
        compute="_compute_batch_booking",
        readonly=False,
        store=True,
        precompute=True,
        tracking=True,
        help="If true, the bank statement will display only one debit "
        "line for all the wire transfers of the SEPA XML file ; if "
        "false, the bank statement will display one debit line per wire "
        "transfer of the SEPA XML file.",
    )

    @api.model
    def _sepa_iban_prefix_list(self):
        # List of IBAN prefixes (not country codes !)
        # Source: https://www.europeanpaymentscouncil.eu/sites/default/
        # files/kb/file/2023-01/
        # EPC409-09%20EPC%20List%20of%20SEPA%20Scheme%20Countries%20v4.0_0.pdf
        # Some countries use IBAN but are not part of the SEPA zone
        # example: Turkey, Madagascar, Tunisia, etc.
        return [
            "AD",
            "AT",
            "BE",
            "BG",
            "ES",
            "HR",
            "CY",
            "CZ",
            "DK",
            "EE",
            "FI",
            "FR",
            "DE",
            "GI",
            "GR",
            "GB",
            "HU",
            "IS",
            "IE",
            "IT",
            "LV",
            "LI",
            "LT",
            "LU",
            "PT",
            "MT",
            "MC",
            "NL",
            "NO",
            "PL",
            "RO",
            "SM",
            "SK",
            "SI",
            "SE",
            "CH",
            "VA",
        ]

    @api.depends(
        "payment_method_line_id",
        "company_partner_bank_id.acc_type",
        "company_partner_bank_id.sanitized_acc_number",
        "payment_line_ids.currency_id",
        "payment_line_ids.partner_bank_id.acc_type",
        "payment_line_ids.partner_bank_id.sanitized_acc_number",
    )
    def _compute_sepa(self):
        eur = self.env.ref("base.EUR")
        sepa_list = self._sepa_iban_prefix_list()
        for order in self:
            sepa = False
            warn_not_sepa = False
            payment_method = order.payment_method_line_id.payment_method_id
            if payment_method.pain_version:
                sepa = True
                if (
                    order.company_partner_bank_id
                    and order.company_partner_bank_id.acc_type != "iban"
                ):
                    sepa = False
                if (
                    order.company_partner_bank_id
                    and order.company_partner_bank_id.sanitized_acc_number[:2]
                    not in sepa_list
                ):
                    sepa = False
                for pline in order.payment_line_ids:
                    if pline.currency_id != eur:
                        sepa = False
                        break
                    if (
                        pline.partner_bank_id
                        and pline.partner_bank_id.acc_type != "iban"
                    ):
                        sepa = False
                        break
                    if (
                        pline.partner_bank_id
                        and pline.partner_bank_id.sanitized_acc_number[:2]
                        not in sepa_list
                    ):
                        sepa = False
                        break
                    sepa = pline._compute_sepa_final_hook(sepa)
                    if not sepa:
                        break
                if not sepa and payment_method.warn_not_sepa:
                    warn_not_sepa = True
            order.sepa = sepa
            order.show_warning_not_sepa = warn_not_sepa

    @api.depends("payment_method_line_id")
    def _compute_batch_booking(self):
        for order in self:
            batch_booking = False
            if order.payment_method_line_id:
                batch_booking = order.payment_method_line_id.default_batch_booking
            order.batch_booking = batch_booking

    @api.model
    def _prepare_field(
        self, field_name, value, max_size, gen_args, raise_if_oversized=False
    ):
        if gen_args is None:
            gen_args = {}
        if not value:
            raise UserError(
                _(
                    "Error in the generation of the XML payment file: "
                    "'%s' is empty. It should have a non-null value."
                )
                % field_name
            )
        if not isinstance(value, str):
            raise UserError(
                _(
                    "Error in the generation of the XML payment file: "
                    "'%(field)s' should be a string, "
                    "but it is %(value_type)s (value: %(value)s).",
                    field=field_name,
                    value_type=type(value),
                    value=value,
                )
            )

        # SEPA uses XML ; XML = UTF-8 ; UTF-8 = support for all characters
        # But we are dealing with banks... with old software that don't support UTF-8 !
        # cf section 1.4 "Character set" of the SEPA Credit Transfer
        # Scheme Customer-to-bank guidelines
        # Allowed caracters are: a-z A-Z 0-9 / - ? : ( ) . , ' + space
        if gen_args["convert_to_ascii"]:
            value = unidecode(value)
            value = re.sub(r"[^a-zA-Z0-9/\-\?:\(\)\.,\'\+\s]", "-", value)

        if max_size and len(value) > max_size:
            if raise_if_oversized:
                raise UserError(
                    _(
                        "Error in the generation of the XML payment file: "
                        "'%(field_name)s' with value '%(value)s' has %(count)s "
                        "caracters, but the maximum is %(max_size)s caracters.",
                        field_name=field_name,
                        value=value,
                        count=len(value),
                        max_size=max_size,
                    )
                )
            else:
                value = value[:max_size]
        return value

    @api.model
    def _validate_xml(self, xml_bytes, gen_args):
        xsd_etree_obj = etree.parse(tools.file_open(gen_args["pain_xsd_file"]))
        official_pain_schema = etree.XMLSchema(xsd_etree_obj)

        try:
            root_to_validate = etree.fromstring(xml_bytes)
            official_pain_schema.assertValid(root_to_validate)
        except Exception as e:
            logger.warning("The XML file is invalid against the XML Schema Definition")
            logger.warning(xml_bytes.decode("utf-8"))
            logger.warning(e)
            raise UserError(
                _(
                    "The generated XML file is not valid against the official "
                    "XML Schema Definition. The generated XML file and the "
                    "full error have been written in the server logs. Here "
                    "is the error, which may give you an idea on the cause "
                    "of the problem : %s"
                )
                % str(e)
            ) from None

    def _finalize_sepa_file_creation(self, xml_root, gen_args):
        objectify.deannotate(xml_root)
        xml_bytes = etree.tostring(
            xml_root, pretty_print=True, encoding="UTF-8", xml_declaration=True
        )
        # I didn't find a way to remove py:pytype and xmlns:py while keeping
        # xmlns:xsi and xmlns
        # If I use objectify.deannotate(xml_root, cleanup_namespaces=True),
        # it will remove all the unused namespaces,
        # so it also removes xmlns:xsi and xmlns.
        # The only solution I found is to manually remove xmlns:py in the output string
        xml_string = xml_bytes.decode("utf-8")
        xml_string = xml_string.replace(
            ''' xmlns:py="http://codespeak.net/lxml/objectify/pytype"''', ""
        )
        xml_bytes = xml_string.encode("utf-8")
        logger.debug(
            "Generated SEPA XML file in format %s below", gen_args["pain_flavor"]
        )
        logger.debug(xml_string)
        self._validate_xml(xml_bytes, gen_args)
        return (xml_bytes, "xml")

    def _generate_pain_nsmap(self):
        self.ensure_one()
        pain_flavor = self.payment_method_id.pain_version
        nsmap = {
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            None: f"urn:iso:std:iso:20022:tech:xsd:{pain_flavor}",
        }
        return nsmap

    def _generate_pain_attrib(self):
        self.ensure_one()
        return {}

    def _generate_group_header_block(self, parent_node, gen_args):
        group_header = objectify.SubElement(parent_node, "GrpHdr")
        group_header.MsgId = self._prepare_field(
            "Message Identification", self.name, 35, gen_args, raise_if_oversized=True
        )
        group_header.CreDtTm = fields.Datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        # Initialize value value ; will be updated in another method
        group_header.NbOfTxs = 0
        group_header.CtrlSum = 0.00
        self._generate_initiating_party_block(group_header, gen_args)
        return group_header

    @api.model
    def _must_have_initiating_party(self, gen_args):
        """This method is designed to be inherited in localization modules for
        countries in which the initiating party is required"""
        return False

    def _generate_initiating_party_block(self, parent_node, gen_args):
        my_company_name = self._prepare_field(
            "Company Name",
            self.company_partner_bank_id.partner_id.name,
            gen_args["name_maxsize"],
            gen_args,
        )
        initiating_party = objectify.SubElement(parent_node, "InitgPty")
        initiating_party.Nm = my_company_name
        initiating_party_identifier = (
            self.payment_method_line_id.initiating_party_identifier
            or self.company_id.initiating_party_identifier
        )
        initiating_party_issuer = (
            self.payment_method_line_id.initiating_party_issuer
            or self.company_id.initiating_party_issuer
        )
        initiating_party_scheme = (
            self.payment_method_line_id.initiating_party_scheme
            or self.company_id.initiating_party_scheme
        )
        # in pain.008.001.02.ch.01.xsd files they use
        # initiating_party_identifier but not initiating_party_issuer
        if initiating_party_identifier:
            iniparty_id = objectify.SubElement(initiating_party, "Id")
            iniparty_org_id = objectify.SubElement(iniparty_id, "OrgId")
            iniparty_org_other = objectify.SubElement(iniparty_org_id, "Othr")
            iniparty_org_other.Id = initiating_party_identifier
            if initiating_party_scheme:
                iniparty_org_other_scheme = objectify.SubElement(
                    iniparty_org_other, "SchmeNm"
                )
                iniparty_org_other_scheme.Prtry = initiating_party_scheme
            if initiating_party_issuer:
                iniparty_org_other.Issr = initiating_party_issuer
        elif self._must_have_initiating_party(gen_args):
            raise UserError(
                _(
                    "Missing 'Initiating Party Issuer' and/or "
                    "'Initiating Party Identifier' for the company '%s'. "
                    "Both fields must have a value."
                )
                % self.company_id.name
            )

    def _generate_charge_bearer(self, parent_node):
        self.ensure_one()
        if self.sepa:
            parent_node.ChrgBr = "SLEV"
        else:
            parent_node.ChrgBr = self.charge_bearer

    def _format_control_sum(self, control_sum):
        self.ensure_one()
        decimal_places = max(
            [line.currency_id.decimal_places for line in self.payment_line_ids]
        )
        fmt = f"%.{decimal_places}f"
        control_sum_str = fmt % control_sum
        return control_sum_str

    def _convert_to_ascii_non_sepa_files(self):
        """This method is designed to be inherited"""
        return True

    def _convert_to_ascii(self):
        self.ensure_one()
        if self.sepa:
            convert_to_ascii = True
        else:
            convert_to_ascii = self._convert_to_ascii_non_sepa_files()
        return convert_to_ascii
