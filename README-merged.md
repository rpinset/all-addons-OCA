# Merged READMEs

## From OCA/OpenUpgrade


[![Pre-commit Status](https://github.com/OCA/OpenUpgrade/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/OpenUpgrade/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/OpenUpgrade/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/OpenUpgrade/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/OpenUpgrade/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/OpenUpgrade)

<!-- /!\ do not modify above this line -->

![OpenUpgrade logo](https://oca.github.io/OpenUpgrade/_images/OpenUpgrade.png)

# Tools to upgrade Odoo instances from a major version to another

This <a href="https://odoo-community.org">OCA</a> project aims to provide an Open Source upgrade path for <a href="https://github.com/odoo/odoo">Odoo</a> from one major Odoo version to the next one.
It is hosted at <a href="https://github.com/oca/openupgrade">GitHub</a>.
For documentation, see <a href="https://oca.github.io/OpenUpgrade">here</a>.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[openupgrade_framework](openupgrade_framework/) | 18.0.1.0.3 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/StefanRijnhart'><img src='https://github.com/StefanRijnhart.png' width='32' height='32' style='border-radius:50%;' alt='StefanRijnhart'/></a> <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Module to integrate in the server_wide_modules option to make upgrades between two major revisions.
[openupgrade_scripts](openupgrade_scripts/) | 18.0.1.0.0 |  | Module that contains all the migrations analysis and scripts for migrate Odoo SA modules.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/account-analytic


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# account-analytic
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-analytic&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/account-analytic/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-analytic/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/account-analytic/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-analytic/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/account-analytic/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-analytic)
[![Translation Status](https://translation.odoo-community.org/widgets/account-analytic-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-analytic-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

account-analytic

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_analytic_distribution_manual](account_analytic_distribution_manual/) | 18.0.1.0.1 |  | Account analytic distribution manual
[account_analytic_line_commercial_partner](account_analytic_line_commercial_partner/) | 18.0.1.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | This module add the commercial partner field to analytic items
[account_analytic_organization](account_analytic_organization/) | 18.0.1.0.0 | <a href='https://github.com/mpascuall'><img src='https://github.com/mpascuall.png' width='32' height='32' style='border-radius:50%;' alt='mpascuall'/></a> | Adds organization field on the partner so you can use it on your analytic
[account_analytic_parent](account_analytic_parent/) | 18.0.1.0.0 |  | This module reintroduces the hierarchy to the analytic accounts.
[account_analytic_required](account_analytic_required/) | 18.0.1.0.0 |  | Account Analytic Required
[account_analytic_sequence](account_analytic_sequence/) | 18.0.1.0.0 |  | Restore the analytic account sequence
[account_analytic_spread_by_tag](account_analytic_spread_by_tag/) | 18.0.1.0.0 | <a href='https://github.com/miquelalzanillas'><img src='https://github.com/miquelalzanillas.png' width='32' height='32' style='border-radius:50%;' alt='miquelalzanillas'/></a> | Account Analytic Spread by Tag
[account_analytic_tag](account_analytic_tag/) | 18.0.1.1.0 |  | Account Analytic Tag
[account_move_analytic_link](account_move_analytic_link/) | 18.0.1.0.1 |  | This module allows users to navigate from journal items that have analytic distribution assigned to the analytic items generated.
[account_move_update_analytic](account_move_update_analytic/) | 18.0.1.0.0 | <a href='https://github.com/remi-filament'><img src='https://github.com/remi-filament.png' width='32' height='32' style='border-radius:50%;' alt='remi-filament'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | This module allows the user to update analytic on posted moves
[analytic_amount_security](analytic_amount_security/) | 18.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Add a group to constrain which users can see what info on the analytic lines
[analytic_base_department](analytic_base_department/) | 18.0.1.0.0 |  | Add relationship between Analytic and Department
[analytic_hr_department_restriction](analytic_hr_department_restriction/) | 18.0.1.1.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Analytic distributions restriction per HR department
[analytic_partner](analytic_partner/) | 18.0.1.0.0 |  | Search and group analytic entries by partner
[hr_expense_analytic_tag](hr_expense_analytic_tag/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Hr Expense Analytic Tag
[hr_timesheet_analytic_tag](hr_timesheet_analytic_tag/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Hr Timesheet Analytic Tag
[pos_analytic_by_config](pos_analytic_by_config/) | 18.0.1.0.1 |  | Use analytic account defined on POS configuration for POS orders
[product_analytic](product_analytic/) | 18.0.1.0.0 |  | Add analytic distribution models on products and product categories
[purchase_analytic](purchase_analytic/) | 18.0.1.0.0 |  | Purchase Analytic
[purchase_analytic_distribution_model_warehouse](purchase_analytic_distribution_model_warehouse/) | 18.0.1.0.1 |  | Use analytic distribution models based on the picking type's warehouse in purchase orders
[purchase_analytic_tag](purchase_analytic_tag/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Purchase Analytic Tag
[purchase_stock_analytic](purchase_stock_analytic/) | 18.0.1.0.0 |  | Copies the analytic distribution of the purchase order itemto the stock move
[sale_analytic_distribution_model_warehouse](sale_analytic_distribution_model_warehouse/) | 18.0.1.0.1 |  | Use analytic distribution models based on the warehouse in sale orders
[sale_analytic_tag](sale_analytic_tag/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Sale Analytic Tag
[stock_analytic](stock_analytic/) | 18.0.1.2.0 |  | Adds analytic distribution in stock move
[stock_landed_costs_analytic](stock_landed_costs_analytic/) | 18.0.1.0.1 |  | This module adds an analytic account and analytic tags on landed costs lines so that on landed costs validation account moves get analytic account and analytic tags values from landed costs lines.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/account-budgeting


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-budgeting&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/account-budgeting/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-budgeting/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/account-budgeting/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-budgeting/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/account-budgeting/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-budgeting)
[![Translation Status](https://translation.odoo-community.org/widgets/account-budgeting-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-budgeting-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-budgeting

account-budgeting

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_budget_oca](account_budget_oca/) | 18.0.1.2.0 |  | Budgets Management

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/account-closing


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-closing&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/account-closing/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-closing/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/account-closing/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-closing/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/account-closing/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-closing)
[![Translation Status](https://translation.odoo-community.org/widgets/account-closing-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-closing-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-closing

account-closing

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_cutoff_accrual_subscription](account_cutoff_accrual_subscription/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Accrued expenses based on subscriptions
[account_cutoff_base](account_cutoff_base/) | 18.0.1.0.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Base module for Account Cut-offs
[account_cutoff_picking](account_cutoff_picking/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Accrued and prepaid expense/revenue from pickings
[account_cutoff_start_end_dates](account_cutoff_start_end_dates/) | 18.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Cutoffs based on start/end dates
[account_fiscal_year_closing](account_fiscal_year_closing/) | 18.0.1.0.0 |  | Generic fiscal year closing wizard
[account_fiscal_year_closing_range](account_fiscal_year_closing_range/) | 18.0.1.0.0 | <a href='https://github.com/kaynnan, marcelsavegnago'><img src='https://github.com/kaynnan, marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='kaynnan, marcelsavegnago'/></a> | Allow mapping account ranges in fiscal year closing
[account_invoice_start_end_dates](account_invoice_start_end_dates/) | 18.0.1.3.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adds start/end dates on invoice/move lines

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/account-financial-reporting


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-financial-reporting&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/account-financial-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-financial-reporting/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/account-financial-reporting/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-financial-reporting/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/account-financial-reporting/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-financial-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/account-financial-reporting-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-financial-reporting-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-financial-reporting

account-financial-reporting

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_financial_report](account_financial_report/) | 18.0.1.4.15 |  | OCA Financial Reports
[account_financial_report_sale](account_financial_report_sale/) | 18.0.1.0.0 |  | OCA Financial Reports Sale
[account_move_line_report_xls](account_move_line_report_xls/) | 18.0.1.0.0 |  | Journal Items Excel export
[account_tax_balance](account_tax_balance/) | 18.0.1.0.4 |  | Compute tax balances based on date range
[mis_builder_cash_flow](mis_builder_cash_flow/) | 18.0.1.0.1 | <a href='https://github.com/jjscarafia'><img src='https://github.com/jjscarafia.png' width='32' height='32' style='border-radius:50%;' alt='jjscarafia'/></a> | MIS Builder Cash Flow
[mis_template_financial_report](mis_template_financial_report/) | 18.0.2.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Profit & Loss / Balance sheet MIS templates
[partner_statement](partner_statement/) | 18.0.1.2.0 | <a href='https://github.com/MiquelRForgeFlow'><img src='https://github.com/MiquelRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='MiquelRForgeFlow'/></a> | OCA Financial Reports

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/account-financial-tools


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-financial-tools&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/account-financial-tools/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-financial-tools/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/account-financial-tools/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-financial-tools/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/account-financial-tools/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-financial-tools)
[![Translation Status](https://translation.odoo-community.org/widgets/account-financial-tools-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-financial-tools-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-financial-tools

account-financial-tools

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_asset_compute_batch](account_asset_compute_batch/) | 18.0.1.0.0 |  | Assets - Compute Depre. in Batch
[account_asset_force_account](account_asset_force_account/) | 18.0.1.0.0 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> | Asset Force Account
[account_asset_low_value](account_asset_low_value/) | 18.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Assets Management - Low Value Asset
[account_asset_management](account_asset_management/) | 18.0.1.1.6 |  | Assets Management
[account_asset_number](account_asset_number/) | 18.0.1.0.0 |  | Assets Number
[account_asset_transfer](account_asset_transfer/) | 18.0.1.0.1 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Asset Transfer from AUC to Asset
[account_cash_deposit](account_cash_deposit/) | 18.0.1.0.0 |  | Manage cash deposits and cash orders
[account_chart_update](account_chart_update/) | 18.0.2.0.0 |  | Wizard to update a company's account chart from a template
[account_chart_update_code_digits](account_chart_update_code_digits/) | 18.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafelbn'><img src='https://github.com/rafelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafelbn'/></a> | Modify account chart digits lenght
[account_chart_update_l10n_eu_oss_oca](account_chart_update_l10n_eu_oss_oca/) | 18.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Account Chart update OSS OCA
[account_check_deposit](account_check_deposit/) | 18.0.1.1.0 |  | Manage deposit of checks to the bank
[account_dashboard_banner](account_dashboard_banner/) | 18.0.2.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add a configurable banner on the accounting dashboard
[account_dashboard_banner_mis_builder](account_dashboard_banner_mis_builder/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Display MIS builder KPIs in the accounting dashboard banner
[account_fiscal_month](account_fiscal_month/) | 18.0.1.0.0 |  | Provide a fiscal month date range type
[account_fiscal_position_vat_check](account_fiscal_position_vat_check/) | 18.0.1.0.0 |  | Check VAT on invoice validation
[account_fiscal_year](account_fiscal_year/) | 18.0.1.0.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Create Account Fiscal Year
[account_fiscal_year_auto_create](account_fiscal_year_auto_create/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Automatically create new fiscal years, based on the datas of the last fiscal years
[account_invoice_constraint_chronology](account_invoice_constraint_chronology/) | 18.0.1.0.1 |  | Account Invoice Constraint Chronology
[account_journal_general_sequence](account_journal_general_sequence/) | 18.0.1.0.1 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Add configurable sequence to account moves, per journal
[account_journal_lock_date](account_journal_lock_date/) | 18.0.1.0.0 |  | Lock each journal independently
[account_journal_restrict_mode](account_journal_restrict_mode/) | 18.0.1.1.0 |  | Lock All Posted Entries of Journals.
[account_loan](account_loan/) | 18.0.1.0.2 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Account Loan management
[account_lock_date_update](account_lock_date_update/) | 18.0.1.0.0 |  | Allow an Account adviser to update locking date without having access to all technical settings
[account_lock_to_date](account_lock_to_date/) | 18.0.1.0.0 |  | Allows to set an account lock date in the future.
[account_maturity_date_default](account_maturity_date_default/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Account Maturity Date Default
[account_move_fiscal_year](account_move_fiscal_year/) | 18.0.1.0.0 |  | Display the fiscal year on journal entries/item
[account_move_line_purchase_info](account_move_line_purchase_info/) | 18.0.2.0.0 |  | Introduces the purchase order line to the journal items
[account_move_line_sale_info](account_move_line_sale_info/) | 18.0.1.0.0 |  | Introduces the purchase order line to the journal items
[account_move_line_tax_editable](account_move_line_tax_editable/) | 18.0.1.0.0 |  | Allows to edit taxes on non-posted account move lines
[account_move_name_sequence](account_move_name_sequence/) | 18.0.2.0.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/moylop260'><img src='https://github.com/moylop260.png' width='32' height='32' style='border-radius:50%;' alt='moylop260'/></a> <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Generate journal entry number from sequence
[account_move_post_date_user](account_move_post_date_user/) | 18.0.1.0.0 | <a href='https://github.com/JordiMForgeFlow'><img src='https://github.com/JordiMForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiMForgeFlow'/></a> | Trace journal entry posting date and user.
[account_move_print](account_move_print/) | 18.0.1.0.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> | Adds the option to print Journal Entries
[account_move_template](account_move_template/) | 18.0.1.0.0 |  | Templates for recurring Journal Entries
[account_netting](account_netting/) | 18.0.1.0.0 |  | Compensate AR/AP accounts from the same partner
[account_partner_required](account_partner_required/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adds an option 'partner policy' on accounts
[account_sequence_option](account_sequence_option/) | 18.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Manage sequence options for account.move, i.e., invoice, bill, entry
[account_spread_cost_revenue](account_spread_cost_revenue/) | 18.0.1.0.0 |  | Spread costs and revenues over a custom period
[account_usability](account_usability/) | 18.0.1.1.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Adds missing menu entries for Account module and adds the option to enable Saxon Accounting
[product_category_tax](product_category_tax/) | 18.0.1.0.0 |  | Configure taxes in the product category
[purchase_unreconciled](purchase_unreconciled/) | 18.0.1.0.0 | <a href='https://github.com/AaronHForgeFlow'><img src='https://github.com/AaronHForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='AaronHForgeFlow'/></a> | Purchase Unreconciled

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/account-fiscal-rule


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-fiscal-rule&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/account-fiscal-rule/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-fiscal-rule/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/account-fiscal-rule/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-fiscal-rule/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/account-fiscal-rule/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-fiscal-rule)
[![Translation Status](https://translation.odoo-community.org/widgets/account-fiscal-rule-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-fiscal-rule-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-fiscal-rule

account-fiscal-rule

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_avatax_exemption](account_avatax_exemption/) | 18.0.1.0.0 |  | This application allows you to add exemptions to Avatax
[account_avatax_exemption_base](account_avatax_exemption_base/) | 18.0.1.0.0 |  | This application allows you to add exemptions base to Avatax
[account_avatax_oca](account_avatax_oca/) | 18.0.1.1.1 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Compute Sales Tax using the Avalara Avatax Service
[account_avatax_oca_log](account_avatax_oca_log/) | 18.0.1.0.0 |  | Add Logs to Avatax calls
[account_avatax_sale_oca](account_avatax_sale_oca/) | 18.0.1.0.0 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Sales Orders with automatic Tax application using Avatax
[account_avatax_website_sale](account_avatax_website_sale/) | 18.0.1.0.0 | <a href='https://github.com/cybernexus'><img src='https://github.com/cybernexus.png' width='32' height='32' style='border-radius:50%;' alt='cybernexus'/></a> | Ecommerce Sales Orders require tax recalculation prior to payment.
[account_ecotax](account_ecotax/) | 18.0.1.1.1 | <a href='https://github.com/mourad-ehm'><img src='https://github.com/mourad-ehm.png' width='32' height='32' style='border-radius:50%;' alt='mourad-ehm'/></a> <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Ecotax Management: in French context is a 'cost' added to the sale price of electrical or electronic appliances or furnishing items
[account_ecotax_sale](account_ecotax_sale/) | 18.0.1.0.0 | <a href='https://github.com/mourad-ehm'><img src='https://github.com/mourad-ehm.png' width='32' height='32' style='border-radius:50%;' alt='mourad-ehm'/></a> <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Sale Ecotaxe
[account_fiscal_position_partner_type](account_fiscal_position_partner_type/) | 18.0.1.1.0 |  | Account Fiscal Position Partner Type
[account_fiscal_position_vies_warning](account_fiscal_position_vies_warning/) | 18.0.1.0.2 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> | Account Fiscal Position Vies Warning
[account_product_fiscal_classification](account_product_fiscal_classification/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Simplify taxes management for products
[l10n_eu_oss_oca](l10n_eu_oss_oca/) | 18.0.1.0.0 |  | L10n EU OSS OCA

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/account-invoice-reporting


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-invoice-reporting&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/account-invoice-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-invoice-reporting/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/account-invoice-reporting/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-invoice-reporting/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/account-invoice-reporting/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-invoice-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/account-invoice-reporting-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-invoice-reporting-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-invoice-reporting

account-invoice-reporting

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_comment_template](account_comment_template/) | 18.0.1.0.0 |  | Comments templates on invoice documents
[account_invoice_line_report](account_invoice_line_report/) | 18.0.1.0.1 |  | New view to manage invoice lines information
[account_invoice_line_sale_line_position](account_invoice_line_sale_line_position/) | 18.0.1.0.1 |  | Adds the related sale line position on invoice line.
[account_invoice_payment_mode_note_template](account_invoice_payment_mode_note_template/) | 18.0.1.0.0 |  | This addon allow user to customize the payment mode note using jinja2 templates
[account_invoice_production_lot](account_invoice_production_lot/) | 18.0.1.0.1 |  | Display delivered serial numbers in invoice
[account_invoice_report_grouped_by_picking](account_invoice_report_grouped_by_picking/) | 18.0.1.0.2 |  | Print invoice lines grouped by picking
[account_invoice_report_grouped_by_picking_sale_mrp](account_invoice_report_grouped_by_picking_sale_mrp/) | 18.0.1.0.0 |  | Take into account BoM kits in invoice report grouped by picking
[account_invoice_report_payment_info](account_invoice_report_payment_info/) | 18.0.1.0.0 |  | Show payment extended info in invoice
[account_invoice_report_picking_customer_note](account_invoice_report_picking_customer_note/) | 18.0.1.0.2 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Print picking customer note in Invoice
[account_invoice_report_product_sticker](account_invoice_report_product_sticker/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Display Product Stickers on Invoice Reports
[account_invoice_report_salesperson](account_invoice_report_salesperson/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Salesperson info in Invoice report
[account_invoice_report_stock_packaging](account_invoice_report_stock_packaging/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Display Packaging on Invoice Report
[account_reporting_volume](account_reporting_volume/) | 18.0.1.0.0 |  | Volume in the invoices analysis view
[account_reporting_weight](account_reporting_weight/) | 18.0.1.0.0 |  | Weights in the invoices analysis view
[partner_time_to_pay](partner_time_to_pay/) | 18.0.1.0.1 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Add receivables and payables statistics to partners
[stock_account_invoice_report_lot_expiry](stock_account_invoice_report_lot_expiry/) | 18.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Display expiry date in the lots table of the invoice report

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/account-invoicing


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-invoicing&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/account-invoicing/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-invoicing/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/account-invoicing/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-invoicing/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/account-invoicing/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-invoicing)
[![Translation Status](https://translation.odoo-community.org/widgets/account-invoicing-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-invoicing-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-invoicing

account-invoicing

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_billing](account_billing/) | 18.0.1.4.0 | <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Group invoice as billing before payment
[account_global_discount](account_global_discount/) | 18.0.1.0.0 |  | Account Global Discount
[account_invoice_auto_send_by_email](account_invoice_auto_send_by_email/) | 18.0.1.0.1 |  | Invoice with the email transmit method are send automatically.
[account_invoice_check_total](account_invoice_check_total/) | 18.0.1.0.0 |  | Check if the verification total is equal to the bill's total
[account_invoice_clearing](account_invoice_clearing/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Account invoice clearing wizard
[account_invoice_crm_tag](account_invoice_crm_tag/) | 18.0.1.0.0 |  | Account Invoice CRM Tag
[account_invoice_custom_rounding](account_invoice_custom_rounding/) | 18.0.1.0.0 |  | Custom taxes rounding method in invoices
[account_invoice_date_due](account_invoice_date_due/) | 18.0.1.0.1 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Update Invoice's Due Date
[account_invoice_default_code_column](account_invoice_default_code_column/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Display Default code product in a dedicated column on invoice reports
[account_invoice_discount_date](account_invoice_discount_date/) | 18.0.1.0.2 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Set the early discount date on invoices
[account_invoice_discount_display_amount](account_invoice_discount_display_amount/) | 18.0.1.0.0 |  | Show total discount applied and total without discount on invoices.
[account_invoice_fiscal_position_update](account_invoice_fiscal_position_update/) | 18.0.2.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Changing the fiscal position of an invoice will auto-update invoice lines
[account_invoice_fixed_discount](account_invoice_fixed_discount/) | 18.0.1.0.0 |  | Allows to apply fixed amount discounts in invoices.
[account_invoice_line_sequence](account_invoice_line_sequence/) | 18.0.1.0.0 |  | Adds sequence field on invoice lines to manage its order.
[account_invoice_merge](account_invoice_merge/) | 18.0.1.0.1 |  | Merge invoices in draft
[account_invoice_payment_term_date_due](account_invoice_payment_term_date_due/) | 18.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Display invoices date due when using payment terms
[account_invoice_pricelist](account_invoice_pricelist/) | 18.0.1.0.3 |  | Add partner pricelist on invoices
[account_invoice_pricelist_sale](account_invoice_pricelist_sale/) | 18.0.1.0.0 |  | Module to fill pricelist from sales order in invoice.
[account_invoice_refund_line_selection](account_invoice_refund_line_selection/) | 18.0.1.0.0 |  | This module allows the user to refund specific lines in a invoice
[account_invoice_refund_link](account_invoice_refund_link/) | 18.0.1.0.0 |  | Show links between refunds and their originator invoices.
[account_invoice_refund_reason](account_invoice_refund_reason/) | 18.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Account Invoice Refund Reason.
[account_invoice_section_sale_order](account_invoice_section_sale_order/) | 18.0.1.0.1 |  | For invoices targetting multiple sale order addsections with sale order name.
[account_invoice_send_template](account_invoice_send_template/) | 18.0.1.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Choose email template when send batch invoices
[account_invoice_show_currency_rate](account_invoice_show_currency_rate/) | 18.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Show currency rate in invoices.
[account_invoice_subscription_per_contact](account_invoice_subscription_per_contact/) | 18.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Account Invoice Subscription per contact
[account_invoice_supplier_ref_unique](account_invoice_supplier_ref_unique/) | 18.0.1.0.0 |  | Checks that supplier invoices are not entered twice
[account_invoice_supplierinfo_update](account_invoice_supplierinfo_update/) | 18.0.1.1.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | In the supplier invoice, automatically updates all products whose unit price on the line is different from the supplier price
[account_invoice_tax_note](account_invoice_tax_note/) | 18.0.1.0.0 |  | Print tax notes on customer invoices
[account_invoice_tax_required](account_invoice_tax_required/) | 18.0.1.0.1 |  | This module adds functional a check on invoice to force user to set tax on invoice line.
[account_invoice_transmit_method](account_invoice_transmit_method/) | 18.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Configure invoice transmit method (email, post, portal, ...)
[account_invoice_transmit_method_substitution_rule](account_invoice_transmit_method_substitution_rule/) | 18.0.1.0.0 |  | This addon allow to set substitution rules for transmit method
[account_invoice_tree_currency](account_invoice_tree_currency/) | 18.0.1.0.0 |  | Show currencies in the invoice tree view
[account_invoice_triple_discount](account_invoice_triple_discount/) | 18.0.1.0.0 |  | Manage triple discount on invoice lines
[account_invoice_warn_message](account_invoice_warn_message/) | 18.0.1.0.0 |  | Add a popup warning on invoice to ensure warning is populated
[account_mail_autosubscribe](account_mail_autosubscribe/) | 18.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Automatically subscribe partners to their company's invoices
[account_manual_currency](account_manual_currency/) | 18.0.1.0.0 |  | Allows to manual currency of Accounting
[account_move_auto_post_ref](account_move_auto_post_ref/) | 18.0.1.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Propagate customer ref when auto-generating next recurring invoice
[account_move_cancel_confirm](account_move_cancel_confirm/) | 18.0.1.0.1 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Account Move Cancel Confirm
[account_move_pivot_view](account_move_pivot_view/) | 18.0.1.0.0 |  | Adds pivot view to Invoices (move in and move out), Refunds, and Receipts
[account_move_tier_validation](account_move_tier_validation/) | 18.0.1.0.2 |  | Extends the functionality of Account Moves to support a tier validation process.
[account_move_tier_validation_approver](account_move_tier_validation_approver/) | 18.0.1.0.0 |  | Account Move Tier Validation Approver
[account_portal_invoice_search](account_portal_invoice_search/) | 18.0.1.0.0 |  | Account Portal Invoice Search
[account_receipt_journal](account_receipt_journal/) | 18.0.1.1.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Define and use journals dedicated to receipts
[account_receipt_send](account_receipt_send/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Send receipts
[account_tax_group_widget_base_amount](account_tax_group_widget_base_amount/) | 18.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Adds base amount to tax group widget
[account_tax_legal_notes_translate](account_tax_legal_notes_translate/) | 18.0.1.0.1 | <a href='https://github.com/SabrinaRMartin'><img src='https://github.com/SabrinaRMartin.png' width='32' height='32' style='border-radius:50%;' alt='SabrinaRMartin'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Agrega traducciones a las notas legales de los impuestos
[account_tax_one_vat](account_tax_one_vat/) | 18.0.1.0.0 |  | Allow only the selection of one VAT Tax.
[account_tax_one_vat_purchase](account_tax_one_vat_purchase/) | 18.0.1.0.0 |  | Allow only the selection of one VAT Tax in purchase order line
[account_tax_one_vat_sale](account_tax_one_vat_sale/) | 18.0.1.0.0 |  | Allow only the selection of one VAT Tax in purchase order line
[account_warn_option](account_warn_option/) | 18.0.1.0.2 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Add Options to Account Warn Messages
[partner_invoicing_mode](partner_invoicing_mode/) | 18.0.1.0.0 |  | Base module for handling multiple partner invoicing mode
[partner_invoicing_mode_at_shipping](partner_invoicing_mode_at_shipping/) | 18.0.1.0.2 |  | Create invoices automatically when goods are shipped.
[partner_invoicing_mode_monthly](partner_invoicing_mode_monthly/) | 18.0.1.0.0 |  | Create invoices automatically on a monthly basis.
[portal_account_personal_data_only](portal_account_personal_data_only/) | 18.0.1.0.0 |  | Portal Accounting Personal Data Only
[product_customerinfo_invoice](product_customerinfo_invoice/) | 18.0.1.0.0 |  | Based on product_customerinfo, this module loads in every account invoice the customer code defined in the product
[product_form_account_move_line_link](product_form_account_move_line_link/) | 18.0.1.0.0 |  | Adds a button on product forms to access Journal Items
[purchase_stock_picking_return_invoicing](purchase_stock_picking_return_invoicing/) | 18.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/MiquelRForgeFlow'><img src='https://github.com/MiquelRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='MiquelRForgeFlow'/></a> | Add an option to refund returned pickings
[sale_credit_note_reversal](sale_credit_note_reversal/) | 18.0.1.0.0 |  | Allow to revert a credit note
[sale_invoiceability_on_payment_transaction](sale_invoiceability_on_payment_transaction/) | 18.0.1.0.0 | <a href='https://github.com/cristina-hidalgo-tecnativa'><img src='https://github.com/cristina-hidalgo-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='cristina-hidalgo-tecnativa'/></a> <a href='https://github.com/carlos-lopez-tecnativa'><img src='https://github.com/carlos-lopez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carlos-lopez-tecnativa'/></a> | Allow invoicing sales orders when a done payment transaction exists.
[sale_invoicing_date_selection](sale_invoicing_date_selection/) | 18.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Set date invoice when you create invoices
[sale_line_refund_to_invoice_qty](sale_line_refund_to_invoice_qty/) | 18.0.1.0.1 |  | Allow deciding whether refunded quantity should be considered as quantity to reinvoice
[sale_order_invoicing_grouping_criteria](sale_order_invoicing_grouping_criteria/) | 18.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Sales order invoicing grouping criteria
[sale_order_invoicing_qty_percentage](sale_order_invoicing_qty_percentage/) | 18.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Sales order invoicing by percentage of the quantity
[sale_stock_picking_invoicing](sale_stock_picking_invoicing/) | 18.0.2.0.0 | <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Sales Stock Picking Invoicing
[stock_account_move_reset_to_draft](stock_account_move_reset_to_draft/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Stock account move reset to draft
[stock_picking_invoicing](stock_picking_invoicing/) | 18.0.2.0.1 |  | Stock Picking Invoicing
[stock_picking_return_refund_option](stock_picking_return_refund_option/) | 18.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Update the refund options in pickings

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/account-payment


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-payment&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/account-payment/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-payment/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/account-payment/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-payment/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/account-payment/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-payment)
[![Translation Status](https://translation.odoo-community.org/widgets/account-payment-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-payment-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-payment

account-payment

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_cash_invoice](account_cash_invoice/) | 18.0.1.0.0 |  | Pay and receive invoices from bank statements
[account_check_printing_report_base](account_check_printing_report_base/) | 18.0.1.0.1 |  | Account Check Printing Report Base
[account_due_list](account_due_list/) | 18.0.1.0.1 |  | List of open credits and debits, with due date
[account_due_list_payment_mode](account_due_list_payment_mode/) | 18.0.1.0.0 |  | Payment Due List Payment Mode
[account_force_early_discount](account_force_early_discount/) | 18.0.1.0.0 | <a href='https://github.com/grindtildeath'><img src='https://github.com/grindtildeath.png' width='32' height='32' style='border-radius:50%;' alt='grindtildeath'/></a> | Allow forcing financial discounts for early payments
[account_move_line_payment](account_move_line_payment/) | 18.0.1.0.0 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Register only due payments
[account_payment_credit_card](account_payment_credit_card/) | 18.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Add support for credit card payments
[account_payment_line](account_payment_line/) | 18.0.1.0.2 | <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | Payment Counterpart Lines
[account_payment_method_base](account_payment_method_base/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add form and list view for account.payment.method
[account_payment_multi_deduction](account_payment_multi_deduction/) | 18.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Payment Register with Multiple Deduction
[account_payment_notification](account_payment_notification/) | 18.0.1.0.1 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Notifiy upcoming payments
[account_payment_promissory_note](account_payment_promissory_note/) | 18.0.1.0.1 |  | Account Payment Promissory Note
[account_payment_return](account_payment_return/) | 18.0.1.0.9 |  | Manage the return of your payments
[account_payment_return_import](account_payment_return_import/) | 18.0.1.0.1 |  | This module adds a generic wizard to import payment returnfile formats. Is only the base to be extended by anothermodules
[account_payment_return_import_iso20022](account_payment_return_import_iso20022/) | 18.0.1.1.1 |  | This addon allows to import payment returns from ISO 20022 files like PAIN or CAMT.
[account_payment_show_invoice](account_payment_show_invoice/) | 18.0.1.0.0 |  | Extends the tree view of payments to show the paid invoices related to the payments using the vendor reference by default
[account_payment_term_extension](account_payment_term_extension/) | 18.0.1.0.1 |  | Adds rounding, months, weeks and multiple payment days properties on payment term lines
[account_payment_tier_validation](account_payment_tier_validation/) | 18.0.1.0.1 |  | Extends the functionality of Payment to support a tier validation process.
[account_payment_widget_amount](account_payment_widget_amount/) | 18.0.1.0.0 |  | Extends the payment widget to be able to choose the payment amount
[account_refund_early_payment_discount](account_refund_early_payment_discount/) | 18.0.1.0.0 | <a href='https://github.com/grindtildeath'><img src='https://github.com/grindtildeath.png' width='32' height='32' style='border-radius:50%;' alt='grindtildeath'/></a> | Suppoprt early payment discount on credit notes
[account_voucher_killer](account_voucher_killer/) | 18.0.1.0.0 |  | Prevent the usage of payments from invoices
[partner_aging](partner_aging/) | 18.0.1.0.0 | <a href='https://github.com/Urvisha-OSI'><img src='https://github.com/Urvisha-OSI.png' width='32' height='32' style='border-radius:50%;' alt='Urvisha-OSI'/></a> | Aging as a view - invoices and credits
[payment_partner](payment_partner/) | 18.0.1.0.0 |  | Filter Payments by Partner

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/account-reconcile


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-reconcile&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/account-reconcile/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-reconcile/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/account-reconcile/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/account-reconcile/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/account-reconcile/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-reconcile)
[![Translation Status](https://translation.odoo-community.org/widgets/account-reconcile-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-reconcile-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-reconcile

account-reconcile

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_in_payment](account_in_payment/) | 18.0.1.0.0 |  | This module enables in-payment mode for your accounting
[account_move_base_import](account_move_base_import/) | 18.0.1.0.3 |  | Journal Entry base import
[account_move_reconcile_forbid_cancel](account_move_reconcile_forbid_cancel/) | 18.0.1.0.0 |  | Account Move Reconcile Forbid Cancel
[account_move_reconcile_helper](account_move_reconcile_helper/) | 18.0.1.0.0 |  | Provides tools to facilitate reconciliation
[account_partner_reconcile](account_partner_reconcile/) | 18.0.1.0.0 |  | Account Partner Reconcile
[account_reconcile_analytic_tag](account_reconcile_analytic_tag/) | 18.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Analytic tags in account reconciliation
[account_reconcile_model_oca](account_reconcile_model_oca/) | 18.0.1.1.3 |  | This includes the logic moved from Odoo Community to Odoo Enterprise
[account_reconcile_oca](account_reconcile_oca/) | 18.0.1.1.8 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Reconcile addons for Odoo CE accounting
[account_reconcile_oca_add_default_filters](account_reconcile_oca_add_default_filters/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add default filters in Reconcile tab when the bank statement line has a partner
[account_reconcile_oca_queue](account_reconcile_oca_queue/) | 18.0.1.1.0 |  | Auto-reconcile in queue jobs
[account_reconcile_restrict_partner_mismatch](account_reconcile_restrict_partner_mismatch/) | 18.0.1.0.0 |  | Restrict reconciliation on receivable and payable accounts to the same partner
[account_reconcile_sale_order](account_reconcile_sale_order/) | 18.0.1.0.1 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Invoice and reconcile sales orders
[account_reconcile_wizard](account_reconcile_wizard/) | 18.0.1.0.0 | <a href='https://github.com/carlos-lopez-tecnativa'><img src='https://github.com/carlos-lopez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carlos-lopez-tecnativa'/></a> | Account Reconcile from Wizard
[account_statement_base](account_statement_base/) | 18.0.1.3.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Base module for Bank Statements
[account_statement_reconcile_status](account_statement_reconcile_status/) | 18.0.1.0.0 |  | Show reconciliation status on bank statements
[base_transaction_id](base_transaction_id/) | 18.0.1.0.0 |  | Base transaction ID for financial institutes

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/agreement


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/agreement&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/agreement/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/agreement/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/agreement/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/agreement/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/agreement/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/agreement)
[![Translation Status](https://translation.odoo-community.org/widgets/agreement-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/agreement-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Agreement

Manage agreements and contracts

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[agreement](agreement/) | 18.0.1.2.0 | <a href='https://github.com/ygol'><img src='https://github.com/ygol.png' width='32' height='32' style='border-radius:50%;' alt='ygol'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adds an agreement object
[agreement_account](agreement_account/) | 18.0.1.0.2 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Agreement on invoices
[agreement_helpdesk_mgmt](agreement_helpdesk_mgmt/) | 18.0.1.0.0 | <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> | Link a helpdesk ticket to an agreement
[agreement_helpdesk_mgmt_fieldservice](agreement_helpdesk_mgmt_fieldservice/) | 18.0.1.0.0 |  | Agreement Helpdesk Mgmt Fieldservice
[agreement_helpdesk_mgmt_sale](agreement_helpdesk_mgmt_sale/) | 18.0.1.0.0 |  | Agreement Helpdesk Mgmt Sale
[agreement_helpdesk_mgmt_serviceprofile](agreement_helpdesk_mgmt_serviceprofile/) | 18.0.1.0.0 | <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> | Agreement Helpdesk Mgmt
[agreement_legal](agreement_legal/) | 18.0.1.1.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/ygol'><img src='https://github.com/ygol.png' width='32' height='32' style='border-radius:50%;' alt='ygol'/></a> | Manage Agreements, LOI and Contracts
[agreement_project](agreement_project/) | 18.0.1.0.0 | <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> <a href='https://github.com/ygol'><img src='https://github.com/ygol.png' width='32' height='32' style='border-radius:50%;' alt='ygol'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Link projects to an agreement
[agreement_rebate](agreement_rebate/) | 18.0.1.2.1 |  | Rebate in agreements
[agreement_repair](agreement_repair/) | 18.0.1.0.0 | <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Link repair orders to an agreement
[agreement_sale](agreement_sale/) | 18.0.1.0.3 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Agreement on sales
[agreement_serviceprofile](agreement_serviceprofile/) | 18.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Adds an Agreement Service Profile object

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/ai


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# ai
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/ai&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/ai/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/ai/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/ai/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/ai/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/ai/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/ai)
[![Translation Status](https://translation.odoo-community.org/widgets/ai-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/ai-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

ai

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[ai_oca_bridge](ai_oca_bridge/) | 18.0.2.0.1 |  | Makes a basic configuration to be used as bridge with external AI systems
[ai_oca_bridge_chatter](ai_oca_bridge_chatter/) | 18.0.2.0.0 |  | Integrate a Bridge with a user that will use it on chatter
[ai_oca_bridge_document_page](ai_oca_bridge_document_page/) | 18.0.1.0.0 |  | Adds Documents synchronization using AI Bridges
[ai_oca_bridge_extra_parameters](ai_oca_bridge_extra_parameters/) | 18.0.1.0.0 | <a href='https://github.com/arielbarreiros96'><img src='https://github.com/arielbarreiros96.png' width='32' height='32' style='border-radius:50%;' alt='arielbarreiros96'/></a> | Adds extra parameters to the AI OCA Bridge payload.
[ai_oca_native_generate_ollama](ai_oca_native_generate_ollama/) | 18.0.1.0.0 |  | This module replaces AI from html_editor to use an Ollama server instead of OpenAI through Odoo IAP.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/automation


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# automation
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/automation&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/automation/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/automation/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/automation/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/automation/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/automation/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/automation)
[![Translation Status](https://translation.odoo-community.org/widgets/automation-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/automation-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

automation

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[automation_oca](automation_oca/) | 18.0.1.0.4 |  | Automate actions in threaded models

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/bank-payment


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/bank-payment&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/bank-payment/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/bank-payment/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/bank-payment/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/bank-payment/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/bank-payment/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/bank-payment)
[![Translation Status](https://translation.odoo-community.org/widgets/bank-payment-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/bank-payment-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# bank-payment

bank-payment

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_banking_mandate](account_banking_mandate/) | 18.0.1.2.1 |  | Banking mandates
[account_banking_mandate_contact](account_banking_mandate_contact/) | 18.0.1.2.1 |  | Assign specific banking mandates in contact level
[account_banking_mandate_sale](account_banking_mandate_sale/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adds mandates on sale orders
[account_banking_mandate_sale_contact](account_banking_mandate_sale_contact/) | 18.0.1.0.1 | <a href='https://github.com/tisho99'><img src='https://github.com/tisho99.png' width='32' height='32' style='border-radius:50%;' alt='tisho99'/></a> | Add a specific contact mandate to sale orders
[account_banking_pain_base](account_banking_pain_base/) | 18.0.1.2.0 |  | Base module for PAIN file generation
[account_banking_sepa_credit_transfer](account_banking_sepa_credit_transfer/) | 18.0.1.1.1 |  | Create SEPA XML files for Credit Transfers
[account_banking_sepa_direct_debit](account_banking_sepa_direct_debit/) | 18.0.1.1.1 |  | Create SEPA files for Direct Debit
[account_invoice_select_for_payment](account_invoice_select_for_payment/) | 18.0.1.0.0 |  | Account Invoice Select for Payment
[account_payment_method_base_mode](account_payment_method_base_mode/) | 18.0.1.0.0 |  | Glue module for base views
[account_payment_mode](account_payment_mode/) | 18.0.1.0.2 |  | Account Payment Mode
[account_payment_order](account_payment_order/) | 18.0.1.2.5 |  | Account Payment Order
[account_payment_order_grouped_output](account_payment_order_grouped_output/) | 18.0.1.0.1 |  | Account Payment Order - Generate grouped moves
[account_payment_order_notification](account_payment_order_notification/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Account Payment Order Notification
[account_payment_order_return](account_payment_order_return/) | 18.0.1.0.0 |  | Account Payment Order Return
[account_payment_order_tier_validation](account_payment_order_tier_validation/) | 18.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Extends the functionality of Payment Orders to support a tier validation process.
[account_payment_partner](account_payment_partner/) | 18.0.1.0.5 |  | Adds payment mode on partners and invoices
[account_payment_purchase](account_payment_purchase/) | 18.0.1.0.1 |  | Adds Bank Account and Payment Mode on Purchase Orders
[account_payment_purchase_stock](account_payment_purchase_stock/) | 18.0.1.0.0 |  | Integrate Account Payment Purchase with Stock
[account_payment_sale](account_payment_sale/) | 18.0.1.0.2 |  | Adds payment mode on sale orders
[account_vendor_bank_account_default](account_vendor_bank_account_default/) | 18.0.1.0.1 | <a href='https://github.com/tisho99'><img src='https://github.com/tisho99.png' width='32' height='32' style='border-radius:50%;' alt='tisho99'/></a> | Set a default bank account on partners for their vendor bills
[account_vendor_bank_account_default_purchase](account_vendor_bank_account_default_purchase/) | 18.0.1.0.0 | <a href='https://github.com/tisho99'><img src='https://github.com/tisho99.png' width='32' height='32' style='border-radius:50%;' alt='tisho99'/></a> | Set a default bank account purchase orders

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/bank-payment-alternative


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/bank-payment-alternative&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/bank-payment-alternative/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/bank-payment-alternative/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/bank-payment-alternative/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/bank-payment-alternative/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/bank-payment-alternative/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/bank-payment-alternative)
[![Translation Status](https://translation.odoo-community.org/widgets/bank-payment-alternative-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/bank-payment-alternative-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Bank Payment - Alternative approach based on Odoo native payment methods

This projet is, as its name suggests, an alternative to the [OCA bank-payment project](https://github.com/OCA/bank-payment). The code of the 18.0 branch of OCA/bank-payment-alternative originates from [pull request 1174](https://github.com/OCA/bank-payment/pull/1174) entitled **Large refactoring/improvement/cleanup of OCA/bank-payment** for 16.0 by Alexis de Lattre (Akretion). As a consequence, the code of the 18.0 branch of OCA/bank-payment-alternative doesn't contain some of the changes/improvements made in the 16.0 branch after commit [da11fcfd1de2072906a170adc21d2b0cc78c9638](https://github.com/OCA/bank-payment/commit/da11fcfd1de2072906a170adc21d2b0cc78c9638), in 17.0 and 18.0 branches of OCA/bank-payment.

In Odoo 18.0, three new fields were added in the **account** module: two fields on res.partner for *Customer Payment Method* and *Supplier Payment Method* and a field *Payment Method* on invoices. These 3 new fields are *many2one* fields that point to *account.payment.method.line*. These fields are redunant with the equivalent fields definied in the OCA module *account_payment_partner* of the project OCA/bank-payment that point to *account.payment.mode* which is defined in the OCA module *account_payment_mode* from OCA/bank-payment.

On 18.0, the project OCA/bank-payment continues to use the object *account.payment.mode* and, by default, hides the 3 equivalent fields of the **account** module that point to *account.payment.method.line*.

On the contrary, the project [OCA/bank-payment-alternative](https://github.com/OCA/bank-payment-alternative) made the changes in the code base to fully adopt the three new *Payment Method* fields added in the **account** module in Odoo 18.0.

In Odoo 19.0, Odoo added a *many2one* field that point to *account.payment.method.line* on sale orders.

According to the [draft pull request 207284](https://github.com/odoo/odoo/pull/207284) on odoo master branch, Odoo plans to merge the object *account.payment.method.line* into the object *account.payment.method*. The project OCA/bank-payment-alternative plans to follow the evolution of the native datamodel in future versions of Odoo.

In the project OCA/bank-payment-alternative, the modules had to be renamed. In the table below, you will find the correspondance between the modules names of OCA/bank-payment and OCA/bank-payment-alternative:

OCA/bank-payment | OCA/bank-payment-alternative
--- | ---
account_payment_mode | *native* + account_payment_base_oca
account_payment_partner | *native*
account_payment_sale | account_payment_base_oca_sale
account_payment_order | account_payment_batch_oca
account_payment_order_tier_validation | account_payment_batch_oca_tier_validation
account_banking_pain_base | account_payment_sepa_base
account_banking_sepa_credit_transfer | account_payment_sepa_credit_transfer
account_banking_mandate | account_payment_mandate
account_banking_mandate_sale | account_payment_mandate_sale
account_banking_sepa_direct_debit | account_payment_sepa_direct_debit

If a developer wants to update an existing OCA module and make it depend on OCA/bank-payment-alternative instead of OCA/bank-payment, the developer should rename the module. That way, the module can continue to evolve under its original name with the dependency on OCA/bank-payment.

For example, in OCA/l10n-france, there is a module named **account_banking_fr_lcr** since 8.0 that adds support for French Letter of Change. This module used to depend on account_payment_order from OCA/bank-payment up to 17.0. An OCA developper migrated this module to 18.0 and switched its dependecy from account_payment_order from OCA/bank-payment to account_payment_batch_oca from OCA/bank-payment-alternative ; he renamed the module to **account_payment_fr_lcr**. That way, the development of the module **account_banking_fr_lcr** can continue with the dependency on account_payment_order from OCA/bank-payment on 18.0 and upper versions.

The project OCA/bank-payment-alternative also introduced several new features and improvements, listed below by order of importance :

* Introduce a new object for payment lots *account.payment.lot* which is used to ease the generation of SCT and SDD XML files. This object is also used in the bank statement reconcile interface, to make it easy for the user to reconcile bank statement lines that correspond to a payment lot (module account_payment_batch_oca_reconcile).
* Take into account the boolean field *allow_out_payment* of res.partner.bank on payment orders: when you try to confirm a payment order that has bank accounts on payment lines with *allow_out_payment = False*, the user gets a blocking error message. The affected payment lines will be shown in red and the user will have a smart button that gives access to the bank accounts that are not allowed to send money to. To enable *allow_out_payment*, the user needs to be part of a specific group *Validate bank accounts* (XMLID *account.group_validate_bank_account*). As a consequence, the native ACL of *res.partner.bank* that give full rights to partner manager is not inherited any more: the security is handled by the boolean field *allow_out_payment*.
* the datamodel of the mandate has been simplified: the field *format* also has the information of the *scheme* field, so *format* now has 3 possible values : *basic*, *sepa_core* or *sepa_b2b*. The field *scheme* has been removed. The field *type* has 2 possible values: *recurrent* or *oneoff* (instead of 3 possible values : *generic*, *recurrent* or *oneoff*). The field *recurrent_sequence_type* has been removed because we don't need to handle the *first* vs *recurring* sequence any more : since November 2016, *the requirement to use the sequence type 'First' in a first of a recurrent series of Collections is no longer mandatory* according to the [EPC](https://www.europeanpaymentscouncil.eu/), cf SDD Core Rulebook. The *final* sequence is now supported by the state field which has a new *final* state that can be activated via a button. The field *partner_id* is NOT a related field of *partner_bank_id* any more, which solves the bug [account_banking_mandate: Change in the filtering behavior of the "Bank Account" field](https://github.com/OCA/bank-payment/issues/1473). With all these simplifications on the mandate datamodel, the form view and list view of mandates are more user-friendly.
* by default, there is a sequence for payment orders and another sequence for debit orders. It is possible to configure a specific sequence for a payment method.
* add support for *Regulatory Reporting* in the SEPA XML structure (tag *RgltryRptg*). Needed in some countries for international non-SEPA credit transfers.
* replace unstructured address by structured address in SEPA XML file (mandatory starting november 2025 according to the EPC).
* add support for pain.008.01.08 (SDD) and pain.001.001.09 (SCT), which are now the recommended versions of the EPC.
* easier download of the banking file after generation.
* add field *acc_number_scrambled* on res.partner.bank for easy and direct use of scrambled account number.
* search on partner from payment/debit orders search view.
* support currencies with *decimal_places* != 2 in ISO20022 XML file generation
* on mandates, fields *format*, *type*, *signature date* and *partner* become readonly when the mandate is not in *draft* state
* remove support for pain.001.001.02/04/05 (SCT) and pain.008.01.03/04 (SDD) which have never been selected by the EPC, in order to simplify the code that generate the XML.
* stop using *safe_eval()* in XML generation.
* replace all @api.onchange by computed fields.
* add sql unicity constraint on payment order number per company.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_payment_base_oca](account_payment_base_oca/) | 18.0.1.6.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | OCA extensions to native payment objects of Odoo
[account_payment_base_oca_sale](account_payment_base_oca_sale/) | 18.0.2.0.0 |  | Adds payment method on sale orders
[account_payment_batch_oca](account_payment_batch_oca/) | 18.0.3.4.0 |  | Add payment orders and debit orders
[account_payment_batch_oca_reconcile](account_payment_batch_oca_reconcile/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Easy reconciliation of payment/debit lots on bank statement reconcile interface
[account_payment_batch_oca_tier_validation](account_payment_batch_oca_tier_validation/) | 18.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Tier validation process on payment/debit orders
[account_payment_mandate](account_payment_mandate/) | 18.0.2.1.0 |  | Add support for banking mandates used in direct debits
[account_payment_mandate_sale](account_payment_mandate_sale/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adds mandates on sale orders
[account_payment_sepa_base](account_payment_sepa_base/) | 18.0.3.0.0 |  | Base module for SEPA file generation
[account_payment_sepa_credit_transfer](account_payment_sepa_credit_transfer/) | 18.0.3.0.1 |  | Create SEPA XML files for Credit Transfers
[account_payment_sepa_direct_debit](account_payment_sepa_direct_debit/) | 18.0.3.0.0 |  | Create SEPA files for Direct Debit

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/bank-statement-import


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/bank-statement-import&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/bank-statement-import/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/bank-statement-import/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/bank-statement-import/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/bank-statement-import/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/bank-statement-import/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/bank-statement-import)
[![Translation Status](https://translation.odoo-community.org/widgets/bank-statement-import-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/bank-statement-import-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# bank-statement-import

bank-statement-import

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_statement_import_base](account_statement_import_base/) | 18.0.1.0.2 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Base module for Bank Statement Import
[account_statement_import_camt](account_statement_import_camt/) | 18.0.1.0.1 |  | CAMT Format Bank Statements Import
[account_statement_import_camt54](account_statement_import_camt54/) | 18.0.1.0.0 |  | Bank Account Camt54 Import
[account_statement_import_file](account_statement_import_file/) | 18.0.1.0.2 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import Statement Files
[account_statement_import_file_reconcile_oca](account_statement_import_file_reconcile_oca/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import Statement Files and Go Direct to Reconciliation
[account_statement_import_move_line](account_statement_import_move_line/) | 18.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Import journal items into bank statement
[account_statement_import_ofx](account_statement_import_ofx/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import OFX Bank Statement
[account_statement_import_ofx_by_acctid](account_statement_import_ofx_by_acctid/) | 18.0.1.0.0 |  | Import OFX Bank Statement by ACCTID
[account_statement_import_online](account_statement_import_online/) | 18.0.1.1.2 | <a href='https://github.com/alexey-pelykh'><img src='https://github.com/alexey-pelykh.png' width='32' height='32' style='border-radius:50%;' alt='alexey-pelykh'/></a> | Online bank statements update
[account_statement_import_online_gocardless](account_statement_import_online_gocardless/) | 18.0.1.0.0 |  | Online Bank Statements: GoCardless
[account_statement_import_online_paypal](account_statement_import_online_paypal/) | 18.0.1.0.3 | <a href='https://github.com/alexey-pelykh'><img src='https://github.com/alexey-pelykh.png' width='32' height='32' style='border-radius:50%;' alt='alexey-pelykh'/></a> | Online bank statements for PayPal.com
[account_statement_import_online_plaid](account_statement_import_online_plaid/) | 18.0.1.0.0 |  | Online Bank Statements: plaid.com
[account_statement_import_online_ponto](account_statement_import_online_ponto/) | 18.0.1.0.1 |  | Online Bank Statements: MyPonto.com
[account_statement_import_online_stripe](account_statement_import_online_stripe/) | 18.0.1.0.1 | <a href='https://github.com/juancarlosonate-tecnativa'><img src='https://github.com/juancarlosonate-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='juancarlosonate-tecnativa'/></a> | Online bank statements for Stripe
[account_statement_import_online_wise](account_statement_import_online_wise/) | 18.0.1.1.0 | <a href='https://github.com/alexey-pelykh'><img src='https://github.com/alexey-pelykh.png' width='32' height='32' style='border-radius:50%;' alt='alexey-pelykh'/></a> | Online bank statements for Wise.com
[account_statement_import_sheet_file](account_statement_import_sheet_file/) | 18.0.1.1.0 | <a href='https://github.com/alexey-pelykh'><img src='https://github.com/alexey-pelykh.png' width='32' height='32' style='border-radius:50%;' alt='alexey-pelykh'/></a> | Import TXT/CSV or XLSX files as Bank Statements in Odoo
[account_statement_line_order](account_statement_line_order/) | 18.0.1.0.0 |  | Adds ordering option on bank statement lines

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/brand


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/brand&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/brand/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/brand/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/brand/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/brand/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/brand/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/brand)
[![Translation Status](https://translation.odoo-community.org/widgets/brand-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/brand-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# brand

brand

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_analytic_brand](account_analytic_brand/) | 18.0.2.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This module allows to propagate analytic distribution from branded analytic distribution models on account moves
[account_brand](account_brand/) | 18.0.1.0.1 | <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Send branded invoices and refunds
[account_invoice_bank_brand](account_invoice_bank_brand/) | 18.0.1.0.0 |  | Enables the automatic selection of the partner'sbank account on invoices based on the brand.
[account_payment_mode_brand](account_payment_mode_brand/) | 18.0.1.0.0 |  | This addon define allowed payment mode per brand
[analytic_brand](analytic_brand/) | 18.0.3.0.1 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This addon allows to define analytic distribution models using brands in their domains.
[brand](brand/) | 18.0.1.0.3 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This is a base addon for brand modules. It adds the brand object and its menu and define an abstract model to be inherited from branded objects
[brand_external_report_layout](brand_external_report_layout/) | 18.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This module allows you to have a different layout by brand for your external reports.
[contract_brand](contract_brand/) | 18.0.2.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This module allows you to manage branded contracts. It adds a brand field on the contract and propagate the value on the invoices.
[contract_forecast_brand](contract_forecast_brand/) | 18.0.1.0.0 |  | This addon add brand field for contract forecast
[contract_payment_mode_brand](contract_payment_mode_brand/) | 18.0.1.0.0 |  | This addon limits payment mode selection in contract to the brand's allowed.
[mail_brand](mail_brand/) | 18.0.1.0.0 | <a href='https://github.com/switch87'><img src='https://github.com/switch87.png' width='32' height='32' style='border-radius:50%;' alt='switch87'/></a> <a href='https://github.com/bosd'><img src='https://github.com/bosd.png' width='32' height='32' style='border-radius:50%;' alt='bosd'/></a> | If a model has a brand defined to it, emails send from this model will be branded accordingly.
[partner_brand](partner_brand/) | 18.0.1.0.2 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Define registered mark in partners according to brand settings
[product_brand](product_brand/) | 18.0.1.1.0 |  | Product Brand Manager
[product_brand_mrp](product_brand_mrp/) | 18.0.1.0.0 |  | This module allows to work with product_brand in MRP.
[product_brand_purchase](product_brand_purchase/) | 18.0.1.0.0 |  | This module allows to work with product_brand in purchase reports.
[product_brand_stock](product_brand_stock/) | 18.0.1.0.0 |  | This module allows to work with product_brand in Stock.
[product_brand_stock_account](product_brand_stock_account/) | 18.0.1.0.0 |  | This module allows to work with product_brand in Stock Account.
[product_brand_tag](product_brand_tag/) | 18.0.1.0.0 |  | Add tags to product brand
[product_contract_brand](product_contract_brand/) | 18.0.1.0.0 |  | This addon propagate the brand from sale order to contract
[sale_analytic_brand](sale_analytic_brand/) | 18.0.2.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This module allows to propagate analytic distribution from branded analytic distribution models on sale order lines
[sale_brand](sale_brand/) | 18.0.1.0.0 | <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Send branded sales orders
[sale_payment_mode_brand](sale_payment_mode_brand/) | 18.0.1.0.0 |  | This addon limit payment mode selection on sale order to the brand allowed payment modes.
[stock_brand](stock_brand/) | 18.0.1.0.0 |  | Manage brands on stock picking documents
[stock_picking_partner_brand](stock_picking_partner_brand/) | 18.0.1.0.0 | <a href='https://github.com/bosd'><img src='https://github.com/bosd.png' width='32' height='32' style='border-radius:50%;' alt='bosd'/></a> | Automatically sets the brand on a Stock Picking based on the selected partner's brand.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/calendar


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# calendar
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/calendar&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/calendar/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/calendar/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/calendar/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/calendar/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/calendar/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/calendar)
[![Translation Status](https://translation.odoo-community.org/widgets/calendar-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/calendar-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

calendar

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[calendar_event_type_color](calendar_event_type_color/) | 18.0.1.0.0 | <a href='https://github.com/yankinmax'><img src='https://github.com/yankinmax.png' width='32' height='32' style='border-radius:50%;' alt='yankinmax'/></a> | Colorize calendar view depending on event type color
[calendar_export_ics](calendar_export_ics/) | 18.0.1.0.1 |  | Allow exporting odoo calendar to an ics file
[calendar_import_ics](calendar_import_ics/) | 18.0.1.0.1 |  | Allow importing an ics file to our calendar
[calendar_public_holiday](calendar_public_holiday/) | 18.0.1.0.1 |  | Manage Public Holidays
[resource_booking](resource_booking/) | 18.0.1.0.14 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/ows-cloud'><img src='https://github.com/ows-cloud.png' width='32' height='32' style='border-radius:50%;' alt='ows-cloud'/></a> | Manage appointments and resource booking

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/commission


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/commission&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/commission/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/commission/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/commission/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/commission/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/commission/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/commission)
[![Translation Status](https://translation.odoo-community.org/widgets/commission-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/commission-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# commission

commission

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_commission_oca](account_commission_oca/) | 18.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Account commissions OCA
[commission_formula_oca](commission_formula_oca/) | 18.0.1.0.0 |  | Commissions computed by formulas
[commission_oca](commission_oca/) | 18.0.1.0.3 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Commissions OCA
[hr_commission_oca](hr_commission_oca/) | 18.0.1.0.0 |  | HR commissions OCA
[sale_commission_oca](sale_commission_oca/) | 18.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Sales commissions OCA
[sale_commission_oca_product_criteria](sale_commission_oca_product_criteria/) | 18.0.1.0.0 | <a href='https://github.com/ilyasProgrammer'><img src='https://github.com/ilyasProgrammer.png' width='32' height='32' style='border-radius:50%;' alt='ilyasProgrammer'/></a> <a href='https://github.com/aleuffre'><img src='https://github.com/aleuffre.png' width='32' height='32' style='border-radius:50%;' alt='aleuffre'/></a> <a href='https://github.com/renda-dev'><img src='https://github.com/renda-dev.png' width='32' height='32' style='border-radius:50%;' alt='renda-dev'/></a> <a href='https://github.com/PicchiSeba'><img src='https://github.com/PicchiSeba.png' width='32' height='32' style='border-radius:50%;' alt='PicchiSeba'/></a> | Advanced commissions rules
[sale_commission_oca_product_criteria_semaphore](sale_commission_oca_product_criteria_semaphore/) | 18.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Add semaphore for advanced commissions rules
[sale_commission_pricelist_oca](sale_commission_pricelist_oca/) | 18.0.1.0.0 |  | Sales commissions by pricelist OCA
[sale_commission_salesman](sale_commission_salesman/) | 18.0.1.0.0 |  | Sales commissions from salesman

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/community-data-files


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/community-data-files&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/community-data-files/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/community-data-files/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/community-data-files/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/community-data-files/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/community-data-files/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/community-data-files)
[![Translation Status](https://translation.odoo-community.org/widgets/community-data-files-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/community-data-files-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# community-data-files

community-data-files

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_payment_unece](account_payment_unece/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | UNECE nomenclature for the payment methods
[account_tax_unece](account_tax_unece/) | 18.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | UNECE nomenclature for taxes
[base_bank_from_iban](base_bank_from_iban/) | 18.0.1.0.1 |  | Bank from IBAN
[base_iso3166](base_iso3166/) | 18.0.1.0.0 |  | ISO 3166
[base_unece](base_unece/) | 18.0.1.0.0 | <a href='https://github.com/astirpe'><img src='https://github.com/astirpe.png' width='32' height='32' style='border-radius:50%;' alt='astirpe'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Base module for UNECE code lists
[company_sanitary_registry](company_sanitary_registry/) | 18.0.1.2.0 |  | Sanitary Registry
[l10n_eu_nace](l10n_eu_nace/) | 18.0.1.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | European NACE partner categories
[l10n_eu_product_adr](l10n_eu_product_adr/) | 18.0.1.0.1 |  | Allows to set appropriate danger class and components
[l10n_eu_product_adr_dangerous_goods](l10n_eu_product_adr_dangerous_goods/) | 18.0.1.0.0 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | l10n Eu Product Adr Dangerous Goods
[product_allergen](product_allergen/) | 18.0.1.0.0 |  | Add allergen information to products
[product_fao_fishing](product_fao_fishing/) | 18.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Set fishing areas and capture technology
[uom_unece](uom_unece/) | 18.0.1.0.0 | <a href='https://github.com/astirpe'><img src='https://github.com/astirpe.png' width='32' height='32' style='border-radius:50%;' alt='astirpe'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | UNECE nomenclature for the units of measure

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/connector


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/connector&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/connector/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/connector/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/connector/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/connector/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/connector/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/connector)
[![Translation Status](https://translation.odoo-community.org/widgets/connector-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/connector-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# connector

connector

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[component](component/) | 18.0.1.0.3 | <a href='https://github.com/guewen'><img src='https://github.com/guewen.png' width='32' height='32' style='border-radius:50%;' alt='guewen'/></a> | Add capabilities to register and use decoupled components, as an alternative to model classes
[component_event](component_event/) | 18.0.1.0.0 |  | Components Events
[connector](connector/) | 18.0.1.0.1 |  | Connector
[connector_base_product](connector_base_product/) | 18.0.1.0.0 |  | Connector Base Product
[test_component](test_component/) | 18.0.1.0.0 | <a href='https://github.com/guewen'><img src='https://github.com/guewen.png' width='32' height='32' style='border-radius:50%;' alt='guewen'/></a> | Automated tests for Components, do not install.
[test_connector](test_connector/) | 18.0.1.0.0 |  | Automated tests for Connector, do not install.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/connector-interfaces


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/connector-interfaces&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/connector-interfaces/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/connector-interfaces/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/connector-interfaces/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/connector-interfaces/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/connector-interfaces/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/connector-interfaces)
[![Translation Status](https://translation.odoo-community.org/widgets/connector-interfaces-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/connector-interfaces-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# connector-interfaces

connector-interfaces

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[connector_importer](connector_importer/) | 18.0.1.2.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | This module takes care of import sessions.
[connector_importer_product](connector_importer_product/) | 18.0.1.0.1 |  | Ease definition of product imports using `connector_importer`.
[connector_importer_source_sftp](connector_importer_source_sftp/) | 18.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Add import source capable of loading files from SFTP.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/connector-telephony


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# connector-telephony
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/connector-telephony&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/connector-telephony/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/connector-telephony/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/connector-telephony/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/connector-telephony/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/connector-telephony/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/connector-telephony)
[![Translation Status](https://translation.odoo-community.org/widgets/connector-telephony-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/connector-telephony-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

connector-telephony

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_phone](base_phone/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Validate phone numbers
[voip_oca](voip_oca/) | 18.0.1.0.3 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Provides the use of Voip

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/contract


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# contract
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/contract&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/contract/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/contract/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/contract/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/contract/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/contract/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/contract)
[![Translation Status](https://translation.odoo-community.org/widgets/contract-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/contract-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

contract

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[agreement_rebate_partner_company_group](agreement_rebate_partner_company_group/) | 18.0.1.0.0 |  | Rebate agreements applied to all company group members
[contract](contract/) | 18.0.2.4.1 |  | Recurring - Contracts Management
[contract_analytic_tag](contract_analytic_tag/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Contract Analytic Tag
[contract_forecast](contract_forecast/) | 18.0.1.0.1 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Contract Forecast
[contract_forecast_variable_quantity](contract_forecast_variable_quantity/) | 18.0.1.0.0 |  | Contract Forecast Variable Quantity
[contract_invoice_auto_validate](contract_invoice_auto_validate/) | 18.0.1.0.1 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This addon auto-validate invoices after its creation from a contract
[contract_invoice_manually](contract_invoice_manually/) | 18.0.1.0.0 |  | Option on contracts to invoice them manually
[contract_invoice_start_end_dates](contract_invoice_start_end_dates/) | 18.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Contract Invoice Start End Dates
[contract_line_successor](contract_line_successor/) | 18.0.1.0.1 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Contract Line Successor
[contract_mandate](contract_mandate/) | 18.0.1.0.0 |  | Mandate in contracts and their invoices
[contract_payment_mode](contract_payment_mode/) | 18.0.1.0.0 |  | Payment mode in contracts and their invoices
[contract_price_revision](contract_price_revision/) | 18.0.1.0.0 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> | Easy revision of contract prices
[contract_queue_job](contract_queue_job/) | 18.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> <a href='https://github.com/BurkhalterY'><img src='https://github.com/BurkhalterY.png' width='32' height='32' style='border-radius:50%;' alt='BurkhalterY'/></a> | This addon make contract invoicing cron plan each contract in a job instead of creating all invoices in one transaction
[contract_refund_on_stop](contract_refund_on_stop/) | 18.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Contract Refund On Stop
[contract_sale](contract_sale/) | 18.0.1.0.0 |  | Contract from Sale
[contract_sale_generation](contract_sale_generation/) | 18.0.1.0.2 |  | Contracts Management - Recurring Sales
[contract_sale_invoicing](contract_sale_invoicing/) | 18.0.1.1.0 |  | Include sales to invoice in contract invoice creation
[contract_sale_mandate](contract_sale_mandate/) | 18.0.1.0.0 |  | This module manages the banking mandate from the sale order to the contract.
[contract_sale_payment_mode](contract_sale_payment_mode/) | 18.0.1.0.0 |  | This addon manages payment mode from sale order to contract.
[contract_sale_transmit_method](contract_sale_transmit_method/) | 18.0.1.0.0 |  | Propagate transmit method (email, post, portal, ...) from sale orders to contracts.
[contract_termination](contract_termination/) | 18.0.1.0.0 |  | contract_termination
[contract_transmit_method](contract_transmit_method/) | 18.0.1.1.0 |  | Set transmit method (email, post, portal, ...) in contracts and propagate it to invoices.
[contract_update_last_date_invoiced](contract_update_last_date_invoiced/) | 18.0.1.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> | This module allows to update the last date invoiced if invoices are deleted.
[contract_variable_qty_prorated](contract_variable_qty_prorated/) | 18.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Contract Variable Qty Prorated
[contract_variable_qty_timesheet](contract_variable_qty_timesheet/) | 18.0.1.0.0 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/danypr92'><img src='https://github.com/danypr92.png' width='32' height='32' style='border-radius:50%;' alt='danypr92'/></a> | Add formula to invoice
[contract_variable_quantity](contract_variable_quantity/) | 18.0.1.0.0 |  | Variable quantity in contract recurrent invoicing
[product_contract](product_contract/) | 18.0.1.1.2 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Recurring - Product Contract
[product_contract_recurrence_in_price](product_contract_recurrence_in_price/) | 18.0.1.0.0 |  | Add an option to include the recurrences in the total of a Sale Order Line.
[product_contract_variable_quantity](product_contract_variable_quantity/) | 18.0.1.0.1 |  | Product contract with variable quantity
[subscription_oca](subscription_oca/) | 18.0.1.0.0 |  | Generate recurring invoices.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/credit-control


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/credit-control&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/credit-control/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/credit-control/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/credit-control/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/credit-control/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/credit-control/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/credit-control)
[![Translation Status](https://translation.odoo-community.org/widgets/credit-control-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/credit-control-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# credit-control

credit-control

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_credit_control](account_credit_control/) | 18.0.2.0.2 |  | Account Credit Control
[account_credit_control_attach_invoice](account_credit_control_attach_invoice/) | 18.0.1.0.0 |  | Extend account credit control to print credit control summary with invoices
[account_credit_control_queue_job](account_credit_control_queue_job/) | 18.0.2.0.0 |  | Account Credit Control
[account_financial_risk](account_financial_risk/) | 18.0.1.2.0 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> | Manage customer risk
[account_invoice_overdue_reminder](account_invoice_overdue_reminder/) | 18.0.1.3.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Simple mail/letter/phone overdue customer invoice reminder
[account_invoice_overdue_warn](account_invoice_overdue_warn/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Show warning on customer form view if it has overdue invoices
[account_invoice_overdue_warn_sale](account_invoice_overdue_warn_sale/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Show overdue warning on sale order form view
[account_payment_return_financial_risk](account_payment_return_financial_risk/) | 18.0.1.0.0 |  | Partner Payment Return Risk
[partner_risk_insurance](partner_risk_insurance/) | 18.0.1.0.3 | <a href='https://github.com/Daniel-CA'><img src='https://github.com/Daniel-CA.png' width='32' height='32' style='border-radius:50%;' alt='Daniel-CA'/></a> <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/omar7r'><img src='https://github.com/omar7r.png' width='32' height='32' style='border-radius:50%;' alt='omar7r'/></a> <a href='https://github.com/Tardo'><img src='https://github.com/Tardo.png' width='32' height='32' style='border-radius:50%;' alt='Tardo'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Risk insurance partner information
[partner_risk_insurance_product_sticker_invoice_report](partner_risk_insurance_product_sticker_invoice_report/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Display a Sticker on Invoice Reports secured with Risk Insurance
[sale_financial_risk](sale_financial_risk/) | 18.0.1.0.7 |  | Manage partner risk in sales orders
[sale_financial_risk_info](sale_financial_risk_info/) | 18.0.1.0.1 |  | Adds risk consumption info in sales orders.
[stock_financial_risk](stock_financial_risk/) | 18.0.1.0.0 |  | Manage partner risk in stock moves
[website_sale_financial_risk](website_sale_financial_risk/) | 18.0.1.0.0 |  | Website Sale Financial Risk

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/crm


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/crm&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/crm/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/crm/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/crm/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/crm/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/crm/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/crm)
[![Translation Status](https://translation.odoo-community.org/widgets/crm-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/crm-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# crm

crm

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[crm_claim](crm_claim/) | 18.0.1.0.0 |  | Track your customers/vendors claims and grievances.
[crm_claim_code](crm_claim_code/) | 18.0.1.0.0 |  | Sequential Code for Claims
[crm_claim_type](crm_claim_type/) | 18.0.1.0.1 |  | Claim types for CRM
[crm_date_deadline_required](crm_date_deadline_required/) | 18.0.1.0.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Field date deadline required in the opportunity
[crm_industry](crm_industry/) | 18.0.1.0.2 |  | Link leads/opportunities to industries
[crm_lead_code](crm_lead_code/) | 18.0.1.0.0 |  | Sequential Code for Leads / Opportunities
[crm_lead_currency](crm_lead_currency/) | 18.0.1.0.0 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | On leads/opportunities, add the amount in the customer's currency.
[crm_lead_firstname](crm_lead_firstname/) | 18.0.1.0.0 |  | Specify split names for contacts in leads
[crm_lead_product](crm_lead_product/) | 18.0.1.0.1 |  | Adds a lead line in the lead/opportunity model in odoo
[crm_lead_to_task](crm_lead_to_task/) | 18.0.1.1.2 |  | Create Tasks from Leads/Opportunities
[crm_lead_vat](crm_lead_vat/) | 18.0.1.0.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Add VAT field to leads
[crm_location](crm_location/) | 18.0.1.0.1 |  | CRM location
[crm_partner_assign](crm_partner_assign/) | 18.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Assign a Partner to an Opportunity/Lead/Partner to indicate Partnership
[crm_partner_capital](crm_partner_capital/) | 18.0.1.0.0 | <a href='https://github.com/adasatorres'><img src='https://github.com/adasatorres.png' width='32' height='32' style='border-radius:50%;' alt='adasatorres'/></a> | This addon extends the functionality of partner_capital
[crm_partner_employee_quantity](crm_partner_employee_quantity/) | 18.0.1.0.0 |  | Show partner employee quantity in CRM leads
[crm_partner_required](crm_partner_required/) | 18.0.1.0.2 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Field partner required in the opportunity
[crm_phonecall](crm_phonecall/) | 18.0.1.1.0 |  | CRM Phone Calls
[crm_phonecall_planner](crm_phonecall_planner/) | 18.0.1.0.0 |  | Schedule phone calls according to some criteria
[crm_phonecall_result](crm_phonecall_result/) | 18.0.1.0.0 |  | Adds phone call result tracking and reporting to CRM phonecalls
[crm_phonecall_summary_predefined](crm_phonecall_summary_predefined/) | 18.0.1.0.0 |  | Allows to choose from a defined summary list
[crm_project_create](crm_project_create/) | 18.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Allow create projects from lead/opportunity
[crm_project_task](crm_project_task/) | 18.0.1.0.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> | Create tasks from lead or opportunity
[crm_salesperson_planner](crm_salesperson_planner/) | 18.0.1.1.0 |  | Crm Salesperson Planner
[crm_security_group](crm_security_group/) | 18.0.1.2.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Add new group in Sales to show only CRM
[crm_stage_mail](crm_stage_mail/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Crm Stage Mail
[crm_stage_multi_team](crm_stage_multi_team/) | 18.0.1.0.1 |  | Allows multiple teams in crm stage
[crm_stage_probability](crm_stage_probability/) | 18.0.1.0.0 |  | Define fixed probability on the stages
[crm_team_parent](crm_team_parent/) | 18.0.1.0.0 |  | Add a parent field on sales teams.
[crm_won_reason](crm_won_reason/) | 18.0.1.0.0 | <a href='https://github.com/ajaniszewska-dev'><img src='https://github.com/ajaniszewska-dev.png' width='32' height='32' style='border-radius:50%;' alt='ajaniszewska-dev'/></a> | CRM won reason
[crm_won_restrict_per_stage](crm_won_restrict_per_stage/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | CRM Won Restrict Per Stage
[marketing_crm_partner](marketing_crm_partner/) | 18.0.1.0.1 |  | Copy tracking fields from leads to partners

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/crowdfunding


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# crowdfunding
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/crowdfunding&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/crowdfunding/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/crowdfunding/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/crowdfunding/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/crowdfunding/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/crowdfunding/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/crowdfunding)
[![Translation Status](https://translation.odoo-community.org/widgets/crowdfunding-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/crowdfunding-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

crowdfunding

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[crowdfunding](crowdfunding/) | 18.0.1.1.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Turn Odoo into a platform for crowdfunding
[crowdfunding_demo](crowdfunding_demo/) | 18.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Installs demo data to have crowdfunding up and running on runbot
[crowdfunding_public_pledge](crowdfunding_public_pledge/) | 18.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Allow users to mark their pledges as public

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/currency


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/currency&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/currency/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/currency/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/currency/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/currency/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/currency/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/currency)
[![Translation Status](https://translation.odoo-community.org/widgets/currency-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/currency-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# currency

currency

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[currency_old_rate_notify](currency_old_rate_notify/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Notify accounting managers when currency rates are too old
[currency_rate_update](currency_rate_update/) | 18.0.1.0.1 |  | Update exchange rates using OCA modules
[currency_rate_update_xe](currency_rate_update_xe/) | 18.0.1.0.0 |  | Update exchange rates using XE.com

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/data-protection


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/data-protection&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/data-protection/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/data-protection/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/data-protection/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/data-protection/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/data-protection/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/data-protection)
[![Translation Status](https://translation.odoo-community.org/widgets/data-protection-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/data-protection-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# data-protection

data-protection

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_export_anonymize](base_export_anonymize/) | 18.0.1.0.0 |  | Anonymize certain fields for a group of users when exporting them directly or via relational fields.
[privacy](privacy/) | 18.0.1.0.0 |  | Provides data privacy and protection features to comply to regulations, such as GDPR.
[privacy_consent](privacy_consent/) | 18.0.1.0.0 |  | Allow people to explicitly accept or reject inclusion in some activity, GDPR compliant
[privacy_partner_to_be_forgotten](privacy_partner_to_be_forgotten/) | 18.0.1.0.0 |  | Anonymize partner data for GDPR compliance

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/ddmrp


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/ddmrp&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/ddmrp/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/ddmrp/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/ddmrp/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/ddmrp/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/ddmrp/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/ddmrp)
[![Translation Status](https://translation.odoo-community.org/widgets/ddmrp-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/ddmrp-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# ddmrp

ddmrp

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[ddmrp](ddmrp/) | 18.0.1.9.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Demand Driven Material Requirements Planning
[ddmrp_adjustment](ddmrp_adjustment/) | 18.0.2.0.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Allow to apply factor adjustments to buffers.
[ddmrp_adjustment_matrix](ddmrp_adjustment_matrix/) | 18.0.1.0.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Wizard to manage DDMRP Adjustments with a 2D matrix.
[ddmrp_chatter](ddmrp_chatter/) | 18.0.1.0.0 |  | Adds chatter and activities to stock buffers.
[ddmrp_coverage_days](ddmrp_coverage_days/) | 18.0.1.0.0 |  | Implements Coverage Days.
[ddmrp_cron_actions_as_job](ddmrp_cron_actions_as_job/) | 18.0.1.0.1 |  | Run DDMRP Buffer Calculation as jobs
[ddmrp_exclude_moves_adu_calc](ddmrp_exclude_moves_adu_calc/) | 18.0.1.1.1 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Define additional rules to exclude certain moves from ADU calculation
[ddmrp_exclude_moves_adu_calc_sales](ddmrp_exclude_moves_adu_calc_sales/) | 18.0.2.0.0 | <a href='https://github.com/DavidJForgeFlow'><img src='https://github.com/DavidJForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='DavidJForgeFlow'/></a> | DDMRP Exclude Moves ADU Calc integration with Sales app.
[ddmrp_history](ddmrp_history/) | 18.0.1.2.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Allow to store historical data of DDMRP buffers.
[ddmrp_packaging](ddmrp_packaging/) | 18.0.1.0.0 |  | DDMRP integration with packaging
[ddmrp_packaging_product_replace](ddmrp_packaging_product_replace/) | 18.0.1.0.0 |  | Glue module for DDMRP packaging and product replace
[ddmrp_product_replace](ddmrp_product_replace/) | 18.0.1.1.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Provides a assisting tool for product replacement.
[ddmrp_purchase_hide_onhand_status](ddmrp_purchase_hide_onhand_status/) | 18.0.1.0.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Replace purchase onhand status with smart button.
[ddmrp_report_part_flow_index](ddmrp_report_part_flow_index/) | 18.0.1.0.1 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Provides the DDMRP Parts Flow Index Report
[ddmrp_warning](ddmrp_warning/) | 18.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Adds configuration warnings on stock buffers.
[ddmrp_warning_as_job](ddmrp_warning_as_job/) | 18.0.1.0.0 |  | Run DDMRP Warning as jobs
[stock_buffer_capacity_limit](stock_buffer_capacity_limit/) | 18.0.1.0.1 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Ensures that the limits of storage are never surpassed
[stock_buffer_route](stock_buffer_route/) | 18.0.1.0.0 |  | Allows to force a route to be used when procuring from Stock Buffers
[stock_buffer_sales_analysis](stock_buffer_sales_analysis/) | 18.0.1.0.0 |  | Allows to access the Sales Analysis from Stock Buffers

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/delivery-carrier


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/delivery-carrier&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/delivery-carrier/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/delivery-carrier/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/delivery-carrier/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/delivery-carrier/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/delivery-carrier/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/delivery-carrier)
[![Translation Status](https://translation.odoo-community.org/widgets/delivery-carrier-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/delivery-carrier-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Delivery Carrier

Are you looking for modules related to logistics? Or would like to contribute
to? There are many repositories with specific purposes. Have a look at this
[README](https://github.com/OCA/wms/blob/18.0/README.md).

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[carrier_account_environment](carrier_account_environment/) | 18.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Configure carriers with server_environment_files
[delivery_auto_refresh](delivery_auto_refresh/) | 18.0.1.0.0 |  | Auto-refresh delivery price in sales orders
[delivery_carrier_account](delivery_carrier_account/) | 18.0.1.0.0 |  | Delivery Carrier Account
[delivery_carrier_agency](delivery_carrier_agency/) | 18.0.1.0.0 |  | Add a model for Carrier Agencies
[delivery_carrier_image](delivery_carrier_image/) | 18.0.1.0.0 |  | This module allows to use a carrier logo in different flows
[delivery_carrier_info](delivery_carrier_info/) | 18.0.1.0.0 |  | Add code on carrier
[delivery_carrier_label_default](delivery_carrier_label_default/) | 18.0.1.0.1 |  | This module defines a basic label to print when no specific carrier is selected.
[delivery_carrier_manual_price](delivery_carrier_manual_price/) | 18.0.1.0.0 |  | Allow setting manual shipping cost in sale order.
[delivery_carrier_manual_weight](delivery_carrier_manual_weight/) | 18.0.1.0.0 |  | Allow setting weight and shipping weight in stock transfers manually based on carrier.
[delivery_carrier_max_weight_constraint](delivery_carrier_max_weight_constraint/) | 18.0.1.0.0 |  | Constrain package maximum weight
[delivery_carrier_multi_zip](delivery_carrier_multi_zip/) | 18.0.1.0.1 |  | Multiple ZIP intervals for the same delivery method
[delivery_carrier_option](delivery_carrier_option/) | 18.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Delivery Carrier Option
[delivery_carrier_partner](delivery_carrier_partner/) | 18.0.1.0.0 |  | Add a partner in the delivery carrier
[delivery_carrier_picking_valid](delivery_carrier_picking_valid/) | 18.0.1.0.0 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Checks if a transfer matches carrier requirements
[delivery_carrier_picking_valid_dangerous_goods](delivery_carrier_picking_valid_dangerous_goods/) | 18.0.1.1.0 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Checks if a transfer matches carrier dangerous goods restrictions
[delivery_carrier_pricelist](delivery_carrier_pricelist/) | 18.0.1.0.1 |  | Compute delivery method price based on the product's pricelist.
[delivery_carrier_report_to_printer](delivery_carrier_report_to_printer/) | 18.0.1.0.0 | <a href='https://github.com/carlos-lopez-tecnativa'><img src='https://github.com/carlos-lopez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carlos-lopez-tecnativa'/></a> | Delivery carrier report to printer
[delivery_carrier_shipping_label](delivery_carrier_shipping_label/) | 18.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Delivery Carrier Shipping Label
[delivery_carrier_shipping_policy](delivery_carrier_shipping_policy/) | 18.0.1.0.0 |  | Delivery Carrier Shipping Policy
[delivery_carrier_warehouse](delivery_carrier_warehouse/) | 18.0.1.0.1 |  | Get delivery method used in sales orders from warehouse
[delivery_correos_express](delivery_correos_express/) | 18.0.1.0.0 |  | Delivery Carrier implementation for Correos Express using their API
[delivery_cttexpress](delivery_cttexpress/) | 18.0.1.0.0 |  | Delivery Carrier implementation for CTT Express API
[delivery_dachser](delivery_dachser/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Delivery Carrier implementation for Dachser API
[delivery_date_exclude_service](delivery_date_exclude_service/) | 18.0.1.0.0 |  | Exclude service products from delivery date computation
[delivery_driver](delivery_driver/) | 18.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Allow choose driver in delivery methods
[delivery_driver_stock_picking_batch](delivery_driver_stock_picking_batch/) | 18.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Add drivers from delivery in stock picking batch
[delivery_dropoff_site](delivery_dropoff_site/) | 18.0.1.0.0 |  | Send goods to sites in which customers come pick up package
[delivery_easypost_oca](delivery_easypost_oca/) | 18.0.1.0.0 |  | OCA Delivery Easypost
[delivery_estimated_package_quantity_by_weight](delivery_estimated_package_quantity_by_weight/) | 18.0.1.0.0 |  | Compute the amount of packages a picking out should have depending on the weight of the products and the limit fixed by the carrier
[delivery_free_fee_removal](delivery_free_fee_removal/) | 18.0.1.0.0 |  | Hide free fee lines on sales orders
[delivery_free_over_untaxed_price](delivery_free_over_untaxed_price/) | 18.0.1.0.0 |  | Decide if delivery is free over the untaxed price.
[delivery_multi_destination](delivery_multi_destination/) | 18.0.1.0.1 |  | Multiple destinations for the same delivery method
[delivery_package_fee](delivery_package_fee/) | 18.0.1.0.0 |  | Add fees on sales order for delivered packages
[delivery_package_number](delivery_package_number/) | 18.0.2.1.0 |  | Set or compute number of packages for a picking
[delivery_package_type_number_parcels](delivery_package_type_number_parcels/) | 18.0.1.0.0 |  | Number of parcels in a package type
[delivery_package_type_shipping_weight](delivery_package_type_shipping_weight/) | 18.0.1.0.0 |  | Set and manage shipping weight based on package type.
[delivery_postlogistics](delivery_postlogistics/) | 18.0.2.0.0 |  | Print PostLogistics shipping labels using the Barcode web service
[delivery_postlogistics_dangerous_goods](delivery_postlogistics_dangerous_goods/) | 18.0.1.0.0 |  | Declare dangerous goods when generating postlogistics labels
[delivery_postlogistics_server_env](delivery_postlogistics_server_env/) | 18.0.1.0.0 |  | Server Environment layer for Delivery Postlogistics
[delivery_price_method](delivery_price_method/) | 18.0.1.1.0 |  | Force a fixed or rule price calculation on Delivery Methods, for example to override a webservice provided prices.
[delivery_purchase](delivery_purchase/) | 18.0.1.0.0 |  | Delivery costs in purchases
[delivery_roulier](delivery_roulier/) | 18.0.1.0.1 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> <a href='https://github.com/hparfr'><img src='https://github.com/hparfr.png' width='32' height='32' style='border-radius:50%;' alt='hparfr'/></a> | Integration of multiple carriers
[delivery_schenker](delivery_schenker/) | 18.0.1.0.0 |  | Delivery Carrier implementation for DB Schenker API
[delivery_state](delivery_state/) | 18.0.1.2.2 |  | Provides fields to be able to contemplate the tracking statesand also adds a global fields
[delivery_ups_oca](delivery_ups_oca/) | 18.0.1.2.0 |  | Integrate UPS webservice
[partner_delivery_info](partner_delivery_info/) | 18.0.1.0.0 |  | Send delivery notice to the shipper from any operation.
[partner_delivery_schedule](partner_delivery_schedule/) | 18.0.1.0.1 |  | Set on partners a schedule for delivery goods
[partner_delivery_zone](partner_delivery_zone/) | 18.0.1.0.1 |  | Enables partner delivery zones for physical products
[sale_order_warehouse_from_delivery_carrier](sale_order_warehouse_from_delivery_carrier/) | 18.0.1.0.0 |  | Sale Order WH from Delivery Carrier
[server_environment_delivery](server_environment_delivery/) | 18.0.1.0.0 |  | Configure prod environment for delivery carriers
[stock_fleet_delivery_driver](stock_fleet_delivery_driver/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Allow choose Vehicle in Carriers, Transfers and Batches
[stock_picking_carrier_from_rule](stock_picking_carrier_from_rule/) | 18.0.1.0.0 |  | Set the carrier on picking if the stock rule used has a partner address set with a delivery method.
[stock_picking_delivery_link](stock_picking_delivery_link/) | 18.0.1.0.3 |  | Adds link to the delivery on all intermediate operations.
[stock_picking_delivery_package_type_domain](stock_picking_delivery_package_type_domain/) | 18.0.1.0.0 |  | This module will allow to extend the domain to filter package type selection in 'Choose Delivery Package' wizard
[stock_picking_report_delivery_cost](stock_picking_report_delivery_cost/) | 18.0.1.0.0 |  | Show delivery cost in delivery slip and picking operations reports

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/dms


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# dms
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/dms&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/dms/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/dms/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/dms/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/dms/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/dms/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/dms)
[![Translation Status](https://translation.odoo-community.org/widgets/dms-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/dms-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

dms

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[dms](dms/) | 18.0.1.1.0 |  | Document Management System for Odoo
[dms_auto_classification](dms_auto_classification/) | 18.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Auto classify documents into DMS
[dms_field](dms_field/) | 18.0.1.2.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Create DMS View and allow to use them inside a record
[dms_field_auto_classification](dms_field_auto_classification/) | 18.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Auto classify files into embedded DMS
[dms_user_role](dms_user_role/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | DMS User Role
[hr_dms_field](hr_dms_field/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Add dms field for employees
[web_editor_media_dialog_dms](web_editor_media_dialog_dms/) | 18.0.1.0.1 |  | Integrate DMS with media dialog of web editor

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/donation


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/donation&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/donation/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/donation/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/donation/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/donation/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/donation/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/donation)
[![Translation Status](https://translation.odoo-community.org/widgets/donation-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/donation-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# donation

donation

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[donation](donation/) | 18.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Manage donations
[donation_base](donation_base/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Base module for donations

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/e-commerce


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# e-commerce
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/e-commerce&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/e-commerce/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/e-commerce/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/e-commerce/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/e-commerce/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/e-commerce/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/e-commerce)
[![Translation Status](https://translation.odoo-community.org/widgets/e-commerce-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/e-commerce-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

e-commerce

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[product_template_multi_link](product_template_multi_link/) | 18.0.1.0.1 |  | Product Multi Links (Template)
[product_template_multi_link_date_span](product_template_multi_link_date_span/) | 18.0.1.0.0 |  | Add an optional date span for when a link is active.
[product_variant_multi_link](product_variant_multi_link/) | 18.0.1.0.0 |  | Product Multi Links (Variant)
[website_sale_acquirer_confirm_order](website_sale_acquirer_confirm_order/) | 18.0.1.0.1 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | eCommerce Confirm Order By Payment Provider
[website_sale_attribute_filter_form_submit](website_sale_attribute_filter_form_submit/) | 18.0.1.0.1 |  | Allow to apply manually the filters on the e-commerce
[website_sale_b2x_alt_price](website_sale_b2x_alt_price/) | 18.0.1.0.0 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Display prices with(out) taxes in eCommerce, complementing normal mode
[website_sale_barcode_search](website_sale_barcode_search/) | 18.0.1.0.0 |  | It improve website product search adding search by barcode
[website_sale_cart_expire](website_sale_cart_expire/) | 18.0.1.0.1 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Cancel carts without activity after a configurable time
[website_sale_category_breadcrumb](website_sale_category_breadcrumb/) | 18.0.1.0.0 | <a href='https://github.com/Rad0van'><img src='https://github.com/Rad0van.png' width='32' height='32' style='border-radius:50%;' alt='Rad0van'/></a> | Displays Product Category Breadcrumb(s) in eCommerce
[website_sale_charge_payment_fee](website_sale_charge_payment_fee/) | 18.0.1.0.0 | <a href='https://github.com/miguel-S73'><img src='https://github.com/miguel-S73.png' width='32' height='32' style='border-radius:50%;' alt='miguel-S73'/></a> | Payment fee charged to customer
[website_sale_checkout_country_vat](website_sale_checkout_country_vat/) | 18.0.1.0.0 |  | Autocomplete VAT in checkout process
[website_sale_checkout_skip_payment](website_sale_checkout_skip_payment/) | 18.0.1.1.1 |  | Skip payment for logged users in checkout process
[website_sale_comparison_hide_price](website_sale_comparison_hide_price/) | 18.0.1.0.0 |  | Hide product prices on the shop
[website_sale_empty_cart](website_sale_empty_cart/) | 18.0.1.0.0 |  | Adds a button in the website cart to empty all
[website_sale_hide_empty_category](website_sale_hide_empty_category/) | 18.0.1.0.1 |  | Hide any Product Categories that are empty
[website_sale_hide_price](website_sale_hide_price/) | 18.0.1.0.0 |  | Hide product prices on the shop
[website_sale_order_shipping_modification](website_sale_order_shipping_modification/) | 18.0.1.0.0 |  | Change the delivery address in quotes from the portal
[website_sale_order_type](website_sale_order_type/) | 18.0.1.0.1 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | This module allows sale_order_type to work with website_sale.
[website_sale_product_assortment](website_sale_product_assortment/) | 18.0.1.1.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Use product assortments to display products available on e-commerce.
[website_sale_product_attribute_filter_category](website_sale_product_attribute_filter_category/) | 18.0.1.0.1 |  | Allow group attributes in shop by categories
[website_sale_product_attribute_filter_order](website_sale_product_attribute_filter_order/) | 18.0.1.0.0 | <a href='https://github.com/Tardo'><img src='https://github.com/Tardo.png' width='32' height='32' style='border-radius:50%;' alt='Tardo'/></a> | Move active checkbox options to the first place of the list
[website_sale_product_attribute_value_filter_existing](website_sale_product_attribute_value_filter_existing/) | 18.0.1.1.3 |  | Allow hide attributes values not used in variants
[website_sale_product_brand](website_sale_product_brand/) | 18.0.1.0.1 |  | Product Brand Filtering in Website
[website_sale_product_description](website_sale_product_description/) | 18.0.1.0.0 |  | Shows custom e-Commerce description for products
[website_sale_product_detail_attribute_image](website_sale_product_detail_attribute_image/) | 18.0.1.0.0 |  | Display attributes images in shop product detail
[website_sale_product_eprel](website_sale_product_eprel/) | 18.0.1.0.0 |  | Display EPREL energy label and product info on website product page.
[website_sale_product_item_cart_custom_qty](website_sale_product_item_cart_custom_qty/) | 18.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Allows to add to cart from product items a custom quantity.
[website_sale_product_minimal_price](website_sale_product_minimal_price/) | 18.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Display minimal price for products that has variants
[website_sale_product_reference_displayed](website_sale_product_reference_displayed/) | 18.0.1.0.1 |  | Display product reference in e-commerce
[website_sale_product_sort](website_sale_product_sort/) | 18.0.1.0.0 |  | Allow to define default sort criteria for e-commerce
[website_sale_require_legal](website_sale_require_legal/) | 18.0.1.0.2 |  | Force the user to accept legal tems to buy in the web shop
[website_sale_secondary_unit](website_sale_secondary_unit/) | 18.0.1.0.1 |  | Allow manage secondary units in website shop
[website_sale_stock_available](website_sale_stock_available/) | 18.0.1.0.0 |  | Display 'Available to promise' in shop online instead of 'Free To Use Quantity'
[website_sale_stock_list_preview](website_sale_stock_list_preview/) | 18.0.1.0.0 |  | Show the stock of products on the product previews
[website_sale_stock_provisioning_date](website_sale_stock_provisioning_date/) | 18.0.1.0.1 |  | Display provisioning date for a product in shop online
[website_sale_suggest_create_account](website_sale_suggest_create_account/) | 18.0.1.0.0 |  | Suggest users to create an account when buying in the website
[website_sale_tax_toggle](website_sale_tax_toggle/) | 18.0.1.0.0 |  | Allow display price in Shop with or without taxes
[website_sale_vat_required](website_sale_vat_required/) | 18.0.1.0.0 |  | VAT number required in checkout form
[website_sale_wishlist_hide_price](website_sale_wishlist_hide_price/) | 18.0.1.0.1 |  | Hide product prices on the shop
[website_sale_wishlist_keep](website_sale_wishlist_keep/) | 18.0.1.0.0 |  | Allows to add products to my cart but keep it in my wishlist"
[website_snippet_product_category](website_snippet_product_category/) | 18.0.1.1.1 | <a href='https://github.com/Tardo'><img src='https://github.com/Tardo.png' width='32' height='32' style='border-radius:50%;' alt='Tardo'/></a> | Adds a new snippet to show e-commerce categories

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/edi


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/edi&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/edi/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/edi/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/edi/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/edi/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/edi/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/edi)
[![Translation Status](https://translation.odoo-community.org/widgets/edi-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/edi-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# edi

edi

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_edi_ubl_cii_payment_unece](account_edi_ubl_cii_payment_unece/) | 18.0.1.0.0 |  | Import/Export UNECE payment codes in UBL and CII XML documents.
[account_einvoice_generate](account_einvoice_generate/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Technical module to generate PDF invoices with embedded XML file
[account_invoice_download](account_invoice_download/) | 18.0.1.1.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Auto-download supplier invoices and import them
[account_invoice_download_ovh](account_invoice_download_ovh/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Get OVH Invoice via the API
[account_invoice_download_scaleway](account_invoice_download_scaleway/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Get Scaleway Invoices via the API
[account_invoice_export](account_invoice_export/) | 18.0.1.0.1 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Account Invoice Export
[account_invoice_export_job](account_invoice_export_job/) | 18.0.1.0.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Account Invoice Export Job
[account_invoice_export_server_env](account_invoice_export_server_env/) | 18.0.1.0.0 |  | Server environment for Account Invoice Export
[account_invoice_facturx](account_invoice_facturx/) | 18.0.2.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Generate Factur-X/ZUGFeRD customer invoices
[account_invoice_facturx_py3o](account_invoice_facturx_py3o/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Generate Factur-X invoices with Py3o reporting engine
[account_invoice_import](account_invoice_import/) | 18.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import supplier invoices/refunds as PDF or XML files
[account_invoice_import_facturx](account_invoice_import_facturx/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import Factur-X/ZUGFeRD Vendor Bills
[account_invoice_import_simple_pdf](account_invoice_import_simple_pdf/) | 18.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import simple PDF vendor bills
[account_invoice_import_ubl](account_invoice_import_ubl/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import UBL XML supplier invoices/refunds
[base_business_document_import](base_business_document_import/) | 18.0.2.0.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Provides technical tools to import sale orders or supplier invoices
[base_business_document_import_phone](base_business_document_import_phone/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Use phone numbers to match partners upon import of business documents
[base_ebill_payment_contract](base_ebill_payment_contract/) | 18.0.1.0.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Base for managing e-billing contracts
[base_edi](base_edi/) | 18.0.1.0.2 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Base module to aggregate EDI features.
[base_facturx](base_facturx/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Base module for Factur-X/ZUGFeRD
[base_import_pdf_by_template](base_import_pdf_by_template/) | 18.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Base Import Pdf by Template
[base_import_pdf_by_template_account](base_import_pdf_by_template_account/) | 18.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Base Import Pdf by Template Account
[base_ubl](base_ubl/) | 18.0.1.0.0 |  | Base module for Universal Business Language (UBL)
[base_ubl_generate](base_ubl_generate/) | 18.0.1.0.1 |  | Base module to generate UBL files (Universal Business Language)
[base_ubl_parse](base_ubl_parse/) | 18.0.1.0.0 |  | Base module to parse UBL files (Universal Business Language)
[partner_identification_import](partner_identification_import/) | 18.0.1.0.1 |  | Provides partner matching on extra ID
[purchase_order_ubl](purchase_order_ubl/) | 18.0.1.0.0 |  | Embed UBL XML file inside the PDF purchase order
[sale_order_customer_free_ref](sale_order_customer_free_ref/) | 18.0.1.0.0 |  | Splits the Customer Reference on sale orders into two fields. An Id and a Free reference. The existing field is transformed into a computed one.
[sale_order_import](sale_order_import/) | 18.0.1.2.0 |  | Import RFQ or sale orders from files
[sale_order_import_packaging](sale_order_import_packaging/) | 18.0.1.0.0 |  | Import the packaging on the sale order line
[sale_order_import_ubl](sale_order_import_ubl/) | 18.0.1.0.1 |  | Import UBL XML sale order files
[sale_order_import_ubl_customer_free_ref](sale_order_import_ubl_customer_free_ref/) | 18.0.1.0.0 |  | Extract CustomerReference from sale UBL
[sale_order_import_ubl_line_customer_ref](sale_order_import_ubl_line_customer_ref/) | 18.0.1.0.0 |  | Extract specific customer reference for each order line
[sale_order_import_ubl_requested_delivery](sale_order_import_ubl_requested_delivery/) | 18.0.1.0.0 |  | Extract RequestedDeliveryPeriod from sale UBL

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/edi-framework


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# edi-framework
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/edi-framework&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/edi-framework/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/edi-framework/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/edi-framework/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/edi-framework/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/edi-framework/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/edi-framework)
[![Translation Status](https://translation.odoo-community.org/widgets/edi-framework-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/edi-framework-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

edi-framework

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[edi_account_core_oca](edi_account_core_oca/) | 18.0.1.1.1 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Define EDI Configuration for Account Moves
[edi_account_oca](edi_account_oca/) | 18.0.1.1.1 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Define some component listeners for Account Moves
[edi_component_oca](edi_component_oca/) | 18.0.1.1.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Allow to use Connector as a source in EDI
[edi_core_oca](edi_core_oca/) | 18.0.1.7.3 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Define backends, exchange types, exchange records, basic automation and views for handling EDI exchanges.
[edi_endpoint_oca](edi_endpoint_oca/) | 18.0.1.0.3 |  | Base module allowing configuration of custom endpoints for EDI framework.
[edi_exchange_deduplicate_oca](edi_exchange_deduplicate_oca/) | 18.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Introduce a deduplication mechanism at the sending step
[edi_exchange_template_oca](edi_exchange_template_oca/) | 18.0.1.3.3 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Allows definition of exchanges via templates.
[edi_exchange_template_party_data](edi_exchange_template_party_data/) | 18.0.1.0.1 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Glue module between edi_exchange_template and edi_party_data
[edi_notification_oca](edi_notification_oca/) | 18.0.1.0.0 |  | Define notification activities on exchange records.
[edi_oca](edi_oca/) | 18.0.1.5.2 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Integrate all EDI modules together
[edi_party_data_oca](edi_party_data_oca/) | 18.0.1.0.1 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Allow to configure and retrieve party information for EDI exchanges.
[edi_product_oca](edi_product_oca/) | 18.0.1.0.0 |  | EDI framework configuration and base logic for products and products packaging
[edi_purchase_oca](edi_purchase_oca/) | 18.0.1.0.0 |  | Define EDI Configuration for Purchase Orders
[edi_queue_oca](edi_queue_oca/) | 18.0.1.0.2 |  | Set Queue Jobs on EDI
[edi_record_metadata_oca](edi_record_metadata_oca/) | 18.0.1.0.5 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Allow to store metadata for related records.
[edi_sale_endpoint](edi_sale_endpoint/) | 18.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Glue module between edi_sale_oca and edi_endpoint_oca.
[edi_sale_input_oca](edi_sale_input_oca/) | 18.0.1.0.2 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Process incoming sale orders with the EDI framework.
[edi_sale_oca](edi_sale_oca/) | 18.0.1.0.1 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Configuration and special behaviors for EDI on sales.
[edi_sale_stock_oca](edi_sale_stock_oca/) | 18.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Configuration and special behaviors for EDI on sales & stock.
[edi_sale_ubl_oca](edi_sale_ubl_oca/) | 18.0.1.0.2 |  | Configuration and special behaviors for EDI UBL exchanges related to sales.
[edi_sale_ubl_output_oca](edi_sale_ubl_output_oca/) | 18.0.1.0.1 |  | Configuration and special behaviors for EDI on sales.
[edi_state_oca](edi_state_oca/) | 18.0.1.0.3 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Allow to assign specific EDI states to related records.
[edi_stock_oca](edi_stock_oca/) | 18.0.1.0.1 |  | Define EDI Configuration for Stock
[edi_storage_oca](edi_storage_oca/) | 18.0.1.1.0 |  | Base module to allow exchanging files via storage backend (eg: SFTP).
[edi_storage_queue_oca](edi_storage_queue_oca/) | 18.0.1.0.0 |  | Integrates EDI Storage with Queue
[edi_ubl_oca](edi_ubl_oca/) | 18.0.1.0.1 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Define EDI backend type for UBL.
[edi_webservice_oca](edi_webservice_oca/) | 18.0.1.0.2 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Defines webservice integration from EDI Exchange records
[edi_xml_oca](edi_xml_oca/) | 18.0.1.0.2 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Base module for EDI exchange using XML files.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/edi-voxel


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/edi-voxel&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/edi-voxel/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/edi-voxel/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/edi-voxel/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/edi-voxel/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/edi-voxel/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/edi-voxel)
[![Translation Status](https://translation.odoo-community.org/widgets/edi-voxel-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/edi-voxel-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# edi-voxel

edi-voxel

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[edi_voxel_account_invoice_oca](edi_voxel_account_invoice_oca/) | 18.0.1.0.1 |  | Sends account invoices to Voxel.
[edi_voxel_oca](edi_voxel_oca/) | 18.0.1.0.0 |  | Base module for connecting with Voxel
[edi_voxel_sale_order_import_oca](edi_voxel_sale_order_import_oca/) | 18.0.1.0.1 |  | Import sale order from Voxel.
[edi_voxel_sale_secondary_unit_oca](edi_voxel_sale_secondary_unit_oca/) | 18.0.1.0.0 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | Map Voxel UoM to Sale Secondary UoM and Use Them
[edi_voxel_secondary_unit_oca](edi_voxel_secondary_unit_oca/) | 18.0.1.0.0 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | Add Voxel UoM code to Secondary UoM model
[edi_voxel_stock_picking_oca](edi_voxel_stock_picking_oca/) | 18.0.1.0.0 |  | Sends stock picking report to Voxel.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/event


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/event&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/event/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/event/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/event/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/event/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/event/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/event)
[![Translation Status](https://translation.odoo-community.org/widgets/event-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/event-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# event

event

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[event_contact](event_contact/) | 18.0.1.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | Add contacts to event and event type
[event_mail](event_mail/) | 18.0.1.0.0 |  | Mail settings in events
[event_min_seat](event_min_seat/) | 18.0.1.0.0 |  | Minimum seats in events
[event_registration_cancel_reason](event_registration_cancel_reason/) | 18.0.1.0.0 |  | Reasons for event registrations cancellations
[event_registration_mass_mailing](event_registration_mass_mailing/) | 18.0.1.0.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | Put event registrations emails into mailing lists
[event_registration_multi_qty](event_registration_multi_qty/) | 18.0.1.0.0 |  | Allow registration grouped by quantities
[event_registration_partner_unique](event_registration_partner_unique/) | 18.0.1.0.0 |  | Enforces 1 registration per partner and event
[event_sale_free_no_invoiceable](event_sale_free_no_invoiceable/) | 18.0.1.0.0 |  | Free tickets no invoiceable
[event_sale_registration_multi_qty](event_sale_registration_multi_qty/) | 18.0.1.0.1 |  | Allows sell registrations with more than one attendee
[event_sale_session](event_sale_session/) | 18.0.1.0.0 |  | Sell Event Sessions
[event_session](event_session/) | 18.0.1.0.0 |  | Sessions in events
[event_session_registration_multi_qty](event_session_registration_multi_qty/) | 18.0.1.0.0 |  | Allow registration grouped by quantities in sessions
[event_stage_cancelled](event_stage_cancelled/) | 18.0.1.0.0 |  | Event cancellation workflows
[partner_event](partner_event/) | 18.0.1.1.0 |  | Link partner to events
[website_event_contact](website_event_contact/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Display your event contacts on your event page
[website_event_filter_city](website_event_filter_city/) | 18.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Add a customizable top area to filter events with city
[website_event_membership_restriction](website_event_membership_restriction/) | 18.0.1.0.0 |  | Restrict event registration to members only
[website_event_questions_by_ticket](website_event_questions_by_ticket/) | 18.0.1.0.0 |  | Events Questions conditional to the chosen ticket
[website_event_require_legal](website_event_require_legal/) | 18.0.1.0.0 |  | Website Event Require Legal
[website_event_require_login](website_event_require_login/) | 18.0.1.0.0 |  | Website Event Require Login
[website_event_ribbon](website_event_ribbon/) | 18.0.1.0.0 |  | Add ribbons on events
[website_event_ticket_limit](website_event_ticket_limit/) | 18.0.1.0.0 |  | Website Event Ticket Limit

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/field-service


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/field-service&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/field-service/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/field-service/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/field-service/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/field-service/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/field-service/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/field-service)
[![Translation Status](https://translation.odoo-community.org/widgets/field-service-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/field-service-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# field-service

field-service

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_territory](base_territory/) | 18.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | This module allows you to define territories, branches, districts and regions to be used for Field Service operations or Sales.
[fieldservice](fieldservice/) | 18.0.5.6.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Manage Field Service Locations, Workers and Orders
[fieldservice_account](fieldservice_account/) | 18.0.1.1.0 | <a href='https://github.com/osimallen'><img src='https://github.com/osimallen.png' width='32' height='32' style='border-radius:50%;' alt='osimallen'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> | Track invoices linked to Field Service orders
[fieldservice_activity](fieldservice_activity/) | 18.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> | Field Service Activities are a set of actions that need to be performed on a service order
[fieldservice_agreement](fieldservice_agreement/) | 18.0.2.0.1 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> <a href='https://github.com/patrickrwilson'><img src='https://github.com/patrickrwilson.png' width='32' height='32' style='border-radius:50%;' alt='patrickrwilson'/></a> | Manage Field Service agreements and contracts
[fieldservice_agreement_repair](fieldservice_agreement_repair/) | 18.0.1.0.0 | <a href='https://github.com/imlopes'><img src='https://github.com/imlopes.png' width='32' height='32' style='border-radius:50%;' alt='imlopes'/></a> <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Fieldservice Agreement Repair
[fieldservice_availability](fieldservice_availability/) | 18.0.1.0.0 | <a href='https://github.com/ppyczko'><img src='https://github.com/ppyczko.png' width='32' height='32' style='border-radius:50%;' alt='ppyczko'/></a> | Provides models for defining blackout days, stress days, and delivery time ranges for FSM availability management.
[fieldservice_calendar](fieldservice_calendar/) | 18.0.1.0.0 | <a href='https://github.com/hparfr'><img src='https://github.com/hparfr.png' width='32' height='32' style='border-radius:50%;' alt='hparfr'/></a> | Add calendar to FSM Orders
[fieldservice_crm](fieldservice_crm/) | 18.0.1.0.0 | <a href='https://github.com/patrickrwilson'><img src='https://github.com/patrickrwilson.png' width='32' height='32' style='border-radius:50%;' alt='patrickrwilson'/></a> | Create Field Service orders from the CRM
[fieldservice_equipment_stock](fieldservice_equipment_stock/) | 18.0.1.0.1 | <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> | Integrate stock operations with your field service equipments
[fieldservice_equipment_warranty](fieldservice_equipment_warranty/) | 18.0.1.0.0 | <a href='https://github.com/imlopes'><img src='https://github.com/imlopes.png' width='32' height='32' style='border-radius:50%;' alt='imlopes'/></a> | Field Service equipment warranty
[fieldservice_geoengine](fieldservice_geoengine/) | 18.0.1.0.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Display Field Service locations on a map with Open Street Map
[fieldservice_kanban_info](fieldservice_kanban_info/) | 18.0.1.0.2 | <a href='https://github.com/ppyczko'><img src='https://github.com/ppyczko.png' width='32' height='32' style='border-radius:50%;' alt='ppyczko'/></a> | Display key service information on Field Service Kanban cards.
[fieldservice_portal](fieldservice_portal/) | 18.0.1.0.0 | <a href='https://github.com/aleuffre'><img src='https://github.com/aleuffre.png' width='32' height='32' style='border-radius:50%;' alt='aleuffre'/></a> <a href='https://github.com/renda-dev'><img src='https://github.com/renda-dev.png' width='32' height='32' style='border-radius:50%;' alt='renda-dev'/></a> | Bridge module between fieldservice and portal.
[fieldservice_project](fieldservice_project/) | 18.0.1.0.1 |  | Create field service orders from a project or project task
[fieldservice_recurring](fieldservice_recurring/) | 18.0.1.2.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Manage recurring Field Service orders
[fieldservice_repair](fieldservice_repair/) | 18.0.3.0.1 | <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Integrate Field Service orders with MRP repair orders
[fieldservice_repair_order_template](fieldservice_repair_order_template/) | 18.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Use Repair Order Templates when creating a repair orders
[fieldservice_route](fieldservice_route/) | 18.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Organize the routes of each day.
[fieldservice_route_availability](fieldservice_route_availability/) | 18.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Restricts blackout days for Scheduled Start (ETA) orders with the same date.
[fieldservice_sale](fieldservice_sale/) | 18.0.1.2.1 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Sell field services.
[fieldservice_sale_agreement](fieldservice_sale_agreement/) | 18.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Integrate Field Service with Sale Agreements
[fieldservice_sale_agreement_equipment_stock](fieldservice_sale_agreement_equipment_stock/) | 18.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Integrate Field Service with Sale Agreements and Stock Equipment
[fieldservice_sale_recurring](fieldservice_sale_recurring/) | 18.0.1.1.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Sell recurring field services.
[fieldservice_sale_recurring_agreement](fieldservice_sale_recurring_agreement/) | 18.0.1.0.0 |  | Field Service Recurring Agreement
[fieldservice_sale_stock](fieldservice_sale_stock/) | 18.0.1.0.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Sell stockable items linked to field service orders.
[fieldservice_sale_stock_route](fieldservice_sale_stock_route/) | 18.0.1.0.0 | <a href='https://github.com/ppyczko'><img src='https://github.com/ppyczko.png' width='32' height='32' style='border-radius:50%;' alt='ppyczko'/></a> | Link between Field Service Sale Stock and Route
[fieldservice_size](fieldservice_size/) | 18.0.1.0.0 | <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Manage Sizes for Field Service Locations and Orders
[fieldservice_skill](fieldservice_skill/) | 18.0.1.0.0 | <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Manage your Field Service workers skills
[fieldservice_stage_server_action](fieldservice_stage_server_action/) | 18.0.1.1.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> | Execute server actions when reaching a Field Service stage
[fieldservice_stock](fieldservice_stock/) | 18.0.2.0.0 | <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> | Integrate the logistics operations with Field Service
[fieldservice_timesheet](fieldservice_timesheet/) | 18.0.1.0.0 |  | Timesheet on Field Service Orders
[fieldservice_vehicle](fieldservice_vehicle/) | 18.0.1.0.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Manage Field Service vehicles and assign drivers

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/fleet


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/fleet&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/fleet/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/fleet/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/fleet/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/fleet/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/fleet/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/fleet)
[![Translation Status](https://translation.odoo-community.org/widgets/fleet-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/fleet-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# fleet

fleet

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[fleet_vehicle_calendar_year](fleet_vehicle_calendar_year/) | 18.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | This module extends the fleet management functionality. Allows the registration of the vehicle's calendar year.
[fleet_vehicle_category](fleet_vehicle_category/) | 18.0.1.0.0 |  | Add category definition for vehicles.
[fleet_vehicle_configuration](fleet_vehicle_configuration/) | 18.0.1.0.0 |  | add vehicle configuration capacity
[fleet_vehicle_fuel_capacity](fleet_vehicle_fuel_capacity/) | 18.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | This module extends the functionality of fleet management. It allows the registration of a vehicle's fuel capacity.
[fleet_vehicle_fuel_type_ethanol](fleet_vehicle_fuel_type_ethanol/) | 18.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | This module extends the fleet management functionality. This adds ethanol as another type of fuel to be used by a vehicle in the fleet.
[fleet_vehicle_history_date_end](fleet_vehicle_history_date_end/) | 18.0.1.0.0 | <a href='https://github.com/mamcode'><img src='https://github.com/mamcode.png' width='32' height='32' style='border-radius:50%;' alt='mamcode'/></a> <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Automatically assign date end in vehicle history when a new driver is assigned.
[fleet_vehicle_inspection](fleet_vehicle_inspection/) | 18.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | This module extends the Fleet module allowing the registration of vehicle entry and exit inspections.
[fleet_vehicle_inspection_template](fleet_vehicle_inspection_template/) | 18.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | This module extend module fleet_vehicle_inspection enable inspection templates feature
[fleet_vehicle_log_fuel](fleet_vehicle_log_fuel/) | 18.0.1.0.0 |  | Add Log Fuels for your vehicles.
[fleet_vehicle_ownership](fleet_vehicle_ownership/) | 18.0.1.0.0 | <a href='https://github.com/cubells'><img src='https://github.com/cubells.png' width='32' height='32' style='border-radius:50%;' alt='cubells'/></a> | Add vehicle ownership, linking partners to vehicles
[fleet_vehicle_purchase](fleet_vehicle_purchase/) | 18.0.1.0.0 |  | Allow to integrate Purcase with Fleet Vehicles
[fleet_vehicle_service_activity](fleet_vehicle_service_activity/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Activity alerts for fleet services
[fleet_vehicle_service_kanban](fleet_vehicle_service_kanban/) | 18.0.1.0.0 | <a href='https://github.com/mamcode'><img src='https://github.com/mamcode.png' width='32' height='32' style='border-radius:50%;' alt='mamcode'/></a> <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Add features of kanban to logs of vehicle services.
[fleet_vehicle_service_services](fleet_vehicle_service_services/) | 18.0.1.0.0 |  | Add subservices in Services.
[fleet_vehicle_stock](fleet_vehicle_stock/) | 18.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | This module is an add-on for the Fleet application in Odoo. It allows you to track your Fleet Vehicles in stock moves.
[fleet_vehicle_usage](fleet_vehicle_usage/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Fleet Vehicle Usage

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/geospatial


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/geospatial&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/geospatial/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/geospatial/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/geospatial/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/geospatial/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/geospatial/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/geospatial)
[![Translation Status](https://translation.odoo-community.org/widgets/geospatial-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/geospatial-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# geospatial

geospatial

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_geoengine](base_geoengine/) | 18.0.1.2.0 |  | Geospatial support for Odoo
[web_leaflet_draw_lib](web_leaflet_draw_lib/) | 18.0.1.0.0 | <a href='https://github.com/NL66278''><img src='https://github.com/NL66278'.png' width='32' height='32' style='border-radius:50%;' alt='NL66278''/></a> | Bring leaflet.draw.js library in odoo.
[web_leaflet_lib](web_leaflet_lib/) | 18.0.1.1.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Bring leaflet.js librairy in odoo.
[web_view_leaflet_map](web_view_leaflet_map/) | 18.0.1.1.2 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add new 'leaflet_map' view, to display markers.
[web_view_leaflet_map_partner](web_view_leaflet_map_partner/) | 18.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add a leaflet map view for partners model

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/helpdesk


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# helpdesk
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/helpdesk&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/helpdesk/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/helpdesk/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/helpdesk/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/helpdesk/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/helpdesk/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/helpdesk)
[![Translation Status](https://translation.odoo-community.org/widgets/helpdesk-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/helpdesk-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

helpdesk

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[helpdesk_mgmt](helpdesk_mgmt/) | 18.0.1.17.0 |  | Helpdesk
[helpdesk_mgmt_activity](helpdesk_mgmt_activity/) | 18.0.1.0.0 |  | Create Activities for Odoo records from the Helpdesk
[helpdesk_mgmt_crm](helpdesk_mgmt_crm/) | 18.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Links helpdesk tickets with leads
[helpdesk_mgmt_fieldservice](helpdesk_mgmt_fieldservice/) | 18.0.1.1.3 |  | Create service orders from a ticket
[helpdesk_mgmt_fieldservice_equipment](helpdesk_mgmt_fieldservice_equipment/) | 18.0.1.0.0 |  | Helpdesk Ticket Field Service Equipment
[helpdesk_mgmt_fieldservice_equipment_warranty](helpdesk_mgmt_fieldservice_equipment_warranty/) | 18.0.1.0.0 |  | Helpdesk Ticket Equipment Warranty
[helpdesk_mgmt_fieldservice_project](helpdesk_mgmt_fieldservice_project/) | 18.0.1.0.0 |  | Helpdesk Mgmt Fieldservice Project
[helpdesk_mgmt_merge](helpdesk_mgmt_merge/) | 18.0.1.0.2 |  | Wizard to merge helpdesk tickets
[helpdesk_mgmt_portal_follower](helpdesk_mgmt_portal_follower/) | 18.0.1.0.0 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> <a href='https://github.com/ppyczko'><img src='https://github.com/ppyczko.png' width='32' height='32' style='border-radius:50%;' alt='ppyczko'/></a> <a href='https://github.com/mpascuall'><img src='https://github.com/mpascuall.png' width='32' height='32' style='border-radius:50%;' alt='mpascuall'/></a> | Add ticket followers from website portal
[helpdesk_mgmt_project](helpdesk_mgmt_project/) | 18.0.1.3.0 |  | Add the option to select project in the tickets.
[helpdesk_mgmt_project_domain](helpdesk_mgmt_project_domain/) | 18.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Enable to set a project domain on ticket
[helpdesk_mgmt_rating](helpdesk_mgmt_rating/) | 18.0.1.0.2 |  | This module allows customer to rate the assistance received on a ticket.
[helpdesk_mgmt_sale](helpdesk_mgmt_sale/) | 18.0.2.1.1 |  | Add the option to select project in the sale orders.
[helpdesk_mgmt_sale_project](helpdesk_mgmt_sale_project/) | 18.0.1.0.0 |  | Helpdesk Sale Project
[helpdesk_mgmt_sla](helpdesk_mgmt_sla/) | 18.0.2.1.0 |  | Add SLA to the tickets for Helpdesk Management.
[helpdesk_mgmt_stage_validation](helpdesk_mgmt_stage_validation/) | 18.0.1.0.0 |  | Validate input data when reaching a Helpdesk Ticket stage
[helpdesk_mgmt_template](helpdesk_mgmt_template/) | 18.0.1.0.0 |  | Create Helpdesk Ticket Template
[helpdesk_mgmt_timesheet](helpdesk_mgmt_timesheet/) | 18.0.1.1.3 |  | Add HR Timesheet to the tickets for Helpdesk Management.
[helpdesk_motive](helpdesk_motive/) | 18.0.1.0.0 | <a href='https://github.com/nelsonramirezs'><img src='https://github.com/nelsonramirezs.png' width='32' height='32' style='border-radius:50%;' alt='nelsonramirezs'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Keep the motive
[helpdesk_portal_priority](helpdesk_portal_priority/) | 18.0.1.0.0 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | Helpdesk Portal Priority
[helpdesk_portal_restriction](helpdesk_portal_restriction/) | 18.0.1.0.0 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | Helpdesk Portal Restriction
[helpdesk_product](helpdesk_product/) | 18.0.1.1.0 |  | Add the option to select product in the tickets.
[helpdesk_ticket_close_inactive](helpdesk_ticket_close_inactive/) | 18.0.1.1.1 | <a href='https://github.com/miquelalzanillas'><img src='https://github.com/miquelalzanillas.png' width='32' height='32' style='border-radius:50%;' alt='miquelalzanillas'/></a> | Helpdesk Ticket Close Inactive
[helpdesk_ticket_open_tab](helpdesk_ticket_open_tab/) | 18.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Helpdesk Ticket Open Tab
[helpdesk_ticket_partner_response](helpdesk_ticket_partner_response/) | 18.0.1.1.1 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Change ticket stage when partner response
[helpdesk_ticket_related](helpdesk_ticket_related/) | 18.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Link tickets to each other
[helpdesk_timesheet_time_type](helpdesk_timesheet_time_type/) | 18.0.1.0.1 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | Helpdesk Timesheet Time Type
[helpdesk_type](helpdesk_type/) | 18.0.1.2.1 | <a href='https://github.com/nelsonramirezs'><img src='https://github.com/nelsonramirezs.png' width='32' height='32' style='border-radius:50%;' alt='nelsonramirezs'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Add a type to your tickets
[helpdesk_type_sla](helpdesk_type_sla/) | 18.0.1.0.0 |  | Helpdesk Type SLA

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/hr


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/hr&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/hr/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/hr/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/hr/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/hr/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/hr/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/hr)
[![Translation Status](https://translation.odoo-community.org/widgets/hr-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/hr-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# hr

hr

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[hr_appraisal_oca](hr_appraisal_oca/) | 18.0.1.1.0 | <a href='https://github.com/ebauza'><img src='https://github.com/ebauza.png' width='32' height='32' style='border-radius:50%;' alt='ebauza'/></a> <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Module for managing employee appraisals
[hr_collective_agreement](hr_collective_agreement/) | 18.0.1.0.0 |  | Create and manage collective agreements
[hr_collective_agreement_partner](hr_collective_agreement_partner/) | 18.0.1.0.0 |  | Partner integration for collective agreements
[hr_contract_employee_calendar_planning](hr_contract_employee_calendar_planning/) | 18.0.1.0.0 |  | Hr Contract Employee Calendar Planning
[hr_contract_reference](hr_contract_reference/) | 18.0.1.0.0 |  | HR Contract Reference
[hr_contract_renew](hr_contract_renew/) | 18.0.1.0.0 |  | Generate a new contract using an existing contract as a base
[hr_course](hr_course/) | 18.0.1.0.0 |  | This module allows your to manage employee's training courses
[hr_department_code](hr_department_code/) | 18.0.1.0.0 |  | HR department code
[hr_employee_age](hr_employee_age/) | 18.0.1.0.0 |  | Age field for employee
[hr_employee_bank_restrict](hr_employee_bank_restrict/) | 18.0.1.0.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Restrict employee bank account in employee partner
[hr_employee_birthday_mail](hr_employee_birthday_mail/) | 18.0.1.0.0 |  | Automating birthday mail messages and fostering for a positive work environment.
[hr_employee_calendar_planning](hr_employee_calendar_planning/) | 18.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Employee Calendar Planning
[hr_employee_document](hr_employee_document/) | 18.0.1.0.0 |  | Documents attached to the employee profile
[hr_employee_firstname](hr_employee_firstname/) | 18.0.1.0.1 | <a href='https://github.com/Savoir-faire Linux'><img src='https://github.com/Savoir-faire Linux.png' width='32' height='32' style='border-radius:50%;' alt='Savoir-faire Linux'/></a> <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Adds First Name to Employee
[hr_employee_id](hr_employee_id/) | 18.0.1.0.0 |  | Employee ID
[hr_employee_language](hr_employee_language/) | 18.0.1.0.0 |  | HR Employee Language
[hr_employee_medical_examination](hr_employee_medical_examination/) | 18.0.1.1.0 |  | Adds information about employee's medical examinations
[hr_employee_partner_external](hr_employee_partner_external/) | 18.0.1.0.0 |  | Associate an external Partner to Employee
[hr_employee_phone_extension](hr_employee_phone_extension/) | 18.0.1.0.0 |  | Employee Phone Extension
[hr_employee_ppe](hr_employee_ppe/) | 18.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> <a href='https://github.com/eduaparicio'><img src='https://github.com/eduaparicio.png' width='32' height='32' style='border-radius:50%;' alt='eduaparicio'/></a> | Personal Protective Equipment (PPE) Management
[hr_employee_relative](hr_employee_relative/) | 18.0.1.0.1 |  | Allows storing information about employee's family
[hr_employee_second_lastname](hr_employee_second_lastname/) | 18.0.1.0.0 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Split Name in First Name, Father's Last Name and Mother's Last Name
[hr_employee_service](hr_employee_service/) | 18.0.1.0.0 |  | Employee service information & duration
[hr_employee_service_contract](hr_employee_service_contract/) | 18.0.1.0.0 |  | Employee service information & duration based on employee's contracts
[hr_employee_ssn](hr_employee_ssn/) | 18.0.1.0.0 |  | View/edit employee's SIN field
[hr_job_category](hr_job_category/) | 18.0.1.0.0 |  | Adds tags to employee through contract and job position
[hr_personal_equipment_request](hr_personal_equipment_request/) | 18.0.1.0.0 |  | This addon allows to manage employee personal equipment
[hr_professional_category](hr_professional_category/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | HR Professional Category

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/hr-attendance


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/hr-attendance&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/hr-attendance/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/hr-attendance/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/hr-attendance/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/hr-attendance/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/hr-attendance/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/hr-attendance)
[![Translation Status](https://translation.odoo-community.org/widgets/hr-attendance-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/hr-attendance-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# hr-attendance

hr-attendance

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[hr_attendance_calendar_view](hr_attendance_calendar_view/) | 18.0.1.0.0 |  | This module adds the calendar view as an option to display attendance
[hr_attendance_reason](hr_attendance_reason/) | 18.0.1.0.1 |  | HR Attendance Reason
[hr_attendance_report_theoretical_time](hr_attendance_report_theoretical_time/) | 18.0.1.2.0 |  | Theoretical vs Attended Time Analysis
[hr_attendance_rest_time_included](hr_attendance_rest_time_included/) | 18.0.1.0.0 |  | Rest time of employee's is included during their working hours
[hr_attendance_rfid](hr_attendance_rfid/) | 18.0.1.0.0 |  | HR Attendance RFID
[hr_contract_update_overtime](hr_contract_update_overtime/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Update Overtime from HR Contract

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/hr-expense


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/hr-expense&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/hr-expense/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/hr-expense/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/hr-expense/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/hr-expense/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/hr-expense/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/hr-expense)
[![Translation Status](https://translation.odoo-community.org/widgets/hr-expense-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/hr-expense-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# hr-expense

hr-expense

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[hr_expense_advance_clearing](hr_expense_advance_clearing/) | 18.0.1.0.3 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Employee Advance and Clearing
[hr_expense_advance_clearing_sequence](hr_expense_advance_clearing_sequence/) | 18.0.1.0.0 |  | HR Expense Advance Clearing Sequence
[hr_expense_cancel](hr_expense_cancel/) | 18.0.1.0.0 |  | Hr expense cancel
[hr_expense_exception](hr_expense_exception/) | 18.0.1.0.0 | <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Custom exceptions on expense report
[hr_expense_invoice](hr_expense_invoice/) | 18.0.1.0.3 |  | Supplier invoices on HR expenses
[hr_expense_payment](hr_expense_payment/) | 18.0.1.0.0 |  | HR Expense Payment
[hr_expense_petty_cash](hr_expense_petty_cash/) | 18.0.1.0.0 |  | Petty Cash
[hr_expense_sequence](hr_expense_sequence/) | 18.0.1.0.0 |  | HR expense sequence
[hr_expense_sequence_option](hr_expense_sequence_option/) | 18.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Manage sequence options for hr.expense.sheet
[hr_expense_tier_validation](hr_expense_tier_validation/) | 18.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Expense Tier Validation
[hr_expense_vendor_receipt](hr_expense_vendor_receipt/) | 18.0.1.0.0 | <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Allow to create Vendor Receipt from Hr Expense

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/hr-holidays


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/hr-holidays&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/hr-holidays/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/hr-holidays/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/hr-holidays/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/hr-holidays/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/hr-holidays/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/hr-holidays)
[![Translation Status](https://translation.odoo-community.org/widgets/hr-holidays-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/hr-holidays-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# hr-holidays

hr-holidays

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[hr_holidays_leave_repeated](hr_holidays_leave_repeated/) | 18.0.1.0.0 |  | Define periodical leaves
[hr_holidays_leave_report_calendar_type](hr_holidays_leave_report_calendar_type/) | 18.0.1.0.0 |  | Adds leave type filter to Time Off Overview calendar
[hr_holidays_natural_period](hr_holidays_natural_period/) | 18.0.1.0.5 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Apply natural days in holidays
[hr_holidays_public](hr_holidays_public/) | 18.0.1.0.6 |  | Manage Public Holidays
[hr_holidays_public_city](hr_holidays_public_city/) | 18.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | HR Holidays Public City
[hr_holidays_settings](hr_holidays_settings/) | 18.0.1.0.0 |  | Enables Settings Form for HR Holidays.
[resource_calendar_flexible_exclude_weekend](resource_calendar_flexible_exclude_weekend/) | 18.0.1.0.0 |  | Resource Calendar Flexible Hours Exclude Weekend
[resource_leaves_geographic](resource_leaves_geographic/) | 18.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Add geographic State to Resource Calendar Leaves

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/infrastructure


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/infrastructure&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/infrastructure/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/infrastructure/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/infrastructure/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/infrastructure/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/infrastructure/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/infrastructure)
[![Translation Status](https://translation.odoo-community.org/widgets/infrastructure-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/infrastructure-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# infrastructure

infrastructure

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_dns_infrastructure](base_dns_infrastructure/) | 18.0.1.0.0 |  | Base module for DNS infrastructure

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/interface-git


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/interface-github&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/interface-github/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/interface-github/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/interface-github/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/interface-github/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/interface-github/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/interface-github)
[![Translation Status](https://translation.odoo-community.org/widgets/interface-github-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/interface-github-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# interface-github

interface-github

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[github_connector](github_connector/) | 18.0.1.0.1 |  | Synchronize information from Github repositories
[github_connector_odoo](github_connector_odoo/) | 18.0.1.0.2 |  | Analyze Odoo modules information from Github repositories

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/intrastat-extrastat


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/intrastat-extrastat&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/intrastat-extrastat/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/intrastat-extrastat/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/intrastat-extrastat/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/intrastat-extrastat/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/intrastat-extrastat/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/intrastat-extrastat)
[![Translation Status](https://translation.odoo-community.org/widgets/intrastat-extrastat-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/intrastat-extrastat-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# intrastat-extrastat

intrastat-extrastat

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[intrastat_base](intrastat_base/) | 18.0.2.0.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/luc-demeyer'><img src='https://github.com/luc-demeyer.png' width='32' height='32' style='border-radius:50%;' alt='luc-demeyer'/></a> | Base module for Intrastat reporting
[intrastat_product](intrastat_product/) | 18.0.1.3.3 |  | Base module for Intrastat Product
[product_harmonized_system](product_harmonized_system/) | 18.0.1.2.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/luc-demeyer'><img src='https://github.com/luc-demeyer.png' width='32' height='32' style='border-radius:50%;' alt='luc-demeyer'/></a> | Base module for Product Import/Export reports
[product_harmonized_system_delivery](product_harmonized_system_delivery/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/luc-demeyer'><img src='https://github.com/luc-demeyer.png' width='32' height='32' style='border-radius:50%;' alt='luc-demeyer'/></a> | Hide native hs_code field provided by the delivery module
[product_harmonized_system_stock](product_harmonized_system_stock/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/luc-demeyer'><img src='https://github.com/luc-demeyer.png' width='32' height='32' style='border-radius:50%;' alt='luc-demeyer'/></a> | Adds a menu entry for H.S. codes
[product_harmonized_system_tax_rate](product_harmonized_system_tax_rate/) | 18.0.1.0.0 | <a href='https://github.com/nayatec'><img src='https://github.com/nayatec.png' width='32' height='32' style='border-radius:50%;' alt='nayatec'/></a> <a href='https://github.com/hparfr'><img src='https://github.com/hparfr.png' width='32' height='32' style='border-radius:50%;' alt='hparfr'/></a> | Add a notion of tax rate linked to an H.S. Code and Country.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/iot


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/iot&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/iot/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/iot/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/iot/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/iot/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/iot/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/iot)
[![Translation Status](https://translation.odoo-community.org/widgets/iot-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/iot-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# iot

iot

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[iot_oca](iot_oca/) | 18.0.1.0.1 |  | IoT base module

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/knowledge


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/knowledge&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/knowledge/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/knowledge/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/knowledge/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/knowledge/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/knowledge/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/knowledge)
[![Translation Status](https://translation.odoo-community.org/widgets/knowledge-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/knowledge-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# knowledge

knowledge

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[attachment_preview](attachment_preview/) | 18.0.1.0.0 |  | Preview attachments supported by Viewer.js
[attachment_zipped_download](attachment_zipped_download/) | 18.0.1.0.0 |  | Attachment Zipped Download
[document_knowledge](document_knowledge/) | 18.0.1.0.2 |  | Documents Knowledge
[document_page](document_page/) | 18.0.2.1.0 |  | Document Page
[document_page_access_group](document_page_access_group/) | 18.0.1.0.1 |  | Choose groups to access document pages
[document_page_access_group_user_role](document_page_access_group_user_role/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Document Page Access Group User Role
[document_page_approval](document_page_approval/) | 18.0.1.1.1 |  | Document Page Approval
[document_page_group](document_page_group/) | 18.0.1.0.0 |  | Define access groups on documents
[document_page_partner](document_page_partner/) | 18.0.1.0.0 |  | Allows to link doucment pages to a partner
[document_page_product](document_page_product/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | This module links document pages to products
[document_page_project](document_page_project/) | 18.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | This module links document pages to projects
[document_page_project_task](document_page_project_task/) | 18.0.2.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | This module links document pages to project tasks
[document_page_reference](document_page_reference/) | 18.0.2.1.2 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Include references on document pages
[document_page_tag](document_page_tag/) | 18.0.1.0.0 |  | Allows you to assign tags or keywords to pages and search for them afterwards
[document_url](document_url/) | 18.0.1.0.1 |  | URL attachment

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-belgium


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-belgium&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-belgium/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-belgium/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-belgium/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-belgium/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-belgium/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-belgium)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-belgium-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-belgium-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-belgium

l10n-belgium

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_statement_import_coda](account_statement_import_coda/) | 18.0.1.0.0 |  | Import CODA Bank Statement
[companyweb_base](companyweb_base/) | 18.0.1.1.2 | <a href='https://github.com/xavier-bouquiaux'><img src='https://github.com/xavier-bouquiaux.png' width='32' height='32' style='border-radius:50%;' alt='xavier-bouquiaux'/></a> | Know who you are dealing with. Enhance Odoo partner data from companyweb.be.
[companyweb_payment_info](companyweb_payment_info/) | 18.0.1.0.1 | <a href='https://github.com/xavier-bouquiaux'><img src='https://github.com/xavier-bouquiaux.png' width='32' height='32' style='border-radius:50%;' alt='xavier-bouquiaux'/></a> | Send your customer payment information to Companyweb
[l10n_be_mis_reports](l10n_be_mis_reports/) | 18.0.1.0.0 |  | MIS Builder templates for the Belgium P&L, Balance Sheets and VAT Declaration
[l10n_be_mis_reports_xml](l10n_be_mis_reports_xml/) | 18.0.1.0.1 |  | Exports MIS Builder templates VAT Declaration as XML to load on the administration websites.
[l10n_be_partner_identification](l10n_be_partner_identification/) | 18.0.1.0.0 |  | Belgium Partner Identification Numbers
[l10n_be_vat_reports](l10n_be_vat_reports/) | 18.0.1.0.0 |  | Belgium VAT Reports

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-brazil


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# l10n-brazil
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-brazil&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-brazil/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-brazil/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-brazil/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-brazil/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-brazil/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-brazil)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-brazil-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-brazil-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

l10n-brazil

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_br_account](l10n_br_account/) | 18.0.1.0.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Invoicing and accounting entries for Brazil
[l10n_br_account_due_list](l10n_br_account_due_list/) | 18.0.1.0.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Brazilian Account Due List
[l10n_br_account_fleet](l10n_br_account_fleet/) | 18.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Brazilian Localization Account Fleet
[l10n_br_account_payment_order](l10n_br_account_payment_order/) | 18.0.1.0.4 | <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> | Brazilian Payment Order
[l10n_br_base](l10n_br_base/) | 18.0.1.4.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Customization of base module for implementations in Brazil.
[l10n_br_base_l10n_br_compat](l10n_br_base_l10n_br_compat/) | 18.0.2.0.0 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Compatibility with the l10n_br module
[l10n_br_cnpj_search](l10n_br_cnpj_search/) | 18.0.1.1.2 |  | Integração com os Webservices da ReceitaWS e SerPro
[l10n_br_coa](l10n_br_coa/) | 18.0.1.0.3 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | Base do Planos de Contas brasileiros
[l10n_br_coa_generic](l10n_br_coa_generic/) | 18.0.1.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | Plano de Contas para empresas do Regime normal (Micro e pequenas empresas)
[l10n_br_coa_simple](l10n_br_coa_simple/) | 18.0.1.0.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Plano de Contas ITG 1000 para Microempresas e Empresa de Pequeno Porte
[l10n_br_crm](l10n_br_crm/) | 18.0.1.2.1 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> | Brazilian Localization CRM
[l10n_br_crm_cnpj_search](l10n_br_crm_cnpj_search/) | 18.0.1.1.0 | <a href='https://github.com/corredato'><img src='https://github.com/corredato.png' width='32' height='32' style='border-radius:50%;' alt='corredato'/></a> <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | CNPJ search in CRM Lead
[l10n_br_cte_spec](l10n_br_cte_spec/) | 18.0.1.1.0 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | CT-e abstract models generated by xsdata-odoo from the official xsd
[l10n_br_currency_rate_update](l10n_br_currency_rate_update/) | 18.0.1.0.2 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Update exchange rates using OCA modules for Brazil
[l10n_br_fiscal](l10n_br_fiscal/) | 18.0.7.5.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Fiscal module/tax engine for Brazil
[l10n_br_fiscal_certificate](l10n_br_fiscal_certificate/) | 18.0.1.3.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | A1 fiscal certificate management for Brazil
[l10n_br_fiscal_closing](l10n_br_fiscal_closing/) | 18.0.1.0.1 |  | Period fiscal closing
[l10n_br_fiscal_dfe](l10n_br_fiscal_dfe/) | 18.0.1.3.0 |  | Distribuição de documentos fiscais
[l10n_br_fiscal_edi](l10n_br_fiscal_edi/) | 18.0.2.0.1 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | Common EDI fiscal features
[l10n_br_fiscal_notification](l10n_br_fiscal_notification/) | 18.0.1.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | Define fiscal document notifications
[l10n_br_hr](l10n_br_hr/) | 18.0.1.2.0 |  | Brazilian Localization HR
[l10n_br_hr_contract](l10n_br_hr_contract/) | 18.0.1.2.0 |  | Brazilian Localization HR Contract
[l10n_br_ie_search](l10n_br_ie_search/) | 18.0.1.0.0 |  | Integração com a API SintegraWS e SEFAZ
[l10n_br_mdfe_spec](l10n_br_mdfe_spec/) | 18.0.1.0.1 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | MDF-e abstract models generated by xsdata-odoo from the official xsd
[l10n_br_mis_report](l10n_br_mis_report/) | 18.0.1.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | Templates de relatórios contábeis brasileiros: Balanço Patrimonial e DRE
[l10n_br_nfe](l10n_br_nfe/) | 18.0.1.0.1 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Eletronic Invoicing for Brazil / NF-e
[l10n_br_nfe_spec](l10n_br_nfe_spec/) | 18.0.2.0.2 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | NF-e abstract models generated by xsdata-odoo from the official xsd
[l10n_br_nfse](l10n_br_nfse/) | 18.0.5.2.1 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Root electronic invoice for service / NFS-e module
[l10n_br_nfse_focus](l10n_br_nfse_focus/) | 18.0.3.1.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | NFS-e (FocusNFE)
[l10n_br_resource](l10n_br_resource/) | 18.0.1.1.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/lfdivino'><img src='https://github.com/lfdivino.png' width='32' height='32' style='border-radius:50%;' alt='lfdivino'/></a> | This module extend core resource to create important brazilian informations. Define a Brazilian calendar and some tools to compute dates used in financial and payroll modules
[l10n_br_sped_base](l10n_br_sped_base/) | 18.0.1.1.0 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Framework abstrato pro SPED
[l10n_br_stock](l10n_br_stock/) | 18.0.1.0.0 |  | Brazilian Localization Warehouse
[l10n_br_zip](l10n_br_zip/) | 18.0.1.1.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Brazilian Localisation ZIP Codes
[spec_driven_model](spec_driven_model/) | 18.0.1.1.2 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | XML binding for Odoo: XML to Odoo models and models to XML.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-bulgaria


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-bulgaria&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-bulgaria/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-bulgaria/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-bulgaria/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-bulgaria/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-bulgaria/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-bulgaria)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-bulgaria-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-bulgaria-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-bulgaria

OCA addons for Bulgarian localization in Odoo 18.0.

Stable release policy for `l10n-bulgaria-oca` modules: stable branches are published each March, in the year following the official Odoo release (e.g., Odoo 19 stable release in March 2027). For beta or earlier versions, follow forked repositories maintained by `rosenvladimirov` or other developers.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_bg_account_reconcile_patch](l10n_bg_account_reconcile_patch/) | 18.0.1.0.0 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Account Reconcile Partner Regex SQL Fix
[l10n_bg_account_statement_import_mt940](l10n_bg_account_statement_import_mt940/) | 18.0.1.0.0 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Account Statement Import Mt940
[l10n_bg_address_extended](l10n_bg_address_extended/) | 18.0.1.0.1 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Bulgaria - Base address extended
[l10n_bg_bank_wallet](l10n_bg_bank_wallet/) | 18.0.1.0.2 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Secure storage of cryptographic keys and passwords for banking integrations
[l10n_bg_city](l10n_bg_city/) | 18.0.1.0.0 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Complete database of Bulgarian cities, municipalities, and administrative-territorial units with EKATTE codes.
[l10n_bg_company_registry](l10n_bg_company_registry/) | 18.0.2.0.1 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Real-time integration with Bulgarian Trade Registry (portal.registryagency.bg)
[l10n_bg_config](l10n_bg_config/) | 18.0.8.0.5 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | This module allows you to install and configure all the localization modules related to Bulgaria.
[l10n_bg_erp_net_fp](l10n_bg_erp_net_fp/) | 18.0.7.0.2 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Integration with ERP.BG fiscal printers through ErpNet.FP server. Supports real-time fiscal receipt printing and status monitoring.
[l10n_bg_hr_holidays](l10n_bg_hr_holidays/) | 18.0.1.0.4 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Bulgarian localization for HR Holidays
[l10n_bg_invoice_copy](l10n_bg_invoice_copy/) | 18.0.1.0.0 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Add COPY watermark to Bulgarian invoice reports
[l10n_bg_mrp_multilang](l10n_bg_mrp_multilang/) | 18.0.1.0.0 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Multilanguage filed for mrp_workcenter name
[l10n_bg_multilang](l10n_bg_multilang/) | 18.0.0.1.0 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Multi Language Partner, Company, Employee
[l10n_bg_payroll_classifications](l10n_bg_payroll_classifications/) | 18.0.6.0.0 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Bulgarian localization for HR payroll with NKPD and Economic Activity classifications
[l10n_bg_project_multilang](l10n_bg_project_multilang/) | 18.0.1.0.0 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Add multilingual support for project task fields in Bulgarian localization
[l10n_bg_report_stock](l10n_bg_report_stock/) | 18.0.1.0.0 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Bulgaria - Accepted delivery documents in stock picking
[l10n_bg_report_theme](l10n_bg_report_theme/) | 18.0.5.0.4 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Professional report theme with modular section-based layout for Bulgarian business documents.
[l10n_bg_reports_audit](l10n_bg_reports_audit/) | 18.0.12.0.3 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> <a href='https://github.com/deyanlyubenov'><img src='https://github.com/deyanlyubenov.png' width='32' height='32' style='border-radius:50%;' alt='deyanlyubenov'/></a> | Technical base module for Bulgarian accounting reports - SQL queries and tag configurations
[l10n_bg_reports_config](l10n_bg_reports_config/) | 18.0.9.0.2 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> <a href='https://github.com/deyanlyubenov'><img src='https://github.com/deyanlyubenov.png' width='32' height='32' style='border-radius:50%;' alt='deyanlyubenov'/></a> | Configuration module for Bulgarian Accounting Reports - Odoo 18.0 specific views and wizards
[l10n_bg_sale_order_delivery_note](l10n_bg_sale_order_delivery_note/) | 18.0.1.0.0 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Generate Accepted Delivery Report for Bulgarian Sale Orders
[l10n_bg_stock_sale_line_description](l10n_bg_stock_sale_line_description/) | 18.0.1.0.1 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Show sale order line description on pickings and delivery slips
[l10n_bg_tariff_code](l10n_bg_tariff_code/) | 18.0.3.0.10 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | TARIC/HS/CN Code Management with EU API Integration
[l10n_bg_tax_offices](l10n_bg_tax_offices/) | 18.0.1.0.0 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Add in partners tax offices and department of NRA Bulgaria
[markdown_viewer_locale](markdown_viewer_locale/) | 18.0.3.0.4 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | View localized Markdown files based on user language
[partner_multilang](partner_multilang/) | 18.0.3.0.4 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | Automatic multilingual partner names with intelligent transliteration and language detection.
[taric_ai_classifier](taric_ai_classifier/) | 18.0.1.0.3 | <a href='https://github.com/rosenvladimirov'><img src='https://github.com/rosenvladimirov.png' width='32' height='32' style='border-radius:50%;' alt='rosenvladimirov'/></a> | AI-powered automatic TARIC and INTRASTAT code classification for products

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [LGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.

## Maintainer

![Rosen Vladimirov](https://github.com/rosenvladimirov.png?size=80)


---

## From OCA/l10n-colombia


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-colombia&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-colombia/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-colombia/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-colombia/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-colombia/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-colombia/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-colombia)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-colombia-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-colombia-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-colombia

l10n-colombia

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_co_currency_rate_update](l10n_co_currency_rate_update/) | 18.0.1.0.0 |  | Tasa de cambio de Superfinanciera para Colombia
[l10n_co_electronic_invoice](l10n_co_electronic_invoice/) | 18.0.1.0.0 |  | Campos y datos de pre-configuración para la Factura Electrónica en Colombia
[l10n_co_electronic_invoice_self](l10n_co_electronic_invoice_self/) | 18.0.2.0.0 |  | Integración con la DIAN Colombia para la emisión de Facturas Electrónicas en modo de operación software propio
[l10n_co_withholding_advance](l10n_co_withholding_advance/) | 18.0.1.0.0 |  | Soporte para retenciones anticipadas en la contabilidad colombiana.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-ecuador


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-ecuador&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-ecuador/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-ecuador/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-ecuador/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-ecuador/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-ecuador/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-ecuador)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-ecuador-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-ecuador-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-ecuador

l10n-ecuador

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_ec_base](l10n_ec_base/) | 18.0.1.0.0 |  | Ecuadorian Localization

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-finland


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-finland&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-finland/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-finland/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-finland/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-finland/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-finland/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-finland)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-finland-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-finland-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-finland

l10n-finland

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_edi_finvoice](account_edi_finvoice/) | 18.0.1.0.7 |  | Import/Export Finvoice 3.0 invoices
[connector_apix](connector_apix/) | 18.0.1.0.2 |  | APIX EDI connector for receiving and sending eInvoices
[l10n_fi_banks](l10n_fi_banks/) | 18.0.1.0.0 |  | Finnish banks and their addresses
[l10n_fi_edicode](l10n_fi_edicode/) | 18.0.1.0.1 |  | Adds EDI code field and operators
[l10n_fi_sale_refund_payment_reference](l10n_fi_sale_refund_payment_reference/) | 18.0.1.0.0 |  | Automatically generate payment references for sale refunds

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-france


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-france&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-france/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-france/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-france/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-france/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-france/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-france)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-france-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-france-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-france

l10n-france

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_balance_ebp_csv_export](account_balance_ebp_csv_export/) | 18.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Export the trial balance in EBP format (CSV or XLSX)
[account_payment_fr_lcr](account_payment_fr_lcr/) | 18.0.1.2.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Create French LCR CFONB files
[account_statement_import_fr_cfonb](account_statement_import_fr_cfonb/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import CFONB bank statements files in Odoo
[country_fr](country_fr/) | 18.0.1.0.0 |  | Set FR country on `base.main_company` record to set up French localisation.
[l10n_fr_account_invoice_facturx](l10n_fr_account_invoice_facturx/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | France-specific module to generate Factur-X invoices
[l10n_fr_account_invoice_import_facturx](l10n_fr_account_invoice_import_facturx/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | France-specific module to import Factur-X invoices
[l10n_fr_account_invoice_import_simple_pdf](l10n_fr_account_invoice_import_simple_pdf/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Invoice import simple PDF: match partners using SIREN
[l10n_fr_account_payment_intl_credit_transfer](l10n_fr_account_payment_intl_credit_transfer/) | 18.0.2.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Regulatory reporting codes for ISO 20022 credit transfer files
[l10n_fr_account_tax_unece](l10n_fr_account_tax_unece/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Auto-configure UNECE params on French taxes
[l10n_fr_business_document_import](l10n_fr_business_document_import/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adapt the module base_business_document_import for France
[l10n_fr_chorus_account](l10n_fr_chorus_account/) | 18.0.1.2.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Generate Chorus-compliant e-invoices and transmit them via the Chorus API
[l10n_fr_chorus_facturx](l10n_fr_chorus_facturx/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Generate Chorus-compliant Factur-X invoices
[l10n_fr_chorus_sale](l10n_fr_chorus_sale/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add checks on sale orders for Chorus Pro
[l10n_fr_cog](l10n_fr_cog/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add Code Officiel Géographique (COG) on countries
[l10n_fr_das2](l10n_fr_das2/) | 18.0.2.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | DAS2 (France)
[l10n_fr_department](l10n_fr_department/) | 18.0.2.1.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Populate Database with French Departments (Départements)
[l10n_fr_department_oversea](l10n_fr_department_oversea/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Populate Database with overseas French Departments (Départements d'outre-mer)
[l10n_fr_hr_check_ssnid](l10n_fr_hr_check_ssnid/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Check validity of Social Security Numbers in French companies
[l10n_fr_intrastat_product](l10n_fr_intrastat_product/) | 18.0.2.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | EMEBI (ex-DEB) for France
[l10n_fr_intrastat_service](l10n_fr_intrastat_service/) | 18.0.1.3.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Module for Intrastat service reporting (DES) for France
[l10n_fr_mis_reports](l10n_fr_mis_reports/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | MIS Report templates for the French P&L and Balance Sheets
[l10n_fr_pos_caisse_ap_ip](l10n_fr_pos_caisse_ap_ip/) | 18.0.1.4.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add support for Caisse-AP payment protocol used in France
[l10n_fr_siret](l10n_fr_siret/) | 18.0.1.3.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Complete support for SIRET/SIREN/NIC with checksum validation
[l10n_fr_siret_account](l10n_fr_siret_account/) | 18.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Glue module between l10n_fr_siret and account
[l10n_fr_siret_lookup](l10n_fr_siret_lookup/) | 18.0.1.1.0 | <a href='https://github.com/remi-filament'><img src='https://github.com/remi-filament.png' width='32' height='32' style='border-radius:50%;' alt='remi-filament'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Lookup partner via an API on the SIRENE directory
[l10n_fr_state](l10n_fr_state/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Populate Database with French States (Régions)

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-germany


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-germany&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-germany/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-germany/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-germany/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-germany/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-germany/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-germany)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-germany-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-germany-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-germany

l10n-germany

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[datev_export](datev_export/) | 18.0.1.0.1 |  | Export invoices and refunds as xml and pdf files zipped in DATEV format.
[datev_export_dtvf](datev_export_dtvf/) | 18.0.2.0.0 |  | Export Data for DATEV (dtvf)
[datev_export_xml](datev_export_xml/) | 18.0.1.0.0 |  | Export invoices and refunds as xml and pdf files zipped in DATEV format.
[datev_import_csv_dtvf](datev_import_csv_dtvf/) | 18.0.1.1.0 |  | Import account moves generated by external software
[l10n_de_location_nuts](l10n_de_location_nuts/) | 18.0.1.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | NUTS specific options for German
[l10n_de_mis_reports](l10n_de_mis_reports/) | 18.0.1.0.0 |  | MIS Builder templates for the German P&L and Balance Sheets (SKR03 + SKR04)
[l10n_de_tax_statement](l10n_de_tax_statement/) | 18.0.3.0.0 | <a href='https://github.com/mt-software-de'><img src='https://github.com/mt-software-de.png' width='32' height='32' style='border-radius:50%;' alt='mt-software-de'/></a> | German VAT Statement
[l10n_de_tax_statement_zm](l10n_de_tax_statement_zm/) | 18.0.2.0.0 |  | German VAT Statement Extension
[l10n_din5008_company_header_country_invisible](l10n_din5008_company_header_country_invisible/) | 18.0.1.0.1 |  | Do not display the companies country on the header of the address block
[l10n_din5008_move_name](l10n_din5008_move_name/) | 18.0.1.0.0 |  | Add Account move name on the name of the move

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-iran


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-iran&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-iran/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-iran/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-iran/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-iran/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-iran/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-iran)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-iran-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-iran-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-iran

l10n-iran

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_ir_account](l10n_ir_account/) | 18.0.1.0.0 |  | iran accounting chart and localization.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-italy


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-italy&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-italy/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-italy/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-italy/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-italy/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-italy/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-italy)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-italy-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-italy-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-italy

Canale Discord sviluppo, tutti i venerdì ore 9.30: https://discord.gg/xnrZXczzRC

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_it_abicab](l10n_it_abicab/) | 18.0.1.0.0 | <a href='https://github.com/Borruso'><img src='https://github.com/Borruso.png' width='32' height='32' style='border-radius:50%;' alt='Borruso'/></a> | Base Bank ABI/CAB codes
[l10n_it_accompanying_invoice](l10n_it_accompanying_invoice/) | 18.0.1.0.0 |  | Stampa della fattura accompagnatoria
[l10n_it_account](l10n_it_account/) | 18.0.1.0.1 |  | Modulo base usato come dipendenza di altri moduli contabili
[l10n_it_account_invoice_start_end_dates](l10n_it_account_invoice_start_end_dates/) | 18.0.1.0.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Set start/end dates on Italian tax move lines for partially/totally deductible VAT
[l10n_it_account_stamp](l10n_it_account_stamp/) | 18.0.1.2.0 |  | Gestione automatica dell'imposta di bollo
[l10n_it_account_vat_period_end_settlement](l10n_it_account_vat_period_end_settlement/) | 18.0.1.0.5 |  | Allow to create the 'VAT Settlement'.
[l10n_it_amount_to_text](l10n_it_amount_to_text/) | 18.0.1.0.0 |  | Localizza le valute in italiano per amount_to_text
[l10n_it_appointment_code](l10n_it_appointment_code/) | 18.0.1.0.0 |  | Aggiunge la tabella dei codici carica da usare nelle dichiarazioni fiscali italiane
[l10n_it_asset_management](l10n_it_asset_management/) | 18.0.1.0.0 |  | Gestione Cespiti
[l10n_it_ateco](l10n_it_ateco/) | 18.0.1.0.0 |  | ITA - Codici Ateco
[l10n_it_bill_of_entry](l10n_it_bill_of_entry/) | 18.0.1.0.0 |  | ITA - Bolle doganali
[l10n_it_central_journal_reportlab](l10n_it_central_journal_reportlab/) | 18.0.1.2.1 | <a href='https://github.com/MarcoCalcagni'><img src='https://github.com/MarcoCalcagni.png' width='32' height='32' style='border-radius:50%;' alt='MarcoCalcagni'/></a> <a href='https://github.com/Borruso'><img src='https://github.com/Borruso.png' width='32' height='32' style='border-radius:50%;' alt='Borruso'/></a> | ITA - Libro giornale - Reportlab
[l10n_it_currency_rate_update_boi](l10n_it_currency_rate_update_boi/) | 18.0.1.0.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Update exchange rates using www.bancaditalia.it
[l10n_it_delivery_note](l10n_it_delivery_note/) | 18.0.1.0.6 | <a href='https://github.com/MarcoCalcagni'><img src='https://github.com/MarcoCalcagni.png' width='32' height='32' style='border-radius:50%;' alt='MarcoCalcagni'/></a> <a href='https://github.com/aleuffre'><img src='https://github.com/aleuffre.png' width='32' height='32' style='border-radius:50%;' alt='aleuffre'/></a> <a href='https://github.com/renda-dev'><img src='https://github.com/renda-dev.png' width='32' height='32' style='border-radius:50%;' alt='renda-dev'/></a> | Crea, gestisce e fattura i DDT partendo dalle consegne
[l10n_it_delivery_note_batch](l10n_it_delivery_note_batch/) | 18.0.1.0.0 | <a href='https://github.com/MarcoCalcagni'><img src='https://github.com/MarcoCalcagni.png' width='32' height='32' style='border-radius:50%;' alt='MarcoCalcagni'/></a> <a href='https://github.com/TheMule71'><img src='https://github.com/TheMule71.png' width='32' height='32' style='border-radius:50%;' alt='TheMule71'/></a> <a href='https://github.com/Borruso'><img src='https://github.com/Borruso.png' width='32' height='32' style='border-radius:50%;' alt='Borruso'/></a> <a href='https://github.com/aleuffre'><img src='https://github.com/aleuffre.png' width='32' height='32' style='border-radius:50%;' alt='aleuffre'/></a> <a href='https://github.com/PicchiSeba'><img src='https://github.com/PicchiSeba.png' width='32' height='32' style='border-radius:50%;' alt='PicchiSeba'/></a> <a href='https://github.com/renda-dev'><img src='https://github.com/renda-dev.png' width='32' height='32' style='border-radius:50%;' alt='renda-dev'/></a> | Crea i DDT partendo da gruppi di prelievi
[l10n_it_delivery_note_customer_code](l10n_it_delivery_note_customer_code/) | 18.0.1.0.0 | <a href='https://github.com/aleuffre'><img src='https://github.com/aleuffre.png' width='32' height='32' style='border-radius:50%;' alt='aleuffre'/></a> <a href='https://github.com/renda-dev'><img src='https://github.com/renda-dev.png' width='32' height='32' style='border-radius:50%;' alt='renda-dev'/></a> <a href='https://github.com/PicchiSeba'><img src='https://github.com/PicchiSeba.png' width='32' height='32' style='border-radius:50%;' alt='PicchiSeba'/></a> | Product Customer code and name for delivery note
[l10n_it_delivery_note_order_link](l10n_it_delivery_note_order_link/) | 18.0.1.0.0 | <a href='https://github.com/andreampiovesana'><img src='https://github.com/andreampiovesana.png' width='32' height='32' style='border-radius:50%;' alt='andreampiovesana'/></a> | Crea collegamento tra i DDT e ordine di vendita/acquisto
[l10n_it_edi_doi_extension](l10n_it_edi_doi_extension/) | 18.0.1.1.1 |  | Declaration of Intent for Italy (OCA)
[l10n_it_edi_extension](l10n_it_edi_extension/) | 18.0.1.10.2 |  | E-invoice base feature
[l10n_it_edi_pec](l10n_it_edi_pec/) | 18.0.1.0.0 |  | Invio e ricezione fatture elettroniche tramite PEC
[l10n_it_edi_related_document](l10n_it_edi_related_document/) | 18.0.1.1.2 |  | Related Documents for EDI
[l10n_it_edi_sdi](l10n_it_edi_sdi/) | 18.0.1.0.0 |  | Logica condivisa per la comunicazione con lo SdI
[l10n_it_edi_sender_partner](l10n_it_edi_sender_partner/) | 18.0.1.0.0 |  | Terzo intermediario o soggetto emittete per fatturazione elettronica
[l10n_it_financial_statement_eu](l10n_it_financial_statement_eu/) | 18.0.1.0.0 | <a href='https://github.com/mktsrl'><img src='https://github.com/mktsrl.png' width='32' height='32' style='border-radius:50%;' alt='mktsrl'/></a> | ITA - Bilancio UE con XBRL
[l10n_it_financial_statements_report](l10n_it_financial_statements_report/) | 18.0.1.1.0 |  | Rendicontazione .pdf e .xls per stato patrimoniale e conto economico a sezioni contrapposte
[l10n_it_fiscalcode_sale](l10n_it_fiscalcode_sale/) | 18.0.1.0.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Mostra il codice fiscale del cliente nella stampa del preventivo
[l10n_it_intrastat](l10n_it_intrastat/) | 18.0.1.1.0 |  | Riclassificazione merci e servizi per dichiarazioni Intrastat
[l10n_it_intrastat_statement](l10n_it_intrastat_statement/) | 18.0.1.0.0 |  | Dichiarazione Intrastat per l'Agenzia delle Dogane
[l10n_it_location_nuts](l10n_it_location_nuts/) | 18.0.1.0.0 |  | Opzioni NUTS specifiche per l'Italia
[l10n_it_riba_oca](l10n_it_riba_oca/) | 18.0.1.2.1 |  | Ricevute bancarie
[l10n_it_vat_registries](l10n_it_vat_registries/) | 18.0.1.2.1 |  | ITA - Registri IVA
[l10n_it_vat_settlement_communication](l10n_it_vat_settlement_communication/) | 18.0.1.0.3 |  | Comunicazione liquidazione IVA ed esportazione file xmlconforme alle specifiche dell'Agenzia delle Entrate
[l10n_it_vat_settlement_date](l10n_it_vat_settlement_date/) | 18.0.1.0.1 |  | Settlement date for VAT Statement
[l10n_it_website_portal_fiscalcode](l10n_it_website_portal_fiscalcode/) | 18.0.1.0.0 |  | Add fiscal code to details of frontend user

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-japan


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-japan&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-japan/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-japan/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-japan/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-japan/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-japan/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-japan)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-japan-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-japan-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Odoo日本向けローカリゼーション (l10n-japan)

[Odooコミュニティ協会(OCA)](https://odoo-community.org/)による、日本向けのローカリゼーションモジュールのレポジトリです。
日本独自の帳票・住所表示・都道府県対応など、Odooを日本で使いやすくするための機能を提供します。

OCAの活動は、オープンで透明度の高い活動をもとにユーザへの提供価値を最大化することを目指すコミュニティの有志により推進されています。

## コミュニティ活動への参加呼びかけ

日本でOdooを使用するにあたっての共通課題は、コミュニティの力で解決しましょう！

本レポジトリでの活動には、申請などなしに**どなたでも**参加いただけます（GitHubのアカウントは必要です）。日本語および英語でのコミュニケーションを受け付けます。

* [イシュー](https://github.com/OCA/l10n-japan/issues)
* [プルリクエスト](https://github.com/OCA/l10n-japan/pulls)
* [ディスカッション](https://github.com/OCA/l10n-japan/discussions)

## コミュニティ活動への参加例

* 日本市場特有の課題に対処する機能を新規追加するプルリクエストを作成
* 既存機能を改善/修正するプルリクエストを作成
* プルリクエストをレビュー（コメント/承認/変更要求）
* 既存機能に不具合がある場合にイシューを作成
* 日本市場の共通課題について、ディスカッションに参加
* 使用した/している機能やコミュニティ活動について、ソーシャルメディア等オープンな場で発信

## やめていただきたいこと

* ライセンス違反（AGPLに基づくソース開示義務の不履行、利用者への不当な制限等）

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_move_delivery_invoice](account_move_delivery_invoice/) | 18.0.1.2.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Account Move Delivery Invoice
[account_payment_term_cutoff_day](account_payment_term_cutoff_day/) | 18.0.1.1.0 |  | Account Payment Term Cutoff Day
[account_tax_rounding_method](account_tax_rounding_method/) | 18.0.1.0.0 |  | Account Tax Rounding Method
[l10n_jp_address_layout](l10n_jp_address_layout/) | 18.0.1.0.0 |  | Japan Address Layout
[l10n_jp_country_state](l10n_jp_country_state/) | 18.0.1.1.0 |  | Japan Country States
[l10n_jp_partner_title_qweb](l10n_jp_partner_title_qweb/) | 18.0.1.0.0 |  | Japan Partner Title QWeb
[l10n_jp_partner_zip_address](l10n_jp_partner_zip_address/) | 18.0.1.0.1 |  | Japan Partner Zip Address
[l10n_jp_summary_invoice](l10n_jp_summary_invoice/) | 18.0.1.5.0 |  | Japan Summary Invoice
[l10n_jp_summary_invoice_carryover](l10n_jp_summary_invoice_carryover/) | 18.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Add carryover amount tracking to summary invoices
[report_alternative_layout](report_alternative_layout/) | 18.0.1.1.0 |  | Report Alternative Layout

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-mexico


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-mexico&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-mexico/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-mexico/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-mexico/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-mexico/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-mexico/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-mexico)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-mexico-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-mexico-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-mexico

l10n-mexico

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[currency_rate_update_banxico](currency_rate_update_banxico/) | 18.0.1.0.0 |  | Update exchange rates using Banxico
[l10n_mx_tax](l10n_mx_tax/) | 18.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Adds ISH, ISN, and IEPS 200% taxes to the Mexican localization

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-netherlands


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-netherlands&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-netherlands/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-netherlands/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-netherlands/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-netherlands/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-netherlands/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-netherlands)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-netherlands-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-netherlands-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-netherlands

l10n-netherlands

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_nl_bank](l10n_nl_bank/) | 18.0.1.0.0 |  | Import all Dutch banks with BIC code
[l10n_nl_bsn](l10n_nl_bsn/) | 18.0.1.0.0 | <a href='https://github.com/astirpe'><img src='https://github.com/astirpe.png' width='32' height='32' style='border-radius:50%;' alt='astirpe'/></a> | Burgerservicenummer (BSN) for Partners
[l10n_nl_kvk_partner](l10n_nl_kvk_partner/) | 18.0.1.0.0 |  | Use the Peppol Endpoint as the Dutch Chamber of Commerce number
[l10n_nl_partner_name](l10n_nl_partner_name/) | 18.0.1.0.0 |  | Adapt parter names to Dutch conventions (support infix)
[l10n_nl_postcode](l10n_nl_postcode/) | 18.0.1.0.0 | <a href='https://github.com/astirpe'><img src='https://github.com/astirpe.png' width='32' height='32' style='border-radius:50%;' alt='astirpe'/></a> | Dutch postcode validation for Partners
[l10n_nl_tax_statement](l10n_nl_tax_statement/) | 18.0.1.0.0 |  | Netherlands BTW Statement
[l10n_nl_tax_statement_date_range](l10n_nl_tax_statement_date_range/) | 18.0.1.0.0 |  | Netherlands BTW Statement - Date range
[l10n_nl_tax_statement_icp](l10n_nl_tax_statement_icp/) | 18.0.1.0.0 |  | Netherlands ICP Statement
[l10n_nl_xaf_auditfile_export](l10n_nl_xaf_auditfile_export/) | 18.0.1.1.0 |  | Export XAF auditfiles for Dutch tax authorities

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-portugal


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# l10n-portugal
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-portugal&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-portugal/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-portugal/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-portugal/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-portugal/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-portugal/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-portugal)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-portugal-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-portugal-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

l10n-portugal

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_pt_account_invoicexpress](l10n_pt_account_invoicexpress/) | 18.0.1.0.1 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Portuguese certified invoices using InvoiceXpress
[l10n_pt_certification](l10n_pt_certification/) | 18.0.1.0.0 |  | Portugal - Accounting (Certification)
[l10n_pt_future_account](l10n_pt_future_account/) | 18.0.1.0.0 |  | Future accounting features for Portugal
[l10n_pt_payment](l10n_pt_payment/) | 18.0.1.0.0 |  | Portugal-specific payment methods: Multibanco and MB WAY
[l10n_pt_stock_invoicexpress](l10n_pt_stock_invoicexpress/) | 18.0.1.0.1 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Portuguese legal transport and shipping documents (Guias de Transporte e Guias de Remessa) generated with InvoiceXpress
[l10n_pt_vat](l10n_pt_vat/) | 18.0.1.0.0 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Portuguese VAT requirements extensions
[payment_easypay_oca](payment_easypay_oca/) | 18.0.1.0.4 |  | Payment Provider for EasyPay with multiple payment methods

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-romania


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-romania&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-romania/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-romania/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-romania/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-romania/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-romania/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-romania)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-romania-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-romania-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-romania

l10n-romania

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[currency_rate_update_RO_BNR](currency_rate_update_RO_BNR/) | 18.0.1.1.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Currency Rate Update National Bank of Romania service
[l10n_ro_account](l10n_ro_account/) | 18.0.0.5.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Account
[l10n_ro_account_bank_statement_import_mt940_alpha](l10n_ro_account_bank_statement_import_mt940_alpha/) | 18.0.0.1.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | MT940 Alpha Format Bank Statements Import
[l10n_ro_account_bank_statement_import_mt940_base](l10n_ro_account_bank_statement_import_mt940_base/) | 18.0.0.2.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - MT940 Bank Statements Import
[l10n_ro_account_bank_statement_import_mt940_bcr](l10n_ro_account_bank_statement_import_mt940_bcr/) | 18.0.0.2.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | MT940 BCR Format Bank Statements Import
[l10n_ro_account_bank_statement_import_mt940_brd](l10n_ro_account_bank_statement_import_mt940_brd/) | 18.0.0.2.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Import bank statements from BRD
[l10n_ro_account_bank_statement_import_mt940_ing](l10n_ro_account_bank_statement_import_mt940_ing/) | 18.0.0.1.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | MT940 ING Format Bank Statements Import
[l10n_ro_account_bank_statement_report](l10n_ro_account_bank_statement_report/) | 18.0.0.1.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Bank Statement Report
[l10n_ro_account_edit_currency_rate](l10n_ro_account_edit_currency_rate/) | 18.0.0.2.0 | <a href='https://github.com/mcojocaru'><img src='https://github.com/mcojocaru.png' width='32' height='32' style='border-radius:50%;' alt='mcojocaru'/></a> | Romania - Invoice Edit Currency Rate
[l10n_ro_account_period_close](l10n_ro_account_period_close/) | 18.0.0.4.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Account Period Closing
[l10n_ro_account_report_invoice](l10n_ro_account_report_invoice/) | 18.0.0.2.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Invoice Report
[l10n_ro_city](l10n_ro_city/) | 18.0.1.10.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - City
[l10n_ro_config](l10n_ro_config/) | 18.0.0.5.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Localization Install and Config Applications
[l10n_ro_dvi](l10n_ro_dvi/) | 18.0.1.3.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - DVI
[l10n_ro_fiscal_validation](l10n_ro_fiscal_validation/) | 18.0.1.1.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Fiscal Validation
[l10n_ro_message_spv](l10n_ro_message_spv/) | 18.0.1.21.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Mesaje SPV
[l10n_ro_nondeductible_vat](l10n_ro_nondeductible_vat/) | 18.0.0.6.0 | <a href='https://github.com/adrian-dks'><img src='https://github.com/adrian-dks.png' width='32' height='32' style='border-radius:50%;' alt='adrian-dks'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Nondeductible VAT
[l10n_ro_partner_create_by_vat](l10n_ro_partner_create_by_vat/) | 18.0.0.5.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Partner Create by VAT
[l10n_ro_partner_unique](l10n_ro_partner_unique/) | 18.0.0.2.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Creates a rule for vat and nrc unique for partners.
[l10n_ro_payment_receipt_report](l10n_ro_payment_receipt_report/) | 18.0.0.1.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Payment Receipt Report
[l10n_ro_payment_to_statement](l10n_ro_payment_to_statement/) | 18.0.0.1.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Add payment to cash statement
[l10n_ro_pos](l10n_ro_pos/) | 18.0.1.4.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Point of Sale
[l10n_ro_stock](l10n_ro_stock/) | 18.0.0.12.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock
[l10n_ro_stock_account](l10n_ro_stock_account/) | 18.0.1.25.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Accounting
[l10n_ro_stock_account_date](l10n_ro_stock_account_date/) | 18.0.1.5.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Accounting Date
[l10n_ro_stock_account_date_wizard](l10n_ro_stock_account_date_wizard/) | 18.0.1.3.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Accounting Date Wizard
[l10n_ro_stock_account_landed_cost](l10n_ro_stock_account_landed_cost/) | 18.0.1.2.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Accounting Landed Cost
[l10n_ro_stock_account_notice](l10n_ro_stock_account_notice/) | 18.0.1.7.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/mcojocaru'><img src='https://github.com/mcojocaru.png' width='32' height='32' style='border-radius:50%;' alt='mcojocaru'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Stock Accounting Notice
[l10n_ro_stock_account_reception_in_progress](l10n_ro_stock_account_reception_in_progress/) | 18.0.0.2.0 | <a href='https://github.com/nct74'><img src='https://github.com/nct74.png' width='32' height='32' style='border-radius:50%;' alt='nct74'/></a> <a href='https://github.com/vasi26ro'><img src='https://github.com/vasi26ro.png' width='32' height='32' style='border-radius:50%;' alt='vasi26ro'/></a> | Romania - Stock Accounting Reception In progress
[l10n_ro_stock_account_tracking](l10n_ro_stock_account_tracking/) | 18.0.1.5.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Accounting
[l10n_ro_stock_picking_comment_template](l10n_ro_stock_picking_comment_template/) | 18.0.0.2.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | This model is going to add a a header and a footer at picking report depeding on the operation type.
[l10n_ro_stock_picking_valued_report](l10n_ro_stock_picking_valued_report/) | 18.0.0.5.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Picking Valued Report
[l10n_ro_stock_price_difference](l10n_ro_stock_price_difference/) | 18.0.0.2.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/mcojocaru'><img src='https://github.com/mcojocaru.png' width='32' height='32' style='border-radius:50%;' alt='mcojocaru'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Stock Accounting Price Difference
[l10n_ro_stock_report](l10n_ro_stock_report/) | 18.0.1.8.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Report (Fișă Magazie)
[l10n_ro_vat_on_payment](l10n_ro_vat_on_payment/) | 18.0.0.5.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - VAT on Payment

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-spain


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# l10n-spain
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-spain&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-spain/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-spain/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-spain/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-spain/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-spain/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-spain)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-spain-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-spain-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

l10n-spain

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_promissory_note_caixabank](account_promissory_note_caixabank/) | 18.0.1.0.0 |  | Impresión de pagaré CaixaBank A4
[delivery_dhl_parcel](delivery_dhl_parcel/) | 18.0.1.0.0 | <a href='https://github.com/hildickethan'><img src='https://github.com/hildickethan.png' width='32' height='32' style='border-radius:50%;' alt='hildickethan'/></a> | Delivery Carrier implementation for DHL Parcel using their API
[delivery_gls_asm](delivery_gls_asm/) | 18.0.1.1.3 | <a href='https://github.com/hildickethan'><img src='https://github.com/hildickethan.png' width='32' height='32' style='border-radius:50%;' alt='hildickethan'/></a> | Delivery Carrier implementation for GLS with ASMRed API
[delivery_seur_atlas](delivery_seur_atlas/) | 18.0.1.0.0 |  | Integrate SEUR Atlas API
[l10n_ca_es_cnae](l10n_ca_es_cnae/) | 18.0.1.0.1 |  | Genera la traducción al catalán de todos los códigos Nace
[l10n_es_account_asset](l10n_es_account_asset/) | 18.0.2.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Gestión de activos fijos para España
[l10n_es_account_banking_sepa_fsdd](l10n_es_account_banking_sepa_fsdd/) | 18.0.1.0.0 |  | Account Banking Sepa - FSDD (Anticipos de crédito)
[l10n_es_account_statement_import_n43](l10n_es_account_statement_import_n43/) | 18.0.1.2.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Importación de extractos bancarios españoles (Norma 43)
[l10n_es_aeat](l10n_es_aeat/) | 18.0.2.1.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Modulo base para declaraciones de la AEAT
[l10n_es_aeat_mod111](l10n_es_aeat_mod111/) | 18.0.1.0.4 |  | AEAT modelo 111
[l10n_es_aeat_mod115](l10n_es_aeat_mod115/) | 18.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | AEAT modelo 115
[l10n_es_aeat_mod123](l10n_es_aeat_mod123/) | 18.0.1.0.3 |  | AEAT modelo 123
[l10n_es_aeat_mod130](l10n_es_aeat_mod130/) | 18.0.1.0.1 |  | AEAT modelo 130
[l10n_es_aeat_mod190](l10n_es_aeat_mod190/) | 18.0.1.4.0 |  | AEAT modelo 190
[l10n_es_aeat_mod216](l10n_es_aeat_mod216/) | 18.0.1.1.2 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | AEAT modelo 216
[l10n_es_aeat_mod296](l10n_es_aeat_mod296/) | 18.0.1.0.1 |  | AEAT modelo 296
[l10n_es_aeat_mod303](l10n_es_aeat_mod303/) | 18.0.1.1.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | AEAT modelo 303
[l10n_es_aeat_mod303_oss](l10n_es_aeat_mod303_oss/) | 18.0.1.0.0 |  | AEAT modelo 303 - OSS
[l10n_es_aeat_mod303_vat_prorate](l10n_es_aeat_mod303_vat_prorate/) | 18.0.1.1.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Prorrata de IVA [303]
[l10n_es_aeat_mod347](l10n_es_aeat_mod347/) | 18.0.1.2.4 |  | AEAT modelo 347
[l10n_es_aeat_mod349](l10n_es_aeat_mod349/) | 18.0.1.0.3 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | AEAT modelo 349
[l10n_es_aeat_mod369](l10n_es_aeat_mod369/) | 18.0.1.0.1 |  | AEAT modelo 369
[l10n_es_aeat_mod390](l10n_es_aeat_mod390/) | 18.0.1.1.5 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | AEAT modelo 390
[l10n_es_aeat_mod390_oss](l10n_es_aeat_mod390_oss/) | 18.0.1.0.0 |  | AEAT modelo 390 - OSS
[l10n_es_aeat_mod390_vat_prorate](l10n_es_aeat_mod390_vat_prorate/) | 18.0.1.1.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | AEAT modelo 390 Prorate
[l10n_es_aeat_partner_check](l10n_es_aeat_partner_check/) | 18.0.1.0.0 |  | AEAT - Comprobación de Calidad de datos identificativos
[l10n_es_aeat_sii_invoice_summary](l10n_es_aeat_sii_invoice_summary/) | 18.0.2.0.0 |  | Envio de factura simplificada resumen TPV a SII
[l10n_es_aeat_sii_match](l10n_es_aeat_sii_match/) | 18.0.2.0.0 | <a href='https://github.com/Abranes'><img src='https://github.com/Abranes.png' width='32' height='32' style='border-radius:50%;' alt='Abranes'/></a> <a href='https://github.com/Reyes4711-S73'><img src='https://github.com/Reyes4711-S73.png' width='32' height='32' style='border-radius:50%;' alt='Reyes4711-S73'/></a> <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Sistema de comprobación y contraste de facturas enviadas al SII
[l10n_es_aeat_sii_oca](l10n_es_aeat_sii_oca/) | 18.0.2.1.5 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Suministro Inmediato de Información en el IVA
[l10n_es_aeat_sii_oss](l10n_es_aeat_sii_oss/) | 18.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Suministro Inmediato de Información en el IVA: OSS
[l10n_es_atc](l10n_es_atc/) | 18.0.1.1.2 |  | Modulo 'glue' de la AEAT para el menú de la ATC
[l10n_es_atc_mod415](l10n_es_atc_mod415/) | 18.0.1.0.0 | <a href='https://github.com/Christian-RB'><img src='https://github.com/Christian-RB.png' width='32' height='32' style='border-radius:50%;' alt='Christian-RB'/></a> | ATC Modelo 415
[l10n_es_atc_mod420](l10n_es_atc_mod420/) | 18.0.1.1.0 | <a href='https://github.com/christian-ramos-tecnativa'><img src='https://github.com/christian-ramos-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='christian-ramos-tecnativa'/></a> <a href='https://github.com/carlos-lopez-tecnativa'><img src='https://github.com/carlos-lopez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carlos-lopez-tecnativa'/></a> | ATC Modelo 420
[l10n_es_atc_sii_oca](l10n_es_atc_sii_oca/) | 18.0.1.0.0 |  | Suministro Inmediato de Información en el IGIC
[l10n_es_cnae](l10n_es_cnae/) | 18.0.1.0.0 |  | Extiende los códigos NACE europeos con los CNAE españoles
[l10n_es_digital_canon](l10n_es_digital_canon/) | 18.0.1.0.0 |  | Aplicación automática del canon digital en facturas, ventas y compras
[l10n_es_facturae](l10n_es_facturae/) | 18.0.1.2.3 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Creación de Facturae
[l10n_es_facturae_face](l10n_es_facturae_face/) | 18.0.1.0.2 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Envío de Facturae a FACe
[l10n_es_facturae_sale_stock](l10n_es_facturae_sale_stock/) | 18.0.1.0.0 |  | Entregas en Factura-e
[l10n_es_hr_collective_agreement](l10n_es_hr_collective_agreement/) | 18.0.1.0.0 |  | Datos iniciales de configuración para convenios colectivos en España
[l10n_es_intrastat_report](l10n_es_intrastat_report/) | 18.0.1.2.2 |  | Spanish Intrastat Product Declaration
[l10n_es_location_nuts](l10n_es_location_nuts/) | 18.0.1.0.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | NUTS specific options for Spain
[l10n_es_mis_report](l10n_es_mis_report/) | 18.0.1.0.2 |  | Plantillas MIS Builder para informes contables españoles
[l10n_es_partner](l10n_es_partner/) | 18.0.1.0.4 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Adaptación de los clientes, proveedores y bancos para España
[l10n_es_partner_mercantil](l10n_es_partner_mercantil/) | 18.0.1.0.0 |  | Añade los datos del registro mercantil a la empresa
[l10n_es_payment_order_confirming_aef](l10n_es_payment_order_confirming_aef/) | 18.0.1.0.2 |  | Exportación de fichero bancario Confirming estándar AEF
[l10n_es_payment_order_confirming_sabadell](l10n_es_payment_order_confirming_sabadell/) | 18.0.1.0.2 |  | Exportación de fichero bancario Confirming para Banco Sabadell
[l10n_es_pos_oca](l10n_es_pos_oca/) | 18.0.1.1.0 |  | Punto de venta adaptado a la legislación española
[l10n_es_pos_sii](l10n_es_pos_sii/) | 18.0.2.0.0 |  | Envío de pedidos del TPV al SII
[l10n_es_pos_sii_match](l10n_es_pos_sii_match/) | 18.0.2.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Extensión del contraste SII para el TPV
[l10n_es_toponyms](l10n_es_toponyms/) | 18.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Topónimos españoles
[l10n_es_vat_book](l10n_es_vat_book/) | 18.0.2.1.3 |  | Libros registro del IVA y del IRPF
[l10n_es_vat_book_invoice_summary](l10n_es_vat_book_invoice_summary/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Facturas resumen en libro de IVA
[l10n_es_vat_book_oss](l10n_es_vat_book_oss/) | 18.0.1.0.2 |  | Libro de IVA OSS
[l10n_es_vat_book_pos](l10n_es_vat_book_pos/) | 18.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Libro de IVA Adaptado al Punto de Venta
[l10n_es_vat_prorate](l10n_es_vat_prorate/) | 18.0.2.0.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Prorrata de IVA para la localización española
[l10n_es_verifactu_oca](l10n_es_verifactu_oca/) | 18.0.1.2.5 |  | Comunicación VERI*FACTU
[payment_redsys](payment_redsys/) | 18.0.1.0.1 |  | Payment Acquirer: Redsys Implementation

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-switzerland


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-switzerland&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-switzerland/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-switzerland/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-switzerland/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-switzerland/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-switzerland/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-switzerland)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-switzerland-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-switzerland-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-switzerland

l10n-switzerland

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[ebill_postfinance](ebill_postfinance/) | 18.0.1.2.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Postfinance eBill integration
[ebill_postfinance_customer_free_ref](ebill_postfinance_customer_free_ref/) | 18.0.1.0.0 |  | Glue module: ebill_postfinance and sale_order_customer_free_ref
[ebill_postfinance_server_env](ebill_postfinance_server_env/) | 18.0.1.0.0 |  | Server environment for eBill Postfinance
[ebill_postfinance_stock](ebill_postfinance_stock/) | 18.0.1.0.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Add stock integration to Postfinance eBill
[l10n_ch_account_tags](l10n_ch_account_tags/) | 18.0.1.0.0 |  | Switzerland Account Tags
[l10n_ch_adr_report](l10n_ch_adr_report/) | 18.0.1.0.0 |  | Print Delivery report to ADR swiss configuration
[l10n_ch_mis_reports](l10n_ch_mis_reports/) | 18.0.1.0.0 | <a href='https://github.com/jguenat'><img src='https://github.com/jguenat.png' width='32' height='32' style='border-radius:50%;' alt='jguenat'/></a> | Specific MIS reports for switzerland localization

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-thailand


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# l10n-thailand
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-thailand&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-thailand/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-thailand/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-thailand/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-thailand/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-thailand/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-thailand)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-thailand-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-thailand-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

l10n-thailand

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[currency_rate_update_TH_BOT](currency_rate_update_TH_BOT/) | 18.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Currency Rate Update - BOT
[l10n_th_account_asset_management](l10n_th_account_asset_management/) | 18.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Thai Localization - Assets Management
[l10n_th_account_tax](l10n_th_account_tax/) | 18.0.1.5.5 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Thai Localization - VAT and Withholding Tax
[l10n_th_account_tax_expense](l10n_th_account_tax_expense/) | 18.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Thai Localization - Expense Tax
[l10n_th_account_tax_multi](l10n_th_account_tax_multi/) | 18.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Thai Localization - Tax with Payment Multi Deduction
[l10n_th_account_tax_report](l10n_th_account_tax_report/) | 18.0.1.0.1 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Thai Localization - VAT and Withholding Tax Reports
[l10n_th_account_wht_cert_form](l10n_th_account_wht_cert_form/) | 18.0.1.0.1 | <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Thai Localization - Withholding Tax Certificate Form
[l10n_th_amount_to_text](l10n_th_amount_to_text/) | 18.0.2.0.0 | <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Convert Amount Text to Thai
[l10n_th_base_sequence](l10n_th_base_sequence/) | 18.0.1.0.0 | <a href='https://github.com/sansirit'><img src='https://github.com/sansirit.png' width='32' height='32' style='border-radius:50%;' alt='sansirit'/></a> <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Thai Localization - Base Sequence
[l10n_th_base_utils](l10n_th_base_utils/) | 18.0.3.0.0 | <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Collection of all Thai fonts, Convert month/year/number to thai
[l10n_th_mis_report](l10n_th_mis_report/) | 18.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Thai Localization - MIS Report
[l10n_th_partner](l10n_th_partner/) | 18.0.2.0.1 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Thai Localization - Partner
[l10n_th_tier_department](l10n_th_tier_department/) | 18.0.1.0.1 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Thai Localization - Tier Department Level
[l10n_th_tier_department_demo](l10n_th_tier_department_demo/) | 18.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Thai Localization - Tier Department Level Demo

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-usa


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-usa&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/l10n-usa/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-usa/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/l10n-usa/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/l10n-usa/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/l10n-usa/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-usa)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-usa-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-usa-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-usa

l10n-usa

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_banking_ach_base](account_banking_ach_base/) | 18.0.1.0.0 |  | Add fields required for North American Banking & Financials
[account_banking_ach_credit_transfer](account_banking_ach_credit_transfer/) | 18.0.1.0.0 |  | Create ACH files for Credit Transfers
[l10n_us_account_routing](l10n_us_account_routing/) | 18.0.1.0.0 |  | Add the routing numbers to the banks
[l10n_us_base_county](l10n_us_base_county/) | 18.0.0.0.0 |  | Add United States counties.
[l10n_us_crm_county](l10n_us_crm_county/) | 18.0.0.0.0 |  | Add United States counties to leads.
[l10n_us_mis_financial_report](l10n_us_mis_financial_report/) | 18.0.1.0.0 | <a href='https://github.com/Christian-RB'><img src='https://github.com/Christian-RB.png' width='32' height='32' style='border-radius:50%;' alt='Christian-RB'/></a> | Profit & Loss (US) / Balance sheet (US) MIS templates
[l10n_us_partner_legal_number](l10n_us_partner_legal_number/) | 18.0.1.0.0 |  | Add Legal Number for North American Banking & Financials

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/mail


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# mail
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/mail&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/mail/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/mail/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/mail/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/mail/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/mail/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/mail)
[![Translation Status](https://translation.odoo-community.org/widgets/mail-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/mail-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

mail

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_search_mail_content](base_search_mail_content/) | 18.0.1.0.2 |  | Base Search Mail Content
[base_user_signature](base_user_signature/) | 18.0.1.0.0 | <a href='https://github.com/imlopes'><img src='https://github.com/imlopes.png' width='32' height='32' style='border-radius:50%;' alt='imlopes'/></a> | Base User Signature
[mail_activity_board](mail_activity_board/) | 18.0.1.1.1 |  | Add Activity Boards
[mail_activity_dashboard](mail_activity_dashboard/) | 18.0.1.0.0 |  | Add Activity Dashboards
[mail_activity_done](mail_activity_done/) | 18.0.1.0.0 |  | Mail Activity Done
[mail_activity_plan_domain](mail_activity_plan_domain/) | 18.0.1.0.0 |  | Apply domain filters to activity plans and their templates
[mail_activity_reminder](mail_activity_reminder/) | 18.0.1.0.0 |  | Reminder notifications about planned activities
[mail_activity_team](mail_activity_team/) | 18.0.1.3.0 |  | Add Teams to Activities
[mail_attach_existing_attachment](mail_attach_existing_attachment/) | 18.0.1.0.1 |  | Adding attachment on the object by sending this one
[mail_attach_existing_attachment_account](mail_attach_existing_attachment_account/) | 18.0.1.0.0 |  | Module to use attach existing attachment for account module
[mail_autogenerated_header](mail_autogenerated_header/) | 18.0.1.1.0 |  | Add headers to Odoo's mails indicating they are autogenerated
[mail_autosubscribe](mail_autosubscribe/) | 18.0.1.1.0 |  | Automatically subscribe partners to its company's business documents
[mail_composer_cc_bcc](mail_composer_cc_bcc/) | 18.0.1.0.2 | <a href='https://github.com/trisdoan'><img src='https://github.com/trisdoan.png' width='32' height='32' style='border-radius:50%;' alt='trisdoan'/></a> | This module enables sending mail to CC and BCC partners in mail composer form.
[mail_debrand](mail_debrand/) | 18.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/joao-p-marques'><img src='https://github.com/joao-p-marques.png' width='32' height='32' style='border-radius:50%;' alt='joao-p-marques'/></a> | Remove Odoo branding in sent emails Removes anchor <a href odoo.com togheder with it's parent ( for powerd by) form all the templates removes any 'odoo' that are in tempalte texts > 20characters
[mail_drop_target](mail_drop_target/) | 18.0.1.0.2 |  | Attach emails to Odoo by dragging them from your desktop
[mail_extra_header](mail_extra_header/) | 18.0.1.0.0 |  | Adds extra headers per mail server to sent mails.
[mail_force_email_notification](mail_force_email_notification/) | 18.0.1.0.0 |  | Context key to define notifications to be sent by emaildefined by force_notification_by_email context key
[mail_forward](mail_forward/) | 18.0.1.0.1 | <a href='https://github.com/carlos-lopez-tecnativa'><img src='https://github.com/carlos-lopez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carlos-lopez-tecnativa'/></a> | Forward messages from the chatter of any document to other users.
[mail_inline_css](mail_inline_css/) | 18.0.1.0.0 |  | Convert style tags in inline style in your mails
[mail_layout_force](mail_layout_force/) | 18.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Force a mail layout on selected email templates
[mail_layout_preview](mail_layout_preview/) | 18.0.1.0.0 |  | Preview email templates in the browser
[mail_message_search](mail_message_search/) | 18.0.1.0.2 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Mail Message Search
[mail_no_user_assign_notification](mail_no_user_assign_notification/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Mail No user Assign Notification
[mail_notification_clean_status_error](mail_notification_clean_status_error/) | 18.0.1.0.0 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Extend Odoo scheduled action to also delete notifications in error.
[mail_notification_custom_subject](mail_notification_custom_subject/) | 18.0.1.0.0 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Apply a custom subject to mail notifications
[mail_optional_autofollow](mail_optional_autofollow/) | 18.0.1.0.0 |  | Choose if you want to automatically add new recipients as followers on mail.compose.message
[mail_optional_follower_notification](mail_optional_follower_notification/) | 18.0.1.0.0 |  | Choose to notify followers on mail.compose.message
[mail_outbound_static](mail_outbound_static/) | 18.0.1.0.1 |  | Allows you to configure the from header for a mail server.
[mail_partner_forwarding](mail_partner_forwarding/) | 18.0.1.0.0 |  | Forwarding notifications for partners
[mail_partner_opt_out](mail_partner_opt_out/) | 18.0.1.0.0 |  | Add the partner's email to the blackmailed list
[mail_post_defer](mail_post_defer/) | 18.0.1.0.2 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Faster and cancellable outgoing messages
[mail_quoted_reply](mail_quoted_reply/) | 18.0.1.0.0 |  | Make a reply using a message
[mail_restrict_follower_selection](mail_restrict_follower_selection/) | 18.0.1.1.0 |  | Define a domain from which followers can be selected
[mail_restrict_send_button](mail_restrict_send_button/) | 18.0.1.0.0 |  | Security for Send Message Button on Chatter Area
[mail_send_confirmation](mail_send_confirmation/) | 18.0.1.0.0 |  | Mail Send Confirmation
[mail_show_follower](mail_show_follower/) | 18.0.1.0.2 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Show CC document followers in mails.
[mail_suggested_recipient_unchecked](mail_suggested_recipient_unchecked/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Mail suggested recipient unchecked
[mail_template_domain](mail_template_domain/) | 18.0.1.0.0 |  | Filter mail templates by domain on the active record
[mail_template_substitute](mail_template_substitute/) | 18.0.1.0.0 |  | This module allows to create substitution rules for mail templates.
[mail_tracking](mail_tracking/) | 18.0.1.0.9 |  | Email tracking system for all mails sent
[mail_tracking_mailgun](mail_tracking_mailgun/) | 18.0.1.0.0 |  | Mail tracking and Mailgun webhooks integration
[mail_tracking_mass_mailing](mail_tracking_mass_mailing/) | 18.0.1.0.0 |  | Improve mass mailing email tracking

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/maintenance


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/maintenance&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/maintenance/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/maintenance/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/maintenance/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/maintenance/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/maintenance/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/maintenance)
[![Translation Status](https://translation.odoo-community.org/widgets/maintenance-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/maintenance-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# maintenance

maintenance

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_maintenance](base_maintenance/) | 18.0.1.0.0 |  | Base Maintenance
[base_maintenance_group](base_maintenance_group/) | 18.0.1.0.0 |  | Provides base access groups for the Maintenance App
[hr_maintenance_security](hr_maintenance_security/) | 18.0.1.0.0 |  | HR Maintenance Security
[maintenance_account](maintenance_account/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Account
[maintenance_equipment_category_hierarchy](maintenance_equipment_category_hierarchy/) | 18.0.1.0.0 |  | Equipment Categories Hierarchy
[maintenance_equipment_contract](maintenance_equipment_contract/) | 18.0.1.0.0 |  | Manage equipment contracts
[maintenance_equipment_hierarchy](maintenance_equipment_hierarchy/) | 18.0.1.0.0 | <a href='https://github.com/dalonsod'><img src='https://github.com/dalonsod.png' width='32' height='32' style='border-radius:50%;' alt='dalonsod'/></a> | Manage equipment hierarchy
[maintenance_equipment_ref](maintenance_equipment_ref/) | 18.0.1.0.0 |  | Adds reference field to maintenance equipment
[maintenance_equipment_sequence](maintenance_equipment_sequence/) | 18.0.1.0.0 |  | Adds sequence to maintenance equipment defined in the equipment's category
[maintenance_equipment_status](maintenance_equipment_status/) | 18.0.1.0.0 |  | Maintenance Equipment Status
[maintenance_equipment_tags](maintenance_equipment_tags/) | 18.0.1.0.0 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Adds category tags to equipment
[maintenance_equipment_usage](maintenance_equipment_usage/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Equipment Usage
[maintenance_helpdesk_mgmt](maintenance_helpdesk_mgmt/) | 18.0.1.1.0 |  | Allows you to link Helpdesk Tickets with maintenance requests
[maintenance_partner](maintenance_partner/) | 18.0.1.0.1 |  | Add Partner information in Maintenance Requests and equipments
[maintenance_plan](maintenance_plan/) | 18.0.1.0.1 |  | Extends preventive maintenance planning
[maintenance_plan_activity](maintenance_plan_activity/) | 18.0.1.0.0 |  | This module allows defining in the maintenance plan activities that will be created once the maintenance requests are created as a consequence of the plan itself.
[maintenance_plan_only](maintenance_plan_only/) | 18.0.1.0.0 |  | Technical module to hide built-in recurrent settings
[maintenance_product](maintenance_product/) | 18.0.1.0.2 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Product
[maintenance_project](maintenance_project/) | 18.0.1.2.0 |  | Adds projects to maintenance equipments and requests
[maintenance_purchase](maintenance_purchase/) | 18.0.1.0.0 |  | Create Equipments with purchases
[maintenance_request_employee](maintenance_request_employee/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Request Employee
[maintenance_request_purchase](maintenance_request_purchase/) | 18.0.1.0.0 |  | Allows you to link PO with maintenance requests
[maintenance_request_repair](maintenance_request_repair/) | 18.0.1.0.0 |  | This is a bridge module between Maintenance and Repair
[maintenance_request_sequence](maintenance_request_sequence/) | 18.0.1.0.0 |  | Adds sequence to maintenance requests
[maintenance_request_tags](maintenance_request_tags/) | 18.0.1.0.0 |  | Adds tags to Maintenance Requests
[maintenance_security](maintenance_security/) | 18.0.2.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Security
[maintenance_stock](maintenance_stock/) | 18.0.1.0.1 |  | Links maintenance requests to stock
[maintenance_timesheet](maintenance_timesheet/) | 18.0.1.1.0 |  | Adds timesheets to maintenance requests
[maintenance_timesheet_time_control](maintenance_timesheet_time_control/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Timesheets Timesheet Time Control

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/management-system


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/management-system&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/management-system/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/management-system/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/management-system/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/management-system/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/management-system/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/management-system)
[![Translation Status](https://translation.odoo-community.org/widgets/management-system-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/management-system-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# management-system

management-system

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[document_page_environment_manual](document_page_environment_manual/) | 18.0.1.0.1 |  | Document Management - Wiki - Environment Manual
[document_page_environmental_aspect](document_page_environmental_aspect/) | 18.0.1.0.1 |  | Environmental Aspects
[document_page_health_safety_manual](document_page_health_safety_manual/) | 18.0.1.0.1 |  | Health and Safety Manual
[document_page_procedure](document_page_procedure/) | 18.0.1.0.1 |  | Document Management - Wiki - Procedures
[document_page_quality_manual](document_page_quality_manual/) | 18.0.1.0.1 |  | Quality Manual
[document_page_work_instruction](document_page_work_instruction/) | 18.0.1.0.1 |  | Document Management - Wiki - Work Instructions
[mgmtsystem](mgmtsystem/) | 18.0.1.2.0 |  | Support for management systems, such as ISO compliance.
[mgmtsystem_action](mgmtsystem_action/) | 18.0.1.0.2 |  | Management System - Action
[mgmtsystem_action_efficacy](mgmtsystem_action_efficacy/) | 18.0.1.0.0 |  | Add information on the application of the Action.
[mgmtsystem_action_template](mgmtsystem_action_template/) | 18.0.1.0.0 |  | Add Template management for Actions.
[mgmtsystem_audit](mgmtsystem_audit/) | 18.0.1.1.0 |  | Management System - Audit
[mgmtsystem_claim](mgmtsystem_claim/) | 18.0.1.0.0 |  | Management System - Claim
[mgmtsystem_hazard](mgmtsystem_hazard/) | 18.0.1.1.0 |  | Hazard
[mgmtsystem_hazard_risk](mgmtsystem_hazard_risk/) | 18.0.1.2.0 |  | Hazard Risk
[mgmtsystem_info_security_manual](mgmtsystem_info_security_manual/) | 18.0.1.0.0 |  | Information Security Management System Manual
[mgmtsystem_manual](mgmtsystem_manual/) | 18.0.1.0.1 |  | Management System - Manual
[mgmtsystem_nonconformity](mgmtsystem_nonconformity/) | 18.0.1.3.0 |  | Management System - Nonconformity
[mgmtsystem_nonconformity_hazard](mgmtsystem_nonconformity_hazard/) | 18.0.1.0.0 |  | Management System - Nonconformity Hazard
[mgmtsystem_nonconformity_hr](mgmtsystem_nonconformity_hr/) | 18.0.1.0.0 |  | Bridge module between hr and mgmsystem and
[mgmtsystem_nonconformity_maintenance_equipment](mgmtsystem_nonconformity_maintenance_equipment/) | 18.0.1.0.0 |  | Management System - Nonconformity Maintenance Equipment
[mgmtsystem_nonconformity_mrp](mgmtsystem_nonconformity_mrp/) | 18.0.1.0.0 |  | Bridge module between mrp and mgmsystem
[mgmtsystem_nonconformity_product](mgmtsystem_nonconformity_product/) | 18.0.1.0.0 |  | Bridge module between Product and Management System.
[mgmtsystem_nonconformity_repair](mgmtsystem_nonconformity_repair/) | 18.0.1.0.0 |  | Bridge module between Repair and Non Conformities
[mgmtsystem_nonconformity_type](mgmtsystem_nonconformity_type/) | 18.0.1.1.0 |  | Add Nonconformity classification for the root context.
[mgmtsystem_objective](mgmtsystem_objective/) | 18.0.1.0.1 |  | Define objectives on your management system
[mgmtsystem_partner](mgmtsystem_partner/) | 18.0.1.0.0 |  | Add Management System reference on Partner's Contacts.
[mgmtsystem_quality](mgmtsystem_quality/) | 18.0.1.0.1 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Manage your quality management system
[mgmtsystem_review](mgmtsystem_review/) | 18.0.2.0.1 |  | Management System - Review
[mgmtsystem_review_objective](mgmtsystem_review_objective/) | 18.0.1.0.1 |  | Integrate reviews and objectives
[mgmtsystem_review_survey](mgmtsystem_review_survey/) | 18.0.2.0.0 |  | Management System - Review Survey
[mgmtsystem_survey](mgmtsystem_survey/) | 18.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Management System - Survey

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/manufacture


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/manufacture&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/manufacture/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/manufacture/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/manufacture/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/manufacture/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/manufacture/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/manufacture)
[![Translation Status](https://translation.odoo-community.org/widgets/manufacture-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/manufacture-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# manufacture

manufacture

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_move_line_mrp_info](account_move_line_mrp_info/) | 18.0.1.0.0 |  | Account Move Line Mrp Info
[mrp_attachment_mgmt](mrp_attachment_mgmt/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Mrp Attachment Mgmt
[mrp_bom_assign_auto](mrp_bom_assign_auto/) | 18.0.1.0.0 |  | Auto select th first BoM that has all components available
[mrp_bom_attribute_match](mrp_bom_attribute_match/) | 18.0.1.1.0 |  | Dynamic BOM component based on product attribute
[mrp_bom_component_menu](mrp_bom_component_menu/) | 18.0.1.0.0 |  | MRP BOM Component Menu
[mrp_bom_hierarchy](mrp_bom_hierarchy/) | 18.0.1.0.1 |  | Make it easy to navigate through BoM hierarchy.
[mrp_bom_image](mrp_bom_image/) | 18.0.1.0.0 |  | Add product Images to BoM
[mrp_bom_line_formula_quantity](mrp_bom_line_formula_quantity/) | 18.0.1.0.0 | <a href='https://github.com/SirAionTech'><img src='https://github.com/SirAionTech.png' width='32' height='32' style='border-radius:50%;' alt='SirAionTech'/></a> | Compute the quantity of a Production Line using a formula in the BoM Line.
[mrp_bom_line_uom_rounding](mrp_bom_line_uom_rounding/) | 18.0.1.0.0 |  | Enforce Unit of Measure rounding on BoM component quantities
[mrp_bom_location](mrp_bom_location/) | 18.0.1.1.2 |  | Adds location field to Bill of Materials and its components.
[mrp_bom_note](mrp_bom_note/) | 18.0.1.0.0 |  | Notes in Bill of Materials
[mrp_bom_select_product_variant](mrp_bom_select_product_variant/) | 18.0.1.0.0 |  | Favors Product variant selection for BOM creation.
[mrp_bom_tracking](mrp_bom_tracking/) | 18.0.1.1.0 |  | Logs any change to a BoM in the chatter
[mrp_bom_version](mrp_bom_version/) | 18.0.1.0.0 |  | BoM versioning
[mrp_bom_warn_message_oca](mrp_bom_warn_message_oca/) | 18.0.1.0.0 |  | Add a configurable warning when a bill of materials is selected on a MRP manufacturing order.
[mrp_bom_widget_section_and_note_one2many](mrp_bom_widget_section_and_note_one2many/) | 18.0.1.0.1 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Add section and note in Bills of Materials
[mrp_byproduct_auto_create_lot](mrp_byproduct_auto_create_lot/) | 18.0.1.0.1 |  | Auto create lots for byproducts on manufacturing orders
[mrp_lot_number_propagation](mrp_lot_number_propagation/) | 18.0.1.1.2 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Propagate a serial number from a component to a finished product
[mrp_lot_production_date](mrp_lot_production_date/) | 18.0.1.0.0 |  | MRP Lot Production Date
[mrp_mass_production_order](mrp_mass_production_order/) | 18.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Create multiple manufacturing orders in one step
[mrp_multi_level](mrp_multi_level/) | 18.0.1.4.2 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Adds an MRP Scheduler
[mrp_multi_level_consume_safety_stock](mrp_multi_level_consume_safety_stock/) | 18.0.1.0.1 | <a href='https://github.com/gurneyalex'><img src='https://github.com/gurneyalex.png' width='32' height='32' style='border-radius:50%;' alt='gurneyalex'/></a> | MRP scheduler: use safety stock during stress periods
[mrp_multi_level_estimate](mrp_multi_level_estimate/) | 18.0.1.1.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Allows to consider demand estimates using MRP multi level.
[mrp_package_propagation](mrp_package_propagation/) | 18.0.1.0.0 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Propagate a package from a component to a finished product
[mrp_packaging_default](mrp_packaging_default/) | 18.0.1.0.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Include packaging info in MRP by default
[mrp_production_allow_recursive](mrp_production_allow_recursive/) | 18.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | MRP Production Allow Recursive
[mrp_production_auto_validate](mrp_production_auto_validate/) | 18.0.1.0.1 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Manufacturing Order Auto-Validation when components are picked
[mrp_production_back_to_draft](mrp_production_back_to_draft/) | 18.0.1.0.1 |  | Allows to return to draft a confirmed or cancelled MO.
[mrp_production_check_bom_alignment](mrp_production_check_bom_alignment/) | 18.0.1.0.1 |  | Verify that a Manufacturing Order's components and workorder are consistent with its Bill of Materials.
[mrp_production_location_picking_type](mrp_production_location_picking_type/) | 18.0.1.0.1 |  | Add production location field to picking types for MRP operations.
[mrp_production_note](mrp_production_note/) | 18.0.1.0.0 |  | Notes in production orders
[mrp_production_picking_type_from_route](mrp_production_picking_type_from_route/) | 18.0.1.0.0 |  | Updates the operation type creating MO based on the product
[mrp_production_putaway_strategy](mrp_production_putaway_strategy/) | 18.0.1.0.0 |  | Applies putaway strategies to manufacturing orders for finished products.
[mrp_repair_order](mrp_repair_order/) | 18.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Create repair order from manufacturing order
[mrp_restrict_lot](mrp_restrict_lot/) | 18.0.1.0.3 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | MRP Restrict Lot
[mrp_sale_info](mrp_sale_info/) | 18.0.1.2.0 |  | Adds sale information to Manufacturing models
[mrp_stock_move_actual_date](mrp_stock_move_actual_date/) | 18.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Extend actual date handling to manufacturing and unbuild orders
[mrp_stock_move_line_qty_picked](mrp_stock_move_line_qty_picked/) | 18.0.1.0.0 |  | Adapt functionality of stock_move_line_qty_picked into MRP
[mrp_subcontracting_inhibit](mrp_subcontracting_inhibit/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Inhibit subcontracting flow on demand
[mrp_subcontracting_purchase_link](mrp_subcontracting_purchase_link/) | 18.0.1.0.0 |  | Link Purchase Order Line to Subcontract Productions
[mrp_subcontracting_skip_no_negative](mrp_subcontracting_skip_no_negative/) | 18.0.1.0.1 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | MRP Subcontracting Skip No Negative
[mrp_tag](mrp_tag/) | 18.0.1.0.0 |  | Allows to add multiple tags to Manufacturing Orders
[mrp_unbuild_move_link](mrp_unbuild_move_link/) | 18.0.1.0.0 |  | Link the stock moves of manufacturing orders to the respective unbuild orders
[mrp_unbuild_valuation_layer_link](mrp_unbuild_valuation_layer_link/) | 18.0.1.0.0 |  | Unbuild orders display the connected valuation layers
[mrp_warehouse_calendar](mrp_warehouse_calendar/) | 18.0.1.0.1 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> | Considers the warehouse calendars in manufacturing
[mrp_workcenter_scrap_reason](mrp_workcenter_scrap_reason/) | 18.0.1.0.0 |  | Filter allowed reason codes with workcenter assigned.
[mrp_workorder_blocking_time](mrp_workorder_blocking_time/) | 18.0.1.0.0 | <a href='https://github.com/imlopes'><img src='https://github.com/imlopes.png' width='32' height='32' style='border-radius:50%;' alt='imlopes'/></a> | Allow to block time on work orders
[mrp_workorder_sequence](mrp_workorder_sequence/) | 18.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | adds sequence to production work orders.
[printing_auto_mrp](printing_auto_mrp/) | 18.0.1.0.1 |  | Printing Auto MRP
[quality_control_oca](quality_control_oca/) | 18.0.1.4.0 |  | Generic infrastructure for quality tests.
[quality_control_stock_oca](quality_control_stock_oca/) | 18.0.1.2.0 |  | Quality control - Stock (OCA)
[sale_mrp_bom_menu](sale_mrp_bom_menu/) | 18.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Add a Sales > Products > Bills of Materials menu
[stock_whole_kit_constraint](stock_whole_kit_constraint/) | 18.0.1.0.0 |  | Avoid to deliver a kit partially

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/manufacture-reporting


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/manufacture-reporting&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/manufacture-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/manufacture-reporting/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/manufacture-reporting/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/manufacture-reporting/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/manufacture-reporting/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/manufacture-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/manufacture-reporting-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/manufacture-reporting-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# manufacture-reporting

manufacture-reporting

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[mrp_bom_current_stock](mrp_bom_current_stock/) | 18.0.1.0.0 |  | Add a report that explodes the bill of materials and show the stock available in the source location.
[mrp_bom_matrix_report](mrp_bom_matrix_report/) | 18.0.1.0.0 |  | MRP BOM Matrix Report
[mrp_bom_structure_xlsx](mrp_bom_structure_xlsx/) | 18.0.1.0.0 |  | Export BoM Structure to Excel .XLSX
[mrp_flattened_bom_xlsx](mrp_flattened_bom_xlsx/) | 18.0.1.0.0 |  | Export Flattened BOM to Excel

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/margin-analysis


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/margin-analysis&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/margin-analysis/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/margin-analysis/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/margin-analysis/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/margin-analysis/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/margin-analysis/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/margin-analysis)
[![Translation Status](https://translation.odoo-community.org/widgets/margin-analysis-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/margin-analysis-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# margin-analysis

margin-analysis

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_invoice_margin](account_invoice_margin/) | 18.0.1.0.1 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Show margin in invoices
[account_invoice_margin_sale](account_invoice_margin_sale/) | 18.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> | Set margin in invoices from sale orders
[product_replenishment_cost](product_replenishment_cost/) | 18.0.1.0.0 |  | Provides an overridable method on product which computethe Replenishment cost of a product
[product_standard_margin](product_standard_margin/) | 18.0.1.1.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Product Margin and Margin Rate
[product_standard_margin_security](product_standard_margin_security/) | 18.0.1.0.0 |  | Security for product standard margin
[sale_elaboration_margin](sale_elaboration_margin/) | 18.0.1.0.0 |  | Compute elaboration margins in sale orders lines
[sale_margin_delivered](sale_margin_delivered/) | 18.0.1.0.1 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Sale Margin Delivered
[sale_margin_delivered_dropshipping](sale_margin_delivered_dropshipping/) | 18.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Sale Margin Delivered Dropshipping
[sale_margin_delivered_security](sale_margin_delivered_security/) | 18.0.1.0.1 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Glue module between sale margin delivered and sale margin security modules
[sale_margin_security](sale_margin_security/) | 18.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Sale Margin Security
[sale_margin_sync](sale_margin_sync/) | 18.0.1.0.0 |  | Recompute sale margin when stock move cost price is changed
[sale_report_margin](sale_report_margin/) | 18.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Sale Report Margin

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/mass-mailing


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/mass-mailing&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/mass-mailing/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/mass-mailing/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/mass-mailing/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/mass-mailing/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/mass-mailing/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/mass-mailing)
[![Translation Status](https://translation.odoo-community.org/widgets/mass-mailing-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/mass-mailing-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# mass-mailing

mass-mailing

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[mass_mailing_custom_unsubscribe](mass_mailing_custom_unsubscribe/) | 18.0.1.1.0 |  | Track metadata for GDPR compliance
[mass_mailing_event_registration_exclude](mass_mailing_event_registration_exclude/) | 18.0.1.0.0 |  | Link mass mailing with event for excluding recipients
[mass_mailing_list_dynamic](mass_mailing_list_dynamic/) | 18.0.1.0.2 |  | Mass mailing lists that get autopopulated
[mass_mailing_partner](mass_mailing_partner/) | 18.0.1.2.0 |  | Link partners with mass-mailing
[mass_mailing_resend](mass_mailing_resend/) | 18.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Resend mass mailings

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/mis-builder

[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# MIS Builder

[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# MIS Builder
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/mis-builder&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/mis-builder/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/mis-builder/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/mis-builder/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/mis-builder/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/mis-builder/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/mis-builder)
[![Translation Status](https://translation.odoo-community.org/widgets/mis-builder-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/mis-builder-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Management Information System reports for Odoo: easily build super fast,
beautiful, custom reports such as P&L, Balance Sheets and more.

This project implements a class of reports where KPI (Key Performance Indicators)
are displayed in rows, and time periods in columns. It focuses on very fast reporting
on accounting data but can also use data from any other Odoo model.

It features the following key characteristics:

- User configurable: end users can create new report templates without development,
  using simple Excel-like formulas.
- Very fast balance reporting for accounting data, even on million lines databases
  and very complex account charts.
- Use the same template for different reports.
- Compare data over different time periods.
- User-configurable styles, rendered perfectly in the UI as well as Excel and PDF exports.
- Interactive display with drill-down.
- Export to PDF and Excel.
- A budgeting module.
- Evaluate KPI over various data sources, such as actuals, simulation, committed costs
  (some custom development is required to create the data source).
- For developers, the accounting balance computation engine is exposed as an easy
  to use API.

Here are some presentations:

- OCA Days 2020 ([video](https://www.youtube.com/watch?v=45FXd8XM5m8))
- Odoo Experience 2017 ([slides](https://www.slideshare.net/acsone/budget-control-with-misbuilder-3-2017), [video](https://youtu.be/0PpxGAf2l-0))
- Odoo Experience 2016 ([slides](https://www.slideshare.net/acsone/misbuilder-2016))
- Odoo Experience 2015 ([slides](https://www.slideshare.net/acsone/misbuilder))

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[mis_builder](mis_builder/) | 18.0.1.8.3 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Build 'Management Information System' Reports and Dashboards
[mis_builder_budget](mis_builder_budget/) | 18.0.2.0.0 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Create budgets for MIS reports
[mis_builder_demo](mis_builder_demo/) | 18.0.1.0.0 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Demo addon for MIS Builder

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/module-composition-analysis

[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# module-composition-analysis
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/module-composition-analysis&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/module-composition-analysis/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/module-composition-analysis/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/module-composition-analysis/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/module-composition-analysis/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/module-composition-analysis/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/module-composition-analysis)
[![Translation Status](https://translation.odoo-community.org/widgets/module-composition-analysis-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/module-composition-analysis-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

module-composition-analysis

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[odoo_project](odoo_project/) | 18.0.1.0.1 |  | Analyze your Odoo projects code bases.
[odoo_project_changelog](odoo_project_changelog/) | 18.0.1.0.0 |  | Generate Changelogs from repositories for installed modules.
[odoo_project_migration](odoo_project_migration/) | 18.0.1.0.0 |  | Analyze your Odoo project migrations.
[odoo_repository](odoo_repository/) | 18.0.1.1.4 |  | Base module to host data collected from Odoo repositories.
[odoo_repository_migration](odoo_repository_migration/) | 18.0.1.0.1 |  | Collect modules migration data for Odoo Repositories.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/multi-company


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/multi-company&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/multi-company/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/multi-company/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/multi-company/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/multi-company/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/multi-company/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/multi-company)
[![Translation Status](https://translation.odoo-community.org/widgets/multi-company-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/multi-company-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# multi-company

multi-company

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_invoice_inter_company](account_invoice_inter_company/) | 18.0.1.0.4 |  | Intercompany invoice rules
[account_multicompany_easy_creation](account_multicompany_easy_creation/) | 18.0.1.0.1 |  | This module adds a wizard to create companies easily
[base_multi_company](base_multi_company/) | 18.0.1.1.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Provides a base for adding multi-company support to models.
[calendar_event_multi_company](calendar_event_multi_company/) | 18.0.1.0.0 |  | This module add multi-company management to calendar events
[calendar_event_type_multi_company](calendar_event_type_multi_company/) | 18.0.1.0.0 |  | This module add multi-company management to calendar event type
[crm_lost_reason_multi_company](crm_lost_reason_multi_company/) | 18.0.1.0.0 |  | This module add multi-company management to crm lost reason
[crm_stage_multi_company](crm_stage_multi_company/) | 18.0.1.0.0 |  | This module adds support for multi company on crm stage.
[crm_tag_multi_company](crm_tag_multi_company/) | 18.0.1.0.0 |  | This module add multi-company management to crm tag
[hr_employee_multi_company](hr_employee_multi_company/) | 18.0.1.0.0 |  | This module add multi-company management to HR Employee
[ir_filters_multi_company](ir_filters_multi_company/) | 18.0.1.0.0 |  | This module add multi-company management to user-defined filters
[ir_ui_view_multi_company](ir_ui_view_multi_company/) | 18.0.1.0.0 |  | This module allows companies operating in a multi-company environment to define custom views for specific companies.
[login_all_company](login_all_company/) | 18.0.0.0.0 |  | Access all your companies when you log in
[mail_multicompany](mail_multicompany/) | 18.0.1.0.0 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Email Gateway Multi company
[mail_template_multi_company](mail_template_multi_company/) | 18.0.1.0.0 | <a href='https://github.com/Olivier-LAURENT'><img src='https://github.com/Olivier-LAURENT.png' width='32' height='32' style='border-radius:50%;' alt='Olivier-LAURENT'/></a> | Mail Template Multi Company
[partner_category_multi_company](partner_category_multi_company/) | 18.0.1.0.0 |  | This module add multi-company management to partner categories
[partner_multi_company](partner_multi_company/) | 18.0.1.0.2 |  | Select individually the partner visibility on each company
[pos_category_multicompany](pos_category_multicompany/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Point of Sale Category in Multi company context
[product_multi_company](product_multi_company/) | 18.0.1.0.0 |  | Select individually the product template visibility on each company
[product_multi_company_stock](product_multi_company_stock/) | 18.0.1.0.1 |  | Does not allow to remove company if there is stock or moves in that company
[product_tax_multicompany_default](product_tax_multicompany_default/) | 18.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Product Tax Multi Company Default
[purchase_sale_inter_company](purchase_sale_inter_company/) | 18.0.1.0.5 |  | Intercompany PO/SO rules
[purchase_sale_stock_inter_company](purchase_sale_stock_inter_company/) | 18.0.1.0.3 |  | Intercompany PO/SO rules with warehouse
[res_company_active](res_company_active/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add the 'active' feature on company model
[res_company_category](res_company_category/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Company Categories
[res_company_code](res_company_code/) | 18.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add 'code' field on company model
[res_company_search_view](res_company_search_view/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add a search view for company model
[res_partner_industry_multi_company](res_partner_industry_multi_company/) | 18.0.1.0.1 |  | This module add multi-company management to res partner industry
[stock_intercompany](stock_intercompany/) | 18.0.1.0.0 |  | Stock Intercompany Delivery-Reception
[utm_medium_multi_company](utm_medium_multi_company/) | 18.0.1.0.0 |  | This module add multi-company management to utm medium
[utm_source_multi_company](utm_source_multi_company/) | 18.0.1.0.0 |  | This module add multi-company management to utm source

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/oca-custom

# Contribute to the OCA's Odoo instance (kick-starter guide)

This one-pager guide aims to help happy volunteers to contribute to the OCA's Odoo
instance, supposedly the OCA's Internal Tools team.

## Table of content

1. [Introduction](#introduction): who we are, how we work
2. [Getting Started](#getting-started)
   - [Concepts](#concepts): main concepts to understand and general organization
   - [Processes](#processes): helping doing the work without missing crucial steps
   - [How-Tos](#how-tos): how to do specific tasks
3. [FAQ](#FAQ)

## Introduction

This repository is managed by OCA's Internal Tools team:

- email: [internaltools@odoo-community.org](mailto:internaltools@odoo-community.org)
- [Github team page](https://github.com/orgs/OCA/teams/internal-tools)
- [Github project Kanban](https://github.com/orgs/OCA/projects/13)

Please refer to the document
[Scope & Objective](https://docs.google.com/document/d/1RcOUstPJDev1bgPZcNXWiHBt5PeqraisU5bKIZatcnY/edit?pli=1&tab=t.0#heading=h.jrsgv4k2u2ao)
to understand the governance and missions of the Internal Tools team within the OCA.
Under the watch of OCA board, this document mainly explains:

- The "Raison d'être" of the Internal Tools group
- Tasks and responsabilities
- Autonomy scope
- How to become part of the group
- Internal governances (leaders & members)
- Useful processes to start working in the group

## Getting Started

This section will guide you to:

1. Build a test environment on a developer's machine, replicating OCA's Odoo production
   instance
2. Push a change in production to OCA's Odoo production instance

### Concepts

This repository is setup as other OCA's repositories to launch CI as usual and as an
extra configuration in order to build the OCA' Docker image used by our Odoo instance,
as well as facilitate the bootstrapping of a development environment.

Managing and freezing modules versions rely on python tools:

- [uv](https://docs.astral.sh/uv/)
- [hatch-odoo](https://pypi.org/project/hatch-odoo/)

### Processes

Here we focus on what to do without explaining how to do it.

### Release

While we are building and publishing a docker image the current state is that the image
is build at deploy time on OCA server.

While technically speaking there is nothing more than accessing to a public commit to
deploy a new version it's a common practice to merge your work on branch 14.0 before
deploying a new version in production.

> **Note**: in this repository we allow unreleased dependencies.

#### Deployment

Ask administrator to deploy the given commit.

### How-Tos

Here we focus on how to do it, it's a suggest way to works but feel free to use your own
way.

#### Setup developer environment

Requirements:

- **uv**: several methods exist to install it, one can be
  `curl -LsSf https://astral.sh/uv/install.sh | sh`. It will install other
  prerequisites.
- Postgresql
- Some dependencies to be able to build some python packages: `libpq-dev`,
  `build-essential`, ...
- wkhtmltopdf

Run the following commands to prepare a python virtual environment with the correct
python version (which uv will download for you if necessary) and install the required
dependencies:

```bash
git clone git@github.com:OCA/oca-custom -branch 14.0
cd oca-custom
uv sync
```

#### Setup database

Setup database with demo data and all OCA modules installed:

```bash
uv run odoo -d oca-custom -i oca_all --stop-after-init --without-demo=
```

The `oca_all` module contains the `__manifest__.py` with all Odoo modules dependencies
for the OCA Odoo instance.

#### Neutralize database

If you are allow to access to a production database, neutralization happens while
stating the Docker container if the running environnement is not the production server.

On development, if your are not using docker you can running neutralize scripts such as:

```bash
 find entrypoints/neutralize/*.sql -type f -exec  psql <dbname> -f {} \;
```

#### Development

For addons living in this repository, you can just change code and restart Odoo with the
`uv run` command.

For addons in other repositories, the procedure is as follows:

- check out the repository somewhere, ie /src/\$repo
- add the following line to `pyproject.toml` in the `[tool.uv.sources]` section:

  ```pyproject
  odoo14-addon-$youraddon = { path = "/srv/$repo/setup/$youraddon", editable = true }
  ```

- run `uv sync`
- restart Odoo

#### Use unreleased dependency

There is two different goals:

- making the test CI pass: using regular test-requirements.txt files add a line such as

  ```
  odoo14-addon-membership-delegated-partner-line @ git+https://github.com/OCA/vertical-association@refs/pull/151/head#subdirectory=setup/membership_delegated_partner_line
  ```

- bring the unreleased dependency in the uv project (and the built docker image), add
  the following line to `pyproject.toml` in the `[tool.uv.sources]` section:

  ```pyproject
  odoo14-addon-membership-delegated-partner-line = { git = "https://github.com/OCA/vertical-association", rev = "refs/pull/151/head", subdirectory = "setup/membership_delegated_partner_line" }
  ```

#### Launch tests

Run tests using pytest launcher.

```bash
uv run pytest --odoo-database oca-custom --cov ./oca_psc_team/ oca_psc_team/
```

#### Update OCB Branch

```bash
uv sync -P odoo
```

#### Update a specific OCA module dependency using the latest pypi release

```bash
uv sync -P odoo14-addon-<module-name>
```

Note bug https://github.com/astral-sh/uv/issues/14684, that says if multiple packages
are sourced from the same branch/PR, we need to specify both of them as to upgrade,
otherwise they don't get rescanned.

#### Bump all dependencies to the latest version

```bash
uv sync -U
```

## FAQ

#### How can I start contributing in OCA toolings?

- Get to know the manifest document of OCA's Internal Tools team:
  [Scope & Objective](https://docs.google.com/document/d/1RcOUstPJDev1bgPZcNXWiHBt5PeqraisU5bKIZatcnY/edit?pli=1&tab=t.0#heading=h.jrsgv4k2u2ao).
- Write to us at
  [internaltools@odoo-community.org](mailto:internaltools@odoo-community.org).
- Install a test environment on your machine of the OCA's Odoo instance by following the
  [§ Getting Started](#getting-started).

#### How to communicate with the OCA Internal Tools?

Our main communication channel is the mailing list
[internaltools@odoo-community.org](mailto:internaltools@odoo-community.org). For
task-related discussion, also directly use the Chatter of the Odoo tasks.

#### Where is the tasks backlog of the OCA Internal Tools?

We use the Odoo project **OCA internal tools workgroup** on the OCA's Odoo instance to
organize our tasks and priorities. A public access to the project can be provided to OCA
members who contributes to the tooling tasks (not requesting privacy form signing).

#### How to access the backend of OCA's Odoo instance?

It can be useful to access Odoo back-end for both task management and browse instance's
modules and data. For such, prerquisites are:

- being a member of the OCA and the **OCA Internal Tools group**
- be registered on OCA's Odoo instance
- fullfil and send back the **Data protection & privacy** form, available on OCA website
  [Resources / How to guides / Protect data & privacy when you support OCA projects](https://odoo-community.org/privacy)

#### What are useful Github repositories?

- The current **oca-custom** is the main repository. It contains both all Odoo modules
  dependencies of OCA instance in `oca_all/__manifest__.py` and all configuration to
  build an Odoo test instance the `uv`, as described in
  [Getting Started](#getting-started).
- [**apps-store**](https://github.com/OCA/apps-store/tree/14.0) holds mechanisms of OCA
  modules replication to official Odoo's App Store

#### How to get representive data, for troubleshooting and test?

Contact the mailing list to get a neutralized and anonymized database.

#### How to gain command line access and read logs?

Only a few people have admin server access, please reach the mailing list for further
details.

#### How to refresh test instance from production instances (on the server)?

`home/odoo/instance/README` gives some guidance.


---

## From OCA/odoo-pim


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/odoo-pim&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/odoo-pim/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/odoo-pim/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/odoo-pim/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/odoo-pim/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/odoo-pim/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/odoo-pim)
[![Translation Status](https://translation.odoo-community.org/widgets/odoo-pim-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/odoo-pim-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# odoo-pim

Product Information Management.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[attribute_set](attribute_set/) | 18.0.1.0.0 |  | Attribute Set
[pim](pim/) | 18.0.1.0.0 |  | Product Information Management
[product_attribute_set](product_attribute_set/) | 18.0.1.0.0 |  | Product Attribute Set

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/operating-unit


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/operating-unit&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/operating-unit/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/operating-unit/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/operating-unit/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/operating-unit/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/operating-unit/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/operating-unit)
[![Translation Status](https://translation.odoo-community.org/widgets/operating-unit-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/operating-unit-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# operating-unit

operating-unit

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_operating_unit](account_operating_unit/) | 18.0.1.0.2 |  | Introduces Operating Unit (OU) in invoices and Accounting Entries with clearing account
[analytic_operating_unit](analytic_operating_unit/) | 18.0.1.0.0 |  | Analytic Operating Unit
[crm_operating_unit](crm_operating_unit/) | 18.0.1.0.0 |  | Operating Unit in CRM
[mrp_operating_unit](mrp_operating_unit/) | 18.0.1.0.0 |  | Operating Unit in MRP
[operating_unit](operating_unit/) | 18.0.1.0.1 |  | An operating unit (OU) is an organizational entity part of a company
[operating_unit_access_all](operating_unit_access_all/) | 18.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Access all Operating Units
[product_operating_unit](product_operating_unit/) | 18.0.1.0.0 |  | Adds the concept of operating unit (OU) in products
[purchase_operating_unit](purchase_operating_unit/) | 18.0.1.0.0 |  | Adds the concecpt of operating unit (OU) in purchase order management
[purchase_stock_operating_unit](purchase_stock_operating_unit/) | 18.0.1.0.0 | <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Copies the operating unit of purchase picking to the stock picking
[report_qweb_operating_unit](report_qweb_operating_unit/) | 18.0.1.1.0 |  | Qweb Report With Operating Unit
[res_partner_operating_unit](res_partner_operating_unit/) | 18.0.1.1.1 |  | Introduces Operating Unit fields in Partner
[sale_operating_unit](sale_operating_unit/) | 18.0.1.0.0 |  | An operating unit (OU) is an organizational entity part of a company
[sale_stock_operating_unit](sale_stock_operating_unit/) | 18.0.1.0.0 |  | An operating unit (OU) is an organizational entity part of a company
[sales_team_operating_unit](sales_team_operating_unit/) | 18.0.1.0.0 |  | Sales Team Operating Unit
[stock_operating_unit](stock_operating_unit/) | 18.0.1.0.0 |  | Adds the concept of operating unit (OU) in stock management
[stock_operating_unit_access_all](stock_operating_unit_access_all/) | 18.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Access all OUs' Stock

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/partner-contact


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/partner-contact&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/partner-contact/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/partner-contact/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/partner-contact/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/partner-contact/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/partner-contact/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/partner-contact)
[![Translation Status](https://translation.odoo-community.org/widgets/partner-contact-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/partner-contact-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# partner-contact

partner-contact

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_partner_company_group](account_partner_company_group/) | 18.0.2.0.0 |  | Adds the possibility to add a company group to a company
[animal](animal/) | 18.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Manage animals information
[base_country_state_translatable](base_country_state_translatable/) | 18.0.1.0.0 |  | Translate Country States
[base_location](base_location/) | 18.0.1.1.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Enhanced zip/npa management system
[base_location_geonames_import](base_location_geonames_import/) | 18.0.1.0.0 |  | Import zip entries from Geonames
[base_location_nuts](base_location_nuts/) | 18.0.1.3.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> | NUTS Regions
[base_partner_company_group](base_partner_company_group/) | 18.0.1.1.0 |  | Adds the possibility to add a company group to a company
[base_partner_sequence](base_partner_sequence/) | 18.0.1.2.0 |  | Sets customer's code from a sequence
[crm_partner_company_group](crm_partner_company_group/) | 18.0.2.0.0 |  | Adds the possibility to add a company group to a company
[partner_accreditation](partner_accreditation/) | 18.0.1.0.0 | <a href='https://github.com/victor-champonnois'><img src='https://github.com/victor-champonnois.png' width='32' height='32' style='border-radius:50%;' alt='victor-champonnois'/></a> | Add Accreditation to Partners
[partner_address_split](partner_address_split/) | 18.0.1.0.0 |  | Add specific helper methods
[partner_address_street3](partner_address_street3/) | 18.0.1.0.0 |  | Add a third address line on partners
[partner_affiliate](partner_affiliate/) | 18.0.1.0.0 |  | Partner Affiliates
[partner_archive_propagate](partner_archive_propagate/) | 18.0.1.0.0 | <a href='https://github.com/ntsirintanis'><img src='https://github.com/ntsirintanis.png' width='32' height='32' style='border-radius:50%;' alt='ntsirintanis'/></a> | Archive/unarchive partner contacts hierarchically
[partner_bank_acc_holder_name](partner_bank_acc_holder_name/) | 18.0.1.0.0 |  | Show the account holder name field on bank accounts
[partner_bank_code](partner_bank_code/) | 18.0.1.0.0 |  | Add fields information in banks
[partner_capital](partner_capital/) | 18.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Partners Capital
[partner_category_description](partner_category_description/) | 18.0.1.0.1 | <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Adds a description field to contact categories to improve organization and managment of customer relationships.
[partner_category_security](partner_category_security/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Partner category security
[partner_category_type](partner_category_type/) | 18.0.1.0.1 | <a href='https://github.com/JordiMForgeFlow'><img src='https://github.com/JordiMForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiMForgeFlow'/></a> | Add a selection field 'Type' to classify Contact Tags.
[partner_company_default](partner_company_default/) | 18.0.1.0.1 |  | Partner Company Default
[partner_company_type](partner_company_type/) | 18.0.1.0.0 |  | Adds a company type to partner that are companies
[partner_contact_access_link](partner_contact_access_link/) | 18.0.1.0.0 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Allow to visit the full contact form from a company
[partner_contact_address_default](partner_contact_address_default/) | 18.0.1.0.1 |  | Set a default delivery address, invoice address and contact for contacts
[partner_contact_age_range](partner_contact_age_range/) | 18.0.1.0.1 |  | Age Range for Contact's
[partner_contact_birthdate](partner_contact_birthdate/) | 18.0.1.0.0 | <a href='https://github.com/Daemo00'><img src='https://github.com/Daemo00.png' width='32' height='32' style='border-radius:50%;' alt='Daemo00'/></a> | Contact's birthdate
[partner_contact_birthplace](partner_contact_birthplace/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | This module allows to define a birthplace for partners.
[partner_contact_department](partner_contact_department/) | 18.0.1.0.1 |  | Assign contacts to departments
[partner_contact_gender](partner_contact_gender/) | 18.0.1.0.0 |  | Add gender field to contacts
[partner_contact_job_position](partner_contact_job_position/) | 18.0.1.0.0 |  | Categorize job positions for contacts
[partner_contact_lang](partner_contact_lang/) | 18.0.1.0.0 |  | Manage language in contacts
[partner_contact_nationality](partner_contact_nationality/) | 18.0.1.0.0 |  | Add nationality field to contacts
[partner_contact_personal_information_page](partner_contact_personal_information_page/) | 18.0.1.0.0 | <a href='https://github.com/Daemo00'><img src='https://github.com/Daemo00.png' width='32' height='32' style='border-radius:50%;' alt='Daemo00'/></a> | Add a page to contacts form to put personal information
[partner_contact_role](partner_contact_role/) | 18.0.1.0.0 |  | Add roles to partners.
[partner_contact_tags_in_popup](partner_contact_tags_in_popup/) | 18.0.1.0.0 | <a href='https://github.com/carmenbianca'><img src='https://github.com/carmenbianca.png' width='32' height='32' style='border-radius:50%;' alt='carmenbianca'/></a> | Display a contact's tags in the 'Contacts & Addresses' pop-up form view.
[partner_contact_type_end_user](partner_contact_type_end_user/) | 18.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Adds a new contact type 'End User'
[partner_country_lang](partner_country_lang/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Partner language according country
[partner_country_state_required](partner_country_state_required/) | 18.0.1.0.0 |  | Partner Country State Required
[partner_deduplicate_acl](partner_deduplicate_acl/) | 18.0.1.0.0 |  | Contact deduplication with fine-grained permission control
[partner_deduplicate_by_ref](partner_deduplicate_by_ref/) | 18.0.1.0.0 |  | Deduplicate Contacts by reference
[partner_deduplicate_by_website](partner_deduplicate_by_website/) | 18.0.1.0.0 |  | Deduplicate Contacts by Website
[partner_deduplicate_filter](partner_deduplicate_filter/) | 18.0.1.0.0 |  | Exclude records from the deduplication
[partner_disable_gravatar](partner_disable_gravatar/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Disable automatic connection to gravatar.com
[partner_duns](partner_duns/) | 18.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Set DUNS (Data Universal Numbering System) on partners
[partner_email_check](partner_email_check/) | 18.0.1.0.0 |  | Validate email address field
[partner_email_duplicate_warn](partner_email_duplicate_warn/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Warning banner on partner form if other partners have the same email
[partner_employee_quantity](partner_employee_quantity/) | 18.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | Know how many employees a partner has
[partner_external_map](partner_external_map/) | 18.0.2.0.0 |  | Add Map and Map Routing buttons on partner form to open GMaps, OSM, Bing and others
[partner_fax](partner_fax/) | 18.0.1.0.0 |  | Add fax number on partner
[partner_firstname](partner_firstname/) | 18.0.6.2.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Split first name and last name for non company partners
[partner_firstname_portal](partner_firstname_portal/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Glue module to make working portal and partner firstname module together
[partner_identification](partner_identification/) | 18.0.1.1.0 |  | Partner Identification Numbers
[partner_identification_eori](partner_identification_eori/) | 18.0.1.0.0 |  | This addon extends "Partner Identification Numbers" to provide a number category for EORI Number
[partner_identification_gln](partner_identification_gln/) | 18.0.1.0.0 |  | This addon extends "Partner Identification Numbers" to provide a number category for GLN registration
[partner_identification_unique_by_category](partner_identification_unique_by_category/) | 18.0.1.0.0 |  | Partner Identification Numbers Unique By Category
[partner_industry_parent](partner_industry_parent/) | 18.0.1.0.0 |  | This module add a parent relation to the partner industry
[partner_industry_secondary](partner_industry_secondary/) | 18.0.1.0.1 |  | Add secondary partner industries
[partner_interest_group](partner_interest_group/) | 18.0.1.0.0 | <a href='https://github.com/victor-champonnois'><img src='https://github.com/victor-champonnois.png' width='32' height='32' style='border-radius:50%;' alt='victor-champonnois'/></a> | Add Interest Group to Partners
[partner_is_company_auth_signup](partner_is_company_auth_signup/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Asks users who register whether they are individuals or companies
[partner_label](partner_label/) | 18.0.1.0.0 |  | Print partner labels
[partner_manual_rank](partner_manual_rank/) | 18.0.1.1.0 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> <a href='https://github.com/frahikLV'><img src='https://github.com/frahikLV.png' width='32' height='32' style='border-radius:50%;' alt='frahikLV'/></a> | Be able to manually flag partners as customer or supplier.
[partner_middlename](partner_middlename/) | 18.0.1.0.0 |  | Have split Middle
[partner_mobile_duplicate_warn](partner_mobile_duplicate_warn/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Warning banner on partner form if another partner has the same mobile
[partner_multi_relation](partner_multi_relation/) | 18.0.1.0.0 |  | Partner Relations
[partner_multi_relation_function](partner_multi_relation_function/) | 18.0.1.0.0 | <a href='https://github.com/NL66278'><img src='https://github.com/NL66278.png' width='32' height='32' style='border-radius:50%;' alt='NL66278'/></a> | Partner Relation Functions
[partner_phone_secondary](partner_phone_secondary/) | 18.0.1.0.1 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Adds a secondary phone number on partners
[partner_phonecall_schedule](partner_phonecall_schedule/) | 18.0.1.0.0 |  | Track the time and days your partners expect phone calls
[partner_pricelist_search](partner_pricelist_search/) | 18.0.1.0.0 |  | Partner pricelist search
[partner_pricelist_tracking](partner_pricelist_tracking/) | 18.0.1.0.0 |  | Track partner pricelist changes
[partner_priority](partner_priority/) | 18.0.1.0.0 | <a href='https://github.com/patrickrwilson'><img src='https://github.com/patrickrwilson.png' width='32' height='32' style='border-radius:50%;' alt='patrickrwilson'/></a> | Adds priority to partners.
[partner_property](partner_property/) | 18.0.1.0.3 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Partner Property
[partner_purchase_manager](partner_purchase_manager/) | 18.0.1.0.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Add purchase manager field in partner
[partner_rank_commercial_entity](partner_rank_commercial_entity/) | 18.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> <a href='https://github.com/yankinmax'><img src='https://github.com/yankinmax.png' width='32' height='32' style='border-radius:50%;' alt='yankinmax'/></a> | Define customer and supplier ranks at the commercial entity level.
[partner_rank_single](partner_rank_single/) | 18.0.2.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> <a href='https://github.com/yankinmax'><img src='https://github.com/yankinmax.png' width='32' height='32' style='border-radius:50%;' alt='yankinmax'/></a> | Introduce single rank for partners.
[partner_readonly_security](partner_readonly_security/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Partner Readonly Security
[partner_ref_unique](partner_ref_unique/) | 18.0.1.0.0 |  | Add an unique constraint to partner ref field
[partner_search_alias](partner_search_alias/) | 18.0.1.0.0 |  | Partner Search Alias
[partner_second_lastname](partner_second_lastname/) | 18.0.2.1.0 |  | Have split first and second lastnames
[partner_shipping_policy](partner_shipping_policy/) | 18.0.1.0.0 |  | Define shipping policy at partners level.
[partner_stage](partner_stage/) | 18.0.1.0.1 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Add lifecycle Stages to Partners
[partner_store](partner_store/) | 18.0.1.0.0 | <a href='https://github.com/wouitmil'><img src='https://github.com/wouitmil.png' width='32' height='32' style='border-radius:50%;' alt='wouitmil'/></a> | Add store type to Partners
[partner_street_city_search](partner_street_city_search/) | 18.0.1.0.0 |  | Enable partner search by street and city
[partner_subject_to_vat](partner_subject_to_vat/) | 18.0.1.0.0 | <a href='https://github.com/victor-champonnois'><img src='https://github.com/victor-champonnois.png' width='32' height='32' style='border-radius:50%;' alt='victor-champonnois'/></a> | Record whether a company is subject to VAT.
[partner_supplier_ref](partner_supplier_ref/) | 18.0.1.0.1 |  | Adds a supplier reference to contacts
[partner_supplier_ref_sequence](partner_supplier_ref_sequence/) | 18.0.1.0.0 |  | Adds a sequence for the Supplier Reference field
[partner_tier_validation](partner_tier_validation/) | 18.0.1.0.0 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Support a tier validation process for Contacts
[partner_title_active](partner_title_active/) | 18.0.1.0.0 |  | Partner Title Active
[partner_title_order](partner_title_order/) | 18.0.1.0.0 |  | Makes partner title sortable by sequence
[partner_type_base](partner_type_base/) | 18.0.2.0.0 |  | Base implementation to improve the address type customization.
[partner_tz](partner_tz/) | 18.0.1.0.1 |  | Remove partner timezone default value and display on form
[partner_vat_unique](partner_vat_unique/) | 18.0.1.0.0 |  | Module to make the VAT number unique for customers and suppliers.
[purchase_supplier_rank](purchase_supplier_rank/) | 18.0.1.0.0 |  | Update Supplier Rank when creating a Purchase Order
[sale_customer_rank](sale_customer_rank/) | 18.0.1.0.0 |  | Update Customer Rank when creating a Sale Order
[sale_partner_company_group](sale_partner_company_group/) | 18.0.2.0.0 |  | Adds the possibility to add a company group to a company


Unported addons
---------------
addon | version | maintainers | summary
--- | --- | --- | ---
[partner_company_group](partner_company_group/) | 18.0.1.0.0 (unported) | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Adds the possibility to add a company group to a company

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/payroll


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/payroll&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/payroll/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/payroll/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/payroll/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/payroll/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/payroll/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/payroll)
[![Translation Status](https://translation.odoo-community.org/widgets/payroll-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/payroll-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# payroll

payroll

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[payroll](payroll/) | 18.0.1.3.2 | <a href='https://github.com/appstogrow'><img src='https://github.com/appstogrow.png' width='32' height='32' style='border-radius:50%;' alt='appstogrow'/></a> <a href='https://github.com/nimarosa'><img src='https://github.com/nimarosa.png' width='32' height='32' style='border-radius:50%;' alt='nimarosa'/></a> | Manage your employee payroll records
[payroll_account](payroll_account/) | 18.0.1.0.6 | <a href='https://github.com/appstogrow'><img src='https://github.com/appstogrow.png' width='32' height='32' style='border-radius:50%;' alt='appstogrow'/></a> <a href='https://github.com/nimarosa'><img src='https://github.com/nimarosa.png' width='32' height='32' style='border-radius:50%;' alt='nimarosa'/></a> | Manage your payroll to accounting
[payroll_contract_advantages](payroll_contract_advantages/) | 18.0.1.0.0 | <a href='https://github.com/nimarosa'><img src='https://github.com/nimarosa.png' width='32' height='32' style='border-radius:50%;' alt='nimarosa'/></a> | Allow to define contract advantages for employees.
[payroll_hr_public_holidays](payroll_hr_public_holidays/) | 18.0.1.0.1 | <a href='https://github.com/nimarosa'><img src='https://github.com/nimarosa.png' width='32' height='32' style='border-radius:50%;' alt='nimarosa'/></a> | Integration between payroll and hr_public_holidays

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/pms


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/pms&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/pms/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/pms/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/pms/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/pms/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/pms/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/pms)
[![Translation Status](https://translation.odoo-community.org/widgets/pms-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/pms-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# pms

pms

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[multi_pms_properties](multi_pms_properties/) | 18.0.1.0.0 |  | Multi Properties Manager

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/pos


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# pos
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/pos&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/pos/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/pos/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/pos/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/pos/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/pos/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/pos)
[![Translation Status](https://translation.odoo-community.org/widgets/pos-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/pos-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

pos

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[pos_barcode_rule_priced_with_change_rate](pos_barcode_rule_priced_with_change_rate/) | 18.0.1.0.0 |  | Add a barcode rule to be able to scan a barcode with price encoded (as the standard "Priced Product" rule), and convert the price according to a given change rate.
[pos_blind_session_closing](pos_blind_session_closing/) | 18.0.1.0.0 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> | Hide cash control details in the closing popup
[pos_config_logo](pos_config_logo/) | 18.0.1.0.0 |  | Set logotypes different from the company's one
[pos_customer_tree_view_vat](pos_customer_tree_view_vat/) | 18.0.1.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | Point of Sale: Show VAT number at Customer Tree View
[pos_display_order_number](pos_display_order_number/) | 18.0.1.0.1 | <a href='https://github.com/henrybackman'><img src='https://github.com/henrybackman.png' width='32' height='32' style='border-radius:50%;' alt='henrybackman'/></a> | POS - Display order number in order summary
[pos_display_total_quantity](pos_display_total_quantity/) | 18.0.1.0.1 | <a href='https://github.com/henrybackman'><img src='https://github.com/henrybackman.png' width='32' height='32' style='border-radius:50%;' alt='henrybackman'/></a> | POS - Display total quantity in order summary
[pos_divide_order_summary](pos_divide_order_summary/) | 18.0.1.0.1 | <a href='https://github.com/henrybackman'><img src='https://github.com/henrybackman.png' width='32' height='32' style='border-radius:50%;' alt='henrybackman'/></a> | POS - Divider order summary
[pos_lot_barcode](pos_lot_barcode/) | 18.0.1.0.1 |  | Scan barcode to enter lot/serial numbers
[pos_margin](pos_margin/) | 18.0.1.1.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Margin on PoS Order
[pos_order_remove_line](pos_order_remove_line/) | 18.0.1.0.0 | <a href='https://github.com/robyf70'><img src='https://github.com/robyf70.png' width='32' height='32' style='border-radius:50%;' alt='robyf70'/></a> | Add button to remove POS order line.
[pos_order_to_sale_order](pos_order_to_sale_order/) | 18.0.1.1.2 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | PoS Order To Sale Order
[pos_partner_birthdate](pos_partner_birthdate/) | 18.0.1.0.0 | <a href='https://github.com/ecino'><img src='https://github.com/ecino.png' width='32' height='32' style='border-radius:50%;' alt='ecino'/></a> | Adds the birthdate in the customer screen of POS
[pos_payment_method_cashdro](pos_payment_method_cashdro/) | 18.0.1.0.2 |  | Allows to pay with CashDro Terminals on the Point of Sale
[pos_payment_terminal](pos_payment_terminal/) | 18.0.1.0.0 |  | Point of sale: support generic payment terminal
[pos_product_display_default_code](pos_product_display_default_code/) | 18.0.1.0.1 |  | pos: display product default code before product name
[pos_product_multi_barcode](pos_product_multi_barcode/) | 18.0.1.0.0 |  | Make product multi barcodes usable in the point of sale
[pos_report_session_summary](pos_report_session_summary/) | 18.0.1.0.0 |  | Adds a Session Summary PDF report on the POS session
[pos_sale_picking_keep](pos_sale_picking_keep/) | 18.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Keep sale pickings from PoS
[pos_session_pay_invoice](pos_session_pay_invoice/) | 18.0.1.0.0 |  | Pay and receive invoices from PoS Session
[pos_supplierinfo_search](pos_supplierinfo_search/) | 18.0.1.0.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Search products by supplier data
[pos_user_restrict_provider_info](pos_user_restrict_provider_info/) | 18.0.1.0.0 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> | Restrict provider info to pos users
[pos_user_restriction](pos_user_restriction/) | 18.0.1.0.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Restrict some users to see and use only certain points of sale

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/product-attribute


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/product-attribute&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/product-attribute/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/product-attribute/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/product-attribute/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/product-attribute/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/product-attribute/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/product-attribute)
[![Translation Status](https://translation.odoo-community.org/widgets/product-attribute-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/product-attribute-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# product-attribute

product-attribute

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[nutritional_info](nutritional_info/) | 18.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Nutritional information.
[pos_product_cost_security](pos_product_cost_security/) | 18.0.1.0.0 |  | Compatibility between Point of Sale and Product Cost Security
[product_abc_classification](product_abc_classification/) | 18.0.1.0.0 |  | ABC classification for sales and warehouse management
[product_assortment](product_assortment/) | 18.0.1.0.1 |  | Adds the ability to manage products assortment
[product_attachment_zipped_download](product_attachment_zipped_download/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Product Attachment Zipped Download
[product_attribute_archive](product_attribute_archive/) | 18.0.1.0.0 |  | Add an active field on product attributes
[product_attribute_value_avoid_auto_fill](product_attribute_value_avoid_auto_fill/) | 18.0.1.0.0 |  | Add option allow filling automatically the values
[product_attribute_value_menu](product_attribute_value_menu/) | 18.0.1.0.1 |  | Product attributes values tree and form. Import attribute values.
[product_barcode_required](product_barcode_required/) | 18.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Make product barcode required when enabled
[product_catalog_stock](product_catalog_stock/) | 18.0.1.0.1 |  | Use the product catalog on stock pickings
[product_category_active](product_category_active/) | 18.0.1.0.0 |  | Add option to archive product categories
[product_category_code](product_category_code/) | 18.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Allows to define a code on product categories
[product_category_name_translatable](product_category_name_translatable/) | 18.0.1.0.0 |  | Translate Product Category Names
[product_category_product_link](product_category_product_link/) | 18.0.1.0.0 |  | Allows to get products from a category
[product_category_tag](product_category_tag/) | 18.0.1.0.0 | <a href='https://github.com/ppyczko'><img src='https://github.com/ppyczko.png' width='32' height='32' style='border-radius:50%;' alt='ppyczko'/></a> | Add tags to product categories
[product_category_type](product_category_type/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add Type field on Product Categories to distinguish between parent and final categories
[product_category_uom](product_category_uom/) | 18.0.1.0.0 |  | Define default product UoM at product category level
[product_code_mandatory](product_code_mandatory/) | 18.0.1.0.0 |  | Set Product Internal Reference as a required field
[product_code_unique](product_code_unique/) | 18.0.1.0.0 |  | Set Product Internal Reference as Unique
[product_company_default](product_company_default/) | 18.0.1.0.0 |  | Product Company Default
[product_cost_security](product_cost_security/) | 18.0.1.1.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Product cost security restriction view
[product_cost_security_stock_account](product_cost_security_stock_account/) | 18.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Glue module between product_cost_security and stock_account
[product_customerinfo](product_customerinfo/) | 18.0.1.3.0 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Allows to define prices for customers in the products
[product_dimension](product_dimension/) | 18.0.1.0.0 |  | Product Dimension
[product_drained_weight](product_drained_weight/) | 18.0.1.0.0 |  | Add 'Drained Weight' on product models
[product_eprel](product_eprel/) | 18.0.1.0.0 |  | Manage EPREL model identifiers and energy label data for products.
[product_form_pricelist](product_form_pricelist/) | 18.0.1.0.0 |  | Show/edit pricelist in product form
[product_get_price_helper](product_get_price_helper/) | 18.0.1.1.0 |  | This module provides a helper function to compute product prices.
[product_ingredient](product_ingredient/) | 18.0.1.0.1 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Product ingredients
[product_list_price_from_pricelist](product_list_price_from_pricelist/) | 18.0.1.0.0 | <a href='https://github.com/carlos-lopez-tecnativa'><img src='https://github.com/carlos-lopez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carlos-lopez-tecnativa'/></a> | Compute product sales price from a pricelist
[product_logistics_uom](product_logistics_uom/) | 18.0.1.1.0 | <a href='https://github.com/hparfr'><img src='https://github.com/hparfr.png' width='32' height='32' style='border-radius:50%;' alt='hparfr'/></a> | Configure product weights and volume UoM
[product_lot_sequence](product_lot_sequence/) | 18.0.1.0.0 |  | Adds ability to define a lot sequence from the product
[product_main_supplierinfo](product_main_supplierinfo/) | 18.0.1.0.0 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Display the main vendor of a product.
[product_manufacturer](product_manufacturer/) | 18.0.1.0.0 |  | Adds manufacturers and attributes on the product view.
[product_medical](product_medical/) | 18.0.1.0.0 |  | Base structure to handle medical products
[product_multi_category](product_multi_category/) | 18.0.1.0.0 |  | Product - Many Categories
[product_multi_price](product_multi_price/) | 18.0.1.0.2 |  | Product Multi Price
[product_net_weight](product_net_weight/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add 'Net Weight' on product models
[product_next_reception_date](product_next_reception_date/) | 18.0.1.0.0 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> <a href='https://github.com/mathieudelva'><img src='https://github.com/mathieudelva.png' width='32' height='32' style='border-radius:50%;' alt='mathieudelva'/></a> | Add 'Next Reception date' on product models
[product_origin](product_origin/) | 18.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Adds the origin of the product
[product_packaging_archive](product_packaging_archive/) | 18.0.1.0.0 |  | Add an active field on product packaging
[product_packaging_calculator](product_packaging_calculator/) | 18.0.1.0.1 |  | Compute product quantity to pick by packaging
[product_packaging_calculator_packaging_level](product_packaging_calculator_packaging_level/) | 18.0.1.0.0 |  | Glue module for packaging level
[product_packaging_dimension](product_packaging_dimension/) | 18.0.1.0.0 |  | Manage packaging dimensions and weight
[product_packaging_level](product_packaging_level/) | 18.0.1.1.0 |  | This module binds a product packaging to a packaging level
[product_packaging_level_salable](product_packaging_level_salable/) | 18.0.1.0.1 |  | Product Packaging level salable
[product_packaging_level_vendor](product_packaging_level_vendor/) | 18.0.1.0.0 |  | Allows to mark a packaging level as vendor specific
[product_packaging_unit_price_calculator](product_packaging_unit_price_calculator/) | 18.0.1.0.0 |  | Wizard to calculate a unit price from a packaging price
[product_pricelist_alternative](product_pricelist_alternative/) | 18.0.1.0.0 |  | Calculate product price based on alternative pricelists
[product_pricelist_assortment](product_pricelist_assortment/) | 18.0.1.0.1 |  | Product assortment and pricelist
[product_pricelist_by_contact](product_pricelist_by_contact/) | 18.0.1.0.0 |  | Product Pricelist Per Contact
[product_pricelist_direct_print](product_pricelist_direct_print/) | 18.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Print price list from menu option, product templates, products variants or price lists
[product_pricelist_direct_print_company_group](product_pricelist_direct_print_company_group/) | 18.0.1.0.0 |  | Print Pricelist items using the company group model
[product_pricelist_direct_print_website_sale](product_pricelist_direct_print_website_sale/) | 18.0.1.0.1 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Extend Product Pricelist Direct Print for filter by public categories
[product_pricelist_direct_print_xlsx](product_pricelist_direct_print_xlsx/) | 18.0.1.0.2 |  | Print price list in XLSX format
[product_pricelist_discount_by_range](product_pricelist_discount_by_range/) | 18.0.1.0.0 |  | Allows to create priceslists with discount ranges
[product_pricelist_fixed_currency_rate](product_pricelist_fixed_currency_rate/) | 18.0.1.0.1 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/kobros-tech'><img src='https://github.com/kobros-tech.png' width='32' height='32' style='border-radius:50%;' alt='kobros-tech'/></a> | Set a fixed currency rate between pricelists
[product_pricelist_item_list_view](product_pricelist_item_list_view/) | 18.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | View and search the list of pricelist items
[product_pricelist_margin](product_pricelist_margin/) | 18.0.1.0.0 |  | This module shows the product's cost and margin from the pricelists.
[product_pricelist_product_price_history](product_pricelist_product_price_history/) | 18.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Track product price history within pricelists
[product_pricelist_revision](product_pricelist_revision/) | 18.0.1.0.1 |  | Product Pricelist Revision
[product_pricelist_supplierinfo](product_pricelist_supplierinfo/) | 18.0.2.0.1 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Allows to create priceslists based on supplier info
[product_print_category](product_print_category/) | 18.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Define print categories for products and automate products print, when data has changed
[product_product_template_link](product_product_template_link/) | 18.0.1.0.0 |  | Adds a button in product to view the template
[product_profile](product_profile/) | 18.0.1.0.0 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> <a href='https://github.com/kevinkhao'><img src='https://github.com/kevinkhao.png' width='32' height='32' style='border-radius:50%;' alt='kevinkhao'/></a> | Allow to configure a product in 1 click
[product_readonly_security](product_readonly_security/) | 18.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Product Readonly Security
[product_route_mto](product_route_mto/) | 18.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | This module allows to compute if a product is an 'MTO' one from its configured routes
[product_sale_description](product_sale_description/) | 18.0.1.0.0 |  | Long and short description for products
[product_sale_manufactured_for](product_sale_manufactured_for/) | 18.0.1.0.0 |  | Allows to indicate in products that they were made specifically for some customers.
[product_sale_team](product_sale_team/) | 18.0.1.0.0 |  | Sale Team for products
[product_secondary_unit](product_secondary_unit/) | 18.0.2.0.2 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Set a secondary unit per product
[product_sequence](product_sequence/) | 18.0.1.0.1 |  | Product Sequence
[product_set](product_set/) | 18.0.1.3.0 |  | Product set
[product_simple_seasonality](product_simple_seasonality/) | 18.0.1.0.0 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> <a href='https://github.com/kevinkhao'><img src='https://github.com/kevinkhao.png' width='32' height='32' style='border-radius:50%;' alt='kevinkhao'/></a> | Product seasonality
[product_state](product_state/) | 18.0.1.0.0 | <a href='https://github.com/emagdalenaC2i'><img src='https://github.com/emagdalenaC2i.png' width='32' height='32' style='border-radius:50%;' alt='emagdalenaC2i'/></a> | Module introducing a state field on product template
[product_state_sale](product_state_sale/) | 18.0.1.0.0 |  | This module add the use of Product State in Sale
[product_state_stock_base](product_state_stock_base/) | 18.0.1.0.0 |  | This module add the use of Product State in Stock
[product_status](product_status/) | 18.0.1.0.1 |  | Product Status Computed From Fields
[product_sticker](product_sticker/) | 18.0.1.0.2 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Product Sticker
[product_stock_state](product_stock_state/) | 18.0.1.0.0 | <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/kevinkhao'><img src='https://github.com/kevinkhao.png' width='32' height='32' style='border-radius:50%;' alt='kevinkhao'/></a> | Compute the state of a product's stockthe stock level and sale_ok field
[product_supplierinfo_archive](product_supplierinfo_archive/) | 18.0.1.0.0 | <a href='https://github.com/GuillemCForgeFlow'><img src='https://github.com/GuillemCForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='GuillemCForgeFlow'/></a> <a href='https://github.com/AlvaroTForgeFlow'><img src='https://github.com/AlvaroTForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='AlvaroTForgeFlow'/></a> <a href='https://github.com/OriolVForgeFlow'><img src='https://github.com/OriolVForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='OriolVForgeFlow'/></a> | Add the active field to the product supplier info
[product_supplierinfo_comment](product_supplierinfo_comment/) | 18.0.1.0.0 |  | Add the comment field to the product supplier info
[product_supplierinfo_import](product_supplierinfo_import/) | 18.0.1.1.0 |  | Import supplier pricelists
[product_supplierinfo_import_margin](product_supplierinfo_import_margin/) | 18.0.1.0.0 |  | Import supplier pricelists and margins
[product_supplierinfo_revision](product_supplierinfo_revision/) | 18.0.1.0.0 |  | Product Supplierinfo Revision
[product_supplierinfo_stock_picking_type](product_supplierinfo_stock_picking_type/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Product supplierinfo stock picking type
[product_tag_view](product_tag_view/) | 18.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Show product tags on General Information tab
[product_tags_code](product_tags_code/) | 18.0.1.0.0 |  | This addon allow to add code on products tags
[product_tier_validation](product_tier_validation/) | 18.0.1.0.0 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Support a tier validation process for Products
[product_total_weight_from_packaging](product_total_weight_from_packaging/) | 18.0.1.0.0 |  | Compute estimated weight based on product's packaging weights
[product_uom_updatable](product_uom_updatable/) | 18.0.1.0.0 |  | allows products uom to be modified after be used in a stock picking if the product uom is of the same category
[product_usability](product_usability/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Adds missing menu entries for Product module and adds extra groups to fine-tune access rights
[product_variant_route_mto](product_variant_route_mto/) | 18.0.1.0.1 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Allow to individually set variants as MTO
[purchase_product_template_tags](purchase_product_template_tags/) | 18.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Show product tags menu in Purchase app
[sale_product_template_tags](sale_product_template_tags/) | 18.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Show product tags menu in Sale app
[stock_lot_production_date](stock_lot_production_date/) | 18.0.1.0.0 | <a href='https://github.com/atchuthan'><img src='https://github.com/atchuthan.png' width='32' height='32' style='border-radius:50%;' alt='atchuthan'/></a> <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Stock Lot Production Date
[uom_alias](uom_alias/) | 18.0.1.0.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Adds alias for UOM

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/product-configurator


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/product-configurator&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/product-configurator/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/product-configurator/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/product-configurator/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/product-configurator/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/product-configurator/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/product-configurator)
[![Translation Status](https://translation.odoo-community.org/widgets/product-configurator-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/product-configurator-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# product-configurator

product-configurator

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[product_configurator](product_configurator/) | 18.0.1.0.0 | <a href='https://github.com/PCatinean'><img src='https://github.com/PCatinean.png' width='32' height='32' style='border-radius:50%;' alt='PCatinean'/></a> | Base for product configuration interface modules
[product_configurator_mrp](product_configurator_mrp/) | 18.0.1.0.0 | <a href='https://github.com/PCatinean'><img src='https://github.com/PCatinean.png' width='32' height='32' style='border-radius:50%;' alt='PCatinean'/></a> | BOM Support for configurable products
[product_configurator_sale](product_configurator_sale/) | 18.0.1.0.1 | <a href='https://github.com/PCatinean'><img src='https://github.com/PCatinean.png' width='32' height='32' style='border-radius:50%;' alt='PCatinean'/></a> | Product configuration interface modules for Sale

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/product-pack


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/product-pack&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/product-pack/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/product-pack/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/product-pack/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/product-pack/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/product-pack/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/product-pack)
[![Translation Status](https://translation.odoo-community.org/widgets/product-pack-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/product-pack-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# product-pack

product-pack

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[product_pack](product_pack/) | 18.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | This module allows you to set a product as a Pack
[purchase_product_pack](purchase_product_pack/) | 18.0.1.0.1 |  | This module allows you to buy product packs
[sale_product_pack](sale_product_pack/) | 18.0.1.0.2 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | This module allows you to sell product packs
[sale_stock_product_pack](sale_stock_product_pack/) | 18.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Compatibility module for packs that are storable products
[stock_product_pack](stock_product_pack/) | 18.0.1.0.0 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | This module allows you to get the right available quantities of the packs

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/product-variant


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/product-variant&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/product-variant/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/product-variant/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/product-variant/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/product-variant/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/product-variant/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/product-variant)
[![Translation Status](https://translation.odoo-community.org/widgets/product-variant-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/product-variant-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# product-variant

product-variant

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[product_attribute_value_archive](product_attribute_value_archive/) | 18.0.1.0.1 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Allows to archive a `product.attribute.value` referenced by archived `product.product`.
[product_variant_attribute_tax](product_variant_attribute_tax/) | 18.0.1.0.0 |  | Set taxes on the product attribute values
[product_variant_change_attribute_value](product_variant_change_attribute_value/) | 18.0.1.0.0 |  | Product Variant Change Attribute Value
[product_variant_configurator](product_variant_configurator/) | 18.0.1.0.0 |  | Provides an abstract model for product variant configuration.
[product_variant_configurator_manual_creation](product_variant_configurator_manual_creation/) | 18.0.1.0.0 | <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | Provides a wizards to make variants on demand
[product_variant_default_code](product_variant_default_code/) | 18.0.1.0.0 | <a href='https://github.com/Kev-Roche'><img src='https://github.com/Kev-Roche.png' width='32' height='32' style='border-radius:50%;' alt='Kev-Roche'/></a> | Allow to automatically generate the variant default code
[product_variant_name](product_variant_name/) | 18.0.1.0.0 |  | Product Variant Name
[product_variant_sale_price](product_variant_sale_price/) | 18.0.1.0.1 |  | Allows to write fixed prices in product variants
[product_variant_specific_description](product_variant_specific_description/) | 18.0.1.0.0 |  | Product Variant Specific Description
[sale_order_line_variant_description](sale_order_line_variant_description/) | 18.0.1.0.0 |  | Sale order line variant description
[sale_variant_configurator](sale_variant_configurator/) | 18.0.1.0.3 |  | Product variants in sale management

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/project


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/project&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/project/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/project/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/project/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/project/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/project/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/project)
[![Translation Status](https://translation.odoo-community.org/widgets/project-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/project-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# project

project

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[project_administrator_restricted_visibility](project_administrator_restricted_visibility/) | 18.0.1.0.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | Adds a 'Project Administrator' access group with restricted visibility to 'Projects'
[project_budget](project_budget/) | 18.0.1.0.0 | <a href='https://github.com/patrickrwilson'><img src='https://github.com/patrickrwilson.png' width='32' height='32' style='border-radius:50%;' alt='patrickrwilson'/></a> | Adds budget management to projects.
[project_department](project_department/) | 18.0.1.0.0 |  | Project Department Categorization
[project_forecast_line](project_forecast_line/) | 18.0.1.0.0 |  | Project Forecast Lines
[project_group](project_group/) | 18.0.1.0.0 |  | Add groups for filtering on projects
[project_group_hr_timesheet](project_group_hr_timesheet/) | 18.0.1.0.0 |  | This module makes project group work properly with timesheets
[project_hr](project_hr/) | 18.0.1.0.2 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Link HR with project
[project_kanban_form_direct_access](project_kanban_form_direct_access/) | 18.0.1.0.0 |  | Project form view can now be accessed directly by clicking the project name.
[project_key](project_key/) | 18.0.1.0.1 |  | Module decorates projects and tasks with Project Key
[project_merge](project_merge/) | 18.0.1.0.0 |  | Wizard to merge project tasks
[project_milestone_status](project_milestone_status/) | 18.0.1.0.0 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | Project Milestone Status
[project_parent](project_parent/) | 18.0.1.0.1 |  | Project Parent
[project_parent_task_filter](project_parent_task_filter/) | 18.0.1.0.0 |  | Add a filter to show the parent tasks
[project_pivot](project_pivot/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Pivot view for projects
[project_portal_task_visibility](project_portal_task_visibility/) | 18.0.1.0.0 |  | Project Portal Task Visibility
[project_purchase_link](project_purchase_link/) | 18.0.1.0.0 |  | Project Purchase Link
[project_reviewer](project_reviewer/) | 18.0.1.0.0 |  | Add the possibility to assign reviewer to a task
[project_role](project_role/) | 18.0.1.0.1 | <a href='https://github.com/alexey-pelykh'><img src='https://github.com/alexey-pelykh.png' width='32' height='32' style='border-radius:50%;' alt='alexey-pelykh'/></a> | Project role-based roster
[project_sequence](project_sequence/) | 18.0.1.1.0 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/anddago78'><img src='https://github.com/anddago78.png' width='32' height='32' style='border-radius:50%;' alt='anddago78'/></a> | Add a sequence field to projects, filled automatically
[project_stage_extra_info](project_stage_extra_info/) | 18.0.1.0.0 |  | Project Stage Extra Info
[project_stage_last_update_date](project_stage_last_update_date/) | 18.0.1.0.0 |  | Project Stage Last Update Date
[project_stakeholder](project_stakeholder/) | 18.0.1.0.0 |  | Manage project stakeholders and their roles
[project_status](project_status/) | 18.0.1.0.0 | <a href='https://github.com/patrickrwilson'><img src='https://github.com/patrickrwilson.png' width='32' height='32' style='border-radius:50%;' alt='patrickrwilson'/></a> | Project Status
[project_tag_hierarchy](project_tag_hierarchy/) | 18.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Project Tag Hierarchy
[project_tag_multicompany](project_tag_multicompany/) | 18.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Project Tag Multicompany
[project_tag_security](project_tag_security/) | 18.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Project Tag Security
[project_task_add_very_high](project_task_add_very_high/) | 18.0.1.1.0 | <a href='https://github.com/astirpe'><img src='https://github.com/astirpe.png' width='32' height='32' style='border-radius:50%;' alt='astirpe'/></a> | Adds extra options 'High' and 'Very High' on tasks
[project_task_ancestor](project_task_ancestor/) | 18.0.1.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> | Project Task Ancestor
[project_task_code](project_task_code/) | 18.0.1.0.1 |  | Sequential Code for Tasks
[project_task_code_portal](project_task_code_portal/) | 18.0.1.1.1 |  | Use custom task code in customer portal
[project_task_default_stage](project_task_default_stage/) | 18.0.1.0.1 |  | Recovery default task stages for projects from v8
[project_task_default_user](project_task_default_user/) | 18.0.1.0.0 | <a href='https://github.com/NICO-SOLUTIONS'><img src='https://github.com/NICO-SOLUTIONS.png' width='32' height='32' style='border-radius:50%;' alt='NICO-SOLUTIONS'/></a> | Auto assign default users to tasks or when changing task stages
[project_task_description_portal](project_task_description_portal/) | 18.0.1.0.0 |  | Dedicated task description for portal users
[project_task_description_template](project_task_description_template/) | 18.0.1.0.0 |  | Add a description template to project tasks
[project_task_material](project_task_material/) | 18.0.1.0.0 |  | Record products spent in a Task
[project_task_name_with_id](project_task_name_with_id/) | 18.0.1.0.0 |  | Project Task Name with ID
[project_task_note](project_task_note/) | 18.0.1.0.2 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Add notes in project tasks
[project_task_parent_completion_blocking](project_task_parent_completion_blocking/) | 18.0.1.0.0 | <a href='https://github.com/david-banon-tecnativa'><img src='https://github.com/david-banon-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='david-banon-tecnativa'/></a> | Prevents a task from being completed if any children task isn't.
[project_task_parent_due_auto](project_task_parent_due_auto/) | 18.0.1.0.1 | <a href='https://github.com/david-banon-tecnativa'><img src='https://github.com/david-banon-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='david-banon-tecnativa'/></a> | Recalculates parent task's due date when child task changes
[project_task_personal_stage_auto_fold](project_task_personal_stage_auto_fold/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Moves task to the first fold personal stage when done
[project_task_pull_request](project_task_pull_request/) | 18.0.1.1.0 |  | Adds a field for a PR URI to project tasks
[project_task_pull_request_state](project_task_pull_request_state/) | 18.0.1.0.0 |  | Track Pull Request state in tasks
[project_task_related](project_task_related/) | 18.0.1.0.0 | <a href='https://github.com/david-banon-tecnativa'><img src='https://github.com/david-banon-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='david-banon-tecnativa'/></a> | Project Related Task
[project_task_stage_auto_state](project_task_stage_auto_state/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Auto-change task state (done/canceled) after N days on selected stages
[project_task_stage_change_restriction](project_task_stage_change_restriction/) | 18.0.1.0.0 |  | Restrict project task stage
[project_task_stage_lock](project_task_stage_lock/) | 18.0.1.0.0 | <a href='https://github.com/DavidJForgeFlow'><img src='https://github.com/DavidJForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='DavidJForgeFlow'/></a> | Locks the Stages in the Kanban view of the project task to avoid modification of the stages in other projects. Also removes the default group by in the stages list view to be able to see the stages order.
[project_task_stage_mgmt](project_task_stage_mgmt/) | 18.0.1.0.0 | <a href='https://github.com/DavidJForgeFlow'><img src='https://github.com/DavidJForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='DavidJForgeFlow'/></a> | Allows to assign and create task stages on project creation wizard
[project_task_stage_state](project_task_stage_state/) | 18.0.1.0.0 |  | Restore State attribute removed from Project Stages in 8.0
[project_task_stock](project_task_stock/) | 18.0.1.1.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Project Task Stock
[project_task_stock_product_set](project_task_stock_product_set/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Project Task Stock Product Set
[project_task_tag](project_task_tag/) | 18.0.1.0.0 |  | Limit tags available on task
[project_template](project_template/) | 18.0.1.0.1 | <a href='https://github.com/patrickrwilson'><img src='https://github.com/patrickrwilson.png' width='32' height='32' style='border-radius:50%;' alt='patrickrwilson'/></a> | Project Templates
[project_timeline](project_timeline/) | 18.0.1.0.0 |  | Timeline view for projects
[project_timeline_hr_timesheet](project_timeline_hr_timesheet/) | 18.0.1.0.0 |  | Shows the progress of tasks on the timeline view.
[project_timesheet_time_control](project_timesheet_time_control/) | 18.0.1.0.7 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Project timesheet time control
[project_type](project_type/) | 18.0.1.0.0 |  | Project Types
[project_update_portal](project_update_portal/) | 18.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Allows portal access for project and update followers
[project_version](project_version/) | 18.0.1.0.0 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | Project Version
[sale_project_copy_tasks](sale_project_copy_tasks/) | 18.0.1.0.0 | <a href='https://github.com/shide'><img src='https://github.com/shide.png' width='32' height='32' style='border-radius:50%;' alt='shide'/></a> <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Copy tasks into sale order's project
[sale_project_reimbursement_cost](sale_project_reimbursement_cost/) | 18.0.1.0.0 |  | Display provisions and reimbursement costs in the Project Updates dashboard.
[sale_project_task_recurrency](sale_project_task_recurrency/) | 18.0.1.0.0 |  | Configuring Task Recurrence from the Product Form.
[sale_project_task_selection](sale_project_task_selection/) | 18.0.1.0.1 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Manually select the Task or Project for a Sale Order Line

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/purchase-reporting


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/purchase-reporting&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/purchase-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/purchase-reporting/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/purchase-reporting/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/purchase-reporting/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/purchase-reporting/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/purchase-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/purchase-reporting-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/purchase-reporting-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# purchase-reporting

purchase-reporting

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[purchase_comment_template](purchase_comment_template/) | 18.0.1.0.2 |  | Comments texts templates on Purchase documents
[purchase_order_report_hide_tax](purchase_order_report_hide_tax/) | 18.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Hide taxes column when they don't add value
[purchase_packaging_report](purchase_packaging_report/) | 18.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Packaging data in purchase reports
[purchase_report_date_format](purchase_report_date_format/) | 18.0.1.0.0 |  | Purchase Report Date Format
[purchase_report_shipping_address](purchase_report_shipping_address/) | 18.0.1.0.0 |  | Purchase Report Shipping Address

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/purchase-workflow

[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# purchase-workflow
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/purchase-workflow&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/purchase-workflow/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/purchase-workflow/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/purchase-workflow/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/purchase-workflow/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/purchase-workflow/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/purchase-workflow)
[![Translation Status](https://translation.odoo-community.org/widgets/purchase-workflow-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/purchase-workflow-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

purchase-workflow

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[partner_supplierinfo_smartbutton](partner_supplierinfo_smartbutton/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Access supplied products from the vendor
[procurement_purchase_no_grouping](procurement_purchase_no_grouping/) | 18.0.1.0.1 |  | Procurement Purchase No Grouping
[procurement_purchase_sale_no_grouping](procurement_purchase_sale_no_grouping/) | 18.0.1.0.0 |  | Procurement Purchase Service No Grouping
[product_main_seller](product_main_seller/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Main Vendor for a product
[product_supplier_code_purchase](product_supplier_code_purchase/) | 18.0.1.0.0 |  | This module adds to the purchase order line the supplier code defined in the product.
[product_supplierinfo_disable_autocreation](product_supplierinfo_disable_autocreation/) | 18.0.1.0.0 |  | Add option to disable automatic creation of pricelists for suppliers
[product_supplierinfo_purchase_contact](product_supplierinfo_purchase_contact/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Add Purchase Contact in product supplier info
[product_supplierinfo_qty_multiplier](product_supplierinfo_qty_multiplier/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Product supplierinfo qty multiplier
[product_supplierinfo_update_price](product_supplierinfo_update_price/) | 18.0.1.0.0 |  | Updates the product's vendor price with the price set in a purchase order.
[purchase_advance_payment](purchase_advance_payment/) | 18.0.1.2.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Allow to add advance payments on purchase orders
[purchase_all_shipments](purchase_all_shipments/) | 18.0.1.0.1 |  | Purchase All Shipments
[purchase_allowed_product](purchase_allowed_product/) | 18.0.1.0.1 |  | This module allows to select only products that can be supplied by the vendor
[purchase_analytic_global](purchase_analytic_global/) | 18.0.1.0.0 |  | Purchase - Analytic Account Global
[purchase_blanket_order](purchase_blanket_order/) | 18.0.1.0.1 |  | Purchase Blanket Orders
[purchase_cancel_reason](purchase_cancel_reason/) | 18.0.1.0.0 |  | Purchase Cancel Reason
[purchase_commercial_partner](purchase_commercial_partner/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add stored related field 'Commercial Supplier' on POs
[purchase_container](purchase_container/) | 18.0.1.1.0 | <a href='https://github.com/nayatec'><img src='https://github.com/nayatec.png' width='32' height='32' style='border-radius:50%;' alt='nayatec'/></a> | Add containers to purchase orders and stock pickings.
[purchase_default_terms_conditions](purchase_default_terms_conditions/) | 18.0.1.0.0 |  | This module allows purchase default terms & conditions
[purchase_delivery_split_date](purchase_delivery_split_date/) | 18.0.2.0.3 |  | Allows Purchase Order you confirm to generate one Incoming Shipment for each expected date indicated in the Purchase Order Lines
[purchase_deposit](purchase_deposit/) | 18.0.1.0.1 |  | Option to create deposit from purchase order
[purchase_exception](purchase_exception/) | 18.0.1.0.1 |  | Custom exceptions on purchase order
[purchase_fop_shipping](purchase_fop_shipping/) | 18.0.1.0.1 |  | Purchase Free-Of-Payment shipping
[purchase_force_invoiced](purchase_force_invoiced/) | 18.0.1.0.2 |  | Allows to force the billing status of the purchase order to "Invoiced"
[purchase_force_invoiced_quantity](purchase_force_invoiced_quantity/) | 18.0.1.1.1 |  | Add manual invoice quantity in purchase order lines
[purchase_invoice_method](purchase_invoice_method/) | 18.0.1.0.0 |  | Allow to force the invoice method of a purchase
[purchase_invoice_plan](purchase_invoice_plan/) | 18.0.1.0.2 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Add to purchases order, ability to manage future invoice plan
[purchase_invoice_status_line](purchase_invoice_status_line/) | 18.0.2.0.0 | <a href='https://github.com/JoanSForgeFlow'><img src='https://github.com/JoanSForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JoanSForgeFlow'/></a> | Add invoice status on purchase order lines
[purchase_last_price_info](purchase_last_price_info/) | 18.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Purchase Product Last Price Info
[purchase_line_procurement_group](purchase_line_procurement_group/) | 18.0.1.0.0 |  | Group purchase order line according to procurement group
[purchase_line_reassign](purchase_line_reassign/) | 18.0.1.0.0 |  | Purchase Line Reassign
[purchase_location_by_line](purchase_location_by_line/) | 18.0.1.0.1 |  | Allows to define a specific destination location on each PO line
[purchase_lot](purchase_lot/) | 18.0.1.0.1 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Purchase Lot
[purchase_manual_currency](purchase_manual_currency/) | 18.0.1.0.0 |  | Allows to manual currency of Purchase
[purchase_manual_delivery](purchase_manual_delivery/) | 18.0.1.0.0 |  | Prevents pickings to be auto generated upon Purchase Order confirmation and adds the ability to manually generate them as the supplier confirms the different purchase order lines.
[purchase_no_rfq](purchase_no_rfq/) | 18.0.1.0.2 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Purchase Order - No Request For Quotation
[purchase_open_qty](purchase_open_qty/) | 18.0.1.0.1 |  | Allows to identify the purchase orders that have quantities pending to invoice or to receive.
[purchase_order_approval_block](purchase_order_approval_block/) | 18.0.1.0.0 |  | Purchase Order Approval Block
[purchase_order_approved](purchase_order_approved/) | 18.0.1.0.2 |  | Add a new state 'Approved' in purchase orders.
[purchase_order_archive](purchase_order_archive/) | 18.0.1.0.0 |  | Archive Purchase Orders
[purchase_order_date_approve_editable](purchase_order_date_approve_editable/) | 18.0.1.0.0 |  | Allows editing the Approval Date on Purchase Orders
[purchase_order_etd_eta](purchase_order_etd_eta/) | 18.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Add Estimated Time of Departure/Arrival fields to Purchase Orders
[purchase_order_general_discount](purchase_order_general_discount/) | 18.0.1.0.0 |  | General discount per purchase order
[purchase_order_internal_note](purchase_order_internal_note/) | 18.0.1.0.0 |  | Adds new field Internal Note to the purchase order. It will not be included in the report.
[purchase_order_line_description](purchase_order_line_description/) | 18.0.1.0.0 |  | Purchase order line description
[purchase_order_line_effective_date](purchase_order_line_effective_date/) | 18.0.0.1.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Calculated effective dates in Purchase Order Lines
[purchase_order_line_menu](purchase_order_line_menu/) | 18.0.1.0.2 |  | Adds Purchase Order Lines Menu
[purchase_order_line_note](purchase_order_line_note/) | 18.0.1.0.0 | <a href='https://github.com/Kev-Roche'><img src='https://github.com/Kev-Roche.png' width='32' height='32' style='border-radius:50%;' alt='Kev-Roche'/></a> | Note on purchase order line
[purchase_order_line_original_date](purchase_order_line_original_date/) | 18.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | adds the Original Expected Arrival to PO lines.
[purchase_order_line_sequence](purchase_order_line_sequence/) | 18.0.2.0.0 |  | Adds sequence to PO lines and propagates it to Invoice lines
[purchase_order_line_stock_available](purchase_order_line_stock_available/) | 18.0.1.0.0 |  | Purchase order line stock available
[purchase_order_owner](purchase_order_owner/) | 18.0.1.0.0 |  | Purchase Order Owner
[purchase_order_price_recalculation](purchase_order_price_recalculation/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Price recalculation in purchases orders
[purchase_order_product_recommendation](purchase_order_product_recommendation/) | 18.0.1.1.0 |  | Recommend products to buy to supplier based on history
[purchase_order_product_recommendation_brand](purchase_order_product_recommendation_brand/) | 18.0.1.0.0 |  | Allow to filter recommendations by brand
[purchase_order_product_recommendation_secondary_unit](purchase_order_product_recommendation_secondary_unit/) | 18.0.1.0.0 |  | Add secondary unit to recommend products wizard
[purchase_order_product_recommendation_xlsx](purchase_order_product_recommendation_xlsx/) | 18.0.1.0.0 |  | Add a way to print recommended products for supplier
[purchase_order_qty_change_no_recompute](purchase_order_qty_change_no_recompute/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Prevent recompute if only quantity has changed in purchase order line
[purchase_order_secondary_unit](purchase_order_secondary_unit/) | 18.0.1.2.2 |  | Purchase product in a secondary unit
[purchase_order_supplier_return](purchase_order_supplier_return/) | 18.0.1.0.0 |  | Return product to supplier and update quantiy received
[purchase_order_supplierinfo_update](purchase_order_supplierinfo_update/) | 18.0.2.0.0 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | Update product supplierinfo with the last purchase price
[purchase_order_type](purchase_order_type/) | 18.0.1.1.2 |  | Purchase Order Type
[purchase_order_type_dashboard](purchase_order_type_dashboard/) | 18.0.1.0.0 | <a href='https://github.com/dalonsod'><img src='https://github.com/dalonsod.png' width='32' height='32' style='border-radius:50%;' alt='dalonsod'/></a> | Purchase Order Type Dashboard
[purchase_order_uninvoiced_amount](purchase_order_uninvoiced_amount/) | 18.0.1.0.0 |  | Purchase Order Univoiced Amount
[purchase_order_uninvoiced_amount_line](purchase_order_uninvoiced_amount_line/) | 18.0.1.0.0 |  | Purchase Order Line Uninvoiced Amount
[purchase_partner_incoterm](purchase_partner_incoterm/) | 18.0.1.0.1 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Add a an incoterm field for supplier and use it on purchase order
[purchase_partner_selectable_option](purchase_partner_selectable_option/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Purchase Partner Selectable Option
[purchase_receipt_expectation](purchase_receipt_expectation/) | 18.0.1.0.1 |  | Purchase Receipt Expectation
[purchase_reception_notify](purchase_reception_notify/) | 18.0.1.0.1 |  | Purchase Reception Notify
[purchase_reception_status](purchase_reception_status/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add reception status on purchase orders (OCA logic)
[purchase_reception_status_line](purchase_reception_status_line/) | 18.0.1.1.0 | <a href='https://github.com/DavidJForgeFlow'><img src='https://github.com/DavidJForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='DavidJForgeFlow'/></a> | Add reception status on purchase order lines
[purchase_representative](purchase_representative/) | 18.0.1.0.0 |  | Purchase Representatives will be the point of contact for RFQ's and PO's
[purchase_request](purchase_request/) | 18.0.2.5.0 |  | Use this module to have notification of requirements of materials and/or external services and keep track of such requirements.
[purchase_request_cancel_confirm](purchase_request_cancel_confirm/) | 18.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Purchase Request Cancel Confirm
[purchase_request_department](purchase_request_department/) | 18.0.1.0.0 |  | Purchase Request Department
[purchase_request_exception](purchase_request_exception/) | 18.0.1.0.0 |  | Custom exceptions on purchase request
[purchase_request_substate](purchase_request_substate/) | 18.0.1.0.0 |  | Purchase Request Sub State
[purchase_request_tier_validation](purchase_request_tier_validation/) | 18.0.1.1.1 |  | Extends the functionality of Purchase Requests to support a tier validation process.
[purchase_request_to_requisition](purchase_request_to_requisition/) | 18.0.1.0.0 |  | Purchase Request to Purchase Agreement
[purchase_request_type](purchase_request_type/) | 18.0.1.0.1 |  | Purchase Request Type
[purchase_requisition_line_description](purchase_requisition_line_description/) | 18.0.1.0.0 |  | Extends the functionality of Purchase Agreements to show line description.
[purchase_sale_link_by_origin](purchase_sale_link_by_origin/) | 18.0.1.0.0 |  | Link PO/SO by the PO's Origin in addition to the default behavior that only links them by their lines
[purchase_security](purchase_security/) | 18.0.1.1.2 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | See only your purchase orders
[purchase_stock_cost_update](purchase_stock_cost_update/) | 18.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Allows to update valuation layers once the purchase is received
[purchase_stock_line_sequence](purchase_stock_line_sequence/) | 18.0.2.0.0 |  | Propagates the purchase order line sequence to stock moves
[purchase_stock_manual_currency](purchase_stock_manual_currency/) | 18.0.1.0.0 |  | Extends manual currency from purchase to stock moves
[purchase_stock_packaging](purchase_stock_packaging/) | 18.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Allows to transmit the product packaging from the procurement values to the generated purchase order line
[purchase_stock_price_unit_sync](purchase_stock_price_unit_sync/) | 18.0.1.0.0 |  | Update cost price in stock moves already done
[purchase_stock_reception_status](purchase_stock_reception_status/) | 18.0.1.0.0 |  | Glue module to integrate OCA reception status with purchase_stock
[purchase_stock_secondary_unit](purchase_stock_secondary_unit/) | 18.0.1.0.0 |  | Get product quantities in a secondary unit
[purchase_substate](purchase_substate/) | 18.0.1.0.0 |  | Purchase Sub State
[purchase_tag](purchase_tag/) | 18.0.1.1.0 |  | Allows to add multiple tags to purchase orders
[purchase_tier_validation](purchase_tier_validation/) | 18.0.1.0.0 |  | Extends the functionality of Purchase Orders to support a tier validation process.
[purchase_triple_discount](purchase_triple_discount/) | 18.0.1.0.0 |  | Manage triple discount on purchase order lines
[purchase_uninvoiced_amount_force_invoiced_line](purchase_uninvoiced_amount_force_invoiced_line/) | 18.0.1.0.0 | <a href='https://github.com/JoanSForgeFlow'><img src='https://github.com/JoanSForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JoanSForgeFlow'/></a> | Glue module between uninvoiced amount line and force invoiced line
[purchase_warn_message](purchase_warn_message/) | 18.0.1.0.0 |  | Add a popup warning on purchase to ensure warning is populated
[purchase_warn_option](purchase_warn_option/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Add Options to Purchase Warn Messages
[purchase_work_acceptance](purchase_work_acceptance/) | 18.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Purchase Work Acceptance
[purchase_work_acceptance_invoice_plan](purchase_work_acceptance_invoice_plan/) | 18.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Purchase Work Acceptance Invoice Plan
[sale_purchase_force_vendor](sale_purchase_force_vendor/) | 18.0.1.0.2 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Sale Purchase Force Vendor
[stock_move_purchase_price_update](stock_move_purchase_price_update/) | 18.0.1.0.0 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> | Allow update purchase price from incoming picking operations
[supplier_calendar](supplier_calendar/) | 18.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Supplier Calendar
[vendor_transport_lead_time](vendor_transport_lead_time/) | 18.0.1.0.1 |  | Purchase delay based on transport and supplier delays

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/queue


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/queue&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/queue/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/queue/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/queue/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/queue/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/queue/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/queue)
[![Translation Status](https://translation.odoo-community.org/widgets/queue-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/queue-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# queue

queue

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_import_async](base_import_async/) | 18.0.1.0.0 |  | Import CSV files in the background
[queue_job](queue_job/) | 18.0.3.1.1 | <a href='https://github.com/guewen'><img src='https://github.com/guewen.png' width='32' height='32' style='border-radius:50%;' alt='guewen'/></a> <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Job Queue
[queue_job_batch](queue_job_batch/) | 18.0.1.0.0 |  | Job Queue Batch
[queue_job_cron](queue_job_cron/) | 18.0.1.1.1 |  | Scheduled Actions as Queue Jobs
[queue_job_cron_jobrunner](queue_job_cron_jobrunner/) | 18.0.1.0.1 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Run jobs without a dedicated JobRunner
[queue_job_profiler](queue_job_profiler/) | 18.0.1.0.1 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Job Queue Profiler
[queue_job_subscribe](queue_job_subscribe/) | 18.0.1.0.0 |  | Control which users are subscribed to queue job notifications
[test_queue_job](test_queue_job/) | 18.0.2.0.5 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Queue Job Tests
[test_queue_job_batch](test_queue_job_batch/) | 18.0.1.0.0 |  | Test Job Queue Batch

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/repair


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/repair&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/repair/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/repair/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/repair/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/repair/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/repair/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/repair)
[![Translation Status](https://translation.odoo-community.org/widgets/repair-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/repair-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# repair

repair

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_repair_config](base_repair_config/) | 18.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Provides general settings for the Repair App
[partner_repair_button](partner_repair_button/) | 18.0.1.0.0 | <a href='https://github.com/AaronHForgeFlow'><img src='https://github.com/AaronHForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='AaronHForgeFlow'/></a> | Partner Repair Smart Button
[repair_order_group](repair_order_group/) | 18.0.1.0.1 |  | Group several repair orders and keep them in sync
[repair_order_group_services](repair_order_group_services/) | 18.0.1.0.0 |  | Support for services in grouped repair orders
[repair_order_line_sequence](repair_order_line_sequence/) | 18.0.1.0.0 |  | Allow to change line order in repairs
[repair_order_product_by_lot](repair_order_product_by_lot/) | 18.0.1.0.0 |  | Select product in repair order by the lot number
[repair_order_template](repair_order_template/) | 18.0.1.0.1 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Use templates to save time when creating repair orders
[repair_picking_after_done](repair_picking_after_done/) | 18.0.1.0.0 |  | Transfer repaired move to another location directly from repair order
[repair_quality_control](repair_quality_control/) | 18.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Create quality controls from repair order
[repair_scheduled_date_calendar_view](repair_scheduled_date_calendar_view/) | 18.0.1.0.0 |  | Repair order calendar view based on scheduled data
[repair_service](repair_service/) | 18.0.1.2.3 |  | Adds services to repair orders, so that they can be added as sale order lines.
[repair_stock](repair_stock/) | 18.0.1.0.0 |  | Repair Stock
[repair_timesheet](repair_timesheet/) | 18.0.1.0.0 | <a href='https://github.com/ppyczko'><img src='https://github.com/ppyczko.png' width='32' height='32' style='border-radius:50%;' alt='ppyczko'/></a> | Repair Timesheet
[repair_type](repair_type/) | 18.0.1.0.1 |  | Repair type
[repair_type_product_destination](repair_type_product_destination/) | 18.0.1.0.0 | <a href='https://github.com/ppyczko'><img src='https://github.com/ppyczko.png' width='32' height='32' style='border-radius:50%;' alt='ppyczko'/></a> | Repair Type - Product Destination

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/report-print-send


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/report-print-send&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/report-print-send/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/report-print-send/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/report-print-send/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/report-print-send/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/report-print-send/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/report-print-send)
[![Translation Status](https://translation.odoo-community.org/widgets/report-print-send-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/report-print-send-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# report-print-send

report-print-send

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_report_to_label_printer](base_report_to_label_printer/) | 18.0.1.1.0 |  | Report to label printer
[base_report_to_printer](base_report_to_printer/) | 18.0.1.3.0 |  | Report to printer
[base_report_to_printer_mail](base_report_to_printer_mail/) | 18.0.1.0.0 |  | Report to printer - Mail extension
[printer_zpl2](printer_zpl2/) | 18.0.1.0.2 |  | Add a ZPL II label printing feature
[printing_auto_base](printing_auto_base/) | 18.0.1.3.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Printing Auto Base
[printing_auto_label_printer](printing_auto_label_printer/) | 18.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Printing Auto Label Printer
[server_env_printing_server](server_env_printing_server/) | 18.0.1.0.0 |  | Server Environment for Printing Server

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/reporting-engine


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# reporting-engine
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/reporting-engine&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/reporting-engine/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/reporting-engine/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/reporting-engine/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/reporting-engine/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/reporting-engine/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/reporting-engine)
[![Translation Status](https://translation.odoo-community.org/widgets/reporting-engine-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/reporting-engine-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

reporting-engine

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_comment_template](base_comment_template/) | 18.0.1.1.2 |  | Add conditional mako template to any reporton models that inherits comment.template.
[bi_sql_editor](bi_sql_editor/) | 18.0.1.0.4 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | BI Views builder, based on Materialized or Normal SQL Views
[pdf_xml_attachment](pdf_xml_attachment/) | 18.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Provides helpers to work w/ PDFs and XML attachments
[report_context](report_context/) | 18.0.1.0.0 |  | Adding context to reports
[report_csv](report_csv/) | 18.0.1.0.2 |  | Base module to create csv report
[report_display_name_in_footer](report_display_name_in_footer/) | 18.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Show document name in report footer
[report_footer_html](report_footer_html/) | 18.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Show HTML content in desired Footer Reports
[report_label](report_label/) | 18.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Print configurable self-adhesive labels reports
[report_layout_config](report_layout_config/) | 18.0.1.0.0 |  | Add possibility to easily modify the global report layout
[report_partner_address](report_partner_address/) | 18.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Translatable partner address details for reports and portal
[report_pdf_form](report_pdf_form/) | 18.0.1.0.0 | <a href='https://github.com/grindtildeath'><img src='https://github.com/grindtildeath.png' width='32' height='32' style='border-radius:50%;' alt='grindtildeath'/></a> | Fill custom PDF form reports
[report_pdf_zip_download](report_pdf_zip_download/) | 18.0.1.0.0 |  | Report PDF ZIP Download
[report_positioned_image](report_positioned_image/) | 18.0.1.0.0 |  | Add positioned images to PDF reports.
[report_py3o](report_py3o/) | 18.0.1.0.3 |  | Reporting engine based on Libreoffice (ODT -> ODT, ODT -> PDF, ODT -> DOC, ODT -> DOCX, ODS -> ODS, etc.)
[report_py3o_fusion_server](report_py3o_fusion_server/) | 18.0.1.0.0 |  | Let the fusion server handle format conversion.
[report_qr](report_qr/) | 18.0.1.0.0 |  | Web QR Manager
[report_qweb_element_page_visibility](report_qweb_element_page_visibility/) | 18.0.1.0.0 |  | Report Qweb Element Page Visibility
[report_qweb_encrypt](report_qweb_encrypt/) | 18.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Allow to encrypt qweb pdfs
[report_qweb_field_option](report_qweb_field_option/) | 18.0.1.1.0 |  | Report Qweb Field Option
[report_qweb_parameter](report_qweb_parameter/) | 18.0.1.0.0 |  | Add new parameters for qweb templates in order to reduce field length and check minimal length
[report_qweb_pdf_cover](report_qweb_pdf_cover/) | 18.0.1.0.0 |  | Add front and back covers to your QWeb PDF reports
[report_qweb_pdf_watermark](report_qweb_pdf_watermark/) | 18.0.1.1.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Add watermarks to your QWEB PDF reports
[report_substitute](report_substitute/) | 18.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This module allows to create substitution rules for report actions.
[report_text_format_option](report_text_format_option/) | 18.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Report Text Format Option
[report_wkhtmltopdf_param](report_wkhtmltopdf_param/) | 18.0.1.0.1 |  | Add new parameters for a paper format to be used by wkhtmltopdf command as arguments.
[report_xlsx](report_xlsx/) | 18.0.1.1.3 |  | Base module to create xlsx report
[report_xlsx_helper](report_xlsx_helper/) | 18.0.1.0.0 |  | Report xlsx helpers
[report_xml](report_xml/) | 18.0.1.1.1 |  | Allow to generate XML reports
[sql_export](sql_export/) | 18.0.1.1.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Export data in csv file with SQL requests
[sql_export_delta](sql_export_delta/) | 18.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Support exporting only the changes from last export
[sql_export_excel](sql_export_excel/) | 18.0.1.0.1 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Allow to export a sql query to an excel file.
[sql_export_mail](sql_export_mail/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Send csv file generated by sql query by mail.
[sql_request_abstract](sql_request_abstract/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Abstract Model to manage SQL Requests

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/rest-framework


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/rest-framework&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/rest-framework/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/rest-framework/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/rest-framework/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/rest-framework/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/rest-framework/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/rest-framework)
[![Translation Status](https://translation.odoo-community.org/widgets/rest-framework-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/rest-framework-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# rest-framework

rest-framework

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[api_log](api_log/) | 18.0.1.0.0 | <a href='https://github.com/paradoxxxzero'><img src='https://github.com/paradoxxxzero.png' width='32' height='32' style='border-radius:50%;' alt='paradoxxxzero'/></a> | Log API requests in database
[api_log_mail](api_log_mail/) | 18.0.1.0.0 | <a href='https://github.com/SirPyTech'><img src='https://github.com/SirPyTech.png' width='32' height='32' style='border-radius:50%;' alt='SirPyTech'/></a> | Notify logged exceptions.
[auth_partner](auth_partner/) | 18.0.1.0.0 | <a href='https://github.com/paradoxxxzero'><img src='https://github.com/paradoxxxzero.png' width='32' height='32' style='border-radius:50%;' alt='paradoxxxzero'/></a> | Implements the base features for a authenticable partner
[base_rest](base_rest/) | 18.0.1.1.2 |  | Develop your own high level REST APIs for Odoo thanks to this addon.
[base_rest_auth_api_key](base_rest_auth_api_key/) | 18.0.1.1.1 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Base Rest: Add support for the auth_api_key security policy into the openapi documentation
[base_rest_pydantic](base_rest_pydantic/) | 18.0.1.0.2 |  | Pydantic binding for base_rest
[extendable](extendable/) | 18.0.1.0.2 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Extendable classes registry loader for Odoo
[extendable_fastapi](extendable_fastapi/) | 18.0.1.0.1 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Allows the use of extendable into fastapi apps
[fastapi](fastapi/) | 18.0.1.3.4 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Odoo FastAPI endpoint
[fastapi_auth_api_key](fastapi_auth_api_key/) | 18.0.1.0.0 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Fastapi Auth API Key
[fastapi_auth_jwt](fastapi_auth_jwt/) | 18.0.1.0.0 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | JWT bearer token authentication for FastAPI.
[fastapi_auth_partner](fastapi_auth_partner/) | 18.0.1.0.0 |  | This provides an implementation of auth_partner for FastAPI
[fastapi_captcha](fastapi_captcha/) | 18.0.1.0.0 | <a href='https://github.com/paradoxxxzero'><img src='https://github.com/paradoxxxzero.png' width='32' height='32' style='border-radius:50%;' alt='paradoxxxzero'/></a> | Add a captcha to your FastAPI routes
[fastapi_captcha_altcha_backend](fastapi_captcha_altcha_backend/) | 18.0.1.0.0 | <a href='https://github.com/paradoxxxzero'><img src='https://github.com/paradoxxxzero.png' width='32' height='32' style='border-radius:50%;' alt='paradoxxxzero'/></a> | Implement Altcha server in FastAPI
[fastapi_endpoint_context](fastapi_endpoint_context/) | 18.0.1.0.0 | <a href='https://github.com/paradoxxxzero'><img src='https://github.com/paradoxxxzero.png' width='32' height='32' style='border-radius:50%;' alt='paradoxxxzero'/></a> | Provides an overridable request context for FastAPI endpoints
[fastapi_log](fastapi_log/) | 18.0.1.0.0 | <a href='https://github.com/paradoxxxzero'><img src='https://github.com/paradoxxxzero.png' width='32' height='32' style='border-radius:50%;' alt='paradoxxxzero'/></a> | Log Fastapi requests in database
[fastapi_log_mail](fastapi_log_mail/) | 18.0.1.0.0 | <a href='https://github.com/SirPyTech'><img src='https://github.com/SirPyTech.png' width='32' height='32' style='border-radius:50%;' alt='SirPyTech'/></a> | Notify logged exceptions.
[pydantic](pydantic/) | 18.0.1.1.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Utility addon to ease mapping between Pydantic and Odoo models
[rest_log](rest_log/) | 18.0.1.0.1 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Track REST API calls into DB

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/rma


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/rma&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/rma/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/rma/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/rma/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/rma/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/rma/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/rma)
[![Translation Status](https://translation.odoo-community.org/widgets/rma-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/rma-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# rma

rma

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[product_warranty](product_warranty/) | 18.0.1.0.0 | <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Product Warranty
[rma](rma/) | 18.0.2.5.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Return Merchandise Authorization (RMA)
[rma_batch](rma_batch/) | 18.0.1.0.0 |  | Group RMAs into batches for collective management
[rma_delivery](rma_delivery/) | 18.0.1.4.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allow to choose a default delivery carrier for returns
[rma_lot](rma_lot/) | 18.0.1.3.0 |  | Manage lot in RMA
[rma_reason](rma_reason/) | 18.0.1.1.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Rma Reason
[rma_repair](rma_repair/) | 18.0.1.0.1 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Create a repair order from rma
[rma_repair_lot](rma_repair_lot/) | 18.0.1.0.1 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | RMA Repair Lot
[rma_sale](rma_sale/) | 18.0.2.3.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Sale Order - Return Merchandise Authorization (RMA)
[rma_sale_auto_detect](rma_sale_auto_detect/) | 18.0.1.0.0 |  | Automatically link RMA products to related sales orders within an eligibility period
[rma_sale_delivery](rma_sale_delivery/) | 18.0.1.1.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | RMA Sale Delivery
[rma_sale_lot](rma_sale_lot/) | 18.0.1.1.0 |  | Manage sale returns with lot.
[rma_sale_mrp](rma_sale_mrp/) | 18.0.1.1.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allow doing RMAs from MRP kits
[rma_sale_reason](rma_sale_reason/) | 18.0.1.0.2 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Rma Sale Reason

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/route-planning


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# route-planning
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/route-planning&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/route-planning/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/route-planning/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/route-planning/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/route-planning/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/route-planning/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/route-planning)
[![Translation Status](https://translation.odoo-community.org/widgets/route-planning-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/route-planning-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

route-planning

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[route_planning](route_planning/) | 18.0.1.0.0 | <a href='https://github.com/carlos-lopez-tecnativa'><img src='https://github.com/carlos-lopez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carlos-lopez-tecnativa'/></a> | Route Planning

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/sale-blanket


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# sale-blanket
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sale-blanket&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/sale-blanket/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/sale-blanket/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/sale-blanket/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/sale-blanket/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/sale-blanket/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-blanket)
[![Translation Status](https://translation.odoo-community.org/widgets/sale-blanket-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sale-blanket-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

sale-blanket

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[sale_blanket_order](sale_blanket_order/) | 18.0.1.2.2 |  | Blanket Orders
[sale_order_blanket_order](sale_order_blanket_order/) | 18.0.1.0.3 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Manage blanket order and call of order
[sale_order_blanket_order_carrier_auto_assign](sale_order_blanket_order_carrier_auto_assign/) | 18.0.1.0.0 |  | Glue between sale_order_blanket_order and sale_order_carrier_auto_assign: keep auto-assigned carrier (delivery-fee) lines out of blanket-order call-off matching so they cannot consume blanket call-off capacity.
[sale_order_blanket_order_stock_prebook](sale_order_blanket_order_stock_prebook/) | 18.0.1.0.0 |  | Allow to prebook stock for blanket order
[sale_order_blanket_order_stock_prebook_release](sale_order_blanket_order_stock_prebook_release/) | 18.0.1.0.0 |  | Ensure that the date priotity when releasing qty is the start date of the blanker order

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/sale-channel


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sale-channel&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/sale-channel/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/sale-channel/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/sale-channel/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/sale-channel/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/sale-channel/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-channel)
[![Translation Status](https://translation.odoo-community.org/widgets/sale-channel-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sale-channel-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# sale-channel

sale-channel

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[sale_channel](sale_channel/) | 18.0.1.0.1 |  | Adds the notion of sale channels
[sale_channel_category](sale_channel_category/) | 18.0.1.0.0 |  | Link Category with sale channel
[sale_channel_partner](sale_channel_partner/) | 18.0.1.0.0 |  | Bind sale channels to contacts
[sale_channel_product](sale_channel_product/) | 18.0.1.0.0 |  | Link Product with sale channel
[sale_channel_search_engine](sale_channel_search_engine/) | 18.0.1.0.0 |  | Abstract module for configuring a search engine on a sale channel
[sale_channel_search_engine_category](sale_channel_search_engine_category/) | 18.0.1.0.0 |  | Implement an export of category in search engine based on sale channel link
[sale_channel_search_engine_product](sale_channel_search_engine_product/) | 18.0.1.0.0 |  | Implement an export of category in search engine based on sale channel link


Unported addons
---------------
addon | version | maintainers | summary
--- | --- | --- | ---
[sale_channel_search_engine_demo](sale_channel_search_engine_demo/) | 16.0.0.0.1 (unported) |  | Implement an export of category in search engine based on sale channel link

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/sale-prebook


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# Sales stock prebooking
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sale-prebook&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/sale-prebook/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/sale-prebook/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/sale-prebook/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/sale-prebook/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/sale-prebook/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-prebook)
[![Translation Status](https://translation.odoo-community.org/widgets/sale-prebook-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sale-prebook-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Manage stock reservations for non confirmed sales orders

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[sale_stock_prebook](sale_stock_prebook/) | 18.0.1.0.0 | <a href='https://github.com/mt-software-de'><img src='https://github.com/mt-software-de.png' width='32' height='32' style='border-radius:50%;' alt='mt-software-de'/></a> | Add process to prebook a sale order's stock before confirming it
[sale_stock_prebook_stock_available_to_promise_release](sale_stock_prebook_stock_available_to_promise_release/) | 18.0.1.0.0 | <a href='https://github.com/mt-software-de'><img src='https://github.com/mt-software-de.png' width='32' height='32' style='border-radius:50%;' alt='mt-software-de'/></a> | Extends the previous available qty to promised with moves of a reservation

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/sale-promotion


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# sale-promotion
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sale-promotion&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/sale-promotion/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/sale-promotion/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/sale-promotion/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/sale-promotion/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/sale-promotion/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-promotion)
[![Translation Status](https://translation.odoo-community.org/widgets/sale-promotion-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sale-promotion-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

sale-promotion

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[loyalty_coupon_no_mail](loyalty_coupon_no_mail/) | 18.0.1.0.0 | <a href='https://github.com/natuan9'><img src='https://github.com/natuan9.png' width='32' height='32' style='border-radius:50%;' alt='natuan9'/></a> | Generate coupons without triggering email notifications
[loyalty_criteria_multi_product](loyalty_criteria_multi_product/) | 18.0.1.0.1 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Allows to set as promotion criteria multi-product conditions
[loyalty_incompatibility](loyalty_incompatibility/) | 18.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allows to set incompatibility rules between promotions
[loyalty_limit](loyalty_limit/) | 18.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Restrict number of promotions per customer or salesman
[loyalty_mass_mailing](loyalty_mass_mailing/) | 18.0.1.0.0 |  | Loyalty Mass Mailing
[loyalty_multi_gift](loyalty_multi_gift/) | 18.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allows to configure multiple gift rewards per promotion
[loyalty_partner_applicability](loyalty_partner_applicability/) | 18.0.1.0.0 |  | Enables the definition of a customer filter for promotion rules that will only be applied to customers who meet the specified conditions in the filter.
[loyalty_program_chatter](loyalty_program_chatter/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Register messages and activities on the sale coupon records
[sale_loyalty_criteria_multi_product](sale_loyalty_criteria_multi_product/) | 18.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allows to set as promotion criteria multi-product conditions
[sale_loyalty_incompatibility](sale_loyalty_incompatibility/) | 18.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allows to set incompatibility rules between promotions in sale orders
[sale_loyalty_limit](sale_loyalty_limit/) | 18.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Restrict number of promotions per customer or salesman
[sale_loyalty_multi_gift](sale_loyalty_multi_gift/) | 18.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allows to configure multiple gift rewards per promotion in sales
[sale_loyalty_order_info](sale_loyalty_order_info/) | 18.0.1.0.0 |  | Add info on sale order about applied loyalties
[sale_loyalty_order_line_link](sale_loyalty_order_line_link/) | 18.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Adds a link between loyalty programs and their generated order linesfor easing tracking
[sale_loyalty_order_suggestion](sale_loyalty_order_suggestion/) | 18.0.1.0.2 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Suggest promotions in the sale order line
[sale_loyalty_order_suggestion_multi_gift](sale_loyalty_order_suggestion_multi_gift/) | 18.0.1.0.3 |  | Suggest promotions with rewards multi gift in the sale order line
[sale_loyalty_order_suggestion_multi_product](sale_loyalty_order_suggestion_multi_product/) | 18.0.1.0.1 |  | Suggest promotions with criteria multi product in the sale order line
[sale_loyalty_partner](sale_loyalty_partner/) | 18.0.1.0.0 |  | Sale Loyalty Partner
[sale_loyalty_partner_applicability](sale_loyalty_partner_applicability/) | 18.0.1.0.0 |  | Enables the definition of a customer filter for promotion rules that will only be applied to customers who meet the specified conditions in the filter.
[website_sale_loyalty_page](website_sale_loyalty_page/) | 18.0.1.0.0 |  | Website Sale Loyalty Page
[website_sale_loyalty_suggestion_wizard](website_sale_loyalty_suggestion_wizard/) | 18.0.1.0.1 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Suggests promotions and allows you to configure and apply these promotions directly from the website
[website_sale_loyalty_suggestion_wizard_multi_gift](website_sale_loyalty_suggestion_wizard_multi_gift/) | 18.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Suggests promotions multi-gift and allows you to configure and apply these promotions directly from the website
[website_sale_loyalty_suggestion_wizard_multi_product](website_sale_loyalty_suggestion_wizard_multi_product/) | 18.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Suggests promotions multi-product and allows you to configure and apply these promotions directly from the website

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/sale-reporting


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sale-reporting&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/sale-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/sale-reporting/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/sale-reporting/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/sale-reporting/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/sale-reporting/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/sale-reporting-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sale-reporting-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# sale-reporting

sale-reporting

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[product_sold_by_delivery_week](product_sold_by_delivery_week/) | 18.0.1.1.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Adds a field that graphically hints the weekly product sales
[sale_comment_template](sale_comment_template/) | 18.0.1.0.0 |  | Comments texts templates on Sale documents
[sale_layout_category_hide_detail](sale_layout_category_hide_detail/) | 18.0.1.0.0 |  | Hide details for sections in sale orders and invoices for reports and customer portal
[sale_order_line_position](sale_order_line_position/) | 18.0.1.0.1 |  | Adds position number on sale order line.
[sale_order_product_recommendation_product_sold_by_delivery_week](sale_order_product_recommendation_product_sold_by_delivery_week/) | 18.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Adds the weekly sales field to the recommendation wizard
[sale_order_report_hide_tax](sale_order_report_hide_tax/) | 18.0.1.0.2 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Hide taxes column when they don't add value
[sale_order_report_product_image](sale_order_report_product_image/) | 18.0.1.0.2 |  | Show product images on Sale documents
[sale_order_weight](sale_order_weight/) | 18.0.1.0.0 |  | Add products weight in report for sale order
[sale_packaging_report](sale_packaging_report/) | 18.0.1.0.0 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Packaging data in sale reports
[sale_report_delivered](sale_report_delivered/) | 18.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Sale Report Delivered
[sale_report_delivered_attribute_values](sale_report_delivered_attribute_values/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Allow to view Attribute values of Lines on Sale Report Delivered
[sale_report_delivered_brand](sale_report_delivered_brand/) | 18.0.1.0.1 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Sale Report Delivered Brand
[sale_report_delivered_elaboration](sale_report_delivered_elaboration/) | 18.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Sale Report Delivered Elaboration
[sale_report_delivered_partner_priority](sale_report_delivered_partner_priority/) | 18.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Sale Report Delivered Partner Priority
[sale_report_delivered_semaphore](sale_report_delivered_semaphore/) | 18.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Sale Report Delivered Semaphore
[sale_report_delivered_subtotal](sale_report_delivered_subtotal/) | 18.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Sale Report Delivered subtotal
[sale_report_delivered_volume](sale_report_delivered_volume/) | 18.0.1.0.0 |  | Sale Report Delivered Volume
[sale_report_salesperson_from_partner](sale_report_salesperson_from_partner/) | 18.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Sale Report Salesperson From Partner

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/sale-workflow


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sale-workflow&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/sale-workflow/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/sale-workflow/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/sale-workflow/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/sale-workflow/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/sale-workflow/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-workflow)
[![Translation Status](https://translation.odoo-community.org/widgets/sale-workflow-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sale-workflow-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# sale-workflow

sale-workflow

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[partner_sale_pivot](partner_sale_pivot/) | 18.0.1.0.0 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | Sales analysis from customer form view
[portal_sale_list_extra_info](portal_sale_list_extra_info/) | 18.0.1.0.0 |  | Adds additional fields 'client_order_ref' and 'amount_untaxed' to the portal view. It also makes it easier to add other fields in the future.
[portal_sale_order_search](portal_sale_order_search/) | 18.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Allow customers to set and search their own order reference in portal
[portal_sale_personal_data_only](portal_sale_personal_data_only/) | 18.0.1.0.0 |  | Portal Sale Personal Data Only
[pricelist_cache](pricelist_cache/) | 18.0.1.0.0 |  | Provide a new model to cache price lists and update it, to make it easier to retrieve them.
[pricelist_cache_rest](pricelist_cache_rest/) | 18.0.1.0.0 |  | Provides an endpoint to get product prices for a given customer
[product_customerinfo_elaboration](product_customerinfo_elaboration/) | 18.0.1.0.0 |  | Allows to define default elaborations and elaboration notes on product customerinfos
[product_customerinfo_sale](product_customerinfo_sale/) | 18.0.1.0.1 |  | Loads in every sale order line the customer code defined in the product
[product_form_sale_link](product_form_sale_link/) | 18.0.1.0.1 |  | Adds a button on product forms to access Sale Lines
[product_price_category](product_price_category/) | 18.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Add Price Category field on product and allow to apply a pricelist on this field.
[product_set_sell_only_by_packaging](product_set_sell_only_by_packaging/) | 18.0.1.0.0 |  | Glue module between `sell_only_by_packaging` and `sale_product_set_packaging_qty`.
[sale_advance_payment](sale_advance_payment/) | 18.0.1.0.2 |  | Allow to add advance payments on sales and then use them on invoices
[sale_automatic_workflow](sale_automatic_workflow/) | 18.0.1.1.0 |  | Sale Automatic Workflow
[sale_automatic_workflow_force_invoiced](sale_automatic_workflow_force_invoiced/) | 18.0.1.0.0 |  | Force Invoice as an automatic workflow option
[sale_automatic_workflow_job](sale_automatic_workflow_job/) | 18.0.1.0.2 |  | Execute sale automatic workflows in queue jobs
[sale_automatic_workflow_periodicity](sale_automatic_workflow_periodicity/) | 18.0.1.0.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Adds a period for the execution of a workflow.
[sale_automatic_workflow_stock](sale_automatic_workflow_stock/) | 18.0.1.0.0 |  | Sale Automatic Workflow Stock
[sale_automatic_workflow_stock_job](sale_automatic_workflow_stock_job/) | 18.0.1.0.0 |  | Sale Automatic Workflow Stock Job
[sale_block_no_stock](sale_block_no_stock/) | 18.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Block Sales if products has not enough Quantity based on a chosen field
[sale_cancel_reason](sale_cancel_reason/) | 18.0.1.0.0 |  | Sale Cancel Reason
[sale_commercial_partner](sale_commercial_partner/) | 18.0.1.2.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add stored related field 'Commercial Entity' on sale orders
[sale_company_currency](sale_company_currency/) | 18.0.1.0.0 |  | Company Currency in Sale Orders
[sale_confirm_group](sale_confirm_group/) | 18.0.1.0.0 |  | Allows configuring a list of groups per-company who are granted permission to confirm sale orders
[sale_custom_rounding](sale_custom_rounding/) | 18.0.1.0.0 |  | Custom taxes rounding method in sale orders
[sale_delivery_split_date](sale_delivery_split_date/) | 18.0.1.0.0 |  | Sale Deliveries split by date
[sale_delivery_state](sale_delivery_state/) | 18.0.1.2.1 |  | Show the delivery state on the sale order
[sale_discount_display_amount](sale_discount_display_amount/) | 18.0.1.0.0 |  | This addon intends to display the amount of the discount computed on sale_order_line and sale_order level
[sale_elaboration](sale_elaboration/) | 18.0.1.3.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Set an elaboration for any sale line
[sale_elaboration_brand](sale_elaboration_brand/) | 18.0.1.0.0 | <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Show product brand in sale elaboration report
[sale_exception](sale_exception/) | 18.0.2.2.0 |  | Custom exceptions on sale order
[sale_exception_product_sale_manufactured_for](sale_exception_product_sale_manufactured_for/) | 18.0.1.0.0 |  | The partner set in the sales order can order only if he/she has a commercial entity that is listed as one of the partners for which the products can be manufactured for.
[sale_fixed_discount](sale_fixed_discount/) | 18.0.1.0.0 |  | Allows to apply fixed amount discounts in sales orders.
[sale_force_invoiced](sale_force_invoiced/) | 18.0.1.0.1 |  | Allows to force the invoice status of the sales order to Invoiced
[sale_force_invoiced_quantity](sale_force_invoiced_quantity/) | 18.0.1.0.0 |  | Add manual invoice quantity in sales order lines
[sale_global_discount](sale_global_discount/) | 18.0.1.0.0 |  | Sale Global Discount
[sale_invoice_blocking](sale_invoice_blocking/) | 18.0.1.0.0 |  | Allow you to block the creation of invoices from a sale order.
[sale_invoice_frequency](sale_invoice_frequency/) | 18.0.1.1.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Define the invoice frequency for customers
[sale_invoice_plan](sale_invoice_plan/) | 18.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Add to sales order, ability to manage future invoice plan
[sale_invoice_plan_report](sale_invoice_plan_report/) | 18.0.1.0.0 | <a href='https://github.com/kaynnan'><img src='https://github.com/kaynnan.png' width='32' height='32' style='border-radius:50%;' alt='kaynnan'/></a> <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Add invoice plan to sales order/quotation PDF report
[sale_invoice_policy](sale_invoice_policy/) | 18.0.1.1.0 |  | Sales Management: let the user choose the invoice policy on the order
[sale_invoice_product_not_alone](sale_invoice_product_not_alone/) | 18.0.1.0.0 |  | Set products to not invoice alone
[sale_invoice_split_payment](sale_invoice_split_payment/) | 18.0.1.0.0 |  | Split by payment term generated invoices from sale orders
[sale_line_name_option](sale_line_name_option/) | 18.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Display product description without reference code on sale order lines
[sale_mail_autosubscribe](sale_mail_autosubscribe/) | 18.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Automatically subscribe partners to their company's sale orders
[sale_manual_delivery](sale_manual_delivery/) | 18.0.1.1.0 |  | Create manually your deliveries
[sale_mrp_bom](sale_mrp_bom/) | 18.0.1.0.0 |  | Allows define a BOM in the sales lines.
[sale_multi_template_application](sale_multi_template_application/) | 18.0.1.0.0 |  | Sale multi template application
[sale_order_amount_to_invoice](sale_order_amount_to_invoice/) | 18.0.1.0.0 |  | Show total amount to invoice in quotations/sales orders
[sale_order_archive](sale_order_archive/) | 18.0.1.0.0 |  | Archive Sale Orders
[sale_order_cancel_optional_email](sale_order_cancel_optional_email/) | 18.0.1.0.0 |  | Cancel sales orders directly without proposing to send email to customer
[sale_order_carrier_auto_assign](sale_order_carrier_auto_assign/) | 18.0.1.0.2 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Auto assign delivery carrier on sale order confirmation
[sale_order_disable_user_autosubscribe](sale_order_disable_user_autosubscribe/) | 18.0.1.0.0 |  | Remove the salesperson from autosubscribed sale followers
[sale_order_finish_service](sale_order_finish_service/) | 18.0.1.0.0 |  | Adds a finish service flag on sale orders
[sale_order_general_discount](sale_order_general_discount/) | 18.0.1.0.1 |  | General discount per sale order
[sale_order_invoice_amount](sale_order_invoice_amount/) | 18.0.1.0.0 |  | Display the invoiced and uninvoiced total in the sale order
[sale_order_invoicing_finished_task](sale_order_invoicing_finished_task/) | 18.0.1.0.0 |  | Control invoice order lines if their related task has been set to invoiceable
[sale_order_line_cancel](sale_order_line_cancel/) | 18.0.1.1.0 |  | Sale cancel remaining
[sale_order_line_cancel_sale_stock](sale_order_line_cancel_sale_stock/) | 18.0.1.1.0 |  | Sale cancel remaining stock
[sale_order_line_chained_move](sale_order_line_chained_move/) | 18.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | This module adds a field on sale order line to get all related move lines
[sale_order_line_client_order_ref](sale_order_line_client_order_ref/) | 18.0.1.0.1 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Customer Reference on Sale Order Lines and Invoice Lines
[sale_order_line_date](sale_order_line_date/) | 18.0.1.0.2 |  | Adds a commitment date to each sale order line.
[sale_order_line_delivery_state](sale_order_line_delivery_state/) | 18.0.1.0.0 |  | Show the delivery state on the sale order line
[sale_order_line_description](sale_order_line_description/) | 18.0.1.0.0 |  | Sale order line description
[sale_order_line_effective_date](sale_order_line_effective_date/) | 18.0.1.1.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Calculated effective dates in Sale Order Lines
[sale_order_line_input](sale_order_line_input/) | 18.0.1.0.1 |  | Search, create or modify directly sale order lines
[sale_order_line_menu](sale_order_line_menu/) | 18.0.1.0.0 |  | Adds a Sale Order Lines Menu
[sale_order_line_no_print](sale_order_line_no_print/) | 18.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Hide order lines in reports
[sale_order_line_note](sale_order_line_note/) | 18.0.1.0.0 |  | Note on sale order line
[sale_order_line_price_history](sale_order_line_price_history/) | 18.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Sale order line price history
[sale_order_line_price_lock_by_pricelist](sale_order_line_price_lock_by_pricelist/) | 18.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Lock price or discount edition depending on pricelist items
[sale_order_line_product_attribute_values](sale_order_line_product_attribute_values/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Store Product Attribute Values in Sale Order Lines
[sale_order_line_remove](sale_order_line_remove/) | 18.0.1.0.0 |  | Allows removal of sale order lines from confirmed orders if not invoiced or received
[sale_order_line_sequence](sale_order_line_sequence/) | 18.0.1.2.0 |  | Propagates SO line sequence to invoices and stock picking.
[sale_order_line_stock_move_history](sale_order_line_stock_move_history/) | 18.0.1.0.0 | <a href='https://github.com/ppyczko'><img src='https://github.com/ppyczko.png' width='32' height='32' style='border-radius:50%;' alt='ppyczko'/></a> | Show stock moves history for sale order lines
[sale_order_line_tag](sale_order_line_tag/) | 18.0.1.0.0 | <a href='https://github.com/smaciaosi'><img src='https://github.com/smaciaosi.png' width='32' height='32' style='border-radius:50%;' alt='smaciaosi'/></a> <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> <a href='https://github.com/ckolobow'><img src='https://github.com/ckolobow.png' width='32' height='32' style='border-radius:50%;' alt='ckolobow'/></a> | Add tags to classify sales order line reasons
[sale_order_lot_generator](sale_order_lot_generator/) | 18.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> <a href='https://github.com/mourad-ehm'><img src='https://github.com/mourad-ehm.png' width='32' height='32' style='border-radius:50%;' alt='mourad-ehm'/></a> <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Sale Order Lot Generator
[sale_order_lot_selection](sale_order_lot_selection/) | 18.0.1.4.0 | <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> | Sale Order Lot Selection
[sale_order_lot_selection_price](sale_order_lot_selection_price/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Sale Order Lot Selection Price
[sale_order_note_template](sale_order_note_template/) | 18.0.1.0.0 |  | Add sale orders terms and conditions template that can be used to quickly fullfill sale order terms and conditions
[sale_order_price_recalculation](sale_order_price_recalculation/) | 18.0.1.0.0 |  | Recalculate prices / Reset descriptions on sale order lines
[sale_order_priority](sale_order_priority/) | 18.0.1.0.0 |  | Define priority on sale orders
[sale_order_product_assortment](sale_order_product_assortment/) | 18.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Module that allows to use the assortments on sale orders
[sale_order_product_availability_inline](sale_order_product_availability_inline/) | 18.0.1.0.1 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | Show product availability in sales order line product drop-down.
[sale_order_product_recommendation](sale_order_product_recommendation/) | 18.0.1.1.3 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Recommend products to sell to customer based on history
[sale_order_report_without_price](sale_order_report_without_price/) | 18.0.1.0.0 |  | Allow you to generate quotation and order reports without price.
[sale_order_requested_delivery](sale_order_requested_delivery/) | 18.0.1.0.0 |  | This module adds two new fields `requested_delivery_period_start` and `requested_delivery_period_end` to both the `sale.order` and `sale.order.line` models.
[sale_order_restrict_copy_archived_product](sale_order_restrict_copy_archived_product/) | 18.0.1.0.0 |  | Restrict dulpication of sales order if they have archived products
[sale_order_revision](sale_order_revision/) | 18.0.1.0.1 |  | Keep track of revised quotations
[sale_order_secondary_unit](sale_order_secondary_unit/) | 18.0.1.0.2 |  | Sale product in a secondary unit
[sale_order_show_currency_rate](sale_order_show_currency_rate/) | 18.0.1.1.0 |  | Show informative exchange rate on sale order PDF reports
[sale_order_split_strategy](sale_order_split_strategy/) | 18.0.1.1.0 | <a href='https://github.com/grindtildeath'><img src='https://github.com/grindtildeath.png' width='32' height='32' style='border-radius:50%;' alt='grindtildeath'/></a> | Define strategies to split sales orders
[sale_order_tag](sale_order_tag/) | 18.0.1.0.0 | <a href='https://github.com/patrickrwilson'><img src='https://github.com/patrickrwilson.png' width='32' height='32' style='border-radius:50%;' alt='patrickrwilson'/></a> | Adds Tags to Sales Orders.
[sale_order_team_from_product](sale_order_team_from_product/) | 18.0.1.0.0 |  | Set Sales Team on quotations from product Sales Teams
[sale_order_transmit_method](sale_order_transmit_method/) | 18.0.1.0.0 |  | Set transmit method (email, post, portal, ...) in sale order and propagate it to invoices
[sale_order_type](sale_order_type/) | 18.0.1.3.0 |  | Sale Order Type
[sale_order_type_confirm_message](sale_order_type_confirm_message/) | 18.0.1.0.0 |  | Confirmation requirement when validating sale
[sale_order_warn_message](sale_order_warn_message/) | 18.0.1.0.1 |  | Add a popup warning on sale to ensure warning is populated
[sale_packaging_default](sale_packaging_default/) | 18.0.1.1.0 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Simplify using products default packaging for sales
[sale_partner_address_restrict](sale_partner_address_restrict/) | 18.0.1.0.0 |  | Restrict addresses domain in the sales order form taking into account the partner selected
[sale_partner_incoterm](sale_partner_incoterm/) | 18.0.1.0.0 |  | Set the customer preferred incoterm on each sales order
[sale_partner_primeship](sale_partner_primeship/) | 18.0.1.0.2 | <a href='https://github.com/nayatec'><img src='https://github.com/nayatec.png' width='32' height='32' style='border-radius:50%;' alt='nayatec'/></a> <a href='https://github.com/paradoxxxzero'><img src='https://github.com/paradoxxxzero.png' width='32' height='32' style='border-radius:50%;' alt='paradoxxxzero'/></a> | Allow you to manage time limited prime memberships and prime membership activation products.
[sale_partner_selectable_option](sale_partner_selectable_option/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Sale Partner Selectable Option
[sale_partner_shipping_default_partner_invoice](sale_partner_shipping_default_partner_invoice/) | 18.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Set invoice address based on shipping address for sales orders
[sale_payment_sheet](sale_payment_sheet/) | 18.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Allow to create invoice payments to commercial users without accounting permissions
[sale_planner_calendar](sale_planner_calendar/) | 18.0.1.0.1 |  | Sale planner calendar
[sale_pricelist_display_surcharge](sale_pricelist_display_surcharge/) | 18.0.1.0.0 |  | This module shows to the customer the surcharges if wanted.
[sale_pricelist_from_commitment_date](sale_pricelist_from_commitment_date/) | 18.0.1.0.0 |  | Use sale order commitment date to compute line price from pricelist
[sale_pricelist_packaging](sale_pricelist_packaging/) | 18.0.1.0.0 | <a href='https://github.com/mathieudelva'><img src='https://github.com/mathieudelva.png' width='32' height='32' style='border-radius:50%;' alt='mathieudelva'/></a> | Sale Pricelist Packaging
[sale_probability_amount](sale_probability_amount/) | 18.0.1.0.0 |  | add a win probability on quotation
[sale_procurement_group_by_line](sale_procurement_group_by_line/) | 18.0.1.0.2 |  | Base module for multiple procurement group by Sale order
[sale_product_identification](sale_product_identification/) | 18.0.1.0.0 |  | Sale Product Identification Numbers
[sale_product_multi_add](sale_product_multi_add/) | 18.0.1.0.0 |  | Sale Product Multi Add
[sale_product_set](sale_product_set/) | 18.0.1.0.0 |  | Sales product set
[sale_product_set_packaging_qty](sale_product_set_packaging_qty/) | 18.0.1.0.0 |  | Manage packaging and quantities on product set lines
[sale_purchase_stock_auto_cancel](sale_purchase_stock_auto_cancel/) | 18.0.1.0.0 | <a href='https://github.com/carlos-lopez-tecnativa'><img src='https://github.com/carlos-lopez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carlos-lopez-tecnativa'/></a> | Sale purchase stock auto cancel
[sale_purchase_stock_auto_confirm](sale_purchase_stock_auto_confirm/) | 18.0.1.0.0 | <a href='https://github.com/carlos-lopez-tecnativa'><img src='https://github.com/carlos-lopez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carlos-lopez-tecnativa'/></a> | Sale purchase stock auto confirm
[sale_quotation_number](sale_quotation_number/) | 18.0.1.0.0 |  | Different sequence for sale quotations
[sale_readonly_security](sale_readonly_security/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Sale Readonly Security
[sale_require_po_doc](sale_require_po_doc/) | 18.0.1.0.1 |  | Sale Orders Require PO or Sales Documentation
[sale_resource_booking](sale_resource_booking/) | 18.0.1.0.0 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Link resource bookings with sales
[sale_semaphore](sale_semaphore/) | 18.0.1.0.1 |  | Adds a semaphore for commercial purposes
[sale_shipping_info_helper](sale_shipping_info_helper/) | 18.0.1.0.0 |  | Add shipping amounts on sale order
[sale_sourced_by_line](sale_sourced_by_line/) | 18.0.1.0.1 |  | Multiple warehouse source locations for Sale order
[sale_start_end_dates](sale_start_end_dates/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adds start date and end date on sale order lines
[sale_stock_cancel_restriction](sale_stock_cancel_restriction/) | 18.0.1.0.0 |  | Sale Stock Cancel Restriction
[sale_stock_delivery_address](sale_stock_delivery_address/) | 18.0.1.1.1 |  | Sale Stock Delivery Address
[sale_stock_delivery_state](sale_stock_delivery_state/) | 18.0.1.0.0 |  | Change the way to compute the delivery state
[sale_stock_expiry_date_on_qty_at_date_widget](sale_stock_expiry_date_on_qty_at_date_widget/) | 18.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> | Show next Expiry Date on Qty at Date Widget
[sale_stock_last_date](sale_stock_last_date/) | 18.0.1.0.0 |  | Displays last delivery date in sale order lines
[sale_stock_line_customer_ref](sale_stock_line_customer_ref/) | 18.0.1.0.0 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Allow you to add a customer reference on order lines propagaged to move operations.
[sale_stock_line_sequence](sale_stock_line_sequence/) | 18.0.1.0.0 |  | Glue Module for Sale Order Line Sequence and Stock Picking Line Sequence
[sale_stock_partner_warehouse](sale_stock_partner_warehouse/) | 18.0.1.1.0 |  | Allow to choose by default a warehouse on SO based on a Partner parameter
[sale_stock_picking_blocking](sale_stock_picking_blocking/) | 18.0.1.0.2 |  | Allow you to block the creation of deliveries from a sale order.
[sale_stock_picking_note](sale_stock_picking_note/) | 18.0.1.1.0 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Add picking note in sale and purchase order
[sale_stock_reservation_issue_on_qty_at_date_widget](sale_stock_reservation_issue_on_qty_at_date_widget/) | 18.0.1.0.2 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> | Warn user when a reservation issue will happen when confirming an order
[sale_stock_return_request](sale_stock_return_request/) | 18.0.1.0.2 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Sale Stock Return Request
[sale_stock_secondary_unit](sale_stock_secondary_unit/) | 18.0.1.0.0 |  | Get product quantities in a secondary unit
[sale_substate](sale_substate/) | 18.0.1.0.0 |  | Sale Sub State
[sale_team_payment_term](sale_team_payment_term/) | 18.0.1.0.0 | <a href='https://github.com/Kev-Roche'><img src='https://github.com/Kev-Roche.png' width='32' height='32' style='border-radius:50%;' alt='Kev-Roche'/></a> | add payment term on sale team
[sale_tier_validation](sale_tier_validation/) | 18.0.1.1.0 |  | Extends the functionality of Sale Orders to support a tier validation process.
[sale_transaction_form_link](sale_transaction_form_link/) | 18.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Allows to display a link to payment transactions on Sale Order form view.
[sale_validity_auto_cancel](sale_validity_auto_cancel/) | 18.0.1.1.0 | <a href='https://github.com/JordiMForgeFlow'><img src='https://github.com/JordiMForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiMForgeFlow'/></a> | Automatically cancel quotations after validity period.
[sale_warn_option](sale_warn_option/) | 18.0.1.0.2 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Add Options to Sale Warn Messages
[sale_wishlist](sale_wishlist/) | 18.0.1.0.0 |  | Handle sale wishlist for partners
[sales_team_security](sales_team_security/) | 18.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | New group for seeing only sales channel's documents
[sell_only_by_packaging](sell_only_by_packaging/) | 18.0.1.1.0 |  | Manage sale of packaging
[web_widget_product_label_section_and_note_full_label_sale](web_widget_product_label_section_and_note_full_label_sale/) | 18.0.1.0.0 |  | Glue module between web_widget_product_label_section_and_note_full_label and sale.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/search-engine


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# search-engine
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/search-engine&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/search-engine/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/search-engine/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/search-engine/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/search-engine/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/search-engine/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/search-engine)
[![Translation Status](https://translation.odoo-community.org/widgets/search-engine-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/search-engine-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

search-engine

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[connector_elasticsearch](connector_elasticsearch/) | 18.0.1.0.0 |  | Connector For Elasticsearch Search Engine
[connector_search_engine](connector_search_engine/) | 18.0.1.1.0 |  | Connector Search Engine
[connector_typesense](connector_typesense/) | 18.0.1.0.0 |  | Connector For Typesense Search Engine
[search_engine_serializer_pydantic](search_engine_serializer_pydantic/) | 18.0.1.0.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Defines base class for pydantic baser serializer


Unported addons
---------------
addon | version | maintainers | summary
--- | --- | --- | ---
[connector_algolia](connector_algolia/) | 14.0.2.2.0 (unported) |  | Connector For Algolia Search Engine
[connector_search_engine_serializer_ir_export](connector_search_engine_serializer_ir_export/) | 16.0.1.0.2 (unported) |  | Use Exporter (ir.exports) as serializer for index
[search_engine_image_thumbnail](search_engine_image_thumbnail/) | 16.0.1.0.7 (unported) | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Generate thumbnails for binded record

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/server-auth


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# server-auth
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-auth&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/server-auth/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/server-auth/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/server-auth/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/server-auth/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/server-auth/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-auth)
[![Translation Status](https://translation.odoo-community.org/widgets/server-auth-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-auth-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

server-auth

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[auth_admin_passkey](auth_admin_passkey/) | 18.0.1.0.0 |  | Allows system administrator to authenticate with any account
[auth_api_key](auth_api_key/) | 18.0.1.0.2 |  | Authenticate http requests from an API key
[auth_api_key_group](auth_api_key_group/) | 18.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Allow grouping API keys together. Grouping per se does nothing. This feature is supposed to be used by other modules to limit access to services or records based on groups of keys.
[auth_api_key_server_env](auth_api_key_server_env/) | 18.0.1.0.0 |  | Configure api keys via server env. This can be very useful to avoid mixing your keys between your various environments when restoring databases. All you have to do is to add a new section to your configuration file according to the following convention:
[auth_jwt](auth_jwt/) | 18.0.1.0.2 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | JWT bearer token authentication.
[auth_jwt_demo](auth_jwt_demo/) | 18.0.1.0.1 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Test/demo module for auth_jwt.
[auth_oauth_filter_by_domain](auth_oauth_filter_by_domain/) | 18.0.1.0.0 | <a href='https://github.com/natuan9'><img src='https://github.com/natuan9.png' width='32' height='32' style='border-radius:50%;' alt='natuan9'/></a> | Filter OAuth providers by domain
[auth_oauth_login_field](auth_oauth_login_field/) | 18.0.1.0.0 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Handle the login field in OAuth signup
[auth_oauth_multi_token](auth_oauth_multi_token/) | 18.0.2.0.0 |  | Allow multiple connection with the same OAuth account
[auth_oidc](auth_oidc/) | 18.0.1.1.0 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Allow users to login through OpenID Connect Provider
[auth_oidc_environment](auth_oidc_environment/) | 18.0.1.0.0 |  | This module allows to use server env for OIDC configuration
[auth_saml](auth_saml/) | 18.0.1.1.1 | <a href='https://github.com/vincent-hatakeyama'><img src='https://github.com/vincent-hatakeyama.png' width='32' height='32' style='border-radius:50%;' alt='vincent-hatakeyama'/></a> | SAML2 Authentication
[auth_session_timeout](auth_session_timeout/) | 18.0.1.0.0 |  | This module disable all inactive sessions since a given delay
[auth_signup_verify_email](auth_signup_verify_email/) | 18.0.1.0.0 |  | Force uninvited users to use a good email for signup
[auth_user_case_insensitive](auth_user_case_insensitive/) | 18.0.1.0.0 |  | Makes the user login field case insensitive
[base_user_empty_password](base_user_empty_password/) | 18.0.1.0.0 | <a href='https://github.com/grindtildeath'><img src='https://github.com/grindtildeath.png' width='32' height='32' style='border-radius:50%;' alt='grindtildeath'/></a> | Allows to empty password of users
[base_user_show_email](base_user_show_email/) | 18.0.1.0.0 |  | Untangle user login and email
[cross_connect_client](cross_connect_client/) | 18.0.1.0.0 | <a href='https://github.com/paradoxxxzero'><img src='https://github.com/paradoxxxzero.png' width='32' height='32' style='border-radius:50%;' alt='paradoxxxzero'/></a> | Cross Connect Client allows to connect to a Cross Connect Server enabled odoo instance.
[cross_connect_server](cross_connect_server/) | 18.0.1.0.0 | <a href='https://github.com/paradoxxxzero'><img src='https://github.com/paradoxxxzero.png' width='32' height='32' style='border-radius:50%;' alt='paradoxxxzero'/></a> | Cross Connect Server allows Cross Connect Client to connect to it.
[impersonate_login](impersonate_login/) | 18.0.1.1.1 | <a href='https://github.com/Kev-Roche'><img src='https://github.com/Kev-Roche.png' width='32' height='32' style='border-radius:50%;' alt='Kev-Roche'/></a> | tools
[password_security](password_security/) | 18.0.1.0.0 |  | Allow admin to set password security requirements.
[user_log_view](user_log_view/) | 18.0.1.0.0 | <a href='https://github.com/trojikman'><img src='https://github.com/trojikman.png' width='32' height='32' style='border-radius:50%;' alt='trojikman'/></a> | Allow to see user's actions log
[users_ldap_mail](users_ldap_mail/) | 18.0.1.0.0 | <a href='https://github.com/joao-p-marques'><img src='https://github.com/joao-p-marques.png' width='32' height='32' style='border-radius:50%;' alt='joao-p-marques'/></a> | LDAP mapping for user name and e-mail
[vault](vault/) | 18.0.1.0.3 |  | Password vault integration in Odoo
[vault_share](vault_share/) | 18.0.1.0.0 |  | Implementation of a mechanism to share secrets

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/server-backend


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-backend&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/server-backend/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/server-backend/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/server-backend/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/server-backend/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/server-backend/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-backend)
[![Translation Status](https://translation.odoo-community.org/widgets/server-backend-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-backend-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# server-backend

server-backend

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_external_dbsource](base_external_dbsource/) | 18.0.1.0.1 |  | External Database Sources
[base_external_dbsource_mssql](base_external_dbsource_mssql/) | 18.0.1.0.4 | <a href='https://github.com/anddago78'><img src='https://github.com/anddago78.png' width='32' height='32' style='border-radius:50%;' alt='anddago78'/></a> | External Database Source - MSSQL
[base_external_dbsource_mysql](base_external_dbsource_mysql/) | 18.0.1.0.0 |  | External Database Source - MySQL
[base_external_dbsource_sqlite](base_external_dbsource_sqlite/) | 18.0.1.0.0 | <a href='https://github.com/anddago78'><img src='https://github.com/anddago78.png' width='32' height='32' style='border-radius:50%;' alt='anddago78'/></a> | External Database Source - SQLite
[base_external_system](base_external_system/) | 18.0.1.0.0 | <a href='https://github.com/NL66278'><img src='https://github.com/NL66278.png' width='32' height='32' style='border-radius:50%;' alt='NL66278'/></a> | Data models allowing for connection to external systems.
[base_global_discount](base_global_discount/) | 18.0.1.0.0 |  | Base Global Discount
[base_group_backend](base_group_backend/) | 18.0.1.1.0 | <a href='https://github.com/FranzPoize'><img src='https://github.com/FranzPoize.png' width='32' height='32' style='border-radius:50%;' alt='FranzPoize'/></a> <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Group backend
[base_ical](base_ical/) | 18.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Provide (readonly) .ics URLs to calendar-like models
[base_import_match](base_import_match/) | 18.0.1.0.0 |  | Try to avoid duplicates before importing
[base_portal_type](base_portal_type/) | 18.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Base module to allow different types of portals
[base_user_effective_permissions](base_user_effective_permissions/) | 18.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Inspect effective permissions applying to a user
[base_user_role](base_user_role/) | 18.0.1.0.7 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> <a href='https://github.com/jcdrubay'><img src='https://github.com/jcdrubay.png' width='32' height='32' style='border-radius:50%;' alt='jcdrubay'/></a> <a href='https://github.com/novawish'><img src='https://github.com/novawish.png' width='32' height='32' style='border-radius:50%;' alt='novawish'/></a> | User roles
[base_user_role_company](base_user_role_company/) | 18.0.1.0.2 |  | User roles by company
[base_user_role_history](base_user_role_history/) | 18.0.1.0.0 | <a href='https://github.com/ThomasBinsfeld'><img src='https://github.com/ThomasBinsfeld.png' width='32' height='32' style='border-radius:50%;' alt='ThomasBinsfeld'/></a> | This module allows to track the changes on users roles.
[base_user_role_profile](base_user_role_profile/) | 18.0.1.0.0 |  | User profiles
[server_action_navigate](server_action_navigate/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/ashishhirpara'><img src='https://github.com/ashishhirpara.png' width='32' height='32' style='border-radius:50%;' alt='ashishhirpara'/></a> | Navigate between any items of any Odoo Models
[server_action_sort](server_action_sort/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Sort any lines of any models by any criterias

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/server-brand


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-brand&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/server-brand/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/server-brand/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/server-brand/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/server-brand/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/server-brand/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-brand)
[![Translation Status](https://translation.odoo-community.org/widgets/server-brand-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-brand-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# server-brand

server-brand

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[disable_odoo_online](disable_odoo_online/) | 18.0.1.0.0 |  | Remove odoo.com Bindings
[portal_odoo_debranding](portal_odoo_debranding/) | 18.0.1.0.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Remove Odoo Branding from Website
[remove_odoo_enterprise](remove_odoo_enterprise/) | 18.0.1.0.0 |  | Remove enterprise modules and setting items

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/server-env


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-env&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/server-env/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/server-env/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/server-env/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/server-env/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/server-env/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-env)
[![Translation Status](https://translation.odoo-community.org/widgets/server-env-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-env-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# server-env

server-env

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[auth_saml_environment](auth_saml_environment/) | 18.0.1.0.0 |  | Allows system administrator to authenticate with any account
[data_encryption](data_encryption/) | 18.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Store accounts and credentials encrypted by environment
[mail_environment](mail_environment/) | 18.0.1.0.1 |  | Configure mail servers with server_environment_files
[mail_environment_google_gmail](mail_environment_google_gmail/) | 18.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Configure Gmail mail servers with server_environment_files
[server_environment](server_environment/) | 18.0.1.0.6 |  | move some configurations out of the database
[server_environment_data_encryption](server_environment_data_encryption/) | 18.0.1.0.1 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Server Environment Data Encryption
[server_environment_ir_config_parameter](server_environment_ir_config_parameter/) | 18.0.1.0.0 |  | Override System Parameters from server environment file

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/server-tools


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-tools&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/server-tools/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/server-tools/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/server-tools/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/server-tools/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/server-tools/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-tools)
[![Translation Status](https://translation.odoo-community.org/widgets/server-tools-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-tools-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# server-tools

server-tools

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[attachment_delete_restrict](attachment_delete_restrict/) | 18.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/Kev-Roche'><img src='https://github.com/Kev-Roche.png' width='32' height='32' style='border-radius:50%;' alt='Kev-Roche'/></a> | Restrict Deletion of Attachments
[attachment_queue](attachment_queue/) | 18.0.1.0.1 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> | Base module adding the concept of queue for processing files
[attachment_synchronize](attachment_synchronize/) | 18.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> <a href='https://github.com/GSLabIt'><img src='https://github.com/GSLabIt.png' width='32' height='32' style='border-radius:50%;' alt='GSLabIt'/></a> <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Attachment Synchronize
[attachment_unindex_content](attachment_unindex_content/) | 18.0.1.0.0 | <a href='https://github.com/moylop260'><img src='https://github.com/moylop260.png' width='32' height='32' style='border-radius:50%;' alt='moylop260'/></a> <a href='https://github.com/ebirbe'><img src='https://github.com/ebirbe.png' width='32' height='32' style='border-radius:50%;' alt='ebirbe'/></a> <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Disable indexing of attachments
[auditlog](auditlog/) | 18.0.2.0.9 |  | Audit Log
[auto_backup](auto_backup/) | 18.0.1.0.1 |  | Backups database
[autovacuum_message_attachment](autovacuum_message_attachment/) | 18.0.1.0.1 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Automatically delete old mail messages and attachments
[base_conditional_image](base_conditional_image/) | 18.0.1.0.0 |  | This module extends the functionality to support conditional images
[base_cron_exclusion](base_cron_exclusion/) | 18.0.1.0.1 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | Allow you to select scheduled actions that should not run simultaneously.
[base_exception](base_exception/) | 18.0.1.1.1 | <a href='https://github.com/hparfr'><img src='https://github.com/hparfr.png' width='32' height='32' style='border-radius:50%;' alt='hparfr'/></a> <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> | This module provide an abstract model to manage customizable exceptions to be applied on different models (sale order, invoice, ...)
[base_fontawesome](base_fontawesome/) | 18.0.2.0.0 |  | Up to date Fontawesome resources.
[base_fontawesome_web_editor](base_fontawesome_web_editor/) | 18.0.1.0.0 |  | Integration between base_fontawesome and web_editor for FontAwesome >= 6.7.2 support.
[base_force_record_noupdate](base_force_record_noupdate/) | 18.0.1.0.0 |  | Manually force noupdate=True on models
[base_m2m_custom_field](base_m2m_custom_field/) | 18.0.1.0.0 |  | Customizations of Many2many
[base_model_restrict_update](base_model_restrict_update/) | 18.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Update Restrict Model
[base_multi_image](base_multi_image/) | 18.0.1.0.0 |  | Allow multiple images for database objects
[base_name_search_improved](base_name_search_improved/) | 18.0.1.1.1 |  | Friendlier search when typing in relation fields
[base_partition](base_partition/) | 18.0.1.0.1 |  | Base module that provide the partition method on all models
[base_remote](base_remote/) | 18.0.1.0.0 |  | Remote Base
[base_search_fuzzy](base_search_fuzzy/) | 18.0.2.0.0 |  | Fuzzy search with the PostgreSQL trigram extension
[base_sequence_option](base_sequence_option/) | 18.0.1.0.1 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Alternative sequence options for specific models
[base_sparse_field_list_support](base_sparse_field_list_support/) | 18.0.1.0.0 |  | add list support to convert_to_cache()
[base_technical_user](base_technical_user/) | 18.0.1.0.1 |  | Add a technical user parameter on the company
[base_temporary_action](base_temporary_action/) | 18.0.1.0.0 |  | This addon allows to create temporary actions
[base_time_window](base_time_window/) | 18.0.1.1.1 |  | Base model to handle time windows
[base_view_inheritance_extension](base_view_inheritance_extension/) | 18.0.1.0.2 |  | Adds more operators for view inheritance
[bus_alt_connection](bus_alt_connection/) | 18.0.1.0.0 |  | Needed when using PgBouncer as a connection pooler
[database_autovacuum_tuning](database_autovacuum_tuning/) | 18.0.1.0.1 |  | Scheduled checks for Odoo autovacuum thresholds and scale factors
[database_cleanup](database_cleanup/) | 18.0.1.0.2 |  | Database cleanup
[database_size](database_size/) | 18.0.1.0.2 |  | Database Size
[dbfilter_from_header](dbfilter_from_header/) | 18.0.1.0.0 |  | Filter databases with HTTP headers
[excel_import_export](excel_import_export/) | 18.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Base module for developing Excel import/export/report
[fetchmail_attach_from_folder](fetchmail_attach_from_folder/) | 18.0.2.0.0 | <a href='https://github.com/NL66278'><img src='https://github.com/NL66278.png' width='32' height='32' style='border-radius:50%;' alt='NL66278'/></a> | Attach mails in an IMAP folder to existing objects
[fetchmail_notify_error_to_sender](fetchmail_notify_error_to_sender/) | 18.0.1.0.0 |  | If fetching mails gives error, send an email to sender
[field_vector](field_vector/) | 18.0.1.0.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | New specialized field to store vector data
[html_text](html_text/) | 18.0.1.0.0 |  | Generate excerpts from any HTML field
[iap_alternative_provider](iap_alternative_provider/) | 18.0.1.0.0 | <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> | Base module for providing alternative provider for iap apps
[jsonifier](jsonifier/) | 18.0.1.1.1 |  | JSON-ify data for all models
[mail_cleanup](mail_cleanup/) | 18.0.1.0.2 |  | Mark as read or delete mails after a set time
[mail_template_attachment_per_lang](mail_template_attachment_per_lang/) | 18.0.1.0.0 |  | Set language specific attachments on mail templates.
[module_analysis](module_analysis/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add analysis tools regarding installed modules to know which installed modules comes from Odoo Core, OCA, or are custom modules
[module_auto_update](module_auto_update/) | 18.0.1.0.2 |  | Automatically update Odoo modules
[module_change_auto_install](module_change_auto_install/) | 18.0.1.0.3 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Customize auto installables modules by configuration
[odoo_test_xmlrunner](odoo_test_xmlrunner/) | 18.0.1.0.0 |  | This module override Odoo testing method to run them with xmlrunner tool.
[onchange_helper](onchange_helper/) | 18.0.1.0.1 |  | Technical module that ease execution of onchange in Python code
[rpc_helper](rpc_helper/) | 18.0.1.0.2 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Helpers for disabling RPC calls
[scheduler_error_mailer](scheduler_error_mailer/) | 18.0.1.0.0 |  | Scheduler Error Mailer
[sentry](sentry/) | 18.0.1.0.4 | <a href='https://github.com/barsi'><img src='https://github.com/barsi.png' width='32' height='32' style='border-radius:50%;' alt='barsi'/></a> <a href='https://github.com/naglis'><img src='https://github.com/naglis.png' width='32' height='32' style='border-radius:50%;' alt='naglis'/></a> <a href='https://github.com/versada'><img src='https://github.com/versada.png' width='32' height='32' style='border-radius:50%;' alt='versada'/></a> <a href='https://github.com/moylop260'><img src='https://github.com/moylop260.png' width='32' height='32' style='border-radius:50%;' alt='moylop260'/></a> <a href='https://github.com/fernandahf'><img src='https://github.com/fernandahf.png' width='32' height='32' style='border-radius:50%;' alt='fernandahf'/></a> | Report Odoo errors to Sentry
[sequence_python](sequence_python/) | 18.0.1.0.0 |  | Calculate a sequence number from a Python expression
[session_db](session_db/) | 18.0.1.0.1 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Store sessions in DB
[test_auditlog](test_auditlog/) | 18.0.1.0.3 |  | Additional unit tests for Audit Log based on accounting models
[test_base_time_window](test_base_time_window/) | 18.0.1.0.0 |  | Test Base model to handle time windows
[tracking_manager](tracking_manager/) | 18.0.1.1.0 | <a href='https://github.com/Kev-Roche'><img src='https://github.com/Kev-Roche.png' width='32' height='32' style='border-radius:50%;' alt='Kev-Roche'/></a> <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> | This module tracks all fields of a model, including one2many and many2many ones.
[tracking_manager_domain](tracking_manager_domain/) | 18.0.1.0.1 | <a href='https://github.com/CRogos'><img src='https://github.com/CRogos.png' width='32' height='32' style='border-radius:50%;' alt='CRogos'/></a> | This module extends the tracking manager to allow to define a domain on fields to track changes only when certain conditions apply.
[upgrade_analysis](upgrade_analysis/) | 18.0.1.4.5 | <a href='https://github.com/StefanRijnhart'><img src='https://github.com/StefanRijnhart.png' width='32' height='32' style='border-radius:50%;' alt='StefanRijnhart'/></a> <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Performs a difference analysis between modules installed on two different Odoo instances

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/server-ux


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-ux&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/server-ux/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/server-ux/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/server-ux/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/server-ux/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/server-ux/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-ux)
[![Translation Status](https://translation.odoo-community.org/widgets/server-ux-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-ux-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# server-ux

server-ux

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[announcement](announcement/) | 18.0.1.0.1 |  | Notify internal users about relevant organization stuff
[barcode_action](barcode_action/) | 18.0.1.0.0 |  | Allows to use barcodes as a launcher
[base_cancel_confirm](base_cancel_confirm/) | 18.0.1.0.2 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Base Cancel Confirm
[base_custom_filter](base_custom_filter/) | 18.0.1.0.0 | <a href='https://github.com/AshishHirapara'><img src='https://github.com/AshishHirapara.png' width='32' height='32' style='border-radius:50%;' alt='AshishHirapara'/></a> <a href='https://github.com/ForgeFlow'><img src='https://github.com/ForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ForgeFlow'/></a> | Add custom filters in standard filters and group by dropdowns
[base_export_manager](base_export_manager/) | 18.0.1.0.2 |  | Manage model export profiles
[base_import_security_group](base_import_security_group/) | 18.0.1.0.0 |  | Group-based permissions for importing CSV files
[base_menu_visibility_restriction](base_menu_visibility_restriction/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Restrict (with groups) menu visibilty
[base_optional_quick_create](base_optional_quick_create/) | 18.0.1.0.1 |  | Avoid "quick create" on m2o fields, on a "by model" basis
[base_revision](base_revision/) | 18.0.1.0.2 |  | Keep track of revised document
[base_search_custom_field_filter](base_search_custom_field_filter/) | 18.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Add custom filters for fields via UI
[base_substate](base_substate/) | 18.0.1.0.2 |  | Base Sub State
[base_technical_features](base_technical_features/) | 18.0.1.0.2 |  | Access to technical features without activating debug mode
[base_tier_validation](base_tier_validation/) | 18.0.3.4.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Implement a validation process based on tiers.
[base_tier_validation_confirm_auth](base_tier_validation_confirm_auth/) | 18.0.1.0.0 |  | Authentication confirmation for base tiers.
[base_tier_validation_correction](base_tier_validation_correction/) | 18.0.1.0.1 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Correct tier.review data after it has been created.
[base_tier_validation_formula](base_tier_validation_formula/) | 18.0.1.0.1 |  | Formulas for Base tier validation
[base_tier_validation_forward](base_tier_validation_forward/) | 18.0.2.0.2 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Forward option for base tiers
[base_tier_validation_server_action](base_tier_validation_server_action/) | 18.0.1.0.1 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Add option to call server action when a tier is validated
[base_warn_option](base_warn_option/) | 18.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Add Options to Warn Messages
[chained_swapper](chained_swapper/) | 18.0.1.0.0 |  | Chained Swapper
[date_range](date_range/) | 18.0.5.0.1 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Manage all kind of date range
[date_range_account](date_range_account/) | 18.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add Date Range menu entry in Invoicing app
[default_multi_user](default_multi_user/) | 18.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Allows to share user-defined defaults among several users.
[developer_menu](developer_menu/) | 18.0.1.1.0 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Menu Shortcut for developer usage
[document_quick_access](document_quick_access/) | 18.0.1.0.0 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Document quick access
[document_quick_access_folder_auto_classification](document_quick_access_folder_auto_classification/) | 18.0.1.0.1 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Auto classification of Documents after reading a QR
[filter_multi_user](filter_multi_user/) | 18.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Allows to share user-defined filters filters among several users.
[mail_message_destiny_link_template](mail_message_destiny_link_template/) | 18.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Mail template to show destiny records in chatter.
[multi_step_wizard](multi_step_wizard/) | 18.0.1.0.1 |  | Multi-Steps Wizards
[sequence_check_digit](sequence_check_digit/) | 18.0.1.1.0 |  | Adds a check digit on sequences
[sequence_reset_period](sequence_reset_period/) | 18.0.1.0.0 |  | Auto-generate yearly/monthly/weekly/daily sequence period ranges
[server_action_mass_edit](server_action_mass_edit/) | 18.0.1.1.3 |  | Mass Editing
[server_action_mass_edit_onchange](server_action_mass_edit_onchange/) | 18.0.1.1.1 |  | Extension of server_action_mass_edit
[template_content_swapper](template_content_swapper/) | 18.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/AungKoKoLin1997'><img src='https://github.com/AungKoKoLin1997.png' width='32' height='32' style='border-radius:50%;' alt='AungKoKoLin1997'/></a> | Template Content Swapper

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/shift-planning


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# shift-planning
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/shift-planning&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/shift-planning/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/shift-planning/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/shift-planning/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/shift-planning/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/shift-planning/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/shift-planning)
[![Translation Status](https://translation.odoo-community.org/widgets/shift-planning-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/shift-planning-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

shift-planning

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[hr_shift](hr_shift/) | 18.0.1.1.0 |  | Define shifts for employees

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/shopfloor-app


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/shopfloor-app&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/shopfloor-app/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/shopfloor-app/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/shopfloor-app/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/shopfloor-app/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/shopfloor-app/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/shopfloor-app)
[![Translation Status](https://translation.odoo-community.org/widgets/shopfloor-app-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/shopfloor-app-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# shopfloor-app

shopfloor-app

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[shopfloor_base](shopfloor_base/) | 18.0.1.1.0 | <a href='https://github.com/guewen'><img src='https://github.com/guewen.png' width='32' height='32' style='border-radius:50%;' alt='guewen'/></a> <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Core module for creating mobile apps
[shopfloor_example](shopfloor_example/) | 18.0.1.0.0 |  | Show how to customize the Shopfloor app frontend.
[shopfloor_mobile_base](shopfloor_mobile_base/) | 18.0.1.2.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Mobile frontend for WMS Shopfloor app
[shopfloor_mobile_base_auth_api_key](shopfloor_mobile_base_auth_api_key/) | 18.0.1.0.0 |  | Provides authentication via API key to Shopfloor base mobile app
[shopfloor_rest_log](shopfloor_rest_log/) | 18.0.1.1.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Integrate rest_log into Shopfloor app
[shopfloor_workstation](shopfloor_workstation/) | 18.0.1.0.0 |  | Manage workstation within a shopfloor application
[shopfloor_workstation_label_printer](shopfloor_workstation_label_printer/) | 18.0.1.0.0 |  | Adds a label printer configuration to shopfloor workstation.
[shopfloor_workstation_mobile](shopfloor_workstation_mobile/) | 18.0.1.0.0 |  | Shopfloor mobile app integration for workstation

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/sign


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sign&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/sign/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/sign/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/sign/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/sign/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/sign/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/sign)
[![Translation Status](https://translation.odoo-community.org/widgets/sign-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sign-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# sign

sign

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[agreement_sign_oca](agreement_sign_oca/) | 18.0.1.0.0 | <a href='https://github.com/miquelalzanillas'><img src='https://github.com/miquelalzanillas.png' width='32' height='32' style='border-radius:50%;' alt='miquelalzanillas'/></a> | Agreement Sign Oca
[project_task_sign_oca](project_task_sign_oca/) | 18.0.1.0.0 | <a href='https://github.com/WesleyOliveira98'><img src='https://github.com/WesleyOliveira98.png' width='32' height='32' style='border-radius:50%;' alt='WesleyOliveira98'/></a> | Project Task Sign Oca
[sign_oca](sign_oca/) | 18.0.1.4.2 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Allow to sign documents inside Odoo CE

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/social


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/social&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/social/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/social/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/social/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/social/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/social/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/social)
[![Translation Status](https://translation.odoo-community.org/widgets/social-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/social-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# social

social

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[fetchmail_thread_default](fetchmail_thread_default/) | 18.0.1.0.0 |  | Post unkonwn messages to an existing thread
[mail_activity_cancel_tracking](mail_activity_cancel_tracking/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Mail Activity Cancel Tracking
[mail_activity_unlink_log](mail_activity_unlink_log/) | 18.0.1.0.0 |  | Leave a message when an activity is unlinked
[mail_gateway](mail_gateway/) | 18.0.1.0.9 |  | Base module for gateway communications
[mail_gateway_telegram](mail_gateway_telegram/) | 18.0.1.0.0 |  | Set a gateway for telegram
[mail_gateway_telegram_standalone](mail_gateway_telegram_standalone/) | 18.0.1.0.0 |  | Generic Telegram API connector
[mail_gateway_whatsapp](mail_gateway_whatsapp/) | 18.0.2.1.4 |  | Set a gateway for WhatsApp
[mail_notification_with_history](mail_notification_with_history/) | 18.0.1.0.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Add the previous chatter discussion into new email notifications.
[mail_thread_create_nolog](mail_thread_create_nolog/) | 18.0.1.0.2 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Display a fake (non-stored) create log in the chatter.
[res_company_mastodon_link](res_company_mastodon_link/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add mastodon url at company model

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/spreadsheet


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/spreadsheet&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/spreadsheet/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/spreadsheet/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/spreadsheet/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/spreadsheet/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/spreadsheet/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/spreadsheet)
[![Translation Status](https://translation.odoo-community.org/widgets/spreadsheet-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/spreadsheet-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# spreadsheet

spreadsheet

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[spreadsheet_dashboard_oca](spreadsheet_dashboard_oca/) | 18.0.1.1.0 |  | Use OCA Spreadsheets on dashboards configuration
[spreadsheet_dashboard_purchase_oca](spreadsheet_dashboard_purchase_oca/) | 18.0.1.0.0 |  | Spreadsheet dashboard for vendors
[spreadsheet_dashboard_purchase_stock_oca](spreadsheet_dashboard_purchase_stock_oca/) | 18.0.1.0.0 |  | Spreadsheet dashboard for purchases
[spreadsheet_oca](spreadsheet_oca/) | 18.0.1.3.1 |  | Allow to edit spreadsheets

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/stock-logistics-availability


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# Stock Availability
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-availability&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-availability/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-availability/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/stock-logistics-availability/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-availability/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-availability/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-availability)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-availability-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-availability-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

This repository contains modules to provide more information about product stock availability in terms of quantities

Are you looking for modules related to logistics? Or would like to contribute
to? There are many repositories with specific purposes. Have a look at this
[README](https://github.com/OCA/wms/blob/18.0/README.md).

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[stock_available](stock_available/) | 18.0.1.0.0 |  | Stock available to promise
[stock_available_base_exclude_location](stock_available_base_exclude_location/) | 18.0.1.0.2 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Base module to exclude locations for product available quantities
[stock_available_immediately](stock_available_immediately/) | 18.0.1.0.0 |  | Ignore planned receptions in quantity available to promise
[stock_available_immediately_exclude_location](stock_available_immediately_exclude_location/) | 18.0.1.0.0 |  | Exclude locations from immediately usable quantity
[stock_available_location_get_domain](stock_available_location_get_domain/) | 18.0.1.0.0 |  | This is a technical helper module in order to reuse the standard _get_domain_locations() function for locations and not quants
[stock_available_unreserved](stock_available_unreserved/) | 18.0.2.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Quantity of stock available for immediate use
[stock_free_quantity](stock_free_quantity/) | 18.0.1.1.0 |  | Stock Free Quantity
[stock_picking_product_availability_inline](stock_picking_product_availability_inline/) | 18.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Show product availability in product drop-down of picking form view.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/stock-logistics-barcode


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-barcode&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-barcode/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-barcode/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/stock-logistics-barcode/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-barcode/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-barcode/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-barcode)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-barcode-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-barcode-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Stock Barcode

Product and product packaging barcodes

Are you looking for modules related to logistics? Or would like to contribute
to? There are many repositories with specific purposes. Have a look at this
[README](https://github.com/OCA/wms/blob/18.0/README.md).

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[barcodes_generator_abstract](barcodes_generator_abstract/) | 18.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Generate Barcodes for Any Models
[barcodes_generator_product](barcodes_generator_product/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Generate Barcodes for Products (Templates and Variants)
[product_multi_barcode](product_multi_barcode/) | 18.0.1.0.1 |  | Multiple barcodes on products
[stock_picking_product_barcode_report](stock_picking_product_barcode_report/) | 18.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | It provides a wizard to select how many barcodes print.
[web_ir_actions_client_scan](web_ir_actions_client_scan/) | 18.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Add an action to scan

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/stock-logistics-interfaces


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-interfaces&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-interfaces/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-interfaces/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/stock-logistics-interfaces/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-interfaces/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-interfaces/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-interfaces)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-interfaces-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-interfaces-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Stock Interfaces

Interfaces to interact with physical devices (vertical lift, measurement device...)

Are you looking for modules related to logistics? Or would like to contribute
to? There are many repositories with specific purposes. Have a look at this
[README](https://github.com/OCA/wms/blob/18.0/README.md).

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[stock_measuring_device](stock_measuring_device/) | 18.0.1.0.0 | <a href='https://github.com/gurneyalex'><img src='https://github.com/gurneyalex.png' width='32' height='32' style='border-radius:50%;' alt='gurneyalex'/></a> | Implement a common interface for measuring and weighing devices
[stock_measuring_device_zippcube](stock_measuring_device_zippcube/) | 18.0.1.0.0 | <a href='https://github.com/gurneyalex'><img src='https://github.com/gurneyalex.png' width='32' height='32' style='border-radius:50%;' alt='gurneyalex'/></a> | Implement interface with Bosche Zippcube devicesfor packaging measurement
[stock_vertical_lift_kardex](stock_vertical_lift_kardex/) | 18.0.1.0.0 |  | Integrate with Kardex Remstar Vertical Lifts

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/stock-logistics-orderpoint


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# Stock Orderpoint
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-orderpoint&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-orderpoint/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-orderpoint/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/stock-logistics-orderpoint/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-orderpoint/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-orderpoint/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-orderpoint)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-orderpoint-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-orderpoint-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Reordering rules

Are you looking for modules related to logistics? Or would like to contribute
to? There are many repositories with specific purposes. Have a look at this
[README](https://github.com/OCA/wms/blob/18.0/README.md).

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[purchase_stock_product_replenish_supplier](purchase_stock_product_replenish_supplier/) | 18.0.1.0.0 |  | Set default supplier in product replenish wizard
[stock_location_orderpoint](stock_location_orderpoint/) | 18.0.1.0.5 | <a href='https://github.com/mt-software-de'><img src='https://github.com/mt-software-de.png' width='32' height='32' style='border-radius:50%;' alt='mt-software-de'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Declare orderpoint on a location allowing to replenish any product with the same criteria.
[stock_orderpoint_default_location](stock_orderpoint_default_location/) | 18.0.1.0.1 |  | This module allows to define a different default location than the stock location
[stock_orderpoint_manual_procurement](stock_orderpoint_manual_procurement/) | 18.0.1.0.0 |  | Allows to create procurement orders from orderpoints instead of relying only on the scheduler.
[stock_orderpoint_move_link](stock_orderpoint_move_link/) | 18.0.1.0.0 |  | Link Reordering rules to stock moves
[stock_orderpoint_mto_as_mts](stock_orderpoint_mto_as_mts/) | 18.0.1.2.0 |  | Materialize need from MTO route through orderpoint
[stock_orderpoint_no_horizon](stock_orderpoint_no_horizon/) | 18.0.1.0.0 |  | Consider all future moves, do not limit horizon to the rule lead days.
[stock_orderpoint_purchase_link](stock_orderpoint_purchase_link/) | 18.0.1.0.0 |  | Link Reordering rules to purchase orders
[stock_orderpoint_uom](stock_orderpoint_uom/) | 18.0.1.0.0 |  | Allows to create procurement orders in the UoM indicated in the orderpoint

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/stock-logistics-putaway


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# Stock Putaway
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-putaway&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-putaway/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-putaway/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/stock-logistics-putaway/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-putaway/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-putaway/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-putaway)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-putaway-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-putaway-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Enhance the way put-aways are computed on move lines for properly storing the products in the stock.

Are you looking for modules related to logistics? Or would like to contribute
to? There are many repositories with specific purposes. Have a look at this
[README](https://github.com/OCA/wms/blob/18.0/README.md).

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[stock_picking_putaway_recompute](stock_picking_putaway_recompute/) | 18.0.1.0.1 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | This module allows to recompute the picking operations putaways if configurations have changed
[stock_putaway_hook](stock_putaway_hook/) | 18.0.1.0.0 |  | Add hooks allowing modules to add more putaway strategies
[stock_putaway_rule_product_handle](stock_putaway_rule_product_handle/) | 18.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | This module allows to show the handle widget on product putaway rules to change the sequence
[stock_storage_type](stock_storage_type/) | 18.0.1.6.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Manage packages and locations storage types
[stock_storage_type_buffer](stock_storage_type_buffer/) | 18.0.1.1.0 |  | Exclude storage locations from put-away if their buffer is full
[stock_storage_type_move_line_qty_picked](stock_storage_type_move_line_qty_picked/) | 18.0.1.0.1 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | stock storage type move line quantity picked
[stock_storage_type_putaway_abc](stock_storage_type_putaway_abc/) | 18.0.1.0.1 |  | Advanced storage strategy ABC for WMS

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/stock-logistics-release-channel


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-release-channel&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-release-channel/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-release-channel/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/stock-logistics-release-channel/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-release-channel/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-release-channel/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-release-channel)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-release-channel-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-release-channel-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Stock Release Channel

Dispatch management. Organize and dispatch work in the warehouse by release channels.

Are you looking for modules related to logistics? Or would like to contribute
to? There are many repositories with specific purposes. Have a look at this
[README](https://github.com/OCA/wms/blob/18.0/README.md).

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[sale_stock_release_channel](sale_stock_release_channel/) | 18.0.1.0.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Sales Stock Release Channel
[sale_stock_release_channel_delivery](sale_stock_release_channel_delivery/) | 18.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Sales Stock Release Channel Delivery
[sale_stock_release_channel_delivery_date](sale_stock_release_channel_delivery_date/) | 18.0.1.0.3 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Compute expected date based on available release channels
[sale_stock_release_channel_delivery_date_plan_shipment_lead_time](sale_stock_release_channel_delivery_date_plan_shipment_lead_time/) | 18.0.1.0.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Sale Stock Release Channel Delivery Date Plan Shipment Lead Time
[stock_release_channel](stock_release_channel/) | 18.0.1.7.1 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/mt-software-de'><img src='https://github.com/mt-software-de.png' width='32' height='32' style='border-radius:50%;' alt='mt-software-de'/></a> | Manage workload in WMS with release channels
[stock_release_channel_auto_release](stock_release_channel_auto_release/) | 18.0.1.0.0 |  | Add an automatic release mode to the release channel
[stock_release_channel_carrier_alternative](stock_release_channel_carrier_alternative/) | 18.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Manage release channel carrier alternative
[stock_release_channel_cutoff](stock_release_channel_cutoff/) | 18.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Add the cutoff time to the release channel
[stock_release_channel_delivery](stock_release_channel_delivery/) | 18.0.1.0.0 |  | Add a carrier selection criteria on the release channel
[stock_release_channel_partner_address](stock_release_channel_partner_address/) | 18.0.1.1.0 |  | Allows defining countries and states filters on channels
[stock_release_channel_partner_delivery_window](stock_release_channel_partner_delivery_window/) | 18.0.1.2.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Allows to define an end date (and time) on a release channel and propagate it to the concerned pickings
[stock_release_channel_plan](stock_release_channel_plan/) | 18.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Manage release channel preparation plan
[stock_release_channel_plan_process_end_time](stock_release_channel_plan_process_end_time/) | 18.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Glue module between release channel plan and process end time
[stock_release_channel_plan_shipment_lead_time](stock_release_channel_plan_shipment_lead_time/) | 18.0.1.0.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Stock release channel plan shipment lead time
[stock_release_channel_process_end_time](stock_release_channel_process_end_time/) | 18.0.1.0.3 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Allows to define an end date (and time) on a release channel and propagate it to the concerned pickings
[stock_release_channel_shipment_advice](stock_release_channel_shipment_advice/) | 18.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Plan shipment advices for ready and released pickings
[stock_release_channel_shipment_lead_time](stock_release_channel_shipment_lead_time/) | 18.0.1.1.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Release channel with shipment lead time
[stock_release_channel_warehouse_calendar](stock_release_channel_warehouse_calendar/) | 18.0.1.0.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Glue module between release channel and warehouse calendar

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/stock-logistics-reporting


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# stock-logistics-reporting
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-reporting&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-reporting/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/stock-logistics-reporting/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-reporting/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-reporting/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-reporting-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-reporting-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Stock Reporting

Are you looking for modules related to logistics? Or would like to contribute
to? There are many repositories with specific purposes. Have a look at this
[README](https://github.com/OCA/wms/blob/18.0/README.md).

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[delivery_line_sale_line_position](delivery_line_sale_line_position/) | 18.0.1.0.0 |  | Adds the sale line position to the delivery report lines
[printing_auto_stock_picking](printing_auto_stock_picking/) | 18.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Printing Auto Stock Picking
[stock_account_valuation_report](stock_account_valuation_report/) | 18.0.1.0.1 |  | Improves logic of the Inventory Valuation Report
[stock_delivery_note](stock_delivery_note/) | 18.0.1.0.0 |  | This module allows to fill in a delivery note that will be displayed on delivery report
[stock_move_delay_report](stock_move_delay_report/) | 18.0.1.0.0 |  | Stock Move Delay Report
[stock_move_pivot_total_price](stock_move_pivot_total_price/) | 18.0.1.0.0 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> | Adds a total price UOM to the stock move pivot view
[stock_move_value_report](stock_move_value_report/) | 18.0.1.0.0 |  | Stock Move Cost Value Report
[stock_picking_batch_report](stock_picking_batch_report/) | 18.0.1.0.0 |  | Stock Picking Batch Report
[stock_picking_comment_template](stock_picking_comment_template/) | 18.0.1.0.0 |  | Comments texts templates on Picking documents
[stock_picking_group_by_partner_by_carrier_sale_line_position](stock_picking_group_by_partner_by_carrier_sale_line_position/) | 18.0.1.0.0 |  | Glue module for sale position and delivery report grouped
[stock_picking_operations_multilang](stock_picking_operations_multilang/) | 18.0.1.0.0 |  | Stock Picking Operations Multilang
[stock_picking_report_custom_description](stock_picking_report_custom_description/) | 18.0.1.0.0 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> | Show moves description in picking reports
[stock_picking_report_delivery_driver](stock_picking_report_delivery_driver/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Delivery Driver info in Stock Picking reports
[stock_picking_report_external_note](stock_picking_report_external_note/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Adds a note in Stock Picking shown on external reports like Delivery Slip
[stock_picking_report_header_repeater](stock_picking_report_header_repeater/) | 18.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Stock Picking Report Header Repeater
[stock_picking_report_incoming_delivery_address](stock_picking_report_incoming_delivery_address/) | 18.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Allow show delivery address in report when picking type is incoming
[stock_picking_report_internal_delivery_address](stock_picking_report_internal_delivery_address/) | 18.0.1.0.0 |  | Show delivery address when picking type is internal
[stock_picking_report_product_sticker](stock_picking_report_product_sticker/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Stock Picking Report - Product Sticker
[stock_picking_report_qty_undelivered](stock_picking_report_qty_undelivered/) | 18.0.1.0.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Print a summary of the undelivered quantity
[stock_picking_report_salesperson](stock_picking_report_salesperson/) | 18.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Salesperson info in Stock Picking reports
[stock_picking_report_summary](stock_picking_report_summary/) | 18.0.1.0.0 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Stock Picking Report Summary
[stock_picking_report_valued](stock_picking_report_valued/) | 18.0.1.1.3 |  | Adding Valued Picking on Delivery Slip report
[stock_picking_report_valued_sale_mrp](stock_picking_report_valued_sale_mrp/) | 18.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allow to summarize the picking related with the selled kits
[stock_portal_lot_list_download](stock_portal_lot_list_download/) | 18.0.1.0.0 |  | Allows portal users to download lot list of delivery pickings in Excel format.
[stock_quantity_history_location](stock_quantity_history_location/) | 18.0.1.0.0 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> <a href='https://github.com/rolandojduartem'><img src='https://github.com/rolandojduartem.png' width='32' height='32' style='border-radius:50%;' alt='rolandojduartem'/></a> | Provides stock quantity by location on past date

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/stock-logistics-request


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-request&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-request/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-request/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/stock-logistics-request/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-request/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-request/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-request)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-request-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-request-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Stock Request

Record needs for products

Are you looking for modules related to logistics? Or would like to contribute
to? There are many repositories with specific purposes. Have a look at this
[README](https://github.com/OCA/wms/blob/18.0/README.md).

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[stock_request](stock_request/) | 18.0.1.1.3 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Internal request for stock
[stock_request_bom](stock_request_bom/) | 18.0.1.0.1 |  | Stock Request with BOM Integration
[stock_request_direction](stock_request_direction/) | 18.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | From or to your warehouse?
[stock_request_kanban](stock_request_kanban/) | 18.0.1.0.1 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Adds a stock request order, and takes stock requests as lines
[stock_request_mrp](stock_request_mrp/) | 18.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Manufacturing request for stock
[stock_request_purchase](stock_request_purchase/) | 18.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Internal request for stock
[stock_request_submit](stock_request_submit/) | 18.0.1.0.0 |  | Add submit state on Stock Requests
[stock_request_tier_validation](stock_request_tier_validation/) | 18.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Extends the functionality of Stock Requests to support a tier validation process.
[stock_return_request](stock_return_request/) | 18.0.1.0.1 |  | Stock Return Request

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/stock-logistics-reservation


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# Stock Reservation
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-reservation&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-reservation/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-reservation/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/stock-logistics-reservation/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-reservation/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-reservation/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-reservation)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-reservation-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-reservation-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Enhance the way products are allocated (virtual reservation) and reserved (rules extending fifo) in the stock.

Are you looking for modules related to logistics? Or would like to contribute
to? There are many repositories with specific purposes. Have a look at this
[README](https://github.com/OCA/wms/blob/18.0/README.md).

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[product_expiry_assign](product_expiry_assign/) | 18.0.1.0.0 |  | Force the reservation of expired lots.
[sale_stock_available_to_promise_release](sale_stock_available_to_promise_release/) | 18.0.2.0.0 |  | Integration between Sales and Available to Promise Release
[sale_stock_available_to_promise_release_dropshipping](sale_stock_available_to_promise_release_dropshipping/) | 18.0.1.0.0 |  | Glue module between sale_stock_available_to_promise_release and stock_dropshipping
[stock_available_to_promise_release](stock_available_to_promise_release/) | 18.0.1.7.0 |  | Release Operations based on available to promise
[stock_available_to_promise_release_carrier_alternative](stock_available_to_promise_release_carrier_alternative/) | 18.0.1.0.1 |  | Advanced selection of preferred shipping methods
[stock_available_to_promise_release_delivery](stock_available_to_promise_release_delivery/) | 18.0.1.0.1 |  | Glue module between release mechanism and delivery.
[stock_available_to_promise_release_dynamic_routing](stock_available_to_promise_release_dynamic_routing/) | 18.0.1.0.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Glue between moves release and dynamic routing
[stock_available_to_promise_release_exclude_location](stock_available_to_promise_release_exclude_location/) | 18.0.1.0.0 |  | Exclude locations from available stock
[stock_move_auto_assign](stock_move_auto_assign/) | 18.0.1.0.1 |  | Try to reserve moves when goods enter in a location
[stock_picking_unreserve_button](stock_picking_unreserve_button/) | 18.0.1.0.0 |  | Stock Picking Unreserve Button
[stock_reserve](stock_reserve/) | 18.0.1.0.0 |  | Stock reservations on products
[stock_reserve_rule](stock_reserve_rule/) | 18.0.1.2.2 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Configure reservation rules by location
[stock_rule_reserve_max_quantity](stock_rule_reserve_max_quantity/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Allows to reserve max available quantity when a move comes from an stock rule

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/stock-logistics-shopfloor


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-shopfloor&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-shopfloor/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-shopfloor/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/stock-logistics-shopfloor/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-shopfloor/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-shopfloor/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-shopfloor)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-shopfloor-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-shopfloor-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Stock Shopfloor

Shopfloor. Warehouse barcode applications to support operators in the warehouse.

Are you looking for modules related to logistics? Or would like to contribute
to? There are many repositories with specific purposes. Have a look at this
[README](https://github.com/OCA/wms/blob/18.0/README.md).

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[shopfloor](shopfloor/) | 18.0.0.14.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | manage warehouse operations with barcode scanners
[shopfloor_batch_automatic_creation](shopfloor_batch_automatic_creation/) | 18.0.1.2.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Create batch transfers for Cluster Picking
[shopfloor_checkout_sync](shopfloor_checkout_sync/) | 18.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Glue module
[shopfloor_cluster_picking_repack](shopfloor_cluster_picking_repack/) | 18.0.1.1.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Build delivery packages at the end of the cluster picking
[shopfloor_dangerous_goods](shopfloor_dangerous_goods/) | 18.0.1.1.0 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Glue Module Between Shopfloor and Stock Dangerous Goods
[shopfloor_dangerous_goods_mobile](shopfloor_dangerous_goods_mobile/) | 18.0.1.1.0 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Glue module between Shopfloor Mobile and Shopfloor Dangerous Goods
[shopfloor_delivery_shipment](shopfloor_delivery_shipment/) | 18.0.1.2.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Manage delivery process with shipment advices
[shopfloor_delivery_shipment_mobile](shopfloor_delivery_shipment_mobile/) | 18.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Frontend for delivery shipment scenario for shopfloor
[shopfloor_gs1](shopfloor_gs1/) | 18.0.1.1.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Integrate GS1 barcode scan into Shopfloor app
[shopfloor_mobile](shopfloor_mobile/) | 18.0.1.5.1 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Mobile frontend for WMS Shopfloor app
[shopfloor_reception](shopfloor_reception/) | 18.0.1.7.2 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Reception scenario for shopfloor
[shopfloor_reception_measuring_device](shopfloor_reception_measuring_device/) | 18.0.1.1.1 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Allows to use measuring devices to measure packagings on the reception
[shopfloor_reception_mobile](shopfloor_reception_mobile/) | 18.0.1.4.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Scenario for receiving products
[shopfloor_reception_package_dimension](shopfloor_reception_package_dimension/) | 18.0.1.0.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Collect Package Dimension from the Reception scenario
[shopfloor_reception_package_dimension_mobile](shopfloor_reception_package_dimension_mobile/) | 18.0.1.0.0 |  | Mobile part for handling dimension on storage package.
[shopfloor_reception_packaging_dimension](shopfloor_reception_packaging_dimension/) | 18.0.1.4.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Collect Packaging Dimension from the Reception scenario
[shopfloor_reception_packaging_dimension_mobile](shopfloor_reception_packaging_dimension_mobile/) | 18.0.1.1.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Frontend for the packaging dimension on reception scenario
[shopfloor_reception_vendor_packaging](shopfloor_reception_vendor_packaging/) | 18.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Manage shopfloor reception behavior for vendor packaging
[shopfloor_single_product_transfer](shopfloor_single_product_transfer/) | 18.0.1.2.0 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Move an item from one location to another.
[shopfloor_single_product_transfer_mobile](shopfloor_single_product_transfer_mobile/) | 18.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Mobile frontend for single product transfer scenario
[shopfloor_vendor_packaging](shopfloor_vendor_packaging/) | 18.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Manage shopfloor behavior for vendor packaging

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/stock-logistics-tracking


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-tracking&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-tracking/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-tracking/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/stock-logistics-tracking/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-tracking/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-tracking/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-tracking)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-tracking-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-tracking-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Stock Tracking

Enhance packages (stock.quant.package).

Are you looking for modules related to logistics? Or would like to contribute
to? There are many repositories with specific purposes. Have a look at this
[README](https://github.com/OCA/wms/blob/18.0/README.md).

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[internal_stock_quant_package](internal_stock_quant_package/) | 18.0.1.1.0 |  | This module allows to declare internal stock quant package
[stock_quant_package_archive](stock_quant_package_archive/) | 18.0.1.0.0 |  | Allow to archive packages
[stock_quant_package_dimension](stock_quant_package_dimension/) | 18.0.1.0.1 |  | Use dimensions on packages
[stock_quant_package_product_packaging](stock_quant_package_product_packaging/) | 18.0.1.3.0 |  | Use product packagings on packages

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/stock-logistics-transport


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-transport&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-transport/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-transport/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/stock-logistics-transport/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-transport/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-transport/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-transport)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-transport-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-transport-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Stock Transport

Manage incoming and outgoing transports.

Are you looking for modules related to logistics? Or would like to contribute
to? There are many repositories with specific purposes. Have a look at this
[README](https://github.com/OCA/wms/blob/18.0/README.md).


<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[printing_auto_shipment_advice](printing_auto_shipment_advice/) | 18.0.1.0.2 |  | Printing Auto Shipment Advice
[shipment_advice](shipment_advice/) | 18.0.1.2.4 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Manage your (un)loading process through shipment advices.
[shipment_advice_planner](shipment_advice_planner/) | 18.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | This module is used to plan ready transfers in shipment advices.
[stock_depot](stock_depot/) | 18.0.1.0.0 |  | This module allows users to manage partners stock depots.
[stock_dock](stock_dock/) | 18.0.1.1.0 |  | Manage the loading docks of your warehouse.
[stock_location_address](stock_location_address/) | 18.0.1.0.0 |  | Adds an address on locations
[stock_location_address_purchase](stock_location_address_purchase/) | 18.0.1.0.0 |  | Uses the location address on purchases
[tms](tms/) | 18.0.1.1.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/santiagordz'><img src='https://github.com/santiagordz.png' width='32' height='32' style='border-radius:50%;' alt='santiagordz'/></a> <a href='https://github.com/EdgarRetes'><img src='https://github.com/EdgarRetes.png' width='32' height='32' style='border-radius:50%;' alt='EdgarRetes'/></a> | Manage Vehicles, Drivers, Routes and Trips

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/stock-logistics-warehouse


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-warehouse&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-warehouse/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-warehouse/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/stock-logistics-warehouse/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-warehouse/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-warehouse/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-warehouse)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-warehouse-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-warehouse-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Stock Warehouse

Extend the stock related models (warehouse, location, picking, move...) but without impact flows and processes. It's mainly adding fields or buttons.

Are you looking for modules related to logistics? Or would like to contribute
to? There are many repositories with specific purposes. Have a look at this
[README](https://github.com/OCA/wms/blob/18.0/README.md).

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_move_line_stock_info](account_move_line_stock_info/) | 18.0.1.0.0 |  | Account Move Line Stock Info
[procurement_auto_create_group](procurement_auto_create_group/) | 18.0.1.0.1 |  | Allows to configure the system to propose automatically new procurement groups during the procurement run.
[product_route_profile](product_route_profile/) | 18.0.1.0.0 | <a href='https://github.com/Kev-Roche'><img src='https://github.com/Kev-Roche.png' width='32' height='32' style='border-radius:50%;' alt='Kev-Roche'/></a> | Add Route profile concept on product
[stock_archive_constraint](stock_archive_constraint/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Stock archive constraint
[stock_change_qty_reason](stock_change_qty_reason/) | 18.0.1.0.0 |  | Stock Quantity Change Reason
[stock_cycle_count](stock_cycle_count/) | 18.0.1.0.3 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Adds the capability to schedule cycle counts in a warehouse through different rules defined by the user.
[stock_demand_estimate](stock_demand_estimate/) | 18.0.1.1.0 |  | Allows to create demand estimates.
[stock_demand_estimate_matrix](stock_demand_estimate_matrix/) | 18.0.1.0.0 |  | Allows to create demand estimates.
[stock_inventory](stock_inventory/) | 18.0.1.1.2 |  | Allows to do an easier follow up of the Inventory Adjustments
[stock_inventory_count_to_zero](stock_inventory_count_to_zero/) | 18.0.1.0.0 |  | Request an inventory count filling the quantities to zero as default
[stock_inventory_discrepancy](stock_inventory_discrepancy/) | 18.0.1.1.0 |  | Adds the capability to show the discrepancy of every line in an inventory and to block the inventory validation when the discrepancy is over a user defined threshold.
[stock_inventory_lockdown](stock_inventory_lockdown/) | 18.0.1.0.1 |  | Lock down stock locations during inventories.
[stock_inventory_preparation_filter](stock_inventory_preparation_filter/) | 18.0.1.0.0 |  | More filters for inventory adjustments
[stock_inventory_verification_request](stock_inventory_verification_request/) | 18.0.1.2.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Adds the capability to request a Slot Verification when a inventory is Pending to Approve
[stock_location_bin_name](stock_location_bin_name/) | 18.0.1.0.1 |  | Compute bin stock location name automatically
[stock_location_children](stock_location_children/) | 18.0.1.0.0 |  | Add relation between stock location and all its children
[stock_location_empty](stock_location_empty/) | 18.0.1.0.0 |  | Adds a filter for empty stock location
[stock_location_fill_state](stock_location_fill_state/) | 18.0.1.1.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | This module allows to identify the fill state of stock locations
[stock_location_fill_state_qty_picked](stock_location_fill_state_qty_picked/) | 18.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Glue module between stock_location_fill_state and stock_move_line_qty_picked
[stock_location_is_sublocation](stock_location_is_sublocation/) | 18.0.1.0.0 |  | Add method to check stock location is sublocation
[stock_location_lockdown](stock_location_lockdown/) | 18.0.1.0.0 |  | Prevent to add stock on locked locations
[stock_location_pending_move](stock_location_pending_move/) | 18.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | This module allows to show pending stock moves (outgoing and incoming) on a stock location
[stock_location_position](stock_location_position/) | 18.0.1.0.0 |  | Add coordinate attributes on stock location.
[stock_location_tray](stock_location_tray/) | 18.0.1.0.0 |  | Organize a location as a matrix of cells
[stock_location_zone](stock_location_zone/) | 18.0.1.0.0 |  | Classify locations with zones.
[stock_lot_catalog](stock_lot_catalog/) | 18.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Stock Lot Catalog
[stock_lot_catalog_condition](stock_lot_catalog_condition/) | 18.0.1.1.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Stock Lot Catalog Condition
[stock_lot_catalog_sale](stock_lot_catalog_sale/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Sale Stock Lot Catalog
[stock_lot_catalog_warehouse](stock_lot_catalog_warehouse/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Stock Lot Catalog Warehouse
[stock_lot_condition](stock_lot_condition/) | 18.0.1.1.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Stock Lot Condition
[stock_lot_image](stock_lot_image/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Stock Lot Image
[stock_lot_warehouse](stock_lot_warehouse/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Stock Lot Warehouse
[stock_move_common_dest](stock_move_common_dest/) | 18.0.1.0.1 |  | Adds field for common destination moves
[stock_move_line_lot_link](stock_move_line_lot_link/) | 18.0.1.0.0 |  | Display Lot/SN column on Detailed Operations to allow navigation.
[stock_move_line_reference_link](stock_move_line_reference_link/) | 18.0.1.0.0 |  | Add link in stock move line references.
[stock_move_location](stock_move_location/) | 18.0.1.0.1 |  | This module allows to move all stock in a stock location to an other one.
[stock_move_location_purchase_uom](stock_move_location_purchase_uom/) | 18.0.1.0.0 |  | This module 'glues' the modules stock_move_location and stock_move_purchase_uom.
[stock_move_packaging_qty](stock_move_packaging_qty/) | 18.0.1.2.1 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Add packaging fields in the stock moves
[stock_move_purchase_uom](stock_move_purchase_uom/) | 18.0.1.1.2 |  | Allow to use the purchase UoM in a stock move
[stock_move_reset_quantity](stock_move_reset_quantity/) | 18.0.1.0.0 |  | Reset quantity to zero
[stock_package_type_volume](stock_package_type_volume/) | 18.0.1.0.0 |  | Compute volume of a package type
[stock_packaging_calculator](stock_packaging_calculator/) | 18.0.2.0.0 |  | Compute product quantity to pick by packaging
[stock_picking_batch_packaging_qty](stock_picking_batch_packaging_qty/) | 18.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Add packaging fields in stock picking batch
[stock_picking_commercial_partner](stock_picking_commercial_partner/) | 18.0.1.0.0 |  | Add Commercial Partner on the Stock Picking
[stock_picking_completion_info](stock_picking_completion_info/) | 18.0.1.0.0 |  | Display on current document completion information according to next operations
[stock_picking_procure_method](stock_picking_procure_method/) | 18.0.1.0.0 |  | Allows to force the procurement method from the picking
[stock_picking_product_assortment](stock_picking_product_assortment/) | 18.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Stock Picking Product Assortment
[stock_picking_show_linked](stock_picking_show_linked/) | 18.0.1.0.0 |  | This addon allows to easily access related pickings (in the case of chained routes) through a button in the parent picking view.
[stock_picking_stage](stock_picking_stage/) | 18.0.1.0.0 | <a href='https://github.com/imlopes'><img src='https://github.com/imlopes.png' width='32' height='32' style='border-radius:50%;' alt='imlopes'/></a> | Stock Picking Stages
[stock_picking_supplier_ref](stock_picking_supplier_ref/) | 18.0.1.1.0 |  | Adds a supplier reference field inside supplier's pickings and allows search for this reference.
[stock_picking_volume](stock_picking_volume/) | 18.0.1.1.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Compute volume information on stock moves and pickings
[stock_picking_volume_packaging](stock_picking_volume_packaging/) | 18.0.1.0.0 |  | Use volume information on potential product packaging to compute the volume of a stock.move
[stock_product_qty_by_packaging](stock_product_qty_by_packaging/) | 18.0.1.0.1 |  | Compute product quantity to pick by packaging
[stock_putaway_product_template](stock_putaway_product_template/) | 18.0.1.0.1 | <a href='https://github.com/kevinkhao'><img src='https://github.com/kevinkhao.png' width='32' height='32' style='border-radius:50%;' alt='kevinkhao'/></a> <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> | Add product template in putaway strategies from the product view
[stock_quant_cost_info](stock_quant_cost_info/) | 18.0.1.0.0 |  | Shows the cost of the quants
[stock_quant_reservation_info](stock_quant_reservation_info/) | 18.0.1.0.0 |  | Allows to see the reserved info of Products
[stock_quant_reservation_info_mrp](stock_quant_reservation_info_mrp/) | 18.0.1.0.0 |  | Allows to see the manufacturing order related to the reserved info of Products
[stock_restrict_immediate_adjustment](stock_restrict_immediate_adjustment/) | 18.0.1.0.0 |  | Restrict immediate stock adjustments from Stock On Hand view
[stock_route_location_source](stock_route_location_source/) | 18.0.1.0.1 |  | Add method to get source location of Inventory Routes
[stock_route_mto](stock_route_mto/) | 18.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Allows to identify MTO routes through a checkbox and availability to filter them.
[stock_secondary_unit](stock_secondary_unit/) | 18.0.1.0.0 |  | Get product quantities in a secondary unit
[stock_storage_category_capacity_name](stock_storage_category_capacity_name/) | 18.0.1.0.1 |  | Allows to have a better display name for Stock Storage Category Capacity model
[stock_valuation_layer_inventory_filter](stock_valuation_layer_inventory_filter/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> | Allows to filter Inventory Adjustments on Stock Valuation Layers
[stock_vertical_lift](stock_vertical_lift/) | 18.0.1.3.1 |  | Provides the core for integration with Vertical Lifts
[stock_vertical_lift_empty_tray_check](stock_vertical_lift_empty_tray_check/) | 18.0.1.0.0 |  | Checks if the tray is actually empty.
[stock_vertical_lift_packaging_level](stock_vertical_lift_packaging_level/) | 18.0.1.0.0 |  | Provides integration with Vertical Lifts and packaging levels
[stock_vertical_lift_qty_by_packaging](stock_vertical_lift_qty_by_packaging/) | 18.0.1.0.0 |  | Glue module for `stock_product_qty_by_packaging` and `stock_vertical_lift`.
[stock_vertical_lift_server_env](stock_vertical_lift_server_env/) | 18.0.1.0.0 |  | Server Environment layer for Vertical Lift
[stock_vertical_lift_storage_type](stock_vertical_lift_storage_type/) | 18.0.1.0.0 |  | Compatibility layer for storage types on vertical lifts
[stock_vlm_mgmt](stock_vlm_mgmt/) | 18.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Light self contained alternative for VLM integrations
[stock_vlm_mgmt_kardex](stock_vlm_mgmt_kardex/) | 18.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Light alternative for Kardex VLM integrations
[stock_vlm_mgmt_modula](stock_vlm_mgmt_modula/) | 18.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Light alternative for Modula VLM integrations
[stock_warehouse_calendar](stock_warehouse_calendar/) | 18.0.1.1.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> | Adds a calendar to the Warehouse
[stock_warehouse_out_pull](stock_warehouse_out_pull/) | 18.0.1.0.2 |  | Restore delivery pull rules as in Odoo <= 17.0
[stock_warehouse_resupply_route_push](stock_warehouse_resupply_route_push/) | 18.0.1.0.1 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Use push rules for resupply from other warehouse routes.
[stock_warehouse_security](stock_warehouse_security/) | 18.0.1.0.0 | <a href='https://github.com/petrus-v'><img src='https://github.com/petrus-v.png' width='32' height='32' style='border-radius:50%;' alt='petrus-v'/></a> | Restrict user access in multi-warehouse environment

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/stock-logistics-workflow


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-workflow&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-workflow/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-workflow/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/stock-logistics-workflow/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-logistics-workflow/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-workflow/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-workflow)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-workflow-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-workflow-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Stock Workflow

Enhance the way flows and processes are working. Find here modules that do not have their place in the other more specialized repositories.

Are you looking for modules related to logistics? Or would like to contribute
to? There are many repositories with specific purposes. Have a look at this
[README](https://github.com/OCA/wms/blob/18.0/README.md).

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[delivery_procurement_group_carrier](delivery_procurement_group_carrier/) | 18.0.1.0.3 |  | Delivery Procurement Group Carrier
[delivery_total_weight_from_packaging](delivery_total_weight_from_packaging/) | 18.0.1.1.0 |  | Include packaging weight on move, transfer and package.
[procurement_auto_create_group_carrier](procurement_auto_create_group_carrier/) | 18.0.1.0.0 |  | Procurement Auto Create Group Carrier
[product_cost_price_avco_sync](product_cost_price_avco_sync/) | 18.0.1.0.0 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Set product cost price from updated moves
[product_customerinfo_picking](product_customerinfo_picking/) | 18.0.1.0.0 |  | This module makes the product customer code visible in the stock moves of a picking.
[purchase_stock_picking_invoice_link](purchase_stock_picking_invoice_link/) | 18.0.2.0.0 |  | Adds link between purchases, pickings and invoices
[sale_line_returned_qty](sale_line_returned_qty/) | 18.0.1.0.0 |  | Track returned quantity of sale order lines.
[sale_line_returned_qty_mrp](sale_line_returned_qty_mrp/) | 18.0.1.0.0 |  | Track returned quantity of sale order lines for BoM products.
[sale_order_global_stock_route](sale_order_global_stock_route/) | 18.0.1.0.0 |  | Add the possibility to choose one warehouse path for an order
[sale_stock_picking_invoice_link](sale_stock_picking_invoice_link/) | 18.0.1.0.0 |  | Adds link between pickings and invoices
[scrap_reason_code](scrap_reason_code/) | 18.0.1.0.1 | <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> | Reason code for scrapping
[stock_account_product_run_fifo_hook](stock_account_product_run_fifo_hook/) | 18.0.1.0.1 |  | Add more flexibility in the run fifo method.
[stock_account_show_automatic_valuation](stock_account_show_automatic_valuation/) | 18.0.1.0.0 |  | Allow automatic valuation for stock moves in community edition
[stock_checkout_sync](stock_checkout_sync/) | 18.0.1.0.1 |  | Sync location for Checkout operations
[stock_dangerous_goods](stock_dangerous_goods/) | 18.0.1.0.0 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Adds utility fields to manage dangerous goods
[stock_dynamic_routing](stock_dynamic_routing/) | 18.0.1.3.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Dynamic routing of stock moves
[stock_dynamic_routing_checkout_sync](stock_dynamic_routing_checkout_sync/) | 18.0.1.0.0 |  | Glue module for tests when dynamic routing and checkout sync are used
[stock_dynamic_routing_delivery](stock_dynamic_routing_delivery/) | 18.0.1.1.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Glue module between stock dynamic routing and delivery
[stock_dynamic_routing_delivery_procurement_group_carrier](stock_dynamic_routing_delivery_procurement_group_carrier/) | 18.0.1.1.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Use the carrier set on the procurement group for propagation
[stock_dynamic_routing_reserve_rule](stock_dynamic_routing_reserve_rule/) | 18.0.1.0.0 |  | Glue module between dynamic routing and reservation rules
[stock_landed_costs_priority](stock_landed_costs_priority/) | 18.0.1.0.0 |  | Add priority to landed costs
[stock_landed_costs_purchase_auto](stock_landed_costs_purchase_auto/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Stock landed costs purchase auto
[stock_lock_lot](stock_lock_lot/) | 18.0.1.0.0 |  | Stock Lock Lot
[stock_lot_scrap](stock_lot_scrap/) | 18.0.1.0.1 |  | This module adds a button in Production Lot/Serial Number view form to Scrap all products contained.
[stock_move_actual_date](stock_move_actual_date/) | 18.0.1.0.1 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Stock Move Actual Date
[stock_move_auto_assign_auto_release](stock_move_auto_assign_auto_release/) | 18.0.1.1.0 |  | Auto release moves after auto assign
[stock_move_forced_lot](stock_move_forced_lot/) | 18.0.1.0.0 |  | This module allows you to set a lot_id in a procurement to force the stock move generated to only reserve the selected lot.
[stock_move_line_change_lot](stock_move_line_change_lot/) | 18.0.1.0.1 |  | Stock Move Line Change Lot
[stock_move_line_dates](stock_move_line_dates/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> | Add Date Scheduled and Deadline dates in move lines
[stock_move_line_expiration_date_required](stock_move_line_expiration_date_required/) | 18.0.1.0.2 |  | Stock Move Line Expiration Date Required
[stock_move_line_qty_picked](stock_move_line_qty_picked/) | 18.0.1.3.1 | <a href='https://github.com/grindtildeath'><img src='https://github.com/grindtildeath.png' width='32' height='32' style='border-radius:50%;' alt='grindtildeath'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Separate quantity picked from the reserved quantity
[stock_move_original_date](stock_move_original_date/) | 18.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | adds the Original Date Scheduled to stock moves.
[stock_move_propagate_first_move](stock_move_propagate_first_move/) | 18.0.1.0.0 |  | This addon propagate the picking type of the original move to all next moves created from procurement
[stock_move_quantity_product_uom](stock_move_quantity_product_uom/) | 18.0.1.0.2 |  | computes stock.move's quantity in the uom of the product.
[stock_move_source_relocate](stock_move_source_relocate/) | 18.0.1.2.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Change source location of unavailable moves
[stock_move_source_relocate_dynamic_routing](stock_move_source_relocate_dynamic_routing/) | 18.0.1.2.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Glue module
[stock_no_negative](stock_no_negative/) | 18.0.1.0.2 |  | Disallow negative stock levels by default
[stock_owner_restriction](stock_owner_restriction/) | 18.0.1.0.0 |  | Do not reserve quantity with assigned owner
[stock_partner_delivery_window](stock_partner_delivery_window/) | 18.0.1.2.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Define preferred delivery time windows for partners
[stock_picking_auto_create_lot](stock_picking_auto_create_lot/) | 18.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Auto create lots for incoming pickings
[stock_picking_auto_create_lot_sequence](stock_picking_auto_create_lot_sequence/) | 18.0.1.0.1 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Stock Picking Auto Create Lot Sequence
[stock_picking_auto_create_package](stock_picking_auto_create_package/) | 18.0.1.0.0 |  | Put all move lines in packs on validation.
[stock_picking_back2draft](stock_picking_back2draft/) | 18.0.1.0.0 |  | Reopen canceled transfers
[stock_picking_backorder_strategy_cancel](stock_picking_backorder_strategy_cancel/) | 18.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> <a href='https://github.com/mgosai'><img src='https://github.com/mgosai.png' width='32' height='32' style='border-radius:50%;' alt='mgosai'/></a> | Picking backordering strategies
[stock_picking_batch_creation](stock_picking_batch_creation/) | 18.0.1.5.1 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Create a batch of pickings to be processed all together
[stock_picking_batch_creation_split_kit](stock_picking_batch_creation_split_kit/) | 18.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Split picking by kit quantity when exceeding limits
[stock_picking_batch_invoice_frequency](stock_picking_batch_invoice_frequency/) | 18.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Invoice Sale Orders from Stock Pickin Batch
[stock_picking_batch_operation_quick_change](stock_picking_batch_operation_quick_change/) | 18.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Change location of all picking batch operations
[stock_picking_batch_planner](stock_picking_batch_planner/) | 18.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Allow planning origin batches/waves from destination batch/wave
[stock_picking_batch_print_invoices](stock_picking_batch_print_invoices/) | 18.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Print invoices from stock picking batchs
[stock_picking_batch_print_pickings](stock_picking_batch_print_pickings/) | 18.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Print Picking from Stock Picking Batch
[stock_picking_batch_validate_confirm](stock_picking_batch_validate_confirm/) | 18.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Request confirmation when validating batch if any pending origin moves
[stock_picking_consolidation_priority](stock_picking_consolidation_priority/) | 18.0.1.0.0 |  | Raise priority of all transfers for a chain when started
[stock_picking_customer_ref](stock_picking_customer_ref/) | 18.0.1.0.0 |  | This module displays the sale reference/description in the pickings
[stock_picking_date_deadline_syncs_scheduled_date](stock_picking_date_deadline_syncs_scheduled_date/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Sync Scheduled Date with Date Deadline in Stock Picking
[stock_picking_filter_lot](stock_picking_filter_lot/) | 18.0.1.0.0 |  | In picking out lots' selection, filter lots based on their location
[stock_picking_group_by_base](stock_picking_group_by_base/) | 18.0.1.0.0 |  | Allows to define a way to create index on extensible domain
[stock_picking_group_by_partner_by_carrier](stock_picking_group_by_partner_by_carrier/) | 18.0.1.3.0 |  | Stock Picking: group by partner and carrier
[stock_picking_group_by_partner_by_carrier_by_date](stock_picking_group_by_partner_by_carrier_by_date/) | 18.0.1.1.0 |  | Stock Picking: group by partner and carrier and scheduled date
[stock_picking_group_by_partner_by_carrier_force_move_type](stock_picking_group_by_partner_by_carrier_force_move_type/) | 18.0.1.0.0 |  | Glue module for Picking Type Force Shipping Policy and Group Transfers by Partner and Carrier
[stock_picking_import_serial_number](stock_picking_import_serial_number/) | 18.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Import S/N from excel file for incoming pickings
[stock_picking_invoice_link](stock_picking_invoice_link/) | 18.0.2.0.1 |  | Adds link between pickings and invoices
[stock_picking_kind](stock_picking_kind/) | 18.0.1.0.0 |  | Computes the kind of picking based on locations
[stock_picking_line_sequence](stock_picking_line_sequence/) | 18.0.1.0.1 |  | Manages the order of stock moves by displaying its sequence
[stock_picking_mass_action](stock_picking_mass_action/) | 18.0.1.0.0 |  | Stock Picking Mass Action
[stock_picking_operation_quick_change](stock_picking_operation_quick_change/) | 18.0.1.0.0 |  | Change location of all picking operations
[stock_picking_origin_reference](stock_picking_origin_reference/) | 18.0.1.0.0 |  | Add clickable button to the Transfer Source Document.
[stock_picking_origin_reference_purchase](stock_picking_origin_reference_purchase/) | 18.0.1.0.0 |  | Transfer to Purchase Order navigation from the Source Document.
[stock_picking_origin_reference_sale](stock_picking_origin_reference_sale/) | 18.0.1.0.0 |  | Transfer to Sales Order navigation from the Source Document.
[stock_picking_partner_note](stock_picking_partner_note/) | 18.0.1.0.0 |  | Add partner notes on picking
[stock_picking_progress](stock_picking_progress/) | 18.0.1.0.1 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> <a href='https://github.com/JuMiSanAr'><img src='https://github.com/JuMiSanAr.png' width='32' height='32' style='border-radius:50%;' alt='JuMiSanAr'/></a> | Compute the stock.picking progression
[stock_picking_propagate_scheduled_date](stock_picking_propagate_scheduled_date/) | 18.0.1.0.0 |  | Propagate Stock Picking Scheduled Date
[stock_picking_purchase_order_link](stock_picking_purchase_order_link/) | 18.0.1.1.0 |  | Link between picking and purchase order
[stock_picking_restrict_cancel_printed](stock_picking_restrict_cancel_printed/) | 18.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Prevent canceling a stock transfer if printed.
[stock_picking_return_lot](stock_picking_return_lot/) | 18.0.1.0.0 |  | Propagate SN/lots from origin picking to return picking.
[stock_picking_return_restricted_qty](stock_picking_return_restricted_qty/) | 18.0.1.0.0 |  | Restrict the return to delivered quantity
[stock_picking_sale_order_link](stock_picking_sale_order_link/) | 18.0.1.0.0 |  | Link between picking and sale order
[stock_picking_send_by_mail](stock_picking_send_by_mail/) | 18.0.1.0.1 |  | Send stock picking by email
[stock_picking_show_backorder](stock_picking_show_backorder/) | 18.0.1.0.0 |  | Provides a new field on stock pickings, allowing to display the corresponding backorders.
[stock_picking_show_lot](stock_picking_show_lot/) | 18.0.1.0.0 |  | Stock Picking Show Lot
[stock_picking_show_return](stock_picking_show_return/) | 18.0.1.0.0 |  | Show returns on stock pickings
[stock_picking_tier_validation](stock_picking_tier_validation/) | 18.0.1.0.2 |  | Extends the functionality of Transfers to support a tier validation process.
[stock_picking_to_batch_group_fields](stock_picking_to_batch_group_fields/) | 18.0.1.0.2 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Allows to create batches grouped by picking fields.
[stock_picking_type_bypass_reservation](stock_picking_type_bypass_reservation/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Bypass reservation on desired Stock Picking Types
[stock_picking_type_force_move_type](stock_picking_type_force_move_type/) | 18.0.1.0.1 |  | Force shipping policies on operation types
[stock_picking_warn_message](stock_picking_warn_message/) | 18.0.1.0.0 |  | Add a popup warning on picking to ensure warning is populated
[stock_picking_whole_scrap](stock_picking_whole_scrap/) | 18.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Create whole scrap from a picking for move lines
[stock_product_set](stock_product_set/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Add product sets in pickings
[stock_production_lot_active](stock_production_lot_active/) | 18.0.1.0.0 | <a href='https://github.com/ThomasBinsfeld'><img src='https://github.com/ThomasBinsfeld.png' width='32' height='32' style='border-radius:50%;' alt='ThomasBinsfeld'/></a> | Allow to archive/unarchive lots/serial numbers
[stock_receipt_lot_info](stock_receipt_lot_info/) | 18.0.1.0.0 |  | Be able to introduce more info on lot/serial number while processing a receipt.
[stock_restrict_lot](stock_restrict_lot/) | 18.0.1.1.2 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Base module that add back the concept of restrict lot on stock move
[stock_scrap_cancel](stock_scrap_cancel/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Stock Scrap Cancel
[stock_scrap_security](stock_scrap_security/) | 18.0.1.0.0 |  | Manage stock scrap access rights with dedicated security groups.
[stock_split_picking](stock_split_picking/) | 18.0.2.1.0 |  | Split a picking in two not transferred pickings
[stock_split_picking_dimension](stock_split_picking_dimension/) | 18.0.1.0.0 |  | Split a picking in two not transferred pickings to ensure that the first one doesn't exceed given dimensions (nbr lines, volume, weight)
[stock_split_picking_kit](stock_split_picking_kit/) | 18.0.1.0.1 |  | Split a picking by a number of kits.
[stock_valuation_layer_usage](stock_valuation_layer_usage/) | 18.0.1.0.0 |  | Trace where has the stock valuation been used in, including the quantities taken.
[stock_warn_option](stock_warn_option/) | 18.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Add Options to Stock Warn Messages

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/stock-weighing


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# stock-weighing
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-weighing&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/stock-weighing/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-weighing/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/stock-weighing/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/stock-weighing/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/stock-weighing/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-weighing)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-weighing-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-weighing-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

stock-weighing

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[sale_elaboration_weighing](sale_elaboration_weighing/) | 18.0.1.0.0 |  | Weighing assistant extension for elaborations
[stock_weighing](stock_weighing/) | 18.0.1.1.1 |  | Weighing assistant for stock operations
[stock_weighing_auto_create_lot](stock_weighing_auto_create_lot/) | 18.0.1.0.0 |  | Allow to create lots from the weighing kanban cards
[stock_weighing_auto_package](stock_weighing_auto_package/) | 18.0.1.0.0 |  | Auto create package for every weighing operation
[stock_weighing_brand](stock_weighing_brand/) | 18.0.1.0.0 |  | Show product logo in Weighing assistant
[stock_weighing_remote_measure](stock_weighing_remote_measure/) | 18.0.1.0.0 |  | Gather the operations weights remotely
[web_widget_remote_measure](web_widget_remote_measure/) | 18.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allows to connect to remote devices to record measures

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/storage


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/storage&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/storage/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/storage/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/storage/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/storage/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/storage/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/storage)
[![Translation Status](https://translation.odoo-community.org/widgets/storage-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/storage-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# storage

storage

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[fs_attachment](fs_attachment/) | 18.0.2.2.2 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Store attachments on external object store
[fs_attachment_s3](fs_attachment_s3/) | 18.0.1.2.1 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Store attachments into S3 complient filesystem
[fs_file](fs_file/) | 18.0.1.0.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Field to store files into filesystem storages
[fs_folder](fs_folder/) | 18.0.2.0.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | A module to link to Odoo records and manage from record forms forlders from external file systems
[fs_folder_demo](fs_folder_demo/) | 18.0.1.0.0 |  | Demo for fs_folder addon
[fs_folder_ms_drive](fs_folder_ms_drive/) | 18.0.2.0.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Display and manage your files from Microsoft drives from within Odoo
[fs_folder_webdav](fs_folder_webdav/) | 18.0.1.0.0 | <a href='https://github.com/jguenat'><img src='https://github.com/jguenat.png' width='32' height='32' style='border-radius:50%;' alt='jguenat'/></a> | UI improvement when managing WebDAV folder
[fs_image](fs_image/) | 18.0.1.0.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Field to store images into filesystem storages
[fs_image_thumbnail](fs_image_thumbnail/) | 18.0.1.0.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Generate and store thumbnail for images
[fs_storage](fs_storage/) | 18.0.2.1.2 |  | Implement the concept of Storage with amazon S3, sftp...
[fs_storage_ms_drive](fs_storage_ms_drive/) | 18.0.2.0.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Add the microsoft drives (OneDrive, Sharepoint) as a storage backend
[image_tag](image_tag/) | 18.0.1.0.0 |  | Image tag model
[microsoft_drive_account](microsoft_drive_account/) | 18.0.2.0.1 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Link user with Microsoft
[storage_backend](storage_backend/) | 18.0.1.0.0 |  | Implement the concept of Storage with amazon S3, sftp...
[storage_backend_ftp](storage_backend_ftp/) | 18.0.1.0.0 |  | Implement FTP Storage
[storage_backend_s3](storage_backend_s3/) | 18.0.1.1.0 |  | Implement amazon S3 Storage
[storage_backend_sftp](storage_backend_sftp/) | 18.0.1.0.0 |  | Implement SFTP Storage
[storage_file](storage_file/) | 18.0.1.2.0 |  | Storage file in storage backend
[storage_file_swap_backend_queue](storage_file_swap_backend_queue/) | 18.0.1.1.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Delegate storage file backend swap to queue jobs
[storage_image](storage_image/) | 18.0.1.2.0 |  | Store image and resized image in a storage backend
[storage_image_product](storage_image_product/) | 18.0.1.1.0 |  | Link images to products and categories
[storage_media](storage_media/) | 18.0.1.3.0 |  | Give the posibility to store media data in Odoo
[storage_media_product](storage_media_product/) | 18.0.1.1.0 |  | Link media to products and categories
[storage_thumbnail](storage_thumbnail/) | 18.0.1.1.0 |  | Abstract module that add the possibility to have thumbnail

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/survey


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/survey&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/survey/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/survey/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/survey/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/survey/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/survey/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/survey)
[![Translation Status](https://translation.odoo-community.org/widgets/survey-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/survey-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# survey

survey

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[partner_survey](partner_survey/) | 18.0.1.0.0 |  | Link partners with their survey results
[survey_xlsx](survey_xlsx/) | 18.0.1.0.0 |  | XLSX Report to show the survey results

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/timesheet


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# timesheet
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/timesheet&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/timesheet/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/timesheet/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/timesheet/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/timesheet/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/timesheet/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/timesheet)
[![Translation Status](https://translation.odoo-community.org/widgets/timesheet-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/timesheet-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

timesheet

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[crm_timesheet](crm_timesheet/) | 18.0.1.0.1 |  | CRM Timesheet
[hr_employee_cost_history](hr_employee_cost_history/) | 18.0.1.1.0 | <a href='https://github.com/SabrinaRMArtin'><img src='https://github.com/SabrinaRMArtin.png' width='32' height='32' style='border-radius:50%;' alt='SabrinaRMArtin'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Adds an history to employee's costs.
[hr_timesheet_autofill_project_off](hr_timesheet_autofill_project_off/) | 18.0.1.0.0 |  | Timesheet - Autofill project off
[hr_timesheet_begin_end](hr_timesheet_begin_end/) | 18.0.1.0.2 |  | Timesheet - Begin/End Hours
[hr_timesheet_calendar](hr_timesheet_calendar/) | 18.0.1.1.0 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | HR Timesheet Calendar
[hr_timesheet_date_order_desc](hr_timesheet_date_order_desc/) | 18.0.1.0.0 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | Add new timesheet entries to the top of the list and order by date descending
[hr_timesheet_day_week](hr_timesheet_day_week/) | 18.0.1.0.0 |  | Timesheets - Day of Week
[hr_timesheet_editable_top](hr_timesheet_editable_top/) | 18.0.1.0.0 |  | Add new timesheet entries to the top of the list
[hr_timesheet_employee_analytic_tag](hr_timesheet_employee_analytic_tag/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Hr Timesheet Employee Analytic Tag
[hr_timesheet_name_customer](hr_timesheet_name_customer/) | 18.0.1.0.0 |  | Add 'Description Customer' field for timesheets
[hr_timesheet_portal](hr_timesheet_portal/) | 18.0.1.0.0 |  | Fill in timesheets via the portal
[hr_timesheet_report](hr_timesheet_report/) | 18.0.1.0.0 | <a href='https://github.com/alexey-pelykh'><img src='https://github.com/alexey-pelykh.png' width='32' height='32' style='border-radius:50%;' alt='alexey-pelykh'/></a> | Generate Timesheet Report from Task Logs
[hr_timesheet_sheet](hr_timesheet_sheet/) | 18.0.1.3.2 |  | Timesheet Sheets, Activities
[hr_timesheet_sheet_attendance](hr_timesheet_sheet_attendance/) | 18.0.1.0.3 |  | HR Timesheet Sheet Attendance
[hr_timesheet_sheet_autodraft](hr_timesheet_sheet_autodraft/) | 18.0.1.0.0 |  | Automatically draft a Timesheet Sheet for every time entry that does not have a relevant Timesheet Sheet existing.
[hr_timesheet_sheet_policy_project_manager](hr_timesheet_sheet_policy_project_manager/) | 18.0.1.0.0 |  | Allows setting Project Manager as Reviewer
[hr_timesheet_sheet_warning](hr_timesheet_sheet_warning/) | 18.0.1.0.0 |  | Timesheet Sheets, Activities
[hr_timesheet_task_domain](hr_timesheet_task_domain/) | 18.0.1.0.0 |  | Limit task selection to tasks on currently-selected project
[hr_timesheet_task_required](hr_timesheet_task_required/) | 18.0.1.0.0 |  | Set task on timesheet as a mandatory field
[hr_timesheet_task_stage](hr_timesheet_task_stage/) | 18.0.1.0.1 |  | Open/Close task from corresponding Task Log entry
[hr_timesheet_time_control_begin_end](hr_timesheet_time_control_begin_end/) | 18.0.1.0.0 | <a href='https://github.com/CRogos'><img src='https://github.com/CRogos.png' width='32' height='32' style='border-radius:50%;' alt='CRogos'/></a> | HR Timesheet Time Control begin/end
[hr_timesheet_time_type](hr_timesheet_time_type/) | 18.0.1.0.0 |  | Ability to add time type in timesheet lines.
[hr_timesheet_type_non_billable](hr_timesheet_type_non_billable/) | 18.0.1.0.0 | <a href='https://github.com/mpascuall'><img src='https://github.com/mpascuall.png' width='32' height='32' style='border-radius:50%;' alt='mpascuall'/></a> | HR Timesheet Type Non Billable
[hr_timesheet_unusual_days](hr_timesheet_unusual_days/) | 18.0.1.0.0 | <a href='https://github.com/CRogos'><img src='https://github.com/CRogos.png' width='32' height='32' style='border-radius:50%;' alt='CRogos'/></a> | HR Timesheet Calendar Unusual Days
[project_task_analytic_propagation](project_task_analytic_propagation/) | 18.0.3.0.2 | <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/sabrinaRMartin'><img src='https://github.com/sabrinaRMartin.png' width='32' height='32' style='border-radius:50%;' alt='sabrinaRMartin'/></a> | Updates timesheet's analytic account when their task changes the analytic.
[project_timesheet_holidays_dynamic_description](project_timesheet_holidays_dynamic_description/) | 18.0.1.0.0 |  | Use the time off description for the generated timesheet lines.
[project_timesheet_holidays_editable](project_timesheet_holidays_editable/) | 18.0.1.0.0 |  | Re-enables timesheet edition when they're generated from leaves
[sale_timesheet_budget](sale_timesheet_budget/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Sale timesheet budget
[sale_timesheet_invoice_link](sale_timesheet_invoice_link/) | 18.0.1.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Link invoices with timesheet lines
[sale_timesheet_line_exclude](sale_timesheet_line_exclude/) | 18.0.1.0.0 |  | Exclude Timesheet Line from Sale Order
[sale_timesheet_rounded](sale_timesheet_rounded/) | 18.0.1.0.0 |  | Round timesheet entries amount based on project settings.
[sale_timesheet_timeline](sale_timesheet_timeline/) | 18.0.1.0.0 |  | Dates planning in sales order lines

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/version-control-platform


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# Version Control Platform configuration
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/version-control-platform&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/version-control-platform/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/version-control-platform/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/version-control-platform/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/version-control-platform/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/version-control-platform/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/version-control-platform)
[![Translation Status](https://translation.odoo-community.org/widgets/version-control-platform-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/version-control-platform-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Version Control Platform allows to import Git information and other kind of contributions in your odoo system

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[vcp_git](vcp_git/) | 18.0.1.0.0 |  | Allows to download code from git
[vcp_github](vcp_github/) | 18.0.1.0.1 |  | Integrate Version Control Platform with Github
[vcp_management](vcp_management/) | 18.0.1.0.1 |  | Management for your Version Control Platforms
[vcp_odoo](vcp_odoo/) | 18.0.1.0.1 |  | Import Odoo modules from VCP Repositories
[vcp_portal](vcp_portal/) | 18.0.1.0.0 |  | Version control platform integration with portal
[vcp_website](vcp_website/) | 18.0.1.0.0 |  | Adds integration of VCP with Odoo Website

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/vertical-association


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/vertical-association&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/vertical-association/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/vertical-association/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/vertical-association/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/vertical-association/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/vertical-association/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/vertical-association)
[![Translation Status](https://translation.odoo-community.org/widgets/vertical-association-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/vertical-association-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# vertical-association

vertical-association

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[contract_membership_delegated_partner](contract_membership_delegated_partner/) | 18.0.1.0.1 |  | Set delegate membership on the contract
[crm_membership](crm_membership/) | 18.0.1.0.0 | <a href='https://github.com/SirPyTech'><img src='https://github.com/SirPyTech.png' width='32' height='32' style='border-radius:50%;' alt='SirPyTech'/></a> | Shows membership data in CRM
[membership_delegated_partner](membership_delegated_partner/) | 18.0.1.1.0 |  | Delegate membership on a specific partner
[membership_extension](membership_extension/) | 18.0.1.1.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Improves user experience of membership addon
[membership_initial_fee](membership_initial_fee/) | 18.0.1.0.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | Initial fee for memberships
[membership_prorate](membership_prorate/) | 18.0.1.0.0 |  | Prorate membership fee
[membership_prorate_variable_period](membership_prorate_variable_period/) | 18.0.1.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | Prorate membership fee for variable periods
[membership_variable_period](membership_variable_period/) | 18.0.1.0.0 |  | Variable period for memberships
[membership_withdrawal](membership_withdrawal/) | 18.0.1.0.1 |  | Log membership withdrawal reason and date of request
[website_membership_gamification](website_membership_gamification/) | 18.0.1.0.0 |  | Show badges assigned to users on website
[website_membership_non_paid_member](website_membership_non_paid_member/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Online Members Directory - Display not paid members
[website_membership_random_order](website_membership_random_order/) | 18.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Online Members Directory - Random order

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/web


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# web
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/web&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/web/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/web/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/web/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/web/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/web/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/web)
[![Translation Status](https://translation.odoo-community.org/widgets/web-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/web-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

web

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[web_calendar_slot_duration](web_calendar_slot_duration/) | 18.0.1.0.0 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Customizable calendar slot durations
[web_chatter_position](web_chatter_position/) | 18.0.1.1.0 | <a href='https://github.com/trisdoan'><img src='https://github.com/trisdoan.png' width='32' height='32' style='border-radius:50%;' alt='trisdoan'/></a> | Add an option to change the chatter position
[web_company_color](web_company_color/) | 18.0.1.1.0 |  | Web Company Color
[web_copy_confirm](web_copy_confirm/) | 18.0.1.0.0 |  | Show confirmation dialogue before copying records
[web_dark_mode](web_dark_mode/) | 18.0.1.0.0 |  | Enabled Dark Mode for the Odoo Backend
[web_datetime_picker_default_time](web_datetime_picker_default_time/) | 18.0.1.0.0 | <a href='https://github.com/grindtildeath'><img src='https://github.com/grindtildeath.png' width='32' height='32' style='border-radius:50%;' alt='grindtildeath'/></a> | Allows to define a default time on datetime picker
[web_dialog_size](web_dialog_size/) | 18.0.1.0.1 |  | A module that lets the user expand a dialog box to the full screen width.
[web_disable_export_group](web_disable_export_group/) | 18.0.1.0.0 |  | Web Disable Export Group
[web_editor_class_selector](web_editor_class_selector/) | 18.0.1.0.0 | <a href='https://github.com/carlos-lopez-tecnativa'><img src='https://github.com/carlos-lopez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carlos-lopez-tecnativa'/></a> | Web editor class selector
[web_editor_disable_chatgpt](web_editor_disable_chatgpt/) | 18.0.1.0.0 |  | Web Disable ChatGPT
[web_environment_ribbon](web_environment_ribbon/) | 18.0.1.0.3 |  | Web Environment Ribbon
[web_excel_export_dynamic_expand](web_excel_export_dynamic_expand/) | 18.0.1.0.0 |  | Export collapsed groups or the full tree, based on its view.
[web_favicon](web_favicon/) | 18.0.1.0.1 |  | Allows to set a custom shortcut icon (aka favicon)
[web_filter_header_button](web_filter_header_button/) | 18.0.1.0.0 |  | Show selected filters as buttons in the control panel
[web_form_banner](web_form_banner/) | 18.0.1.1.0 |  | Web Form Banner
[web_group_expand](web_group_expand/) | 18.0.1.0.1 |  | Group Expand Buttons
[web_help](web_help/) | 18.0.1.0.0 |  | Help Framework
[web_ir_actions_act_multi](web_ir_actions_act_multi/) | 18.0.1.0.0 |  | Enables triggering of more than one action on ActionManager
[web_ir_actions_act_window_message](web_ir_actions_act_window_message/) | 18.0.1.0.1 |  | Show a message box to users
[web_m2x_options](web_m2x_options/) | 18.0.1.0.3 |  | web_m2x_options
[web_m2x_options_manager](web_m2x_options_manager/) | 18.0.1.0.0 |  | Adds an interface to manage the "Create" and "Create and Edit" options for specific models and fields.
[web_no_bubble](web_no_bubble/) | 18.0.1.0.0 |  | Remove the bubbles from the web interface
[web_notify](web_notify/) | 18.0.1.1.1 |  | Send notification messages to user
[web_notify_channel_message](web_notify_channel_message/) | 18.0.1.0.1 |  | Send an instant notification to channel users when a new message is posted
[web_notify_upgrade](web_notify_upgrade/) | 18.0.1.0.0 |  | Notify active users when a module is installed or updated
[web_pivot_computed_measure](web_pivot_computed_measure/) | 18.0.1.0.5 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Web Pivot Computed Measure
[web_portal_properties](web_portal_properties/) | 18.0.1.0.0 |  | Add a new field on properties to show them on portal
[web_pwa_customize](web_pwa_customize/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Web Pwa Customize
[web_quick_start_screen](web_quick_start_screen/) | 18.0.1.0.0 |  | Configurable start screen for quick actions
[web_refresher](web_refresher/) | 18.0.1.0.0 |  | Web Refresher
[web_remember_tree_column_width](web_remember_tree_column_width/) | 18.0.1.0.2 | <a href='https://github.com/frahikLV'><img src='https://github.com/frahikLV.png' width='32' height='32' style='border-radius:50%;' alt='frahikLV'/></a> <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> <a href='https://github.com/cuongnmtm'><img src='https://github.com/cuongnmtm.png' width='32' height='32' style='border-radius:50%;' alt='cuongnmtm'/></a> | Remember the tree columns' widths across sessions.
[web_responsive](web_responsive/) | 18.0.1.0.6 | <a href='https://github.com/Tardo'><img src='https://github.com/Tardo.png' width='32' height='32' style='border-radius:50%;' alt='Tardo'/></a> <a href='https://github.com/SplashS'><img src='https://github.com/SplashS.png' width='32' height='32' style='border-radius:50%;' alt='SplashS'/></a> | Responsive web client, community-supported
[web_save_discard_button](web_save_discard_button/) | 18.0.1.0.1 | <a href='https://github.com/synconics'><img src='https://github.com/synconics.png' width='32' height='32' style='border-radius:50%;' alt='synconics'/></a> | Save & Discard Buttons
[web_search_with_and](web_search_with_and/) | 18.0.1.0.1 |  | Use AND conditions on omnibar search
[web_send_message_popup](web_send_message_popup/) | 18.0.1.0.0 |  | Web Send Message as Popup
[web_session_auto_close](web_session_auto_close/) | 18.0.1.0.1 |  | Automatically logs out inactive users based on a configurable timeout.
[web_sort_menu](web_sort_menu/) | 18.0.1.0.0 |  | Sort Apps in DropDown/NavBar Menu alphabetically
[web_systray_button_init_action](web_systray_button_init_action/) | 18.0.1.0.2 |  | Add a button to go to the user init action.
[web_theme_classic](web_theme_classic/) | 18.0.1.2.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Contrasted style on fields to improve the UI.
[web_time_range_menu_custom](web_time_range_menu_custom/) | 18.0.1.0.0 |  | Web Time Range Menu Custom
[web_timeline](web_timeline/) | 18.0.1.0.3 |  | Interactive visualization chart to show events in time
[web_toggle_chatter](web_toggle_chatter/) | 18.0.1.0.0 |  | Toggle chatter in backend form views
[web_touchscreen](web_touchscreen/) | 18.0.1.0.0 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | UX improvements for touch screens
[web_tree_column_keyboard_resize](web_tree_column_keyboard_resize/) | 18.0.1.0.0 |  | Allow resizing tree view columns using keyboard shortcuts
[web_tree_dynamic_colored_field](web_tree_dynamic_colored_field/) | 18.0.1.0.1 |  | Allows you to dynamically color fields on tree views
[web_tree_many2one_clickable](web_tree_many2one_clickable/) | 18.0.1.0.1 |  | Open the linked resource when clicking on their name
[web_widget_bokeh_chart](web_widget_bokeh_chart/) | 18.0.1.0.1 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/JasminSForgeFlow'><img src='https://github.com/JasminSForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JasminSForgeFlow'/></a> | This widget allows to display charts using Bokeh library.
[web_widget_domain_editor_dialog](web_widget_domain_editor_dialog/) | 18.0.1.0.0 |  | Recovers the Domain Editor Dialog functionality
[web_widget_dropdown_dynamic](web_widget_dropdown_dynamic/) | 18.0.2.0.0 |  | This module adds support for dynamic dropdown widget
[web_widget_mpld3_chart](web_widget_mpld3_chart/) | 18.0.1.0.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/ThiagoMForgeFlow'><img src='https://github.com/ThiagoMForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ThiagoMForgeFlow'/></a> | This widget allows to display charts using MPLD3 library.
[web_widget_numeric_step](web_widget_numeric_step/) | 18.0.1.0.2 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Web Widget Numeric Step
[web_widget_o2m_attachment_image_gallery](web_widget_o2m_attachment_image_gallery/) | 18.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Widget o2m Attachment Image Gallery Widget
[web_widget_one2many_tree_line_duplicate](web_widget_one2many_tree_line_duplicate/) | 18.0.1.0.1 |  | Web Widget One2many Tree Line Duplicate
[web_widget_open_tab](web_widget_open_tab/) | 18.0.1.0.0 |  | Allow to open record from trees on new tab from tree views
[web_widget_popover](web_widget_popover/) | 18.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Render an icon that displays the field content in a popover
[web_widget_product_label_section_and_note_full_label](web_widget_product_label_section_and_note_full_label/) | 18.0.1.0.0 |  | Display the full label in the product_label_section_and_note widget.
[web_widget_product_label_section_and_note_name_visibility](web_widget_product_label_section_and_note_name_visibility/) | 18.0.1.0.1 | <a href='https://github.com/carlos-lopez-tecnativa'><img src='https://github.com/carlos-lopez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carlos-lopez-tecnativa'/></a> | Alternate the visibility of the product and description.
[web_widget_url_advanced](web_widget_url_advanced/) | 18.0.1.0.0 |  | This module extends URL widget for displaying anchors with custom labels.
[web_widget_x2many_2d_matrix](web_widget_x2many_2d_matrix/) | 18.0.2.1.0 | <a href='https://github.com/JasminSForgeFlow'><img src='https://github.com/JasminSForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JasminSForgeFlow'/></a> <a href='https://github.com/DavidJForgeFlow'><img src='https://github.com/DavidJForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='DavidJForgeFlow'/></a> <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Show list fields as a matrix

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/web-api


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/web-api&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/web-api/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/web-api/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/web-api/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/web-api/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/web-api/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/web-api)
[![Translation Status](https://translation.odoo-community.org/widgets/web-api-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/web-api-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# web-api

web-api

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[endpoint](endpoint/) | 18.0.1.1.1 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Provide custom endpoint machinery.
[endpoint_auth_api_key](endpoint_auth_api_key/) | 18.0.1.0.1 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Provide API key auth for endpoints.
[endpoint_cache](endpoint_cache/) | 18.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Provide basic caching utils for endpoints
[endpoint_cache_preheat](endpoint_cache_preheat/) | 18.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Provide basic pre-caching features for endpoints
[endpoint_jsonifier](endpoint_jsonifier/) | 18.0.1.0.0 | <a href='https://github.com/SilvioC2C'><img src='https://github.com/SilvioC2C.png' width='32' height='32' style='border-radius:50%;' alt='SilvioC2C'/></a> <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Allow to configure jsonifier parsers on endpoints
[endpoint_route_handler](endpoint_route_handler/) | 18.0.1.1.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Provide mixin and tool to generate custom endpoints on the fly.
[webservice](webservice/) | 18.0.1.1.0 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Defines webservice abstract definition to be used generally

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/web-api-contrib


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/web-api-contrib&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/web-api-contrib/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/web-api-contrib/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/web-api-contrib/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/web-api-contrib/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/web-api-contrib/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/web-api-contrib)
[![Translation Status](https://translation.odoo-community.org/widgets/web-api-contrib-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/web-api-contrib-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# web-api-contrib

web-api-contrib

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[endpoint_product_catalog](endpoint_product_catalog/) | 18.0.1.0.0 | <a href='https://github.com/SilvioC2C'><img src='https://github.com/SilvioC2C.png' width='32' height='32' style='border-radius:50%;' alt='SilvioC2C'/></a> <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Handle endpoints for product catalogs

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/website


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# website
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/website&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/website/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/website/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/website/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/website/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/website/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/website)
[![Translation Status](https://translation.odoo-community.org/widgets/website-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/website-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

website

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[website_altcha](website_altcha/) | 18.0.1.0.0 |  | Use self hosted privacy friendly captcha for verifying website users are not bots
[website_cf_turnstile_login](website_cf_turnstile_login/) | 18.0.1.0.0 | <a href='https://github.com/adasatorres'><img src='https://github.com/adasatorres.png' width='32' height='32' style='border-radius:50%;' alt='adasatorres'/></a> | Add Cloudflare Turnstile captcha to login form
[website_cookiebot](website_cookiebot/) | 18.0.1.0.0 |  | Ask for cookies consent connecting with Cookiebot
[website_cookiefirst](website_cookiefirst/) | 18.0.2.0.0 |  | Cookiefirst integration
[website_crm_quick_answer](website_crm_quick_answer/) | 18.0.1.0.0 |  | Add an automatic answer for contacts asking for info
[website_form_require_legal](website_form_require_legal/) | 18.0.1.0.1 |  | Add possibility to require confirm legal terms.
[website_forum_subscription](website_forum_subscription/) | 18.0.1.0.2 |  | Adds a button to allow subscription from the website
[website_google_tag_manager](website_google_tag_manager/) | 18.0.1.0.0 |  | Add support for Google Tag Manager
[website_legal_page](website_legal_page/) | 18.0.1.0.0 |  | Website Legal Page
[website_menu_by_user_status](website_menu_by_user_status/) | 18.0.1.0.0 |  | Allow to manage the display of website.menus
[website_odoo_debranding](website_odoo_debranding/) | 18.0.1.0.0 |  | Remove Odoo Branding from Website
[website_partner_form](website_partner_form/) | 18.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Allow to edit partner website fields on partner form view, in the back office
[website_product_document_download_counter](website_product_document_download_counter/) | 18.0.1.0.0 |  | Counts the product document downloads from the website.
[website_require_login](website_require_login/) | 18.0.1.0.0 |  | Website Login Required
[website_search_header](website_search_header/) | 18.0.1.0.0 |  | Website Search in Header
[website_select2](website_select2/) | 18.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Integrate select2 in Odoo websites
[website_snippet_country_dropdown](website_snippet_country_dropdown/) | 18.0.1.0.1 |  | Allow to select country in a dropdown
[website_user_login_redirect_custom](website_user_login_redirect_custom/) | 18.0.1.0.0 |  | Redirect website/portal user to custom URL after login or signup
[website_whatsapp](website_whatsapp/) | 18.0.1.0.1 | <a href='https://github.com/ioans73'><img src='https://github.com/ioans73.png' width='32' height='32' style='border-radius:50%;' alt='ioans73'/></a> | Whatsapp integration

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

