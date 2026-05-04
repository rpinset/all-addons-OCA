from datetime import date

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "l10n_py")
class TestAssociatedDocument(TransactionCase):
    """Tests para l10n_py.associated.document (Grupo H SIFEN)"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.AssociatedDoc = cls.env["l10n_py.associated.document"]
        cls.company = cls.env.ref("base.main_company")
        cls.country_py = cls.env.ref("base.py")

        # Crear move mínimo para asociar documentos
        cls.partner = cls.env["res.partner"].create(
            {"name": "Test Partner PY", "country_id": cls.country_py.id}
        )

        cls.journal = cls.env["account.journal"].create(
            {
                "name": "Ventas AD Test",
                "type": "sale",
                "code": "VAD",
                "company_id": cls.company.id,
                "l10n_latam_use_documents": True,
            }
        )

        cls.move = cls.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": cls.partner.id,
                "journal_id": cls.journal.id,
            }
        )

        cls.valid_cdc = "01800094011001001000000712024011010974900" + "001"
        # Ensure 44 digits
        cls.valid_cdc = cls.valid_cdc.ljust(44, "0")[:44]

    # ============== F08: Electrónico ==============

    def test_electronic_requires_cdc(self):
        """F08: Documento electrónico sin CDC → error"""
        with self.assertRaises(ValidationError):
            self.AssociatedDoc.create(
                {
                    "move_id": self.move.id,
                    "association_type": "1",
                }
            )

    def test_electronic_with_valid_cdc(self):
        """F08: Documento electrónico con CDC válido → OK"""
        doc = self.AssociatedDoc.create(
            {
                "move_id": self.move.id,
                "association_type": "1",
                "cdc": self.valid_cdc,
            }
        )
        self.assertTrue(doc.id)

    def test_electronic_no_printed_fields(self):
        """F08: Documento electrónico no puede tener campos impresos"""
        with self.assertRaises(ValidationError):
            self.AssociatedDoc.create(
                {
                    "move_id": self.move.id,
                    "association_type": "1",
                    "cdc": self.valid_cdc,
                    "timbrado": "12345678",
                }
            )

    def test_cdc_format_validation(self):
        """F08: CDC con formato inválido → error"""
        with self.assertRaises(ValidationError):
            self.AssociatedDoc.create(
                {
                    "move_id": self.move.id,
                    "association_type": "1",
                    "cdc": "123",  # muy corto
                }
            )

        with self.assertRaises(ValidationError):
            self.AssociatedDoc.create(
                {
                    "move_id": self.move.id,
                    "association_type": "1",
                    "cdc": "A" * 44,  # letras
                }
            )

    # ============== F08: Impreso ==============

    def test_printed_requires_all_fields(self):
        """F08: Documento impreso sin campos obligatorios → error"""
        # Sin timbrado
        with self.assertRaises(ValidationError):
            self.AssociatedDoc.create(
                {
                    "move_id": self.move.id,
                    "association_type": "2",
                    "establishment": "001",
                    "expedition_point": "001",
                    "doc_number": "0000001",
                    "doc_type_code": "1",
                    "doc_date": date.today(),
                    # falta timbrado
                }
            )

    def test_printed_complete(self):
        """F08: Documento impreso con todos los campos → OK"""
        doc = self.AssociatedDoc.create(
            {
                "move_id": self.move.id,
                "association_type": "2",
                "timbrado": "12345678",
                "establishment": "001",
                "expedition_point": "001",
                "doc_number": "0000001",
                "doc_type_code": "1",
                "doc_date": date.today(),
            }
        )
        self.assertTrue(doc.id)

    def test_printed_no_cdc(self):
        """F08: Documento impreso no puede tener CDC"""
        with self.assertRaises(ValidationError):
            self.AssociatedDoc.create(
                {
                    "move_id": self.move.id,
                    "association_type": "2",
                    "timbrado": "12345678",
                    "establishment": "001",
                    "expedition_point": "001",
                    "doc_number": "0000001",
                    "doc_type_code": "1",
                    "doc_date": date.today(),
                    "cdc": self.valid_cdc,
                }
            )

    # ============== F08: Constancia ==============

    def test_constancia_complete(self):
        """F08: Constancia electrónica con tipo y número → OK"""
        doc = self.AssociatedDoc.create(
            {
                "move_id": self.move.id,
                "association_type": "3",
                "constancia_type": "1",
                "constancia_number": "CONST-2024-001",
            }
        )
        self.assertTrue(doc.id)

    def test_constancia_no_cdc_no_printed(self):
        """F08: Constancia no puede tener CDC ni campos impresos"""
        with self.assertRaises(ValidationError):
            self.AssociatedDoc.create(
                {
                    "move_id": self.move.id,
                    "association_type": "3",
                    "constancia_type": "1",
                    "constancia_number": "CONST-001",
                    "cdc": self.valid_cdc,
                }
            )

        with self.assertRaises(ValidationError):
            self.AssociatedDoc.create(
                {
                    "move_id": self.move.id,
                    "association_type": "3",
                    "constancia_type": "1",
                    "constancia_number": "CONST-001",
                    "timbrado": "12345678",
                }
            )

    def test_constancia_requires_type_and_number(self):
        """F08: Constancia sin tipo o número → error"""
        with self.assertRaises(ValidationError):
            self.AssociatedDoc.create(
                {
                    "move_id": self.move.id,
                    "association_type": "3",
                    # falta tipo y número
                }
            )

        with self.assertRaises(ValidationError):
            self.AssociatedDoc.create(
                {
                    "move_id": self.move.id,
                    "association_type": "3",
                    "constancia_type": "1",
                    # falta número
                }
            )
