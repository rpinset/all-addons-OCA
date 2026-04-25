# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openupgradelib import openupgrade

XMLID_TO_RENAME = [
    "event_event_ticket_form_view",
    "event_event_ticket_view_form_from_event",
    "event_event_ticket_view_kanban_from_event",
    "event_event_ticket_view_tree_from_event",
    "event_type_ticket_view_form_from_type",
    "event_type_ticket_view_tree_from_type",
    "product_category_events",
    "product_product_event",
]


def migrate(cr, version):
    # Done without the openupgrade decorator to force its execution when this module
    # is auto-installed as dependency of event_sale
    xmlid_renames = [(f"event_sale.{x}", f"event_product.{x}") for x in XMLID_TO_RENAME]
    openupgrade.rename_xmlids(cr, xmlid_renames)
