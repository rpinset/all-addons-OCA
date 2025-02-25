# Copyright 2025 ForgeFlow (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class AccountReconcileModel(models.Model):
    _inherit = "account.reconcile.model"

    company_id = fields.Many2one(check_company=True)
