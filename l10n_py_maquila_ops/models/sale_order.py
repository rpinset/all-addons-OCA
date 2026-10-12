# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    l10n_py_maquila_program_id = fields.Many2one(
        "l10n_py.maquila.program",
        string="Maquila Program",
    )
    l10n_py_maquila_type = fields.Selection(
        related="l10n_py_maquila_program_id.maquila_type",
        string="Maquila Type",
    )
    l10n_py_is_maquila_export = fields.Boolean(
        compute="_compute_is_maquila_export",
    )

    l10n_py_maquila_cap_override = fields.Boolean(
        string="Override Domestic Sales Cap",
        groups="l10n_py_maquila_base.group_maquila_manager",
        tracking=True,
        copy=False,
        help="Explicit exception to the Art. 18 domestic sales cap of pure "
        "maquila. Only Maquila managers can set it; a reason is required and "
        "the use is logged in the chatter when the order is confirmed.",
    )
    l10n_py_maquila_cap_override_reason = fields.Char(
        string="Override Reason",
        groups="l10n_py_maquila_base.group_maquila_manager",
        tracking=True,
        copy=False,
    )

    @api.depends("l10n_py_maquila_program_id")
    def _compute_is_maquila_export(self):
        for order in self:
            order.l10n_py_is_maquila_export = bool(order.l10n_py_maquila_program_id)

    @api.onchange("l10n_py_maquila_program_id")
    def _onchange_maquila_program(self):
        if not self.l10n_py_maquila_program_id:
            return
        partner = self.partner_id
        company = self.company_id or self.env.company
        is_foreign = (
            bool(partner.country_id) and partner.country_id != company.country_id
        )
        if (
            is_foreign
            and self.fiscal_position_id
            and self.fiscal_position_id.auto_apply
        ):
            # A fiscal position was already auto-detected for the foreign
            # partner (e.g. the chart's "Ventas - Exportación" position,
            # which maps IVA to the exonerated tax). Keep it instead of
            # overwriting it with the maquila position below, which has no
            # tax mapping of its own and would leave the VAT untouched.
            return
        fp = self.env.ref(
            "l10n_py_maquila_ops.fiscal_position_maquila_export",
            raise_if_not_found=False,
        )
        if fp:
            self.fiscal_position_id = fp

    def action_confirm(self):
        py_country = self.env.ref("base.py", raise_if_not_found=False)
        for order in self:
            # A salesperson without a maquila group must still be able to
            # confirm: the cap is a company rule, not a permission, so the
            # program and the exports are read with sudo.
            program = order.sudo().l10n_py_maquila_program_id
            # Art. 18 caps domestic sales only for the "pura" modality.
            if not (program and py_country and program.maquila_type == "pura"):
                continue
            if order.partner_id.country_id != py_country:
                continue
            order_sudo = order.sudo()
            if order_sudo.l10n_py_maquila_cap_override:
                order._apply_maquila_cap_override()
                continue
            order._check_maquila_domestic_cap(program)
        return super().action_confirm()

    def _apply_maquila_cap_override(self):
        """Explicit and audited exception to the Art. 18 cap."""
        self.ensure_one()
        if not self.env.user.has_group("l10n_py_maquila_base.group_maquila_manager"):
            raise UserError(
                _("Only Maquila managers can override the domestic sales cap.")
            )
        reason = self.sudo().l10n_py_maquila_cap_override_reason
        if not reason:
            raise UserError(
                _("A reason is required to override the domestic sales cap.")
            )
        self.message_post(
            body=_(
                "Art. 18 domestic sales cap overridden by %(user)s. Reason: "
                "%(reason)s",
                user=self.env.user.name,
                reason=reason,
            )
        )

    def _check_maquila_domestic_cap(self, program):
        """Ley 7547/2025 Art. 18: pure maquila may sell to the domestic market
        up to a percentage (10% by default) of the exported volume of the last
        year. The cap only applies to the pure modality (the caller filters).
        Amounts are converted to the company currency before comparing.

        Open legal questions, deliberately not decided here:
        - The law says "volumen exportado" (volume); the module measures the
          exported FOB value because quantities of different products and
          units cannot be added. Pending confirmation with the Secretaria
          Ejecutiva / DNIT.
        - "ultimo ano" is read as the previous calendar year; a rolling
          12-month window is the alternative reading.
        A pure maquila with no exports in that period has cap == 0, so any
        domestic sale is blocked; the only way around is the explicit,
        audited override (manager group + reason logged in the chatter)."""
        self.ensure_one()
        company = self.company_id
        company_currency = company.currency_id
        today = fields.Date.context_today(self)
        pct = program.internal_sale_pct or 10.0
        year = today.year
        prior_exports = (
            self.env["l10n_py.maquila.export.line"]
            .sudo()
            .search(
                [
                    ("export_id.program_id", "=", program.id),
                    ("export_id.date_export", ">=", f"{year - 1}-01-01"),
                    ("export_id.date_export", "<=", f"{year - 1}-12-31"),
                ]
            )
        )
        export_base = sum(
            line.currency_id._convert(
                line.fob_value,
                company_currency,
                company,
                line.export_id.date_export or today,
            )
            for line in prior_exports
        )
        cap = export_base * pct / 100.0
        py_country = self.env.ref("base.py")
        other_domestic = (
            self.sudo()
            .search(
                [
                    ("l10n_py_maquila_program_id", "=", program.id),
                    ("state", "=", "sale"),
                    ("id", "!=", self.id),
                ]
            )
            .filtered(lambda o: o.partner_id.country_id == py_country)
        )
        already = sum(
            o.currency_id._convert(o.amount_untaxed, company_currency, company, today)
            for o in other_domestic
        )
        current = self.currency_id._convert(
            self.amount_untaxed, company_currency, company, today
        )
        if not cap:
            raise UserError(
                _(
                    "Program %(program)s (pure maquila) has no exports in the "
                    "last year, so the Art. 18 domestic sales cap is zero and "
                    "domestic sales are not allowed. A Maquila manager can "
                    "override this explicitly on the order.",
                    program=program.code,
                )
            )
        if already + current > cap:
            raise UserError(
                _(
                    "Domestic sales for program %(program)s would exceed the "
                    "%(pct)s%% cap of prior-year exports (cap: %(cap).2f %(cur)s).",
                    program=program.code,
                    pct=pct,
                    cap=cap,
                    cur=company_currency.name,
                )
            )
