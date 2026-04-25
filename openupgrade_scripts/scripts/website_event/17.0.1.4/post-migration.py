# Copyright 2024-2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade
from psycopg2.extras import Json


def fill_event_question(env):
    # Query ‘name’, ‘email’, ‘phone’ fields of ‘res.partner’ with their translations
    env.cr.execute(
        """
        SELECT imf.name, imf.field_description
        FROM ir_model_fields AS imf
        JOIN ir_model AS im ON imf.model_id = im.id
        WHERE im.model = 'res.partner'
        AND imf.name IN ('name', 'email', 'phone')
    """
    )
    field_descriptions = dict(env.cr.fetchall())
    question_types = [
        ("name", True),
        ("email", True),
        ("phone", False),
    ]
    for qtype, mandatory in question_types:
        title_json = field_descriptions.get(qtype)
        env.cr.execute(
            """
            INSERT INTO event_question (
                event_id, title, question_type,
                is_mandatory_answer, once_per_order,
                sequence, create_date, write_date
            )
            SELECT ee.id, %s, %s, %s, FALSE, 10, now(), now()
            FROM event_event AS ee
        """,
            (Json(title_json), qtype, mandatory),
        )


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env, "website_event", "17.0.1.4/noupdate_changes.xml")
    fill_event_question(env)
