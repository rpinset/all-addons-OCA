# Merged READMEs

## From OCA/OpenUpgrade


[![Pre-commit Status](https://github.com/OCA/OpenUpgrade/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/OpenUpgrade/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/OpenUpgrade/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/OpenUpgrade/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/OpenUpgrade/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/OpenUpgrade)

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
[openupgrade_framework](openupgrade_framework/) | 17.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/StefanRijnhart'><img src='https://github.com/StefanRijnhart.png' width='32' height='32' style='border-radius:50%;' alt='StefanRijnhart'/></a> <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Module to integrate in the server_wide_modules option to make upgrades between two major revisions.
[openupgrade_scripts](openupgrade_scripts/) | 17.0.1.0.1 |  | Module that contains all the migrations analysis and scripts for migrate Odoo SA modules.

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-analytic&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/account-analytic/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-analytic/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/account-analytic/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-analytic/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/account-analytic/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-analytic)
[![Translation Status](https://translation.odoo-community.org/widgets/account-analytic-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-analytic-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-analytic

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_analytic_account_tag](account_analytic_account_tag/) | 17.0.1.0.0 |  | Restore the tag_ids in account.analytic.account
[account_analytic_distribution_manual](account_analytic_distribution_manual/) | 17.0.1.0.1 |  | Account analytic distribution manual
[account_analytic_distribution_manual_date](account_analytic_distribution_manual_date/) | 17.0.1.0.0 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> | Account analytic distribution manual date
[account_analytic_distribution_model_recalculate](account_analytic_distribution_model_recalculate/) | 17.0.1.1.0 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> | Add the posibility to change the analytic distribution of the journal items assigned by the distribution model
[account_analytic_distribution_widget_rebalance](account_analytic_distribution_widget_rebalance/) | 17.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Add a button to rebalance the analytic distribution back to 100%
[account_analytic_document_date](account_analytic_document_date/) | 17.0.1.0.1 | <a href='https://github.com/mpascuall'><img src='https://github.com/mpascuall.png' width='32' height='32' style='border-radius:50%;' alt='mpascuall'/></a> <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> | Account Analytic Document Date
[account_analytic_line_name_text](account_analytic_line_name_text/) | 17.0.1.0.0 |  | Changes account analytic line name field to Text.
[account_analytic_organization](account_analytic_organization/) | 17.0.1.0.0 | <a href='https://github.com/mpascuall'><img src='https://github.com/mpascuall.png' width='32' height='32' style='border-radius:50%;' alt='mpascuall'/></a> | Adds organization field on the partner so you can use it on your analytic
[account_analytic_parent](account_analytic_parent/) | 17.0.1.0.0 |  | This module reintroduces the hierarchy to the analytic accounts.
[account_analytic_required](account_analytic_required/) | 17.0.1.0.0 |  | Account Analytic Required
[account_analytic_sequence](account_analytic_sequence/) | 17.0.1.0.0 |  | Restore the analytic account sequence
[account_analytic_spread_by_tag](account_analytic_spread_by_tag/) | 17.0.1.0.1 |  | Account Analytic Spread by Tag
[account_analytic_tag](account_analytic_tag/) | 17.0.1.1.1 |  | Account Analytic Tag
[account_move_update_analytic](account_move_update_analytic/) | 17.0.1.2.1 | <a href='https://github.com/remi-filament'><img src='https://github.com/remi-filament.png' width='32' height='32' style='border-radius:50%;' alt='remi-filament'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | This module allows the user to update analytic on posted moves
[analytic_base_department](analytic_base_department/) | 17.0.1.0.0 |  | Add relationship between Analytic and Department
[analytic_partner](analytic_partner/) | 17.0.1.0.0 |  | Search and group analytic entries by partner
[hr_timesheet_analytic_tag](hr_timesheet_analytic_tag/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Hr Timesheet Analytic Tag
[mrp_stock_analytic](mrp_stock_analytic/) | 17.0.1.0.0 |  | MRP Stock Analytic
[pos_analytic_by_config](pos_analytic_by_config/) | 17.0.1.0.0 |  | Use analytic account defined on POS configuration for POS orders
[product_analytic](product_analytic/) | 17.0.1.0.0 |  | Add analytic account on products and product categories
[purchase_analytic](purchase_analytic/) | 17.0.1.0.0 |  | Purchase Analytic
[purchase_analytic_tag](purchase_analytic_tag/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Purchase Analytic Tag
[purchase_request_analytic](purchase_request_analytic/) | 17.0.1.0.0 |  | Purchase Request Analytic
[purchase_stock_analytic](purchase_stock_analytic/) | 17.0.1.0.0 |  | Copies the analytic distribution of the purchase order itemto the stock move
[sale_analytic_tag](sale_analytic_tag/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Sale Analytic Tag
[stock_analytic](stock_analytic/) | 17.0.1.2.1 |  | Adds analytic distribution in stock move
[stock_analytic_rule](stock_analytic_rule/) | 17.0.1.0.0 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> | Adds distribution rules for stock moves to automatically create analytic lines
[stock_landed_costs_analytic](stock_landed_costs_analytic/) | 17.0.1.0.0 |  | This module adds an analytic account and analytic tags on landed costs lines so that on landed costs validation account moves get analytic account and analytic tags values from landed costs lines.
[stock_picking_analytic](stock_picking_analytic/) | 17.0.1.0.0 |  | Allows to define the analytic account on picking level

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-budgeting&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/account-budgeting/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-budgeting/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/account-budgeting/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-budgeting/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/account-budgeting/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-budgeting)
[![Translation Status](https://translation.odoo-community.org/widgets/account-budgeting-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-budgeting-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-budgeting

{'TODO': 'add repo description.'}

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_budget_oca](account_budget_oca/) | 17.0.1.0.0 |  | Budgets Management

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-closing&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/account-closing/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-closing/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/account-closing/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-closing/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/account-closing/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-closing)
[![Translation Status](https://translation.odoo-community.org/widgets/account-closing-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-closing-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-closing

Odoo Accountant closing tools

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_cutoff_accrual_subscription](account_cutoff_accrual_subscription/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Accrued expenses based on subscriptions
[account_cutoff_base](account_cutoff_base/) | 17.0.1.2.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Base module for Account Cut-offs
[account_cutoff_picking](account_cutoff_picking/) | 17.0.1.1.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Accrued and prepaid expense/revenue from pickings
[account_cutoff_start_end_dates](account_cutoff_start_end_dates/) | 17.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Cutoffs based on start/end dates
[account_invoice_start_end_dates](account_invoice_start_end_dates/) | 17.0.1.4.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adds start/end dates on invoice/move lines
[account_move_cutoff](account_move_cutoff/) | 17.0.0.1.0 | <a href='https://github.com/petrus-v'><img src='https://github.com/petrus-v.png' width='32' height='32' style='border-radius:50%;' alt='petrus-v'/></a> | Account move Cut-offs, manage Deferred Revenues/Expenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-financial-reporting&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/account-financial-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-financial-reporting/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/account-financial-reporting/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-financial-reporting/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/account-financial-reporting/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-financial-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/account-financial-reporting-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-financial-reporting-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-financial-reporting

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_financial_report](account_financial_report/) | 17.0.1.9.9 |  | OCA Financial Reports
[account_move_line_report_xls](account_move_line_report_xls/) | 17.0.1.0.0 |  | Journal Items Excel export
[account_purchase_stock_report_non_billed](account_purchase_stock_report_non_billed/) | 17.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Account Purchase Stock Report Non Billed
[account_sale_stock_report_non_billed](account_sale_stock_report_non_billed/) | 17.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Account Sale Stock Report Non Billed
[account_tax_balance](account_tax_balance/) | 17.0.1.0.2 |  | Compute tax balances based on date range
[mis_builder_cash_flow](mis_builder_cash_flow/) | 17.0.1.0.1 | <a href='https://github.com/jjscarafia'><img src='https://github.com/jjscarafia.png' width='32' height='32' style='border-radius:50%;' alt='jjscarafia'/></a> | MIS Builder Cash Flow
[mis_template_financial_report](mis_template_financial_report/) | 17.0.1.0.1 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Profit & Loss / Balance sheet MIS templates
[partner_statement](partner_statement/) | 17.0.1.3.3 | <a href='https://github.com/MiquelRForgeFlow'><img src='https://github.com/MiquelRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='MiquelRForgeFlow'/></a> | OCA Financial Reports

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-financial-tools&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/account-financial-tools/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-financial-tools/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/account-financial-tools/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-financial-tools/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/account-financial-tools/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-financial-tools)
[![Translation Status](https://translation.odoo-community.org/widgets/account-financial-tools-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-financial-tools-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-financial-tools

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_account_tag_code](account_account_tag_code/) | 17.0.1.0.0 |  | Add a code field to the accounts tags
[account_asset_force_account](account_asset_force_account/) | 17.0.1.1.0 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> | This module allows you to enforce specific accounts for assets, including depreciation and expense accounts, through asset profiles and forms.
[account_asset_management](account_asset_management/) | 17.0.1.2.2 |  | Assets Management
[account_asset_management_stock_lot](account_asset_management_stock_lot/) | 17.0.1.0.0 |  | Assets Management Stock Lot
[account_bank_statement_chatter](account_bank_statement_chatter/) | 17.0.1.0.0 | <a href='https://github.com/cubells'><img src='https://github.com/cubells.png' width='32' height='32' style='border-radius:50%;' alt='cubells'/></a> | Chatter on bank statements
[account_chart_update](account_chart_update/) | 17.0.1.1.2 |  | Wizard to update a company's account chart from a template
[account_chart_update_l10n_eu_oss](account_chart_update_l10n_eu_oss/) | 17.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Account Chart update OSS
[account_check_deposit](account_check_deposit/) | 17.0.1.0.0 |  | Manage deposit of checks to the bank
[account_fiscal_month](account_fiscal_month/) | 17.0.1.0.0 |  | Provide a fiscal month date range type
[account_fiscal_year](account_fiscal_year/) | 17.0.1.1.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Create Account Fiscal Year
[account_journal_lock_date](account_journal_lock_date/) | 17.0.1.0.0 |  | Lock each journal independently
[account_journal_restrict_mode](account_journal_restrict_mode/) | 17.0.1.0.0 |  | Lock All Posted Entries of Journals.
[account_loan](account_loan/) | 17.0.2.2.1 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Account Loan management
[account_lock_date_update](account_lock_date_update/) | 17.0.1.0.1 |  | Allow an Account adviser to update locking date without having access to all technical settings
[account_lock_to_date](account_lock_to_date/) | 17.0.1.0.1 |  | Allows to set an account lock date in the future.
[account_move_budget](account_move_budget/) | 17.0.1.0.0 |  | Create Accounting Budgets
[account_move_line_purchase_info](account_move_line_purchase_info/) | 17.0.2.0.0 |  | Introduces the purchase order line to the journal items
[account_move_line_sale_info](account_move_line_sale_info/) | 17.0.1.0.0 |  | Introduces the purchase order line to the journal items
[account_move_line_tax_editable](account_move_line_tax_editable/) | 17.0.1.0.0 |  | Allows to edit taxes on non-posted account move lines
[account_move_name_sequence](account_move_name_sequence/) | 17.0.1.0.5 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/moylop260'><img src='https://github.com/moylop260.png' width='32' height='32' style='border-radius:50%;' alt='moylop260'/></a> <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Generate journal entry number from sequence
[account_move_post_date_user](account_move_post_date_user/) | 17.0.1.0.0 | <a href='https://github.com/JordiMForgeFlow'><img src='https://github.com/JordiMForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiMForgeFlow'/></a> | Trace journal entry posting date and user.
[account_move_print](account_move_print/) | 17.0.1.0.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> | Adds the option to print Journal Entries
[account_move_template](account_move_template/) | 17.0.1.0.1 |  | Templates for recurring Journal Entries
[account_netting](account_netting/) | 17.0.1.0.0 |  | Compensate AR/AP accounts from the same partner
[account_partner_required](account_partner_required/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adds an option 'partner policy' on accounts
[account_payroll_sheet_import](account_payroll_sheet_import/) | 17.0.1.0.0 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> | Import payroll from sheet files and generate journal entries
[account_sequence_option](account_sequence_option/) | 17.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Manage sequence options for account.move, i.e., invoice, bill, entry
[account_spread_cost_revenue](account_spread_cost_revenue/) | 17.0.1.0.0 |  | Spread costs and revenues over a custom period
[account_tax_repartition_line_tax_group_account](account_tax_repartition_line_tax_group_account/) | 17.0.1.0.0 |  | Set a default account from tax group to tax repartition lines
[account_usability](account_usability/) | 17.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Adds missing menu entries for Account module and adds the option to enable Saxon Accounting
[mail_template_substitute_account_move](mail_template_substitute_account_move/) | 17.0.1.0.0 | <a href='https://github.com/SodexisTeam'><img src='https://github.com/SodexisTeam.png' width='32' height='32' style='border-radius:50%;' alt='SodexisTeam'/></a> | Module to support Mail Template Substitution for Account Move
[purchase_unreconciled](purchase_unreconciled/) | 17.0.2.1.0 | <a href='https://github.com/AaronHForgeFlow'><img src='https://github.com/AaronHForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='AaronHForgeFlow'/></a> | Purchase Unreconciled

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-fiscal-rule&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/account-fiscal-rule/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-fiscal-rule/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/account-fiscal-rule/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-fiscal-rule/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/account-fiscal-rule/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-fiscal-rule)
[![Translation Status](https://translation.odoo-community.org/widgets/account-fiscal-rule-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-fiscal-rule-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-fiscal-rule

Odoo Accounting Taxe and Fiscal Features

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_avatax_oca](account_avatax_oca/) | 17.0.1.4.1 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Compute Sales Tax using the Avalara Avatax Service
[account_avatax_sale_oca](account_avatax_sale_oca/) | 17.0.1.1.0 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Sales Orders with automatic Tax application using Avatax
[account_avatax_website_sale](account_avatax_website_sale/) | 17.0.1.0.0 | <a href='https://github.com/cybernexus'><img src='https://github.com/cybernexus.png' width='32' height='32' style='border-radius:50%;' alt='cybernexus'/></a> | Ecommerce Sales Orders require tax recalculation prior to payment.
[account_ecotax](account_ecotax/) | 17.0.1.1.2 | <a href='https://github.com/mourad-ehm'><img src='https://github.com/mourad-ehm.png' width='32' height='32' style='border-radius:50%;' alt='mourad-ehm'/></a> <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Ecotax Management: in French context is a 'cost' added to the sale price of electrical or electronic appliances or furnishing items
[account_ecotax_sale](account_ecotax_sale/) | 17.0.1.0.2 | <a href='https://github.com/mourad-ehm'><img src='https://github.com/mourad-ehm.png' width='32' height='32' style='border-radius:50%;' alt='mourad-ehm'/></a> <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Sale Ecotaxe
[account_ecotax_tax](account_ecotax_tax/) | 17.0.1.0.1 | <a href='https://github.com/mourad-ehm'><img src='https://github.com/mourad-ehm.png' width='32' height='32' style='border-radius:50%;' alt='mourad-ehm'/></a> <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Use Odoo tax mechanism to compute the ecotaxes
[account_fiscal_position_autodetect_optional_vies](account_fiscal_position_autodetect_optional_vies/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Account Fiscal Position Autodetect optional VIES
[account_fiscal_position_partner_type](account_fiscal_position_partner_type/) | 17.0.1.1.0 |  | Account Fiscal Position Partner Type
[l10n_eu_oss_oca](l10n_eu_oss_oca/) | 17.0.1.1.3 |  | L10n EU OSS OCA

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-invoice-reporting&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/account-invoice-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-invoice-reporting/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/account-invoice-reporting/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-invoice-reporting/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/account-invoice-reporting/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-invoice-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/account-invoice-reporting-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-invoice-reporting-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-invoice-reporting

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_comment_template](account_comment_template/) | 17.0.1.0.0 |  | Comments templates on invoice documents
[account_invoice_bank_details](account_invoice_bank_details/) | 17.0.1.0.1 |  | Select bank account base on currency + print bank details on reportreports and customer portal
[account_invoice_line_report](account_invoice_line_report/) | 17.0.1.0.0 |  | New view to manage invoice lines information
[account_invoice_line_sale_line_position](account_invoice_line_sale_line_position/) | 17.0.1.0.0 |  | Adds the related sale line position on invoice line.
[account_invoice_production_lot](account_invoice_production_lot/) | 17.0.1.0.1 |  | Display delivered serial numbers in invoice
[account_invoice_report_grouped_by_picking](account_invoice_report_grouped_by_picking/) | 17.0.1.0.6 |  | Print invoice lines grouped by picking
[partner_time_to_pay](partner_time_to_pay/) | 17.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Add receivables and payables statistics to partners

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-invoicing&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/account-invoicing/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-invoicing/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/account-invoicing/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-invoicing/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/account-invoicing/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-invoicing)
[![Translation Status](https://translation.odoo-community.org/widgets/account-invoicing-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-invoicing-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-invoicing

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_global_discount](account_global_discount/) | 17.0.1.0.0 |  | Account Global Discount
[account_invoice_auto_send_by_email](account_invoice_auto_send_by_email/) | 17.0.1.0.0 |  | Invoice with the email transmit method are send automatically.
[account_invoice_block_payment](account_invoice_block_payment/) | 17.0.1.0.0 |  | Module to block payment of invoices
[account_invoice_blocking](account_invoice_blocking/) | 17.0.1.0.2 |  | Set a blocking (No Follow-up) flag on invoices
[account_invoice_crm_tag](account_invoice_crm_tag/) | 17.0.1.0.0 |  | Account Invoice CRM Tag
[account_invoice_customer_no_autofollow](account_invoice_customer_no_autofollow/) | 17.0.1.0.0 |  | Do not add customer as follower in Invoices
[account_invoice_date_due](account_invoice_date_due/) | 17.0.1.0.1 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Update Invoice's Due Date
[account_invoice_discount_display_amount](account_invoice_discount_display_amount/) | 17.0.1.0.0 |  | Show total discount applied and total without discount on invoices.
[account_invoice_fixed_discount](account_invoice_fixed_discount/) | 17.0.1.1.0 |  | Allows to apply fixed amount discounts in invoices.
[account_invoice_mass_sending](account_invoice_mass_sending/) | 17.0.1.0.0 | <a href='https://github.com/jguenat'><img src='https://github.com/jguenat.png' width='32' height='32' style='border-radius:50%;' alt='jguenat'/></a> | This addon adds a mass sending feature on invoices.
[account_invoice_pricelist](account_invoice_pricelist/) | 17.0.1.0.4 |  | Add partner pricelist on invoices
[account_invoice_refund_link](account_invoice_refund_link/) | 17.0.1.0.1 |  | Show links between refunds and their originator invoices.
[account_invoice_section_sale_order](account_invoice_section_sale_order/) | 17.0.2.2.0 |  | For invoices targetting multiple sale order addsections with sale order name.
[account_invoice_show_currency_rate](account_invoice_show_currency_rate/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Show currency rate in invoices.
[account_invoice_subscription_per_contact](account_invoice_subscription_per_contact/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Account Invoice Subscription per contact
[account_invoice_supplier_ref_unique](account_invoice_supplier_ref_unique/) | 17.0.1.0.0 |  | Checks that supplier invoices are not entered twice
[account_invoice_supplierinfo_update](account_invoice_supplierinfo_update/) | 17.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | In the supplier invoice, automatically updates all products whose unit price on the line is different from the supplier price
[account_invoice_transmit_method](account_invoice_transmit_method/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Configure invoice transmit method (email, post, portal, ...)
[account_invoice_triple_discount](account_invoice_triple_discount/) | 17.0.1.0.0 |  | Manage triple discount on invoice lines
[account_invoice_warn_message](account_invoice_warn_message/) | 17.0.1.0.0 |  | Add a popup warning on invoice to ensure warning is populated
[account_manual_currency](account_manual_currency/) | 17.0.1.0.0 |  | Allows to manual currency of Accounting
[account_menu_invoice_refund](account_menu_invoice_refund/) | 17.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | New invoice menu that combine invoices and refunds
[account_move_cancel_confirm](account_move_cancel_confirm/) | 17.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Account Move Cancel Confirm
[account_move_tag](account_move_tag/) | 17.0.1.0.0 |  | Adds tags to the account move so vendor bills and customer invoices can be easily distinguished in the accounting journal.
[account_move_tier_validation](account_move_tier_validation/) | 17.0.1.0.1 |  | Extends the functionality of Account Moves to support a tier validation process.
[partner_invoicing_mode](partner_invoicing_mode/) | 17.0.1.0.0 |  | Base module for handling multiple partner invoicing mode
[portal_account_personal_data_only](portal_account_personal_data_only/) | 17.0.1.0.0 |  | Portal Accounting Personal Data Only
[product_form_account_move_line_link](product_form_account_move_line_link/) | 17.0.1.0.0 |  | Adds a button on product forms to access Journal Items
[purchase_stock_picking_return_invoicing](purchase_stock_picking_return_invoicing/) | 17.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/MiquelRForgeFlow'><img src='https://github.com/MiquelRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='MiquelRForgeFlow'/></a> | Add an option to refund returned pickings
[sale_invoicing_date_selection](sale_invoicing_date_selection/) | 17.0.1.0.1 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Set date invoice when you create invoices
[sale_order_invoicing_grouping_criteria](sale_order_invoicing_grouping_criteria/) | 17.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Sales order invoicing grouping criteria
[sale_order_invoicing_qty_percentage](sale_order_invoicing_qty_percentage/) | 17.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Sales order invoicing by percentage of the quantity
[sale_order_type_whole_delivered_invoiceability](sale_order_type_whole_delivered_invoiceability/) | 17.0.1.0.0 |  | Sale Order Type Whole Delivered Invoiceability
[sale_order_whole_delivered_invoiceability](sale_order_whole_delivered_invoiceability/) | 17.0.1.0.0 |  | Sale Order Whole Delivered Invoiceability
[sale_timesheet_invoice_description](sale_timesheet_invoice_description/) | 17.0.1.0.1 |  | Add timesheet details in invoice line
[stock_account_move_reset_to_draft](stock_account_move_reset_to_draft/) | 17.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Stock account move reset to draft
[stock_picking_invoicing](stock_picking_invoicing/) | 17.0.1.0.0 |  | Stock Picking Invoicing
[stock_picking_invoicing_incoterm](stock_picking_invoicing_incoterm/) | 17.0.1.0.0 |  | Stock Picking Invoicing Incoterm
[stock_picking_return_refund_option](stock_picking_return_refund_option/) | 17.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Update the refund options in pickings

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-payment&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/account-payment/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-payment/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/account-payment/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-payment/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/account-payment/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-payment)
[![Translation Status](https://translation.odoo-community.org/widgets/account-payment-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-payment-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-payment

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_due_list](account_due_list/) | 17.0.1.0.0 |  | List of open credits and debits, with due date
[account_due_list_aging_comment](account_due_list_aging_comment/) | 17.0.1.0.0 |  | Account Due List Aging Comment
[account_due_list_payment_mode](account_due_list_payment_mode/) | 17.0.1.0.0 |  | Payment Due List Payment Mode
[account_move_reconcile_export](account_move_reconcile_export/) | 17.0.1.0.0 |  | Manage the export of reconciled moves linked to invoices
[account_payment_multi_deduction](account_payment_multi_deduction/) | 17.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Payment Register with Multiple Deduction
[account_payment_promissory_note](account_payment_promissory_note/) | 17.0.1.0.1 |  | Account Payment Promissory Note
[account_payment_return](account_payment_return/) | 17.0.1.2.2 |  | Manage the return of your payments
[account_payment_return_import](account_payment_return_import/) | 17.0.1.0.0 |  | This module adds a generic wizard to import payment returnfile formats. Is only the base to be extended by anothermodules
[account_payment_return_import_iso20022](account_payment_return_import_iso20022/) | 17.0.1.0.1 |  | This addon allows to import payment returns from ISO 20022 files like PAIN or CAMT.
[account_payment_term_extension](account_payment_term_extension/) | 17.0.1.0.5 |  | Adds rounding, months, weeks and multiple payment days properties on payment term lines
[account_payment_term_partner_paydays](account_payment_term_partner_paydays/) | 17.0.1.0.0 |  | Allows to define payment days for partners.
[account_payment_term_security](account_payment_term_security/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Payment Term Security
[account_payment_widget_amount](account_payment_widget_amount/) | 17.0.1.0.0 |  | Extends the payment widget to be able to choose the payment amount
[partner_aging](partner_aging/) | 17.0.1.0.0 | <a href='https://github.com/Urvisha-OSI'><img src='https://github.com/Urvisha-OSI.png' width='32' height='32' style='border-radius:50%;' alt='Urvisha-OSI'/></a> | Aging as a view - invoices and credits
[partner_restrict_payment_acquirer](partner_restrict_payment_acquirer/) | 17.0.1.0.0 |  | Partner Restrict Payment Acquirer
[product_restrict_payment_acquirer](product_restrict_payment_acquirer/) | 17.0.1.0.0 | <a href='https://github.com/bearnard21'><img src='https://github.com/bearnard21.png' width='32' height='32' style='border-radius:50%;' alt='bearnard21'/></a> <a href='https://github.com/CetmixGitDrone'><img src='https://github.com/CetmixGitDrone.png' width='32' height='32' style='border-radius:50%;' alt='CetmixGitDrone'/></a> | Product Restrict Payment Acquirer
[sale_payment_term_security](sale_payment_term_security/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Sale Payment Term Security

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-reconcile&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/account-reconcile/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-reconcile/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/account-reconcile/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/account-reconcile/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/account-reconcile/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-reconcile)
[![Translation Status](https://translation.odoo-community.org/widgets/account-reconcile-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-reconcile-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-reconcile

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_in_payment](account_in_payment/) | 17.0.1.0.0 |  | This module enables in-payment mode for your accounting
[account_mass_reconcile](account_mass_reconcile/) | 17.0.1.0.1 |  | Account Mass Reconcile
[account_partner_reconcile](account_partner_reconcile/) | 17.0.1.0.0 |  | Account Partner Reconcile
[account_reconcile_model_oca](account_reconcile_model_oca/) | 17.0.1.0.4 |  | This includes the logic moved from Odoo Community to Odoo Enterprise
[account_reconcile_oca](account_reconcile_oca/) | 17.0.1.5.28 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Reconcile addons for Odoo CE accounting
[account_statement_base](account_statement_base/) | 17.0.1.6.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Base module for Bank Statements

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/agreement&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/agreement/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/agreement/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/agreement/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/agreement/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/agreement/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/agreement)
[![Translation Status](https://translation.odoo-community.org/widgets/agreement-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/agreement-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Agreements modules

TODO: add repo description

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[agreement](agreement/) | 17.0.1.1.1 | <a href='https://github.com/ygol'><img src='https://github.com/ygol.png' width='32' height='32' style='border-radius:50%;' alt='ygol'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adds an agreement object
[agreement_account](agreement_account/) | 17.0.1.0.2 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Agreement on invoices
[agreement_legal](agreement_legal/) | 17.0.3.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/ygol'><img src='https://github.com/ygol.png' width='32' height='32' style='border-radius:50%;' alt='ygol'/></a> | Manage Agreements, LOI and Contracts
[agreement_project](agreement_project/) | 17.0.1.0.0 | <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> <a href='https://github.com/ygol'><img src='https://github.com/ygol.png' width='32' height='32' style='border-radius:50%;' alt='ygol'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Link projects to an agreement
[agreement_repair](agreement_repair/) | 17.0.1.0.1 | <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Link repair orders to an agreement
[agreement_sale](agreement_sale/) | 17.0.1.0.2 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Agreement on sales

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/ai&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/ai/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/ai/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/ai/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/ai/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/ai/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/ai)
[![Translation Status](https://translation.odoo-community.org/widgets/ai-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/ai-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# ai

ai

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[ai_oca_bridge](ai_oca_bridge/) | 17.0.2.0.0 |  | Makes a basic configuration to be used as bridge with external AI systems
[ai_oca_bridge_chatter](ai_oca_bridge_chatter/) | 17.0.2.0.0 |  | Integrate a Bridge with a user that will use it on chatter
[ai_oca_bridge_document_page](ai_oca_bridge_document_page/) | 17.0.2.0.0 |  | Adds Documents synchronization using AI Bridges
[ai_oca_bridge_extra_parameters](ai_oca_bridge_extra_parameters/) | 17.0.1.0.1 | <a href='https://github.com/arielbarreiros96'><img src='https://github.com/arielbarreiros96.png' width='32' height='32' style='border-radius:50%;' alt='arielbarreiros96'/></a> | Adds extra parameters to the AI OCA Bridge payload.

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/automation&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/automation/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/automation/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/automation/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/automation/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/automation/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/automation)
[![Translation Status](https://translation.odoo-community.org/widgets/automation-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/automation-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# automation

automation

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[automation_oca](automation_oca/) | 17.0.1.1.0 |  | Automate actions in threaded models

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/bank-payment&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/bank-payment/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/bank-payment/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/bank-payment/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/bank-payment/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/bank-payment/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/bank-payment)
[![Translation Status](https://translation.odoo-community.org/widgets/bank-payment-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/bank-payment-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# bank-payment

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_banking_international_credit_transfer](account_banking_international_credit_transfer/) | 17.0.1.0.0 |  | Create PAIN XML files for International Credit Transfers
[account_banking_mandate](account_banking_mandate/) | 17.0.1.0.4 |  | Banking mandates
[account_banking_mandate_contact](account_banking_mandate_contact/) | 17.0.1.1.2 |  | Assign specific banking mandates in contact level
[account_banking_mandate_sale](account_banking_mandate_sale/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adds mandates on sale orders
[account_banking_mandate_sale_contact](account_banking_mandate_sale_contact/) | 17.0.1.0.1 | <a href='https://github.com/tisho99'><img src='https://github.com/tisho99.png' width='32' height='32' style='border-radius:50%;' alt='tisho99'/></a> | Add a specific contact mandate to sale orders
[account_banking_pain_base](account_banking_pain_base/) | 17.0.1.1.0 |  | Base module for PAIN file generation
[account_banking_sepa_credit_transfer](account_banking_sepa_credit_transfer/) | 17.0.1.1.1 |  | Create SEPA XML files for Credit Transfers
[account_banking_sepa_direct_debit](account_banking_sepa_direct_debit/) | 17.0.1.3.1 |  | Create SEPA files for Direct Debit
[account_payment_mode](account_payment_mode/) | 17.0.1.1.0 |  | Account Payment Mode
[account_payment_order](account_payment_order/) | 17.0.1.7.6 |  | Account Payment Order
[account_payment_order_grouped_output](account_payment_order_grouped_output/) | 17.0.1.0.0 |  | Account Payment Order - Generate grouped moves
[account_payment_order_notification](account_payment_order_notification/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Account Payment Order Notification
[account_payment_order_return](account_payment_order_return/) | 17.0.1.0.1 |  | Account Payment Order Return
[account_payment_partner](account_payment_partner/) | 17.0.1.0.9 |  | Adds payment mode on partners and invoices
[account_payment_purchase](account_payment_purchase/) | 17.0.1.2.3 |  | Adds Bank Account and Payment Mode on Purchase Orders
[account_payment_purchase_stock](account_payment_purchase_stock/) | 17.0.1.0.0 |  | Integrate Account Payment Purchase with Stock
[account_payment_sale](account_payment_sale/) | 17.0.1.0.4 |  | Adds payment mode on sale orders
[account_vendor_bank_account_default](account_vendor_bank_account_default/) | 17.0.1.0.1 | <a href='https://github.com/tisho99'><img src='https://github.com/tisho99.png' width='32' height='32' style='border-radius:50%;' alt='tisho99'/></a> | Set a default bank account on partners for their vendor bills
[account_vendor_bank_account_default_purchase](account_vendor_bank_account_default_purchase/) | 17.0.1.0.0 | <a href='https://github.com/tisho99'><img src='https://github.com/tisho99.png' width='32' height='32' style='border-radius:50%;' alt='tisho99'/></a> | Set a default bank account purchase orders

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/bank-statement-import&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/bank-statement-import/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/bank-statement-import/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/bank-statement-import/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/bank-statement-import/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/bank-statement-import/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/bank-statement-import)
[![Translation Status](https://translation.odoo-community.org/widgets/bank-statement-import-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/bank-statement-import-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# OCA bank statement import modules for Odoo

This repository hosts additionnal parsers and import features for bank statements.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_statement_import_base](account_statement_import_base/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Base module for Bank Statement Import
[account_statement_import_camt](account_statement_import_camt/) | 17.0.1.0.1 |  | CAMT Format Bank Statements Import
[account_statement_import_camt54](account_statement_import_camt54/) | 17.0.1.0.0 |  | Bank Account Camt54 Import
[account_statement_import_file](account_statement_import_file/) | 17.0.1.0.2 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import Statement Files
[account_statement_import_file_reconcile_oca](account_statement_import_file_reconcile_oca/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import Statement Files and Go Direct to Reconciliation
[account_statement_import_move_line](account_statement_import_move_line/) | 17.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Import journal items into bank statement
[account_statement_import_ofx](account_statement_import_ofx/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import OFX Bank Statement
[account_statement_import_ofx_by_acctid](account_statement_import_ofx_by_acctid/) | 17.0.1.0.0 |  | Import OFX Bank Statement by ACCTID
[account_statement_import_online](account_statement_import_online/) | 17.0.1.1.2 | <a href='https://github.com/alexey-pelykh'><img src='https://github.com/alexey-pelykh.png' width='32' height='32' style='border-radius:50%;' alt='alexey-pelykh'/></a> | Online bank statements update
[account_statement_import_online_gocardless](account_statement_import_online_gocardless/) | 17.0.1.0.5 |  | Online Bank Statements: GoCardless
[account_statement_import_online_paypal](account_statement_import_online_paypal/) | 17.0.1.0.2 | <a href='https://github.com/alexey-pelykh'><img src='https://github.com/alexey-pelykh.png' width='32' height='32' style='border-radius:50%;' alt='alexey-pelykh'/></a> | Online bank statements for PayPal.com
[account_statement_import_online_plaid](account_statement_import_online_plaid/) | 17.0.1.0.0 |  | Online Bank Statements: plaid.com
[account_statement_import_online_ponto](account_statement_import_online_ponto/) | 17.0.1.1.1 |  | Online Bank Statements: MyPonto.com
[account_statement_import_online_stripe](account_statement_import_online_stripe/) | 17.0.1.0.2 | <a href='https://github.com/juancarlosonate-tecnativa'><img src='https://github.com/juancarlosonate-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='juancarlosonate-tecnativa'/></a> | Online bank statements for Stripe
[account_statement_import_paypal](account_statement_import_paypal/) | 17.0.1.0.0 |  | Import PayPal CSV files as Bank Statements in Odoo
[account_statement_import_sheet_file](account_statement_import_sheet_file/) | 17.0.1.2.0 | <a href='https://github.com/alexey-pelykh'><img src='https://github.com/alexey-pelykh.png' width='32' height='32' style='border-radius:50%;' alt='alexey-pelykh'/></a> | Import TXT/CSV or XLSX files as Bank Statements in Odoo

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/brand&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/brand/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/brand/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/brand/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/brand/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/brand/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/brand)
[![Translation Status](https://translation.odoo-community.org/widgets/brand-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/brand-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# brand

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_brand](account_brand/) | 17.0.1.0.0 | <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Send branded invoices and refunds
[analytic_brand](analytic_brand/) | 17.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This addon associate an analytic account to a brand that will be used as a default value where the brand is used if the analytic accounting is activated
[brand](brand/) | 17.0.1.1.1 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This is a base addon for brand modules. It adds the brand object and its menu and define an abstract model to be inherited from branded objects
[partner_brand](partner_brand/) | 17.0.1.0.0 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Define registered mark in partners according to brand settings
[product_brand](product_brand/) | 17.0.1.2.0 |  | Product Brand Manager
[product_brand_purchase](product_brand_purchase/) | 17.0.1.0.0 |  | This module allows to work with product_brand in purchase reports.
[sale_brand](sale_brand/) | 17.0.1.0.0 | <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Send branded sales orders

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/calendar&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/calendar/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/calendar/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/calendar/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/calendar/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/calendar/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/calendar)
[![Translation Status](https://translation.odoo-community.org/widgets/calendar-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/calendar-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# calendar

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[calendar_event_description_layout](calendar_event_description_layout/) | 17.0.1.0.0 |  | Adjusts the layout of the calendar event form by placing the description field in its own page.
[resource_booking](resource_booking/) | 17.0.1.1.4 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/ows-cloud'><img src='https://github.com/ows-cloud.png' width='32' height='32' style='border-radius:50%;' alt='ows-cloud'/></a> | Manage appointments and resource booking

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/commission&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/commission/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/commission/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/commission/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/commission/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/commission/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/commission)
[![Translation Status](https://translation.odoo-community.org/widgets/commission-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/commission-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# commission

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_commission](account_commission/) | 17.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Account commissions
[commission](commission/) | 17.0.1.1.2 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Commissions
[commission_formula](commission_formula/) | 17.0.1.0.0 |  | Commissions computed by formulas
[hr_commission](hr_commission/) | 17.0.1.0.0 |  | HR commissions
[sale_commission](sale_commission/) | 17.0.1.1.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Sales commissions
[sale_commission_pricelist](sale_commission_pricelist/) | 17.0.1.0.0 |  | Sales commissions by pricelist
[sale_commission_salesman](sale_commission_salesman/) | 17.0.1.0.1 |  | Sales commissions from salesman

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/community-data-files&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/community-data-files/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/community-data-files/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/community-data-files/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/community-data-files/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/community-data-files/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/community-data-files)
[![Translation Status](https://translation.odoo-community.org/widgets/community-data-files-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/community-data-files-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# community-data-files

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_payment_unece](account_payment_unece/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | UNECE nomenclature for the payment methods
[account_tax_unece](account_tax_unece/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | UNECE nomenclature for taxes
[base_bank_from_iban](base_bank_from_iban/) | 17.0.1.0.4 |  | Bank from IBAN
[base_currency_iso_4217](base_currency_iso_4217/) | 17.0.1.0.0 |  | Adds numeric code and full name to currencies, following the ISO 4217 specification
[base_iso3166](base_iso3166/) | 17.0.1.0.1 |  | ISO 3166
[base_unece](base_unece/) | 17.0.1.0.0 | <a href='https://github.com/astirpe'><img src='https://github.com/astirpe.png' width='32' height='32' style='border-radius:50%;' alt='astirpe'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Base module for UNECE code lists
[company_sanitary_registry](company_sanitary_registry/) | 17.0.1.0.0 |  | Sanitary Registry
[l10n_eu_nace](l10n_eu_nace/) | 17.0.1.0.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | European NACE partner categories
[l10n_eu_product_adr](l10n_eu_product_adr/) | 17.0.1.0.0 |  | Allows to set appropriate danger class and components
[l10n_eu_product_adr_dangerous_goods](l10n_eu_product_adr_dangerous_goods/) | 17.0.1.0.0 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | l10n Eu Product Adr Dangerous Goods
[product_fao_fishing](product_fao_fishing/) | 17.0.1.0.0 |  | Set fishing areas and capture technology
[uom_unece](uom_unece/) | 17.0.1.0.0 | <a href='https://github.com/astirpe'><img src='https://github.com/astirpe.png' width='32' height='32' style='border-radius:50%;' alt='astirpe'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | UNECE nomenclature for the units of measure

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/connector&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/connector/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/connector/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/connector/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/connector/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/connector/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/connector)
[![Translation Status](https://translation.odoo-community.org/widgets/connector-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/connector-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# connector

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[component](component/) | 17.0.1.0.1 | <a href='https://github.com/guewen'><img src='https://github.com/guewen.png' width='32' height='32' style='border-radius:50%;' alt='guewen'/></a> | Add capabilities to register and use decoupled components, as an alternative to model classes
[component_event](component_event/) | 17.0.1.0.1 |  | Components Events
[connector](connector/) | 17.0.1.0.2 |  | Connector
[connector_base_product](connector_base_product/) | 17.0.1.0.0 |  | Connector Base Product
[test_component](test_component/) | 17.0.1.0.1 | <a href='https://github.com/guewen'><img src='https://github.com/guewen.png' width='32' height='32' style='border-radius:50%;' alt='guewen'/></a> | Automated tests for Components, do not install.
[test_connector](test_connector/) | 17.0.1.0.0 |  | Automated tests for Connector, do not install.

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/connector-interfaces&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/connector-interfaces/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/connector-interfaces/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/connector-interfaces/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/connector-interfaces/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/connector-interfaces/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/connector-interfaces)
[![Translation Status](https://translation.odoo-community.org/widgets/connector-interfaces-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/connector-interfaces-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# connector-interfaces

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[connector_importer](connector_importer/) | 17.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | This module takes care of import sessions.
[connector_importer_product](connector_importer_product/) | 17.0.1.0.0 |  | Ease definition of product imports using `connector_importer`.

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

## From OCA/connector-jira


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/connector-jira&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/connector-jira/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/connector-jira/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/connector-jira/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/connector-jira/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/connector-jira/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/connector-jira)
[![Translation Status](https://translation.odoo-community.org/widgets/connector-jira-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/connector-jira-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# connector-jira

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[connector_jira](connector_jira/) | 17.0.1.0.0 |  | JIRA Connector
[connector_jira_servicedesk](connector_jira_servicedesk/) | 17.0.1.0.0 |  | JIRA Connector - Service Desk Extension

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/connector-telephony&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/connector-telephony/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/connector-telephony/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/connector-telephony/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/connector-telephony/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/connector-telephony/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/connector-telephony)
[![Translation Status](https://translation.odoo-community.org/widgets/connector-telephony-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/connector-telephony-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# connector-telephony

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[asterisk_click2dial](asterisk_click2dial/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Asterisk-Odoo connector
[base_phone](base_phone/) | 17.0.1.0.2 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Validate phone numbers
[voip_oca](voip_oca/) | 17.0.1.0.3 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Provides the use of Voip

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/contract&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/contract/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/contract/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/contract/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/contract/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/contract/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/contract)
[![Translation Status](https://translation.odoo-community.org/widgets/contract-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/contract-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# contract

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[contract](contract/) | 17.0.1.5.4 |  | Recurring - Contracts Management
[contract_analytic_tag](contract_analytic_tag/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Contract Analytic Tag
[contract_invoice_auto_validate](contract_invoice_auto_validate/) | 17.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This addon auto-validate invoices after its creation from a contract
[contract_invoice_start_end_dates](contract_invoice_start_end_dates/) | 17.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Contract Invoice Start End Dates
[contract_mandate](contract_mandate/) | 17.0.1.0.0 |  | Mandate in contracts and their invoices
[contract_payment_mode](contract_payment_mode/) | 17.0.1.0.0 |  | Payment mode in contracts and their invoices
[contract_price_revision](contract_price_revision/) | 17.0.1.0.0 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> | Easy revision of contract prices
[contract_queue_job](contract_queue_job/) | 17.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> <a href='https://github.com/BurkhalterY'><img src='https://github.com/BurkhalterY.png' width='32' height='32' style='border-radius:50%;' alt='BurkhalterY'/></a> | This addon make contract invoicing cron plan each contract in a job instead of creating all invoices in one transaction
[contract_sale](contract_sale/) | 17.0.1.0.0 |  | Contract from Sale
[contract_sale_invoicing](contract_sale_invoicing/) | 17.0.1.1.0 |  | Include sales to invoice in contract invoice creation
[contract_update_last_date_invoiced](contract_update_last_date_invoiced/) | 17.0.1.0.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | This module allows to update the last date invoiced if invoices are deleted.
[contract_variable_qty_timesheet](contract_variable_qty_timesheet/) | 17.0.1.0.0 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/danypr92'><img src='https://github.com/danypr92.png' width='32' height='32' style='border-radius:50%;' alt='danypr92'/></a> | Add formula to invoice
[contract_variable_quantity](contract_variable_quantity/) | 17.0.1.0.2 |  | Variable quantity in contract recurrent invoicing
[product_contract](product_contract/) | 17.0.2.3.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Recurring - Product Contract
[subscription_oca](subscription_oca/) | 17.0.1.0.0 |  | Generate recurring invoices.

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/credit-control&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/credit-control/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/credit-control/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/credit-control/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/credit-control/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/credit-control/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/credit-control)
[![Translation Status](https://translation.odoo-community.org/widgets/credit-control-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/credit-control-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# credit-control

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_credit_control](account_credit_control/) | 17.0.2.2.6 |  | Account Credit Control
[account_credit_control_dunning_fees](account_credit_control_dunning_fees/) | 17.0.1.0.0 |  | Credit control dunning fees
[account_financial_risk](account_financial_risk/) | 17.0.1.3.0 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> | Manage customer risk
[account_invoice_overdue_reminder](account_invoice_overdue_reminder/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Simple mail/letter/phone overdue customer invoice reminder
[account_invoice_overdue_warn](account_invoice_overdue_warn/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Show warning on customer form view if it has overdue invoices
[account_invoice_overdue_warn_sale](account_invoice_overdue_warn_sale/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Show overdue warning on sale order form view
[account_payment_return_financial_risk](account_payment_return_financial_risk/) | 17.0.1.0.0 |  | Partner Payment Return Risk
[partner_risk_insurance](partner_risk_insurance/) | 17.0.1.0.0 | <a href='https://github.com/Daniel-CA'><img src='https://github.com/Daniel-CA.png' width='32' height='32' style='border-radius:50%;' alt='Daniel-CA'/></a> <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/omar7r'><img src='https://github.com/omar7r.png' width='32' height='32' style='border-radius:50%;' alt='omar7r'/></a> <a href='https://github.com/Tardo'><img src='https://github.com/Tardo.png' width='32' height='32' style='border-radius:50%;' alt='Tardo'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Risk insurance partner information
[sale_financial_risk](sale_financial_risk/) | 17.0.1.0.4 |  | Manage partner risk in sales orders
[sale_financial_risk_info](sale_financial_risk_info/) | 17.0.1.0.0 |  | Adds risk consumption info in sales orders.

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/crm&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/crm/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/crm/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/crm/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/crm/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/crm/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/crm)
[![Translation Status](https://translation.odoo-community.org/widgets/crm-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/crm-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# crm

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[crm_claim](crm_claim/) | 17.0.1.0.1 |  | Track your customers/vendors claims and grievances.
[crm_claim_code](crm_claim_code/) | 17.0.1.0.0 |  | Sequential Code for Claims
[crm_claim_type](crm_claim_type/) | 17.0.1.0.0 |  | Claim types for CRM
[crm_exception](crm_exception/) | 17.0.1.0.0 |  | CRM Exception
[crm_industry](crm_industry/) | 17.0.1.0.1 |  | Link leads/opportunities to industries
[crm_lead_code](crm_lead_code/) | 17.0.1.1.1 |  | Sequential Code for Leads / Opportunities
[crm_lead_currency](crm_lead_currency/) | 17.0.1.0.1 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | On leads/opportunities, add the amount in the customer's currency.
[crm_lead_firstname](crm_lead_firstname/) | 17.0.1.0.1 |  | Specify split names for contacts in leads
[crm_lead_product](crm_lead_product/) | 17.0.1.0.1 |  | Adds a lead line in the lead/opportunity model in odoo
[crm_lead_to_task](crm_lead_to_task/) | 17.0.1.1.0 |  | Create Tasks from Leads/Opportunities
[crm_lead_vat](crm_lead_vat/) | 17.0.1.0.2 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Add VAT field to leads
[crm_location](crm_location/) | 17.0.1.0.0 |  | CRM location
[crm_partner_assign](crm_partner_assign/) | 17.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Assign a Partner to an Opportunity/Lead/Partner to indicate Partnership
[crm_phonecall](crm_phonecall/) | 17.0.1.0.0 |  | CRM Phone Calls
[crm_phonecall_summary_predefined](crm_phonecall_summary_predefined/) | 17.0.1.0.0 |  | Allows to choose from a defined summary list
[crm_project_task](crm_project_task/) | 17.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Create tasks from lead or opportunity
[crm_salesperson_planner](crm_salesperson_planner/) | 17.0.1.1.0 |  | Crm Salesperson Planner
[crm_stage_probability](crm_stage_probability/) | 17.0.1.0.0 |  | Define fixed probability on the stages
[marketing_crm_partner](marketing_crm_partner/) | 17.0.1.0.0 |  | Copy tracking fields from leads to partners

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/currency&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/currency/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/currency/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/currency/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/currency/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/currency/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/currency)
[![Translation Status](https://translation.odoo-community.org/widgets/currency-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/currency-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# currency

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[currency_rate_update](currency_rate_update/) | 17.0.1.0.1 |  | Update exchange rates using OCA modules
[currency_rate_update_xe](currency_rate_update_xe/) | 17.0.1.0.0 |  | Update exchange rates using XE.com

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/data-protection&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/data-protection/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/data-protection/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/data-protection/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/data-protection/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/data-protection/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/data-protection)
[![Translation Status](https://translation.odoo-community.org/widgets/data-protection-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/data-protection-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# data-protection

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[privacy](privacy/) | 17.0.1.0.0 |  | Provides data privacy and protection features to comply to regulations, such as GDPR.
[privacy_consent](privacy_consent/) | 17.0.1.0.1 |  | Allow people to explicitly accept or reject inclusion in some activity, GDPR compliant
[privacy_partner_to_be_forgotten](privacy_partner_to_be_forgotten/) | 17.0.1.0.0 |  | Anonymize partner data for GDPR compliance

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/ddmrp&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/ddmrp/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/ddmrp/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/ddmrp/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/ddmrp/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/ddmrp/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/ddmrp)
[![Translation Status](https://translation.odoo-community.org/widgets/ddmrp-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/ddmrp-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# ddmrp

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[ddmrp](ddmrp/) | 17.0.1.9.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Demand Driven Material Requirements Planning
[ddmrp_adjustment](ddmrp_adjustment/) | 17.0.1.2.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Allow to apply factor adjustments to buffers.
[ddmrp_chatter](ddmrp_chatter/) | 17.0.1.0.0 |  | Adds chatter and activities to stock buffers.
[ddmrp_cron_actions_as_job](ddmrp_cron_actions_as_job/) | 17.0.1.0.1 |  | Run DDMRP Buffer Calculation as jobs
[ddmrp_exclude_moves_adu_calc](ddmrp_exclude_moves_adu_calc/) | 17.0.1.1.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Define additional rules to exclude certain moves from ADU calculation
[ddmrp_exclude_moves_adu_calc_sales](ddmrp_exclude_moves_adu_calc_sales/) | 17.0.2.0.0 | <a href='https://github.com/DavidJForgeFlow'><img src='https://github.com/DavidJForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='DavidJForgeFlow'/></a> | DDMRP Exclude Moves ADU Calc integration with Sales app.
[ddmrp_history](ddmrp_history/) | 17.0.1.0.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Allow to store historical data of DDMRP buffers.
[ddmrp_include_location_final](ddmrp_include_location_final/) | 17.0.1.0.0 | <a href='https://github.com/DavidJForgeFlow'><img src='https://github.com/DavidJForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='DavidJForgeFlow'/></a> | This module implements the final location logic of v18 added in v17 by stock_push_delay to DDMRP logic.
[ddmrp_product_replace](ddmrp_product_replace/) | 17.0.1.2.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Provides a assisting tool for product replacement.
[ddmrp_report_part_flow_index](ddmrp_report_part_flow_index/) | 17.0.1.0.1 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Provides the DDMRP Parts Flow Index Report
[ddmrp_warning](ddmrp_warning/) | 17.0.1.1.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Adds configuration warnings on stock buffers.
[ddmrp_warning_as_job](ddmrp_warning_as_job/) | 17.0.1.0.0 |  | Run DDMRP Warning as jobs

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/delivery-carrier&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/delivery-carrier/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/delivery-carrier/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/delivery-carrier/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/delivery-carrier/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/delivery-carrier/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/delivery-carrier)
[![Translation Status](https://translation.odoo-community.org/widgets/delivery-carrier-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/delivery-carrier-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# delivery-carrier

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_delivery_carrier_label](base_delivery_carrier_label/) | 17.0.1.1.0 |  | Base module for carrier labels
[delivery_auto_refresh](delivery_auto_refresh/) | 17.0.1.0.0 |  | Auto-refresh delivery price in sales orders
[delivery_carrier_account](delivery_carrier_account/) | 17.0.1.0.0 |  | Delivery Carrier Account
[delivery_carrier_agency](delivery_carrier_agency/) | 17.0.1.0.0 |  | Add a model for Carrier Agencies
[delivery_carrier_global_manifest](delivery_carrier_global_manifest/) | 17.0.1.0.0 | <a href='https://github.com/tisho99'><img src='https://github.com/tisho99.png' width='32' height='32' style='border-radius:50%;' alt='tisho99'/></a> | Manifest files for all carriers
[delivery_carrier_info](delivery_carrier_info/) | 17.0.1.0.0 |  | Add code on carrier
[delivery_carrier_manual_price](delivery_carrier_manual_price/) | 17.0.1.0.0 |  | Allow setting manual shipping cost in sale order.
[delivery_carrier_manual_weight](delivery_carrier_manual_weight/) | 17.0.1.0.0 |  | Allow setting weight and shipping weight in stock transfers manually based on carrier.
[delivery_carrier_multi_zip](delivery_carrier_multi_zip/) | 17.0.1.0.0 |  | Multiple ZIP intervals for the same delivery method
[delivery_carrier_partner](delivery_carrier_partner/) | 17.0.1.0.0 |  | Add a partner in the delivery carrier
[delivery_cbl](delivery_cbl/) | 17.0.2.0.1 |  | Integrate CBL webservice
[delivery_correos_express](delivery_correos_express/) | 17.0.1.0.0 |  | Delivery Carrier implementation for Correos Express using their API
[delivery_cttexpress](delivery_cttexpress/) | 17.0.1.0.1 |  | Delivery Carrier implementation for CTT Express API
[delivery_driver](delivery_driver/) | 17.0.1.0.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Allow choose driver in delivery methods
[delivery_easypost_oca](delivery_easypost_oca/) | 17.0.1.0.0 |  | OCA Delivery Easypost
[delivery_estimated_package_quantity_by_weight](delivery_estimated_package_quantity_by_weight/) | 17.0.1.0.0 |  | Compute the amount of packages a picking out should have depending on the weight of the products and the limit fixed by the carrier
[delivery_free_fee_removal](delivery_free_fee_removal/) | 17.0.1.0.0 |  | Hide free fee lines on sales orders
[delivery_multi_destination](delivery_multi_destination/) | 17.0.1.0.1 |  | Multiple destinations for the same delivery method
[delivery_package_number](delivery_package_number/) | 17.0.1.0.0 |  | Set or compute number of packages for a picking
[delivery_package_type_number_parcels](delivery_package_type_number_parcels/) | 17.0.1.0.0 |  | Number of parcels in a package type
[delivery_price_method](delivery_price_method/) | 17.0.1.0.0 |  | Force a fixed or rule price calculation on Delivery Methods, for example to override a webservice provided prices.
[delivery_purchase](delivery_purchase/) | 17.0.1.0.0 |  | Delivery costs in purchases
[delivery_purchase_multi_destination](delivery_purchase_multi_destination/) | 17.0.1.0.0 |  | Multiple origins for delivery costs in purchases
[delivery_roulier](delivery_roulier/) | 17.0.1.0.1 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Integration of multiple carriers
[delivery_roulier_option](delivery_roulier_option/) | 17.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Add options to roulier modules
[delivery_schenker](delivery_schenker/) | 17.0.1.0.0 |  | Delivery Carrier implementation for DB Schenker API
[delivery_sendcloud_oca](delivery_sendcloud_oca/) | 17.0.1.0.0 |  | Compute shipping costs and ship with Sendcloud
[delivery_state](delivery_state/) | 17.0.1.0.0 |  | Provides fields to be able to contemplate the tracking statesand also adds a global fields
[delivery_ups_oca](delivery_ups_oca/) | 17.0.1.0.0 |  | Integrate UPS webservice
[partner_delivery_info](partner_delivery_info/) | 17.0.1.0.0 |  | Send delivery notice to the shipper from any operation.
[partner_delivery_schedule](partner_delivery_schedule/) | 17.0.1.0.0 |  | Set on partners a schedule for delivery goods
[partner_delivery_zone](partner_delivery_zone/) | 17.0.1.0.1 |  | Enables partner delivery zones for physical products
[sale_order_warehouse_from_delivery_carrier](sale_order_warehouse_from_delivery_carrier/) | 17.0.1.0.0 |  | Sale Order WH from Delivery Carrier
[stock_picking_report_delivery_cost](stock_picking_report_delivery_cost/) | 17.0.1.0.0 |  | Show delivery cost in delivery slip and picking operations reports

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/dms&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/dms/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/dms/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/dms/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/dms/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/dms/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/dms)
[![Translation Status](https://translation.odoo-community.org/widgets/dms-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/dms-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# dms

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[dms](dms/) | 17.0.1.2.5 |  | Document Management System for Odoo
[dms_attachment_link](dms_attachment_link/) | 17.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Dms Attachment Link
[dms_file_sequence](dms_file_sequence/) | 17.0.1.0.1 | <a href='https://github.com/miquelalzanillas'><img src='https://github.com/miquelalzanillas.png' width='32' height='32' style='border-radius:50%;' alt='miquelalzanillas'/></a> <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Dms File Sequence
[dms_storage](dms_storage/) | 17.0.1.0.0 |  | Integrate DMS with external Storages

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/e-commerce&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/e-commerce/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/e-commerce/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/e-commerce/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/e-commerce/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/e-commerce/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/e-commerce)
[![Translation Status](https://translation.odoo-community.org/widgets/e-commerce-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/e-commerce-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# e-commerce

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[website_sale_b2x_alt_price](website_sale_b2x_alt_price/) | 17.0.1.0.0 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Display prices with(out) taxes in eCommerce, complementing normal mode
[website_sale_barcode_search](website_sale_barcode_search/) | 17.0.1.0.0 |  | It improve website product search adding search by barcode
[website_sale_cart_add_product_xlsx_csv](website_sale_cart_add_product_xlsx_csv/) | 17.0.1.0.1 |  | Adds button to import xlsx or csv in website cart
[website_sale_checkout_skip_payment](website_sale_checkout_skip_payment/) | 17.0.1.0.1 |  | Skip payment for logged users in checkout process
[website_sale_comparison_hide_price](website_sale_comparison_hide_price/) | 17.0.1.0.0 |  | Hide product prices on the shop
[website_sale_empty_cart](website_sale_empty_cart/) | 17.0.1.0.0 |  | Adds a button in the website cart to empty all
[website_sale_hide_empty_category](website_sale_hide_empty_category/) | 17.0.1.0.2 |  | Hide any Product Categories that are empty
[website_sale_hide_price](website_sale_hide_price/) | 17.0.1.2.1 |  | Hide product prices on the shop
[website_sale_menu_partner_top_selling](website_sale_menu_partner_top_selling/) | 17.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Displays the user's regular products in the e-commerce.
[website_sale_order_type](website_sale_order_type/) | 17.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | This module allows sale_order_type to work with website_sale.
[website_sale_product_attachment](website_sale_product_attachment/) | 17.0.1.0.0 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Let visitors download attachments from a product page
[website_sale_product_attribute_filter_category](website_sale_product_attribute_filter_category/) | 17.0.1.0.0 |  | Allow group attributes in shop by categories
[website_sale_product_attribute_filter_order](website_sale_product_attribute_filter_order/) | 17.0.1.0.0 | <a href='https://github.com/Tardo'><img src='https://github.com/Tardo.png' width='32' height='32' style='border-radius:50%;' alt='Tardo'/></a> | Move active checkbox options to the first place of the list
[website_sale_product_attribute_value_filter_existing](website_sale_product_attribute_value_filter_existing/) | 17.0.1.1.1 |  | Allow hide attributes values not used in variants
[website_sale_product_brand](website_sale_product_brand/) | 17.0.1.0.0 |  | Product Brand Filtering in Website
[website_sale_product_description](website_sale_product_description/) | 17.0.1.0.0 |  | Shows custom e-Commerce description for products
[website_sale_product_detail_attribute_image](website_sale_product_detail_attribute_image/) | 17.0.1.0.0 |  | Display attributes images in shop product detail
[website_sale_product_matrix](website_sale_product_matrix/) | 17.0.1.0.2 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Product matrix in eCommerce
[website_sale_product_matrix_hide_price](website_sale_product_matrix_hide_price/) | 17.0.1.0.0 |  | Hide product prices on the shop
[website_sale_product_minimal_price](website_sale_product_minimal_price/) | 17.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Display minimal price for products that has variants
[website_sale_product_minimal_price_hide_price](website_sale_product_minimal_price_hide_price/) | 17.0.1.0.0 |  | Hide the product price scale when website prices are hidden
[website_sale_product_multi_website](website_sale_product_multi_website/) | 17.0.1.0.2 |  | Show products in many websites
[website_sale_product_reference_displayed](website_sale_product_reference_displayed/) | 17.0.1.0.0 |  | Display product reference in e-commerce
[website_sale_require_legal](website_sale_require_legal/) | 17.0.1.0.0 |  | Force the user to accept legal tems to buy in the web shop
[website_sale_resource_booking](website_sale_resource_booking/) | 17.0.1.0.0 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Let customers book resources temporarily before buying
[website_sale_secondary_unit](website_sale_secondary_unit/) | 17.0.1.0.0 |  | Allow manage secondary units in website shop
[website_sale_secondary_unit_product_matrix](website_sale_secondary_unit_product_matrix/) | 17.0.1.0.2 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Product matrix with secondary units in eCommerce
[website_sale_stock_available](website_sale_stock_available/) | 17.0.1.0.0 |  | Display 'Available to promise' in shop online instead of 'Free To Use Quantity'
[website_sale_stock_product_matrix](website_sale_stock_product_matrix/) | 17.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Stock hints in eCommerce product matrix
[website_sale_stock_provisioning_date](website_sale_stock_provisioning_date/) | 17.0.1.0.0 |  | Display provisioning date for a product in shop online
[website_sale_suggest_create_account](website_sale_suggest_create_account/) | 17.0.1.0.0 |  | Suggest users to create an account when buying in the website
[website_sale_vat_required](website_sale_vat_required/) | 17.0.1.0.0 |  | VAT number required in checkout form
[website_sale_wishlist_hide_price](website_sale_wishlist_hide_price/) | 17.0.1.0.0 |  | Hide product prices on the shop
[website_sale_wishlist_keep](website_sale_wishlist_keep/) | 17.0.1.0.0 |  | Allows to add products to my cart but keep it in my wishlist"
[website_snippet_product_category](website_snippet_product_category/) | 17.0.1.1.0 | <a href='https://github.com/Tardo'><img src='https://github.com/Tardo.png' width='32' height='32' style='border-radius:50%;' alt='Tardo'/></a> | Adds a new snippet to show e-commerce categories

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

## From OCA/e-learning


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/e-learning&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/e-learning/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/e-learning/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/e-learning/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/e-learning/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/e-learning/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/e-learning)
[![Translation Status](https://translation.odoo-community.org/widgets/e-learning-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/e-learning-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# e-learning

e-learning

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[website_sale_slides_order_line_link](website_sale_slides_order_line_link/) | 17.0.1.0.1 |  | Link sales order lines to slide channel participations in sold courses.

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/edi&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/edi/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/edi/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/edi/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/edi/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/edi/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/edi)
[![Translation Status](https://translation.odoo-community.org/widgets/edi-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/edi-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# edi

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_einvoice_generate](account_einvoice_generate/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Technical module to generate PDF invoices with embedded XML file
[account_invoice_export](account_invoice_export/) | 17.0.1.0.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Account Invoice Export
[account_invoice_facturx](account_invoice_facturx/) | 17.0.1.2.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Generate Factur-X/ZUGFeRD customer invoices
[base_business_document_import](base_business_document_import/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Provides technical tools to import sale orders or supplier invoices
[base_ebill_payment_contract](base_ebill_payment_contract/) | 17.0.1.0.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Base for managing e-billing contracts
[base_edi](base_edi/) | 17.0.1.1.1 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Base module to aggregate EDI features.
[base_facturx](base_facturx/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Base module for Factur-X/ZUGFeRD
[base_import_pdf_by_template](base_import_pdf_by_template/) | 17.0.1.2.11 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Base Import Pdf by Template
[base_import_pdf_by_template_account](base_import_pdf_by_template_account/) | 17.0.1.0.8 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Base Import Pdf by Template Account
[base_ubl](base_ubl/) | 17.0.1.0.1 |  | Base module for Universal Business Language (UBL)
[pdf_helper](pdf_helper/) | 17.0.1.0.1 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Provides helpers to work w/ PDFs
[test_base_import_pdf_by_template](test_base_import_pdf_by_template/) | 17.0.1.1.2 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Test Base Import Pdf by Template

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

## From OCA/edi-ediversa


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/edi-ediversa&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/edi-ediversa/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/edi-ediversa/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/edi-ediversa/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/edi-ediversa/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/edi-ediversa/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/edi-ediversa)
[![Translation Status](https://translation.odoo-community.org/widgets/edi-ediversa-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/edi-ediversa-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# edi-ediversa

edi-ediversa

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[edi_ediversa_oca](edi_ediversa_oca/) | 17.0.1.0.0 | <a href='https://github.com/ValentinVinagre'><img src='https://github.com/ValentinVinagre.png' width='32' height='32' style='border-radius:50%;' alt='ValentinVinagre'/></a> | Ediversa - Base Module
[edi_ediversa_oca_invoice_send](edi_ediversa_oca_invoice_send/) | 17.0.1.0.1 | <a href='https://github.com/ValentinVinagre'><img src='https://github.com/ValentinVinagre.png' width='32' height='32' style='border-radius:50%;' alt='ValentinVinagre'/></a> | Send customer invoices to Ediversa
[edi_ediversa_oca_sale_order_import](edi_ediversa_oca_sale_order_import/) | 17.0.1.0.0 | <a href='https://github.com/ValentinVinagre'><img src='https://github.com/ValentinVinagre.png' width='32' height='32' style='border-radius:50%;' alt='ValentinVinagre'/></a> | Process sale orders from Ediversa

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/edi-framework&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/edi-framework/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/edi-framework/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/edi-framework/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/edi-framework/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/edi-framework/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/edi-framework)
[![Translation Status](https://translation.odoo-community.org/widgets/edi-framework-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/edi-framework-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# edi-framework

{'TODO': 'add repo description.'}

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[edi_account_oca](edi_account_oca/) | 17.0.1.0.0 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Define EDI Configuration for Account Moves
[edi_endpoint_oca](edi_endpoint_oca/) | 17.0.1.0.0 |  | Base module allowing configuration of custom endpoints for EDI framework.
[edi_exchange_template_oca](edi_exchange_template_oca/) | 17.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Allows definition of exchanges via templates.
[edi_oca](edi_oca/) | 17.0.1.3.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Define backends, exchange types, exchange records, basic automation and views for handling EDI exchanges.
[edi_project_oca](edi_project_oca/) | 17.0.1.0.0 |  | Define EDI Configuration for Projects and Tasks
[edi_record_metadata_oca](edi_record_metadata_oca/) | 17.0.1.0.1 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Allow to store metadata for related records.
[edi_storage_oca](edi_storage_oca/) | 17.0.1.0.0 |  | Base module to allow exchanging files via storage backend (eg: SFTP).
[edi_webservice_oca](edi_webservice_oca/) | 17.0.1.0.1 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Defines webservice integration from EDI Exchange records

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/edi-voxel&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/edi-voxel/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/edi-voxel/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/edi-voxel/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/edi-voxel/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/edi-voxel/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/edi-voxel)
[![Translation Status](https://translation.odoo-community.org/widgets/edi-voxel-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/edi-voxel-17-0/?utm_source=widget)

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
[edi_voxel_account_invoice_oca](edi_voxel_account_invoice_oca/) | 17.0.1.0.1 |  | Sends account invoices to Voxel.
[edi_voxel_oca](edi_voxel_oca/) | 17.0.1.0.1 |  | Base module for connecting with Voxel
[edi_voxel_sale_order_import_oca](edi_voxel_sale_order_import_oca/) | 17.0.1.0.0 |  | Import sale order from Voxel.

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/event&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/event/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/event/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/event/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/event/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/event/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/event)
[![Translation Status](https://translation.odoo-community.org/widgets/event-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/event-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# event

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[crm_event](crm_event/) | 17.0.1.0.1 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Link opportunities to event categories
[event_email_reminder](event_email_reminder/) | 17.0.1.0.0 |  | Send an email before an event start
[event_mail](event_mail/) | 17.0.1.0.0 |  | Mail settings in events
[event_min_seat](event_min_seat/) | 17.0.1.0.0 |  | Minimum seats in events
[event_project](event_project/) | 17.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Event project
[event_registration_cancel_reason](event_registration_cancel_reason/) | 17.0.1.0.0 |  | Reasons for event registrations cancellations
[event_registration_partner_unique](event_registration_partner_unique/) | 17.0.1.0.0 |  | Enforces 1 registration per partner and event
[event_sale_free_no_invoiceable](event_sale_free_no_invoiceable/) | 17.0.1.0.0 |  | Free tickets no invoiceable
[event_sale_reservation](event_sale_reservation/) | 17.0.1.0.2 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Allow selling event registrations before the event exists
[event_sale_update_qty](event_sale_update_qty/) | 17.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Update event registrations from confirmed sale order lines.
[event_stage_cancelled](event_stage_cancelled/) | 17.0.1.0.0 |  | Event cancellation workflows
[event_track_location_overlap](event_track_location_overlap/) | 17.0.1.0.0 |  | Restrict event track location overlapping
[partner_event](partner_event/) | 17.0.1.1.1 |  | Link partner to events
[sale_crm_event_reservation](sale_crm_event_reservation/) | 17.0.1.0.2 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Combine event reservations, opportunities and quotations
[website_event_crm_invitation](website_event_crm_invitation/) | 17.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Invite leads to event types on website
[website_event_filter_city](website_event_filter_city/) | 17.0.1.1.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Add a customizable top area to filter events with city
[website_event_membership_restriction](website_event_membership_restriction/) | 17.0.1.0.0 |  | Restrict event registration to members only
[website_event_questions_by_ticket](website_event_questions_by_ticket/) | 17.0.1.0.0 |  | Events Questions conditional to the chosen ticket
[website_event_require_legal](website_event_require_legal/) | 17.0.1.0.0 |  | Website Event Require Legal
[website_event_require_login](website_event_require_login/) | 17.0.1.0.0 |  | Website Event Require Login
[website_event_ribbon](website_event_ribbon/) | 17.0.1.0.0 |  | Add ribbons on events
[website_event_sale_b2x_alt_price](website_event_sale_b2x_alt_price/) | 17.0.1.0.0 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Display alt. price (B2B for B2C websites, and viceversa)
[website_event_track_stage_cancelled](website_event_track_stage_cancelled/) | 17.0.1.0.0 |  | Event session cancellation workflows

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/field-service&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/field-service/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/field-service/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/field-service/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/field-service/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/field-service/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/field-service)
[![Translation Status](https://translation.odoo-community.org/widgets/field-service-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/field-service-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Field Service Management

[Field Service Management](https://en.wikipedia.org/wiki/Field_service_management) (FSM) coordinates company resources employed at, or en route to, client sites, rather than on the company's premises. FSM most commonly refers to companies who need to manage installation, service or repairs of systems or equipment.

Examples of field service use cases are:

- In telecommunications and cable industry, technicians who install cable or run phone lines into residences or business establishments.
- In healthcare, mobile nurses who provide in-home care for elderly or disabled.
- In gas utilities, engineers who are dispatched to investigate and repair suspected leaks.
- In heavy engineering, mining, industrial and manufacturing, technicians dispatched for preventative maintenance and repair.
- In property maintenance, including landscaping, irrigation, and home and office cleaning.
- In HVAC industry, technicians have the expertise and equipment to investigate units in residential, commercial and industrial environments.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_territory](base_territory/) | 17.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | This module allows you to define territories, branches, districts and regions to be used for Field Service operations or Sales.
[fieldservice](fieldservice/) | 17.0.2.8.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Manage Field Service Locations, Workers and Orders
[fieldservice_account](fieldservice_account/) | 17.0.1.1.0 | <a href='https://github.com/osimallen'><img src='https://github.com/osimallen.png' width='32' height='32' style='border-radius:50%;' alt='osimallen'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> | Track invoices linked to Field Service orders
[fieldservice_account_analytic](fieldservice_account_analytic/) | 17.0.1.1.0 | <a href='https://github.com/osimallen'><img src='https://github.com/osimallen.png' width='32' height='32' style='border-radius:50%;' alt='osimallen'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> | Track analytic accounts on Field Service locations and orders
[fieldservice_activity](fieldservice_activity/) | 17.0.1.1.2 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> | Field Service Activities are a set of actions that need to be performed on a service order
[fieldservice_address_no_change](fieldservice_address_no_change/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Prevents address changes in completed Field Service orders to preserve historical data.
[fieldservice_agreement](fieldservice_agreement/) | 17.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> <a href='https://github.com/patrickrwilson'><img src='https://github.com/patrickrwilson.png' width='32' height='32' style='border-radius:50%;' alt='patrickrwilson'/></a> | Manage Field Service agreements and contracts
[fieldservice_agreement_repair](fieldservice_agreement_repair/) | 17.0.1.0.0 |  | Fieldservice Agreement Repair
[fieldservice_availability](fieldservice_availability/) | 17.0.1.0.1 | <a href='https://github.com/ppyczko'><img src='https://github.com/ppyczko.png' width='32' height='32' style='border-radius:50%;' alt='ppyczko'/></a> | Provides models for defining blackout days, stress days, and delivery time ranges for FSM availability management.
[fieldservice_base_location](fieldservice_base_location/) | 17.0.1.0.0 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> | Autocomplete address in field service locations
[fieldservice_calendar](fieldservice_calendar/) | 17.0.1.0.0 | <a href='https://github.com/hparfr'><img src='https://github.com/hparfr.png' width='32' height='32' style='border-radius:50%;' alt='hparfr'/></a> | Add calendar to FSM Orders
[fieldservice_crm](fieldservice_crm/) | 17.0.1.2.0 | <a href='https://github.com/patrickrwilson'><img src='https://github.com/patrickrwilson.png' width='32' height='32' style='border-radius:50%;' alt='patrickrwilson'/></a> | Create Field Service orders from the CRM
[fieldservice_current_location](fieldservice_current_location/) | 17.0.1.1.2 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Use current location on fsm orders
[fieldservice_equipment_stock](fieldservice_equipment_stock/) | 17.0.1.0.0 | <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> | Integrate stock operations with your field service equipments
[fieldservice_equipment_stock_return](fieldservice_equipment_stock_return/) | 17.0.1.0.0 | <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> <a href='https://github.com/imlopes'><img src='https://github.com/imlopes.png' width='32' height='32' style='border-radius:50%;' alt='imlopes'/></a> | Integrate return orders for field service equipments
[fieldservice_fleet](fieldservice_fleet/) | 17.0.1.0.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Link Field Service vehicles with Odoo Fleet
[fieldservice_geoengine](fieldservice_geoengine/) | 17.0.1.2.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Display Field Service locations on a map with Open Street Map
[fieldservice_isp_flow](fieldservice_isp_flow/) | 17.0.1.0.0 | <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> | Field Service workflow for Internet Service Providers
[fieldservice_kanban_info](fieldservice_kanban_info/) | 17.0.1.0.0 | <a href='https://github.com/ppyczko'><img src='https://github.com/ppyczko.png' width='32' height='32' style='border-radius:50%;' alt='ppyczko'/></a> | Display key service information on Field Service Kanban cards.
[fieldservice_maintenance](fieldservice_maintenance/) | 17.0.1.0.0 | <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> | Integrate Field Service orders with maintenance requests
[fieldservice_portal](fieldservice_portal/) | 17.0.1.1.0 | <a href='https://github.com/aleuffre'><img src='https://github.com/aleuffre.png' width='32' height='32' style='border-radius:50%;' alt='aleuffre'/></a> <a href='https://github.com/renda-dev'><img src='https://github.com/renda-dev.png' width='32' height='32' style='border-radius:50%;' alt='renda-dev'/></a> | Bridge module between fieldservice and portal.
[fieldservice_project](fieldservice_project/) | 17.0.1.0.0 |  | Create field service orders from a project or project task
[fieldservice_recurring](fieldservice_recurring/) | 17.0.2.1.1 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Manage recurring Field Service orders
[fieldservice_repair](fieldservice_repair/) | 17.0.1.0.1 | <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Integrate Field Service orders with MRP repair orders
[fieldservice_repair_order_template](fieldservice_repair_order_template/) | 17.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Use Repair Order Templates when creating a repair orders
[fieldservice_route](fieldservice_route/) | 17.0.1.2.1 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Organize the routes of each day.
[fieldservice_route_availability](fieldservice_route_availability/) | 17.0.1.1.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Restricts blackout days for Scheduled Start (ETA) orders with the same date.
[fieldservice_sale](fieldservice_sale/) | 17.0.1.3.1 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Sell field services.
[fieldservice_sale_agreement](fieldservice_sale_agreement/) | 17.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Integrate Field Service with Sale Agreements
[fieldservice_sale_agreement_equipment_stock](fieldservice_sale_agreement_equipment_stock/) | 17.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Integrate Field Service with Sale Agreements and Stock Equipment
[fieldservice_sale_recurring](fieldservice_sale_recurring/) | 17.0.1.1.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Sell recurring field services.
[fieldservice_sale_stock](fieldservice_sale_stock/) | 17.0.1.1.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Sell stockable items linked to field service orders.
[fieldservice_sale_stock_from_pos](fieldservice_sale_stock_from_pos/) | 17.0.1.0.0 | <a href='https://github.com/borbrador'><img src='https://github.com/borbrador.png' width='32' height='32' style='border-radius:50%;' alt='borbrador'/></a> | Create Field Service Orders from POS Orders
[fieldservice_size](fieldservice_size/) | 17.0.1.0.1 | <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Manage Sizes for Field Service Locations and Orders
[fieldservice_skill](fieldservice_skill/) | 17.0.1.0.0 | <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Manage your Field Service workers skills
[fieldservice_stage_server_action](fieldservice_stage_server_action/) | 17.0.1.3.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> | Execute server actions when reaching a Field Service stage
[fieldservice_stage_validation](fieldservice_stage_validation/) | 17.0.1.1.0 | <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Validate input data when reaching a Field Service stage
[fieldservice_stock](fieldservice_stock/) | 17.0.1.2.0 | <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> | Integrate the logistics operations with Field Service
[fieldservice_stock_request](fieldservice_stock_request/) | 17.0.1.3.0 | <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> | Integrate Stock Requests with Field Service Orders
[fieldservice_stock_scrap](fieldservice_stock_scrap/) | 17.0.1.2.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Scrap stock from Field Service order of Stock Requests
[fieldservice_timeline](fieldservice_timeline/) | 17.0.1.0.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | This module is a display timeline view of the Field Service order in Odoo.
[fieldservice_vehicle](fieldservice_vehicle/) | 17.0.1.1.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Manage Field Service vehicles and assign drivers

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/fleet&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/fleet/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/fleet/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/fleet/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/fleet/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/fleet/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/fleet)
[![Translation Status](https://translation.odoo-community.org/widgets/fleet-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/fleet-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# fleet

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[fleet_vehicle_category](fleet_vehicle_category/) | 17.0.1.0.0 |  | Add category definition for vehicles.
[fleet_vehicle_fuel_capacity](fleet_vehicle_fuel_capacity/) | 17.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | This module extends the functionality of fleet management. It allows the registration of a vehicle's fuel capacity.
[fleet_vehicle_history_date_end](fleet_vehicle_history_date_end/) | 17.0.1.0.0 | <a href='https://github.com/mamcode'><img src='https://github.com/mamcode.png' width='32' height='32' style='border-radius:50%;' alt='mamcode'/></a> <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Automatically assign date end in vehicle history when a new driver is assigned.
[fleet_vehicle_inspection](fleet_vehicle_inspection/) | 17.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | This module extends the Fleet module allowing the registration of vehicle entry and exit inspections.
[fleet_vehicle_inspection_template](fleet_vehicle_inspection_template/) | 17.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | This module extend module fleet_vehicle_inspection enable inspection templates feature
[fleet_vehicle_service_services](fleet_vehicle_service_services/) | 17.0.1.0.0 |  | Add subservices in Services.
[fleet_vehicle_usage](fleet_vehicle_usage/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Fleet Vehicle Usage

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/geospatial&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/geospatial/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/geospatial/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/geospatial/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/geospatial/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/geospatial/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/geospatial)
[![Translation Status](https://translation.odoo-community.org/widgets/geospatial-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/geospatial-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# geospatial

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_geoengine](base_geoengine/) | 17.0.1.4.0 |  | Geospatial support for Odoo
[base_geoengine_demo](base_geoengine_demo/) | 17.0.1.0.1 |  | Geo spatial support Demo
[geoengine_base_geolocalize](geoengine_base_geolocalize/) | 17.0.1.0.0 |  | Geospatial support for base_geolocalize
[geoengine_partner](geoengine_partner/) | 17.0.1.0.0 |  | Geospatial support of partners
[web_leaflet_lib](web_leaflet_lib/) | 17.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Bring leaflet.js librairy in odoo.

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/helpdesk&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/helpdesk/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/helpdesk/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/helpdesk/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/helpdesk/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/helpdesk/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/helpdesk)
[![Translation Status](https://translation.odoo-community.org/widgets/helpdesk-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/helpdesk-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# helpdesk

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[helpdesk_mgmt](helpdesk_mgmt/) | 17.0.1.10.4 |  | Helpdesk
[helpdesk_mgmt_activity](helpdesk_mgmt_activity/) | 17.0.1.0.0 |  | Create Activities for Odoo records from the Helpdesk
[helpdesk_mgmt_assign_method](helpdesk_mgmt_assign_method/) | 17.0.1.0.0 |  | Helpdesk Assign Method
[helpdesk_mgmt_crm](helpdesk_mgmt_crm/) | 17.0.1.0.2 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Links helpdesk tickets with leads
[helpdesk_mgmt_merge](helpdesk_mgmt_merge/) | 17.0.1.0.0 |  | Wizard to merge helpdesk tickets
[helpdesk_mgmt_portal_follower](helpdesk_mgmt_portal_follower/) | 17.0.1.0.0 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> <a href='https://github.com/ppyczko'><img src='https://github.com/ppyczko.png' width='32' height='32' style='border-radius:50%;' alt='ppyczko'/></a> <a href='https://github.com/mpascuall'><img src='https://github.com/mpascuall.png' width='32' height='32' style='border-radius:50%;' alt='mpascuall'/></a> | Add ticket followers from website portal
[helpdesk_mgmt_project](helpdesk_mgmt_project/) | 17.0.1.0.1 |  | Add the option to select project in the tickets.
[helpdesk_mgmt_project_domain](helpdesk_mgmt_project_domain/) | 17.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Enable to set a project domain on ticket
[helpdesk_mgmt_rating](helpdesk_mgmt_rating/) | 17.0.1.0.2 |  | This module allows customer to rate the assistance received on a ticket.
[helpdesk_mgmt_sale](helpdesk_mgmt_sale/) | 17.0.1.0.2 |  | Add the option to select project in the sale orders.
[helpdesk_mgmt_sla](helpdesk_mgmt_sla/) | 17.0.1.0.0 |  | Add SLA to the tickets for Helpdesk Management.
[helpdesk_mgmt_stage_validation](helpdesk_mgmt_stage_validation/) | 17.0.1.1.0 |  | Validate input data when reaching a Helpdesk Ticket stage
[helpdesk_mgmt_team_partner](helpdesk_mgmt_team_partner/) | 17.0.1.0.0 |  | Allows dynamic control over which contact (partner_id) on ticket, based on the configuration of the assigned Helpdesk Team (team_id)
[helpdesk_mgmt_template](helpdesk_mgmt_template/) | 17.0.1.0.0 |  | Create Helpdesk Ticket Template
[helpdesk_mgmt_timesheet](helpdesk_mgmt_timesheet/) | 17.0.1.0.4 |  | Add HR Timesheet to the tickets for Helpdesk Management.
[helpdesk_mgmtsystem_nonconformity](helpdesk_mgmtsystem_nonconformity/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Links helpdesk tickets with nonconformities
[helpdesk_portal_restriction](helpdesk_portal_restriction/) | 17.0.1.0.0 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | Helpdesk Portal Restriction
[helpdesk_ticket_close_inactive](helpdesk_ticket_close_inactive/) | 17.0.1.1.2 | <a href='https://github.com/miquelalzanillas'><img src='https://github.com/miquelalzanillas.png' width='32' height='32' style='border-radius:50%;' alt='miquelalzanillas'/></a> | Helpdesk Ticket Close Inactive
[helpdesk_ticket_open_tab](helpdesk_ticket_open_tab/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Helpdesk Ticket Open Tab
[helpdesk_ticket_partner_response](helpdesk_ticket_partner_response/) | 17.0.1.0.2 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Change ticket stage when partner response
[helpdesk_ticket_related](helpdesk_ticket_related/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Link tickets to each other
[helpdesk_timesheet_time_type](helpdesk_timesheet_time_type/) | 17.0.1.0.0 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | Helpdesk Timesheet Time Type
[helpdesk_timesheet_time_type_non_billable](helpdesk_timesheet_time_type_non_billable/) | 17.0.1.0.0 | <a href='https://github.com/mpascuall'><img src='https://github.com/mpascuall.png' width='32' height='32' style='border-radius:50%;' alt='mpascuall'/></a> | Helpdesk Timesheet Time Type Non Billable
[helpdesk_type](helpdesk_type/) | 17.0.1.1.1 | <a href='https://github.com/nelsonramirezs'><img src='https://github.com/nelsonramirezs.png' width='32' height='32' style='border-radius:50%;' alt='nelsonramirezs'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Add a type to your tickets

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/hr&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/hr/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/hr/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/hr/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/hr/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/hr/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/hr)
[![Translation Status](https://translation.odoo-community.org/widgets/hr-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/hr-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# hr

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[hr_announcement](hr_announcement/) | 17.0.1.0.0 |  | Announcement
[hr_contract_bonus](hr_contract_bonus/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Manage bonuses in employee contracts
[hr_course](hr_course/) | 17.0.1.0.1 |  | This module allows your to manage employee's training courses
[hr_department_code](hr_department_code/) | 17.0.1.0.0 |  | HR department code
[hr_employee_age](hr_employee_age/) | 17.0.1.0.0 |  | Age field for employee
[hr_employee_calendar_planning](hr_employee_calendar_planning/) | 17.0.1.0.4 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Employee Calendar Planning
[hr_employee_document](hr_employee_document/) | 17.0.1.0.1 |  | Documents attached to the employee profile
[hr_employee_document_from_applicant](hr_employee_document_from_applicant/) | 17.0.1.0.0 | <a href='https://github.com/ursais'><img src='https://github.com/ursais.png' width='32' height='32' style='border-radius:50%;' alt='ursais'/></a> | HR Employee Document from Applicant
[hr_employee_firstname](hr_employee_firstname/) | 17.0.1.0.2 | <a href='https://github.com/Savoir-faire Linux'><img src='https://github.com/Savoir-faire Linux.png' width='32' height='32' style='border-radius:50%;' alt='Savoir-faire Linux'/></a> <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Adds First Name to Employee
[hr_employee_id](hr_employee_id/) | 17.0.1.0.0 |  | Employee ID
[hr_employee_language](hr_employee_language/) | 17.0.1.0.0 |  | HR Employee Language
[hr_employee_medical_examination](hr_employee_medical_examination/) | 17.0.1.1.0 |  | Adds information about employee's medical examinations
[hr_employee_partner_external](hr_employee_partner_external/) | 17.0.1.0.0 |  | Associate an external Partner to Employee
[hr_employee_ppe](hr_employee_ppe/) | 17.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> <a href='https://github.com/eduaparicio'><img src='https://github.com/eduaparicio.png' width='32' height='32' style='border-radius:50%;' alt='eduaparicio'/></a> | Personal Protective Equipment (PPE) Management
[hr_employee_relative](hr_employee_relative/) | 17.0.1.0.0 |  | Allows storing information about employee's family
[hr_employee_second_lastname](hr_employee_second_lastname/) | 17.0.1.0.2 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Split Name in First Name, Father's Last Name and Mother's Last Name
[hr_employee_ssn](hr_employee_ssn/) | 17.0.1.0.0 |  | View/edit employee's SIN field
[hr_job_category](hr_job_category/) | 17.0.1.0.1 |  | Adds tags to employee through contract and job position
[hr_personal_equipment_request](hr_personal_equipment_request/) | 17.0.1.0.0 |  | This addon allows to manage employee personal equipment
[hr_personal_equipment_request_tier_validation](hr_personal_equipment_request_tier_validation/) | 17.0.1.0.0 |  | Enables tier validation from hr.personal.equipment.request
[hr_professional_category](hr_professional_category/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | HR Professional Category
[hr_study](hr_study/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Structured study field for employees
[hr_work_entry_profile](hr_work_entry_profile/) | 17.0.1.0.0 |  | User can access their work entries from the profile view.

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/hr-attendance&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/hr-attendance/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/hr-attendance/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/hr-attendance/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/hr-attendance/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/hr-attendance/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/hr-attendance)
[![Translation Status](https://translation.odoo-community.org/widgets/hr-attendance-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/hr-attendance-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# hr-attendance

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[hr_attendance_autoclose](hr_attendance_autoclose/) | 17.0.1.0.0 |  | Close stale Attendances
[hr_attendance_calendar_view](hr_attendance_calendar_view/) | 17.0.1.0.0 |  | This module adds the calendar view as an option to display attendance
[hr_attendance_reason](hr_attendance_reason/) | 17.0.1.1.1 |  | HR Attendance Reason
[hr_attendance_report_theoretical_time](hr_attendance_report_theoretical_time/) | 17.0.1.1.0 |  | Theoretical vs Attended Time Analysis
[hr_attendance_rfid](hr_attendance_rfid/) | 17.0.1.0.0 |  | HR Attendance RFID
[hr_contract_update_overtime](hr_contract_update_overtime/) | 17.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Update Overtime from HR Contract

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/hr-expense&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/hr-expense/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/hr-expense/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/hr-expense/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/hr-expense/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/hr-expense/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/hr-expense)
[![Translation Status](https://translation.odoo-community.org/widgets/hr-expense-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/hr-expense-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# hr-expense

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[hr_expense_advance_clearing](hr_expense_advance_clearing/) | 17.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Employee Advance and Clearing
[hr_expense_advance_clearing_sequence](hr_expense_advance_clearing_sequence/) | 17.0.1.0.0 |  | HR Expense Advance Clearing Sequence
[hr_expense_cancel](hr_expense_cancel/) | 17.0.1.0.3 |  | Hr expense cancel
[hr_expense_employee_analytic_default](hr_expense_employee_analytic_default/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Expense Employee Analytic Default
[hr_expense_invoice](hr_expense_invoice/) | 17.0.1.0.4 |  | Supplier invoices on HR expenses
[hr_expense_journal](hr_expense_journal/) | 17.0.1.0.0 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Set the Journal for the payment type used to pay the expense
[hr_expense_payment](hr_expense_payment/) | 17.0.1.0.1 |  | HR Expense Payment
[hr_expense_sequence](hr_expense_sequence/) | 17.0.1.0.0 |  | HR expense sequence
[hr_expense_sequence_option](hr_expense_sequence_option/) | 17.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Manage sequence options for hr.expense.sheet
[hr_expense_tier_validation](hr_expense_tier_validation/) | 17.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Expense Tier Validation

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/hr-holidays&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/hr-holidays/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/hr-holidays/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/hr-holidays/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/hr-holidays/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/hr-holidays/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/hr-holidays)
[![Translation Status](https://translation.odoo-community.org/widgets/hr-holidays-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/hr-holidays-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# hr-holidays

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[hr_holidays_leave_report_calendar_type](hr_holidays_leave_report_calendar_type/) | 17.0.1.0.0 |  | Adds leave type filter to Time Off Overview calendar
[hr_holidays_natural_period](hr_holidays_natural_period/) | 17.0.1.0.4 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Apply natural days in holidays
[hr_holidays_public](hr_holidays_public/) | 17.0.1.0.11 |  | Manage Public Holidays
[hr_holidays_public_city](hr_holidays_public_city/) | 17.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | HR Holidays Public City
[hr_holidays_settings](hr_holidays_settings/) | 17.0.1.0.1 |  | Enables Settings Form for HR Holidays.
[hr_leave_custom_hour_interval](hr_leave_custom_hour_interval/) | 17.0.1.0.1 |  | Edit start and end of leaves using time intervals

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/interface-github&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/interface-github/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/interface-github/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/interface-github/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/interface-github/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/interface-github/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/interface-github)
[![Translation Status](https://translation.odoo-community.org/widgets/interface-github-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/interface-github-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# interface-github

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[github_connector](github_connector/) | 17.0.1.0.0 |  | Synchronize information from Github repositories
[github_connector_odoo](github_connector_odoo/) | 17.0.1.0.1 |  | Analyze Odoo modules information from Github repositories

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/intrastat-extrastat&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/intrastat-extrastat/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/intrastat-extrastat/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/intrastat-extrastat/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/intrastat-extrastat/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/intrastat-extrastat/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/intrastat-extrastat)
[![Translation Status](https://translation.odoo-community.org/widgets/intrastat-extrastat-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/intrastat-extrastat-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# intrastat-extrastat

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[intrastat_base](intrastat_base/) | 17.0.1.0.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/luc-demeyer'><img src='https://github.com/luc-demeyer.png' width='32' height='32' style='border-radius:50%;' alt='luc-demeyer'/></a> | Base module for Intrastat reporting
[intrastat_product](intrastat_product/) | 17.0.1.5.2 |  | Base module for Intrastat Product
[intrastat_product_generic](intrastat_product_generic/) | 17.0.1.0.0 |  | Generic Intrastat Product Declaration
[intrastat_product_hscodes_import](intrastat_product_hscodes_import/) | 17.0.1.0.0 |  | Module used to import HS Codes for Intrastat Product
[product_harmonized_system](product_harmonized_system/) | 17.0.1.2.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/luc-demeyer'><img src='https://github.com/luc-demeyer.png' width='32' height='32' style='border-radius:50%;' alt='luc-demeyer'/></a> | Base module for Product Import/Export reports
[product_harmonized_system_delivery](product_harmonized_system_delivery/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/luc-demeyer'><img src='https://github.com/luc-demeyer.png' width='32' height='32' style='border-radius:50%;' alt='luc-demeyer'/></a> | Hide native hs_code field provided by the delivery module
[product_harmonized_system_stock](product_harmonized_system_stock/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/luc-demeyer'><img src='https://github.com/luc-demeyer.png' width='32' height='32' style='border-radius:50%;' alt='luc-demeyer'/></a> | Adds a menu entry for H.S. codes

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/iot&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/iot/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/iot/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/iot/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/iot/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/iot/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/iot)
[![Translation Status](https://translation.odoo-community.org/widgets/iot-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/iot-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# OCA IOT modules

This project aims to deal with modules related to IOT

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[iot_amqp_oca](iot_amqp_oca/) | 17.0.1.0.0 |  | Integrate Iot Outputs with AMQP
[iot_input_oca](iot_input_oca/) | 17.0.1.0.0 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | IoT Input module
[iot_oca](iot_oca/) | 17.0.1.0.1 |  | IoT base module
[iot_output_oca](iot_output_oca/) | 17.0.1.0.0 |  | IoT allow multiple outputs
[iot_rule](iot_rule/) | 17.0.1.0.0 |  | Define IoT Rules (Keys that control Inputs)
[iot_template_oca](iot_template_oca/) | 17.0.1.0.0 |  | IoT module for managing templates

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/knowledge&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/knowledge/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/knowledge/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/knowledge/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/knowledge/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/knowledge/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/knowledge)
[![Translation Status](https://translation.odoo-community.org/widgets/knowledge-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/knowledge-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# knowledge

Knowlesge management addons. Also has some usefull tools to handle attachments

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[attachment_category](attachment_category/) | 17.0.1.0.1 |  | Adds a document category to help classification
[attachment_zipped_download](attachment_zipped_download/) | 17.0.1.0.0 |  | Attachment Zipped Download
[document_knowledge](document_knowledge/) | 17.0.1.0.1 |  | Documents Knowledge
[document_page](document_page/) | 17.0.1.1.2 |  | Document Page
[document_page_access_group](document_page_access_group/) | 17.0.2.0.0 |  | Choose groups to access document pages
[document_page_approval](document_page_approval/) | 17.0.1.1.0 |  | Document Page Approval
[document_page_group](document_page_group/) | 17.0.1.0.0 |  | Define access groups on documents
[document_page_partner](document_page_partner/) | 17.0.1.0.0 |  | Allows to link doucment pages to a partner
[document_page_product](document_page_product/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | This module links document pages to products
[document_page_project](document_page_project/) | 17.0.1.0.0 |  | This module links document pages to projects
[document_page_reference](document_page_reference/) | 17.0.1.0.0 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Include references on document pages
[document_page_tag](document_page_tag/) | 17.0.1.0.0 |  | Allows you to assign tags or keywords to pages and search for them afterwards
[document_page_tag_print_control](document_page_tag_print_control/) | 17.0.1.0.0 |  | Restricts document page printing based on assigned tags
[document_url](document_url/) | 17.0.1.0.1 |  | URL attachment

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-belgium&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/l10n-belgium/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-belgium/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/l10n-belgium/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-belgium/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/l10n-belgium/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-belgium)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-belgium-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-belgium-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-belgium

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_statement_import_coda](account_statement_import_coda/) | 17.0.1.0.0 |  | Import CODA Bank Statement
[companyweb_base](companyweb_base/) | 17.0.1.1.0 | <a href='https://github.com/xavier-bouquiaux'><img src='https://github.com/xavier-bouquiaux.png' width='32' height='32' style='border-radius:50%;' alt='xavier-bouquiaux'/></a> | Know who you are dealing with. Enhance Odoo partner data from companyweb.be.
[companyweb_payment_info](companyweb_payment_info/) | 17.0.1.0.2 | <a href='https://github.com/xavier-bouquiaux'><img src='https://github.com/xavier-bouquiaux.png' width='32' height='32' style='border-radius:50%;' alt='xavier-bouquiaux'/></a> | Send your customer payment information to Companyweb
[l10n_be_intrastat_product](l10n_be_intrastat_product/) | 17.0.1.0.0 | <a href='https://github.com/luc-demeyer'><img src='https://github.com/luc-demeyer.png' width='32' height='32' style='border-radius:50%;' alt='luc-demeyer'/></a> <a href='https://github.com/jdidderen-noviat'><img src='https://github.com/jdidderen-noviat.png' width='32' height='32' style='border-radius:50%;' alt='jdidderen-noviat'/></a> | Intrastat Product Declaration for Belgium
[l10n_be_mis_reports](l10n_be_mis_reports/) | 17.0.2.0.1 |  | MIS Builder templates for the Belgium P&L, Balance Sheets and VAT Declaration
[l10n_be_partner_kbo_bce](l10n_be_partner_kbo_bce/) | 17.0.1.0.0 |  | Belgium - KBO/BCE numbers

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-brazil&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/l10n-brazil/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-brazil/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/l10n-brazil/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-brazil/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/l10n-brazil/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-brazil)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-brazil-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-brazil-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-brazil

Odoo Brazilian localization

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_br_account](l10n_br_account/) | 17.0.1.0.2 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Invoicing and accounting entries for Brazil
[l10n_br_account_due_list](l10n_br_account_due_list/) | 17.0.1.0.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Brazilian Account Due List
[l10n_br_account_fleet](l10n_br_account_fleet/) | 17.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Brazilian Localization Account Fleet
[l10n_br_account_nfe](l10n_br_account_nfe/) | 17.0.1.0.0 | <a href='https://github.com/antoniospneto'><img src='https://github.com/antoniospneto.png' width='32' height='32' style='border-radius:50%;' alt='antoniospneto'/></a> <a href='https://github.com/felipemotter'><img src='https://github.com/felipemotter.png' width='32' height='32' style='border-radius:50%;' alt='felipemotter'/></a> <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> | Integration between l10n_br_account and l10n_br_nfe
[l10n_br_account_payment_order](l10n_br_account_payment_order/) | 17.0.1.1.0 | <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> | Brazilian Payment Order
[l10n_br_base](l10n_br_base/) | 17.0.1.5.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Customization of base module for implementations in Brazil.
[l10n_br_cnpj_search](l10n_br_cnpj_search/) | 17.0.1.1.3 |  | Integração com os Webservices da ReceitaWS e SerPro
[l10n_br_coa](l10n_br_coa/) | 17.0.1.0.1 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | Base do Planos de Contas brasileiros
[l10n_br_coa_generic](l10n_br_coa_generic/) | 17.0.1.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | Plano de Contas para empresas do Regime normal (Micro e pequenas empresas)
[l10n_br_coa_simple](l10n_br_coa_simple/) | 17.0.1.0.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Plano de Contas ITG 1000 para Microempresas e Empresa de Pequeno Porte
[l10n_br_contract](l10n_br_contract/) | 17.0.1.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Customization of Contract module for implementations in Brazil.
[l10n_br_crm](l10n_br_crm/) | 17.0.1.1.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> | Brazilian Localization CRM
[l10n_br_crm_cnpj_search](l10n_br_crm_cnpj_search/) | 17.0.1.0.0 | <a href='https://github.com/corredato'><img src='https://github.com/corredato.png' width='32' height='32' style='border-radius:50%;' alt='corredato'/></a> <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | CNPJ search in CRM Lead
[l10n_br_cte](l10n_br_cte/) | 17.0.9.3.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Brazilian Electronic Invoice CT-e
[l10n_br_cte_spec](l10n_br_cte_spec/) | 17.0.1.1.0 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | CT-e abstract models generated by xsdata-odoo from the official xsd
[l10n_br_currency_rate_update](l10n_br_currency_rate_update/) | 17.0.1.0.1 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Update exchange rates using OCA modules for Brazil
[l10n_br_fiscal](l10n_br_fiscal/) | 17.0.7.4.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Fiscal module/tax engine for Brazil
[l10n_br_fiscal_certificate](l10n_br_fiscal_certificate/) | 17.0.1.1.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | A1 fiscal certificate management for Brazil
[l10n_br_fiscal_closing](l10n_br_fiscal_closing/) | 17.0.1.0.0 |  | Period fiscal closing
[l10n_br_fiscal_dfe](l10n_br_fiscal_dfe/) | 17.0.1.1.0 |  | Distribuição de documentos fiscais
[l10n_br_fiscal_edi](l10n_br_fiscal_edi/) | 17.0.2.0.1 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | Common EDI fiscal features
[l10n_br_fiscal_notification](l10n_br_fiscal_notification/) | 17.0.1.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | Define fiscal document notifications
[l10n_br_fiscal_subsequent_document](l10n_br_fiscal_subsequent_document/) | 17.0.1.0.0 |  | Documentos Fiscais Subsequentes
[l10n_br_hr](l10n_br_hr/) | 17.0.1.1.0 |  | Brazilian Localization HR
[l10n_br_hr_contract](l10n_br_hr_contract/) | 17.0.1.1.0 |  | Brazilian Localization HR Contract
[l10n_br_hr_expense_invoice](l10n_br_hr_expense_invoice/) | 17.0.1.0.1 |  | Customization of HR Expense Invoice module for implementations in Brazil.
[l10n_br_ie_search](l10n_br_ie_search/) | 17.0.1.1.0 |  | Integração com a API SintegraWS e SEFAZ
[l10n_br_mdfe](l10n_br_mdfe/) | 17.0.1.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Brazilian Eletronic Invoice MDF-e
[l10n_br_mdfe_spec](l10n_br_mdfe_spec/) | 17.0.1.0.0 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | MDF-e abstract models generated by xsdata-odoo from the official xsd
[l10n_br_mis_report](l10n_br_mis_report/) | 17.0.1.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | Templates de relatórios contábeis brasileiros: Balanço Patrimonial e DRE
[l10n_br_nfe](l10n_br_nfe/) | 17.0.5.0.0 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Eletronic Invoicing for Brazil / NF-e
[l10n_br_nfe_spec](l10n_br_nfe_spec/) | 17.0.2.0.0 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | NF-e abstract models generated by xsdata-odoo from the official xsd
[l10n_br_nfse](l10n_br_nfse/) | 17.0.4.2.2 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/luismalta'><img src='https://github.com/luismalta.png' width='32' height='32' style='border-radius:50%;' alt='luismalta'/></a> <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Root electronic invoice for service / NFS-e module
[l10n_br_nfse_focus](l10n_br_nfse_focus/) | 17.0.2.2.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | NFS-e (FocusNFE)
[l10n_br_portal](l10n_br_portal/) | 17.0.1.0.0 |  | Campos Brasileiros no Portal
[l10n_br_product_contract](l10n_br_product_contract/) | 17.0.1.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Criação de contratos através dos Pedidos de Vendas
[l10n_br_purchase](l10n_br_purchase/) | 17.0.1.0.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Brazilian Localization Purchase
[l10n_br_purchase_request](l10n_br_purchase_request/) | 17.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Purchase Request Brazilian Localization Purchase Request
[l10n_br_purchase_requisition](l10n_br_purchase_requisition/) | 17.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Brazilian Localization Purchase Requisition
[l10n_br_resource](l10n_br_resource/) | 17.0.1.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/lfdivino'><img src='https://github.com/lfdivino.png' width='32' height='32' style='border-radius:50%;' alt='lfdivino'/></a> | This module extend core resource to create important brazilian informations. Define a Brazilian calendar and some tools to compute dates used in financial and payroll modules
[l10n_br_sale](l10n_br_sale/) | 17.0.1.0.1 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Brazilian Localization Sale
[l10n_br_sale_invoice_plan](l10n_br_sale_invoice_plan/) | 17.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Brazilian Localization Sale Invoice Plan
[l10n_br_sped_base](l10n_br_sped_base/) | 17.0.1.1.1 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Framework abstrato pro SPED
[l10n_br_stock](l10n_br_stock/) | 17.0.1.0.0 |  | Brazilian Localization Warehouse
[l10n_br_stock_account](l10n_br_stock_account/) | 17.0.1.0.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> | Invoice from Picking (nota fiscal de remessa) and other WMS overrides
[l10n_br_stock_account_report](l10n_br_stock_account_report/) | 17.0.1.0.0 | <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> | P7 Stock Valuation Report
[l10n_br_zip](l10n_br_zip/) | 17.0.1.1.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Brazilian Localisation ZIP Codes
[spec_driven_model](spec_driven_model/) | 17.0.1.1.1 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | XML binding for Odoo: XML to Odoo models and models to XML.

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-ecuador&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/l10n-ecuador/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-ecuador/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/l10n-ecuador/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-ecuador/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/l10n-ecuador/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-ecuador)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-ecuador-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-ecuador-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-ecuador

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_ec_account_edi](l10n_ec_account_edi/) | 17.0.1.1.4 |  | Electronic data interchange adapted Ecuadorian localization
[l10n_ec_base](l10n_ec_base/) | 17.0.1.0.2 |  | Ecuadorian Localization
[l10n_ec_credit_note](l10n_ec_credit_note/) | 17.0.1.0.0 |  | Credit Notes extension for Ecuador
[l10n_ec_withhold](l10n_ec_withhold/) | 17.0.1.0.1 |  | Electronic Withholding adapted Ecuadorian localization

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-finland&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/l10n-finland/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-finland/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/l10n-finland/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-finland/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/l10n-finland/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-finland)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-finland-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-finland-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-finland

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_fi_banks](l10n_fi_banks/) | 17.0.1.0.2 |  | Finnish and Nordic banks and their addresses
[l10n_fi_edicode](l10n_fi_edicode/) | 17.0.1.0.1 |  | Adds EDI code field and operators
[l10n_fi_payment_terms](l10n_fi_payment_terms/) | 17.0.1.0.0 |  | Common Finnish invoice payment terms
[l10n_fi_sale_refund_payment_reference](l10n_fi_sale_refund_payment_reference/) | 17.0.1.0.0 |  | Automatically generate payment references for sale refunds

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-france&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/l10n-france/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-france/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/l10n-france/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-france/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/l10n-france/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-france)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-france-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-france-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# French Localization

French Localization Modules

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_banking_fr_lcr](account_banking_fr_lcr/) | 17.0.1.0.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Create French LCR CFONB files
[account_statement_import_fr_cfonb](account_statement_import_fr_cfonb/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import CFONB bank statements files in Odoo
[l10n_fr_account_invoice_facturx](l10n_fr_account_invoice_facturx/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | France-specific module to generate Factur-X invoices
[l10n_fr_account_tax_unece](l10n_fr_account_tax_unece/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Auto-configure UNECE params on French taxes
[l10n_fr_chorus_account](l10n_fr_chorus_account/) | 17.0.2.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Generate Chorus-compliant e-invoices and transmit them via the Chorus API
[l10n_fr_chorus_facturx](l10n_fr_chorus_facturx/) | 17.0.2.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Generate Chorus-compliant Factur-X invoices
[l10n_fr_chorus_sale](l10n_fr_chorus_sale/) | 17.0.2.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add checks on sale orders for Chorus Pro
[l10n_fr_cog](l10n_fr_cog/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add Code Officiel Géographique (COG) on countries
[l10n_fr_das2](l10n_fr_das2/) | 17.0.3.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | DAS2 (France)
[l10n_fr_department](l10n_fr_department/) | 17.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Populate Database with French Departments (Départements)
[l10n_fr_department_oversea](l10n_fr_department_oversea/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Populate Database with overseas French Departments (Départements d'outre-mer)
[l10n_fr_hr_check_ssnid](l10n_fr_hr_check_ssnid/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Check validity of Social Security Numbers in French companies
[l10n_fr_intrastat_product](l10n_fr_intrastat_product/) | 17.0.1.2.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | EMEBI (ex-DEB) for France
[l10n_fr_intrastat_service](l10n_fr_intrastat_service/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Module for Intrastat service reporting (DES) for France
[l10n_fr_mis_reports](l10n_fr_mis_reports/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | MIS Report templates for the French P&L and Balance Sheets
[l10n_fr_pos_caisse_ap_ip](l10n_fr_pos_caisse_ap_ip/) | 17.0.1.4.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add support for Caisse-AP payment protocol used in France
[l10n_fr_siret](l10n_fr_siret/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | French company identity numbers SIRET/SIREN/NIC
[l10n_fr_state](l10n_fr_state/) | 17.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Populate Database with French States (Régions)

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-germany&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/l10n-germany/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-germany/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/l10n-germany/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-germany/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/l10n-germany/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-germany)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-germany-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-germany-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-germany

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[datev_export](datev_export/) | 17.0.1.0.0 |  | Export invoices and refunds as xml and pdf files zipped in DATEV format.
[datev_export_xml](datev_export_xml/) | 17.0.1.0.1 |  | Export invoices and refunds as xml and pdf files zipped in DATEV format.
[datev_import_csv_dtvf](datev_import_csv_dtvf/) | 17.0.1.0.1 |  | Import account moves generated by external software
[l10n_de_mis_reports](l10n_de_mis_reports/) | 17.0.1.1.2 |  | MIS Builder templates for the German P&L and Balance Sheets (SKR03 + SKR04)
[l10n_de_tax_statement](l10n_de_tax_statement/) | 17.0.1.0.1 |  | German VAT Statement
[l10n_de_tax_statement_zm](l10n_de_tax_statement_zm/) | 17.0.1.0.1 |  | German VAT Statement Extension
[l10n_din5008_move_name](l10n_din5008_move_name/) | 17.0.1.1.0 |  | Add Account move name on the name of the move

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-iran&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/l10n-iran/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-iran/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/l10n-iran/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-iran/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/l10n-iran/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-iran)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-iran-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-iran-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-iran

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_ir_account](l10n_ir_account/) | 17.0.1.0.1 |  | iran accounting chart and localization.
[l10n_ir_states](l10n_ir_states/) | 17.0.1.0.0 |  | Add Iran States and Cities

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-japan&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/l10n-japan/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-japan/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/l10n-japan/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-japan/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/l10n-japan/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-japan)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-japan-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-japan-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-japan

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_payment_term_cutoff_day](account_payment_term_cutoff_day/) | 17.0.1.1.0 |  | Account Payment Term Cutoff Day
[account_tax_rounding_method](account_tax_rounding_method/) | 17.0.1.0.0 |  | Account Tax Rounding Method
[l10n_jp_address_layout](l10n_jp_address_layout/) | 17.0.1.0.0 |  | Japan Address Layout
[l10n_jp_country_state](l10n_jp_country_state/) | 17.0.1.1.0 |  | Japan Country States
[l10n_jp_partner_title_qweb](l10n_jp_partner_title_qweb/) | 17.0.1.0.0 |  | Japan Partner Title QWeb
[l10n_jp_partner_zip_address](l10n_jp_partner_zip_address/) | 17.0.1.0.0 |  | Japan Partner Zip Address

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-mexico&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/l10n-mexico/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-mexico/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/l10n-mexico/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-mexico/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/l10n-mexico/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-mexico)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-mexico-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-mexico-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Odoo modules for Mexico

This repository contains modules specific to Mexico.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[currency_rate_update_banxico](currency_rate_update_banxico/) | 17.0.1.0.0 |  | Update exchange rates using Banxico
[l10n_mx_catalogs](l10n_mx_catalogs/) | 17.0.1.2.0 |  | Catálogos del Servicio de Administración Tributaria de México
[l10n_mx_cfdi](l10n_mx_cfdi/) | 17.0.1.0.0 |  | Allow generating CFDI (Comprobante Fiscal Digital por Internet)
[l10n_mx_cfdi_account](l10n_mx_cfdi_account/) | 17.0.1.0.2 |  | Mexico CFDI Account Integration
[l10n_mx_res_partner_csf](l10n_mx_res_partner_csf/) | 17.0.1.1.0 |  | Scan and extract information from CSF

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-netherlands&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/l10n-netherlands/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-netherlands/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/l10n-netherlands/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-netherlands/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/l10n-netherlands/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-netherlands)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-netherlands-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-netherlands-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-netherlands

Odoo Dutch Localization

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_nl_bank](l10n_nl_bank/) | 17.0.1.0.0 |  | Import all Dutch banks with BIC code
[l10n_nl_partner_name](l10n_nl_partner_name/) | 17.0.1.0.0 |  | Adapt parter names to Dutch conventions (support infix)
[l10n_nl_tax_statement](l10n_nl_tax_statement/) | 17.0.1.0.0 |  | Netherlands BTW Statement
[l10n_nl_xaf_auditfile_export](l10n_nl_xaf_auditfile_export/) | 17.0.1.1.0 |  | Export XAF auditfiles for Dutch tax authorities

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-portugal&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/l10n-portugal/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-portugal/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/l10n-portugal/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-portugal/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/l10n-portugal/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-portugal)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-portugal-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-portugal-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_pt_account_invoicexpress](l10n_pt_account_invoicexpress/) | 17.0.1.0.1 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Portuguese certified invoices using InvoiceXpress
[l10n_pt_stock_invoicexpress](l10n_pt_stock_invoicexpress/) | 17.0.1.0.1 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Portuguese legal transport and shipping documents (Guias de Transporte e Guias de Remessa) generated with InvoiceXpress
[l10n_pt_vat](l10n_pt_vat/) | 17.0.1.2.0 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Portuguese VAT requirements extensions

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-romania&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/l10n-romania/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-romania/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/l10n-romania/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-romania/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/l10n-romania/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-romania)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-romania-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-romania-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-romania

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[currency_rate_update_RO_BNR](currency_rate_update_RO_BNR/) | 17.0.1.6.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Currency Rate Update National Bank of Romania service
[l10n_ro_account](l10n_ro_account/) | 17.0.1.10.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Account
[l10n_ro_account_anaf_sync](l10n_ro_account_anaf_sync/) | 17.0.1.6.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Account ANAF Sync
[l10n_ro_account_bank_statement_import_mt940_alpha](l10n_ro_account_bank_statement_import_mt940_alpha/) | 17.0.0.1.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | MT940 Alpha Format Bank Statements Import
[l10n_ro_account_bank_statement_import_mt940_base](l10n_ro_account_bank_statement_import_mt940_base/) | 17.0.0.2.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - MT940 Bank Statements Import
[l10n_ro_account_bank_statement_import_mt940_bcr](l10n_ro_account_bank_statement_import_mt940_bcr/) | 17.0.0.1.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | MT940 BCR Format Bank Statements Import
[l10n_ro_account_bank_statement_import_mt940_brd](l10n_ro_account_bank_statement_import_mt940_brd/) | 17.0.0.1.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Import bank statements from BRD
[l10n_ro_account_bank_statement_import_mt940_ing](l10n_ro_account_bank_statement_import_mt940_ing/) | 17.0.0.2.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | MT940 ING Format Bank Statements Import
[l10n_ro_account_bank_statement_import_mt940_rffsn](l10n_ro_account_bank_statement_import_mt940_rffsn/) | 17.0.0.1.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Import bank statements from Raiffeisen
[l10n_ro_account_bank_statement_report](l10n_ro_account_bank_statement_report/) | 17.0.1.2.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Bank Statement Report
[l10n_ro_account_edit_currency_rate](l10n_ro_account_edit_currency_rate/) | 17.0.0.5.0 | <a href='https://github.com/mcojocaru'><img src='https://github.com/mcojocaru.png' width='32' height='32' style='border-radius:50%;' alt='mcojocaru'/></a> | Romania - Invoice Edit Currency Rate
[l10n_ro_account_period_close](l10n_ro_account_period_close/) | 17.0.0.4.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Account Period Closing
[l10n_ro_account_report_invoice](l10n_ro_account_report_invoice/) | 17.0.1.5.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Invoice Report
[l10n_ro_city](l10n_ro_city/) | 17.0.1.7.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - City
[l10n_ro_config](l10n_ro_config/) | 17.0.1.17.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Localization Install and Config Applications
[l10n_ro_dvi](l10n_ro_dvi/) | 17.0.1.9.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - DVI
[l10n_ro_etransport](l10n_ro_etransport/) | 17.0.0.6.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - E-Trasnport
[l10n_ro_fiscal_validation](l10n_ro_fiscal_validation/) | 17.0.1.2.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Fiscal Validation
[l10n_ro_message_spv](l10n_ro_message_spv/) | 17.0.1.41.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Mesaje SPV
[l10n_ro_nondeductible_vat](l10n_ro_nondeductible_vat/) | 17.0.0.9.0 | <a href='https://github.com/adrian-dks'><img src='https://github.com/adrian-dks.png' width='32' height='32' style='border-radius:50%;' alt='adrian-dks'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Nondeductible VAT
[l10n_ro_partner_create_by_vat](l10n_ro_partner_create_by_vat/) | 17.0.1.13.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Partner Create by VAT
[l10n_ro_partner_unique](l10n_ro_partner_unique/) | 17.0.1.3.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Creates a rule for vat and nrc unique for partners.
[l10n_ro_payment_receipt_report](l10n_ro_payment_receipt_report/) | 17.0.1.2.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Payment Receipt Report
[l10n_ro_payment_to_statement](l10n_ro_payment_to_statement/) | 17.0.1.6.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Add payment to cash statement
[l10n_ro_pos](l10n_ro_pos/) | 17.0.1.4.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Point of Sale
[l10n_ro_stock](l10n_ro_stock/) | 17.0.0.9.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock
[l10n_ro_stock_account](l10n_ro_stock_account/) | 17.0.1.36.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Accounting
[l10n_ro_stock_account_date](l10n_ro_stock_account_date/) | 17.0.1.15.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Accounting Date
[l10n_ro_stock_account_date_wizard](l10n_ro_stock_account_date_wizard/) | 17.0.1.4.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Accounting Date Wizard
[l10n_ro_stock_account_landed_cost](l10n_ro_stock_account_landed_cost/) | 17.0.1.6.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Accounting Landed Cost
[l10n_ro_stock_account_notice](l10n_ro_stock_account_notice/) | 17.0.1.11.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/mcojocaru'><img src='https://github.com/mcojocaru.png' width='32' height='32' style='border-radius:50%;' alt='mcojocaru'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Stock Accounting Notice
[l10n_ro_stock_account_reception_in_progress](l10n_ro_stock_account_reception_in_progress/) | 17.0.0.6.0 | <a href='https://github.com/nct74'><img src='https://github.com/nct74.png' width='32' height='32' style='border-radius:50%;' alt='nct74'/></a> <a href='https://github.com/vasi26ro'><img src='https://github.com/vasi26ro.png' width='32' height='32' style='border-radius:50%;' alt='vasi26ro'/></a> | Romania - Stock Accounting Reception In progress
[l10n_ro_stock_account_tracking](l10n_ro_stock_account_tracking/) | 17.0.1.6.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Accounting
[l10n_ro_stock_picking_comment_template](l10n_ro_stock_picking_comment_template/) | 17.0.0.4.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | This model is going to add a a header and a footer at picking report depeding on the operation type.
[l10n_ro_stock_picking_valued_report](l10n_ro_stock_picking_valued_report/) | 17.0.0.3.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Picking Valued Report
[l10n_ro_stock_price_difference](l10n_ro_stock_price_difference/) | 17.0.0.5.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/mcojocaru'><img src='https://github.com/mcojocaru.png' width='32' height='32' style='border-radius:50%;' alt='mcojocaru'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Stock Accounting Price Difference
[l10n_ro_stock_report](l10n_ro_stock_report/) | 17.0.1.4.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Report (Fișă Magazie)
[l10n_ro_vat_on_payment](l10n_ro_vat_on_payment/) | 17.0.1.7.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - VAT on Payment

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

## From OCA/l10n-russia


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-russia&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/l10n-russia/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-russia/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/l10n-russia/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-russia/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/l10n-russia/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-russia)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-russia-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-russia-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Odoo Russian Localization / Российская локализация для Odoo

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_ru](l10n_ru/) | 17.0.1.0.1 | <a href='https://github.com/Katulos'><img src='https://github.com/Katulos.png' width='32' height='32' style='border-radius:50%;' alt='Katulos'/></a> | Russia - Accounting
[l10n_ru_banks](l10n_ru_banks/) | 17.0.1.0.1 | <a href='https://github.com/Katulos'><img src='https://github.com/Katulos.png' width='32' height='32' style='border-radius:50%;' alt='Katulos'/></a> | Russian banks and their addresses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-spain&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/l10n-spain/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-spain/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/l10n-spain/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-spain/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/l10n-spain/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-spain)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-spain-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-spain-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[delivery_dhl_parcel](delivery_dhl_parcel/) | 17.0.2.0.2 | <a href='https://github.com/hildickethan'><img src='https://github.com/hildickethan.png' width='32' height='32' style='border-radius:50%;' alt='hildickethan'/></a> | Delivery Carrier implementation for DHL Parcel using their API
[delivery_gls_asm](delivery_gls_asm/) | 17.0.1.0.4 | <a href='https://github.com/hildickethan'><img src='https://github.com/hildickethan.png' width='32' height='32' style='border-radius:50%;' alt='hildickethan'/></a> | Delivery Carrier implementation for GLS with ASMRed API
[delivery_mrw](delivery_mrw/) | 17.0.1.0.0 |  | Delivery Carrier implementation for MRW with SAGEC API
[delivery_seur_atlas](delivery_seur_atlas/) | 17.0.1.0.0 |  | Integrate SEUR Atlas API
[l10n_ca_es_cnae](l10n_ca_es_cnae/) | 17.0.1.1.0 |  | Genera la traducción al catalán de todos los códigos Nace
[l10n_es_account_asset](l10n_es_account_asset/) | 17.0.2.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Gestión de activos fijos para España
[l10n_es_account_banking_sepa_fsdd](l10n_es_account_banking_sepa_fsdd/) | 17.0.1.0.1 |  | Account Banking Sepa - FSDD (Anticipos de crédito)
[l10n_es_account_statement_import_n43](l10n_es_account_statement_import_n43/) | 17.0.1.1.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Importación de extractos bancarios españoles (Norma 43)
[l10n_es_aeat](l10n_es_aeat/) | 17.0.2.7.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Modulo base para declaraciones de la AEAT
[l10n_es_aeat_mod111](l10n_es_aeat_mod111/) | 17.0.1.0.3 |  | AEAT modelo 111
[l10n_es_aeat_mod115](l10n_es_aeat_mod115/) | 17.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | AEAT modelo 115
[l10n_es_aeat_mod123](l10n_es_aeat_mod123/) | 17.0.1.1.3 |  | AEAT modelo 123
[l10n_es_aeat_mod130](l10n_es_aeat_mod130/) | 17.0.1.0.3 |  | AEAT modelo 130
[l10n_es_aeat_mod190](l10n_es_aeat_mod190/) | 17.0.1.4.0 |  | AEAT modelo 190
[l10n_es_aeat_mod216](l10n_es_aeat_mod216/) | 17.0.1.1.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | AEAT modelo 216
[l10n_es_aeat_mod296](l10n_es_aeat_mod296/) | 17.0.1.0.2 |  | AEAT modelo 296
[l10n_es_aeat_mod303](l10n_es_aeat_mod303/) | 17.0.1.11.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | AEAT modelo 303
[l10n_es_aeat_mod303_oss](l10n_es_aeat_mod303_oss/) | 17.0.1.0.0 |  | AEAT modelo 303 - OSS
[l10n_es_aeat_mod303_vat_prorate](l10n_es_aeat_mod303_vat_prorate/) | 17.0.3.1.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Prorrata de IVA [303]
[l10n_es_aeat_mod347](l10n_es_aeat_mod347/) | 17.0.1.7.3 |  | AEAT modelo 347
[l10n_es_aeat_mod349](l10n_es_aeat_mod349/) | 17.0.1.2.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | AEAT modelo 349
[l10n_es_aeat_mod369](l10n_es_aeat_mod369/) | 17.0.1.0.0 |  | AEAT modelo 369
[l10n_es_aeat_mod390](l10n_es_aeat_mod390/) | 17.0.1.9.4 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | AEAT modelo 390
[l10n_es_aeat_mod390_oss](l10n_es_aeat_mod390_oss/) | 17.0.1.0.0 |  | AEAT modelo 390 - OSS
[l10n_es_aeat_mod592](l10n_es_aeat_mod592/) | 17.0.1.0.4 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | AEAT modelo 592
[l10n_es_aeat_partner_check](l10n_es_aeat_partner_check/) | 17.0.1.0.0 |  | AEAT - Comprobación de Calidad de datos identificativos
[l10n_es_aeat_sii_invoice_summary](l10n_es_aeat_sii_invoice_summary/) | 17.0.1.1.0 |  | Envio de factura simplificada resumen TPV a SII
[l10n_es_aeat_sii_match](l10n_es_aeat_sii_match/) | 17.0.1.0.5 | <a href='https://github.com/Abranes'><img src='https://github.com/Abranes.png' width='32' height='32' style='border-radius:50%;' alt='Abranes'/></a> <a href='https://github.com/Reyes4711-S73'><img src='https://github.com/Reyes4711-S73.png' width='32' height='32' style='border-radius:50%;' alt='Reyes4711-S73'/></a> | Sistema de comprobación y contraste de facturas enviadas al SII
[l10n_es_aeat_sii_oca](l10n_es_aeat_sii_oca/) | 17.0.1.7.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Suministro Inmediato de Información en el IVA
[l10n_es_aeat_sii_oss](l10n_es_aeat_sii_oss/) | 17.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Suministro Inmediato de Información en el IVA: OSS
[l10n_es_atc](l10n_es_atc/) | 17.0.1.0.4 |  | Modulo 'glue' de la AEAT para el menú de la ATC
[l10n_es_atc_mod415](l10n_es_atc_mod415/) | 17.0.1.0.0 | <a href='https://github.com/Christian-RB'><img src='https://github.com/Christian-RB.png' width='32' height='32' style='border-radius:50%;' alt='Christian-RB'/></a> | ATC Modelo 415
[l10n_es_atc_mod417](l10n_es_atc_mod417/) | 17.0.1.2.3 | <a href='https://github.com/carlos-lopez-tecnativa'><img src='https://github.com/carlos-lopez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carlos-lopez-tecnativa'/></a> | ATC Modelo 417
[l10n_es_atc_mod420](l10n_es_atc_mod420/) | 17.0.1.1.4 | <a href='https://github.com/Christian-RB'><img src='https://github.com/Christian-RB.png' width='32' height='32' style='border-radius:50%;' alt='Christian-RB'/></a> | ATC Modelo 420
[l10n_es_atc_mod425](l10n_es_atc_mod425/) | 17.0.1.0.3 | <a href='https://github.com/nicolasramos'><img src='https://github.com/nicolasramos.png' width='32' height='32' style='border-radius:50%;' alt='nicolasramos'/></a> | ATC Modelo 425
[l10n_es_atc_sii_oca](l10n_es_atc_sii_oca/) | 17.0.1.0.0 |  | Suministro Inmediato de Información en el IGIC
[l10n_es_cnae](l10n_es_cnae/) | 17.0.1.1.0 |  | Extiende los códigos NACE europeos con los CNAE españoles
[l10n_es_facturae](l10n_es_facturae/) | 17.0.1.5.1 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Creación de Facturae
[l10n_es_facturae_face](l10n_es_facturae_face/) | 17.0.1.0.3 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Envío de Facturae a FACe
[l10n_es_facturae_literal_legal](l10n_es_facturae_literal_legal/) | 17.0.1.0.0 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> | Facturae - Literal Legal Texts
[l10n_es_facturae_special_payment](l10n_es_facturae_special_payment/) | 17.0.1.1.0 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> | Facturae - Special Payment
[l10n_es_igic](l10n_es_igic/) | 17.0.2.2.0 |  | IGIC (Impuesto General Indirecto Canario)
[l10n_es_igic_reav](l10n_es_igic_reav/) | 17.0.1.0.3 |  | Aplicación REAV en la localización canaria
[l10n_es_intrastat_report](l10n_es_intrastat_report/) | 17.0.1.1.4 |  | Spanish Intrastat Product Declaration
[l10n_es_location_nuts](l10n_es_location_nuts/) | 17.0.1.0.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | NUTS specific options for Spain
[l10n_es_mis_report](l10n_es_mis_report/) | 17.0.1.0.1 |  | Plantillas MIS Builder para informes contables españoles
[l10n_es_partner](l10n_es_partner/) | 17.0.1.0.7 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Adaptación de los clientes, proveedores y bancos para España
[l10n_es_partner_mercantil](l10n_es_partner_mercantil/) | 17.0.1.0.1 |  | Añade los datos del registro mercantil a la empresa
[l10n_es_payment_order_confirming_aef](l10n_es_payment_order_confirming_aef/) | 17.0.1.1.1 |  | Exportación de fichero bancario Confirming estándar AEF
[l10n_es_payment_order_confirming_sabadell](l10n_es_payment_order_confirming_sabadell/) | 17.0.1.1.0 |  | Exportación de fichero bancario Confirming para Banco Sabadell
[l10n_es_pos_oca](l10n_es_pos_oca/) | 17.0.1.1.0 |  | Punto de venta adaptado a la legislación española
[l10n_es_pos_sii](l10n_es_pos_sii/) | 17.0.1.1.0 |  | Envío de pedidos del TPV al SII
[l10n_es_reav](l10n_es_reav/) | 17.0.1.0.0 | <a href='https://github.com/Bilbonet'><img src='https://github.com/Bilbonet.png' width='32' height='32' style='border-radius:50%;' alt='Bilbonet'/></a> | REAV - Régimen Especial Agencias de Viajes
[l10n_es_toponyms](l10n_es_toponyms/) | 17.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Topónimos españoles
[l10n_es_vat_book](l10n_es_vat_book/) | 17.0.2.2.0 |  | Libros registro del IVA y del IRPF
[l10n_es_vat_book_igic](l10n_es_vat_book_igic/) | 17.0.1.0.2 | <a href='https://github.com/nicolasramos'><img src='https://github.com/nicolasramos.png' width='32' height='32' style='border-radius:50%;' alt='nicolasramos'/></a> | Libro de IGIC
[l10n_es_vat_book_invoice_summary](l10n_es_vat_book_invoice_summary/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Facturas resumen en libro de IVA
[l10n_es_vat_book_oss](l10n_es_vat_book_oss/) | 17.0.1.0.2 |  | Libro de IVA OSS
[l10n_es_vat_book_pos](l10n_es_vat_book_pos/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Libro de IVA Adaptado al Punto de Venta
[l10n_es_vat_prorate](l10n_es_vat_prorate/) | 17.0.3.3.0 |  | Prorrata de IVA para la localización española
[l10n_es_verifactu_oca](l10n_es_verifactu_oca/) | 17.0.1.3.0 |  | Comunicación VERI*FACTU
[payment_redsys](payment_redsys/) | 17.0.1.0.4 |  | Payment Acquirer: Redsys Implementation

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-switzerland&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/l10n-switzerland/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-switzerland/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/l10n-switzerland/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-switzerland/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/l10n-switzerland/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-switzerland)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-switzerland-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-switzerland-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-switzerland

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[ebill_postfinance](ebill_postfinance/) | 17.0.1.0.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Postfinance eBill integration
[ebill_postfinance_server_env](ebill_postfinance_server_env/) | 17.0.1.0.0 |  | Server environment for eBill Postfinance
[ebill_postfinance_stock](ebill_postfinance_stock/) | 17.0.1.0.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Add stock integration to Postfinance eBill
[l10n_ch_qr_no_amount](l10n_ch_qr_no_amount/) | 17.0.1.0.0 | <a href='https://github.com/grindtildeath'><img src='https://github.com/grindtildeath.png' width='32' height='32' style='border-radius:50%;' alt='grindtildeath'/></a> | Allow to print QR bill without amount

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-thailand&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/l10n-thailand/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-thailand/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/l10n-thailand/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-thailand/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/l10n-thailand/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-thailand)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-thailand-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-thailand-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-thailand

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[currency_rate_update_TH_BOT](currency_rate_update_TH_BOT/) | 17.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Currency Rate Update - BOT
[l10n_th_amount_to_text](l10n_th_amount_to_text/) | 17.0.1.0.0 | <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Convert Amount Text to Thai
[l10n_th_base_sequence](l10n_th_base_sequence/) | 17.0.1.0.0 | <a href='https://github.com/sansirit'><img src='https://github.com/sansirit.png' width='32' height='32' style='border-radius:50%;' alt='sansirit'/></a> <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Thai Localization - Base Sequence
[l10n_th_fonts](l10n_th_fonts/) | 17.0.1.0.0 | <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Collection of all Thai fonts
[l10n_th_mis_report](l10n_th_mis_report/) | 17.0.1.1.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Thai Localization - MIS Report
[l10n_th_partner](l10n_th_partner/) | 17.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Thai Localization - Partner
[l10n_th_tier_department](l10n_th_tier_department/) | 17.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Thai Localization - Tier Department Level
[l10n_th_tier_department_demo](l10n_th_tier_department_demo/) | 17.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Thai Localization - Tier Department Level Demo

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-usa&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/l10n-usa/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-usa/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/l10n-usa/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/l10n-usa/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/l10n-usa/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-usa)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-usa-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-usa-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-usa

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_banking_ach_base](account_banking_ach_base/) | 17.0.1.0.0 |  | Add fields required for North American Banking & Financials
[account_banking_ach_credit_transfer](account_banking_ach_credit_transfer/) | 17.0.1.0.0 |  | Create ACH files for Credit Transfers
[l10n_us_form_1099](l10n_us_form_1099/) | 17.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Manage 1099 Types and Suppliers
[l10n_us_gaap](l10n_us_gaap/) | 17.0.1.0.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> | United States Sample GAAP Chart of Accounts
[l10n_us_gaap_mis_report](l10n_us_gaap_mis_report/) | 17.0.1.0.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> | MIS Builder Templates for US Chart of Accounts
[l10n_us_mis_financial_report](l10n_us_mis_financial_report/) | 17.0.1.0.0 | <a href='https://github.com/Christian-RB'><img src='https://github.com/Christian-RB.png' width='32' height='32' style='border-radius:50%;' alt='Christian-RB'/></a> | Profit & Loss (US) / Balance sheet (US) MIS templates
[l10n_us_partner_legal_number](l10n_us_partner_legal_number/) | 17.0.1.0.0 |  | Add Legal Number for North American Banking & Financials

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/mail&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/mail/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/mail/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/mail/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/mail/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/mail/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/mail)
[![Translation Status](https://translation.odoo-community.org/widgets/mail-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/mail-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# mail

mail

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[mail_activity_future_counter](mail_activity_future_counter/) | 17.0.1.0.0 |  | Add a badge counter on the bottom-right of the activity clock icon of the navigation bar, showing the count of future activities.
[mail_activity_plan_domain](mail_activity_plan_domain/) | 17.0.1.0.0 |  | Apply domain filters to activity plans and their templates
[mail_chatter_split](mail_chatter_split/) | 17.0.1.0.0 |  | Separate user messages, activities and automatic logs in the chatter
[mail_message_search](mail_message_search/) | 17.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Mail Message Search
[mail_notification_link](mail_notification_link/) | 17.0.1.0.0 |  | Navigate to document by clicking on notification name
[mail_notification_sound_volume](mail_notification_sound_volume/) | 17.0.1.0.0 |  | Allow users to configure notification sound volume
[mail_notify_employee_leave](mail_notify_employee_leave/) | 17.0.1.0.0 |  | Notifies users when they mention or assign someone who is out of office.
[mail_sent_history](mail_sent_history/) | 17.0.1.0.0 |  | View and browse messages and notes you have sent
[mail_template_domain](mail_template_domain/) | 17.0.1.0.0 |  | Filter mail templates by domain on the active record

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/maintenance&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/maintenance/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/maintenance/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/maintenance/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/maintenance/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/maintenance/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/maintenance)
[![Translation Status](https://translation.odoo-community.org/widgets/maintenance-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/maintenance-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# maintenance

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_maintenance](base_maintenance/) | 17.0.1.1.0 |  | Base Maintenance
[maintenance_account](maintenance_account/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Account
[maintenance_equipment_category_hierarchy](maintenance_equipment_category_hierarchy/) | 17.0.1.0.0 |  | Equipment Categories Hierarchy
[maintenance_equipment_contract](maintenance_equipment_contract/) | 17.0.1.0.1 |  | Manage equipment contracts
[maintenance_equipment_hierarchy](maintenance_equipment_hierarchy/) | 17.0.1.0.1 | <a href='https://github.com/dalonsod'><img src='https://github.com/dalonsod.png' width='32' height='32' style='border-radius:50%;' alt='dalonsod'/></a> | Manage equipment hierarchy
[maintenance_equipment_sequence](maintenance_equipment_sequence/) | 17.0.1.0.1 | <a href='https://github.com/AdriaGForgeFlow'><img src='https://github.com/AdriaGForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='AdriaGForgeFlow'/></a> | Adds sequence to maintenance equipment defined in the equipment's category
[maintenance_equipment_status](maintenance_equipment_status/) | 17.0.1.0.0 |  | Maintenance Equipment Status
[maintenance_equipment_usage](maintenance_equipment_usage/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Equipment Usage
[maintenance_location](maintenance_location/) | 17.0.1.1.0 |  | Define a location system for maintenance
[maintenance_plan](maintenance_plan/) | 17.0.1.1.2 |  | Extends preventive maintenance planning
[maintenance_product](maintenance_product/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Product
[maintenance_project](maintenance_project/) | 17.0.2.0.0 |  | Adds projects to maintenance equipments and requests
[maintenance_request_employee](maintenance_request_employee/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Request Employee
[maintenance_request_purchase](maintenance_request_purchase/) | 17.0.1.0.0 |  | Allows you to link PO with maintenance requests
[maintenance_timesheet](maintenance_timesheet/) | 17.0.1.1.0 |  | Adds timesheets to maintenance requests
[maintenance_timesheet_time_control](maintenance_timesheet_time_control/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Timesheets Timesheet Time Control

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/management-system&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/management-system/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/management-system/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/management-system/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/management-system/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/management-system/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/management-system)
[![Translation Status](https://translation.odoo-community.org/widgets/management-system-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/management-system-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Management System

Odoo modules to support management systems

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[document_page_environment_manual](document_page_environment_manual/) | 17.0.1.0.1 |  | Document Management - Wiki - Environment Manual
[document_page_environmental_aspect](document_page_environmental_aspect/) | 17.0.1.0.1 |  | Environmental Aspects
[document_page_health_safety_manual](document_page_health_safety_manual/) | 17.0.1.0.1 |  | Health and Safety Manual
[document_page_procedure](document_page_procedure/) | 17.0.1.0.1 |  | Document Management - Wiki - Procedures
[document_page_quality_manual](document_page_quality_manual/) | 17.0.1.0.1 |  | Quality Manual
[document_page_work_instruction](document_page_work_instruction/) | 17.0.1.0.1 |  | Document Management - Wiki - Work Instructions
[mgmtsystem](mgmtsystem/) | 17.0.1.3.0 |  | Management System
[mgmtsystem_action](mgmtsystem_action/) | 17.0.1.0.1 |  | Management System - Action
[mgmtsystem_action_efficacy](mgmtsystem_action_efficacy/) | 17.0.1.0.1 |  | Add information on the application of the Action.
[mgmtsystem_action_template](mgmtsystem_action_template/) | 17.0.1.0.0 |  | Add Template management for Actions.
[mgmtsystem_audit](mgmtsystem_audit/) | 17.0.1.2.0 |  | Management System - Audit
[mgmtsystem_hazard](mgmtsystem_hazard/) | 17.0.1.1.0 |  | Hazard
[mgmtsystem_hazard_risk](mgmtsystem_hazard_risk/) | 17.0.1.1.0 |  | Hazard Risk
[mgmtsystem_health_safety](mgmtsystem_health_safety/) | 17.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Manage your health and safety management system
[mgmtsystem_info_security_manual](mgmtsystem_info_security_manual/) | 17.0.1.0.0 |  | Information Security Management System Manual
[mgmtsystem_manual](mgmtsystem_manual/) | 17.0.1.0.1 |  | Management System - Manual
[mgmtsystem_nonconformity](mgmtsystem_nonconformity/) | 17.0.1.2.1 |  | Management System - Nonconformity
[mgmtsystem_nonconformity_hazard](mgmtsystem_nonconformity_hazard/) | 17.0.1.0.0 |  | Management System - Nonconformity Hazard
[mgmtsystem_nonconformity_hr](mgmtsystem_nonconformity_hr/) | 17.0.1.0.0 |  | Bridge module between hr and mgmsystem and
[mgmtsystem_nonconformity_maintenance_equipment](mgmtsystem_nonconformity_maintenance_equipment/) | 17.0.1.0.0 |  | Management System - Nonconformity Maintenance Equipment
[mgmtsystem_nonconformity_mrp](mgmtsystem_nonconformity_mrp/) | 17.0.1.0.0 |  | Bridge module between mrp and mgmsystem
[mgmtsystem_nonconformity_product](mgmtsystem_nonconformity_product/) | 17.0.1.0.0 |  | Bridge module between Product and Management System.
[mgmtsystem_nonconformity_quality_control_oca](mgmtsystem_nonconformity_quality_control_oca/) | 17.0.1.0.0 |  | Bridge module between Quality Control and Non Conformities
[mgmtsystem_nonconformity_repair](mgmtsystem_nonconformity_repair/) | 17.0.1.0.0 |  | Bridge module between Repair and Non Conformities
[mgmtsystem_nonconformity_type](mgmtsystem_nonconformity_type/) | 17.0.1.0.0 |  | Add Nonconformity classification for the root context.
[mgmtsystem_partner](mgmtsystem_partner/) | 17.0.1.0.0 |  | Add Management System reference on Partner's Contacts.
[mgmtsystem_quality](mgmtsystem_quality/) | 17.0.1.0.1 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Manage your quality management system
[mgmtsystem_review](mgmtsystem_review/) | 17.0.2.0.0 |  | Management System - Review
[mgmtsystem_review_survey](mgmtsystem_review_survey/) | 17.0.2.0.0 |  | Management System - Review Survey
[mgmtsystem_survey](mgmtsystem_survey/) | 17.0.1.0.0 |  | Management System - Survey

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# manufacture
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/manufacture&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/manufacture/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/manufacture/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/manufacture/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/manufacture/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/manufacture/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/manufacture)
[![Translation Status](https://translation.odoo-community.org/widgets/manufacture-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/manufacture-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_move_line_mrp_info](account_move_line_mrp_info/) | 17.0.1.1.0 |  | Account Move Line Mrp Info
[mrp_attachment_mgmt](mrp_attachment_mgmt/) | 17.0.1.1.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Mrp Attachment Mgmt
[mrp_bom_attribute_match](mrp_bom_attribute_match/) | 17.0.1.0.1 |  | Dynamic BOM component based on product attribute
[mrp_bom_component_menu](mrp_bom_component_menu/) | 17.0.1.0.0 |  | MRP BOM Component Menu
[mrp_bom_hierarchy](mrp_bom_hierarchy/) | 17.0.1.0.1 |  | Make it easy to navigate through BoM hierarchy.
[mrp_bom_tracking](mrp_bom_tracking/) | 17.0.1.0.1 |  | Logs any change to a BoM in the chatter
[mrp_bom_widget_section_and_note_one2many](mrp_bom_widget_section_and_note_one2many/) | 17.0.1.0.0 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Add section and note in Bills of Materials
[mrp_component_operation](mrp_component_operation/) | 17.0.1.0.0 |  | Allows to operate the components from a MO
[mrp_component_operation_scrap_reason](mrp_component_operation_scrap_reason/) | 17.0.1.0.1 |  | Allows to pass a reason to scrap with MRP component operation
[mrp_lot_number_propagation](mrp_lot_number_propagation/) | 17.0.1.0.0 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Propagate a serial number from a component to a finished product
[mrp_lot_production_date](mrp_lot_production_date/) | 17.0.1.0.0 |  | MRP Lot Production Date
[mrp_mass_production_order](mrp_mass_production_order/) | 17.0.2.3.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Create multiple manufacturing orders in one step
[mrp_multi_level](mrp_multi_level/) | 17.0.1.4.1 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Adds an MRP Scheduler
[mrp_multi_level_estimate](mrp_multi_level_estimate/) | 17.0.1.1.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Allows to consider demand estimates using MRP multi level.
[mrp_planned_order_matrix](mrp_planned_order_matrix/) | 17.0.1.0.0 |  | Allows to create fixed planned orders on a grid view.
[mrp_production_back_to_draft](mrp_production_back_to_draft/) | 17.0.1.0.2 |  | Allows to return to draft a confirmed or cancelled MO.
[mrp_production_generator_by_date_interval](mrp_production_generator_by_date_interval/) | 17.0.1.0.0 |  | MRP Production Generator By Date Interval
[mrp_production_note](mrp_production_note/) | 17.0.1.0.0 |  | Notes in production orders
[mrp_production_picking_type_from_route](mrp_production_picking_type_from_route/) | 17.0.1.0.0 |  | Updates the operation type creating MO based on the product
[mrp_production_quant_manual_assign](mrp_production_quant_manual_assign/) | 17.0.1.0.1 |  | Production - Manual Quant Assignment
[mrp_production_serial_matrix](mrp_production_serial_matrix/) | 17.0.2.0.0 |  | MRP Production Serial Matrix
[mrp_production_serial_matrix_import_xlsx](mrp_production_serial_matrix_import_xlsx/) | 17.0.1.0.0 |  | MRP Production Serial Matrix Import Xlsx
[mrp_production_serial_matrix_queue_job](mrp_production_serial_matrix_queue_job/) | 17.0.1.0.0 |  | MRP Production Serial Matrix Queue Job
[mrp_repair_order](mrp_repair_order/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Create repair order from manufacturing order
[mrp_sale_info](mrp_sale_info/) | 17.0.1.1.0 |  | Adds sale information to Manufacturing models
[mrp_subcontracting_bom_dual_use](mrp_subcontracting_bom_dual_use/) | 17.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Mrp subcontracting bom dual use
[mrp_subcontracting_purchase_link](mrp_subcontracting_purchase_link/) | 17.0.1.0.0 |  | Link Purchase Order Line to Subcontract Productions
[mrp_subcontracting_skip_no_negative](mrp_subcontracting_skip_no_negative/) | 17.0.1.0.1 |  | MRP Subcontracting Skip No Negative
[mrp_tag](mrp_tag/) | 17.0.1.0.0 |  | Allows to add multiple tags to Manufacturing Orders
[mrp_warehouse_calendar](mrp_warehouse_calendar/) | 17.0.1.0.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> | Considers the warehouse calendars in manufacturing
[mrp_workorder_sequence](mrp_workorder_sequence/) | 17.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | adds sequence to production work orders.
[purchase_mrp_distribution](purchase_mrp_distribution/) | 17.0.1.0.0 |  | Purchase MRP Distribution
[quality_control_mrp_oca](quality_control_mrp_oca/) | 17.0.1.1.0 |  | MRP extension for quality control (OCA)
[quality_control_oca](quality_control_oca/) | 17.0.1.5.0 |  | Generic infrastructure for quality tests.
[quality_control_oca_timesheet](quality_control_oca_timesheet/) | 17.0.1.0.0 | <a href='https://github.com/ppyczko'><img src='https://github.com/ppyczko.png' width='32' height='32' style='border-radius:50%;' alt='ppyczko'/></a> | Quality Control - Timesheet (OCA)
[quality_control_stock_oca](quality_control_stock_oca/) | 17.0.2.1.0 |  | Quality control - Stock (OCA)
[stock_replenishment_mrp_bom_selection](stock_replenishment_mrp_bom_selection/) | 17.0.1.0.0 |  | Stock Replenishment MRP BoM Selection

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/manufacture-reporting&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/manufacture-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/manufacture-reporting/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/manufacture-reporting/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/manufacture-reporting/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/manufacture-reporting/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/manufacture-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/manufacture-reporting-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/manufacture-reporting-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# manufacture-reporting

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[mrp_bom_current_stock](mrp_bom_current_stock/) | 17.0.1.0.0 |  | Add a report that explodes the bill of materials and show the stock available in the source location.
[mrp_bom_structure_report_level_1](mrp_bom_structure_report_level_1/) | 17.0.1.0.0 |  | MRP BOM Structure Report Level 1
[mrp_bom_structure_xlsx](mrp_bom_structure_xlsx/) | 17.0.1.0.1 |  | Export BoM Structure to Excel .XLSX
[mrp_bom_structure_xlsx_level_1](mrp_bom_structure_xlsx_level_1/) | 17.0.1.0.0 |  | Export BOM Structure (Level 1) to Excel .XLSX
[mrp_flattened_bom_xlsx](mrp_flattened_bom_xlsx/) | 17.0.1.0.0 |  | Export Flattened BOM to Excel

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/margin-analysis&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/margin-analysis/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/margin-analysis/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/margin-analysis/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/margin-analysis/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/margin-analysis/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/margin-analysis)
[![Translation Status](https://translation.odoo-community.org/widgets/margin-analysis-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/margin-analysis-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# margin-analysis

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_invoice_margin](account_invoice_margin/) | 17.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Show margin in invoices
[account_invoice_margin_sale](account_invoice_margin_sale/) | 17.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> | Set margin in invoices from sale orders
[sale_margin_security](sale_margin_security/) | 17.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Sale Margin Security
[sale_report_margin](sale_report_margin/) | 17.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Sale Report Margin

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/mis-builder&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/mis-builder/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/mis-builder/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/mis-builder/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/mis-builder/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/mis-builder/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/mis-builder)
[![Translation Status](https://translation.odoo-community.org/widgets/mis-builder-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/mis-builder-17-0/?utm_source=widget)

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
[mis_builder](mis_builder/) | 17.0.1.5.0 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Build 'Management Information System' Reports and Dashboards
[mis_builder_budget](mis_builder_budget/) | 17.0.1.4.0 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Create budgets for MIS reports
[mis_builder_demo](mis_builder_demo/) | 17.0.1.0.0 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Demo addon for MIS Builder

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

## From OCA/mis-builder-contrib


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/mis-builder-contrib&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/mis-builder-contrib/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/mis-builder-contrib/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/mis-builder-contrib/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/mis-builder-contrib/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/mis-builder-contrib/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/mis-builder-contrib)
[![Translation Status](https://translation.odoo-community.org/widgets/mis-builder-contrib-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/mis-builder-contrib-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# mis-builder-contrib

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[mis_builder_analytic](mis_builder_analytic/) | 17.0.1.0.0 |  | Provide account analytic lines for MIS builder reports
[mis_builder_contract](mis_builder_contract/) | 17.0.1.0.0 |  | Provide account contract lines for MIS builder reports

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/multi-company&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/multi-company/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/multi-company/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/multi-company/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/multi-company/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/multi-company/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/multi-company)
[![Translation Status](https://translation.odoo-community.org/widgets/multi-company-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/multi-company-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# multi-company

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_invoice_inter_company](account_invoice_inter_company/) | 17.0.1.1.5 |  | Intercompany invoice rules
[account_multicompany_easy_creation](account_multicompany_easy_creation/) | 17.0.1.0.0 |  | This module adds a wizard to create companies easily
[base_multi_company](base_multi_company/) | 17.0.2.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Provides a base for adding multi-company support to models.
[crm_tag_multi_company](crm_tag_multi_company/) | 17.0.1.0.0 |  | This module add multi-company management to crm tag
[mail_multicompany](mail_multicompany/) | 17.0.1.0.0 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Email Gateway Multi company
[mail_template_multi_company](mail_template_multi_company/) | 17.0.1.0.0 | <a href='https://github.com/Olivier-LAURENT'><img src='https://github.com/Olivier-LAURENT.png' width='32' height='32' style='border-radius:50%;' alt='Olivier-LAURENT'/></a> | Mail Template Multi Company
[partner_multi_company](partner_multi_company/) | 17.0.1.0.3 |  | Select individually the partner visibility on each company
[product_multi_company](product_multi_company/) | 17.0.2.0.0 |  | Select individually the product template visibility on each company
[product_tax_multicompany_default](product_tax_multicompany_default/) | 17.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Product Tax Multi Company Default
[purchase_sale_inter_company](purchase_sale_inter_company/) | 17.0.1.0.0 |  | Intercompany PO/SO rules
[purchase_sale_stock_inter_company](purchase_sale_stock_inter_company/) | 17.0.1.0.2 |  | Intercompany PO/SO rules with warehouse
[res_company_active](res_company_active/) | 17.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add the 'active' feature on company model

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/operating-unit&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/operating-unit/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/operating-unit/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/operating-unit/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/operating-unit/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/operating-unit/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/operating-unit)
[![Translation Status](https://translation.odoo-community.org/widgets/operating-unit-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/operating-unit-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# operating-unit

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_financial_report_operating_unit](account_financial_report_operating_unit/) | 17.0.1.0.0 |  | Introduces Operating Unit (OU) in financial reports
[account_operating_unit](account_operating_unit/) | 17.0.1.3.0 |  | Introduces Operating Unit (OU) in invoices and Accounting Entries with clearing account
[account_operating_unit_access_all](account_operating_unit_access_all/) | 17.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Access all OUs' Accounting
[analytic_operating_unit](analytic_operating_unit/) | 17.0.1.0.0 |  | Analytic Operating Unit
[analytic_operating_unit_access_all](analytic_operating_unit_access_all/) | 17.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Access all OUs' Analytics
[contract_operating_unit](contract_operating_unit/) | 17.0.1.1.0 |  | Contract Operating Unit
[contract_operating_unit_access_all](contract_operating_unit_access_all/) | 17.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Access all OUs' Contracts
[crm_operating_unit](crm_operating_unit/) | 17.0.1.1.0 |  | Operating Unit in CRM
[hr_operating_unit](hr_operating_unit/) | 17.0.1.0.0 |  | HR Operating Unit
[mail_operating_unit](mail_operating_unit/) | 17.0.2.0.0 |  | Mail Operating Unit
[operating_unit](operating_unit/) | 17.0.1.1.1 |  | An operating unit (OU) is an organizational entity part of a company
[operating_unit_access_all](operating_unit_access_all/) | 17.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Access all Operating Units
[pos_operating_unit](pos_operating_unit/) | 17.0.1.0.0 |  | POS with Operating Units
[product_operating_unit](product_operating_unit/) | 17.0.1.0.0 |  | Adds the concept of operating unit (OU) in products
[project_operating_unit](project_operating_unit/) | 17.0.1.1.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | This module adds operating unit information to projects and tasks.
[purchase_operating_unit](purchase_operating_unit/) | 17.0.1.1.0 |  | Adds the concecpt of operating unit (OU) in purchase order management
[report_qweb_operating_unit](report_qweb_operating_unit/) | 17.0.1.0.0 |  | Qweb Report With Operating Unit
[res_partner_operating_unit](res_partner_operating_unit/) | 17.0.1.1.0 |  | Introduces Operating Unit fields in Partner
[sale_operating_unit](sale_operating_unit/) | 17.0.1.1.0 |  | An operating unit (OU) is an organizational entity part of a company
[sale_stock_operating_unit](sale_stock_operating_unit/) | 17.0.1.0.0 |  | An operating unit (OU) is an organizational entity part of a company
[sales_team_operating_unit](sales_team_operating_unit/) | 17.0.1.0.0 |  | Sales Team Operating Unit
[stock_operating_unit](stock_operating_unit/) | 17.0.1.1.0 |  | Adds the concept of operating unit (OU) in stock management
[stock_operating_unit_access_all](stock_operating_unit_access_all/) | 17.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Access all OUs' Stock

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/partner-contact&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/partner-contact/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/partner-contact/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/partner-contact/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/partner-contact/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/partner-contact/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/partner-contact)
[![Translation Status](https://translation.odoo-community.org/widgets/partner-contact-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/partner-contact-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Partner Contact

Contact-related odoo addons.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_partner_company_group](account_partner_company_group/) | 17.0.1.0.0 |  | Adds the possibility to add a company group to a company
[animal](animal/) | 17.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Manage animals information
[base_country_state_translatable](base_country_state_translatable/) | 17.0.1.0.0 |  | Translate Country States
[base_location](base_location/) | 17.0.1.1.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Enhanced zip/npa management system
[base_location_geonames_import](base_location_geonames_import/) | 17.0.1.0.1 |  | Import zip entries from Geonames
[base_location_nuts](base_location_nuts/) | 17.0.1.0.2 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | NUTS Regions
[base_partner_company_group](base_partner_company_group/) | 17.0.1.0.0 |  | Adds the possibility to add a company group to a company
[base_partner_sequence](base_partner_sequence/) | 17.0.1.0.0 |  | Sets customer's code from a sequence
[crm_partner_company_group](crm_partner_company_group/) | 17.0.1.1.0 |  | Adds the possibility to add a company group to a company
[partner_address_split](partner_address_split/) | 17.0.1.0.0 |  | Add specific helper methods
[partner_address_street3](partner_address_street3/) | 17.0.1.0.0 |  | Add a third address line on partners
[partner_affiliate](partner_affiliate/) | 17.0.1.1.0 |  | Partner Affiliates
[partner_category_description](partner_category_description/) | 17.0.1.0.0 | <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Adds a description field to contact categories to improve organization and managment of customer relationships.
[partner_category_security](partner_category_security/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Partner category security
[partner_category_type](partner_category_type/) | 17.0.1.0.0 | <a href='https://github.com/JordiMForgeFlow'><img src='https://github.com/JordiMForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiMForgeFlow'/></a> | Add a selection field 'Type' to classify Contact Tags.
[partner_company_default](partner_company_default/) | 17.0.1.0.0 |  | Partner Company Default
[partner_company_group](partner_company_group/) | 17.0.1.0.0 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Adds the possibility to add a company group to a company
[partner_company_type](partner_company_type/) | 17.0.1.0.0 |  | Adds a company type to partner that are companies
[partner_contact_access_link](partner_contact_access_link/) | 17.0.1.0.0 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Allow to visit the full contact form from a company
[partner_contact_address_default](partner_contact_address_default/) | 17.0.2.0.0 |  | Set a default delivery address, invoice address and contact for contacts
[partner_contact_birthdate](partner_contact_birthdate/) | 17.0.1.1.0 | <a href='https://github.com/Daemo00'><img src='https://github.com/Daemo00.png' width='32' height='32' style='border-radius:50%;' alt='Daemo00'/></a> | Contact's birthdate
[partner_contact_birthplace](partner_contact_birthplace/) | 17.0.1.0.0 |  | This module allows to define a birthplace for partners.
[partner_contact_department](partner_contact_department/) | 17.0.1.0.0 |  | Assign contacts to departments
[partner_contact_gender](partner_contact_gender/) | 17.0.1.0.1 |  | Add gender field to contacts
[partner_contact_job_position](partner_contact_job_position/) | 17.0.1.0.0 |  | Categorize job positions for contacts
[partner_contact_lang](partner_contact_lang/) | 17.0.1.0.0 |  | Manage language in contacts
[partner_contact_nationality](partner_contact_nationality/) | 17.0.1.0.0 |  | Add nationality field to contacts
[partner_contact_personal_information_page](partner_contact_personal_information_page/) | 17.0.1.0.0 | <a href='https://github.com/Daemo00'><img src='https://github.com/Daemo00.png' width='32' height='32' style='border-radius:50%;' alt='Daemo00'/></a> | Add a page to contacts form to put personal information
[partner_contact_role](partner_contact_role/) | 17.0.1.0.0 |  | Add roles to partners.
[partner_country_lang](partner_country_lang/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Partner language according country
[partner_country_state_required](partner_country_state_required/) | 17.0.1.0.0 |  | Partner Country State Required
[partner_data_vies_populator](partner_data_vies_populator/) | 17.0.1.1.0 |  | Populate Partner name and address using the VIES webservice
[partner_deduplicate_acl](partner_deduplicate_acl/) | 17.0.1.0.0 |  | Contact deduplication with fine-grained permission control
[partner_deduplicate_by_website](partner_deduplicate_by_website/) | 17.0.1.0.0 |  | Deduplicate Contacts by Website
[partner_deduplicate_filter](partner_deduplicate_filter/) | 17.0.1.0.0 |  | Exclude records from the deduplication
[partner_disable_gravatar](partner_disable_gravatar/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Disable automatic connection to gravatar.com
[partner_display_name_line_break](partner_display_name_line_break/) | 17.0.1.0.1 |  | Split the company and the partner name on two different lines
[partner_duns](partner_duns/) | 17.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Set DUNS (Data Universal Numbering System) on partners
[partner_email_check](partner_email_check/) | 17.0.1.1.0 |  | Validate email address field
[partner_email_duplicate_warn](partner_email_duplicate_warn/) | 17.0.1.0.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Warning banner on partner form if another partner has the same email
[partner_employee_quantity](partner_employee_quantity/) | 17.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | Know how many employees a partner has
[partner_external_map](partner_external_map/) | 17.0.1.0.0 |  | Add Map and Map Routing buttons on partner form to open GMaps, OSM, Bing and others
[partner_fax](partner_fax/) | 17.0.1.1.0 |  | Add fax number on partner
[partner_firstname](partner_firstname/) | 17.0.1.1.0 |  | Split first name and last name for non company partners
[partner_identification](partner_identification/) | 17.0.1.2.0 |  | Partner Identification Numbers
[partner_identification_gln](partner_identification_gln/) | 17.0.1.0.0 |  | This addon extends "Partner Identification Numbers" to provide a number category for GLN registration
[partner_industry_secondary](partner_industry_secondary/) | 17.0.1.1.1 |  | Add secondary partner industries
[partner_lastname_uppercase](partner_lastname_uppercase/) | 17.0.1.0.0 |  | Uppercases the the last names of partners
[partner_manual_rank](partner_manual_rank/) | 17.0.1.1.0 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> <a href='https://github.com/frahikLV'><img src='https://github.com/frahikLV.png' width='32' height='32' style='border-radius:50%;' alt='frahikLV'/></a> | Be able to manually flag partners as customer or supplier.
[partner_multi_relation](partner_multi_relation/) | 17.0.1.0.0 |  | Partner Relations
[partner_phonecall_schedule](partner_phonecall_schedule/) | 17.0.1.0.0 |  | Track the time and days your partners expect phone calls
[partner_pricelist_search](partner_pricelist_search/) | 17.0.1.0.0 |  | Partner pricelist search
[partner_priority](partner_priority/) | 17.0.1.0.0 | <a href='https://github.com/patrickrwilson'><img src='https://github.com/patrickrwilson.png' width='32' height='32' style='border-radius:50%;' alt='patrickrwilson'/></a> | Adds priority to partners.
[partner_property](partner_property/) | 17.0.1.1.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Partner Property
[partner_purchase_manager](partner_purchase_manager/) | 17.0.1.0.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Add purchase manager field in partner
[partner_readonly_security](partner_readonly_security/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Partner Readonly Security
[partner_ref_unique](partner_ref_unique/) | 17.0.1.1.0 |  | Add an unique constraint to partner ref field
[partner_salesperson_propagate](partner_salesperson_propagate/) | 17.0.1.0.0 |  | Propagate any changes in the salesperson field from the partner to its contacts.
[partner_search_alias](partner_search_alias/) | 17.0.1.0.0 |  | Partner Search Alias
[partner_second_lastname](partner_second_lastname/) | 17.0.1.0.2 |  | Have split first and second lastnames
[partner_shipping_policy](partner_shipping_policy/) | 17.0.1.0.0 |  | Define shipping policy at partners level.
[partner_socialmedia](partner_socialmedia/) | 17.0.1.0.1 |  | Add social media fields to contacts
[partner_stage](partner_stage/) | 17.0.1.1.0 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Add lifecycle Stages to Partners
[partner_stage_only_confirmed](partner_stage_only_confirmed/) | 17.0.1.1.0 |  | Adds filters on form views to display only confirmed partners
[partner_store](partner_store/) | 17.0.1.0.0 | <a href='https://github.com/wouitmil'><img src='https://github.com/wouitmil.png' width='32' height='32' style='border-radius:50%;' alt='wouitmil'/></a> | Add store type to Partners
[partner_subject_to_vat](partner_subject_to_vat/) | 17.0.1.0.0 | <a href='https://github.com/victor-champonnois'><img src='https://github.com/victor-champonnois.png' width='32' height='32' style='border-radius:50%;' alt='victor-champonnois'/></a> | Record whether a company is subject to VAT.
[partner_tier_validation](partner_tier_validation/) | 17.0.1.0.1 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Support a tier validation process for Contacts
[partner_title_active](partner_title_active/) | 17.0.1.0.0 |  | Partner Title Active
[partner_tz](partner_tz/) | 17.0.1.0.0 |  | Remove partner timezone default value and display on form
[partner_utm_source](partner_utm_source/) | 17.0.1.0.0 |  | This module adds the use of utm source in partners
[partner_vat_unique](partner_vat_unique/) | 17.0.1.0.0 |  | Module to make the VAT number unique for customers and suppliers.
[sale_customer_rank](sale_customer_rank/) | 17.0.1.0.0 |  | Update Customer Rank when creating a Sale Order
[sale_partner_company_group](sale_partner_company_group/) | 17.0.1.0.0 |  | Adds the possibility to add a company group to a company

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/payroll&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/payroll/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/payroll/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/payroll/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/payroll/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/payroll/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/payroll)
[![Translation Status](https://translation.odoo-community.org/widgets/payroll-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/payroll-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Modules to manage your Payroll in Odoo

Modules to manage your Payroll in Odoo

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[hr_payroll_document](hr_payroll_document/) | 17.0.1.1.2 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Manage payroll for each employee
[payroll](payroll/) | 17.0.1.2.1 | <a href='https://github.com/appstogrow'><img src='https://github.com/appstogrow.png' width='32' height='32' style='border-radius:50%;' alt='appstogrow'/></a> <a href='https://github.com/nimarosa'><img src='https://github.com/nimarosa.png' width='32' height='32' style='border-radius:50%;' alt='nimarosa'/></a> | Manage your employee payroll records
[payroll_account](payroll_account/) | 17.0.1.0.0 | <a href='https://github.com/appstogrow'><img src='https://github.com/appstogrow.png' width='32' height='32' style='border-radius:50%;' alt='appstogrow'/></a> <a href='https://github.com/nimarosa'><img src='https://github.com/nimarosa.png' width='32' height='32' style='border-radius:50%;' alt='nimarosa'/></a> | Manage your payroll to accounting
[payroll_contract_advantages](payroll_contract_advantages/) | 17.0.1.0.0 | <a href='https://github.com/nimarosa'><img src='https://github.com/nimarosa.png' width='32' height='32' style='border-radius:50%;' alt='nimarosa'/></a> | Allow to define contract advantages for employees.
[payroll_hr_public_holidays](payroll_hr_public_holidays/) | 17.0.1.0.0 | <a href='https://github.com/nimarosa'><img src='https://github.com/nimarosa.png' width='32' height='32' style='border-radius:50%;' alt='nimarosa'/></a> | Integration between payroll and hr_public_holidays

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/pos&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/pos/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/pos/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/pos/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/pos/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/pos/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/pos)
[![Translation Status](https://translation.odoo-community.org/widgets/pos-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/pos-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Point of Sale

Odoo modules for Point of Sale.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[pos_cash_control_extension](pos_cash_control_extension/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | This module extends the cash in/out control
[pos_cash_move_reason](pos_cash_move_reason/) | 17.0.1.0.0 |  | POS cash in-out reason
[pos_category_vertical_display](pos_category_vertical_display/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | POS Category Vertical Display
[pos_config_phone](pos_config_phone/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Display phone of POS in ticket
[pos_customer_age_warning](pos_customer_age_warning/) | 17.0.0.1.0 |  | Display customer's age in POS interface according to the age setting
[pos_customer_history_color](pos_customer_history_color/) | 17.0.1.0.0 | <a href='https://github.com/Serpent Consulting Services Pvt. Ltd.'><img src='https://github.com/Serpent Consulting Services Pvt. Ltd..png' width='32' height='32' style='border-radius:50%;' alt='Serpent Consulting Services Pvt. Ltd.'/></a> | Point of Sale - Customer history color
[pos_early_receipt_printing](pos_early_receipt_printing/) | 17.0.1.0.0 |  | Generate bill from Shop
[pos_hide_cost_price_and_margin](pos_hide_cost_price_and_margin/) | 17.0.1.0.0 |  | Hide Cost and Margin on PoS
[pos_lot_barcode](pos_lot_barcode/) | 17.0.1.0.2 |  | Scan barcode to enter lot/serial numbers
[pos_lot_selection](pos_lot_selection/) | 17.0.1.0.1 |  | POS Lot Selection
[pos_margin](pos_margin/) | 17.0.1.1.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Margin on PoS Order
[pos_open_cashbox_after_payment](pos_open_cashbox_after_payment/) | 17.0.1.0.0 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> | Allways Open the cashbox when a payment is made
[pos_order_attachment](pos_order_attachment/) | 17.0.1.0.1 |  | Add attachments on a point of sale order
[pos_order_copy](pos_order_copy/) | 17.0.1.0.0 |  | Copy Orders from PoS Frontend
[pos_order_line_customer_history](pos_order_line_customer_history/) | 17.0.1.0.0 | <a href='https://github.com/Serpent Consulting Services Pvt. Ltd.'><img src='https://github.com/Serpent Consulting Services Pvt. Ltd..png' width='32' height='32' style='border-radius:50%;' alt='Serpent Consulting Services Pvt. Ltd.'/></a> | Adds product in the customer history screen of POS
[pos_order_line_show_product_info](pos_order_line_show_product_info/) | 17.0.1.0.0 | <a href='https://github.com/Serpent Consulting Services Pvt. Ltd.'><img src='https://github.com/Serpent Consulting Services Pvt. Ltd..png' width='32' height='32' style='border-radius:50%;' alt='Serpent Consulting Services Pvt. Ltd.'/></a> | Point of Sale - Orderline Product Info
[pos_order_split_invoice](pos_order_split_invoice/) | 17.0.1.0.0 |  | Allow to generate a secondary invoice from a point of sale order for a second partner
[pos_order_to_sale_order](pos_order_to_sale_order/) | 17.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | PoS Order To Sale Order
[pos_partner_address_required](pos_partner_address_required/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Put partner address required in pos
[pos_partner_birthdate](pos_partner_birthdate/) | 17.0.1.1.0 | <a href='https://github.com/ecino'><img src='https://github.com/ecino.png' width='32' height='32' style='border-radius:50%;' alt='ecino'/></a> | Adds the birthdate in the customer screen of POS
[pos_partner_firstname](pos_partner_firstname/) | 17.0.1.0.1 | <a href='https://github.com/robyf70'><img src='https://github.com/robyf70.png' width='32' height='32' style='border-radius:50%;' alt='robyf70'/></a> | POS Support of partner firstname
[pos_partner_firstname_required](pos_partner_firstname_required/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Put partner firstname required in pos
[pos_partner_ref](pos_partner_ref/) | 17.0.1.0.0 | <a href='https://github.com/invitu'><img src='https://github.com/invitu.png' width='32' height='32' style='border-radius:50%;' alt='invitu'/></a> | Adds the partner ref in the customer screen of POS
[pos_partner_sale_warning](pos_partner_sale_warning/) | 17.0.1.0.0 |  | Show partner sales warning in POS
[pos_partner_second_lastname](pos_partner_second_lastname/) | 17.0.1.0.0 |  | Manage second last name inside Point Of Sale Frontend
[pos_partner_vat_required](pos_partner_vat_required/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Put partner vat required in pos
[pos_partner_vat_valid](pos_partner_vat_valid/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Validate partner vat in POS
[pos_payment_method_cashdro](pos_payment_method_cashdro/) | 17.0.1.0.0 |  | Allows to pay with CashDro Terminals on the Point of Sale
[pos_product_expiry](pos_product_expiry/) | 17.0.1.0.1 |  | Evaluate expiry of lot
[pos_product_info_location](pos_product_info_location/) | 17.0.1.0.0 | <a href='https://github.com/Serpent Consulting Services Pvt. Ltd.'><img src='https://github.com/Serpent Consulting Services Pvt. Ltd..png' width='32' height='32' style='border-radius:50%;' alt='Serpent Consulting Services Pvt. Ltd.'/></a> | Point of Sale - Product Info Location
[pos_product_template](pos_product_template/) | 17.0.1.0.0 |  | Manage Product Template in Front End Point Of Sale
[pos_receipt_gift_card](pos_receipt_gift_card/) | 17.0.1.0.0 |  | Attach the generated gift card code to the sales ticket
[pos_session_sequence](pos_session_sequence/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Generates a sequence of POS sessions
[pos_show_clock](pos_show_clock/) | 17.0.1.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/ygcarvalh'><img src='https://github.com/ygcarvalh.png' width='32' height='32' style='border-radius:50%;' alt='ygcarvalh'/></a> <a href='https://github.com/felipezago'><img src='https://github.com/felipezago.png' width='32' height='32' style='border-radius:50%;' alt='felipezago'/></a> | Point of Sale: Display Current Date and Time on POS sreen
[pos_stock_available_online](pos_stock_available_online/) | 17.0.1.0.0 |  | Show the available quantity of products in the Point of Sale
[pos_user_restrict_stripe_bypass_user](pos_user_restrict_stripe_bypass_user/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | POS User Restrict Strype Bypass User
[pos_user_restriction](pos_user_restriction/) | 17.0.1.0.1 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Restrict some users to see and use only certain points of sale

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/product-attribute&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/product-attribute/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/product-attribute/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/product-attribute/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/product-attribute/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/product-attribute/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/product-attribute)
[![Translation Status](https://translation.odoo-community.org/widgets/product-attribute-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/product-attribute-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# product-attribute

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[product_assortment](product_assortment/) | 17.0.1.0.0 |  | Adds the ability to manage products assortment
[product_attribute_auto_add](product_attribute_auto_add/) | 17.0.1.0.0 | <a href='https://github.com/mike-cetmix'><img src='https://github.com/mike-cetmix.png' width='32' height='32' style='border-radius:50%;' alt='mike-cetmix'/></a> | Add new attribute values to product templates automatically
[product_attribute_company_favorite](product_attribute_company_favorite/) | 17.0.1.0.0 | <a href='https://github.com/victor-champonnois'><img src='https://github.com/victor-champonnois.png' width='32' height='32' style='border-radius:50%;' alt='victor-champonnois'/></a> | Possibility to set favorite product attributes per company
[product_category_active](product_category_active/) | 17.0.1.0.0 |  | Add option to archive product categories
[product_category_code](product_category_code/) | 17.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Allows to define a code on product categories
[product_category_code_unique](product_category_code_unique/) | 17.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Allows to set product category code field as unique
[product_category_description](product_category_description/) | 17.0.1.0.0 | <a href='https://github.com/MarcBForgeFlow'><img src='https://github.com/MarcBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='MarcBForgeFlow'/></a> | Allows to add a detailed description for a product category.
[product_category_product_link](product_category_product_link/) | 17.0.1.0.0 |  | Allows to get products from a category
[product_code_mandatory](product_code_mandatory/) | 17.0.1.0.0 |  | Set Product Internal Reference as a required field
[product_code_unique](product_code_unique/) | 17.0.1.0.0 |  | Set Product Internal Reference as Unique
[product_company_default](product_company_default/) | 17.0.1.0.0 | <a href='https://github.com/AungKoKoLin1997'><img src='https://github.com/AungKoKoLin1997.png' width='32' height='32' style='border-radius:50%;' alt='AungKoKoLin1997'/></a> | Product Company Default
[product_cost_security](product_cost_security/) | 17.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Product cost security restriction view
[product_dimension](product_dimension/) | 17.0.1.0.0 |  | Product Dimension
[product_document_domain](product_document_domain/) | 17.0.1.0.0 | <a href='https://github.com/tisho99'><img src='https://github.com/tisho99.png' width='32' height='32' style='border-radius:50%;' alt='tisho99'/></a> | More user friendly domain and new filters for product documents
[product_form_pricelist](product_form_pricelist/) | 17.0.1.0.0 |  | Show/edit pricelist in product form
[product_logistics_uom](product_logistics_uom/) | 17.0.1.0.0 | <a href='https://github.com/hparfr'><img src='https://github.com/hparfr.png' width='32' height='32' style='border-radius:50%;' alt='hparfr'/></a> | Configure product weights and volume UoM
[product_logistics_uom_total_weight](product_logistics_uom_total_weight/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | View the product weight in differents views
[product_lot_sequence](product_lot_sequence/) | 17.0.1.0.0 |  | Adds ability to define a lot sequence from the product
[product_main_supplierinfo](product_main_supplierinfo/) | 17.0.1.0.1 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Display the main vendor of a product.
[product_manufacturer](product_manufacturer/) | 17.0.1.0.0 |  | Adds manufacturers and attributes on the product view.
[product_multi_category](product_multi_category/) | 17.0.1.0.0 |  | Product - Many Categories
[product_multi_code](product_multi_code/) | 17.0.1.1.0 |  | Allow multiple internal references (default_code) per product
[product_net_weight](product_net_weight/) | 17.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add 'Net Weight' on product models
[product_origin](product_origin/) | 17.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Adds the origin of the product
[product_packaging_dimension](product_packaging_dimension/) | 17.0.1.0.0 |  | Manage packaging dimensions and weight
[product_packaging_level](product_packaging_level/) | 17.0.1.0.0 |  | This module binds a product packaging to a packaging level
[product_packaging_level_salable](product_packaging_level_salable/) | 17.0.1.0.0 |  | Product Packaging level salable
[product_pricelist_assortment](product_pricelist_assortment/) | 17.0.1.0.0 |  | Product assortment and pricelist
[product_pricelist_by_contact](product_pricelist_by_contact/) | 17.0.1.0.0 |  | Product Pricelist Per Contact
[product_pricelist_direct_print](product_pricelist_direct_print/) | 17.0.1.1.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Print price list from menu option, product templates, products variants or price lists
[product_pricelist_fixed_currency_rate](product_pricelist_fixed_currency_rate/) | 17.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/kobros-tech'><img src='https://github.com/kobros-tech.png' width='32' height='32' style='border-radius:50%;' alt='kobros-tech'/></a> | Set a fixed currency rate between pricelists
[product_pricelist_item_list_view](product_pricelist_item_list_view/) | 17.0.1.1.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | View and search the list of pricelist items
[product_pricelist_revision](product_pricelist_revision/) | 17.0.1.0.0 |  | Product Pricelist Revision
[product_pricelist_simulation](product_pricelist_simulation/) | 17.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Simulate the product price for all pricelists
[product_pricelist_supplierinfo](product_pricelist_supplierinfo/) | 17.0.2.1.0 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Allows to create priceslists based on supplier info
[product_print_category](product_print_category/) | 17.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Define print categories for products and automate products print, when data has changed
[product_product_template_link](product_product_template_link/) | 17.0.1.0.0 |  | Adds a button in product to view the template
[product_profile](product_profile/) | 17.0.1.0.0 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> <a href='https://github.com/kevinkhao'><img src='https://github.com/kevinkhao.png' width='32' height='32' style='border-radius:50%;' alt='kevinkhao'/></a> | Allow to configure a product in 1 click
[product_readonly_security](product_readonly_security/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Product Readonly Security
[product_restricted_type](product_restricted_type/) | 17.0.1.0.0 |  | Product Restricted Type
[product_route_mto](product_route_mto/) | 17.0.1.0.0 |  | This module allows to compute if a product is an 'MTO' one from its configured routes
[product_secondary_unit](product_secondary_unit/) | 17.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Set a secondary unit per product
[product_sequence](product_sequence/) | 17.0.1.0.0 |  | Product Sequence
[product_set](product_set/) | 17.0.1.0.1 |  | Product set
[product_state](product_state/) | 17.0.1.2.1 | <a href='https://github.com/emagdalenaC2i'><img src='https://github.com/emagdalenaC2i.png' width='32' height='32' style='border-radius:50%;' alt='emagdalenaC2i'/></a> | Module introducing a state field on product template
[product_state_sale](product_state_sale/) | 17.0.1.1.0 |  | This module add the use of Product State in Sale
[product_state_stock_base](product_state_stock_base/) | 17.0.1.1.0 |  | This module add the use of Product State in Stock
[product_status](product_status/) | 17.0.1.2.0 |  | Product Status Computed From Fields
[product_supplierinfo_archive](product_supplierinfo_archive/) | 17.0.1.0.0 | <a href='https://github.com/GuillemCForgeFlow'><img src='https://github.com/GuillemCForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='GuillemCForgeFlow'/></a> <a href='https://github.com/AlvaroTForgeFlow'><img src='https://github.com/AlvaroTForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='AlvaroTForgeFlow'/></a> <a href='https://github.com/OriolVForgeFlow'><img src='https://github.com/OriolVForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='OriolVForgeFlow'/></a> | Add the active field to the product supplier info
[product_supplierinfo_code](product_supplierinfo_code/) | 17.0.1.0.0 |  | Allows to get main supplierinfo product_code on product level
[product_supplierinfo_for_customer](product_supplierinfo_for_customer/) | 17.0.1.1.2 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Allows to define prices for customers in the products
[product_supplierinfo_revision](product_supplierinfo_revision/) | 17.0.1.0.0 |  | Product Supplierinfo Revision
[product_uom_measure_type](product_uom_measure_type/) | 17.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Product - UoM Measure Type
[product_usability](product_usability/) | 17.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Adds missing menu entries for Product module and adds extra groups to fine-tune access rights
[purchase_product_template_tags](purchase_product_template_tags/) | 17.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Show product tags menu in Purchase app
[sale_product_matrix_secondary_unit](sale_product_matrix_secondary_unit/) | 17.0.1.0.0 | <a href='https://github.com/carlos-lopez-tecnativa'><img src='https://github.com/carlos-lopez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carlos-lopez-tecnativa'/></a> | Secondary unit in product matrix
[sale_product_template_tags](sale_product_template_tags/) | 17.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Show product tags menu in Sale app
[stock_product_template_tags](stock_product_template_tags/) | 17.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Show product tags menu in Inventory app
[stock_production_lot_expired_date](stock_production_lot_expired_date/) | 17.0.1.0.1 |  | Stock production lot expired date
[uom_alias](uom_alias/) | 17.0.1.0.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Adds alias for UOM
[uom_category_active](uom_category_active/) | 17.0.1.0.1 |  | Add option to archive UoM categories

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/product-configurator&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/product-configurator/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/product-configurator/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/product-configurator/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/product-configurator/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/product-configurator/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/product-configurator)
[![Translation Status](https://translation.odoo-community.org/widgets/product-configurator-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/product-configurator-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# product-configurator

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[product_configurator](product_configurator/) | 17.0.1.0.2 | <a href='https://github.com/PCatinean'><img src='https://github.com/PCatinean.png' width='32' height='32' style='border-radius:50%;' alt='PCatinean'/></a> | Base for product configuration interface modules
[product_configurator_sale](product_configurator_sale/) | 17.0.1.0.0 | <a href='https://github.com/PCatinean'><img src='https://github.com/PCatinean.png' width='32' height='32' style='border-radius:50%;' alt='PCatinean'/></a> | Product configuration interface modules for Sale
[website_product_configurator](website_product_configurator/) | 17.0.1.0.0 | <a href='https://github.com/PCatinean'><img src='https://github.com/PCatinean.png' width='32' height='32' style='border-radius:50%;' alt='PCatinean'/></a> | Configure products in e-shop

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/product-pack&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/product-pack/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/product-pack/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/product-pack/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/product-pack/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/product-pack/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/product-pack)
[![Translation Status](https://translation.odoo-community.org/widgets/product-pack-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/product-pack-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# product-pack

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[product_pack](product_pack/) | 17.0.2.0.1 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | This module allows you to set a product as a Pack
[sale_product_pack](sale_product_pack/) | 17.0.2.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | This module allows you to sell product packs
[sale_product_pack_fixed_discount](sale_product_pack_fixed_discount/) | 17.0.1.0.0 | <a href='https://github.com/petrus-v'><img src='https://github.com/petrus-v.png' width='32' height='32' style='border-radius:50%;' alt='petrus-v'/></a> | Glue module between sale product pack and sale fixed discount
[sale_stock_product_pack](sale_stock_product_pack/) | 17.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Compatibility module for packs that are storable products
[stock_product_pack](stock_product_pack/) | 17.0.1.0.0 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | This module allows you to get the right available quantities of the packs
[website_sale_product_pack](website_sale_product_pack/) | 17.0.2.0.1 |  | Compatibility module of product pack with e-commerce

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/product-variant&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/product-variant/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/product-variant/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/product-variant/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/product-variant/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/product-variant/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/product-variant)
[![Translation Status](https://translation.odoo-community.org/widgets/product-variant-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/product-variant-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# product-variant

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[product_variant_attribute_tax](product_variant_attribute_tax/) | 17.0.1.0.0 |  | Set taxes on the product attribute values
[product_variant_configurator](product_variant_configurator/) | 17.0.1.0.0 |  | Provides an abstract model for product variant configuration.
[product_variant_default_code](product_variant_default_code/) | 17.0.1.0.0 | <a href='https://github.com/Kev-Roche'><img src='https://github.com/Kev-Roche.png' width='32' height='32' style='border-radius:50%;' alt='Kev-Roche'/></a> | Product Variant Default Code
[product_variant_name](product_variant_name/) | 17.0.1.0.0 |  | Product Variant Name
[product_variant_sale_price](product_variant_sale_price/) | 17.0.1.2.1 |  | Allows to write fixed prices in product variants
[purchase_variant_configurator](purchase_variant_configurator/) | 17.0.1.0.1 |  | Product variants in purchase management

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/project&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/project/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/project/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/project/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/project/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/project/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/project)
[![Translation Status](https://translation.odoo-community.org/widgets/project-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/project-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# project

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[project_administrator_restricted_visibility](project_administrator_restricted_visibility/) | 17.0.1.0.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | Adds a 'Project Administrator' access group with restricted visibility to 'Projects'
[project_analytic_code](project_analytic_code/) | 17.0.0.1.0 |  | Search projects by analytic account code.
[project_department](project_department/) | 17.0.1.0.0 |  | Project Department Categorization
[project_group](project_group/) | 17.0.1.0.0 |  | Add groups for filtering on projects
[project_group_hr_timesheet](project_group_hr_timesheet/) | 17.0.1.0.0 |  | This module makes project group work properly with timesheets
[project_hr](project_hr/) | 17.0.1.0.2 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Link HR with project
[project_key](project_key/) | 17.0.1.1.1 |  | Module decorates projects and tasks with Project Key
[project_merge](project_merge/) | 17.0.1.0.0 |  | Wizard to merge project tasks
[project_milestone_status](project_milestone_status/) | 17.0.1.0.0 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | Project Milestone Status
[project_parent](project_parent/) | 17.0.1.0.0 |  | Project Parent
[project_parent_task_filter](project_parent_task_filter/) | 17.0.1.0.0 |  | Add a filter to show the parent tasks
[project_portal_task_visibility](project_portal_task_visibility/) | 17.0.1.0.0 |  | Project Portal Task Visibility
[project_purchase_link](project_purchase_link/) | 17.0.1.0.0 |  | Project Purchase Link
[project_risk](project_risk/) | 17.0.1.0.0 |  | MOR risk management method
[project_role](project_role/) | 17.0.1.0.0 | <a href='https://github.com/alexey-pelykh'><img src='https://github.com/alexey-pelykh.png' width='32' height='32' style='border-radius:50%;' alt='alexey-pelykh'/></a> | Project role-based roster
[project_sequence](project_sequence/) | 17.0.1.0.0 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/anddago78'><img src='https://github.com/anddago78.png' width='32' height='32' style='border-radius:50%;' alt='anddago78'/></a> | Add a sequence field to projects, filled automatically
[project_status](project_status/) | 17.0.1.0.0 | <a href='https://github.com/patrickrwilson'><img src='https://github.com/patrickrwilson.png' width='32' height='32' style='border-radius:50%;' alt='patrickrwilson'/></a> | Project Status
[project_tag_hierarchy](project_tag_hierarchy/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Project Tag Hierarchy
[project_task_add_very_high](project_task_add_very_high/) | 17.0.1.0.0 | <a href='https://github.com/astirpe'><img src='https://github.com/astirpe.png' width='32' height='32' style='border-radius:50%;' alt='astirpe'/></a> | Adds extra options 'High' and 'Very High' on tasks
[project_task_code](project_task_code/) | 17.0.1.0.0 |  | Sequential Code for Tasks
[project_task_default_stage](project_task_default_stage/) | 17.0.1.0.1 |  | Recovery default task stages for projects from v8
[project_task_description_template](project_task_description_template/) | 17.0.1.0.0 |  | Add a description template to project tasks
[project_task_material](project_task_material/) | 17.0.1.0.0 |  | Record products spent in a Task
[project_task_name_with_id](project_task_name_with_id/) | 17.0.1.0.1 |  | Project Task Name with ID
[project_task_note](project_task_note/) | 17.0.1.0.2 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Add notes in project tasks
[project_task_pull_request](project_task_pull_request/) | 17.0.1.0.0 |  | Adds a field for a PR URI to project tasks
[project_task_related](project_task_related/) | 17.0.1.0.3 | <a href='https://github.com/david-banon-tecnativa'><img src='https://github.com/david-banon-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='david-banon-tecnativa'/></a> | Project Related Task
[project_task_stage_mgmt](project_task_stage_mgmt/) | 17.0.1.0.0 | <a href='https://github.com/DavidJForgeFlow'><img src='https://github.com/DavidJForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='DavidJForgeFlow'/></a> | Allows to assign and create task stages on project creation wizard
[project_task_stage_state](project_task_stage_state/) | 17.0.1.0.0 |  | Restore State attribute removed from Project Stages in 8.0
[project_task_tag](project_task_tag/) | 17.0.1.0.0 |  | Limit tags available on task
[project_template](project_template/) | 17.0.1.0.0 | <a href='https://github.com/patrickrwilson'><img src='https://github.com/patrickrwilson.png' width='32' height='32' style='border-radius:50%;' alt='patrickrwilson'/></a> | Project Templates
[project_timeline](project_timeline/) | 17.0.1.2.0 |  | Timeline view for projects
[project_timeline_hr_timesheet](project_timeline_hr_timesheet/) | 17.0.1.0.0 |  | Shows the progress of tasks on the timeline view.
[project_timesheet_time_control](project_timesheet_time_control/) | 17.0.1.1.2 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | Project timesheet time control
[project_type](project_type/) | 17.0.1.0.2 |  | Project Types
[project_version](project_version/) | 17.0.1.0.0 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | Project Version
[sale_project_reimbursement_cost](sale_project_reimbursement_cost/) | 17.0.1.0.0 |  | Display provisions and reimbursement costs in the Project Updates dashboard.
[sale_project_task_recurrency](sale_project_task_recurrency/) | 17.0.1.2.0 |  | Configuring Task Recurrence from the Product Form.

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/purchase-reporting&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/purchase-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/purchase-reporting/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/purchase-reporting/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/purchase-reporting/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/purchase-reporting/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/purchase-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/purchase-reporting-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/purchase-reporting-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# purchase-reporting

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[purchase_comment_template](purchase_comment_template/) | 17.0.1.0.0 |  | Comments texts templates on Purchase documents
[purchase_order_report_grouped_by_vendor](purchase_order_report_grouped_by_vendor/) | 17.0.1.0.0 |  | Purchase order report grouping orders by vendor
[purchase_packaging_report](purchase_packaging_report/) | 17.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Packaging data in purchase reports
[purchase_report_date_format](purchase_report_date_format/) | 17.0.1.0.0 |  | Purchase Report Date Format
[purchase_report_hide_line](purchase_report_hide_line/) | 17.0.1.0.0 | <a href='https://github.com/tisho99'><img src='https://github.com/tisho99.png' width='32' height='32' style='border-radius:50%;' alt='tisho99'/></a> | Hide purchase order lines from the Purchase Report
[purchase_report_payment_term](purchase_report_payment_term/) | 17.0.1.0.0 |  | Purchase Report Payment Term
[purchase_report_shipping_address](purchase_report_shipping_address/) | 17.0.1.0.0 |  | Purchase Report Shipping Address

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/purchase-workflow&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/purchase-workflow/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/purchase-workflow/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/purchase-workflow/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/purchase-workflow/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/purchase-workflow/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/purchase-workflow)
[![Translation Status](https://translation.odoo-community.org/widgets/purchase-workflow-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/purchase-workflow-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# purchase-workflow

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[procurement_purchase_no_grouping](procurement_purchase_no_grouping/) | 17.0.1.0.0 |  | Procurement Purchase No Grouping
[procurement_purchase_requisition_generation](procurement_purchase_requisition_generation/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Procurement Purchase Requisition Generation
[procurement_purchase_requisition_generation_dropshipping](procurement_purchase_requisition_generation_dropshipping/) | 17.0.1.0.0 | <a href='https://github.com/carlos-lopez-tecnativa'><img src='https://github.com/carlos-lopez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carlos-lopez-tecnativa'/></a> | Procurement purchase requisition dropshipping
[procurement_purchase_sale_no_grouping](procurement_purchase_sale_no_grouping/) | 17.0.1.0.0 |  | Procurement Purchase Service No Grouping
[product_supplier_code_purchase](product_supplier_code_purchase/) | 17.0.1.0.0 |  | This module adds to the purchase order line the supplier code defined in the product.
[product_supplierinfo_disable_autocreation](product_supplierinfo_disable_autocreation/) | 17.0.1.0.1 |  | Add option to disable automatic creation of pricelists for suppliers
[purchase_advance_payment](purchase_advance_payment/) | 17.0.1.5.1 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Allow to add advance payments on purchase orders
[purchase_advance_payment_line](purchase_advance_payment_line/) | 17.0.1.0.0 |  | Allow to add advance payment lines on purchase orders
[purchase_all_shipments](purchase_all_shipments/) | 17.0.1.0.0 |  | Purchase All Shipments
[purchase_allowed_product](purchase_allowed_product/) | 17.0.1.0.0 |  | This module allows to select only products that can be supplied by the vendor
[purchase_billing_address](purchase_billing_address/) | 17.0.1.0.0 |  | Create a new partner type (purchase), to differentiate the purchase order and invoice addresses.
[purchase_blanket_order](purchase_blanket_order/) | 17.0.1.0.1 |  | Purchase Blanket Orders
[purchase_cancel_reason](purchase_cancel_reason/) | 17.0.1.0.0 |  | Purchase Cancel Reason
[purchase_commercial_partner](purchase_commercial_partner/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add stored related field 'Commercial Supplier' on POs
[purchase_default_terms_conditions](purchase_default_terms_conditions/) | 17.0.1.0.0 |  | This module allows purchase default terms & conditions
[purchase_delivery_split_date](purchase_delivery_split_date/) | 17.0.1.0.3 |  | Allows Purchase Order you confirm to generate one Incoming Shipment for each expected date indicated in the Purchase Order Lines
[purchase_deposit](purchase_deposit/) | 17.0.1.1.1 |  | Option to create deposit from purchase order
[purchase_exception](purchase_exception/) | 17.0.1.0.0 |  | Custom exceptions on purchase order
[purchase_fop_shipping](purchase_fop_shipping/) | 17.0.1.0.1 |  | Purchase Free-Of-Payment shipping
[purchase_force_invoiced](purchase_force_invoiced/) | 17.0.1.0.1 |  | Allows to force the billing status of the purchase order to "Invoiced"
[purchase_invoice_method](purchase_invoice_method/) | 17.0.1.0.0 |  | Allow to force the invoice method of a purchase
[purchase_invoice_plan](purchase_invoice_plan/) | 17.0.1.0.1 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Add to purchases order, ability to manage future invoice plan
[purchase_invoice_status_line](purchase_invoice_status_line/) | 17.0.1.0.1 | <a href='https://github.com/JoanSForgeFlow'><img src='https://github.com/JoanSForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JoanSForgeFlow'/></a> | Add invoice status on purchase order lines
[purchase_last_price_info](purchase_last_price_info/) | 17.0.1.0.3 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Purchase Product Last Price Info
[purchase_location_by_line](purchase_location_by_line/) | 17.0.1.0.1 |  | Allows to define a specific destination location on each PO line
[purchase_lot](purchase_lot/) | 17.0.1.0.1 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Purchase Lot
[purchase_manual_currency](purchase_manual_currency/) | 17.0.1.0.0 |  | Allows to manual currency of Purchase
[purchase_manual_delivery](purchase_manual_delivery/) | 17.0.1.0.1 |  | Prevents pickings to be auto generated upon Purchase Order confirmation and adds the ability to manually generate them as the supplier confirms the different purchase order lines.
[purchase_mass_mail](purchase_mass_mail/) | 17.0.1.0.0 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/anddago78'><img src='https://github.com/anddago78.png' width='32' height='32' style='border-radius:50%;' alt='anddago78'/></a> | Automatically send massive emails to many purchase orders
[purchase_merge](purchase_merge/) | 17.0.1.0.0 |  | Wizard to merge purchase with required conditions
[purchase_no_rfq](purchase_no_rfq/) | 17.0.1.1.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Purchase Order - No Request For Quotation
[purchase_open_qty](purchase_open_qty/) | 17.0.2.0.1 |  | Allows to identify the purchase orders that have quantities pending to invoice or to receive.
[purchase_order_approved](purchase_order_approved/) | 17.0.1.0.2 |  | Add a new state 'Approved' in purchase orders.
[purchase_order_archive](purchase_order_archive/) | 17.0.1.0.0 |  | Archive Purchase Orders
[purchase_order_date_approve_editable](purchase_order_date_approve_editable/) | 17.0.1.0.0 |  | Allows editing the Approval Date on Purchase Orders
[purchase_order_general_discount](purchase_order_general_discount/) | 17.0.1.0.0 |  | General discount per purchase order
[purchase_order_line_deep_sort](purchase_order_line_deep_sort/) | 17.0.1.0.0 |  | Purchase Order Line Sort
[purchase_order_line_menu](purchase_order_line_menu/) | 17.0.1.1.1 |  | Adds Purchase Order Lines Menu
[purchase_order_line_sequence](purchase_order_line_sequence/) | 17.0.1.0.0 |  | Adds sequence to PO lines and propagates it toInvoice lines and Stock Moves
[purchase_order_line_stock_available](purchase_order_line_stock_available/) | 17.0.1.0.0 |  | Purchase order line stock available
[purchase_order_product_recommendation](purchase_order_product_recommendation/) | 17.0.1.0.0 |  | Recommend products to buy to supplier based on history
[purchase_order_qty_change_no_recompute](purchase_order_qty_change_no_recompute/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Prevent recompute if only quantity has changed in purchase order line
[purchase_order_secondary_unit](purchase_order_secondary_unit/) | 17.0.1.0.0 |  | Purchase product in a secondary unit
[purchase_order_supplierinfo_update](purchase_order_supplierinfo_update/) | 17.0.1.0.1 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | Update product supplierinfo with the last purchase price
[purchase_order_type](purchase_order_type/) | 17.0.1.0.2 |  | Purchase Order Type
[purchase_order_type_dashboard](purchase_order_type_dashboard/) | 17.0.1.0.0 | <a href='https://github.com/dalonsod'><img src='https://github.com/dalonsod.png' width='32' height='32' style='border-radius:50%;' alt='dalonsod'/></a> | Purchase Order Type Dashboard
[purchase_order_uninvoiced_amount](purchase_order_uninvoiced_amount/) | 17.0.1.0.1 |  | Purchase Order Univoiced Amount
[purchase_order_uninvoiced_amount_line](purchase_order_uninvoiced_amount_line/) | 17.0.1.0.0 |  | Purchase Order Line Uninvoiced Amount
[purchase_order_weight_volume](purchase_order_weight_volume/) | 17.0.1.0.0 | <a href='https://github.com/ilyasProgrammer'><img src='https://github.com/ilyasProgrammer.png' width='32' height='32' style='border-radius:50%;' alt='ilyasProgrammer'/></a> | Display purchase order weight and volume
[purchase_partner_incoterm](purchase_partner_incoterm/) | 17.0.1.0.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Add a an incoterm field for supplier and use it on purchase order
[purchase_partner_selectable_option](purchase_partner_selectable_option/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Purchase Partner Selectable Option
[purchase_reception_notify](purchase_reception_notify/) | 17.0.1.0.1 |  | Purchase Reception Notify
[purchase_reception_status](purchase_reception_status/) | 17.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add reception status on purchase orders (OCA logic)
[purchase_reception_status_line](purchase_reception_status_line/) | 17.0.1.0.0 | <a href='https://github.com/DavidJForgeFlow'><img src='https://github.com/DavidJForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='DavidJForgeFlow'/></a> | Add reception status on purchase order lines
[purchase_reception_threshold](purchase_reception_threshold/) | 17.0.1.0.0 |  | Purchase Receipt Threshold
[purchase_reorder_control](purchase_reorder_control/) | 17.0.1.0.0 |  | Restrict reordering unpurchaseable product
[purchase_request](purchase_request/) | 17.0.2.3.3 |  | Use this module to have notification of requirements of materials and/or external services and keep track of such requirements.
[purchase_request_department](purchase_request_department/) | 17.0.1.0.0 |  | Purchase Request Department
[purchase_request_tier_validation](purchase_request_tier_validation/) | 17.0.1.1.1 |  | Extends the functionality of Purchase Requests to support a tier validation process.
[purchase_requisition_multiple_vendor](purchase_requisition_multiple_vendor/) | 17.0.1.0.0 |  | Create multiple purchase alternatives for different vendors using the same wizard.
[purchase_requisition_order_remaining_qty](purchase_requisition_order_remaining_qty/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Purchase Requisition Order Remaining Qty
[purchase_requisition_tier_validation](purchase_requisition_tier_validation/) | 17.0.1.0.0 |  | Extends the functionality of Purchase Agreements to support a tier validation process.
[purchase_sale_link_by_origin](purchase_sale_link_by_origin/) | 17.0.1.0.0 |  | Link PO/SO by the PO's Origin in addition to the default behavior that only links them by their lines
[purchase_security](purchase_security/) | 17.0.1.0.3 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | See only your purchase orders
[purchase_start_end_dates](purchase_start_end_dates/) | 17.0.1.0.0 |  | Adds start date and end date on purchase order lines
[purchase_stock_manual_currency](purchase_stock_manual_currency/) | 17.0.1.0.0 |  | Extends manual currency from purchase to stock moves
[purchase_stock_packaging](purchase_stock_packaging/) | 17.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Allows to transmit the product packaging from the procurement values to the generated purchase order line
[purchase_stock_price_unit_sync](purchase_stock_price_unit_sync/) | 17.0.1.0.0 |  | Update cost price in stock moves already done
[purchase_stock_reception_status](purchase_stock_reception_status/) | 17.0.1.0.0 |  | Glue module to integrate OCA reception status with purchase_stock
[purchase_stock_secondary_unit](purchase_stock_secondary_unit/) | 17.0.1.0.0 |  | Get product quantities in a secondary unit
[purchase_tag](purchase_tag/) | 17.0.1.2.0 |  | Allows to add multiple tags to purchase orders
[purchase_tier_validation](purchase_tier_validation/) | 17.0.1.0.0 |  | Extends the functionality of Purchase Orders to support a tier validation process.
[purchase_transport_mode](purchase_transport_mode/) | 17.0.1.0.0 |  | Purchase expection based on constraints
[purchase_triple_discount](purchase_triple_discount/) | 17.0.1.0.0 |  | Manage triple discount on purchase order lines
[purchase_v12_control_menu](purchase_v12_control_menu/) | 17.0.1.0.0 |  | Purchase Control Menu from v12
[purchase_warn_message](purchase_warn_message/) | 17.0.1.0.0 |  | Add a popup warning on purchase to ensure warning is populated
[sale_purchase_force_vendor](sale_purchase_force_vendor/) | 17.0.1.0.2 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Sale Purchase Force Vendor
[supplier_calendar](supplier_calendar/) | 17.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Supplier Calendar

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/queue&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/queue/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/queue/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/queue/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/queue/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/queue/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/queue)
[![Translation Status](https://translation.odoo-community.org/widgets/queue-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/queue-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Queue Job

Asynchronous Job Queue. Delay Model methods in asynchronous jobs, executed in the background as soon as possible or on a schedule. Support Channels to segregates jobs in different queues with different capacities. Unlike scheduled tasks, a job captures arguments for later processing.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_import_async](base_import_async/) | 17.0.1.0.0 |  | Import CSV files in the background
[queue_job](queue_job/) | 17.0.1.5.3 | <a href='https://github.com/guewen'><img src='https://github.com/guewen.png' width='32' height='32' style='border-radius:50%;' alt='guewen'/></a> | Job Queue
[queue_job_cron](queue_job_cron/) | 17.0.1.1.0 |  | Scheduled Actions as Queue Jobs
[queue_job_cron_jobrunner](queue_job_cron_jobrunner/) | 17.0.1.1.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Run jobs without a dedicated JobRunner
[queue_job_subscribe](queue_job_subscribe/) | 17.0.1.0.0 |  | Control which users are subscribed to queue job notifications
[test_queue_job](test_queue_job/) | 17.0.1.2.0 |  | Queue Job Tests

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/repair&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/repair/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/repair/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/repair/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/repair/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/repair/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/repair)
[![Translation Status](https://translation.odoo-community.org/widgets/repair-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/repair-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Repair

Odoo modules related to repairs.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_repair_config](base_repair_config/) | 17.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Provides general settings for the Repair App
[repair_order_line_sequence](repair_order_line_sequence/) | 17.0.1.0.0 |  | Allow to change line order in repairs
[repair_order_template](repair_order_template/) | 17.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Use templates to save time when creating repair orders
[repair_picking](repair_picking/) | 17.0.1.0.0 |  | Enhanced repair order management with pickings for adding and removing components
[repair_picking_after_done](repair_picking_after_done/) | 17.0.1.1.0 |  | Transfer repaired move to another location directly from repair order
[repair_quality_control](repair_quality_control/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Create quality controls from repair order
[repair_quotation_manual_sync](repair_quotation_manual_sync/) | 17.0.1.0.1 |  | Manually Synchronize Repair Orders with their Quotations
[repair_refurbish](repair_refurbish/) | 17.0.2.0.0 |  | Create refurbished products during repair
[repair_restrict_lot](repair_restrict_lot/) | 17.0.1.0.0 |  | Repair Restrict Lot
[repair_service](repair_service/) | 17.0.1.0.1 |  | Adds services to repair orders, so that they can be added as sale order lines.
[repair_stock](repair_stock/) | 17.0.1.1.0 |  | Repair Stock
[repair_stock_move_menu](repair_stock_move_menu/) | 17.0.1.0.0 |  | Adds a menu to obtain a list with repair moves
[repair_substate](repair_substate/) | 17.0.1.0.0 |  | Repair Sub State
[repair_timesheet](repair_timesheet/) | 17.0.1.0.0 | <a href='https://github.com/ppyczko'><img src='https://github.com/ppyczko.png' width='32' height='32' style='border-radius:50%;' alt='ppyczko'/></a> | Repair Timesheet
[repair_type](repair_type/) | 17.0.1.1.1 |  | Repair type
[repair_type_product_destination](repair_type_product_destination/) | 17.0.1.0.0 | <a href='https://github.com/ppyczko'><img src='https://github.com/ppyczko.png' width='32' height='32' style='border-radius:50%;' alt='ppyczko'/></a> | Repair Type - Product Destination

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/report-print-send&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/report-print-send/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/report-print-send/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/report-print-send/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/report-print-send/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/report-print-send/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/report-print-send)
[![Translation Status](https://translation.odoo-community.org/widgets/report-print-send-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/report-print-send-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# report-print-send

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_report_to_printer](base_report_to_printer/) | 17.0.1.2.2 |  | Report to printer
[printer_zpl2](printer_zpl2/) | 17.0.1.1.1 |  | Add a ZPL II label printing feature

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/reporting-engine&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/reporting-engine/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/reporting-engine/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/reporting-engine/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/reporting-engine/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/reporting-engine/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/reporting-engine)
[![Translation Status](https://translation.odoo-community.org/widgets/reporting-engine-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/reporting-engine-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# reporting-engine

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_comment_template](base_comment_template/) | 17.0.1.0.1 |  | Add conditional mako template to any reporton models that inherits comment.template.
[bi_sql_editor](bi_sql_editor/) | 17.0.2.1.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | BI Views builder, based on Materialized or Normal SQL Views
[bi_view_editor](bi_view_editor/) | 17.0.1.1.0 |  | Graphical BI views builder for Odoo
[bi_view_editor_spreadsheet_dashboard](bi_view_editor_spreadsheet_dashboard/) | 17.0.1.0.0 |  | Glue module for BI View Editor and Spreadsheet Dashboard
[kpi](kpi/) | 17.0.1.2.0 |  | Key Performance Indicator
[report_async](report_async/) | 17.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Central place to run reports live or async
[report_csv](report_csv/) | 17.0.1.0.1 |  | Base module to create csv report
[report_layout_config](report_layout_config/) | 17.0.1.0.0 |  | Add possibility to easily modify the global report layout
[report_py3o](report_py3o/) | 17.0.1.0.0 |  | Reporting engine based on Libreoffice (ODT -> ODT, ODT -> PDF, ODT -> DOC, ODT -> DOCX, ODS -> ODS, etc.)
[report_qweb_element_page_visibility](report_qweb_element_page_visibility/) | 17.0.1.0.0 |  | Report Qweb Element Page Visibility
[report_qweb_field_option](report_qweb_field_option/) | 17.0.1.0.1 |  | Report Qweb Field Option
[report_qweb_parameter](report_qweb_parameter/) | 17.0.1.0.2 |  | Add new parameters for qweb templates in order to reduce field length and check minimal length
[report_qweb_pdf_watermark](report_qweb_pdf_watermark/) | 17.0.1.0.2 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Add watermarks to your QWEB PDF reports
[report_qweb_signer](report_qweb_signer/) | 17.0.1.0.3 |  | Sign Qweb PDFs usign a PKCS#12 certificate
[report_substitute](report_substitute/) | 17.0.1.1.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This module allows to create substitution rules for report actions.
[report_text_format_option](report_text_format_option/) | 17.0.1.0.0 |  | Report Text Format Option
[report_wkhtmltopdf_param](report_wkhtmltopdf_param/) | 17.0.1.0.0 |  | Add new parameters for a paper format to be used by wkhtmltopdf command as arguments.
[report_xlsx](report_xlsx/) | 17.0.1.0.2 |  | Base module to create xlsx report
[report_xlsx_helper](report_xlsx_helper/) | 17.0.1.0.1 |  | Report xlsx helpers
[report_xml](report_xml/) | 17.0.1.0.1 |  | Allow to generate XML reports
[sql_export](sql_export/) | 17.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Export data in csv file with SQL requests
[sql_export_excel](sql_export_excel/) | 17.0.1.0.0 |  | Allow to export a sql query to an excel file.
[sql_export_mail](sql_export_mail/) | 17.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Send csv file generated by sql query by mail.
[sql_request_abstract](sql_request_abstract/) | 17.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Abstract Model to manage SQL Requests

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/rest-framework&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/rest-framework/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/rest-framework/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/rest-framework/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/rest-framework/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/rest-framework/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/rest-framework)
[![Translation Status](https://translation.odoo-community.org/widgets/rest-framework-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/rest-framework-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Rest Frameworks

This repository has nice modules to interact with Odoo using JSON and HTTP requests.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[fastapi](fastapi/) | 17.0.3.2.1 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Odoo FastAPI endpoint
[fastapi_auth_api_key](fastapi_auth_api_key/) | 17.0.1.0.0 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Fastapi Auth API Key
[graphql_base](graphql_base/) | 17.0.1.1.0 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Base GraphQL/GraphiQL controller
[graphql_demo](graphql_demo/) | 17.0.1.0.1 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | GraphQL Demo
[pydantic](pydantic/) | 17.0.1.1.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Utility addon to ease mapping between Pydantic and Odoo models


Unported addons
---------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_rest](base_rest/) | 16.0.1.0.2 (unported) |  | Develop your own high level REST APIs for Odoo thanks to this addon.
[base_rest_auth_api_key](base_rest_auth_api_key/) | 16.0.1.0.0 (unported) | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Base Rest: Add support for the auth_api_key security policy into the openapi documentation
[base_rest_auth_jwt](base_rest_auth_jwt/) | 15.0.1.1.0 (unported) | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Base Rest: Add support for the auth_jwt security policy into the openapi documentation
[base_rest_auth_user_service](base_rest_auth_user_service/) | 15.0.1.0.1 (unported) |  | Login/logout from session using a REST call
[base_rest_datamodel](base_rest_datamodel/) | 16.0.1.0.0 (unported) |  | Datamodel binding for base_rest
[base_rest_demo](base_rest_demo/) | 16.0.2.0.2 (unported) | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Demo addon for Base REST
[base_rest_pydantic](base_rest_pydantic/) | 16.0.2.0.1 (unported) |  | Pydantic binding for base_rest
[datamodel](datamodel/) | 16.0.1.0.1 (unported) | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | This addon allows you to define simple data models supporting serialization/deserialization
[extendable](extendable/) | 16.0.1.0.1 (unported) | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Extendable classes registry loader for Odoo
[extendable_fastapi](extendable_fastapi/) | 16.0.2.1.1 (unported) | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Allows the use of extendable into fastapi apps
[fastapi_auth_jwt](fastapi_auth_jwt/) | 16.0.1.0.1 (unported) | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | JWT bearer token authentication for FastAPI.
[fastapi_auth_jwt_demo](fastapi_auth_jwt_demo/) | 16.0.2.0.0 (unported) | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Test/demo module for fastapi_auth_jwt.
[model_serializer](model_serializer/) | 15.0.1.2.0 (unported) | <a href='https://github.com/fdegrave'><img src='https://github.com/fdegrave.png' width='32' height='32' style='border-radius:50%;' alt='fdegrave'/></a> | Automatically translate Odoo models into Datamodels for (de)serialization
[rest_log](rest_log/) | 15.0.1.0.0 (unported) | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Track REST API calls into DB

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/rma&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/rma/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/rma/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/rma/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/rma/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/rma/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/rma)
[![Translation Status](https://translation.odoo-community.org/widgets/rma-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/rma-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# rma

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[product_warranty](product_warranty/) | 17.0.1.0.0 | <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Product Warranty
[rma](rma/) | 17.0.3.3.3 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Return Merchandise Authorization (RMA)
[rma_lot](rma_lot/) | 17.0.1.1.0 |  | Manage lot in RMA
[rma_repair](rma_repair/) | 17.0.1.0.2 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Create a repair order from rma
[rma_sale](rma_sale/) | 17.0.2.1.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Sale Order - Return Merchandise Authorization (RMA)

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sale-promotion&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/sale-promotion/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/sale-promotion/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/sale-promotion/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/sale-promotion/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/sale-promotion/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-promotion)
[![Translation Status](https://translation.odoo-community.org/widgets/sale-promotion-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sale-promotion-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Sales promotion management

Odoo addons for handling promotions on the sales funnel.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[coupon_chatter](coupon_chatter/) | 17.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Register messages and activities on the sale coupon records
[loyalty_card_fixed_expiration_date](loyalty_card_fixed_expiration_date/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> | Set a fixed expiration date for loyalty cards
[loyalty_incompatibility](loyalty_incompatibility/) | 17.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allows to set incompatibility rules between promotions
[loyalty_limit](loyalty_limit/) | 17.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Restrict number of promotions per customer or salesman
[loyalty_partner_applicability](loyalty_partner_applicability/) | 17.0.1.0.0 |  | Enables the definition of a customer filter for promotion rules that will only be applied to customers who meet the specified conditions in the filter.
[sale_loyalty_incompatibility](sale_loyalty_incompatibility/) | 17.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allows to set incompatibility rules between promotions in sale orders
[sale_loyalty_limit](sale_loyalty_limit/) | 17.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Restrict number of promotions per customer or salesman
[sale_loyalty_order_line_link](sale_loyalty_order_line_link/) | 17.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Adds a link between loyalty programs and their generated order linesfor easing tracking
[sale_loyalty_partner_applicability](sale_loyalty_partner_applicability/) | 17.0.1.0.0 |  | Enables the definition of a customer filter for promotion rules that will only be applied to customers who meet the specified conditions in the filter.

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sale-reporting&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/sale-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/sale-reporting/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/sale-reporting/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/sale-reporting/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/sale-reporting/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/sale-reporting-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sale-reporting-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# sale-reporting

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[sale_comment_template](sale_comment_template/) | 17.0.1.0.0 |  | Comments texts templates on Sale documents
[sale_layout_category_hide_detail](sale_layout_category_hide_detail/) | 17.0.1.1.0 |  | Hide details for sections in sale orders and invoices for reports and customer portal
[sale_order_line_position](sale_order_line_position/) | 17.0.1.0.0 |  | Adds position number on sale order line.
[sale_order_report_product_image](sale_order_report_product_image/) | 17.0.1.0.2 |  | Show product images on Sale documents
[sale_quotation_builder](sale_quotation_builder/) | 17.0.1.0.1 |  | Build great quotation templates
[sale_report_salesman](sale_report_salesman/) | 17.0.1.0.0 | <a href='https://github.com/carolina-fernandez'><img src='https://github.com/carolina-fernandez.png' width='32' height='32' style='border-radius:50%;' alt='carolina-fernandez'/></a> | Adds the Sales Reporting menu to the Salespersons user group.
[sale_report_salesperson_from_partner](sale_report_salesperson_from_partner/) | 17.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Sale Report Salesperson From Partner

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sale-workflow&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/sale-workflow/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/sale-workflow/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/sale-workflow/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/sale-workflow/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/sale-workflow/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-workflow)
[![Translation Status](https://translation.odoo-community.org/widgets/sale-workflow-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sale-workflow-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# sale-workflow

This project aim to deal with modules related to manage sale and their related workflow.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[partner_contact_sale_info_propagation](partner_contact_sale_info_propagation/) | 17.0.1.0.0 |  | Propagate Salesperson and Sales Teams from Company to Contacts
[partner_sale_pivot](partner_sale_pivot/) | 17.0.1.0.0 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | Sales analysis from customer form view
[portal_sale_personal_data_only](portal_sale_personal_data_only/) | 17.0.1.0.0 |  | Portal Sale Personal Data Only
[product_form_sale_link](product_form_sale_link/) | 17.0.1.0.0 |  | Adds a button on product forms to access Sale Lines
[product_supplierinfo_for_customer_sale](product_supplierinfo_for_customer_sale/) | 17.0.1.0.1 |  | Loads in every sale order line the customer code defined in the product
[sale_advance_payment](sale_advance_payment/) | 17.0.1.0.5 |  | Allow to add advance payments on sales and then use them on invoices
[sale_attached_product](sale_attached_product/) | 17.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Define products that will be added automatically when adding another in a sales order
[sale_automatic_workflow](sale_automatic_workflow/) | 17.0.1.2.1 |  | Sale Automatic Workflow
[sale_automatic_workflow_stock](sale_automatic_workflow_stock/) | 17.0.1.0.0 |  | Sale Automatic Workflow Stock
[sale_blanket_order](sale_blanket_order/) | 17.0.2.1.0 |  | Blanket Orders
[sale_block_no_stock](sale_block_no_stock/) | 17.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Block Sales if products has not enough Quantity based on a chosen field
[sale_cancel_reason](sale_cancel_reason/) | 17.0.1.0.0 |  | Sale Cancel Reason
[sale_commercial_partner](sale_commercial_partner/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add stored related field 'Commercial Entity' on sale orders
[sale_delivery_split_date](sale_delivery_split_date/) | 17.0.1.0.0 |  | Sale Deliveries split by date
[sale_delivery_state](sale_delivery_state/) | 17.0.2.0.0 |  | Show the delivery state on the sale order
[sale_discount_display_amount](sale_discount_display_amount/) | 17.0.1.1.2 |  | This addon intends to display the amount of the discount computed on sale_order_line and sale_order level
[sale_elaboration](sale_elaboration/) | 17.0.1.0.1 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Set an elaboration for any sale line
[sale_exception](sale_exception/) | 17.0.1.0.0 |  | Custom exceptions on sale order
[sale_exception_holidays_public](sale_exception_holidays_public/) | 17.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Raise a sale exception if there is a commitment_date on the SO and this date is a public holidays for the shipping partner address
[sale_fixed_discount](sale_fixed_discount/) | 17.0.2.1.1 |  | Allows to apply fixed amount discounts in sales orders.
[sale_force_invoiced](sale_force_invoiced/) | 17.0.1.1.1 |  | Allows to force the invoice status of the sales order to Invoiced
[sale_force_invoiced_quantity](sale_force_invoiced_quantity/) | 17.0.1.0.0 |  | Add manual invoice quantity in sales order lines
[sale_force_whole_invoiceability](sale_force_whole_invoiceability/) | 17.0.1.0.1 |  | Sale Force Whole Invoiceability
[sale_global_discount](sale_global_discount/) | 17.0.1.0.0 |  | Sale Global Discount
[sale_invoice_blocking](sale_invoice_blocking/) | 17.0.1.0.0 |  | Allow you to block the creation of invoices from a sale order.
[sale_invoice_frequency](sale_invoice_frequency/) | 17.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Define the invoice frequency for customers
[sale_invoice_plan](sale_invoice_plan/) | 17.0.1.0.1 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Add to sales order, ability to manage future invoice plan
[sale_invoice_policy](sale_invoice_policy/) | 17.0.1.0.0 |  | Sales Management: let the user choose the invoice policy on the order
[sale_manual_delivery](sale_manual_delivery/) | 17.0.1.0.0 |  | Create manually your deliveries
[sale_multi_template_application](sale_multi_template_application/) | 17.0.1.0.0 |  | Sale multi template application
[sale_order_archive](sale_order_archive/) | 17.0.1.0.0 |  | Archive Sale Orders
[sale_order_carrier_auto_assign](sale_order_carrier_auto_assign/) | 17.0.1.1.2 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Auto assign delivery carrier on sale order confirmation
[sale_order_general_discount](sale_order_general_discount/) | 17.0.1.0.0 |  | General discount per sale order
[sale_order_invoice_amount](sale_order_invoice_amount/) | 17.0.1.0.1 |  | Improves Sales Order invoiced/to invoice amount calculation based on product quantities when the company setting is enabled.
[sale_order_invoicing_finished_task](sale_order_invoicing_finished_task/) | 17.0.2.0.0 |  | Control invoice order lines if their related task has been set to invoiceable
[sale_order_line_cancel](sale_order_line_cancel/) | 17.0.1.0.0 |  | Sale cancel remaining
[sale_order_line_date](sale_order_line_date/) | 17.0.1.0.2 |  | Adds a commitment date to each sale order line.
[sale_order_line_description](sale_order_line_description/) | 17.0.1.0.0 |  | Sale order line description
[sale_order_line_input](sale_order_line_input/) | 17.0.1.0.0 |  | Search, create or modify directly sale order lines
[sale_order_line_menu](sale_order_line_menu/) | 17.0.1.0.0 |  | Adds a Sale Order Lines Menu
[sale_order_line_note](sale_order_line_note/) | 17.0.1.0.0 |  | Note on sale order line
[sale_order_line_price_history](sale_order_line_price_history/) | 17.0.1.1.1 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Sale order line price history
[sale_order_line_sequence](sale_order_line_sequence/) | 17.0.1.1.1 |  | Propagates SO line sequence to invoices and stock picking.
[sale_order_line_tag](sale_order_line_tag/) | 17.0.1.0.1 | <a href='https://github.com/smaciaosi'><img src='https://github.com/smaciaosi.png' width='32' height='32' style='border-radius:50%;' alt='smaciaosi'/></a> <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> <a href='https://github.com/ckolobow'><img src='https://github.com/ckolobow.png' width='32' height='32' style='border-radius:50%;' alt='ckolobow'/></a> | Add tags to classify sales order line reasons
[sale_order_lot_generator](sale_order_lot_generator/) | 17.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> <a href='https://github.com/mourad-ehm'><img src='https://github.com/mourad-ehm.png' width='32' height='32' style='border-radius:50%;' alt='mourad-ehm'/></a> <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Sale Order Lot Generator
[sale_order_lot_selection](sale_order_lot_selection/) | 17.0.1.0.0 | <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> | Sale Order Lot Selection
[sale_order_partner_no_autofollow](sale_order_partner_no_autofollow/) | 17.0.1.0.0 |  | Do not add customer as follower in Sales Orders
[sale_order_price_recalculation](sale_order_price_recalculation/) | 17.0.1.0.0 |  | Recalculate prices / Reset descriptions on sale order lines
[sale_order_priority](sale_order_priority/) | 17.0.1.0.1 |  | Define priority on sale orders
[sale_order_product_assortment](sale_order_product_assortment/) | 17.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Module that allows to use the assortments on sale orders
[sale_order_product_availability_inline](sale_order_product_availability_inline/) | 17.0.1.0.0 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | Show product availability in sales order line product drop-down.
[sale_order_product_recommendation](sale_order_product_recommendation/) | 17.0.1.1.1 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Recommend products to sell to customer based on history
[sale_order_qty_change_no_recompute](sale_order_qty_change_no_recompute/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Prevent recompute if only quantity has changed in sale order line
[sale_order_report_without_price](sale_order_report_without_price/) | 17.0.1.0.0 |  | Allow you to generate quotation and order reports without price.
[sale_order_revision](sale_order_revision/) | 17.0.1.0.0 |  | Keep track of revised quotations
[sale_order_secondary_unit](sale_order_secondary_unit/) | 17.0.1.0.6 |  | Sale product in a secondary unit
[sale_order_type](sale_order_type/) | 17.0.1.1.1 |  | Sale Order Type
[sale_order_type_confirm_message](sale_order_type_confirm_message/) | 17.0.1.0.0 |  | Confirmation requirement when validating sale
[sale_order_warn_message](sale_order_warn_message/) | 17.0.1.0.1 |  | Add a popup warning on sale to ensure warning is populated
[sale_packaging_default](sale_packaging_default/) | 17.0.1.0.0 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Simplify using products default packaging for sales
[sale_partner_address_restrict](sale_partner_address_restrict/) | 17.0.1.1.0 |  | Restrict addresses domain in the sales order form taking into account the partner selected
[sale_partner_incoterm](sale_partner_incoterm/) | 17.0.1.0.0 |  | Set the customer preferred incoterm on each sales order
[sale_partner_order_template](sale_partner_order_template/) | 17.0.1.0.0 |  | Order template in partner
[sale_partner_selectable_option](sale_partner_selectable_option/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Sale Partner Selectable Option
[sale_partner_utm_source](sale_partner_utm_source/) | 17.0.1.0.0 |  | This module adds the use of utm source in sales
[sale_payment_sheet](sale_payment_sheet/) | 17.0.1.0.1 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Allow to create invoice payments to commercial users without accounting permissions
[sale_pricelist_global_rule](sale_pricelist_global_rule/) | 17.0.1.0.2 |  | Apply a global rule to all sale order
[sale_procurement_group_by_line](sale_procurement_group_by_line/) | 17.0.1.0.2 |  | Base module for multiple procurement group by Sale order
[sale_product_configurator_widget_product_label](sale_product_configurator_widget_product_label/) | 17.0.1.0.0 | <a href='https://github.com/carlos-lopez-tecnativa'><img src='https://github.com/carlos-lopez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carlos-lopez-tecnativa'/></a> | Sale product configurator widget product label
[sale_product_multi_add](sale_product_multi_add/) | 17.0.1.0.1 |  | Sale Product Multi Add
[sale_product_set](sale_product_set/) | 17.0.1.0.0 |  | Sale product set
[sale_promotion_rule](sale_promotion_rule/) | 17.0.1.0.0 |  | Module to manage promotion rule on sale order
[sale_purchase_procurement_group_by_line](sale_purchase_procurement_group_by_line/) | 17.0.1.0.0 |  | Glue module between 'MTO Sale <-> Purchase' and 'Sale Procurement Group by Line'
[sale_quotation_number](sale_quotation_number/) | 17.0.1.1.2 |  | Different sequence for sale quotations
[sale_readonly_security](sale_readonly_security/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Sale Readonly Security
[sale_resource_booking](sale_resource_booking/) | 17.0.1.0.0 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Link resource bookings with sales
[sale_restricted_qty](sale_restricted_qty/) | 17.0.1.0.0 | <a href='https://github.com/ashishhirapara'><img src='https://github.com/ashishhirapara.png' width='32' height='32' style='border-radius:50%;' alt='ashishhirapara'/></a> | Sale order min quantity
[sale_shipping_info_helper](sale_shipping_info_helper/) | 17.0.1.0.0 |  | Add shipping amounts on sale order
[sale_sourced_by_line](sale_sourced_by_line/) | 17.0.1.0.2 |  | Multiple warehouse source locations for Sale order
[sale_start_end_dates](sale_start_end_dates/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adds start date and end date on sale order lines
[sale_stock_cancel_restriction](sale_stock_cancel_restriction/) | 17.0.1.0.0 |  | Sale Stock Cancel Restriction
[sale_stock_delivery_state](sale_stock_delivery_state/) | 17.0.1.0.0 |  | Change the way to compute the delivery state
[sale_stock_line_sequence](sale_stock_line_sequence/) | 17.0.1.0.0 |  | Glue Module for Sale Order Line Sequence and Stock Picking Line Sequence
[sale_stock_picking_blocking](sale_stock_picking_blocking/) | 17.0.1.1.1 |  | Allow you to block the creation of deliveries from a sale order.
[sale_stock_picking_note](sale_stock_picking_note/) | 17.0.1.0.0 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Add picking note in sale and purchase order
[sale_stock_secondary_unit](sale_stock_secondary_unit/) | 17.0.1.0.1 |  | Get product quantities in a secondary unit
[sale_substate](sale_substate/) | 17.0.1.0.1 |  | Sale Sub State
[sale_tier_validation](sale_tier_validation/) | 17.0.1.1.1 |  | Extends the functionality of Sale Orders to support a tier validation process.
[sale_validity_auto_cancel](sale_validity_auto_cancel/) | 17.0.1.0.0 | <a href='https://github.com/JordiMForgeFlow'><img src='https://github.com/JordiMForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiMForgeFlow'/></a> | Automatically cancel quotations after validity period.
[sales_team_invoiced_target_domain](sales_team_invoiced_target_domain/) | 17.0.1.0.0 |  | Sales Team Invoiced Target Domain
[sales_team_security](sales_team_security/) | 17.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | New group for seeing only sales channel's documents
[sales_team_security_crm](sales_team_security_crm/) | 17.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Integrates sales_team_security with crm
[sales_team_security_sale](sales_team_security_sale/) | 17.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Integrates sales_team_security with sale

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-auth&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/server-auth/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/server-auth/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/server-auth/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/server-auth/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/server-auth/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-auth)
[![Translation Status](https://translation.odoo-community.org/widgets/server-auth-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-auth-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Server Authentication

Modules for handling various authentication schemes

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[apikey_scope_editable](apikey_scope_editable/) | 17.0.1.0.0 |  | Set the API Key scope at creation
[auth_admin_passkey](auth_admin_passkey/) | 17.0.1.0.0 |  | Allows system administrator to authenticate with any account
[auth_admin_passkey_totp_mail_enforce](auth_admin_passkey_totp_mail_enforce/) | 17.0.1.0.0 |  | Disable 2FA if Passkey is being used
[auth_api_key](auth_api_key/) | 17.0.1.1.2 |  | Authenticate http requests from an API key
[auth_api_key_group](auth_api_key_group/) | 17.0.1.0.1 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Allow grouping API keys together. Grouping per se does nothing. This feature is supposed to be used by other modules to limit access to services or records based on groups of keys.
[auth_api_key_server_env](auth_api_key_server_env/) | 17.0.1.0.0 |  | Configure api keys via server env. This can be very useful to avoid mixing your keys between your various environments when restoring databases. All you have to do is to add a new section to your configuration file according to the following convention:
[auth_jwt](auth_jwt/) | 17.0.1.0.0 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | JWT bearer token authentication.
[auth_ldaps](auth_ldaps/) | 17.0.1.0.0 |  | Allows to use LDAP over SSL authentication
[auth_oauth_autologin](auth_oauth_autologin/) | 17.0.1.0.1 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Automatically redirect to the OAuth provider for login
[auth_oauth_multi_token](auth_oauth_multi_token/) | 17.0.1.1.1 |  | Allow multiple connection with the same OAuth account
[auth_oidc](auth_oidc/) | 17.0.1.2.0 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Allow users to login through OpenID Connect Provider
[auth_saml](auth_saml/) | 17.0.1.1.0 | <a href='https://github.com/vincent-hatakeyama'><img src='https://github.com/vincent-hatakeyama.png' width='32' height='32' style='border-radius:50%;' alt='vincent-hatakeyama'/></a> | SAML2 Authentication
[auth_session_timeout](auth_session_timeout/) | 17.0.1.0.1 |  | This module disable all inactive sessions since a given delay
[auth_signup_verify_email](auth_signup_verify_email/) | 17.0.1.0.0 |  | Force uninvited users to use a good email for signup
[auth_user_case_insensitive](auth_user_case_insensitive/) | 17.0.1.0.0 |  | Makes the user login field case insensitive
[impersonate_login](impersonate_login/) | 17.0.1.0.2 | <a href='https://github.com/Kev-Roche'><img src='https://github.com/Kev-Roche.png' width='32' height='32' style='border-radius:50%;' alt='Kev-Roche'/></a> | tools
[password_security](password_security/) | 17.0.2.0.0 |  | Allow admin to set password security requirements.
[user_log_view](user_log_view/) | 17.0.1.0.0 | <a href='https://github.com/trojikman'><img src='https://github.com/trojikman.png' width='32' height='32' style='border-radius:50%;' alt='trojikman'/></a> | Allow to see user's actions log
[users_ldap_groups](users_ldap_groups/) | 17.0.1.0.0 |  | Adds user accounts to groups based on rules defined by the administrator.
[users_ldap_mail](users_ldap_mail/) | 17.0.1.0.0 | <a href='https://github.com/joao-p-marques'><img src='https://github.com/joao-p-marques.png' width='32' height='32' style='border-radius:50%;' alt='joao-p-marques'/></a> | LDAP mapping for user name and e-mail
[users_ldap_populate](users_ldap_populate/) | 17.0.1.0.1 | <a href='https://github.com/joao-p-marques'><img src='https://github.com/joao-p-marques.png' width='32' height='32' style='border-radius:50%;' alt='joao-p-marques'/></a> | LDAP Populate

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-backend&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/server-backend/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/server-backend/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/server-backend/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/server-backend/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/server-backend/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-backend)
[![Translation Status](https://translation.odoo-community.org/widgets/server-backend-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-backend-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# server-backend

Mainly base modules used by others

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_external_dbsource](base_external_dbsource/) | 17.0.1.0.0 |  | External Database Sources
[base_external_dbsource_mysql](base_external_dbsource_mysql/) | 17.0.1.0.0 |  | External Database Source - MySQL
[base_external_dbsource_sqlite](base_external_dbsource_sqlite/) | 17.0.1.0.0 | <a href='https://github.com/anddago78'><img src='https://github.com/anddago78.png' width='32' height='32' style='border-radius:50%;' alt='anddago78'/></a> | External Database Source - SQLite
[base_global_discount](base_global_discount/) | 17.0.1.0.0 |  | Base Global Discount
[base_import_match](base_import_match/) | 17.0.1.0.0 |  | Try to avoid duplicates before importing
[base_user_role](base_user_role/) | 17.0.1.1.2 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> <a href='https://github.com/jcdrubay'><img src='https://github.com/jcdrubay.png' width='32' height='32' style='border-radius:50%;' alt='jcdrubay'/></a> <a href='https://github.com/novawish'><img src='https://github.com/novawish.png' width='32' height='32' style='border-radius:50%;' alt='novawish'/></a> | User roles
[base_user_role_company](base_user_role_company/) | 17.0.1.2.0 |  | User roles by company
[base_user_role_history](base_user_role_history/) | 17.0.1.0.0 | <a href='https://github.com/ThomasBinsfeld'><img src='https://github.com/ThomasBinsfeld.png' width='32' height='32' style='border-radius:50%;' alt='ThomasBinsfeld'/></a> | This module allows to track the changes on users roles.
[server_action_navigate](server_action_navigate/) | 17.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/ashishhirpara'><img src='https://github.com/ashishhirpara.png' width='32' height='32' style='border-radius:50%;' alt='ashishhirpara'/></a> | Navigate between any items of any Odoo Models

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-brand&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/server-brand/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/server-brand/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/server-brand/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/server-brand/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/server-brand/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-brand)
[![Translation Status](https://translation.odoo-community.org/widgets/server-brand-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-brand-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Tools for removing Odoo branding

Modules to help remove Odoo branding and advertising.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[disable_odoo_online](disable_odoo_online/) | 17.0.1.0.0 |  | Remove odoo.com Bindings
[hr_expense_remove_mobile_link](hr_expense_remove_mobile_link/) | 17.0.1.0.0 |  | Remove Odoo Enterprise mobile app download links
[portal_odoo_debranding](portal_odoo_debranding/) | 17.0.1.0.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Remove Odoo Branding from Website
[remove_odoo_enterprise](remove_odoo_enterprise/) | 17.0.1.0.1 |  | Remove enterprise modules and setting items

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-env&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/server-env/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/server-env/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/server-env/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/server-env/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/server-env/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-env)
[![Translation Status](https://translation.odoo-community.org/widgets/server-env-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-env-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# server-env

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[data_encryption](data_encryption/) | 17.0.1.0.0 |  | Store accounts and credentials encrypted by environment
[mail_environment](mail_environment/) | 17.0.1.0.1 |  | Configure mail servers with server_environment_files
[mail_environment_office365](mail_environment_office365/) | 17.0.1.0.0 |  | Configure Office365 parameters with environment variables via server_environment
[server_environment](server_environment/) | 17.0.1.2.1 |  | move some configurations out of the database
[server_environment_autocreate](server_environment_autocreate/) | 17.0.1.0.0 |  | Add ability to auto create records
[server_environment_data_encryption](server_environment_data_encryption/) | 17.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Server Environment Data Encryption
[server_environment_ir_config_parameter](server_environment_ir_config_parameter/) | 17.0.1.0.0 |  | Override System Parameters from server environment file

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-tools&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/server-tools/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/server-tools/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/server-tools/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/server-tools/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/server-tools/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-tools)
[![Translation Status](https://translation.odoo-community.org/widgets/server-tools-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-tools-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Server Tools

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[attachment_logging](attachment_logging/) | 17.0.1.0.0 |  | Show attachment information in chatter
[attachment_queue](attachment_queue/) | 17.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> | Base module adding the concept of queue for processing files
[auditlog](auditlog/) | 17.0.1.1.1 |  | Audit Log
[auto_backup](auto_backup/) | 17.0.1.1.1 |  | Backups database
[auto_backup_fs_file](auto_backup_fs_file/) | 17.0.1.0.0 |  | Store backups using some FSSPEC implementation
[base_cron_exclusion](base_cron_exclusion/) | 17.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | Allow you to select scheduled actions that should not run simultaneously.
[base_exception](base_exception/) | 17.0.1.1.0 | <a href='https://github.com/hparfr'><img src='https://github.com/hparfr.png' width='32' height='32' style='border-radius:50%;' alt='hparfr'/></a> <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> | This module provide an abstract model to manage customizable exceptions to be applied on different models (sale order, invoice, ...)
[base_fontawesome](base_fontawesome/) | 17.0.1.1.0 |  | Up to date Fontawesome resources.
[base_fontawesome_web_editor](base_fontawesome_web_editor/) | 17.0.1.0.1 |  | Integration between base_fontawesome and web_editor for FontAwesome >= 6.7.2 support.
[base_force_record_noupdate](base_force_record_noupdate/) | 17.0.1.0.0 |  | Manually force noupdate=True on models
[base_m2m_custom_field](base_m2m_custom_field/) | 17.0.1.0.0 |  | Customizations of Many2many
[base_model_restrict_update](base_model_restrict_update/) | 17.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Update Restrict Model
[base_name_search_improved](base_name_search_improved/) | 17.0.1.0.0 |  | Friendlier search when typing in relation fields
[base_partition](base_partition/) | 17.0.1.0.0 |  | Base module that provide the partition method on all models
[base_search_fuzzy](base_search_fuzzy/) | 17.0.1.0.0 |  | Fuzzy search with the PostgreSQL trigram extension
[base_sequence_option](base_sequence_option/) | 17.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Alternative sequence options for specific models
[base_sparse_field_list_support](base_sparse_field_list_support/) | 17.0.1.0.0 |  | add list support to convert_to_cache()
[base_technical_user](base_technical_user/) | 17.0.1.0.0 |  | Add a technical user parameter on the company
[base_view_inheritance_extension](base_view_inheritance_extension/) | 17.0.1.1.0 |  | Adds more operators for view inheritance
[base_write_diff](base_write_diff/) | 17.0.1.0.0 |  | Prevents updates on fields whose values won't change anyway
[bus_alt_connection](bus_alt_connection/) | 17.0.1.0.0 |  | Needed when using PgBouncer as a connection pooler
[database_cleanup](database_cleanup/) | 17.0.1.2.3 |  | Database cleanup
[dbfilter_from_header](dbfilter_from_header/) | 17.0.1.0.0 |  | Filter databases with HTTP headers
[fetchmail_attach_from_folder](fetchmail_attach_from_folder/) | 17.0.1.0.0 | <a href='https://github.com/NL66278'><img src='https://github.com/NL66278.png' width='32' height='32' style='border-radius:50%;' alt='NL66278'/></a> | Attach mails in an IMAP folder to existing objects
[fetchmail_notify_error_to_sender](fetchmail_notify_error_to_sender/) | 17.0.1.0.0 |  | If fetching mails gives error, send an email to sender
[fetchmail_notify_error_to_sender_test](fetchmail_notify_error_to_sender_test/) | 17.0.1.0.0 |  | Test for Fetchmail Notify Error to Sender
[html_text](html_text/) | 17.0.1.0.0 |  | Generate excerpts from any HTML field
[iap_alternative_provider](iap_alternative_provider/) | 17.0.1.0.0 | <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> | Base module for providing alternative provider for iap apps
[jsonifier](jsonifier/) | 17.0.1.0.0 |  | JSON-ify data for all models
[mail_template_attachment_per_lang](mail_template_attachment_per_lang/) | 17.0.1.0.0 |  | Set language specific attachments on mail templates.
[module_analysis](module_analysis/) | 17.0.1.0.3 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add analysis tools regarding installed modules to know which installed modules comes from Odoo Core, OCA, or are custom modules
[module_auto_update](module_auto_update/) | 17.0.1.0.0 |  | Automatically update Odoo modules
[module_change_auto_install](module_change_auto_install/) | 17.0.1.0.2 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Customize auto installables modules by configuration
[onchange_helper](onchange_helper/) | 17.0.1.0.2 |  | Technical module that ease execution of onchange in Python code
[rpc_helper](rpc_helper/) | 17.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Helpers for disabling RPC calls
[scheduler_error_mailer](scheduler_error_mailer/) | 17.0.1.0.0 |  | Scheduler Error Mailer
[sentry](sentry/) | 17.0.1.0.0 | <a href='https://github.com/barsi'><img src='https://github.com/barsi.png' width='32' height='32' style='border-radius:50%;' alt='barsi'/></a> <a href='https://github.com/naglis'><img src='https://github.com/naglis.png' width='32' height='32' style='border-radius:50%;' alt='naglis'/></a> <a href='https://github.com/versada'><img src='https://github.com/versada.png' width='32' height='32' style='border-radius:50%;' alt='versada'/></a> <a href='https://github.com/moylop260'><img src='https://github.com/moylop260.png' width='32' height='32' style='border-radius:50%;' alt='moylop260'/></a> <a href='https://github.com/fernandahf'><img src='https://github.com/fernandahf.png' width='32' height='32' style='border-radius:50%;' alt='fernandahf'/></a> | Report Odoo errors to Sentry
[sequence_python](sequence_python/) | 17.0.1.0.0 |  | Calculate a sequence number from a Python expression
[server_action_logging](server_action_logging/) | 17.0.1.0.0 |  | Module that provides a logging mechanism for server actions
[session_db](session_db/) | 17.0.1.0.1 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Store sessions in DB
[slow_statement_logger](slow_statement_logger/) | 17.0.1.0.0 |  | Log slow SQL statements
[test_auditlog](test_auditlog/) | 17.0.1.0.2 |  | Additional unit tests for Audit Log based on accounting models
[tracking_manager](tracking_manager/) | 17.0.1.1.0 | <a href='https://github.com/Kev-Roche'><img src='https://github.com/Kev-Roche.png' width='32' height='32' style='border-radius:50%;' alt='Kev-Roche'/></a> <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> | This module tracks all fields of a model, including one2many and many2many ones.
[tracking_manager_domain](tracking_manager_domain/) | 17.0.1.2.0 | <a href='https://github.com/CRogos'><img src='https://github.com/CRogos.png' width='32' height='32' style='border-radius:50%;' alt='CRogos'/></a> | This module extends the tracking manager to allow to define a domain on fields to track changes only when certain conditions apply.
[upgrade_analysis](upgrade_analysis/) | 17.0.1.0.5 | <a href='https://github.com/StefanRijnhart'><img src='https://github.com/StefanRijnhart.png' width='32' height='32' style='border-radius:50%;' alt='StefanRijnhart'/></a> <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Performs a difference analysis between modules installed on two different Odoo instances


Unported addons
---------------
addon | version | maintainers | summary
--- | --- | --- | ---
[views_migration_17](views_migration_17/) | 17.0.1.0.0 (unported) |  | Views Migration to v17

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-ux&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/server-ux/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/server-ux/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/server-ux/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/server-ux/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/server-ux/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-ux)
[![Translation Status](https://translation.odoo-community.org/widgets/server-ux-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-ux-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# server-ux

Server side features for usability and user experience related.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[announcement](announcement/) | 17.0.1.0.1 |  | Notify internal users about relevant organization stuff
[barcode_action](barcode_action/) | 17.0.1.0.1 |  | Allows to use barcodes as a launcher
[base_cancel_confirm](base_cancel_confirm/) | 17.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Base Cancel Confirm
[base_export_manager](base_export_manager/) | 17.0.1.0.1 |  | Manage model export profiles
[base_import_security_group](base_import_security_group/) | 17.0.1.0.0 |  | Group-based permissions for importing CSV files
[base_menu_visibility_restriction](base_menu_visibility_restriction/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Restrict (with groups) menu visibilty
[base_optional_quick_create](base_optional_quick_create/) | 17.0.1.0.0 |  | Avoid "quick create" on m2o fields, on a "by model" basis
[base_revision](base_revision/) | 17.0.1.0.0 |  | Keep track of revised document
[base_search_custom_field_filter](base_search_custom_field_filter/) | 17.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Add custom filters for fields via UI
[base_substate](base_substate/) | 17.0.1.0.1 |  | Base Sub State
[base_technical_features](base_technical_features/) | 17.0.1.0.2 |  | Access to technical features without activating debug mode
[base_tier_validation](base_tier_validation/) | 17.0.4.1.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Implement a validation process based on tiers.
[base_tier_validation_formula](base_tier_validation_formula/) | 17.0.1.0.0 |  | Formulas for Base tier validation
[base_tier_validation_forward](base_tier_validation_forward/) | 17.0.2.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Forward option for base tiers
[base_tier_validation_server_action](base_tier_validation_server_action/) | 17.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Add option to call server action when a tier is validated
[date_range](date_range/) | 17.0.1.2.1 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Manage all kind of date range
[date_range_account](date_range_account/) | 17.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add Date Range menu entry in Invoicing app
[document_quick_access](document_quick_access/) | 17.0.1.0.0 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Document quick access
[mail_message_destiny_link_template](mail_message_destiny_link_template/) | 17.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Mail template to show destiny records in chatter.
[mail_suggested_recipient_unchecked](mail_suggested_recipient_unchecked/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Mail suggested recipient unchecked
[multi_step_wizard](multi_step_wizard/) | 17.0.1.0.0 |  | Multi-Steps Wizards
[sequence_reset_period](sequence_reset_period/) | 17.0.1.0.0 |  | Auto-generate yearly/monthly/weekly/daily sequence period ranges
[server_action_mass_edit](server_action_mass_edit/) | 17.0.1.0.2 |  | Mass Editing

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/shift-planning&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/shift-planning/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/shift-planning/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/shift-planning/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/shift-planning/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/shift-planning/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/shift-planning)
[![Translation Status](https://translation.odoo-community.org/widgets/shift-planning-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/shift-planning-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# shift-planning

TODO: add repo description

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[hr_shift](hr_shift/) | 17.0.1.1.0 |  | Define shifts for employees
[hr_shift_holidays_public](hr_shift_holidays_public/) | 17.0.1.0.0 |  | Avoid planning shifts on holidays

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sign&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/sign/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/sign/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/sign/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/sign/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/sign/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/sign)
[![Translation Status](https://translation.odoo-community.org/widgets/sign-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sign-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Odoo modules for signing purposes

Here are OCA modules that have digital signature functionalities.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[agreement_sign_oca](agreement_sign_oca/) | 17.0.1.1.0 | <a href='https://github.com/miquelalzanillas'><img src='https://github.com/miquelalzanillas.png' width='32' height='32' style='border-radius:50%;' alt='miquelalzanillas'/></a> | Agreement Sign Oca
[maintenance_sign_oca](maintenance_sign_oca/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Sign Oca
[project_task_sign_oca](project_task_sign_oca/) | 17.0.1.0.0 | <a href='https://github.com/WesleyOliveira98'><img src='https://github.com/WesleyOliveira98.png' width='32' height='32' style='border-radius:50%;' alt='WesleyOliveira98'/></a> | Project Task Sign Oca
[sign_oca](sign_oca/) | 17.0.1.2.2 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Allow to sign documents inside Odoo CE

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/social&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/social/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/social/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/social/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/social/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/social/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/social)
[![Translation Status](https://translation.odoo-community.org/widgets/social-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/social-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# social

{'TODO': 'add repo description.'}

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_search_mail_content](base_search_mail_content/) | 17.0.1.1.0 |  | Base Search Mail Content
[base_user_signature](base_user_signature/) | 17.0.1.0.0 | <a href='https://github.com/imlopes'><img src='https://github.com/imlopes.png' width='32' height='32' style='border-radius:50%;' alt='imlopes'/></a> | Base User Signature
[mail_activity_board](mail_activity_board/) | 17.0.1.1.1 |  | Add Activity Boards
[mail_activity_cancel_tracking](mail_activity_cancel_tracking/) | 17.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Mail Activity Cancel Tracking
[mail_activity_done](mail_activity_done/) | 17.0.1.0.0 |  | Mail Activity Done
[mail_activity_reminder](mail_activity_reminder/) | 17.0.1.0.1 |  | Reminder notifications about planned activities
[mail_activity_team](mail_activity_team/) | 17.0.2.0.2 |  | Add Teams to Activities
[mail_attach_existing_attachment](mail_attach_existing_attachment/) | 17.0.1.0.1 |  | Adding attachment on the object by sending this one
[mail_attach_existing_attachment_account](mail_attach_existing_attachment_account/) | 17.0.1.0.0 |  | Module to use attach existing attachment for account module
[mail_autogenerated_header](mail_autogenerated_header/) | 17.0.1.1.0 |  | Add headers to Odoo's mails indicating they are autogenerated
[mail_autosubscribe](mail_autosubscribe/) | 17.0.1.0.0 |  | Automatically subscribe partners to its company's business documents
[mail_composer_cc_bcc](mail_composer_cc_bcc/) | 17.0.1.0.1 | <a href='https://github.com/trisdoan'><img src='https://github.com/trisdoan.png' width='32' height='32' style='border-radius:50%;' alt='trisdoan'/></a> | This module enables sending mail to CC and BCC partners in mail composer form.
[mail_composer_cc_bcc_account](mail_composer_cc_bcc_account/) | 17.0.1.0.1 | <a href='https://github.com/hailangvn2023'><img src='https://github.com/hailangvn2023.png' width='32' height='32' style='border-radius:50%;' alt='hailangvn2023'/></a> | This module enables sending mail to CC and BCC partners for invoices.
[mail_debrand](mail_debrand/) | 17.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/joao-p-marques'><img src='https://github.com/joao-p-marques.png' width='32' height='32' style='border-radius:50%;' alt='joao-p-marques'/></a> | Remove Odoo branding in sent emails Removes anchor <a href odoo.com togheder with it's parent ( for powerd by) form all the templates removes any 'odoo' that are in tempalte texts > 20characters
[mail_disable_follower_notification](mail_disable_follower_notification/) | 17.0.1.0.0 |  | Don't send emails by default when adding followers to records
[mail_discuss_channel_unread_sort](mail_discuss_channel_unread_sort/) | 17.0.1.0.0 |  | Sort discuss channels by most recent unread activity
[mail_forward](mail_forward/) | 17.0.2.0.1 | <a href='https://github.com/carlos-lopez-tecnativa'><img src='https://github.com/carlos-lopez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carlos-lopez-tecnativa'/></a> | Forward messages from the chatter of any document to other users.
[mail_gateway](mail_gateway/) | 17.0.1.0.10 |  | Base module for gateway communications
[mail_gateway_whatsapp](mail_gateway_whatsapp/) | 17.0.1.1.3 |  | Set a gateway for whatsapp
[mail_history_mark_unread](mail_history_mark_unread/) | 17.0.1.1.0 |  | Add 'Mark as Unread' action to messages in History mailbox and Search results
[mail_layout_force](mail_layout_force/) | 17.0.1.0.1 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Force a mail layout on selected email templates
[mail_layout_preview](mail_layout_preview/) | 17.0.1.0.0 |  | Preview email templates in the browser
[mail_no_user_assign_notification](mail_no_user_assign_notification/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Mail No user Assign Notification
[mail_notification_custom_subject](mail_notification_custom_subject/) | 17.0.1.2.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Apply a custom subject to mail notifications
[mail_optional_autofollow](mail_optional_autofollow/) | 17.0.1.0.0 |  | Choose if you want to automatically add new recipients as followers on mail.compose.message
[mail_optional_follower_notification](mail_optional_follower_notification/) | 17.0.1.1.0 |  | Choose to notify followers on mail.compose.message
[mail_outbound_static](mail_outbound_static/) | 17.0.1.0.1 |  | Allows you to configure the from header for a mail server.
[mail_partner_forwarding](mail_partner_forwarding/) | 17.0.1.0.1 |  | Forwarding notifications for partners
[mail_partner_opt_out](mail_partner_opt_out/) | 17.0.1.0.0 |  | Add the partner's email to the blackmailed list
[mail_print](mail_print/) | 17.0.1.0.0 |  | Print messages from the chatter of any document.
[mail_quoted_reply](mail_quoted_reply/) | 17.0.1.0.0 |  | Make a reply using a message
[mail_restrict_follower_selection](mail_restrict_follower_selection/) | 17.0.1.0.0 |  | Define a domain from which followers can be selected
[mail_send_confirmation](mail_send_confirmation/) | 17.0.1.0.1 |  | Mail Send Confirmation
[mail_server_by_user](mail_server_by_user/) | 17.0.1.0.0 | <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | Email Server By User
[mail_show_follower](mail_show_follower/) | 17.0.1.0.2 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Show CC document followers in mails.
[mail_template_substitute](mail_template_substitute/) | 17.0.1.0.0 |  | This module allows to create substitution rules for mail templates.
[mail_tracking](mail_tracking/) | 17.0.1.0.5 |  | Email tracking system for all mails sent
[mail_tracking_mailgun](mail_tracking_mailgun/) | 17.0.1.0.1 |  | Mail tracking and Mailgun webhooks integration
[mail_tracking_mass_mailing](mail_tracking_mass_mailing/) | 17.0.1.0.0 |  | Improve mass mailing email tracking
[mass_mailing_custom_unsubscribe](mass_mailing_custom_unsubscribe/) | 17.0.1.0.1 |  | Track metadata for GDPR compliance
[mass_mailing_event_registration_exclude](mass_mailing_event_registration_exclude/) | 17.0.1.0.0 |  | Link mass mailing with event for excluding recipients
[mass_mailing_list_dynamic](mass_mailing_list_dynamic/) | 17.0.1.0.2 |  | Mass mailing lists that get autopopulated
[mass_mailing_partner](mass_mailing_partner/) | 17.0.1.1.0 |  | Link partners with mass-mailing
[mass_mailing_resend](mass_mailing_resend/) | 17.0.1.1.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Resend mass mailings
[mute_notification_user_autosubscribe](mute_notification_user_autosubscribe/) | 17.0.1.0.0 |  | Do not send notifications to users autosubcribed through user_id field
[outgoing_email_by_model](outgoing_email_by_model/) | 17.0.1.0.0 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Outgoing Email by Model

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/spreadsheet&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/spreadsheet/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/spreadsheet/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/spreadsheet/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/spreadsheet/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/spreadsheet/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/spreadsheet)
[![Translation Status](https://translation.odoo-community.org/widgets/spreadsheet-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/spreadsheet-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Spreadsheet modules for Odoo

Modules that expand the Odoo spreadsheets features.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[spreadsheet_dashboard_oca](spreadsheet_dashboard_oca/) | 17.0.1.0.0 |  | Use OCA Spreadsheets on dashboards configuration
[spreadsheet_oca](spreadsheet_oca/) | 17.0.1.0.6 |  | Allow to edit spreadsheets

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-availability&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-availability/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-logistics-availability/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/stock-logistics-availability/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-logistics-availability/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-availability/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-availability)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-availability-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-availability-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Stock Availability modules

 This repository contains modules to provide more information about product stock availability in terms of quantities

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[sale_stock_available_info_popup](sale_stock_available_info_popup/) | 17.0.1.0.0 |  | Adds an 'Available to promise' quantity to the popover shown in sale order line that display stock info of the product
[stock_available](stock_available/) | 17.0.1.0.0 |  | Stock available to promise
[stock_available_base_exclude_location](stock_available_base_exclude_location/) | 17.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Base module to exclude locations for product available quantities
[stock_available_immediately](stock_available_immediately/) | 17.0.1.0.0 |  | Ignore planned receptions in quantity available to promise
[stock_available_mrp](stock_available_mrp/) | 17.0.1.1.0 |  | Consider the production potential is available to promise
[stock_free_quantity](stock_free_quantity/) | 17.0.1.1.0 |  | Stock Free Quantity
[stock_quant_available_quantity](stock_quant_available_quantity/) | 17.0.1.0.0 | <a href='https://github.com/tisho99'><img src='https://github.com/tisho99.png' width='32' height='32' style='border-radius:50%;' alt='tisho99'/></a> | Shows Available Quantity in the stock quant views

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-barcode&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-barcode/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-logistics-barcode/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/stock-logistics-barcode/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-logistics-barcode/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-barcode/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-barcode)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-barcode-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-barcode-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# stock-logistics-barcode

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[barcodes_generator_abstract](barcodes_generator_abstract/) | 17.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Generate Barcodes for Any Models
[barcodes_generator_location](barcodes_generator_location/) | 17.0.1.0.1 |  | Generate Barcodes for Stock Locations
[barcodes_generator_product](barcodes_generator_product/) | 17.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Generate Barcodes for Products (Templates and Variants)
[product_multi_barcode](product_multi_barcode/) | 17.0.1.0.1 |  | Multiple barcodes on products
[stock_picking_product_barcode_report](stock_picking_product_barcode_report/) | 17.0.1.0.1 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | It provides a wizard to select how many barcodes print.

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-orderpoint&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-orderpoint/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-logistics-orderpoint/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/stock-logistics-orderpoint/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-logistics-orderpoint/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-orderpoint/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-orderpoint)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-orderpoint-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-orderpoint-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Stock Logistics Orderpoint

This repository contains modules to extend reordering rules (available on warehouses locations) functionalities.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[stock_orderpoint_generator](stock_orderpoint_generator/) | 17.0.1.0.0 |  | Mass configuration of stock order points

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-reporting&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-logistics-reporting/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/stock-logistics-reporting/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-logistics-reporting/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-reporting/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-reporting-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-reporting-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# stock-logistics-reporting

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[delivery_line_sale_line_position](delivery_line_sale_line_position/) | 17.0.1.0.0 |  | Adds the sale line position to the delivery report lines
[stock_move_pivot_total_price](stock_move_pivot_total_price/) | 17.0.1.0.0 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> | Adds a total price UOM to the stock move pivot view
[stock_move_value_report](stock_move_value_report/) | 17.0.1.0.1 |  | Stock Move Cost Value Report
[stock_picking_comment_template](stock_picking_comment_template/) | 17.0.1.0.0 |  | Comments texts templates on Picking documents
[stock_picking_operations_multilang](stock_picking_operations_multilang/) | 17.0.1.0.0 |  | Stock Picking Operations Multilang
[stock_picking_report_custom_description](stock_picking_report_custom_description/) | 17.0.1.1.1 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> | Show moves description in picking reports
[stock_picking_report_delivery_driver](stock_picking_report_delivery_driver/) | 17.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Delivery Driver info in Stock Picking reports
[stock_picking_report_external_note](stock_picking_report_external_note/) | 17.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Adds a note in Stock Picking shown on external reports like Delivery Slip
[stock_picking_report_valued](stock_picking_report_valued/) | 17.0.1.2.0 |  | Adding Valued Picking on Delivery Slip report
[stock_quant_history](stock_quant_history/) | 17.0.1.0.0 | <a href='https://github.com/petrus-v'><img src='https://github.com/petrus-v.png' width='32' height='32' style='border-radius:50%;' alt='petrus-v'/></a> | Re-generate stock quants for given date
[stock_quant_history_queued](stock_quant_history_queued/) | 17.0.1.0.0 | <a href='https://github.com/petrus-v'><img src='https://github.com/petrus-v.png' width='32' height='32' style='border-radius:50%;' alt='petrus-v'/></a> | Use Queue jop to generate stock quants snapshots
[stock_quantity_history_location](stock_quantity_history_location/) | 17.0.1.0.0 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> <a href='https://github.com/rolandojduartem'><img src='https://github.com/rolandojduartem.png' width='32' height='32' style='border-radius:50%;' alt='rolandojduartem'/></a> | Provides stock quantity by location on past date

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-request&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-request/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-logistics-request/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/stock-logistics-request/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-logistics-request/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-request/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-request)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-request-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-request-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Stock Logistics Request

This repository contains modules to provide another way of creating stock movements. Provided as a dedicated application, users will be able to create their stock needs by product and location.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[stock_request](stock_request/) | 17.0.1.1.6 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Internal request for stock
[stock_request_analytic](stock_request_analytic/) | 17.0.1.0.0 |  | Internal request for stock
[stock_request_direction](stock_request_direction/) | 17.0.1.1.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | From or to your warehouse?
[stock_request_kanban](stock_request_kanban/) | 17.0.1.0.2 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Adds a stock request order, and takes stock requests as lines
[stock_request_mrp](stock_request_mrp/) | 17.0.1.0.1 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Manufacturing request for stock
[stock_request_picking_type](stock_request_picking_type/) | 17.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Add Stock Requests to the Inventory App
[stock_request_purchase](stock_request_purchase/) | 17.0.1.0.3 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Internal request for stock
[stock_request_stage](stock_request_stage/) | 17.0.1.0.0 |  | Adds the possibility to manage stock requests by stages
[stock_request_submit](stock_request_submit/) | 17.0.1.0.0 |  | Add submit state on Stock Requests

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-transport&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-transport/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-logistics-transport/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/stock-logistics-transport/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-logistics-transport/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-transport/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-transport)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-transport-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-transport-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# stock-logistics-transport

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[stock_depot](stock_depot/) | 17.0.1.0.0 |  | This module allows users to manage partners stock depots.
[stock_dock](stock_dock/) | 17.0.1.0.0 |  | Manage the loading docks of your warehouse.
[stock_location_address](stock_location_address/) | 17.0.1.0.0 |  | Adds an address on locations
[stock_location_address_purchase](stock_location_address_purchase/) | 17.0.1.0.0 |  | Uses the location address on purchases
[tms](tms/) | 17.0.1.1.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/santiagordz'><img src='https://github.com/santiagordz.png' width='32' height='32' style='border-radius:50%;' alt='santiagordz'/></a> <a href='https://github.com/EdgarRetes'><img src='https://github.com/EdgarRetes.png' width='32' height='32' style='border-radius:50%;' alt='EdgarRetes'/></a> | Manage Vehicles, Drivers, Routes and Trips
[tms_account](tms_account/) | 17.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/santiagordz'><img src='https://github.com/santiagordz.png' width='32' height='32' style='border-radius:50%;' alt='santiagordz'/></a> <a href='https://github.com/EdgarRetes'><img src='https://github.com/EdgarRetes.png' width='32' height='32' style='border-radius:50%;' alt='EdgarRetes'/></a> | Track invoices linked to TMS orders
[tms_account_asset](tms_account_asset/) | 17.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/santiagordz'><img src='https://github.com/santiagordz.png' width='32' height='32' style='border-radius:50%;' alt='santiagordz'/></a> <a href='https://github.com/EdgarRetes'><img src='https://github.com/EdgarRetes.png' width='32' height='32' style='border-radius:50%;' alt='EdgarRetes'/></a> | Manage TMS assets
[tms_expense](tms_expense/) | 17.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/santiagordz'><img src='https://github.com/santiagordz.png' width='32' height='32' style='border-radius:50%;' alt='santiagordz'/></a> <a href='https://github.com/EdgarRetes'><img src='https://github.com/EdgarRetes.png' width='32' height='32' style='border-radius:50%;' alt='EdgarRetes'/></a> | Manage expenses of a trip: hotel, tolls, fuel
[tms_product](tms_product/) | 17.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/santiagordz'><img src='https://github.com/santiagordz.png' width='32' height='32' style='border-radius:50%;' alt='santiagordz'/></a> <a href='https://github.com/EdgarRetes'><img src='https://github.com/EdgarRetes.png' width='32' height='32' style='border-radius:50%;' alt='EdgarRetes'/></a> | Manage Vehicles as Products
[tms_purchase](tms_purchase/) | 17.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/santiagordz'><img src='https://github.com/santiagordz.png' width='32' height='32' style='border-radius:50%;' alt='santiagordz'/></a> <a href='https://github.com/EdgarRetes'><img src='https://github.com/EdgarRetes.png' width='32' height='32' style='border-radius:50%;' alt='EdgarRetes'/></a> | Manage purchase requests to drivers and other suppliers
[tms_sale](tms_sale/) | 17.0.1.0.1 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/santiagordz'><img src='https://github.com/santiagordz.png' width='32' height='32' style='border-radius:50%;' alt='santiagordz'/></a> <a href='https://github.com/EdgarRetes'><img src='https://github.com/EdgarRetes.png' width='32' height='32' style='border-radius:50%;' alt='EdgarRetes'/></a> | Sell transportation management system.

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-warehouse&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-warehouse/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-logistics-warehouse/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/stock-logistics-warehouse/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-logistics-warehouse/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-warehouse/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-warehouse)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-warehouse-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-warehouse-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# stock-logistics-warehouse

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_move_line_product](account_move_line_product/) | 17.0.1.0.0 |  | Displays the product in the journal entries and items
[account_move_line_stock_info](account_move_line_stock_info/) | 17.0.1.0.0 |  | Account Move Line Stock Info
[base_product_merge](base_product_merge/) | 17.0.1.0.0 | <a href='https://github.com/JasminSForgeFlow'><img src='https://github.com/JasminSForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JasminSForgeFlow'/></a> | Merge duplicate products
[procurement_auto_create_group](procurement_auto_create_group/) | 17.0.1.0.0 |  | Allows to configure the system to propose automatically new procurement groups during the procurement run.
[product_route_profile](product_route_profile/) | 17.0.1.0.0 | <a href='https://github.com/Kev-Roche'><img src='https://github.com/Kev-Roche.png' width='32' height='32' style='border-radius:50%;' alt='Kev-Roche'/></a> | Add Route profile concept on product
[scrap_reason_code](scrap_reason_code/) | 17.0.1.0.1 | <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> | Reason code for scrapping
[stock_account_change_qty_reason](stock_account_change_qty_reason/) | 17.0.1.0.0 |  | Stock Account Change Quantity Reason
[stock_archive_constraint](stock_archive_constraint/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Stock archive constraint
[stock_change_qty_reason](stock_change_qty_reason/) | 17.0.1.0.0 |  | Stock Quantity Change Reason
[stock_demand_estimate](stock_demand_estimate/) | 17.0.1.1.1 |  | Allows to create demand estimates.
[stock_demand_estimate_matrix](stock_demand_estimate_matrix/) | 17.0.1.0.0 |  | Allows to create demand estimates.
[stock_exception](stock_exception/) | 17.0.1.0.0 |  | Custom exceptions on stock picking
[stock_helper](stock_helper/) | 17.0.1.1.1 |  | Add methods shared between various stock modules
[stock_inventory](stock_inventory/) | 17.0.1.3.0 |  | Allows to do an easier follow up of the Inventory Adjustments
[stock_inventory_discrepancy](stock_inventory_discrepancy/) | 17.0.1.1.0 |  | Adds the capability to show the discrepancy of every line in an inventory and to block the inventory validation when the discrepancy is over a user defined threshold.
[stock_inventory_preparation_filter](stock_inventory_preparation_filter/) | 17.0.1.0.0 |  | More filters for inventory adjustments
[stock_location_lockdown](stock_location_lockdown/) | 17.0.1.0.0 |  | Prevent to add stock on locked locations
[stock_location_position](stock_location_position/) | 17.0.1.0.0 |  | Add coordinate attributes on stock location.
[stock_location_zone](stock_location_zone/) | 17.0.1.0.0 |  | Classify locations with zones.
[stock_move_location](stock_move_location/) | 17.0.1.0.0 |  | This module allows to move all stock in a stock location to an other one.
[stock_mts_mto_rule](stock_mts_mto_rule/) | 17.0.1.0.1 |  | Add a MTS+MTO route
[stock_packaging_calculator](stock_packaging_calculator/) | 17.0.1.1.0 |  | Compute product quantity to pick by packaging
[stock_picking_procure_method](stock_picking_procure_method/) | 17.0.1.0.0 |  | Allows to force the procurement method from the picking
[stock_picking_show_linked](stock_picking_show_linked/) | 17.0.1.0.0 |  | This addon allows to easily access related pickings (in the case of chained routes) through a button in the parent picking view.
[stock_picking_volume](stock_picking_volume/) | 17.0.1.1.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Compute volume information on stock moves and pickings
[stock_picking_volume_packaging](stock_picking_volume_packaging/) | 17.0.1.0.0 |  | Use volume information on potential product packaging to compute the volume of a stock.move
[stock_putaway_product_template](stock_putaway_product_template/) | 17.0.1.0.0 | <a href='https://github.com/kevinkhao'><img src='https://github.com/kevinkhao.png' width='32' height='32' style='border-radius:50%;' alt='kevinkhao'/></a> <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> | Add product template in putaway strategies from the product view
[stock_quant_manual_assign](stock_quant_manual_assign/) | 17.0.1.1.0 |  | Stock - Manual Quant Assignment
[stock_quant_reservation_info](stock_quant_reservation_info/) | 17.0.1.0.1 |  | Allows to see the reserved info of Products
[stock_quant_reservation_info_mrp](stock_quant_reservation_info_mrp/) | 17.0.1.0.0 |  | Allows to see the manufacturing order related to the reserved info of Products
[stock_removal_location_by_priority](stock_removal_location_by_priority/) | 17.0.1.0.0 |  | Establish a removal priority on stock locations.
[stock_reserve](stock_reserve/) | 17.0.1.0.0 |  | Stock reservations on products
[stock_reserve_sale](stock_reserve_sale/) | 17.0.1.0.0 |  | Stock Reserve Sales
[stock_route_mto](stock_route_mto/) | 17.0.1.0.0 |  | Allows to identify MTO routes through a checkbox and availability to filter them.
[stock_search_supplierinfo_code](stock_search_supplierinfo_code/) | 17.0.1.0.0 |  | Allows to search for picking from supplierinfo code
[stock_secondary_unit](stock_secondary_unit/) | 17.0.1.2.0 |  | Get product quantities in a secondary unit
[stock_warehouse_calendar](stock_warehouse_calendar/) | 17.0.1.0.1 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> | Adds a calendar to the Warehouse

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-workflow&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-workflow/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-logistics-workflow/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/stock-logistics-workflow/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-logistics-workflow/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-workflow/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-workflow)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-workflow-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-workflow-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# stock-logistics-workflow

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[delivery_procurement_group_carrier](delivery_procurement_group_carrier/) | 17.0.1.1.1 |  | Delivery Procurement Group Carrier
[product_cost_price_avco_sync](product_cost_price_avco_sync/) | 17.0.1.0.0 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Set product cost price from updated moves
[purchase_stock_picking_invoice_link](purchase_stock_picking_invoice_link/) | 17.0.1.0.0 |  | Adds link between purchases, pickings and invoices
[sale_order_global_stock_route](sale_order_global_stock_route/) | 17.0.1.0.0 |  | Add the possibility to choose one warehouse path for an order
[sale_planned_consumed_date](sale_planned_consumed_date/) | 17.0.1.0.0 |  | Sale planned consumed date
[sale_stock_restocking_fee_invoicing](sale_stock_restocking_fee_invoicing/) | 17.0.1.0.0 |  | On demand charge restocking fee for accepting returned goods .
[stock_account_product_run_fifo_hook](stock_account_product_run_fifo_hook/) | 17.0.1.0.1 |  | Add more flexibility in the run fifo method.
[stock_account_show_automatic_valuation](stock_account_show_automatic_valuation/) | 17.0.1.0.0 |  | Allow automatic valuation for stock moves in community edition
[stock_auto_move](stock_auto_move/) | 17.0.1.0.0 |  | Automatic Move Processing
[stock_landed_costs_priority](stock_landed_costs_priority/) | 17.0.1.0.0 |  | Add priority to landed costs
[stock_lock_lot](stock_lock_lot/) | 17.0.1.0.0 |  | Stock Lock Lot
[stock_lot_on_hand_first](stock_lot_on_hand_first/) | 17.0.1.0.0 | <a href='https://github.com/grindtildeath'><img src='https://github.com/grindtildeath.png' width='32' height='32' style='border-radius:50%;' alt='grindtildeath'/></a> | Allows to display lots on hand first in M2o fields
[stock_lot_production_date](stock_lot_production_date/) | 17.0.1.0.0 | <a href='https://github.com/atchuthan'><img src='https://github.com/atchuthan.png' width='32' height='32' style='border-radius:50%;' alt='atchuthan'/></a> | Stock Lot Production Date
[stock_lot_scrap](stock_lot_scrap/) | 17.0.1.0.0 |  | This module adds a button in Production Lot/Serial Number view form to Scrap all products contained.
[stock_move_backdating](stock_move_backdating/) | 17.0.1.0.0 |  | Stock Move Backdating
[stock_move_forced_lot](stock_move_forced_lot/) | 17.0.1.0.0 |  | This module allows you to set a lot_id in a procurement to force the stock move generated to only reserve the selected lot.
[stock_move_line_qty_picked](stock_move_line_qty_picked/) | 17.0.1.0.0 | <a href='https://github.com/grindtildeath'><img src='https://github.com/grindtildeath.png' width='32' height='32' style='border-radius:50%;' alt='grindtildeath'/></a> | Separate quantity picked from the reserved quantity
[stock_move_line_reference_link](stock_move_line_reference_link/) | 17.0.1.0.0 |  | Add link in stock move line references.
[stock_move_planned_consumed_date](stock_move_planned_consumed_date/) | 17.0.1.0.0 |  | Stock Move planned consumed date
[stock_move_propagate_first_move](stock_move_propagate_first_move/) | 17.0.1.0.0 |  | This addon propagate the picking type of the original move to all next moves created from procurement
[stock_move_quantity_product_uom](stock_move_quantity_product_uom/) | 17.0.1.0.0 |  | computes stock.move's quantity in the uom of the product.
[stock_no_negative](stock_no_negative/) | 17.0.1.0.0 |  | Disallow negative stock levels by default
[stock_picking_auto_create_lot](stock_picking_auto_create_lot/) | 17.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Auto create lots for incoming pickings
[stock_picking_auto_create_lot_sequence](stock_picking_auto_create_lot_sequence/) | 17.0.1.0.0 |  | Stock Picking Auto Create Lot Sequence
[stock_picking_back2draft](stock_picking_back2draft/) | 17.0.1.0.0 |  | Reopen cancelled pickings
[stock_picking_batch_print_pickings](stock_picking_batch_print_pickings/) | 17.0.1.0.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Print Picking from Stock Picking Batch
[stock_picking_carrier](stock_picking_carrier/) | 17.0.1.0.0 |  | Stock Picking Carrier
[stock_picking_filter_lot](stock_picking_filter_lot/) | 17.0.1.0.0 |  | In picking out lots' selection, filter lots based on their location
[stock_picking_group_by_base](stock_picking_group_by_base/) | 17.0.1.0.1 |  | Allows to define a way to create index on extensible domain
[stock_picking_group_by_partner_by_carrier](stock_picking_group_by_partner_by_carrier/) | 17.0.0.0.0 |  | Stock Picking: group by partner and carrier
[stock_picking_import_serial_number](stock_picking_import_serial_number/) | 17.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Import S/N from excel file for incoming pickings
[stock_picking_invoice_link](stock_picking_invoice_link/) | 17.0.1.2.5 |  | Adds link between pickings and invoices
[stock_picking_kind](stock_picking_kind/) | 17.0.1.0.0 |  | Computes the kind of picking based on locations
[stock_picking_line_sequence](stock_picking_line_sequence/) | 17.0.1.0.1 |  | Manages the order of stock moves by displaying its sequence
[stock_picking_mass_action](stock_picking_mass_action/) | 17.0.1.0.0 |  | Stock Picking Mass Action
[stock_picking_origin_reference](stock_picking_origin_reference/) | 17.0.1.0.0 |  | Add clickable button to the Transfer Source Document.
[stock_picking_origin_reference_purchase](stock_picking_origin_reference_purchase/) | 17.0.1.0.0 |  | Transfer to Purchase Order navigation from the Source Document.
[stock_picking_origin_reference_sale](stock_picking_origin_reference_sale/) | 17.0.1.0.0 |  | Transfer to Sales Order navigation from the Source Document.
[stock_picking_origin_state](stock_picking_origin_state/) | 17.0.1.0.0 |  | Expose the aggregated state of the origin pickings on a transfer
[stock_picking_partner_note](stock_picking_partner_note/) | 17.0.1.0.0 |  | Add partner notes on picking
[stock_picking_purchase_order_link](stock_picking_purchase_order_link/) | 17.0.1.0.0 |  | Link between picking and purchase order
[stock_picking_return_lot](stock_picking_return_lot/) | 17.0.1.0.0 |  | Propagate SN/lots from origin picking to return picking.
[stock_picking_return_restricted_qty](stock_picking_return_restricted_qty/) | 17.0.1.0.0 |  | Restrict the return to delivered quantity
[stock_picking_sale_order_link](stock_picking_sale_order_link/) | 17.0.1.0.0 |  | Link between picking and sale order
[stock_picking_send_by_mail](stock_picking_send_by_mail/) | 17.0.1.0.0 |  | Send stock picking by email
[stock_picking_show_backorder](stock_picking_show_backorder/) | 17.0.1.0.0 |  | Provides a new field on stock pickings, allowing to display the corresponding backorders.
[stock_picking_show_return](stock_picking_show_return/) | 17.0.1.0.1 |  | Show returns on stock pickings
[stock_picking_supplier_ref](stock_picking_supplier_ref/) | 17.0.1.0.0 |  | Adds a supplier reference field inside supplier's pickings and allows search for this reference.
[stock_picking_tier_validation](stock_picking_tier_validation/) | 17.0.1.0.0 |  | Extends the functionality of Transfers to support a tier validation process.
[stock_picking_warn_message](stock_picking_warn_message/) | 17.0.1.0.0 |  | Add a popup warning on picking to ensure warning is populated
[stock_product_security](stock_product_security/) | 17.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Stock Product Security
[stock_production_lot_active](stock_production_lot_active/) | 17.0.1.0.0 | <a href='https://github.com/ThomasBinsfeld'><img src='https://github.com/ThomasBinsfeld.png' width='32' height='32' style='border-radius:50%;' alt='ThomasBinsfeld'/></a> | Allow to archive/unarchive lots/serial numbers
[stock_push_delay](stock_push_delay/) | 17.0.1.1.1 |  | Manual evaluation of Push rules
[stock_putaway_hook](stock_putaway_hook/) | 17.0.1.0.0 |  | Add hooks allowing modules to add more putaway strategies
[stock_quant_package_dimension](stock_quant_package_dimension/) | 17.0.1.0.0 |  | Use dimensions on packages
[stock_quant_package_product_packaging](stock_quant_package_product_packaging/) | 17.0.1.0.0 |  | Use product packagings on packages
[stock_receipt_lot_info](stock_receipt_lot_info/) | 17.0.1.0.0 |  | Be able to introduce more info on lot/serial number while processing a receipt.
[stock_restrict_by_planned_consumed_date](stock_restrict_by_planned_consumed_date/) | 17.0.1.0.0 |  | Stock restrict by planned consumed date
[stock_restrict_lot](stock_restrict_lot/) | 17.0.1.2.1 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Base module that add back the concept of restrict lot on stock move
[stock_scrap_tier_validation](stock_scrap_tier_validation/) | 17.0.1.0.1 |  | Stock Scrap Tier Validation
[stock_scrap_tier_validation_mrp](stock_scrap_tier_validation_mrp/) | 17.0.1.0.0 |  | Stock Scrap Tier Validation: MRP compatibility
[stock_split_picking](stock_split_picking/) | 17.0.1.0.0 |  | Split a picking in two not transferred pickings
[stock_valuation_layer_usage](stock_valuation_layer_usage/) | 17.0.1.1.0 |  | Trace where has the stock valuation been used in, including the quantities taken.

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-weighing&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/stock-weighing/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-weighing/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/stock-weighing/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/stock-weighing/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/stock-weighing/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-weighing)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-weighing-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-weighing-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# stock-weighing

stock-weighing

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[web_widget_remote_measure](web_widget_remote_measure/) | 17.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allows to connect to remote devices to record measures
[web_widget_remote_measure_utilcell](web_widget_remote_measure_utilcell/) | 17.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Compatibility with UTILCELL propietary protocols

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/storage&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/storage/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/storage/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/storage/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/storage/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/storage/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/storage)
[![Translation Status](https://translation.odoo-community.org/widgets/storage-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/storage-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# storage

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[fs_attachment](fs_attachment/) | 17.0.1.6.2 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Store attachments on external object store
[fs_attachment_s3](fs_attachment_s3/) | 17.0.1.2.1 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Store attachments into S3 complient filesystem
[fs_base_multi_image](fs_base_multi_image/) | 17.0.1.0.1 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Mulitple Images from External File System
[fs_base_multi_media](fs_base_multi_media/) | 17.0.1.0.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Give the possibility to store media data in external filesystem from odoo
[fs_file](fs_file/) | 17.0.1.0.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Field to store files into filesystem storages
[fs_file_demo](fs_file_demo/) | 17.0.1.0.0 |  | Demo addon for fs_file and fs_image
[fs_image](fs_image/) | 17.0.1.0.2 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Field to store images into filesystem storages
[fs_image_thumbnail](fs_image_thumbnail/) | 17.0.1.0.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Generate and store thumbnail for images
[fs_product_brand_multi_image](fs_product_brand_multi_image/) | 17.0.1.0.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Link images to product brands
[fs_product_multi_image](fs_product_multi_image/) | 17.0.1.0.1 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Manage multi images from extenal file system on product
[fs_product_multi_media](fs_product_multi_media/) | 17.0.1.0.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Link media to products and categories
[fs_storage](fs_storage/) | 17.0.2.1.1 |  | Implement the concept of Storage with amazon S3, sftp...
[image_tag](image_tag/) | 17.0.1.0.0 |  | Image tag model
[storage_backend](storage_backend/) | 17.0.1.0.0 |  | Implement the concept of Storage with amazon S3, sftp...
[storage_backend_sftp](storage_backend_sftp/) | 17.0.1.0.0 |  | Implement SFTP Storage

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/survey&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/survey/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/survey/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/survey/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/survey/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/survey/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/survey)
[![Translation Status](https://translation.odoo-community.org/widgets/survey-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/survey-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# survey

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[partner_survey](partner_survey/) | 17.0.1.0.0 |  | Link partners with their survey results
[survey_answer_generation](survey_answer_generation/) | 17.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Link and compare answers from another survey
[survey_certification_py3o](survey_certification_py3o/) | 17.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Survey Certification Py3o
[survey_certification_sending](survey_certification_sending/) | 17.0.1.1.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Controls the automatic sending of certifications in surveys.
[survey_contact_generation](survey_contact_generation/) | 17.0.1.0.1 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Generate new contacts from surveys
[survey_crm_generation](survey_crm_generation/) | 17.0.1.0.2 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Generate CRM leads/opportunities from surveys
[survey_crm_sale_generation](survey_crm_sale_generation/) | 17.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Link CRM leads to sale orders generated from surveys
[survey_legal](survey_legal/) | 17.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Require legal terms before survey submit
[survey_multi_company](survey_multi_company/) | 17.0.1.0.1 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Company security for surveys
[survey_next_survey_update_partner](survey_next_survey_update_partner/) | 17.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Update the partner values when it's generated from the previous survey
[survey_partner_representative](survey_partner_representative/) | 17.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Fill the survey on behalf of others
[survey_question_type_binary](survey_question_type_binary/) | 17.0.1.0.0 |  | This module add binary field as question type for survey page
[survey_resource_booking](survey_resource_booking/) | 17.0.1.0.0 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Access survey answers from resource booking
[survey_result_mail](survey_result_mail/) | 17.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Send survey answers to the survey user
[survey_sale_generation](survey_sale_generation/) | 17.0.1.0.3 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Generate sale orders from surveys
[survey_skip_start](survey_skip_start/) | 17.0.1.0.2 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Skip the surveys start screen and go directly to fill the form

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/timesheet&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/timesheet/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/timesheet/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/timesheet/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/timesheet/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/timesheet/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/timesheet)
[![Translation Status](https://translation.odoo-community.org/widgets/timesheet-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/timesheet-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# timesheet

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[crm_timesheet](crm_timesheet/) | 17.0.1.0.2 |  | CRM Timesheet
[hr_timesheet_autofill_project_off](hr_timesheet_autofill_project_off/) | 17.0.1.0.0 |  | Timesheet - Autofill project off
[hr_timesheet_begin_end](hr_timesheet_begin_end/) | 17.0.1.0.1 |  | Timesheet - Begin/End Hours
[hr_timesheet_calendar](hr_timesheet_calendar/) | 17.0.1.0.0 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | HR Timesheet Calendar
[hr_timesheet_date_order_desc](hr_timesheet_date_order_desc/) | 17.0.1.0.0 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | Add new timesheet entries to the top of the list and order by date descending
[hr_timesheet_editable_top](hr_timesheet_editable_top/) | 17.0.1.0.0 |  | Add new timesheet entries to the top of the list
[hr_timesheet_employee_analytic_tag](hr_timesheet_employee_analytic_tag/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Hr Timesheet Employee Analytic Tag
[hr_timesheet_portal](hr_timesheet_portal/) | 17.0.1.0.0 |  | Fill in timesheets via the portal
[hr_timesheet_report](hr_timesheet_report/) | 17.0.1.0.0 | <a href='https://github.com/alexey-pelykh'><img src='https://github.com/alexey-pelykh.png' width='32' height='32' style='border-radius:50%;' alt='alexey-pelykh'/></a> | Generate Timesheet Report from Task Logs
[hr_timesheet_sheet](hr_timesheet_sheet/) | 17.0.1.2.0 |  | Timesheet Sheets, Activities
[hr_timesheet_sheet_autodraft](hr_timesheet_sheet_autodraft/) | 17.0.1.0.0 |  | Automatically draft a Timesheet Sheet for every time entry that does not have a relevant Timesheet Sheet existing.
[hr_timesheet_task_domain](hr_timesheet_task_domain/) | 17.0.1.0.0 |  | Limit task selection to tasks on currently-selected project
[hr_timesheet_task_required](hr_timesheet_task_required/) | 17.0.1.0.1 |  | Set task on timesheet as a mandatory field
[hr_timesheet_task_stage](hr_timesheet_task_stage/) | 17.0.1.1.0 |  | Open/Close task from corresponding Task Log entry
[hr_timesheet_time_type](hr_timesheet_time_type/) | 17.0.1.0.0 |  | Ability to add time type in timesheet lines.
[hr_timesheet_type_non_billable](hr_timesheet_type_non_billable/) | 17.0.1.0.0 | <a href='https://github.com/mpascuall'><img src='https://github.com/mpascuall.png' width='32' height='32' style='border-radius:50%;' alt='mpascuall'/></a> | HR Timesheet Type Non Billable
[hr_timesheet_unusual_days](hr_timesheet_unusual_days/) | 17.0.1.0.0 | <a href='https://github.com/CRogos'><img src='https://github.com/CRogos.png' width='32' height='32' style='border-radius:50%;' alt='CRogos'/></a> | HR Timesheet Calendar Unusual Days
[project_task_analytic_propagation](project_task_analytic_propagation/) | 17.0.1.0.0 | <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Updates timesheet's analytic account when their task changes the analytic.
[project_timesheet_billable_per_line](project_timesheet_billable_per_line/) | 17.0.1.0.0 |  | Generate sales orders from billable timesheets grouped by analytic account
[project_timesheet_holidays_editable](project_timesheet_holidays_editable/) | 17.0.1.0.0 |  | Re-enables timesheet edition when they're generated from leaves
[sale_timesheet_line_exclude](sale_timesheet_line_exclude/) | 17.0.1.2.1 |  | Exclude Timesheet Line from Sale Order
[sale_timesheet_rounded](sale_timesheet_rounded/) | 17.0.1.0.0 |  | Round timesheet entries amount based on project settings.
[sale_timesheet_timeline](sale_timesheet_timeline/) | 17.0.1.0.0 |  | Dates planning in sales order lines

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/vertical-association&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/vertical-association/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/vertical-association/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/vertical-association/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/vertical-association/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/vertical-association/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/vertical-association)
[![Translation Status](https://translation.odoo-community.org/widgets/vertical-association-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/vertical-association-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# vertical-association

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[contract_membership_delegated_partner](contract_membership_delegated_partner/) | 17.0.1.0.0 |  | Set delegate membership on the contract
[membership_delegated_partner](membership_delegated_partner/) | 17.0.1.0.0 |  | Delegate membership on a specific partner
[membership_extension](membership_extension/) | 17.0.1.0.3 |  | Improves user experience of membership addon
[membership_initial_fee](membership_initial_fee/) | 17.0.1.0.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | Initial fee for memberships
[membership_variable_period](membership_variable_period/) | 17.0.1.0.1 |  | Variable period for memberships
[website_membership_gamification](website_membership_gamification/) | 17.0.1.0.0 |  | Show badges assigned to users on website
[website_membership_random_order](website_membership_random_order/) | 17.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Online Members Directory - Random order

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

## From OCA/vertical-edition


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/vertical-edition&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/vertical-edition/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/vertical-edition/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/vertical-edition/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/vertical-edition/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/vertical-edition/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/vertical-edition)
[![Translation Status](https://translation.odoo-community.org/widgets/vertical-edition-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/vertical-edition-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# vertical-edition

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[bookstore_mgmt](bookstore_mgmt/) | 17.0.3.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> <a href='https://github.com/miquelalzanillas'><img src='https://github.com/miquelalzanillas.png' width='32' height='32' style='border-radius:50%;' alt='miquelalzanillas'/></a> | Bookstore management system for Odoo
[bookstore_mgmt_google_books_api](bookstore_mgmt_google_books_api/) | 17.0.1.2.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> <a href='https://github.com/miquelalzanillas'><img src='https://github.com/miquelalzanillas.png' width='32' height='32' style='border-radius:50%;' alt='miquelalzanillas'/></a> | Bookstore integration with Google Books API

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

## From OCA/vertical-hotel


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/vertical-hotel&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/vertical-hotel/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/vertical-hotel/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/vertical-hotel/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/vertical-hotel/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/vertical-hotel/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/vertical-hotel)
[![Translation Status](https://translation.odoo-community.org/widgets/vertical-hotel-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/vertical-hotel-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# vertical-hotel

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[hotel](hotel/) | 17.0.1.0.0 |  | Hotel Management to Manage Folio and Hotel Configuration
[hotel_housekeeping](hotel_housekeeping/) | 17.0.1.0.0 |  | Manages Housekeeping Activities and its Process
[hotel_reservation](hotel_reservation/) | 17.0.1.0.0 |  | Manages Guest Reservation & displays Reservation Summary
[hotel_restaurant](hotel_restaurant/) | 17.0.1.0.0 |  | Table booking facilities and Managing customers orders
[report_hotel_reservation](report_hotel_reservation/) | 17.0.1.0.0 |  | Hotel Reservation Management - Reporting
[report_hotel_restaurant](report_hotel_restaurant/) | 17.0.1.0.0 |  | Restaurant Management - Reporting

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/web&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/web/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/web/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/web/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/web/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/web/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/web)
[![Translation Status](https://translation.odoo-community.org/widgets/web-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/web-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# web

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[web_calendar_slot_duration](web_calendar_slot_duration/) | 17.0.1.0.0 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Customizable calendar slot durations
[web_chatter_position](web_chatter_position/) | 17.0.1.0.1 | <a href='https://github.com/trisdoan'><img src='https://github.com/trisdoan.png' width='32' height='32' style='border-radius:50%;' alt='trisdoan'/></a> | Add an option to change the chatter position
[web_company_color](web_company_color/) | 17.0.1.2.3 |  | Web Company Color
[web_dialog_size](web_dialog_size/) | 17.0.1.0.1 |  | A module that lets the user expand a dialog box to the full screen width.
[web_editor_class_selector](web_editor_class_selector/) | 17.0.1.1.0 |  | Web editor class selector
[web_environment_ribbon](web_environment_ribbon/) | 17.0.1.0.3 |  | Web Environment Ribbon
[web_favicon](web_favicon/) | 17.0.1.0.2 |  | Allows to set a custom shortcut icon (aka favicon)
[web_field_tooltip](web_field_tooltip/) | 17.0.1.0.0 |  | Displays customizable tooltips for fields
[web_font_size_report_layout](web_font_size_report_layout/) | 17.0.1.1.0 |  | Adds a font size selector (pt) to the Document Layout wizard
[web_group_expand](web_group_expand/) | 17.0.1.0.0 |  | Group Expand Buttons
[web_ir_actions_act_multi](web_ir_actions_act_multi/) | 17.0.1.0.0 |  | Enables triggering of more than one action on ActionManager
[web_m2x_options](web_m2x_options/) | 17.0.1.0.8 |  | web_m2x_options
[web_m2x_options_manager](web_m2x_options_manager/) | 17.0.1.0.1 |  | Adds an interface to manage the "Create" and "Create and Edit" options for specific models and fields.
[web_no_bubble](web_no_bubble/) | 17.0.1.0.0 |  | Remove the bubbles from the web interface
[web_notify](web_notify/) | 17.0.1.1.0 |  | Send notification messages to user
[web_pivot_computed_measure](web_pivot_computed_measure/) | 17.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Web Pivot Computed Measure
[web_pwa_customize](web_pwa_customize/) | 17.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Web Pwa Customize
[web_refresher](web_refresher/) | 17.0.1.1.3 |  | Web Refresher
[web_remember_tree_column_width](web_remember_tree_column_width/) | 17.0.1.0.0 | <a href='https://github.com/frahikLV'><img src='https://github.com/frahikLV.png' width='32' height='32' style='border-radius:50%;' alt='frahikLV'/></a> <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> <a href='https://github.com/cuongnmtm'><img src='https://github.com/cuongnmtm.png' width='32' height='32' style='border-radius:50%;' alt='cuongnmtm'/></a> | Remember the tree columns' widths across sessions.
[web_responsive](web_responsive/) | 17.0.1.1.10 | <a href='https://github.com/Tardo'><img src='https://github.com/Tardo.png' width='32' height='32' style='border-radius:50%;' alt='Tardo'/></a> <a href='https://github.com/SplashS'><img src='https://github.com/SplashS.png' width='32' height='32' style='border-radius:50%;' alt='SplashS'/></a> | Responsive web client, community-supported
[web_save_discard_button](web_save_discard_button/) | 17.0.1.0.1 | <a href='https://github.com/synconics'><img src='https://github.com/synconics.png' width='32' height='32' style='border-radius:50%;' alt='synconics'/></a> | Save & Discard Buttons
[web_search_with_and](web_search_with_and/) | 17.0.1.0.0 |  | Use AND conditions on omnibar search
[web_theme_classic](web_theme_classic/) | 17.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Contrasted style on fields to improve the UI.
[web_time_range_menu_custom](web_time_range_menu_custom/) | 17.0.1.0.0 |  | Web Time Range Menu Custom
[web_timeline](web_timeline/) | 17.0.1.1.0 | <a href='https://github.com/tarteo'><img src='https://github.com/tarteo.png' width='32' height='32' style='border-radius:50%;' alt='tarteo'/></a> | Interactive visualization chart to show events in time
[web_tree_duplicate](web_tree_duplicate/) | 17.0.1.0.0 | <a href='https://github.com/tarteo'><img src='https://github.com/tarteo.png' width='32' height='32' style='border-radius:50%;' alt='tarteo'/></a> | Duplicate records directly from the tree view.
[web_tree_dynamic_colored_field](web_tree_dynamic_colored_field/) | 17.0.1.0.0 |  | Allows you to dynamically color fields on tree views
[web_tree_many2one_clickable](web_tree_many2one_clickable/) | 17.0.1.0.0 |  | Open the linked resource when clicking on their name
[web_widget_bokeh_chart](web_widget_bokeh_chart/) | 17.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | This widget allows to display charts using Bokeh library.
[web_widget_domain_editor_dialog](web_widget_domain_editor_dialog/) | 17.0.1.0.0 |  | Recovers the Domain Editor Dialog functionality
[web_widget_dropdown_dynamic](web_widget_dropdown_dynamic/) | 17.0.2.0.0 |  | This module adds support for dynamic dropdown widget
[web_widget_image_download](web_widget_image_download/) | 17.0.1.0.0 |  | Allows to download any image from its widget
[web_widget_mpld3_chart](web_widget_mpld3_chart/) | 17.0.1.0.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | This widget allows to display charts using MPLD3 library.
[web_widget_numeric_step](web_widget_numeric_step/) | 17.0.1.0.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Web Widget Numeric Step
[web_widget_open_tab](web_widget_open_tab/) | 17.0.1.0.0 |  | Allow to open record from trees on new tab from tree views
[web_widget_plotly_chart](web_widget_plotly_chart/) | 17.0.1.0.0 | <a href='https://github.com/robyf70'><img src='https://github.com/robyf70.png' width='32' height='32' style='border-radius:50%;' alt='robyf70'/></a> | Allow to draw plotly charts.
[web_widget_popover](web_widget_popover/) | 17.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Render an icon that displays the field content in a popover
[web_widget_product_label_section_and_note](web_widget_product_label_section_and_note/) | 17.0.2.0.2 |  | unify the product and name into a single column
[web_widget_section_and_note_text_scrollable](web_widget_section_and_note_text_scrollable/) | 17.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Make the text field of Section and Note widget scrollable
[web_widget_url_advanced](web_widget_url_advanced/) | 17.0.1.0.0 |  | This module extends URL widget for displaying anchors with custom labels.
[web_widget_x2many_2d_matrix](web_widget_x2many_2d_matrix/) | 17.0.2.0.1 | <a href='https://github.com/JasminSForgeFlow'><img src='https://github.com/JasminSForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JasminSForgeFlow'/></a> <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Show list fields as a matrix

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/web-api&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/web-api/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/web-api/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/web-api/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/web-api/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/web-api/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/web-api)
[![Translation Status](https://translation.odoo-community.org/widgets/web-api-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/web-api-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Web API

Collect Odoo modules that help exposing web APIs and/or deal with external web APIs.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[endpoint](endpoint/) | 17.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Provide custom endpoint machinery.
[endpoint_auth_api_key](endpoint_auth_api_key/) | 17.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Provide API key auth for endpoints.
[endpoint_route_handler](endpoint_route_handler/) | 17.0.1.0.2 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Provide mixin and tool to generate custom endpoints on the fly.
[webservice](webservice/) | 17.0.1.0.1 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Defines webservice abstract definition to be used generally

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/website&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/website/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/website/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/website/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/website/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/website/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/website)
[![Translation Status](https://translation.odoo-community.org/widgets/website-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/website-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# website

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[portal_invitation_by_website](portal_invitation_by_website/) | 17.0.1.1.1 |  | Restrict portal users to a specific website from the invitation wizard
[website_breadcrumb](website_breadcrumb/) | 17.0.1.0.0 |  | Let you have breadcrumbs in website pages
[website_conditional_visibility_user_group](website_conditional_visibility_user_group/) | 17.0.1.0.0 |  | Only internal users will see the blocks you add this condition to
[website_cookiebot](website_cookiebot/) | 17.0.1.0.1 |  | Ask for cookies consent connecting with Cookiebot
[website_cookiefirst](website_cookiefirst/) | 17.0.2.0.1 |  | Cookiefirst integration
[website_crm_quick_answer](website_crm_quick_answer/) | 17.0.1.0.0 |  | Add an automatic answer for contacts asking for info
[website_form_require_legal](website_form_require_legal/) | 17.0.1.0.0 |  | Add possibility to require confirm legal terms.
[website_forum_subscription](website_forum_subscription/) | 17.0.1.0.1 |  | Adds a button to allow subscription from the website
[website_google_tag_manager](website_google_tag_manager/) | 17.0.1.0.1 |  | Add support for Google Tag Manager
[website_legal_page](website_legal_page/) | 17.0.1.0.0 |  | Website Legal Page
[website_local_font](website_local_font/) | 17.0.1.0.0 |  | Allows to add local fonts on Odoo website
[website_login_page_editable](website_login_page_editable/) | 17.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Add an editable area to the website login page
[website_menu_by_user_status](website_menu_by_user_status/) | 17.0.1.0.0 |  | Allow to manage the display of website.menus
[website_odoo_debranding](website_odoo_debranding/) | 17.0.1.0.0 |  | Remove Odoo Branding from Website
[website_require_login](website_require_login/) | 17.0.1.0.0 |  | Website Login Required
[website_snippet_big_button](website_snippet_big_button/) | 17.0.1.0.0 |  | A snippet that adds two big buttons
[website_snippet_marginless_gallery](website_snippet_marginless_gallery/) | 17.0.1.0.0 |  | Add a snippet to have a marginless image gallery
[website_whatsapp](website_whatsapp/) | 17.0.1.1.0 | <a href='https://github.com/ioans73'><img src='https://github.com/ioans73.png' width='32' height='32' style='border-radius:50%;' alt='ioans73'/></a> | Whatsapp integration

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

## From OCA/wms


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/wms&target_branch=17.0)
[![Pre-commit Status](https://github.com/OCA/wms/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/OCA/wms/actions/workflows/pre-commit.yml?query=branch%3A17.0)
[![Build Status](https://github.com/OCA/wms/actions/workflows/test.yml/badge.svg?branch=17.0)](https://github.com/OCA/wms/actions/workflows/test.yml?query=branch%3A17.0)
[![codecov](https://codecov.io/gh/OCA/wms/branch/17.0/graph/badge.svg)](https://codecov.io/gh/OCA/wms)
[![Translation Status](https://translation.odoo-community.org/widgets/wms-17-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/wms-17-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# wms

WMS modules for Odoo

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[stock_picking_type_shipping_policy](stock_picking_type_shipping_policy/) | 17.0.1.0.0 |  | Define different shipping policies according to picking type
[stock_warehouse_flow](stock_warehouse_flow/) | 17.0.1.0.0 |  | Configure routing flow for stock moves

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

