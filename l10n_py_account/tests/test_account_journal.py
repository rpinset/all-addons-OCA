from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "l10n_py")
class TestAccountJournal(TransactionCase):
    """Tests para account.journal (extensión paraguaya)"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Journal = cls.env["account.journal"]
        cls.company = cls.env.ref("base.main_company")

    def test_establishment_validation(self):
        """Validación formato 3 dígitos"""
        journal = self.Journal.create(
            {
                "name": "Test Journal",
                "type": "sale",
                "code": "TJ1",
                "company_id": self.company.id,
                "l10n_py_establishment": "001",
                "l10n_py_point": "001",
            }
        )
        self.assertEqual(journal.l10n_py_establishment, "001")

        with self.assertRaises(ValidationError):
            self.Journal.create(
                {
                    "name": "Test Journal Bad",
                    "type": "sale",
                    "code": "TJ2",
                    "company_id": self.company.id,
                    "l10n_py_establishment": "01",
                    "l10n_py_point": "001",
                }
            )

    def test_point_validation(self):
        """Validación formato 3 dígitos"""
        with self.assertRaises(ValidationError):
            self.Journal.create(
                {
                    "name": "Test Journal Bad",
                    "type": "sale",
                    "code": "TJ3",
                    "company_id": self.company.id,
                    "l10n_py_establishment": "001",
                    "l10n_py_point": "1",
                }
            )
