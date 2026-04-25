# Copyright 2023-2024 Tecnativa - Víctor Martínez
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """It is important to set the appropriate report_footer and company_details values.
    The report_footer field already existed before, but it only represented the 'extra'
    text that was added after the company data (https://github.com/odoo/odoo/blob/cc0060e889603eb2e47fa44a8a22a70d7d784185/addons/web/views/report_templates.xml#L367).
    Now in v15 this data https://github.com/odoo/odoo/blob/3a28e5b0adbb36bdb1155a6854cdfbe4e7f9b187/addons/web/views/report_templates.xml#L338
    is not shown unless it is defined; therefore, we must apply the corresponding
    default that would be defined from the base.document.layout wizard and then add the
    old report_footer data (if it was defined).
    There is now a company_details field that does not have a default value, so it will
    be created empty.
    It is important to define the corresponding value that would be defined from the
    base.document.layout wizard because in the report now only the content of that
    field is shown, while in v14 it was not necessary since the address was shown
    according to the partner_id field.
    v14 https://github.com/odoo/odoo/blob/cc0060e889603eb2e47fa44a8a22a70d7d784185/addons/web/views/report_templates.xml#L343
    vs v15 https://github.com/odoo/odoo/blob/3a28e5b0adbb36bdb1155a6854cdfbe4e7f9b187/addons/web/views/report_templates.xml#L319
    """  # noqa: B950
    for company in env["res.company"].search([]):
        # We define what the footer should have as it had v14
        # https://github.com/odoo/odoo/blob/cc0060e889603eb2e47fa44a8a22a70d7d784185/addons/web/views/report_templates.xml#L362  # noqa: B950
        report_footer = '<ul class="list-inline">'
        if company.phone:
            report_footer += f'<li class="list-inline-item"><i class="fa fa-phone" role="img"/> <span class="o_force_ltr">{company.phone}</span></li>'  # noqa: B950
        if company.email:
            report_footer += f'<li class="list-inline-item"><i class="fa fa-at" role="img"/> <span>{company.email}</span></li>'  # noqa: B950
        if company.website:
            report_footer += f'<li class="list-inline-item"><i class="fa fa-globe" role="img"/> <span>{company.website}</span></li>'  # noqa: B950
        if company.vat:
            vat_label = company.country_id.vat_label or "Tax ID"
            report_footer += f'<li class="list-inline-item"><i class="fa fa-building-o" role="img"/>{vat_label}: <span>{company.vat}</span></li>'  # noqa: B950
        report_footer += "</ul>"
        # Add the extra text (if any) with a separating line
        if company.report_footer:
            report_footer += "<hr>" + company.report_footer
        company_details = (
            env["base.document.layout"].with_company(company)._default_company_details()
        )
        company.write(
            {
                "report_footer": report_footer,
                "company_details": company_details,
            }
        )
