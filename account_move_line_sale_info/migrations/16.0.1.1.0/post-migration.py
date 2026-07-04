# Copyright 2024 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Backfill sale_line_id on anglo-saxon COGS lines that the previous
    implementation left empty when several invoice lines on the same move
    shared the same product and quantity.

    Mirrors the per-move pair-aware logic now used in
    AccountMove._stock_account_prepare_anglo_saxon_out_lines_vals
    """
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    move_groups = env["account.move.line"].read_group(
        domain=[
            ("display_type", "=", "cogs"),
            ("sale_line_id", "=", False),
            (
                "move_id.move_type",
                "in",
                ("out_invoice", "out_refund", "out_receipt"),
            ),
            ("company_id.anglo_saxon_accounting", "=", True),
        ],
        fields=["move_id"],
        groupby=["move_id"],
    )
    if not move_groups:
        return
    move_ids = [g["move_id"][0] for g in move_groups]
    moves = env["account.move"].browse(move_ids)
    _logger.info(
        "account_move_line_sale_info: backfilling sale_line_id on COGS "
        "lines for %s moves",
        len(moves),
    )
    updated = 0
    for move in moves:
        broken = move.line_ids.filtered(
            lambda l: l.display_type == "cogs" and not l.sale_line_id
        )
        # Respect any SOL already linked to other COGS
        # lines in the move
        consumed = set(
            move.line_ids.filtered(
                lambda l: l.display_type == "cogs" and l.sale_line_id
            )
            .mapped("sale_line_id")
            .ids
        )
        # First group COGS pair lines by product and qty
        groups_by_pq = {}
        for cogs in broken:
            key = (cogs.product_id.id, cogs.quantity)
            groups_by_pq.setdefault(key, env["account.move.line"])
            groups_by_pq[key] |= cogs
        # For each product/qty group, assign SOL candidates
        for (product_id, quantity), group in groups_by_pq.items():
            candidates = move.invoice_line_ids.filtered(
                lambda il: il.product_id.id == product_id and il.quantity == quantity
            ).mapped("sale_line_ids")
            available = [sol for sol in candidates if sol.id not in consumed]
            if not available:
                continue
            # Within a (product, qty) group each invoice line produced
            # one interim row + one expense row
            # Pair them by creation order (id ASC) and
            # assign one available SOL per pair
            accounts = group.mapped("account_id")
            if len(accounts) != 2:
                _logger.warning(
                    "Skipping move %s product %s qty %s: expected 2 "
                    "distinct COGS pair accounts, found %s",
                    move.id,
                    product_id,
                    quantity,
                    len(accounts),
                )
                continue
            rows_a = group.filtered(lambda l: l.account_id == accounts[0]).sorted("id")
            rows_b = group.filtered(lambda l: l.account_id == accounts[1]).sorted("id")
            if len(rows_a) != len(rows_b):
                _logger.warning(
                    "Skipping move %s product %s qty %s: unbalanced "
                    "COGS rows (%s vs %s)",
                    move.id,
                    product_id,
                    quantity,
                    len(rows_a),
                    len(rows_b),
                )
                continue
            pair_count = min(len(rows_a), len(available))
            for i in range(pair_count):
                sol_id = available[i].id
                (rows_a[i] + rows_b[i]).with_context(check_move_validity=False).write(
                    {"sale_line_id": sol_id}
                )
                consumed.add(sol_id)
                updated += 2
    _logger.info(
        "account_move_line_sale_info: backfilled sale_line_id on %s " "COGS lines",
        updated,
    )
