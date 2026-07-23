# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from unittest.mock import patch

from psycopg2 import IntegrityError

from odoo.tests.common import TransactionCase, tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestSIFENConnector(TransactionCase):
    """Test SIFEN connector model."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.ref("base.main_company")
        cls.company.write(
            {
                "l10n_py_ruc": "80012345",
            }
        )
        # Remove any existing connector from demo data
        cls.env["l10n_py.edi.connector"].sudo().search(
            [("company_id", "=", cls.company.id)]
        ).unlink()

    def test_create_sifen_connector(self):
        """Test creating a SIFEN connector."""
        connector = self.env["l10n_py.edi.connector"].create(
            {
                "name": "SIFEN Test",
                "company_id": self.company.id,
                "provider_type": "sifen",
                "environment": "test",
            }
        )
        self.assertEqual(connector.provider_type, "sifen")
        self.assertEqual(connector.environment, "test")

    @mute_logger("odoo.sql_db")
    def test_company_unique_constraint(self):
        """Test that only one connector per company is allowed."""
        # Ensure a connector exists for the company
        existing = (
            self.env["l10n_py.edi.connector"]
            .sudo()
            .search([("company_id", "=", self.company.id)])
        )
        if not existing:
            self.env["l10n_py.edi.connector"].create(
                {
                    "name": "Connector 1",
                    "company_id": self.company.id,
                    "provider_type": "sifen",
                    "environment": "test",
                }
            )
        with self.assertRaises(IntegrityError), self.cr.savepoint():
            self.env["l10n_py.edi.connector"].create(
                {
                    "name": "Connector 2",
                    "company_id": self.company.id,
                    "provider_type": "sifen",
                    "environment": "test",
                }
            )

    @patch(
        "odoo.addons.l10n_py_edi_sifen.models.edi_connector"
        ".EDIConnector._sifen_get_consulta"
    )
    def test_test_connection(self, mock_consulta):
        """Test test_connection returns notification action."""
        mock_instance = mock_consulta.return_value
        mock_instance.consultar_ruc.return_value = True
        mock_instance.cleanup.return_value = None

        connector = self.env["l10n_py.edi.connector"].create(
            {
                "name": "SIFEN Test",
                "company_id": self.company.id,
                "provider_type": "sifen",
                "environment": "test",
            }
        )
        result = connector.test_connection()
        self.assertEqual(result["type"], "ir.actions.client")
        self.assertEqual(result["tag"], "display_notification")
