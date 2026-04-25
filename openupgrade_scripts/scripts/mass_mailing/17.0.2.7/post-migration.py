# Copyright 2025 Carlos Lopez - Tecnativa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def _utm_campaign_fill_ab_testing_winner_mailing_id(env):
    openupgrade.logged_query(
        env.cr,
        """
        WITH winner_mailing AS (
            SELECT
                campaign_id,
                MAX(id) AS mailing_id
            FROM
                mailing_mailing
            WHERE
                ab_testing_enabled IS TRUE
                AND state = 'done'
                AND ab_testing_pc = 100
            GROUP BY
                campaign_id
        )
        UPDATE utm_campaign
            SET ab_testing_winner_mailing_id = winner_mailing.mailing_id
        FROM winner_mailing
        WHERE utm_campaign.id = winner_mailing.campaign_id
            AND utm_campaign.ab_testing_completed IS TRUE
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env, "mass_mailing", "17.0.2.7/noupdate_changes.xml")
    openupgrade.delete_record_translations(
        env.cr, "mass_mailing", ["mass_mailing_mail_layout"], field_list=["arch_db"]
    )
    _utm_campaign_fill_ab_testing_winner_mailing_id(env)
