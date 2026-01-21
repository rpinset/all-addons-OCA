from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.delete_sql_constraint_safely(
        env, "date_range", "date_range", "date_range_uniq"
    )
    openupgrade.m2o_to_x2m(
        env.cr, env["date.range"], "date_range", "company_ids", "company_id"
    )
    rule = env.ref("date_range.date_range_comp_rule")
    if rule:
        rule.domain_force = (
            "['|',('company_ids', 'in', company_ids),('company_ids','=',False)]"
        )
