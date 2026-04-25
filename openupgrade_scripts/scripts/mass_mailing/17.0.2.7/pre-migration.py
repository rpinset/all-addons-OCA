# Copyright 2025 Carlos Lopez - Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

_xmlids_renames = [
    (
        "mass_mailing.access_mailing_contact_subscription_mm_user",
        "mass_mailing.access_mailing_subscription_mm_user",
    ),
    ("mass_mailing.view", "mass_mailing.mailing_view"),
    ("mass_mailing.unsubscribe", "mass_mailing.unsubscribe_form"),
    ("mass_mailing.page_unsubscribe", "mass_mailing.page_mailing_unsubscribe"),
    (
        "mass_mailing.mailing_contact_subscription_view_form",
        "mass_mailing.mailing_subscription_view_form",
    ),
    (
        "mass_mailing.mailing_contact_subscription_view_search",
        "mass_mailing.mailing_subscription_view_search",
    ),
    (
        "mass_mailing.mailing_contact_subscription_view_tree",
        "mass_mailing.mailing_subscription_view_tree",
    ),
    ("mass_mailing.mass_mailing_contact_0", "mass_mailing.mass_mail_contact_0"),
]
_models_renames = [
    ("mailing.contact.subscription", "mailing.subscription"),
]
_tables_renames = [
    ("mailing_contact_list_rel", "mailing_subscription"),
]
_fields_renames = [
    (
        "mailing.subscription",
        "mailing_subscription",
        "unsubscription_date",
        "opt_out_datetime",
    ),
]


def _mailing_subscription_add_xmlid_contact_0(env):
    """
    Add XML ID to prevent SQL unique constraint error
    because in V16, a record was added without an XML ID:
    https://github.com/odoo/odoo/blob/f7db1775af3cb641f6cc88607b2d9dce611fb049/addons/mass_mailing/data/mailing_list_data.xml#L10
    and now, in V17, a new record is created using an XML ID:
    https://github.com/odoo/odoo/blob/8ec4108b978f00b0a373a28f602780d87aa0d000/addons/mass_mailing/data/mailing_subscription.xml#L4
    """
    env.cr.execute(
        """
    WITH contact_0 AS (
            SELECT res_id
            FROM ir_model_data imd
            WHERE imd.module = 'mass_mailing'
                AND imd.name = 'mass_mail_contact_0'
                AND imd.model = 'mailing.contact'
        ),
        list_0 AS (
            SELECT res_id
            FROM ir_model_data imd
            WHERE imd.module = 'mass_mailing'
                AND imd.name = 'mailing_list_data'
                AND imd.model = 'mailing.list'
        )
    SELECT id
    FROM mailing_subscription
        JOIN contact_0 ON mailing_subscription.contact_id = contact_0.res_id
        JOIN list_0 ON mailing_subscription.list_id = list_0.res_id
    """
    )
    res = env.cr.fetchone()
    if res:
        openupgrade.add_xmlid(
            env.cr,
            "mass_mailing",
            "mailing_list_data_sub_contact_0",
            "mailing.subscription",
            res[0],
        )


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, _xmlids_renames)
    openupgrade.rename_models(env.cr, _models_renames)
    openupgrade.rename_tables(env.cr, _tables_renames)
    openupgrade.rename_fields(env, _fields_renames)
    _mailing_subscription_add_xmlid_contact_0(env)
