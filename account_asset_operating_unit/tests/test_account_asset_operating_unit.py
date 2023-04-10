# Copyright 2021 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import time

from odoo import Command, fields
from odoo.tests.common import TransactionCase


class TestAccountAssetOperatingUnit(TransactionCase):
    def setUp(self):
        super().setUp()
        self.AccountAccount = self.env["account.account"]
        self.AccountAsset = self.env["account.asset"]
        self.ResUsers = self.env["res.users"]
        self.product_id = self.env["product.template"].search(
            [("type", "=", "service")], limit=1
        )
        self.partner = self.env["res.partner"].create({"name": "Test Partner"})
        # Groups
        self.grp_account_manager = self.env.ref("account.group_account_manager")
        self.group_user = self.env.ref("base.group_user")
        # Company
        self.company = self.env.ref("base.main_company")
        # Main Operating Unit
        self.main_OU = self.env.ref("operating_unit.main_operating_unit")
        # B2C Operating Unit
        self.b2c_OU = self.env.ref("operating_unit.b2c_operating_unit")
        # Create User 1 with Main OU
        self.user1 = self._create_user(
            "user_1",
            [self.grp_account_manager, self.group_user],
            self.company,
            [self.main_OU],
        )
        # Create User 2 with B2C OU
        self.user2 = self._create_user(
            "user_2",
            [self.grp_account_manager, self.group_user],
            self.company,
            [self.b2c_OU],
        )
        # Accounts
        self.account_expense = self.AccountAccount.search(
            [
                ("company_id", "=", self.company.id),
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_expenses").id,
                ),
            ],
            limit=1,
        )
        self.account_asset = self.env["account.account"].search(
            [
                ("company_id", "=", self.company.id),
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_current_assets").id,
                ),
            ],
            limit=1,
        )
        # Journal
        self.journal_purchase = self.env["account.journal"].search(
            [("company_id", "=", self.company.id), ("type", "=", "purchase")], limit=1
        )
        # Asset Group
        self.asset_group_id = self.env["account.asset.group"].create(
            {
                "name": "Fixed Assets",
                "code": "FA",
            }
        )
        # Asset Profile
        self.profile_id = self.env["account.asset.profile"].create(
            {
                "account_expense_depreciation_id": self.account_expense.id,
                "account_asset_id": self.account_asset.id,
                "account_depreciation_id": self.account_asset.id,
                "journal_id": self.journal_purchase.id,
                "name": "Hardware - 3 Years",
                "method_time": "year",
                "method_number": 3,
                "method_period": "year",
                "group_ids": [(6, 0, [self.asset_group_id.id])],
            }
        )
        self.asset1 = self._create_asset(self.user1.id, self.main_OU)
        self.asset2 = self._create_asset(self.user2.id, self.b2c_OU)
        self.invoice = (
            self.env["account.move"]
            .with_context(check_move_validity=False)
            .create(
                {
                    "move_type": "in_invoice",
                    "invoice_date": fields.Date.context_today(self.env.user),
                    "partner_id": self.partner.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "test 2",
                                "product_id": self.product_id.id,
                                "price_unit": 10000.00,
                                "quantity": 1,
                            }
                        ),
                        Command.create(
                            {
                                "name": "test 3",
                                "product_id": self.product_id.id,
                                "price_unit": 20000.00,
                                "quantity": 1,
                            }
                        ),
                    ],
                }
            )
        )

    def _create_user(self, login, groups, company, operating_units):
        """Create a user."""
        group_ids = [group.id for group in groups]
        user = self.ResUsers.create(
            {
                "name": login,
                "login": login,
                "password": "demo",
                "email": "test@yourcompany.com",
                "company_id": company.id,
                "company_ids": [(4, company.id)],
                "operating_unit_ids": [(4, ou.id) for ou in operating_units],
                "groups_id": [(6, 0, group_ids)],
            }
        )
        return user

    def _create_asset(self, uid, operating_unit):
        asset = self.AccountAsset.with_user(uid).create(
            {
                "name": "Test Asset",
                "profile_id": self.profile_id.id,
                "purchase_value": 1000,
                "salvage_value": 0,
                "date_start": time.strftime("%Y-01-01"),
                "method_time": "year",
                "method_number": 3,
                "method_period": "month",
                "operating_unit_id": operating_unit.id,
            }
        )
        return asset

    def test_create_asset_from_move(self):
        all_assets = self.env["account.asset"].search([])
        ctx = dict(self.invoice._context)
        invoice = self.invoice.with_context(**ctx)
        self.profile_id.asset_product_item = True
        # Compute depreciation lines on invoice validation
        self.profile_id.open_asset = True
        self.assertTrue(len(invoice.invoice_line_ids) == 2)
        invoice.invoice_line_ids.write(
            {"quantity": 1, "asset_profile_id": self.profile_id.id}
        )
        invoice.action_post()
        # Retrieve all assets after invoice validation
        current_assets = self.env["account.asset"].search([])
        new_assets = current_assets - all_assets
        self.assertEqual(len(new_assets), 2)
        for asset in new_assets:
            dlines = asset.depreciation_line_ids.filtered(
                lambda l: l.type == "depreciate"
            )
            dlines = dlines.sorted(key=lambda l: l.line_date)
            self.assertAlmostEqual(dlines[0].depreciated_value, 0.0)
            self.assertAlmostEqual(dlines[-1].remaining_value, 0.0)
            move = dlines[0].create_move()
            m = self.env["account.move"].browse(move)
            self.assertEqual(m.operating_unit_id, new_assets.operating_unit_id)

    def test_asset(self):
        # User 2 is only assigned to B2C Operating Unit, and cannot
        # access asset for Main Operating Unit.
        asset_ids = self.AccountAsset.with_user(self.user2.id).search(
            [
                ("id", "=", self.asset2.id),
                ("operating_unit_id", "=", self.main_OU.id),
            ]
        )
        self.assertEqual(
            asset_ids.ids,
            [],
            "User 2 should not have access to %s" % self.main_OU.name,
        )
        self.assertEqual(self.asset1.operating_unit_id.id, self.main_OU.id)

    def test_asset_report(self):
        fy_dates = self.env.company.compute_fiscalyear_dates(fields.date.today())
        wizard = self.env["wiz.account.asset.report"].create(
            {
                "asset_group_id": self.asset_group_id.id,
                "date_from": fy_dates["date_from"],
                "date_to": fy_dates["date_to"],
                "operating_unit_id": self.main_OU.id,
            }
        )
        report_action = wizard.xls_export()
        self.assertGreaterEqual(
            report_action.items(),
            {
                "type": "ir.actions.report",
                "report_type": "xlsx",
                "report_name": "account_asset_management.asset_report_xls",
            }.items(),
        )
        model = self.env["report.%s" % report_action["report_name"]].with_context(
            active_model=wizard._name, **report_action["context"]
        )
        model.create_xlsx_report(wizard.ids, data=report_action["data"])
