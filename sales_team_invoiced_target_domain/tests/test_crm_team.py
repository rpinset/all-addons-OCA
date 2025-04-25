from odoo import fields
from odoo.tests.common import TransactionCase


class TestCrmTeamInvoiced(TransactionCase):
    def setUp(self):
        super(TestCrmTeamInvoiced, self).setUp()
        self.team = self.env["crm.team"].create({"name": "Test Team"})
        self.team2 = self.env["crm.team"].create({"name": "Test Team 2"})
        self.partner_id = self.env["res.partner"].create({"name": "Test Partner"})

    def create_account_move(self, team_id, payment_state_code, amount):
        move = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "team_id": team_id.id,
                "date": fields.Date.today(),
                "amount_untaxed_signed": amount,
                "payment_state": payment_state_code,
                "partner_id": self.partner_id.id,
                "invoice_line_ids": [
                    (0, 0, {"name": "Test Line", "quantity": 1, "price_unit": amount})
                ],
            }
        )
        move.action_post()
        return move

    def test_compute_invoiced_multiple_teams_with_all_payment_states(self):
        payment_states = ["not_paid", "in_payment", "paid", "partial", "reversed"]
        self.env.company.sales_team_invoiced_domain = str(
            [("payment_state", "in", payment_states)]
        )
        for state in payment_states:
            self.create_account_move(self.team, state, 100)
            self.create_account_move(self.team2, state, 50)
        (self.team + self.team2)._compute_invoiced()
        self.assertEqual(self.team.invoiced, 500.0)
        self.assertEqual(self.team2.invoiced, 250.0)

    def test_compute_invoiced_empty_domain(self):
        self.env.company.sales_team_invoiced_domain = "[]"
        self.create_account_move(self.team, "paid", 100)
        self.create_account_move(self.team2, "paid", 50)
        (self.team + self.team2)._compute_invoiced()
        expected_team_invoiced = sum(
            self.env["account.move"]
            .search(
                [
                    ("move_type", "in", ("out_invoice", "out_refund", "out_receipt")),
                    ("team_id", "=", self.team.id),
                    (
                        "date",
                        ">=",
                        fields.Date.to_string(fields.Date.today().replace(day=1)),
                    ),
                    ("date", "<=", fields.Date.to_string(fields.Date.today())),
                ]
            )
            .mapped("amount_untaxed_signed")
        )
        expected_team2_invoiced = sum(
            self.env["account.move"]
            .search(
                [
                    ("move_type", "in", ("out_invoice", "out_refund", "out_receipt")),
                    ("team_id", "=", self.team2.id),
                    (
                        "date",
                        ">=",
                        fields.Date.to_string(fields.Date.today().replace(day=1)),
                    ),
                    ("date", "<=", fields.Date.to_string(fields.Date.today())),
                ]
            )
            .mapped("amount_untaxed_signed")
        )
        self.assertEqual(self.team.invoiced, expected_team_invoiced)
        self.assertEqual(self.team2.invoiced, expected_team2_invoiced)

    def test_compute_invoiced_invalid_domain(self):
        self.env.company.sales_team_invoiced_domain = "invaid domain"
        with self.assertRaises(SyntaxError):
            (self.team + self.team2)._compute_invoiced()
