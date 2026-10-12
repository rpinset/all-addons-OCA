# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "l10n_py")
class TestGravadoParcialGuard(TransactionCase):
    """B2: 'Gravado parcial' (iAfecIVA=4) has no real dPropIVA
    calculation implemented -- generating the electronic document with
    it would silently emit an incorrect fiscal proportion. Must fail
    loud during validation instead."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tax_gravado_parcial = cls.env["account.tax"].create(
            {
                "name": "IVA Gravado parcial test",
                "amount": 10,
                "amount_type": "percent",
                "type_tax_use": "sale",
                "l10n_py_iva_affectation": "4",
            }
        )
        cls.product = cls.env["product.product"].create(
            {"name": "Producto gravado parcial"}
        )

    def _invoice_with_partial_tax(self):
        partner = self.env["res.partner"].create({"name": "Cliente test"})
        return self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": partner.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "quantity": 1,
                            "price_unit": 100,
                            "tax_ids": [(6, 0, [self.tax_gravado_parcial.id])],
                        },
                    )
                ],
            }
        )

    def test_gravado_parcial_line_fails_validation(self):
        inv = self._invoice_with_partial_tax()
        with self.assertRaises(UserError) as cm:
            inv._validate_edi_data()
        self.assertIn("Gravado parcial", str(cm.exception))

    def test_regular_gravado_line_does_not_trigger_this_guard(self):
        """Sanity check: a normal, fully-taxed line must never trigger
        the 'Gravado parcial' guard, even though other, unrelated
        _validate_edi_data errors may still raise for this minimal
        invoice (company RUC, timbrado, etc.)."""
        tax_normal = self.env["account.tax"].create(
            {
                "name": "IVA normal test",
                "amount": 10,
                "amount_type": "percent",
                "type_tax_use": "sale",
                "l10n_py_iva_affectation": "1",
            }
        )
        partner = self.env["res.partner"].create({"name": "Cliente normal test"})
        inv = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": partner.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "quantity": 1,
                            "price_unit": 100,
                            "tax_ids": [(6, 0, [tax_normal.id])],
                        },
                    )
                ],
            }
        )
        try:
            inv._validate_edi_data()
        except UserError as exc:
            self.assertNotIn("Gravado parcial", str(exc))
