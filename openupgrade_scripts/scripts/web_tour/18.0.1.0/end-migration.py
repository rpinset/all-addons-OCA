from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version=None):
    """
    Set consumed tours from legacy table after migration
    """
    openupgrade.logged_query(
        env.cr,
        f"""
        INSERT INTO res_users_web_tour_tour_rel
        (res_users_id, web_tour_tour_id)
        SELECT legacy_table.user_id, web_tour_tour.id
        FROM
        {openupgrade.get_legacy_name('web_tour_tour')} legacy_table,
        web_tour_tour
        WHERE web_tour_tour.name=legacy_table.name
        ON CONFLICT DO NOTHING
        """,
    )
