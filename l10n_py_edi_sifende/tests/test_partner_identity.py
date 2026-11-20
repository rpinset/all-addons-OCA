# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from lxml import etree

from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestPartnerIdentity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country = cls.env.ref("base.py")
        cls.ci_type = cls.env.ref("l10n_py_base.it_ci")

    def partner_form(self, name):
        form = Form(self.env["res.partner"])
        form.name = name
        form.country_id = self.country
        return form

    def test_el_cliente_con_cedula_guarda_el_documento_desde_la_pantalla(self):
        form = self.partner_form("Ana González")
        form.l10n_latam_identification_type_id = self.ci_type
        form.vat = "1234567"
        partner = form.save()
        self.assertEqual(partner.l10n_py_taxpayer_type, "2")
        self.assertEqual(partner.l10n_py_doc_type, "1")
        self.assertEqual(partner.l10n_py_doc_number, "1234567")

    def test_el_innominado_se_puede_elegir_desde_la_pantalla(self):
        form = self.partner_form("Sin Nombre")
        form.l10n_py_taxpayer_type = "2"
        form.l10n_py_doc_type = "4"
        form.l10n_py_doc_number = "0"
        partner = form.save()
        self.assertEqual(partner.l10n_py_doc_type, "4")
        self.assertEqual(partner.l10n_py_doc_number, "0")

    def test_los_campos_propios_del_contacto_van_en_un_grupo_para_mostrar_su_etiqueta(
        self,
    ):
        arch = self.env["res.partner"].get_view(
            self.env.ref("base.view_partner_form").id
        )["arch"]
        tree = etree.fromstring(arch)
        for name in (
            "l10n_py_taxpayer_type",
            "l10n_py_activity_description",
            "l10n_py_doc_type",
            "l10n_py_doc_number",
            "l10n_py_sifende_city_id",
        ):
            node = tree.xpath(f"//field[@name='{name}']")[0]
            self.assertEqual(node.getparent().tag, "group", name)
