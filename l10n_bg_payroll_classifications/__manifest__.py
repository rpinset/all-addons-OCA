#  Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Bulgarian HR Payroll Classifications",
    "version": "18.0.5.0.2",
    "category": "Human Resources/Localization",
    "summary": (
        "Bulgarian localization for HR payroll with NKPD and Economic Activity "
        "classifications"
    ),
    "author": "Odoo Community Association (OCA), Rosen Vladimirov",
    "website": "https://github.com/OCA/l10n-bulgaria",
    "license": "LGPL-3",
    "depends": ["base", "hr"],
    "data": [
        "security/ir.model.access.csv",
        "data/bg_hr_payroll_economic_activity/parent/bg.hr.payroll.economic.activity.csv",
        "data/bg_hr_payroll_economic_activity/div/bg.hr.payroll.economic.activity.csv",
        "data/bg_hr_payroll_economic_activity/grp/bg.hr.payroll.economic.activity.csv",
        "data/bg_hr_payroll_economic_activity/cls/bg.hr.payroll.economic.activity.csv",
        "data/bg_hr_payroll_ncop_classification/major/bg.hr.payroll.ncop.classification.csv",
        "data/bg_hr_payroll_ncop_classification/sub_major/bg.hr.payroll.ncop.classification.csv",
        "data/bg_hr_payroll_ncop_classification/minor/bg.hr.payroll.ncop.classification.csv",
        "data/bg_hr_payroll_ncop_classification/unit/bg.hr.payroll.ncop.classification.csv",
        "data/bg_hr_payroll_ncop_classification/occupation/bg.hr.payroll.ncop.classification.csv",
        "views/bg_ncop_classification.xml",
        "views/bg_mod_economic_activity.xml",
        "views/hr_job_views.xml",
        "views/hr_menus.xml",
    ],
    "images": ["static/description/banner.png"],
    "demo": [],
    "installable": True,
    "auto_install": False,
    "application": False,
    "maintainers": ["rosenvladimirov"],
    "contributors": ["Rosen Vladimirov"],
    "support": "https://github.com/OCA/l10n-bulgaria/issues",
    "countries": ["BG"],
}
