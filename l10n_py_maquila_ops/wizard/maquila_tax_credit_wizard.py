# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class MaquilaTaxCreditWizard(models.TransientModel):
    _name = "l10n_py.maquila.tax.credit.wizard"
    _description = "Maquila Tax Credit (IVA) Wizard"

    program_id = fields.Many2one(
        "l10n_py.maquila.program",
        required=True,
        domain="[('state', '=', 'active')]",
    )
    action_type = fields.Selection(
        [
            ("compensate", "Compensate"),
            ("transfer", "Transfer to Third Party"),
        ],
        required=True,
        default="compensate",
    )
    transfer_partner_id = fields.Many2one(
        "res.partner",
        string="Transfer To",
    )
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.ref("base.USD"),
    )
    amount = fields.Monetary(required=True)
    debit_account_id = fields.Many2one(
        "account.account",
        string="Debit Account",
    )
    credit_account_id = fields.Many2one(
        "account.account",
        string="Credit Account",
    )

    def action_execute(self):
        self.ensure_one()
        if self.action_type == "transfer" and not self.transfer_partner_id:
            raise UserError(_("Please select a partner for the transfer."))
        if not self.amount:
            raise UserError(_("Amount must be greater than zero."))

        ref = _(
            "IVA Credit %(action_type)s - %(program)s - %(date)s",
            action_type=self.action_type,
            program=self.program_id.code,
            date=fields.Date.today(),
        )
        journal = self.env["account.journal"].search(
            [("type", "=", "general"), ("company_id", "=", self.env.company.id)],
            limit=1,
        )
        if not journal:
            raise UserError(_("No miscellaneous journal found."))
        if not self.debit_account_id or not self.credit_account_id:
            raise UserError(_("Please select both debit and credit accounts."))
        company = self.env.company
        today = fields.Date.today()
        amount = self.currency_id._convert(
            self.amount, company.currency_id, company, today
        )
        foreign = self.currency_id != company.currency_id

        def _line(account_id, debit, credit, sign, partner_id=False):
            vals = {
                "name": ref,
                "debit": debit,
                "credit": credit,
                "account_id": account_id,
                "partner_id": partner_id,
            }
            if foreign:
                vals["currency_id"] = self.currency_id.id
                vals["amount_currency"] = sign * self.amount
            return (0, 0, vals)

        transfer_partner = (
            self.transfer_partner_id.id if self.action_type == "transfer" else False
        )
        move_vals = {
            "move_type": "entry",
            "date": today,
            "ref": ref,
            "l10n_py_maquila_program_id": self.program_id.id,
            "journal_id": journal.id,
            "line_ids": [
                _line(self.debit_account_id.id, amount, 0, 1, transfer_partner),
                _line(self.credit_account_id.id, 0, amount, -1),
            ],
        }
        move = self.env["account.move"].create(move_vals)
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": move.id,
            "view_mode": "form",
        }
