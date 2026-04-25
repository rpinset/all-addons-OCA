from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version=None):
    """
    web_tour.tour used to be just a marker which tour has been run for which user,
    with a new record for every user who finished the tour.
    In v18 tours are unique by name and have a many2many field for recording which
    users have completed it.
    Move the v17 table out of the way so that we can set tours as consumed in
    end-migration (matched by tour name, if a tour name changes from v17 to v18,
    the migration script will have to rename it in the legacy table - no core module
    does this)
    """
    openupgrade.remove_tables_fks(env.cr, ["web_tour_tour"])
    openupgrade.rename_tables(env.cr, [("web_tour_tour", None)])
