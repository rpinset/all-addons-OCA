# Copyright 2020-2022 CorporateHub (https://corporatehub.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2.extensions import AsIs

from odoo import api, fields, models, tools


class L10nEeReportingViesDeclaration(models.Model):
    _name = "l10n.ee.reporting.vies.declaration"
    _description = "l10n EE Reporting VIES declaration"
    _auto = False
    _order = "date desc"

    company_id = fields.Many2one("res.company", readonly=True)
    move_line_id = fields.Many2one("account.move.line", readonly=True)
    date = fields.Date(readonly=True)
    amount = fields.Monetary(readonly=True)
    currency_id = fields.Many2one("res.currency", readonly=True)
    product_id = fields.Many2one("product.product", readonly=True)
    product_type = fields.Selection(
        [("goods", "Goods"), ("services", "Services")],
        readonly=True,
    )
    partner_id = fields.Many2one("res.partner", readonly=True)
    partner_vat = fields.Char(string="Tax ID", readonly=True)

    @api.model
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        l10n_ee_accounting_kmd2017_3_1 = self.env.ref(
            "l10n_ee_accounting.kmd2017_3_1",
            raise_if_not_found=False,
        )
        if not l10n_ee_accounting_kmd2017_3_1:
            self.env.cr.execute(
                """
                CREATE OR REPLACE VIEW %s AS (
                    SELECT
                        NULL::INTEGER AS id,
                        NULL::INTEGER AS company_id,
                        NULL::INTEGER AS move_line_id,
                        NULL::DATE AS date,
                        NULL::NUMERIC AS amount,
                        NULL::INTEGER AS currency_id,
                        NULL::INTEGER as product_id,
                        NULL::VARCHAR AS product_type,
                        NULL::INTEGER as partner_id,
                        NULL::VARCHAR as partner_vat
                    LIMIT 0
                )
                """,
                (AsIs(self._table),),
            )
            return

        self.env.cr.execute(
            """
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    move_line.id AS id,
                    move_line.company_id AS company_id,
                    move_line.id AS move_line_id,
                    move_line.date AS date,
                    (
                        CASE WHEN tag.tax_negate IS TRUE
                            THEN -move_line.balance
                            ELSE move_line.balance
                        END
                    ) AS amount,
                    move_line.company_currency_id AS currency_id,
                    move_line.product_id as product_id,
                    (
                        CASE
                            WHEN product_template.type = 'service' THEN 'services'
                            ELSE 'goods'
                        END
                    ) AS product_type,
                    move_line.partner_id as partner_id,
                    partner.vat as partner_vat
                FROM %s AS move_line
                INNER JOIN %s AS move_line_tax_rel ON
                    move_line_tax_rel.account_move_line_id = move_line.id
                INNER JOIN %s AS tag ON
                    tag.id = move_line_tax_rel.account_account_tag_id
                INNER JOIN %s AS product ON
                    product.id = move_line.product_id
                INNER JOIN %s AS product_template ON
                    product_template.id = product.product_tmpl_id
                INNER JOIN %s AS partner ON
                    partner.id = move_line.partner_id
                WHERE
                    partner.vat IS NOT NULL AND
                    move_line_tax_rel.account_account_tag_id IN %s
            )
            """,
            (
                AsIs(self._table),
                AsIs(self.env["account.move.line"]._table),
                AsIs(self.env["account.move.line"]._fields["tax_tag_ids"].relation),
                AsIs(self.env["account.account.tag"]._table),
                AsIs(self.env["product.product"]._table),
                AsIs(self.env["product.template"]._table),
                AsIs(self.env["res.partner"]._table),
                tuple(l10n_ee_accounting_kmd2017_3_1.tag_ids.ids),
            ),
        )
