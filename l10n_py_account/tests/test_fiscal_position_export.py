from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "l10n_py")
class TestFiscalPositionExport(TransactionCase):
    def test_export_fp_maps_vat_to_exonerado(self):
        company = self.env["res.company"].create({"name": "PY Co FP"})
        self.env["account.chart.template"].try_loading(
            "py", company=company, install_demo=False
        )
        fp = (
            self.env["account.fiscal.position"]
            .with_company(company)
            .search([("name", "=", "Ventas - Exportación")], limit=1)
        )
        self.assertTrue(fp, "FP de exportación debe existir")
        self.assertTrue(
            fp.l10n_py_is_export,
            "El marcador l10n_py_is_export debe venir seteado del CSV del template",
        )
        vat10 = (
            self.env["account.tax"]
            .with_company(company)
            .search([("type_tax_use", "=", "sale"), ("amount", "=", 10)], limit=1)
        )
        mapped = fp.map_tax(vat10)
        self.assertEqual(
            mapped.l10n_py_iva_affectation,
            "2",
            "La FP debe mapear IVA 10% venta -> exonerado (afectación 2)",
        )

    def test_foreign_partner_gets_export_fp(self):
        company = self.env["res.company"].create({"name": "PY Co Rank"})
        self.env["account.chart.template"].try_loading(
            "py", company=company, install_demo=False
        )
        foreign = self.env["res.partner"].create(
            {"name": "Cliente Brasil", "country_id": self.env.ref("base.br").id}
        )
        fp = (
            self.env["account.fiscal.position"]
            .with_company(company)
            ._get_fiscal_position(foreign)
        )
        self.assertEqual(
            fp.name,
            "Ventas - Exportación",
            "Parceiro do exterior deve resolver a FP de exportación",
        )

    def test_domestic_partner_does_not_get_export_fp(self):
        company = self.env["res.company"].create({"name": "PY Co Dom"})
        self.env["account.chart.template"].try_loading(
            "py", company=company, install_demo=False
        )
        domestic = self.env["res.partner"].create(
            {"name": "Cliente PY", "country_id": self.env.ref("base.py").id}
        )
        fp = (
            self.env["account.fiscal.position"]
            .with_company(company)
            ._get_fiscal_position(domestic)
        )
        self.assertNotEqual(
            fp.name,
            "Ventas - Exportación",
            "Venda doméstica NÃO pode resolver a FP de exportación "
            "(IVA exonerado indevido)",
        )

    def test_ranking_does_not_filter_other_auto_apply_fpos(self):
        """Contrato del core: falsy FILTRA la posición. La función de ranking
        debe ser neutra para posiciones no-export — de lo contrario, con socio
        PY se descartan TODAS las auto_apply y una posición doméstica
        automática jamás aplicaría (los tests anteriores pasarían por
        coincidencia, al ser la de exportación la única auto_apply del chart).
        """
        company = self.env["res.company"].create({"name": "PY Co Rank2"})
        self.env["account.chart.template"].try_loading(
            "py", company=company, install_demo=False
        )
        domestic_fp = (
            self.env["account.fiscal.position"]
            .with_company(company)
            .create(
                {
                    "name": "Ventas - Régimen doméstico",
                    "auto_apply": True,
                    "country_id": self.env.ref("base.py").id,
                    "company_id": company.id,
                }
            )
        )
        domestic = self.env["res.partner"].create(
            {"name": "Cliente PY 2", "country_id": self.env.ref("base.py").id}
        )
        fp = (
            self.env["account.fiscal.position"]
            .with_company(company)
            ._get_fiscal_position(domestic)
        )
        self.assertEqual(
            fp,
            domestic_fp,
            "Una auto_apply doméstica debe seguir aplicando con socio PY: la "
            "función de ranking no puede filtrar posiciones no-export",
        )
        foreign = self.env["res.partner"].create(
            {"name": "Cliente AR", "country_id": self.env.ref("base.ar").id}
        )
        fp_foreign = (
            self.env["account.fiscal.position"]
            .with_company(company)
            ._get_fiscal_position(foreign)
        )
        self.assertEqual(
            fp_foreign.name,
            "Ventas - Exportación",
            "Con socio del exterior la export (prioridad 2) debe ganarle a "
            "cualquier otra auto_apply",
        )
