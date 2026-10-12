# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).


def create_py_company(cls, name="Test Empresa Paraguay SA", **vals):
    """Create a Paraguayan company for a test class and make it the current one.

    The localization tests must not rely on (nor modify) ``base.main_company``:
    the Odoo demo company stays whatever the Odoo demo data made it, and the
    Paraguayan demo data lives in its own company (see the demo files).
    ``cls.env`` is replaced by an environment whose current company is the new one.
    """
    country_py = cls.env.ref("base.py")
    currency_pyg = cls.env.ref("base.PYG")
    currency_pyg.active = True
    company = cls.env["res.company"].create(
        {
            "name": name,
            "country_id": country_py.id,
            "account_fiscal_country_id": country_py.id,
            "currency_id": currency_pyg.id,
            **vals,
        }
    )
    cls.env.user.company_ids |= company
    cls.env = cls.env(
        context=dict(cls.env.context, allowed_company_ids=[company.id]),
    )
    return cls.env["res.company"].browse(company.id)
