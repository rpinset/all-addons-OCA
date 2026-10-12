from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "l10n_py")
class TestIvaAffectation(TransactionCase):
    def test_field_exists_without_default(self):
        tax = self.env["account.tax"].create(
            {
                "name": "IVA test",
                "amount": 10,
                "amount_type": "percent",
                "type_tax_use": "sale",
            }
        )
        # Sin default: un impuesto sin afectación explícita queda falsy para
        # que el fallback de retrocompatibilidad (_l10n_py_infer_affectation)
        # trabaje en bases existentes. Un default '1' marcaría como Gravado
        # el Exento preexistente en el upgrade.
        self.assertFalse(tax.l10n_py_iva_affectation)

    def test_affectation_settable(self):
        tax = self.env["account.tax"].create(
            {
                "name": "IVA exonerado",
                "amount": 0,
                "amount_type": "percent",
                "type_tax_use": "sale",
                "l10n_py_iva_affectation": "2",
            }
        )
        self.assertEqual(tax.l10n_py_iva_affectation, "2")

    def test_chart_has_exonerado_sale_tax(self):
        # após carga do chart PY na company de teste
        company = self.env["res.company"].create({"name": "PY Co Chart"})
        self.env["account.chart.template"].try_loading(
            "py", company=company, install_demo=False
        )
        tax = (
            self.env["account.tax"]
            .with_company(company)
            .search(
                [
                    ("type_tax_use", "=", "sale"),
                    ("l10n_py_iva_affectation", "=", "2"),
                    ("amount", "=", 0),
                ],
                limit=1,
            )
        )
        self.assertTrue(
            tax, "Debe existir un IVA exonerado de venta (afectación 2) en el chart PY"
        )
