# Copyright 2023 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from base64 import b64encode

from odoo import exceptions
from odoo.tests import tagged
from odoo.tools.misc import file_open

from odoo.addons.account.tests.common import AccountTestInvoicingCommon

_logger = logging.getLogger(__name__)


@tagged("post_install_l10n", "post_install", "-at_install")
class TestDatevImportCsvDtvf(AccountTestInvoicingCommon):
    @classmethod
    @AccountTestInvoicingCommon.setup_country("de")
    @AccountTestInvoicingCommon.setup_chart_template("de_skr03")
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "l10n_germany_skr03",
                "country_id": cls.env.ref("base.de").id,
            }
        )
        for code in ("1200",):
            _logger.info(f"create account {code} for test")
            cls.env["account.account"].create(
                {
                    "name": code,
                    "code": code,
                    "account_type": "asset_receivable",
                    "reconcile": True,
                }
            )
        # cls.env["account.account"].search(
        #     [("code", "=", "4900")]
        # ).account_type = "income"
        for code in ("4811",):
            if cls.env["account.analytic.account"].search(
                [
                    ("code", "=", code),
                    ("company_id", "=", cls.env.company.id),
                ]
            ):
                continue
            _logger.info(f"create analytic.account {code} for test")
            cls.env["account.analytic.account"].create(
                {
                    "name": code,
                    "code": code,
                    "plan_id": cls.env.ref("analytic.analytic_plan_internal").id,
                }
            )

    def _test_wizard(self, filename):
        wizard = self.env["account.move.import"].create(
            {
                "file_to_import": b64encode(file_open(filename).read().encode("utf8")),
                "force_journal_id": self.env["account.journal"]
                .search([("type", "=", "sale")], limit=1)
                .id,
                "force_move_ref": "/",
                "force_move_line_name": "/",
                "post_move": True,
            }
        )
        action = wizard.run_import()
        move = self.env[action["res_model"]].browse(action["res_id"])
        self.assertEqual(len(move.line_ids), 196)
        first_line = move.line_ids[:1]
        self.assertEqual(first_line.account_id.code, "4900")
        self.assertEqual(first_line.credit, 0.01)
        last_line = move.line_ids[-1:]
        self.assertEqual(last_line.account_id.code, "2450")
        self.assertEqual(last_line.debit, 72)
        analytic_lines = move.line_ids.mapped("analytic_line_ids")
        self.assertEqual(len(analytic_lines), 1)
        self.assertEqual(sum(analytic_lines.mapped("amount")), 0.01)

    def test_wizard_comma_separated(self):
        self._test_wizard("datev_import_csv_dtvf/examples/datev_export.csv")

    def test_wizard_semicolon_separated(self):
        self._test_wizard("datev_import_csv_dtvf/examples/datev_export_semicolon.csv")

    def test_wizard_broken_file(self):
        wizard = self.env["account.move.import"].create(
            {
                "file_to_import": b64encode(
                    b"file,with\nwrong\ndate,format,in,third,line,,,,,wrong date"
                ),
                "force_journal_id": self.env["account.journal"]
                .search([("type", "=", "sale")], limit=1)
                .id,
                "force_move_ref": "/",
                "force_move_line_name": "/",
            }
        )
        with self.assertRaises(exceptions.UserError):
            wizard.run_import()

    def test_nonexisting_account_journal(self):
        wizard = self.env["account.move.import"].create(
            {
                "file_to_import": b64encode(
                    b"EXTF,700,22,Buchungsstapel,12,20230417083808874,,,,,12345,1234,20220101,"
                    b"4,20221201,20221231,Buchungsstapel 20220101,MM,1,,,EUR,"
                    b"\nnonexisting,accounts\n42,H,,,,,42424242,424242420,,23/01"
                ),
            }
        )
        with self.assertRaises(exceptions.UserError):
            wizard.run_import()
