# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def pre_init_hook(env):
    env.cr.execute(
        "ALTER TABLE sale_order ADD COLUMN IF NOT EXISTS route_area_id INTEGER"
    )
