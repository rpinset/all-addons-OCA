# Copyright (C) 2022 Trevi Software (https://trevi.et)
# Copyright (C) 2014 Michael Telahun Makonnen <mmakonnen@gmail.com>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Federal Income Tax Tables 2008",
    "summary": "Ethiopian Federal Income Tax tables (rev. 2008)",
    "version": "14.0.1.0.0",
    "category": "Localization",
    "images": ["static/src/img/main_screenshot.png"],
    "license": "AGPL-3",
    "author": "TREVI Software",
    "website": "https://github.com/trevi-software/trevi-hr",
    "depends": [
        "payroll",
        "l10n_et_payroll_category",
    ],
    "data": [
        "data/payroll_data.xml",
    ],
    "installable": True,
}
