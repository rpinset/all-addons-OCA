# Copyright 2020-2022 CorporateHub (https://corporatehub.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2.extensions import AsIs

from odoo import api, fields, models, tools


class L10nEeReportingKmdInf(models.Model):
    _name = "l10n.ee.reporting.kmd.inf"
    _description = "l10n EE Reporting KMD INF"
    _auto = False
    _order = "part asc, move_date desc, partner_name asc"

    company_id = fields.Many2one("res.company", readonly=True)
    part = fields.Selection([("A", "Part A"), ("B", "Part B")], readonly=True)
    currency_id = fields.Many2one("res.currency", readonly=True)
    move_id = fields.Many2one("account.move", readonly=True)
    move_date = fields.Date(readonly=True)
    invoice_date = fields.Date(readonly=True)
    invoice_amount_untaxed = fields.Monetary(readonly=True)
    invoice_amount_total = fields.Monetary(readonly=True)
    tax_group_id = fields.Many2one("account.tax.group", readonly=True)
    tax_rate = fields.Float(readonly=True)
    transactions_tax_base_amount = fields.Monetary(readonly=True)
    transactions_tax_amount = fields.Monetary(readonly=True)
    partner_id = fields.Many2one("res.partner", readonly=True)
    partner_name = fields.Char(readonly=True)
    partner_vat = fields.Char(string="Partner Tax ID", readonly=True)

    @api.model
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        l10n_ee_accounting_vat_20 = self.env.ref(
            "l10n_ee_accounting.vat_20",
            raise_if_not_found=False,
        )
        l10n_ee_accounting_vat_9 = self.env.ref(
            "l10n_ee_accounting.vat_9",
            raise_if_not_found=False,
        )
        base_ee = self.env.ref("base.ee")
        if not l10n_ee_accounting_vat_20 or not l10n_ee_accounting_vat_9:
            self.env.cr.execute(
                """CREATE OR REPLACE VIEW %s AS (
                SELECT
                    NULL::INTEGER AS id,
                    NULL::INTEGER AS company_id,
                    NULL::VARCHAR AS part,
                    NULL::INTEGER AS currency_id,
                    NULL::INTEGER AS move_id,
                    NULL::DATE AS move_date,
                    NULL::DATE AS invoice_date,
                    NULL::NUMERIC AS invoice_amount_untaxed,
                    NULL::NUMERIC AS invoice_amount_total,
                    NULL::INTEGER AS tax_group_id,
                    NULL::NUMERIC AS tax_rate,
                    NULL::NUMERIC AS transactions_tax_base_amount,
                    NULL::NUMERIC AS transactions_tax_amount,
                    NULL::INTEGER AS partner_id,
                    NULL::VARCHAR AS partner_name,
                    NULL::VARCHAR AS partner_vat
                LIMIT 0
            )""",
                (AsIs(self._table),),
            )
            return

        self.env.cr.execute(
            """CREATE OR REPLACE VIEW %s AS (
            SELECT
                entry.id AS id,
                entry.company_id AS company_id,
                entry.part AS part,
                entry.currency_id AS currency_id,
                entry.move_id AS move_id,
                entry.move_date AS move_date,
                entry.invoice_date AS invoice_date,
                entry.invoice_amount_untaxed AS invoice_amount_untaxed,
                entry.invoice_amount_total AS invoice_amount_total,
                entry.tax_group_id AS tax_group_id,
                entry.tax_rate AS tax_rate,
                SUM(
                    tax_move_line.tax_base_amount
                        * SIGN(entry.invoice_amount_total)
                ) AS transactions_tax_base_amount,
                SUM(
                    GREATEST(tax_move_line.debit, tax_move_line.credit)
                        * SIGN(entry.invoice_amount_total)
                ) AS transactions_tax_amount,
                entry.partner_id AS partner_id,
                entry.partner_name AS partner_name,
                entry.partner_vat AS partner_vat
            FROM (
                SELECT
                    ROW_NUMBER () OVER () as id,
                    move_line.company_id AS company_id,
                    (
                        CASE
                            WHEN move.move_type = 'out_invoice' THEN 'A'
                            WHEN move.move_type = 'out_refund' THEN 'A'
                            WHEN move.move_type = 'in_invoice' THEN 'B'
                            WHEN move.move_type = 'in_refund' THEN 'B'
                        END
                    ) AS part,
                    move_line.company_currency_id AS currency_id,
                    move.id AS move_id,
                    move.date AS move_date,
                    move.invoice_date AS invoice_date,
                    move.amount_untaxed_signed AS invoice_amount_untaxed,
                    move.amount_total_signed AS invoice_amount_total,
                    tax.tax_group_id AS tax_group_id,
                    (
                        CASE
                            WHEN tax.tax_group_id = %s THEN 20
                            WHEN tax.tax_group_id = %s THEN 9
                        END
                    ) AS tax_rate,
                    ARRAY_AGG(tax.id) as tax_ids,
                    partner.id AS partner_id,
                    partner.name AS partner_name,
                    partner.vat AS partner_vat
                FROM %s AS move_line
                INNER JOIN %s AS move ON
                    move.id = move_line.move_id
                INNER JOIN %s AS aml_tax_rel ON
                    aml_tax_rel.account_move_line_id = move_line.id
                INNER JOIN %s AS tax ON
                    tax.id = aml_tax_rel.account_tax_id
                INNER JOIN %s AS partner ON
                    partner.id = move_line.partner_id
                WHERE
                        move.state = 'posted'
                    AND
                        move.move_type IN (
                            'out_invoice',
                            'out_refund',
                            'in_invoice',
                            'in_refund'
                        )
                    AND
                        tax.tax_group_id IN (%s, %s)
                    AND
                        partner.is_company IS TRUE
                    AND
                        partner.vat IS NOT NULL
                    AND
                        partner.country_id = %s
                GROUP BY
                    move_line.company_id,
                    part,
                    move_line.company_currency_id,
                    move.id,
                    move.date,
                    move.invoice_date,
                    move.amount_untaxed_signed,
                    move.amount_total_signed,
                    tax.tax_group_id,
                    partner.id,
                    partner.name,
                    partner.vat
                ORDER BY
                    part,
                    invoice_date
            ) AS entry
            INNER JOIN account_move_line AS tax_move_line ON
                    tax_move_line.move_id = entry.move_id
                AND
                    tax_move_line.partner_id = entry.partner_id
                AND
                    tax_move_line.tax_line_id =ANY (entry.tax_ids)
            GROUP BY
                entry.id,
                entry.company_id,
                entry.part,
                entry.currency_id,
                entry.move_id,
                entry.move_date,
                entry.invoice_date,
                entry.invoice_amount_untaxed,
                entry.invoice_amount_total,
                entry.tax_group_id,
                entry.tax_rate,
                entry.partner_id,
                entry.partner_name,
                entry.partner_vat
        )""",
            (
                AsIs(self._table),
                l10n_ee_accounting_vat_20.id,
                l10n_ee_accounting_vat_9.id,
                AsIs(self.env["account.move.line"]._table),
                AsIs(self.env["account.move"]._table),
                AsIs(self.env["account.move.line"]._fields["tax_ids"].relation),
                AsIs(self.env["account.tax"]._table),
                AsIs(self.env["res.partner"]._table),
                l10n_ee_accounting_vat_20.id,
                l10n_ee_accounting_vat_9.id,
                base_ee.id,
            ),
        )
