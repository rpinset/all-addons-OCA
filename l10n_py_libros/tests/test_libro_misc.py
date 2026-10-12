from pathlib import Path

from odoo.tests import tagged

from .test_libro_common import LibroCommonCase

FORBIDDEN_TERMS = (
    "claude",
    "anthropic",
    "co-authored-by",
    "generated with",
    "chatgpt",
    "openai",
    "gpt-",
    "copilot",
)


@tagged("post_install", "-at_install", "l10n_py", "l10n_py_libros")
class TestLibroMisc(LibroCommonCase):
    def test_module_installs_without_enterprise(self):
        module = self.env["ir.module.module"].search([("name", "=", "l10n_py_libros")])
        self.assertEqual(module.state, "installed")
        self.assertNotIn("account_reports", module.dependencies_id.mapped("name"))

    def test_flag_partner_company_dependent(self):
        company_b = self.env["res.company"].create({"name": "Empresa B Libros Test"})
        self.supplier.with_company(self.company.id).l10n_py_libro_electronic = True
        self.assertTrue(
            self.supplier.with_company(self.company.id).l10n_py_libro_electronic
        )
        self.assertFalse(
            self.supplier.with_company(company_b.id).l10n_py_libro_electronic
        )

    def test_mapeamento_tabla3_tabla4_active_test_false(self):
        mapping_model = self.env["l10n_py.libro.document.type.map"]
        record = mapping_model.search([("codigo_tabla4", "=", "109")], limit=1)
        record.active = False
        found = mapping_model.with_context(active_test=False).search(
            [("codigo_tabla4", "=", "109")]
        )
        self.assertIn(record, found)

    def test_dominio_multivalorado_ventas_e_compras(self):
        mapping_model = self.env["l10n_py.libro.document.type.map"]
        codigos_ventas = mapping_model._get_codigos_for_tipo_registro("ventas")
        codigos_compras = mapping_model._get_codigos_for_tipo_registro("compras")
        for codigo in ("109", "110", "111"):
            self.assertIn(codigo, codigos_ventas)
            self.assertIn(codigo, codigos_compras)
        codigos_ingresos = mapping_model._get_codigos_for_tipo_registro("ingresos")
        codigos_egresos = mapping_model._get_codigos_for_tipo_registro("egresos")
        self.assertIn("208", codigos_ingresos)
        self.assertIn("208", codigos_egresos)

    def test_identificacao_ausente_marca_linha_em_erro(self):
        invoice = self._create_invoice(
            "out_invoice", [(self.product, self.tax_10, 1100.0)]
        )
        invoice.action_post()
        libro = self._create_libro("ventas")
        libro.action_generate_lines()
        line = libro.line_ids
        line.with_context(l10n_py_libro_regenerating=True).write(
            {"f_tipo_identificacion": False, "f_numero_identificacion": False}
        )
        self.assertEqual(line.state, "erro")

    def test_monto_total_zero_marca_linha_em_erro(self):
        invoice = self._create_invoice(
            "out_invoice", [(self.product, self.tax_10, 1100.0)]
        )
        invoice.action_post()
        libro = self._create_libro("ventas")
        libro.action_generate_lines()
        line = libro.line_ids
        line.with_context(l10n_py_libro_regenerating=True).write(
            {"f_monto_total": 0, "f_monto_gravado_10": 0}
        )
        self.assertEqual(line.state, "erro")

    def test_excluir_linha_em_erro_permitido(self):
        invoice = self._create_invoice(
            "in_invoice", [(self.product, self.tax_10_purchase, 1100.0)]
        )
        invoice.action_post()
        libro = self._create_libro("compras")
        libro.action_generate_lines()
        line = libro.line_ids
        self.assertEqual(line.state, "erro")
        line.unlink()
        self.assertEqual(len(libro.line_ids), 0)

    def test_no_ai_attribution(self):
        module_dir = Path(__file__).resolve().parent.parent
        self_file = Path(__file__).resolve()
        for path in module_dir.rglob("*"):
            if path == self_file:
                # This file legitimately holds the forbidden-terms list used
                # to scan every other file in the module.
                continue
            if path.is_file() and path.suffix in (
                ".py",
                ".xml",
                ".csv",
                ".md",
                ".rst",
            ):
                content = path.read_text(encoding="utf-8", errors="ignore").lower()
                for term in FORBIDDEN_TERMS:
                    self.assertNotIn(term, content, f"Term {term!r} found in {path}")
