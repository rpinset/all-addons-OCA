# Copyright 2016-2020 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def post_init_hook(env):
    """Add street3 to address format"""
    query = """
        UPDATE res_country
        SET address_format = replace(
        address_format,
        E'%(street2)s\n',
        E'%(street2)s\n%(street3)s\n'
        )
    """
    env.cr.execute(query)


def uninstall_hook(env):
    """Remove street3 from address format"""
    # Remove %(street3)s\n from address_format
    query = """
        UPDATE res_country
        SET address_format = replace(
        address_format,
        E'%(street3)s\n',
        ''
        )
    """
    env.cr.execute(query)

    # Remove %(street3)s from address_format
    query = """
        UPDATE res_country
        SET address_format = replace(
        address_format,
        E'%(street3)s',
        ''
        )
    """
    env.cr.execute(query)
