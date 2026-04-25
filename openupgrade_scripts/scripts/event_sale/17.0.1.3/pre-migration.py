# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def _adjust_event_ticket_sequence(env):
    """As now the order is by sequence, and on v16 it was the price, we have to assign
    the sequence numbers to preserve the previous order by default. Once in v17, you
    can redefine the order to your choice if desired.
    """
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE event_event_ticket eet
        SET sequence = sub.row_number
        FROM (
            SELECT id, event_id, row_number()
            OVER (PARTITION BY event_id order by price)
            FROM event_event_ticket
        ) as sub
        WHERE sub.id = eet.id
        """,
    )


def _prefill_event_registration_sale_status(env):
    openupgrade.add_columns(
        env, [(False, "sale_status", "char", "to_pay", "event_registration")]
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE event_registration er
        SET sale_status = 'free'
        FROM sale_order_line sol
        WHERE sol.id = er.sale_order_line_id AND sol.price_total = 0
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """UPDATE event_registration
        SET sale_status = 'sold'
        WHERE is_paid AND sale_status = 'to_pay'
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    _adjust_event_ticket_sequence(env)
    _prefill_event_registration_sale_status(env)
