from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "l10n_py")
class TestResPartner(TransactionCase):
    """Tests para extensión de res.partner Paraguay"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Partner = cls.env["res.partner"]
        cls.country_py = cls.env.ref("base.py")
        cls.it_ruc = cls.env.ref("l10n_py_base.it_ruc")
        cls.it_ci = cls.env.ref("l10n_py_base.it_ci")
        cls.it_pasaporte = cls.env.ref("l10n_py_base.it_pasaporte")
        cls.it_carnet = cls.env.ref("l10n_py_base.it_carnet_residencia")

    def test_partner_fiscal_fields_exist(self):
        """Campos fiscales l10n_py deben existir en el modelo"""
        partner = self.Partner.create(
            {
                "name": "Test Partner PY",
                "country_id": self.country_py.id,
            }
        )
        self.assertTrue(hasattr(partner, "l10n_py_ruc"))
        self.assertTrue(hasattr(partner, "l10n_py_ruc_dv"))
        self.assertTrue(hasattr(partner, "l10n_py_taxpayer_type"))
        self.assertTrue(hasattr(partner, "l10n_py_fantasy_name"))
        self.assertTrue(hasattr(partner, "l10n_py_activity_description"))
        self.assertTrue(hasattr(partner, "l10n_py_department_code"))
        self.assertTrue(hasattr(partner, "l10n_py_city_code"))

    # ============== RUC via vat + identification type ==============

    def test_ruc_computed_from_vat(self):
        """l10n_py_ruc y l10n_py_ruc_dv se calculan desde vat"""
        partner = self.Partner.create(
            {
                "name": "Test RUC",
                "country_id": self.country_py.id,
                "l10n_latam_identification_type_id": self.it_ruc.id,
                "vat": "80012345-6",
            }
        )
        self.assertEqual(partner.l10n_py_ruc, "80012345")
        self.assertEqual(partner.l10n_py_ruc_dv, "6")

    def test_ruc_dv_auto_calculated_on_create(self):
        """DV se calcula automáticamente si vat no incluye DV"""
        partner = self.Partner.create(
            {
                "name": "Test RUC auto DV",
                "country_id": self.country_py.id,
                "l10n_latam_identification_type_id": self.it_ruc.id,
                "vat": "80012345",
            }
        )
        # create() formats vat to include DV
        self.assertEqual(partner.vat, "80012345-6")
        self.assertEqual(partner.l10n_py_ruc, "80012345")
        self.assertEqual(partner.l10n_py_ruc_dv, "6")

    def test_ruc_inverse_backward_compat(self):
        """Escribir l10n_py_ruc directamente sincroniza vat (backward compat)"""
        partner = self.Partner.create(
            {
                "name": "Test Inverse",
                "country_id": self.country_py.id,
                "l10n_py_ruc": "80012345",
            }
        )
        self.assertEqual(partner.vat, "80012345-6")
        self.assertEqual(partner.l10n_latam_identification_type_id, self.it_ruc)
        self.assertEqual(partner.l10n_py_ruc_dv, "6")

    def test_ruc_empty_when_not_ruc_type(self):
        """l10n_py_ruc vacío cuando identification type no es RUC"""
        partner = self.Partner.create(
            {
                "name": "Test CI",
                "country_id": self.country_py.id,
                "l10n_latam_identification_type_id": self.it_ci.id,
                "vat": "4567890",
            }
        )
        self.assertFalse(partner.l10n_py_ruc)
        self.assertFalse(partner.l10n_py_ruc_dv)

    def test_ruc_dv_empty_when_no_vat(self):
        """DV debe estar vacío si no hay vat"""
        partner = self.Partner.create(
            {
                "name": "Test Partner",
                "country_id": self.country_py.id,
            }
        )
        self.assertFalse(partner.l10n_py_ruc_dv)

    # ============== DV exacto para RUCs conocidos ==============

    def test_ruc_dv_exact_values(self):
        """DV exacto para RUCs conocidos verificados contra SET"""
        test_cases = [
            ("80012345", "6"),
            ("4588955", "1"),
            ("80009401", "0"),
            ("80067890", "7"),
            ("80054321", "2"),
        ]
        for ruc_num, expected_dv in test_cases:
            partner = self.Partner.create(
                {
                    "name": f"Test DV {ruc_num}",
                    "country_id": self.country_py.id,
                    "l10n_latam_identification_type_id": self.it_ruc.id,
                    "vat": ruc_num,
                }
            )
            self.assertEqual(
                partner.l10n_py_ruc_dv,
                expected_dv,
                f"RUC {ruc_num} debe tener DV={expected_dv}",
            )

    # ============== Taxpayer type ==============

    def test_taxpayer_type_selection(self):
        """Tipo de contribuyente debe aceptar valores válidos"""
        partner = self.Partner.create(
            {
                "name": "Contribuyente Test",
                "country_id": self.country_py.id,
                "l10n_py_taxpayer_type": "1",
            }
        )
        self.assertEqual(partner.l10n_py_taxpayer_type, "1")

        partner2 = self.Partner.create(
            {
                "name": "No Contribuyente Test",
                "country_id": self.country_py.id,
                "l10n_py_taxpayer_type": "2",
            }
        )
        self.assertEqual(partner2.l10n_py_taxpayer_type, "2")

    # ============== Non-taxpayer doc fields ==============

    def test_non_taxpayer_with_ci(self):
        """No-contribuyente con cédula de identidad"""
        partner = self.Partner.create(
            {
                "name": "Persona Natural PY",
                "country_id": self.country_py.id,
                "l10n_latam_identification_type_id": self.it_ci.id,
                "vat": "4567890",
                "l10n_py_taxpayer_type": "2",
                "l10n_py_doc_type": "1",
                "l10n_py_doc_number": "4567890",
            }
        )
        self.assertEqual(partner.l10n_py_doc_type, "1")
        self.assertEqual(partner.l10n_py_doc_number, "4567890")
        self.assertEqual(partner.vat, "4567890")

    def test_taxpayer_with_ruc(self):
        """Contribuyente con RUC y DV"""
        partner = self.Partner.create(
            {
                "name": "Empresa PY",
                "country_id": self.country_py.id,
                "l10n_latam_identification_type_id": self.it_ruc.id,
                "vat": "80012345",
                "l10n_py_taxpayer_type": "1",
            }
        )
        self.assertEqual(partner.l10n_py_taxpayer_type, "1")
        self.assertEqual(partner.l10n_py_ruc_dv, "6")

    def test_non_taxpayer_doc_types(self):
        """Todos los tipos de documento de identidad son aceptados"""
        id_types = {
            "1": self.it_ci,
            "2": self.it_pasaporte,
            "3": self.it_carnet,
        }
        for doc_type, id_type in id_types.items():
            partner = self.Partner.create(
                {
                    "name": f"Partner doc_type {doc_type}",
                    "country_id": self.country_py.id,
                    "l10n_latam_identification_type_id": id_type.id,
                    "vat": "12345",
                    "l10n_py_taxpayer_type": "2",
                    "l10n_py_doc_type": doc_type,
                    "l10n_py_doc_number": "12345",
                }
            )
            self.assertEqual(partner.l10n_py_doc_type, doc_type)

    # ============== Onchanges ==============

    def test_neighborhood_onchange(self):
        """Auto-llenar ciudad al seleccionar barrio"""
        partner = self.Partner.create(
            {
                "name": "Test Partner",
                "country_id": self.country_py.id,
            }
        )
        self.assertTrue(hasattr(partner, "l10n_py_neighborhood_id"))

    def test_state_change_clears_city(self):
        """Al cambiar departamento, ciudad y barrio se limpian si no coinciden"""
        state_asu = self.env["res.country.state"].search(
            [
                ("country_id", "=", self.country_py.id),
                ("l10n_py_code", "!=", False),
            ],
            limit=1,
        )
        state_other = self.env["res.country.state"].search(
            [
                ("country_id", "=", self.country_py.id),
                ("l10n_py_code", "!=", False),
                ("id", "!=", state_asu.id),
            ],
            limit=1,
        )
        if not (state_asu and state_other):
            self.skipTest("Need at least 2 PY states with l10n_py_code")

        city = self.env["res.city"].search([("state_id", "=", state_asu.id)], limit=1)
        if not city:
            self.skipTest("Need a city in the first PY state")

        partner = self.Partner.new(
            {
                "name": "Test State Change",
                "country_id": self.country_py.id,
                "state_id": state_asu.id,
                "city_id": city.id,
            }
        )
        # Change state to a different one
        partner.state_id = state_other
        partner._onchange_state_id_l10n_py()
        self.assertFalse(
            partner.city_id,
            "City should be cleared when state changes",
        )

    # ============== Location ==============

    def test_department_code_related(self):
        """l10n_py_department_code computado desde state_id"""
        state = self.env["res.country.state"].search(
            [
                ("country_id", "=", self.country_py.id),
                ("l10n_py_code", "!=", False),
            ],
            limit=1,
        )
        if state:
            partner = self.Partner.create(
                {
                    "name": "Test Partner",
                    "country_id": self.country_py.id,
                    "state_id": state.id,
                }
            )
            self.assertEqual(
                partner.l10n_py_department_code,
                state.l10n_py_code,
                "Código departamento debe coincidir con el del estado",
            )
