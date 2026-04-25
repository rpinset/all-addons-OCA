# Copyright 2024 Viindoo Technology Joint Stock Company (Viindoo)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


def _base_automation_create_compute_fields(env):
    _new_columns = [
        ("base.automation", "trg_field_ref", "many2one_reference"),
        ("base.automation", "trg_selection_field_id", "many2one"),
    ]

    openupgrade.add_columns(env, _new_columns)


def _base_automation_sync_from_ir_act_server(env):
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE base_automation
            ADD COLUMN IF NOT EXISTS model_id INTEGER,
            ADD COLUMN IF NOT EXISTS name JSONB;
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE base_automation ba
            SET model_id = ias.model_id,
                name = ias.name
        FROM ir_act_server ias
        WHERE ba.action_server_id = ias.id
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    _base_automation_create_compute_fields(env)
    _base_automation_sync_from_ir_act_server(env)
