# Copyright 2025 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>

from odoo.tools.sql import column_exists


def migrate(cr, version):
    if not column_exists(
        cr, "stock_release_channel", "recompute_channel_on_pickings_at_release"
    ) and column_exists(cr, "res_company", "recompute_channel_on_pickings_at_release"):
        cr.execute(
            """
            ALTER TABLE stock_release_channel ADD COLUMN
            recompute_channel_on_pickings_at_release boolean;

            UPDATE stock_release_channel
            SET recompute_channel_on_pickings_at_release =
            res_company.recompute_channel_on_pickings_at_release
            FROM res_company
            WHERE res_company.id = stock_release_channel.company_id;
            """
        )
