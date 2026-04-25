# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def convert_triggering_answer_id_m2o_to_m2m(env):
    openupgrade.logged_query(
        env.cr,
        "UPDATE survey_question SET triggering_answer_id=NULL WHERE NOT is_conditional",
    )
    openupgrade.m2o_to_x2m(
        env.cr,
        env["survey.question"],
        "survey_question",
        "triggering_answer_ids",
        "triggering_answer_id",
    )


@openupgrade.migrate()
def migrate(env, version):
    convert_triggering_answer_id_m2o_to_m2m(env)
