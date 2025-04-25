from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(
        env,
        [
            (
                "res.company",
                "res_company",
                "crm_team_invoiced_domain",
                "sales_team_invoiced_domain",
            ),
        ],
    )
