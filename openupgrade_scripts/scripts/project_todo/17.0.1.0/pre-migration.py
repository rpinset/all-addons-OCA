# Copyright 2024 Viindoo Technology Joint Stock Company (Viindoo)
# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


def _convert_note_tag_to_project_tags(env):
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO project_tags (
            color, create_uid, write_uid, name, create_date, write_date
        )
        SELECT color, create_uid, write_uid, name, create_date, write_date
        FROM note_tag
        ON CONFLICT (name) DO NOTHING;
        """,
    )


def _convert_note_note_to_project_task(env):
    openupgrade.logged_query(
        env.cr, "ALTER TABLE project_task ADD COLUMN old_note_id INTEGER"
    )
    # if the OCA project_task_code was installed, code is required
    column_exists = openupgrade.column_exists(env.cr, "project_task", "code")
    openupgrade.logged_query(
        env.cr,
        f"""
            INSERT INTO project_task(
                create_uid, write_uid, create_date, write_date,
                active, name, description, priority, sequence, state, project_id,
                display_in_project, company_id, color, old_note_id
                {column_exists and ", code" or ""}
            )
            SELECT create_uid, write_uid, create_date, write_date,
                open, name, memo, '0', sequence, '01_in_progress', null,
                true, company_id, color, id
                {column_exists and ", ('OU' || id::VARCHAR)" or ""}
            FROM note_note
            """,
    )


def _fill_project_tags(env):
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO project_tags_project_task_rel (project_task_id, project_tags_id)
        SELECT project_task.id, project_tags.id
        FROM note_tags_rel rel
        JOIN project_task ON project_task.old_note_id = rel.note_id
        JOIN note_tag ON rel.tag_id = note_tag.id
        JOIN project_tags ON project_tags.name = note_tag.name;
        """,
    )


def _fill_stage_for_todo_task(env):
    openupgrade.logged_query(
        env.cr, "ALTER TABLE project_task_type ADD COLUMN old_note_stage_id INTEGER"
    )
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO project_task_type (
            create_uid, write_uid, create_date, write_date, active,
            user_id, sequence, name, fold, old_note_stage_id
        )
        SELECT
            create_uid, write_uid, create_date, write_date, true,
            user_id, sequence, name, fold, id
        FROM note_stage
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO project_task_user_rel(
            task_id, user_id, stage_id
        )
        SELECT
            project_task.id task_id,
            project_task_type.user_id,
            project_task_type.id stage_id
        FROM note_stage_rel rel
        JOIN project_task ON project_task.old_note_id = rel.note_id
        JOIN project_task_type ON project_task_type.old_note_stage_id = rel.stage_id
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    _convert_note_tag_to_project_tags(env)
    _convert_note_note_to_project_task(env)
    _fill_project_tags(env)
    _fill_stage_for_todo_task(env)
    openupgrade.merge_models(env.cr, "note.note", "project.task", "old_note_id")
