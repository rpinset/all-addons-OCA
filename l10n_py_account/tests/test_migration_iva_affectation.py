# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
import importlib.util
from pathlib import Path

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


def _load_migrate_function():
    """Import migrate(cr, version) from the versioned migration file
    without relying on it being an importable Python module (Odoo's
    migrations/ folders are not packages)."""
    migration_path = (
        Path(__file__).resolve().parents[1]
        / "migrations"
        / "18.0.1.1.0"
        / "post-migrate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "l10n_py_account_post_migrate_18_0_1_1_0", migration_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.migrate


@tagged("post_install", "-at_install", "l10n_py")
class TestMigrationIvaAffectation(TransactionCase):
    def _create_tax(self, amount, affectation):
        tax = self.env["account.tax"].create(
            {
                "name": f"Test tax {affectation}/{amount}",
                "amount": amount,
                "amount_type": "percent",
                "type_tax_use": "sale",
            }
        )
        # Bypass the field's own default/ORM write to simulate the exact
        # pre-migration state (a pre-existing row backfilled to "1" by
        # Odoo's schema sync), independently of whatever the model's
        # current default/constraints do on create().
        self.env.cr.execute(
            "UPDATE account_tax SET l10n_py_iva_affectation = %s WHERE id = %s",
            (affectation, tax.id),
        )
        tax.invalidate_recordset(["l10n_py_iva_affectation"])
        return tax

    def test_migration_reclassifies_zero_amount_gravado_as_exenta(self):
        """B1: a pre-existing amount=0 tax left at the backfilled default
        '1' must become '3' (Exenta) after the migration -- otherwise it
        keeps being reported as Gravado (ivaTipo=1) in the SIFEN
        document, silently, after upgrading to this version."""
        tax = self._create_tax(amount=0, affectation="1")
        migrate = _load_migrate_function()
        migrate(self.env.cr, "18.0.1.1.0")
        tax.invalidate_recordset(["l10n_py_iva_affectation"])
        self.assertEqual(tax.l10n_py_iva_affectation, "3")

    def test_migration_never_touches_a_real_gravado_tax(self):
        """A tax with a real, non-zero rate and affectation '1' is
        legitimately Gravado -- the migration must not touch it."""
        tax = self._create_tax(amount=10, affectation="1")
        migrate = _load_migrate_function()
        migrate(self.env.cr, "18.0.1.1.0")
        tax.invalidate_recordset(["l10n_py_iva_affectation"])
        self.assertEqual(tax.l10n_py_iva_affectation, "1")

    def test_migration_never_overrides_an_explicit_exonerado(self):
        """A tax already explicitly classified as Exonerado ('2') must
        not be reclassified -- the migration only touches rows still at
        the backfilled default '1'."""
        tax = self._create_tax(amount=0, affectation="2")
        migrate = _load_migrate_function()
        migrate(self.env.cr, "18.0.1.1.0")
        tax.invalidate_recordset(["l10n_py_iva_affectation"])
        self.assertEqual(tax.l10n_py_iva_affectation, "2")
