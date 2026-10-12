# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MaquilaGuarantee(models.Model):
    _name = "l10n_py.maquila.guarantee"
    _description = "Maquila Customs Guarantee"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True, tracking=True)
    program_id = fields.Many2one(
        "l10n_py.maquila.program",
        required=True,
        tracking=True,
    )
    guarantee_type = fields.Selection(
        [
            ("bank", "Bank Guarantee"),
            ("insurance", "Insurance Bond"),
            ("deposit", "Cash Deposit"),
            ("mortgage", "Mortgage"),
        ],
        required=True,
        tracking=True,
    )
    scope = fields.Selection(
        [
            ("operation", "Per Operation"),
            ("global", "Global"),
        ],
        default="operation",
        required=True,
        tracking=True,
        help="Decreto 5714/2026 Art. 28: the DNIT may authorize global "
        "guarantees covering one or more customs operations. A per-operation "
        "guarantee covers a single admission. Form, modalities and validity "
        "follow art. 293 of the Customs Code (Ley 2422/2004) and its "
        "regulations; they are not validated by this module.",
    )
    issuer = fields.Char(
        help="Bank or insurance company",
    )
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.ref("base.USD"),
    )
    amount = fields.Monetary(required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
    state = fields.Selection(
        [
            ("active", "Active"),
            ("expired", "Expired"),
            ("released", "Released"),
        ],
        default="active",
        required=True,
        tracking=True,
    )
    admission_ids = fields.One2many(
        "l10n_py.maquila.admission",
        "guarantee_id",
        string="Admissions",
    )
    amount_used = fields.Monetary(
        compute="_compute_amounts",
    )
    amount_available = fields.Monetary(
        compute="_compute_amounts",
    )
    company_id = fields.Many2one(
        related="program_id.company_id",
        store=True,
    )

    @api.depends(
        "amount",
        "currency_id",
        "admission_ids.state",
        "admission_ids.amount_cif",
        "admission_ids.currency_id",
    )
    def _compute_amounts(self):
        for rec in self:
            # Sum CIF amounts of active admissions linked to this guarantee,
            # converted to the guarantee currency.
            company = rec.company_id or self.env.company
            active = rec.admission_ids.filtered(
                lambda a: a.state in ("admitted", "in_production")
            )
            rec.amount_used = sum(
                adm.currency_id._convert(
                    adm.amount_cif,
                    rec.currency_id,
                    company,
                    adm.date_admission or fields.Date.context_today(rec),
                )
                if adm.currency_id and rec.currency_id
                else adm.amount_cif
                for adm in active
            )
            rec.amount_available = rec.amount - rec.amount_used

    def _scope_admissions(self):
        """Admissions that still hold the guarantee: a closed or expired
        admission releases a per-operation guarantee."""
        self.ensure_one()
        return self.admission_ids.filtered(
            lambda a: a.state not in ("closed", "expired")
        )

    @api.constrains("scope", "admission_ids")
    def _check_scope_admissions(self):
        for rec in self:
            if rec.scope == "operation" and len(rec._scope_admissions()) > 1:
                raise ValidationError(
                    _(
                        "A per-operation guarantee covers a single admission. "
                        "Use a global guarantee for several operations."
                    )
                )

    @api.model
    def _cron_expire_guarantees(self):
        """A guarantee past its end date must not keep covering admissions."""
        expired = self.search(
            [
                ("state", "=", "active"),
                ("date_end", "<", fields.Date.context_today(self)),
            ]
        )
        expired.write({"state": "expired"})
        return expired
