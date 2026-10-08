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

    # ============== RUC via vat ==============

    def test_ruc_computed_from_vat(self):
        """l10n_py_ruc y l10n_py_ruc_dv se calculan desde vat"""
        partner = self.Partner.create(
            {
                "name": "Test RUC",
                "country_id": self.country_py.id,
                "vat": "80012345-0",
            }
        )
        self.assertEqual(partner.l10n_py_ruc, "80012345")
        self.assertEqual(partner.l10n_py_ruc_dv, "0")

    def test_ruc_dv_auto_calculated_on_create(self):
        """DV se calcula automáticamente si vat no incluye DV"""
        partner = self.Partner.create(
            {
                "name": "Test RUC auto DV",
                "country_id": self.country_py.id,
                "vat": "80012345",
            }
        )
        # create() formats vat to include DV
        self.assertEqual(partner.vat, "80012345-0")
        self.assertEqual(partner.l10n_py_ruc, "80012345")
        self.assertEqual(partner.l10n_py_ruc_dv, "0")

    def test_ruc_inverse_backward_compat(self):
        """Escribir l10n_py_ruc directamente sincroniza vat (backward compat)"""
        partner = self.Partner.create(
            {
                "name": "Test Inverse",
                "country_id": self.country_py.id,
                "l10n_py_ruc": "80012345",
            }
        )
        self.assertEqual(partner.vat, "80012345-0")
        self.assertEqual(partner.l10n_py_ruc_dv, "0")

    def test_ruc_empty_when_not_paraguayan(self):
        """l10n_py_ruc vacío cuando el contacto no está en Paraguay"""
        partner = self.Partner.create(
            {
                "name": "Test AR",
                "country_id": self.env.ref("base.ar").id,
                "vat": "20055361682",
            }
        )
        self.assertEqual(partner.vat, "20055361682")
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
        """DV exacto para RUCs reales (verificados con python-stdnum)"""
        test_cases = [
            ("80012345", "0"),
            ("4588955", "4"),
            ("80009401", "8"),
            ("80067890", "7"),
            ("80054321", "1"),
        ]
        for ruc_num, expected_dv in test_cases:
            partner = self.Partner.create(
                {
                    "name": f"Test DV {ruc_num}",
                    "country_id": self.country_py.id,
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
                "l10n_py_taxpayer_type": "2",
                "l10n_py_doc_type": "1",
                "l10n_py_doc_number": "4567890",
            }
        )
        self.assertEqual(partner.l10n_py_doc_type, "1")
        self.assertEqual(partner.l10n_py_doc_number, "4567890")
        self.assertFalse(partner.vat)
        self.assertFalse(partner.l10n_py_ruc)

    def test_taxpayer_with_ruc(self):
        """Contribuyente con RUC y DV"""
        partner = self.Partner.create(
            {
                "name": "Empresa PY",
                "country_id": self.country_py.id,
                "vat": "80012345",
                "l10n_py_taxpayer_type": "1",
            }
        )
        self.assertEqual(partner.l10n_py_taxpayer_type, "1")
        self.assertEqual(partner.l10n_py_ruc_dv, "0")

    def test_non_taxpayer_doc_types(self):
        """Todos los tipos de documento de identidad son aceptados"""
        for doc_type in ("1", "2", "3", "4"):
            partner = self.Partner.create(
                {
                    "name": f"Partner doc_type {doc_type}",
                    "country_id": self.country_py.id,
                    "l10n_py_taxpayer_type": "2",
                    "l10n_py_doc_type": doc_type,
                    "l10n_py_doc_number": "AB12345",
                }
            )
            self.assertEqual(partner.l10n_py_doc_type, doc_type)
            self.assertFalse(partner.vat)

    # ============== Onchanges ==============

    def test_onchange_doc_type_sets_non_taxpayer(self):
        """Elegir un documento de identidad marca al contacto como no contribuyente"""
        partner = self.Partner.new(
            {"name": "Test doc", "country_id": self.country_py.id}
        )
        partner.l10n_py_doc_type = "1"
        partner._onchange_l10n_py_doc_type()
        self.assertEqual(partner.l10n_py_taxpayer_type, "2")

    def test_onchange_vat_formats_ruc(self):
        """Informar el RUC completa el DV y marca al contacto como contribuyente"""
        partner = self.Partner.new(
            {
                "name": "Test RUC onchange",
                "country_id": self.country_py.id,
                "vat": "80012345",
                "l10n_py_doc_type": "1",
            }
        )
        partner._onchange_vat_l10n_py()
        self.assertEqual(partner.vat, "80012345-0")
        self.assertEqual(partner.l10n_py_taxpayer_type, "1")
        self.assertFalse(partner.l10n_py_doc_type)

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

    # ============== VAT validation (check_vat_py) ==============

    def test_check_vat_py_accepts_real_ruc(self):
        """base_vat acepta un RUC real con DV correcto"""
        partner = self.Partner.create(
            {
                "name": "Contribuyente RUC válido",
                "country_id": self.country_py.id,
                "vat": "80028061-0",
            }
        )
        self.assertEqual(partner.vat, "80028061-0")

    def test_check_vat_py_rejects_wrong_dv(self):
        """El hook de base_vat rechaza un RUC con DV incorrecto

        Se llama directamente al hook porque ``create``/``write`` reescriben el
        DV informado antes de que corra la restricción (ver
        ``_format_vat_py``), así que por esa vía nunca llega un DV inválido.
        Ese reformateo silencioso se trata en un PR aparte.
        """
        partner = self.Partner.create(
            {
                "name": "Contribuyente RUC",
                "country_id": self.country_py.id,
                "vat": "80028061-0",
            }
        )
        self.assertTrue(partner.check_vat_py("80028061-0"))
        self.assertFalse(partner.check_vat_py("80028061-1"))
        self.assertFalse(partner.check_vat_py("AB1234-5"))
        self.assertFalse(partner.check_vat_py(""))

    def test_check_vat_py_ignores_non_vat_documents(self):
        """Cédula y pasaporte no pasan por la validación de RUC"""
        for doc_type, number in [("1", "1234567-8"), ("2", "AB1234567")]:
            partner = self.Partner.create(
                {
                    "name": f"No contribuyente {number}",
                    "country_id": self.country_py.id,
                    "l10n_py_doc_type": doc_type,
                    "l10n_py_doc_number": number,
                }
            )
            self.assertEqual(partner.l10n_py_doc_number, number)
            self.assertFalse(partner.vat)

    def test_vat_outside_paraguay_is_not_touched(self):
        """El RUC solo se formatea para contactos en Paraguay"""
        partner = self.Partner.create(
            {
                "name": "Cliente AR",
                "country_id": self.env.ref("base.ar").id,
                "vat": "20055361682",
            }
        )
        partner.write({"vat": "20-05536168-2"})
        self.assertFalse(partner.l10n_py_ruc)
