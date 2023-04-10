import os
import uuid

from lxml import etree, objectify

from odoo import _, models
from odoo.exceptions import ValidationError


class CroatiaXMLMixin(models.AbstractModel):
    _name = "l10n.hr.xml.mixin"
    _description = "Abstract class for handling XML in Croatia"
    """
    Abstract model containing common xml methods for all sorts of XML reports
    so, no need to import etree, objectify and such modules everywhere
    """

    def check_valid_phone(self, phone):
        """Za PDV obrazac:
        Broj telefona, počinje sa znakom + nakon kojeg slijedi 8-13 brojeva, npr +38514445555
        """
        if not phone:
            return False
        for r in [" ", "/", ".", ",", "(", ")"]:
            phone = phone.replace(r, "")
        if phone.startswith("00"):
            phone = "+" + phone[2:]
        if not phone.startswith("+") and phone.startswith("385"):
            phone = "+" + phone
        if 14 < len(phone) < 7 or not phone.startswith("+385"):
            raise ValidationError(_("Phone %s not valid!") % phone)
        return phone

    def get_company_data(self, report_type):
        company = self.company_id
        err = ""
        if not company.partner_id.city:
            err += "Nedostaje upisan grad\n"
        if not company.partner_id.street:
            err += "Nedostaje adresni podatak : Ulica\n"
        if not company.partner_id.company_registry:  # vidi u l10n_hr !
            err += "Nedostaje porezni broj  (OIB)\n"
        if err != "":
            raise ValidationError(err)

    def get_xml_metadata(self, xml_naslov, xml_autor, xml_conforms):
        """
        Used n : JOPPD, ...
        :return: XML common metadata object for all xml-s defined by Institutions
        """
        MD = self._get_elementmaker(
            namespace="http://e-porezna.porezna-uprava.hr/sheme/Metapodaci/v2-0"
        )
        identifikator = uuid.uuid4()
        date_time = self.company_id.get_l10n_hr_time_formatted()["datum_meta"]
        meta = MD.Metapodaci(
            MD.Naslov(xml_naslov, dc="http://purl.org/dc/elements/1.1/title"),
            MD.Autor(xml_autor, dc="http://purl.org/dc/elements/1.1/creator"),
            MD.Datum(date_time, dc="http://purl.org/dc/elements/1.1/date"),
            MD.Format("text/xml", dc="http://purl.org/dc/elements/1.1/format"),
            MD.Jezik("hr-HR", dc="http://purl.org/dc/elements/1.1/language"),
            MD.Identifikator(
                identifikator, dc="http://purl.org/dc/elements/1.1/identifier"
            ),
            MD.Uskladjenost(xml_conforms, dc="http://purl.org/dc/terms/conformsTo"),
            MD.Tip("Elektronički obrazac", dc="http://purl.org/dc/elements/1.1/type"),
            MD.Adresant("Ministarstvo Financija, Porezna uprava, Zagreb"),
        )
        return meta, identifikator

    def _get_elementmaker(self, annotate=False, namespace=False):
        """
        :param annotate:
        :param namespace:
        :return: simply deanotate xml object
        """
        return objectify.ElementMaker(annotate=annotate, namespace=namespace)

    def get_xml_string(
        self,
        xml_object,
        deannotate=False,
        pretty=False,
        encoding="unicode",
        replace=False,
    ):
        """
        :param xml_object: etree xml object
        :param deannotate: True to remove annotations
        :param pretty: pretty_print
        :param encoding:
        :param replace: list of tuples to replace in xlm string
        :return: xml string
        """
        if deannotate:
            objectify.deannotate(xml_object)
        string = etree.tostring(xml_object, pretty_print=pretty, encoding=encoding)
        if replace:
            for r1, r2 in replace:
                string = string.replace(r1, r2)
        return string

    def validate_xml(self, xml_string, xsd_path, xsd_file):
        """
        :param xml_string:
        :param xsd_path: absolute path to schema folder (put schema folders in module)
        :param xsd_file: xsd file name for vaidating
        :return: False , or Error description if error occurs
        """
        os.chdir(xsd_path)
        xml_schema = etree.XMLSchema(etree.parse(os.path.join(xsd_path, xsd_file)))
        try:
            xml_schema.validate(etree.XML(xml_string))
        except AssertionError as E:
            return E[0]
        except Exception as E:
            return E
        return False
