# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MaquilaProgram(models.Model):
    _name = "l10n_py.maquila.program"
    _description = "Maquila Program"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "code"

    name = fields.Char(required=True, tracking=True)
    code = fields.Char(
        string="Biministerial Resolution",
        required=True,
        tracking=True,
        help="Resolucion biministerial (e.g. RES-BIM-2026-001)",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("suspended", "Suspended"),
            ("closed", "Closed"),
        ],
        default="draft",
        required=True,
        tracking=True,
    )
    maquila_type = fields.Selection(
        [
            ("pura", "Maquila Pura"),
            ("servicio", "Maquila de Servicios"),
            ("ociosidad", "Capacidad Ociosa"),
            ("sub_maquila", "Sub-Maquila (Sub-contratación)"),
            ("shelter", "Shelter / Albergue"),
            ("coexistencia", "Coexistencia (régimen ordinario)"),
            ("abrigo", "Maquila de Abrigo"),
        ],
        required=True,
        tracking=True,
        help="Legal modalities under Ley 7547/2025 (Arts. 3, 25-27). "
        "'abrigo' is kept for the textile/garment rubro.",
    )
    legal_regime = fields.Selection(
        [
            ("ley_7547", "Ley 7547/2025"),
            ("ley_1064", "Ley 1064/97 (legacy)"),
        ],
        default="ley_7547",
        required=True,
        tracking=True,
        help="Legacy 1064/97 programs keep prior conditions for 12 months, "
        "then migrate to Ley 7547/2025 (Art. 42).",
    )
    benefit_duration_years = fields.Integer(
        default=20,
        help="Benefit term in years (Ley 7547/2025 Art. 13: 20 years, renewable).",
    )
    benefit_expiry = fields.Date(
        compute="_compute_benefit_expiry",
        store=True,
        help="End of the benefit term, computed from the resolution date.",
    )
    matriz_partner_id = fields.Many2one(
        "res.partner",
        string="Foreign Matrix",
        required=True,
        tracking=True,
        help="Foreign parent company (owner of temporary goods)",
    )
    company_id = fields.Many2one(
        "res.company",
        string="Maquiladora",
        required=True,
        default=lambda self: self.env.company,
        tracking=True,
    )
    agreement_id = fields.Many2one(
        "agreement",
        string="CNIME Contract",
        tracking=True,
        help="OCA Agreement linked to CNIME contract",
    )
    cnime_resolution_date = fields.Date(
        string="CNIME Resolution Date",
        tracking=True,
    )
    cnime_resolution_expiry = fields.Date(
        string="CNIME Resolution Expiry",
        tracking=True,
    )
    internal_sale_pct = fields.Float(
        string="Internal Market %",
        help="Percentage allowed for domestic sale (capacidad ociosa type)",
    )
    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        string="Analytic Account",
        tracking=True,
        help="Analytic account for accounting segregation of this program",
    )
    resolution_attachment = fields.Binary(
        string="Resolution PDF",
        attachment=True,
    )
    resolution_attachment_name = fields.Char()
    product_line_ids = fields.One2many(
        "l10n_py.maquila.program.product",
        "program_id",
        string="Product Lines",
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            "code_company_uniq",
            "unique(code, company_id)",
            "The resolution code must be unique per company.",
        ),
    ]

    @api.depends("cnime_resolution_date", "benefit_duration_years")
    def _compute_benefit_expiry(self):
        for program in self:
            if program.cnime_resolution_date and program.benefit_duration_years:
                program.benefit_expiry = program.cnime_resolution_date + relativedelta(
                    years=program.benefit_duration_years
                )
            else:
                program.benefit_expiry = False

    @api.constrains("internal_sale_pct")
    def _check_internal_sale_pct(self):
        for program in self:
            if not 0 <= program.internal_sale_pct <= 100:
                raise ValidationError(
                    _("Internal market %% must be between 0 and 100.")
                )

    def _schedule_unique_expiry_activity(self, date_deadline, summary):
        """Schedule a warning activity only if an open one with the same
        summary does not already exist (idempotent cron)."""
        self.ensure_one()
        activity_type = self.env.ref("mail.mail_activity_data_warning")
        existing = self.env["mail.activity"].search_count(
            [
                ("res_model", "=", self._name),
                ("res_id", "=", self.id),
                ("activity_type_id", "=", activity_type.id),
                ("summary", "=", summary),
            ]
        )
        if not existing:
            self.activity_schedule(
                "mail.mail_activity_data_warning",
                date_deadline=date_deadline,
                summary=summary,
            )

    def action_activate(self):
        self.write({"state": "active"})

    def action_suspend(self):
        self.write({"state": "suspended"})

    def action_close(self):
        self.write({"state": "closed"})

    def action_draft(self):
        self.write({"state": "draft"})

    @api.model
    def _cron_check_expiry(self):
        """Check for programs, contracts, and INTN certificates nearing expiry."""
        today = fields.Date.today()

        # Programs expiring in 90 days
        limit_program = today + relativedelta(days=90)
        expiring_programs = self.search(
            [
                ("state", "=", "active"),
                ("cnime_resolution_expiry", "<=", limit_program),
                ("cnime_resolution_expiry", ">=", today),
            ]
        )
        for program in expiring_programs:
            program._schedule_unique_expiry_activity(
                program.cnime_resolution_expiry,
                _(
                    "Program %(code)s expires on %(date)s",
                    code=program.code,
                    date=program.cnime_resolution_expiry,
                ),
            )

        # Contracts expiring in 120 days
        limit_contract = today + relativedelta(days=120)
        programs_contract = self.search(
            [
                ("state", "=", "active"),
                ("agreement_id.end_date", "<=", limit_contract),
                ("agreement_id.end_date", ">=", today),
            ]
        )
        for program in programs_contract:
            program._schedule_unique_expiry_activity(
                program.agreement_id.end_date,
                _(
                    "Contract for program %(code)s expires on %(date)s",
                    code=program.code,
                    date=program.agreement_id.end_date,
                ),
            )

        # INTN certificates expiring in 60 days
        limit_intn = today + relativedelta(days=60)
        expiring_intn = self.env["l10n_py.maquila.program.product"].search(
            [
                ("program_id.state", "=", "active"),
                ("intn_expiry_date", "<=", limit_intn),
                ("intn_expiry_date", ">=", today),
            ]
        )
        for line in expiring_intn:
            line.program_id._schedule_unique_expiry_activity(
                line.intn_expiry_date,
                _(
                    "INTN certificate for %(product)s expires on %(date)s",
                    product=line.product_id.name,
                    date=line.intn_expiry_date,
                ),
            )


class MaquilaProgramProduct(models.Model):
    _name = "l10n_py.maquila.program.product"
    _description = "Maquila Program Product"

    program_id = fields.Many2one(
        "l10n_py.maquila.program",
        required=True,
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        "product.product",
        required=True,
    )
    intn_certificate = fields.Char(
        string="INTN Certificate",
    )
    intn_certificate_date = fields.Date(
        string="INTN Certificate Date",
    )
    intn_expiry_date = fields.Date(
        string="INTN Expiry Date",
        help="INTN certificate validity (typically 2 years)",
    )
