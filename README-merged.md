# Merged READMEs

## From OCA/OpenUpgrade

[![Pre-commit Status](https://github.com/OCA/OpenUpgrade/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/OpenUpgrade/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/OpenUpgrade/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/OpenUpgrade/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/OpenUpgrade/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/openupgrade)

<!-- /!\ do not modify above this line -->

![OpenUpgrade logo](https://oca.github.io/OpenUpgrade/_images/OpenUpgrade.png)

# Tools to upgrade Odoo instances from a major version to another

This <a href="https://odoo-community.org">OCA</a> project aims to provide an
Open Source upgrade path for <a href="https://github.com/odoo/odoo">Odoo</a> from one
major Odoo version to the next one.

It is hosted at <a href="https://github.com/oca/openupgrade">GitHub</a>.

For documentation, see <a href="https://oca.github.io/OpenUpgrade">here</a>.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[openupgrade_framework](openupgrade_framework/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/StefanRijnhart'><img src='https://github.com/StefanRijnhart.png' width='32' height='32' style='border-radius:50%;' alt='StefanRijnhart'/></a> <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Module to integrate in the server_wide_modules option to make upgrades between two major revisions.
[openupgrade_scripts](openupgrade_scripts/) | 16.0.1.0.5 |  | Module that contains all the migrations analysis and scripts for migrating Odoo SA modules.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-analytic&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/account-analytic/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-analytic/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/account-analytic/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-analytic/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/account-analytic/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-analytic)
[![Translation Status](https://translation.odoo-community.org/widgets/account-analytic-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-analytic-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_analytic_account_tag](account_analytic_account_tag/) | 16.0.1.0.0 |  | Restore the tag_ids in account.analytic.account
[account_analytic_distribution_manual](account_analytic_distribution_manual/) | 16.0.2.5.0 |  | Account analytic distribution manual
[account_analytic_document_date](account_analytic_document_date/) | 16.0.1.0.2 | <a href='https://github.com/mpascuall'><img src='https://github.com/mpascuall.png' width='32' height='32' style='border-radius:50%;' alt='mpascuall'/></a> <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> | Account Analytic Document Date
[account_analytic_organization](account_analytic_organization/) | 16.0.1.0.1 | <a href='https://github.com/mpascuall'><img src='https://github.com/mpascuall.png' width='32' height='32' style='border-radius:50%;' alt='mpascuall'/></a> | Adds organization field on the partner so you can use it on your analytic
[account_analytic_parent](account_analytic_parent/) | 16.0.1.0.1 |  | This module reintroduces the hierarchy to the analytic accounts.
[account_analytic_required](account_analytic_required/) | 16.0.2.0.1 |  | Account Analytic Required
[account_analytic_root](account_analytic_root/) | 16.0.1.0.0 | <a href='https://github.com/victor-champonnois'><img src='https://github.com/victor-champonnois.png' width='32' height='32' style='border-radius:50%;' alt='victor-champonnois'/></a> | Compute the Root Analytic Account
[account_analytic_sequence](account_analytic_sequence/) | 16.0.1.0.0 |  | Restore the analytic account sequence
[account_analytic_tag](account_analytic_tag/) | 16.0.1.1.2 |  | Account Analytic Tag
[account_analytic_tag_distribution](account_analytic_tag_distribution/) | 16.0.1.0.2 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Account Analytic Tag Distribution
[account_move_update_analytic](account_move_update_analytic/) | 16.0.1.0.2 | <a href='https://github.com/remi-filament'><img src='https://github.com/remi-filament.png' width='32' height='32' style='border-radius:50%;' alt='remi-filament'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | This module allows the user to update analytic on posted moves
[analytic_amount_security](analytic_amount_security/) | 16.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Add a group to constrain which users can see what info on the analytic lines
[analytic_base_department](analytic_base_department/) | 16.0.1.0.0 |  | Add relationship between Analytic and Department
[analytic_distribution_widget_remove_save](analytic_distribution_widget_remove_save/) | 16.0.1.0.1 |  | Remove save button on analytic distribution widget
[analytic_hr_department_restriction](analytic_hr_department_restriction/) | 16.0.1.1.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Analytic distributions restriction per HR department
[analytic_mixin_analytic_account](analytic_mixin_analytic_account/) | 16.0.1.0.0 |  | Analytic Mixin Analytic Account
[analytic_partner](analytic_partner/) | 16.0.1.0.0 |  | Search and group analytic entries by partner
[crm_claim_analytic](crm_claim_analytic/) | 16.0.1.0.0 | <a href='https://github.com/MiguelPoyatos'><img src='https://github.com/MiguelPoyatos.png' width='32' height='32' style='border-radius:50%;' alt='MiguelPoyatos'/></a> | CRM Claim Analytic
[hr_department_analytic](hr_department_analytic/) | 16.0.1.0.0 |  | This module allows to specify analytic account on hr department
[hr_expense_analytic_tag](hr_expense_analytic_tag/) | 16.0.1.0.2 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Hr Expense Analytic Tag
[hr_timesheet_analytic_tag](hr_timesheet_analytic_tag/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Hr Timesheet Analytic Tag
[mrp_stock_analytic](mrp_stock_analytic/) | 16.0.1.0.0 |  | MRP Stock Analytic
[pos_analytic_by_config](pos_analytic_by_config/) | 16.0.1.0.1 |  | Use analytic account defined on POS configuration for POS orders
[product_analytic](product_analytic/) | 16.0.1.1.1 |  | Add analytic account on products and product categories
[product_analytic_purchase](product_analytic_purchase/) | 16.0.1.0.0 |  | Glue module between purchase and product_analytic
[product_analytic_sale](product_analytic_sale/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Glue module between sale and product_analytic
[purchase_analytic](purchase_analytic/) | 16.0.2.1.0 |  | Purchase Analytic
[purchase_analytic_tag](purchase_analytic_tag/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Purchase Analytic Tag
[purchase_stock_analytic](purchase_stock_analytic/) | 16.0.1.0.1 |  | Copies the analytic distribution of the purchase order item to the stock move
[sale_analytic_tag](sale_analytic_tag/) | 16.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Sale Analytic Tag
[stock_analytic](stock_analytic/) | 16.0.1.4.0 |  | Adds analytic distribution in stock move
[stock_landed_costs_analytic](stock_landed_costs_analytic/) | 16.0.1.0.0 |  | This module adds an analytic account and analytic tags on landed costs lines so that on landed costs validation account moves get analytic account and analytic tags values from landed costs lines.
[stock_picking_analytic](stock_picking_analytic/) | 16.0.1.0.1 |  | Allows to define the analytic account on picking level

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-budgeting&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/account-budgeting/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-budgeting/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/account-budgeting/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-budgeting/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/account-budgeting/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-budgeting)
[![Translation Status](https://translation.odoo-community.org/widgets/account-budgeting-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-budgeting-16-0/?utm_source=widget)

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
[account_budget_oca](account_budget_oca/) | 16.0.1.0.2 |  | Budgets Management

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-closing&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/account-closing/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-closing/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/account-closing/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-closing/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/account-closing/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-closing)
[![Translation Status](https://translation.odoo-community.org/widgets/account-closing-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-closing-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# account-closing

{'TODO': 'add repo description.'}

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_cutoff_accrual_order_base](account_cutoff_accrual_order_base/) | 16.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Accrued Order Base
[account_cutoff_accrual_order_stock_base](account_cutoff_accrual_order_stock_base/) | 16.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Accrued Order Stock Base
[account_cutoff_accrual_purchase](account_cutoff_accrual_purchase/) | 16.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Accrued Expense on Purchase Order
[account_cutoff_accrual_purchase_stock](account_cutoff_accrual_purchase_stock/) | 16.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Accrued Order Base
[account_cutoff_accrual_sale](account_cutoff_accrual_sale/) | 16.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Accrued Revenue on Sales Order
[account_cutoff_accrual_sale_stock](account_cutoff_accrual_sale_stock/) | 16.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Glue module for Cut-Off Accruals on Sales with Stock
[account_cutoff_accrual_sale_stock_delivery](account_cutoff_accrual_sale_stock_delivery/) | 16.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Glue module for Cut-Off Accruals on Sales with Stock Delivery
[account_cutoff_accrual_subscription](account_cutoff_accrual_subscription/) | 16.0.1.2.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Accrued expenses based on subscriptions
[account_cutoff_base](account_cutoff_base/) | 16.0.1.6.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Base module for Account Cut-offs
[account_cutoff_picking](account_cutoff_picking/) | 16.0.1.3.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Accrued and prepaid expense/revenue from pickings
[account_cutoff_start_end_dates](account_cutoff_start_end_dates/) | 16.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Cutoffs based on start/end dates
[account_fiscal_year_closing](account_fiscal_year_closing/) | 16.0.1.0.0 |  | Generic fiscal year closing wizard
[account_invoice_start_end_dates](account_invoice_start_end_dates/) | 16.0.1.5.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adds start/end dates on invoice/move lines
[account_invoice_start_end_dates_move](account_invoice_start_end_dates_move/) | 16.0.1.0.0 |  | Add the possibility to choose start and end dates on account invoice.
[account_multicurrency_revaluation](account_multicurrency_revaluation/) | 16.0.1.0.1 |  | Manage revaluation for multicurrency environment

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# account-financial-reporting
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-financial-reporting&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/account-financial-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-financial-reporting/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/account-financial-reporting/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-financial-reporting/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/account-financial-reporting/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-financial-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/account-financial-reporting-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-financial-reporting-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_financial_report](account_financial_report/) | 16.0.1.18.0 |  | OCA Financial Reports
[account_financial_report_sale](account_financial_report_sale/) | 16.0.1.1.0 |  | OCA Financial Reports Sale
[account_liquidity_forecast](account_liquidity_forecast/) | 16.0.1.0.0 |  | Account Liquidity Forecast
[account_purchase_stock_report_non_billed](account_purchase_stock_report_non_billed/) | 16.0.1.0.1 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Account Purchase Stock Report Non Billed
[account_sale_stock_report_non_billed](account_sale_stock_report_non_billed/) | 16.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Account Sale Stock Report Non Billed
[account_tax_balance](account_tax_balance/) | 16.0.1.1.4 |  | Compute tax balances based on date range
[mis_builder_cash_flow](mis_builder_cash_flow/) | 16.0.1.1.0 | <a href='https://github.com/jjscarafia'><img src='https://github.com/jjscarafia.png' width='32' height='32' style='border-radius:50%;' alt='jjscarafia'/></a> | MIS Builder Cash Flow
[mis_template_financial_report](mis_template_financial_report/) | 16.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Profit & Loss / Balance sheet MIS templates
[partner_statement](partner_statement/) | 16.0.1.3.3 | <a href='https://github.com/MiquelRForgeFlow'><img src='https://github.com/MiquelRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='MiquelRForgeFlow'/></a> | OCA Financial Reports

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# account-financial-tools
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-financial-tools&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/account-financial-tools/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-financial-tools/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/account-financial-tools/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-financial-tools/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/account-financial-tools/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-financial-tools)
[![Translation Status](https://translation.odoo-community.org/widgets/account-financial-tools-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-financial-tools-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_account_tag_code](account_account_tag_code/) | 16.0.1.0.0 |  | Add a code field to the accounts tags
[account_asset_batch_compute](account_asset_batch_compute/) | 16.0.1.0.0 |  | Add the possibility to compute assets in batch
[account_asset_low_value](account_asset_low_value/) | 16.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Assets Management - Low Value Asset
[account_asset_management](account_asset_management/) | 16.0.1.3.0 |  | Assets Management
[account_asset_management_stock_lot](account_asset_management_stock_lot/) | 16.0.1.0.0 |  | Assets Management Stock Lot
[account_asset_number](account_asset_number/) | 16.0.1.1.0 |  | Assets Number
[account_asset_transfer](account_asset_transfer/) | 16.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Asset Transfer from AUC to Asset
[account_bank_statement_chatter](account_bank_statement_chatter/) | 16.0.1.0.0 | <a href='https://github.com/cubells'><img src='https://github.com/cubells.png' width='32' height='32' style='border-radius:50%;' alt='cubells'/></a> | Chatter on bank statements
[account_cash_deposit](account_cash_deposit/) | 16.0.1.4.0 |  | Manage cash deposits and cash orders
[account_chart_update](account_chart_update/) | 16.0.2.0.8 |  | Wizard to update a company's account chart from a template
[account_chart_update_l10n_eu_oss_oca](account_chart_update_l10n_eu_oss_oca/) | 16.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Account Chart update OSS OCA
[account_chart_update_multilang](account_chart_update_multilang/) | 16.0.1.0.3 | <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Update tax and fiscal position templates with multilang
[account_dashboard_banner](account_dashboard_banner/) | 16.0.2.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add a configurable banner on the accounting dashboard
[account_fiscal_month](account_fiscal_month/) | 16.0.1.1.0 |  | Provide a fiscal month date range type
[account_fiscal_position_vat_check](account_fiscal_position_vat_check/) | 16.0.1.1.0 |  | Check VAT on invoice validation
[account_fiscal_year](account_fiscal_year/) | 16.0.1.3.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Create Account Fiscal Year
[account_fiscal_year_auto_create](account_fiscal_year_auto_create/) | 16.0.1.0.2 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Automatically create new fiscal years, based on the datas of the last fiscal years
[account_invoice_constraint_chronology](account_invoice_constraint_chronology/) | 16.0.1.1.3 |  | Account Invoice Constraint Chronology
[account_journal_general_sequence](account_journal_general_sequence/) | 16.0.2.1.0 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Add configurable sequence to account moves, per journal
[account_journal_lock_date](account_journal_lock_date/) | 16.0.1.0.0 |  | Lock each journal independently
[account_journal_restrict_mode](account_journal_restrict_mode/) | 16.0.1.1.0 |  | Lock All Posted Entries of Journals.
[account_loan](account_loan/) | 16.0.1.1.1 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Account Loan management
[account_lock_date_update](account_lock_date_update/) | 16.0.1.0.1 |  | Allow an Account adviser to update locking date without having access to all technical settings
[account_lock_to_date](account_lock_to_date/) | 16.0.1.0.0 |  | Allows to set an account lock date in the future.
[account_move_budget](account_move_budget/) | 16.0.1.1.0 |  | Create Accounting Budgets
[account_move_fiscal_month](account_move_fiscal_month/) | 16.0.1.0.0 |  | Display the fiscal month on journal entries/item
[account_move_fiscal_year](account_move_fiscal_year/) | 16.0.1.0.0 |  | Display the fiscal year on journal entries/item
[account_move_line_check_number](account_move_line_check_number/) | 16.0.1.0.1 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Add the check number in the journal items
[account_move_line_landed_cost_info](account_move_line_landed_cost_info/) | 16.0.1.0.0 |  | Introduces the landed cost adjustment lines to the journal items
[account_move_line_purchase_info](account_move_line_purchase_info/) | 16.0.2.1.0 |  | Introduces the purchase order line to the journal items
[account_move_line_repair_info](account_move_line_repair_info/) | 16.0.1.0.0 |  | Introduces the repair order to the journal items
[account_move_line_sale_info](account_move_line_sale_info/) | 16.0.1.1.0 |  | Introduces the purchase order line to the journal items
[account_move_line_tax_editable](account_move_line_tax_editable/) | 16.0.1.0.1 |  | Allows to edit taxes on non-posted account move lines
[account_move_name_sequence](account_move_name_sequence/) | 16.0.1.1.12 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/moylop260'><img src='https://github.com/moylop260.png' width='32' height='32' style='border-radius:50%;' alt='moylop260'/></a> <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Generate journal entry number from sequence
[account_move_post_date_user](account_move_post_date_user/) | 16.0.1.0.0 | <a href='https://github.com/JordiMForgeFlow'><img src='https://github.com/JordiMForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiMForgeFlow'/></a> | Trace journal entry posting date and user.
[account_move_print](account_move_print/) | 16.0.1.0.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> | Adds the option to print Journal Entries
[account_move_template](account_move_template/) | 16.0.1.0.3 |  | Templates for recurring Journal Entries
[account_move_transfer_partner](account_move_transfer_partner/) | 16.0.1.0.0 | <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | Automation to translate amount due from many partners to one partner
[account_netting](account_netting/) | 16.0.1.0.1 |  | Compensate AR/AP accounts from the same partner
[account_partner_required](account_partner_required/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adds an option 'partner policy' on accounts
[account_reversal](account_reversal/) | 16.0.1.0.0 |  | Account reversal usability improvements
[account_sequence_option](account_sequence_option/) | 16.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Manage sequence options for account.move, i.e., invoice, bill, entry
[account_spread_cost_revenue](account_spread_cost_revenue/) | 16.0.1.0.1 |  | Spread costs and revenues over a custom period
[account_template_active](account_template_active/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Allow to disable / enable account template items (tax, fiscal position, account)
[account_usability](account_usability/) | 16.0.1.1.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Adds missing menu entries for Account module and adds the option to enable Saxon Accounting
[base_vat_optional_vies](base_vat_optional_vies/) | 16.0.1.1.1 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Optional validation of VAT via VIES
[purchase_unreconciled](purchase_unreconciled/) | 16.0.1.0.1 | <a href='https://github.com/AaronHForgeFlow'><img src='https://github.com/AaronHForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='AaronHForgeFlow'/></a> | Purchase Unreconciled
[stock_account_anglo_saxon_cogs_kit](stock_account_anglo_saxon_cogs_kit/) | 16.0.2.0.0 | <a href='https://github.com/MarinaAForgeFlow'><img src='https://github.com/MarinaAForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='MarinaAForgeFlow'/></a> <a href='https://github.com/AaronHForgeFlow'><img src='https://github.com/AaronHForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='AaronHForgeFlow'/></a> | Stock Account Anglo Saxon COGS Kit

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# account-fiscal-rule
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-fiscal-rule&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/account-fiscal-rule/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-fiscal-rule/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/account-fiscal-rule/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-fiscal-rule/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/account-fiscal-rule/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-fiscal-rule)
[![Translation Status](https://translation.odoo-community.org/widgets/account-fiscal-rule-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-fiscal-rule-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Odoo Accounting Taxe and Fiscal Features

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_avatax_exemption](account_avatax_exemption/) | 16.0.1.0.0 |  | This application allows you to add exemptions to Avatax
[account_avatax_exemption_base](account_avatax_exemption_base/) | 16.0.1.1.1 |  | This application allows you to add exemptions base to Avatax
[account_avatax_oca](account_avatax_oca/) | 16.0.1.7.0 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Compute Sales Tax using the Avalara Avatax Service
[account_avatax_oca_log](account_avatax_oca_log/) | 16.0.1.0.0 |  | Add Logs to Avatax calls
[account_avatax_repair_oca](account_avatax_repair_oca/) | 16.0.1.0.0 |  | Repair Orders with automatic Tax application using Avatax
[account_avatax_sale_oca](account_avatax_sale_oca/) | 16.0.1.3.0 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Sales Orders with automatic Tax application using Avatax
[account_avatax_website_sale](account_avatax_website_sale/) | 16.0.1.0.0 | <a href='https://github.com/cybernexus'><img src='https://github.com/cybernexus.png' width='32' height='32' style='border-radius:50%;' alt='cybernexus'/></a> | Ecommerce Sales Orders require tax recalculation prior to payment.
[account_ecotax](account_ecotax/) | 16.0.2.0.0 | <a href='https://github.com/mourad-ehm'><img src='https://github.com/mourad-ehm.png' width='32' height='32' style='border-radius:50%;' alt='mourad-ehm'/></a> <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Ecotax Management: in French context is a 'cost' added to the sale price of electrical or electronic appliances or furnishing items
[account_ecotax_report](account_ecotax_report/) | 16.0.1.0.0 | <a href='https://github.com/mourad-ehm'><img src='https://github.com/mourad-ehm.png' width='32' height='32' style='border-radius:50%;' alt='mourad-ehm'/></a> <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Ecotax Reporting add fields and view to anlysis ecotaxe
[account_ecotax_sale](account_ecotax_sale/) | 16.0.3.0.0 | <a href='https://github.com/mourad-ehm'><img src='https://github.com/mourad-ehm.png' width='32' height='32' style='border-radius:50%;' alt='mourad-ehm'/></a> <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Sale Ecotaxe
[account_ecotax_sale_tax](account_ecotax_sale_tax/) | 16.0.3.0.0 | <a href='https://github.com/mourad-ehm'><img src='https://github.com/mourad-ehm.png' width='32' height='32' style='border-radius:50%;' alt='mourad-ehm'/></a> <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Sale Ecotaxe managed as a tax
[account_ecotax_tax](account_ecotax_tax/) | 16.0.2.0.0 | <a href='https://github.com/mourad-ehm'><img src='https://github.com/mourad-ehm.png' width='32' height='32' style='border-radius:50%;' alt='mourad-ehm'/></a> <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Use Odoo tax mechanism to compute the ecotaxes
[account_fiscal_position_autodetect_optional_vies](account_fiscal_position_autodetect_optional_vies/) | 16.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Account Fiscal Position Autodetect optional VIES
[account_fiscal_position_partner_type](account_fiscal_position_partner_type/) | 16.0.1.0.2 |  | Account Fiscal Position Partner Type
[account_fiscal_position_type](account_fiscal_position_type/) | 16.0.1.0.4 |  | Add sale / purchase type on fiscal position
[account_product_fiscal_classification](account_product_fiscal_classification/) | 16.0.1.2.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Simplify taxes management for products
[l10n_eu_oss_oca](l10n_eu_oss_oca/) | 16.0.1.1.2 |  | L10n EU OSS OCA

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# account-invoice-reporting
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-invoice-reporting&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/account-invoice-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-invoice-reporting/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/account-invoice-reporting/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-invoice-reporting/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/account-invoice-reporting/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-invoice-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/account-invoice-reporting-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-invoice-reporting-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_comment_template](account_comment_template/) | 16.0.1.0.1 |  | Comments templates on invoice documents
[account_invoice_line_report](account_invoice_line_report/) | 16.0.1.0.0 |  | New view to manage invoice lines information
[account_invoice_production_lot](account_invoice_production_lot/) | 16.0.1.0.1 |  | Display delivered serial numbers in invoice
[account_invoice_report_due_list](account_invoice_report_due_list/) | 16.0.1.0.1 |  | Show multiple due data in invoice
[account_invoice_report_grouped_by_picking](account_invoice_report_grouped_by_picking/) | 16.0.1.1.9 |  | Print invoice lines grouped by picking
[account_invoice_report_header_repeater](account_invoice_report_header_repeater/) | 16.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Account Invoice Report Header Repeater
[account_invoice_report_lot_expiration_date](account_invoice_report_lot_expiration_date/) | 16.0.1.0.0 |  | This addon adds the batch expiration date to the invoice.
[account_invoice_report_payment_info](account_invoice_report_payment_info/) | 16.0.1.0.1 |  | Show payment extended info in invoice
[account_invoice_report_picking_customer_note](account_invoice_report_picking_customer_note/) | 16.0.1.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/Andrii9090'><img src='https://github.com/Andrii9090.png' width='32' height='32' style='border-radius:50%;' alt='Andrii9090'/></a> <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Print picking customer note in Invoice
[account_invoice_report_product_sticker](account_invoice_report_product_sticker/) | 16.0.1.0.4 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Display Product Stickers on Invoice Reports
[account_invoice_report_salesperson](account_invoice_report_salesperson/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Salesperson info in Invoice report
[account_reporting_volume](account_reporting_volume/) | 16.0.1.0.0 |  | Volume in the invoices analysis view
[account_reporting_weight](account_reporting_weight/) | 16.0.1.0.0 |  | Weights in the invoices analysis view
[partner_time_to_pay](partner_time_to_pay/) | 16.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Add receivables and payables statistics to partners
[stock_account_invoice_report_lot_expiry](stock_account_invoice_report_lot_expiry/) | 16.0.1.0.5 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Display expiry date in the lots table of the invoice report

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# account-invoicing
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-invoicing&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/account-invoicing/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-invoicing/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/account-invoicing/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-invoicing/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/account-invoicing/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-invoicing)
[![Translation Status](https://translation.odoo-community.org/widgets/account-invoicing-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-invoicing-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_billing](account_billing/) | 16.0.1.2.2 | <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Group invoice as billing before payment
[account_global_discount](account_global_discount/) | 16.0.2.0.0 |  | Account Global Discount
[account_invoice_alternate_payer](account_invoice_alternate_payer/) | 16.0.1.0.0 |  | Set a alternate payor/payee in invoices
[account_invoice_analytic_search](account_invoice_analytic_search/) | 16.0.1.0.0 |  | Search invoices by analytic account or by project manager
[account_invoice_block_payment](account_invoice_block_payment/) | 16.0.1.0.0 |  | Module to block payment of invoices
[account_invoice_blocking](account_invoice_blocking/) | 16.0.1.0.1 |  | Set a blocking (No Follow-up) flag on invoices
[account_invoice_change_currency](account_invoice_change_currency/) | 16.0.1.0.1 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> <a href='https://github.com/rolandojduartem'><img src='https://github.com/rolandojduartem.png' width='32' height='32' style='border-radius:50%;' alt='rolandojduartem'/></a> | Allows to change currency of Invoice by wizard
[account_invoice_check_picking_date](account_invoice_check_picking_date/) | 16.0.1.0.1 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> | Check if date of pickings match with accounting date
[account_invoice_check_total](account_invoice_check_total/) | 16.0.1.1.0 |  | Check if the verification total is equal to the bill's total
[account_invoice_clearing](account_invoice_clearing/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Account invoice clearing wizard
[account_invoice_crm_tag](account_invoice_crm_tag/) | 16.0.1.0.0 |  | Account Invoice CRM Tag
[account_invoice_currency_taxes](account_invoice_currency_taxes/) | 16.0.1.0.2 |  | Taxes in company currency in invoice report
[account_invoice_customer_no_autofollow](account_invoice_customer_no_autofollow/) | 16.0.1.0.1 |  | Do not add customer as follower in Invoices
[account_invoice_date_due](account_invoice_date_due/) | 16.0.1.0.1 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> <a href='https://github.com/joao-p-marques'><img src='https://github.com/joao-p-marques.png' width='32' height='32' style='border-radius:50%;' alt='joao-p-marques'/></a> | Update Invoice's Due Date
[account_invoice_default_code_column](account_invoice_default_code_column/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Display Default code product in a dedicated column on invoice reports
[account_invoice_discount_date](account_invoice_discount_date/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Set the early discount date on invoices
[account_invoice_discount_display_amount](account_invoice_discount_display_amount/) | 16.0.1.1.2 |  | Show total discount applied and total without discount on invoices.
[account_invoice_fiscal_position_update](account_invoice_fiscal_position_update/) | 16.0.1.0.2 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Changing the fiscal position of an invoice will auto-update invoice lines
[account_invoice_fixed_discount](account_invoice_fixed_discount/) | 16.0.3.0.0 |  | Allows to apply fixed amount discounts in invoices.
[account_invoice_fixed_triple_discount](account_invoice_fixed_triple_discount/) | 16.0.2.0.0 |  | Compatibility between fixed and triple discount modules
[account_invoice_force_number](account_invoice_force_number/) | 16.0.1.0.1 |  | Allows to force invoice numbering on specific invoices
[account_invoice_google_document_ai](account_invoice_google_document_ai/) | 16.0.1.0.0 |  | Allows to import data from document using Google Document AI
[account_invoice_line_default_account](account_invoice_line_default_account/) | 16.0.1.0.0 |  | Account Invoice Line Default Account
[account_invoice_mass_sending](account_invoice_mass_sending/) | 16.0.1.2.0 | <a href='https://github.com/jguenat'><img src='https://github.com/jguenat.png' width='32' height='32' style='border-radius:50%;' alt='jguenat'/></a> | This addon adds a mass sending feature on invoices.
[account_invoice_mass_sending_direct_print](account_invoice_mass_sending_direct_print/) | 16.0.1.0.0 |  | This addon adds a mass sending direct print feature on invoices.
[account_invoice_merge](account_invoice_merge/) | 16.0.1.0.1 |  | Merge invoices in draft
[account_invoice_merge_attachment](account_invoice_merge_attachment/) | 16.0.1.0.0 |  | Consider attachment during invoice merge process
[account_invoice_partner_reference](account_invoice_partner_reference/) | 16.0.1.0.0 |  | Add partner reference in the billing tree view.
[account_invoice_payment_retention](account_invoice_payment_retention/) | 16.0.1.0.0 |  | Account Invoice Payment Retention
[account_invoice_payment_term_date_due](account_invoice_payment_term_date_due/) | 16.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Display invoices date due when using payment terms
[account_invoice_pricelist](account_invoice_pricelist/) | 16.0.1.1.1 |  | Add partner pricelist on invoices
[account_invoice_pricelist_sale](account_invoice_pricelist_sale/) | 16.0.1.0.0 |  | Module to fill pricelist from sales order in invoice.
[account_invoice_recipient_bank_currency](account_invoice_recipient_bank_currency/) | 16.0.1.0.1 |  | Module to fill recipient bank from invoices by using the invoice's currency.
[account_invoice_refund_code](account_invoice_refund_code/) | 16.0.1.0.0 |  | This module allows to have specific refund codes.
[account_invoice_refund_line_selection](account_invoice_refund_line_selection/) | 16.0.1.0.0 |  | This module allows the user to refund specific lines in a invoice
[account_invoice_refund_link](account_invoice_refund_link/) | 16.0.1.0.5 |  | Show links between refunds and their originator invoices.
[account_invoice_refund_reason](account_invoice_refund_reason/) | 16.0.1.0.1 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Account Invoice Refund Reason.
[account_invoice_refund_reason_skip_anglo_saxon](account_invoice_refund_reason_skip_anglo_saxon/) | 16.0.1.0.0 | <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | Account Invoice Refund Reason.
[account_invoice_refund_reinvoice](account_invoice_refund_reinvoice/) | 16.0.1.0.0 |  | Allow to Reinvoice a Refund
[account_invoice_section_sale_order](account_invoice_section_sale_order/) | 16.0.1.2.0 |  | For invoices targetting multiple sale order addsections with sale order name.
[account_invoice_show_currency_rate](account_invoice_show_currency_rate/) | 16.0.1.0.8 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Show currency rate in invoices.
[account_invoice_supplier_ref_unique](account_invoice_supplier_ref_unique/) | 16.0.1.0.0 |  | Checks that supplier invoices are not entered twice
[account_invoice_supplier_self_invoice](account_invoice_supplier_self_invoice/) | 16.0.1.0.0 |  | Purchase Self Invoice
[account_invoice_supplierinfo_update](account_invoice_supplierinfo_update/) | 16.0.1.1.3 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | In the supplier invoice, automatically updates all products whose unit price on the line is different from the supplier price
[account_invoice_supplierinfo_update_discount](account_invoice_supplierinfo_update_discount/) | 16.0.2.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | In the supplier invoice, automatically update all products whose discount on the line is different from the supplier discount
[account_invoice_supplierinfo_update_qty_multiplier](account_invoice_supplierinfo_update_qty_multiplier/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | In the invoice Supplierinfo wizard, allow to change the Quantity Multiplier field
[account_invoice_supplierinfo_update_triple_discount](account_invoice_supplierinfo_update_triple_discount/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | In the supplier invoice, automatically update all products whose discounts on the line is different from the supplier discounts
[account_invoice_tax_note](account_invoice_tax_note/) | 16.0.1.0.2 |  | Print tax notes on customer invoices
[account_invoice_tax_required](account_invoice_tax_required/) | 16.0.1.1.1 |  | This module adds functional a check on invoice to force user to set tax on invoice line.
[account_invoice_transmit_method](account_invoice_transmit_method/) | 16.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Configure invoice transmit method (email, post, portal, ...)
[account_invoice_tree_currency](account_invoice_tree_currency/) | 16.0.1.0.0 |  | Show currencies in the invoice tree view
[account_invoice_triple_discount](account_invoice_triple_discount/) | 16.0.5.0.0 |  | Manage triple discount on invoice lines
[account_invoice_uom_column](account_invoice_uom_column/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Display UoM invoice line in a dedicated column on invoice reports
[account_invoice_validation_queued](account_invoice_validation_queued/) | 16.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Enqueue account invoice validation
[account_invoice_view_payment](account_invoice_view_payment/) | 16.0.1.0.0 |  | Access to the payment from an invoice
[account_invoice_warn_message](account_invoice_warn_message/) | 16.0.1.0.0 |  | Add a popup warning on invoice to ensure warning is populated
[account_mail_autosubscribe](account_mail_autosubscribe/) | 16.0.1.0.1 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Automatically subscribe partners to their company's invoices
[account_menu_invoice_refund](account_menu_invoice_refund/) | 16.0.1.0.1 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | New invoice menu that combine invoices and refunds
[account_move_auto_post_ref](account_move_auto_post_ref/) | 16.0.1.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Propagate customer ref when auto-generating next recurring invoice
[account_move_cancel_confirm](account_move_cancel_confirm/) | 16.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Account Move Cancel Confirm
[account_move_line_packaging](account_move_line_packaging/) | 16.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Add packaging to invoice lines
[account_move_line_purchase_packaging](account_move_line_purchase_packaging/) | 16.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Purchase packaging support on invoice lines
[account_move_original_partner](account_move_original_partner/) | 16.0.1.0.0 |  | Display original customers when creating invoices from multiple sale orders.
[account_move_sent_usability](account_move_sent_usability/) | 16.0.1.1.0 |  | Allows to filter moves on 'is_move_sent' and to see the value of the field in form
[account_move_substate](account_move_substate/) | 16.0.1.0.1 |  | Account Move Sub State
[account_move_tier_validation](account_move_tier_validation/) | 16.0.1.1.0 |  | Extends the functionality of Account Moves to support a tier validation process.
[account_receipt_journal](account_receipt_journal/) | 16.0.1.1.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> <a href='https://github.com/anddago78'><img src='https://github.com/anddago78.png' width='32' height='32' style='border-radius:50%;' alt='anddago78'/></a> | Define and use journals dedicated to receipts
[account_receipt_send](account_receipt_send/) | 16.0.1.0.2 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Send receipts
[account_tax_change](account_tax_change/) | 16.0.1.0.3 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Configure your tax changes starting from a date.
[account_tax_group_widget_base_amount](account_tax_group_widget_base_amount/) | 16.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Adds base amount to tax group widget
[account_tax_one_vat](account_tax_one_vat/) | 16.0.1.0.0 |  | Allow only the selection of one VAT Tax.
[account_tax_one_vat_purchase](account_tax_one_vat_purchase/) | 16.0.1.0.0 |  | Allow only the selection of one VAT Tax in purchase order line
[account_tax_one_vat_sale](account_tax_one_vat_sale/) | 16.0.1.0.0 |  | Allow only the selection of one VAT Tax in purchase order line
[partner_invoicing_mode](partner_invoicing_mode/) | 16.0.2.0.1 |  | Base module for handling multiple partner invoicing mode
[partner_invoicing_mode_at_shipping](partner_invoicing_mode_at_shipping/) | 16.0.1.2.0 |  | Create invoices automatically when goods are shipped.
[partner_invoicing_mode_cash_on_delivery](partner_invoicing_mode_cash_on_delivery/) | 16.0.1.0.0 |  | This module allows users to distinguish cash on delivery invoices in the automatic invoicing flow
[partner_invoicing_mode_monthly](partner_invoicing_mode_monthly/) | 16.0.2.0.0 |  | Create invoices automatically on a monthly basis.
[partner_last_invoice_date](partner_last_invoice_date/) | 16.0.1.0.1 |  | Add Last Invoice Date to Partners.
[portal_account_personal_data_only](portal_account_personal_data_only/) | 16.0.1.0.0 |  | Portal Accounting Personal Data Only
[product_form_account_move_line_link](product_form_account_move_line_link/) | 16.0.1.0.0 |  | Adds a button on product forms to access Journal Items
[product_supplierinfo_for_customer_invoice](product_supplierinfo_for_customer_invoice/) | 16.0.1.0.0 |  | Based on product_customer_code, this module loads in every account invoice the customer code defined in the product
[purchase_invoicing_no_zero_line](purchase_invoicing_no_zero_line/) | 16.0.1.0.1 |  | Avoid creation of zero quantity invoice lines from purchase
[purchase_stock_picking_return_invoicing](purchase_stock_picking_return_invoicing/) | 16.0.1.0.2 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/MiquelRForgeFlow'><img src='https://github.com/MiquelRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='MiquelRForgeFlow'/></a> | Add an option to refund returned pickings
[sale_credit_note_reversal](sale_credit_note_reversal/) | 16.0.1.0.0 |  | Allow to revert a credit note
[sale_invoice_date_from_picking](sale_invoice_date_from_picking/) | 16.0.1.0.0 |  | Sale Invoice Date From Picking
[sale_invoicing_date_from_picking](sale_invoicing_date_from_picking/) | 16.0.1.0.0 |  | Applies the wizard date to invoices generated from pickings
[sale_invoicing_date_selection](sale_invoicing_date_selection/) | 16.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Set date invoice when you create invoices
[sale_line_refund_to_invoice_qty](sale_line_refund_to_invoice_qty/) | 16.0.1.0.0 |  | Allow deciding whether refunded quantity should be considered as quantity to reinvoice
[sale_line_refund_to_invoice_qty_skip_anglo_saxon](sale_line_refund_to_invoice_qty_skip_anglo_saxon/) | 16.0.1.0.0 | <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | Sale Line Refund To Invoice Qty skip anglo saxon.
[sale_order_invoicing_grouping_criteria](sale_order_invoicing_grouping_criteria/) | 16.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Sales order invoicing grouping criteria
[sale_order_invoicing_qty_percentage](sale_order_invoicing_qty_percentage/) | 16.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Sales order invoicing by percentage of the quantity
[sale_order_invoicing_queued](sale_order_invoicing_queued/) | 16.0.1.0.0 |  | Enqueue sales order invoicing
[sale_stock_picking_invoicing](sale_stock_picking_invoicing/) | 16.0.1.0.1 | <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Sales Stock Picking Invocing
[sale_timesheet_invoice_description](sale_timesheet_invoice_description/) | 16.0.1.0.1 |  | Add timesheet details in invoice line
[stock_account_move_reset_to_draft](stock_account_move_reset_to_draft/) | 16.0.1.0.3 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Stock account move reset to draft
[stock_picking_invoicing](stock_picking_invoicing/) | 16.0.1.0.4 |  | Stock Picking Invoicing
[stock_picking_return_refund_option](stock_picking_return_refund_option/) | 16.0.1.0.2 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Update the refund options in pickings

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# account-payment
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-payment&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/account-payment/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-payment/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/account-payment/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-payment/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/account-payment/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-payment)
[![Translation Status](https://translation.odoo-community.org/widgets/account-payment-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-payment-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Account Payment

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_cash_invoice](account_cash_invoice/) | 16.0.1.0.4 |  | Pay and receive invoices from bank statements
[account_check_printing_report_base](account_check_printing_report_base/) | 16.0.1.0.0 |  | Account Check Printing Report Base
[account_due_list](account_due_list/) | 16.0.1.2.1 |  | List of open credits and debits, with due date
[account_due_list_aging_comment](account_due_list_aging_comment/) | 16.0.1.0.0 |  | Account Due List Aging Comment
[account_due_list_days_overdue](account_due_list_days_overdue/) | 16.0.1.0.0 |  | Payments Due list days overdue
[account_due_list_payment_mode](account_due_list_payment_mode/) | 16.0.1.0.0 |  | Payment Due List Payment Mode
[account_move_line_payment](account_move_line_payment/) | 16.0.1.0.0 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Register only due payments
[account_payment_batch_process](account_payment_batch_process/) | 16.0.1.0.1 |  | Account Batch Payments Processing for Customers Invoices and Supplier Invoices
[account_payment_batch_process_discount](account_payment_batch_process_discount/) | 16.0.1.0.0 | <a href='https://github.com/mgosai'><img src='https://github.com/mgosai.png' width='32' height='32' style='border-radius:50%;' alt='mgosai'/></a> | Discount on batch payments
[account_payment_credit_card](account_payment_credit_card/) | 16.0.1.0.1 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Add support for credit card payments
[account_payment_line](account_payment_line/) | 16.0.1.0.1 | <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | Payment Counterpart Lines
[account_payment_line_import](account_payment_line_import/) | 16.0.1.0.0 | <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | Payment Counterpart Lines Import XLSX
[account_payment_multi_deduction](account_payment_multi_deduction/) | 16.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Payment Register with Multiple Deduction
[account_payment_notification](account_payment_notification/) | 16.0.1.0.1 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Notifiy upcoming payments
[account_payment_promissory_note](account_payment_promissory_note/) | 16.0.1.0.1 |  | Account Payment Promissory Note
[account_payment_return](account_payment_return/) | 16.0.1.2.4 |  | Manage the return of your payments
[account_payment_return_import](account_payment_return_import/) | 16.0.1.0.2 |  | This module adds a generic wizard to import payment returnfile formats. Is only the base to be extended by anothermodules
[account_payment_return_import_iso20022](account_payment_return_import_iso20022/) | 16.0.1.0.3 |  | This addon allows to import payment returns from ISO 20022 files like PAIN or CAMT.
[account_payment_term_discount](account_payment_term_discount/) | 16.0.1.1.0 | <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> | Account Payment Terms Discount
[account_payment_term_extension](account_payment_term_extension/) | 16.0.1.0.4 |  | Adds rounding, months, weeks and multiple payment days properties on payment term lines
[account_payment_term_partner_holiday](account_payment_term_partner_holiday/) | 16.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Account Payment Term Partner Holiday
[account_payment_term_restriction](account_payment_term_restriction/) | 16.0.1.0.0 |  | Restricts the usage of Payment Terms Journal Entries
[account_payment_term_restriction_purchase](account_payment_term_restriction_purchase/) | 16.0.1.0.0 |  | Restricts the usage of Payment Terms on POs
[account_payment_term_restriction_sale](account_payment_term_restriction_sale/) | 16.0.1.0.0 |  | Restricts the usage of Payment Terms on SOs
[account_payment_widget_amount](account_payment_widget_amount/) | 16.0.1.0.0 | <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | Extends the payment widget to be able to choose the payment amount
[partner_aging](partner_aging/) | 16.0.1.0.0 | <a href='https://github.com/Urvisha-OSI'><img src='https://github.com/Urvisha-OSI.png' width='32' height='32' style='border-radius:50%;' alt='Urvisha-OSI'/></a> | Aging as a view - invoices and credits
[payment_partner](payment_partner/) | 16.0.1.0.0 |  | Filter Payments by Partner

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# account-reconcile
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/account-reconcile&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/account-reconcile/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-reconcile/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/account-reconcile/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/account-reconcile/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/account-reconcile/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/account-reconcile)
[![Translation Status](https://translation.odoo-community.org/widgets/account-reconcile-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/account-reconcile-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_in_payment](account_in_payment/) | 16.0.1.0.0 |  | This module enables in-payment mode for your accounting
[account_mass_reconcile](account_mass_reconcile/) | 16.0.1.1.3 |  | Account Mass Reconcile
[account_move_base_import](account_move_base_import/) | 16.0.1.0.2 |  | Journal Entry base import
[account_move_line_reconcile_manual](account_move_line_reconcile_manual/) | 16.0.2.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Manually reconcile Journal Items
[account_move_reconcile_forbid_cancel](account_move_reconcile_forbid_cancel/) | 16.0.1.0.1 |  | Account Move Reconcile Forbid Cancel
[account_move_reconcile_helper](account_move_reconcile_helper/) | 16.0.1.0.0 |  | Provides tools to facilitate reconciliation
[account_move_so_import](account_move_so_import/) | 16.0.1.0.0 |  | Journal Entry Sale Order completion
[account_partner_reconcile](account_partner_reconcile/) | 16.0.1.0.0 |  | Account Partner Reconcile
[account_reconcile_analytic_tag](account_reconcile_analytic_tag/) | 16.0.1.2.2 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Analytic tags in account reconciliation
[account_reconcile_match_regex](account_reconcile_match_regex/) | 16.0.1.0.0 |  | Use a regex to find invoice name in matching
[account_reconcile_oca](account_reconcile_oca/) | 16.0.2.5.1 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Reconcile addons for Odoo CE accounting
[account_reconcile_oca_add_default_filters](account_reconcile_oca_add_default_filters/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add default filters in Reconcile tab when the bank statement line has a partner
[account_statement_base](account_statement_base/) | 16.0.1.15.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Base module for Bank Statements
[bank_statement_check_number](bank_statement_check_number/) | 16.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Add the check number in the bank statements
[base_transaction_id](base_transaction_id/) | 16.0.1.0.0 |  | Base transaction ID for financial institutes

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/agreement&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/agreement/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/agreement/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/agreement/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/agreement/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/agreement/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/agreement)
[![Translation Status](https://translation.odoo-community.org/widgets/agreement-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/agreement-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Agreements modules

None

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[agreement](agreement/) | 16.0.1.0.0 | <a href='https://github.com/ygol'><img src='https://github.com/ygol.png' width='32' height='32' style='border-radius:50%;' alt='ygol'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adds an agreement object
[agreement_legal](agreement_legal/) | 16.0.2.0.4 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/ygol'><img src='https://github.com/ygol.png' width='32' height='32' style='border-radius:50%;' alt='ygol'/></a> | Manage Agreements, LOI and Contracts
[agreement_maintenance](agreement_maintenance/) | 16.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Manage maintenance agreements and contracts
[agreement_rebate](agreement_rebate/) | 16.0.1.0.4 |  | Rebate in agreements
[agreement_sale](agreement_sale/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Agreement on sales
[agreement_serviceprofile](agreement_serviceprofile/) | 16.0.1.0.1 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Adds an Agreement Service Profile object

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/ai&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/ai/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/ai/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/ai/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/ai/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/ai/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/ai)
[![Translation Status](https://translation.odoo-community.org/widgets/ai-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/ai-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

ai

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[ai_automation](ai_automation/) | 16.0.1.0.1 |  | Integrate `ai_tools` with server actions to automate tasks using AI.
[ai_oca_bridge](ai_oca_bridge/) | 16.0.3.0.1 |  | Makes a basic configuration to be used as bridge with external AI systems
[ai_oca_bridge_chatter](ai_oca_bridge_chatter/) | 16.0.1.0.1 |  | Integrate a Bridge with a user that will use it on chatter
[ai_oca_bridge_crm_lead](ai_oca_bridge_crm_lead/) | 16.0.2.0.0 |  | Adds CRM Lead triggers for AI Bridges
[ai_oca_bridge_document_page](ai_oca_bridge_document_page/) | 16.0.2.0.0 |  | Adds Documents synchronization using AI Bridges
[ai_oca_bridge_extra_parameters](ai_oca_bridge_extra_parameters/) | 16.0.1.0.1 | <a href='https://github.com/arielbarreiros96'><img src='https://github.com/arielbarreiros96.png' width='32' height='32' style='border-radius:50%;' alt='arielbarreiros96'/></a> | Adds extra parameters to the AI OCA Bridge payload.
[ai_oca_bridge_fieldservice](ai_oca_bridge_fieldservice/) | 16.0.2.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Integrate AI Bridge with Field Service
[ai_oca_bridge_helpdesk_mgmt](ai_oca_bridge_helpdesk_mgmt/) | 16.0.1.0.0 |  | Integrate AI Bridge with Helpdesk Management
[ai_oca_bridge_mrp](ai_oca_bridge_mrp/) | 16.0.2.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Adds MRP triggers for AI Bridges
[ai_oca_mcp](ai_oca_mcp/) | 16.0.1.0.0 |  | MCP Interface for Odoo
[ai_tool](ai_tool/) | 16.0.1.0.1 |  | We want to generate some specific AI Tools that might be used in other places, like MCP or native.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/automation&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/automation/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/automation/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/automation/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/automation/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/automation/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/automation)
[![Translation Status](https://translation.odoo-community.org/widgets/automation-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/automation-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

automation

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[automation_oca](automation_oca/) | 16.0.1.6.2 |  | Automate actions in threaded models

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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

[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# bank-payment
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/bank-payment&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/bank-payment/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/bank-payment/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/bank-payment/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/bank-payment/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/bank-payment/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/bank-payment)
[![Translation Status](https://translation.odoo-community.org/widgets/bank-payment-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/bank-payment-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Banking payment addons for Odoo.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_banking_mandate](account_banking_mandate/) | 16.0.1.3.5 |  | Banking mandates
[account_banking_mandate_contact](account_banking_mandate_contact/) | 16.0.1.1.0 |  | Assign specific banking mandates in contact level
[account_banking_mandate_sale](account_banking_mandate_sale/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adds mandates on sale orders
[account_banking_mandate_sale_contact](account_banking_mandate_sale_contact/) | 16.0.1.0.1 | <a href='https://github.com/tisho99'><img src='https://github.com/tisho99.png' width='32' height='32' style='border-radius:50%;' alt='tisho99'/></a> | Add a specific contact mandate to sale orders
[account_banking_pain_base](account_banking_pain_base/) | 16.0.1.2.4 |  | Base module for PAIN file generation
[account_banking_sepa_credit_transfer](account_banking_sepa_credit_transfer/) | 16.0.1.2.1 |  | Create SEPA XML files for Credit Transfers
[account_banking_sepa_direct_debit](account_banking_sepa_direct_debit/) | 16.0.1.4.6 |  | Create SEPA files for Direct Debit
[account_payment_method_fs_storage](account_payment_method_fs_storage/) | 16.0.1.0.3 |  | Add the possibility to specify on the payment method, a storage where files generated will be pushed to upon payment
[account_payment_mode](account_payment_mode/) | 16.0.2.0.0 |  | Account Payment Mode
[account_payment_order](account_payment_order/) | 16.0.1.14.0 |  | Account Payment Order
[account_payment_order_grouped_output](account_payment_order_grouped_output/) | 16.0.1.0.4 |  | Account Payment Order - Generate grouped moves
[account_payment_order_notification](account_payment_order_notification/) | 16.0.1.0.3 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Account Payment Order Notification
[account_payment_order_return](account_payment_order_return/) | 16.0.1.0.1 |  | Account Payment Order Return
[account_payment_order_tier_validation](account_payment_order_tier_validation/) | 16.0.1.1.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Extends the functionality of Payment Orders to support a tier validation process.
[account_payment_order_vendor_email](account_payment_order_vendor_email/) | 16.0.1.0.1 | <a href='https://github.com/ursais'><img src='https://github.com/ursais.png' width='32' height='32' style='border-radius:50%;' alt='ursais'/></a> | Account Payment Order Email
[account_payment_partner](account_payment_partner/) | 16.0.1.2.9 |  | Adds payment mode on partners and invoices
[account_payment_purchase](account_payment_purchase/) | 16.0.2.0.6 |  | Adds Bank Account and Payment Mode on Purchase Orders
[account_payment_purchase_stock](account_payment_purchase_stock/) | 16.0.1.0.1 |  | Integrate Account Payment Purchase with Stock
[account_payment_sale](account_payment_sale/) | 16.0.1.0.7 |  | Adds payment mode on sale orders

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# OCA bank statement import modules for Odoo
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/bank-statement-import&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/bank-statement-import/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/bank-statement-import/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/bank-statement-import/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/bank-statement-import/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/bank-statement-import/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/bank-statement-import)
[![Translation Status](https://translation.odoo-community.org/widgets/bank-statement-import-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/bank-statement-import-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

This repository hosts additionnal parsers and import features for bank statements.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_journal_dashboard_statement_button](account_journal_dashboard_statement_button/) | 16.0.1.0.0 |  | This module enhances the Account Journal Dashboard by introducing a shortcut button in the Bank and Cash journals. The button provides a direct link to the Bank Statements view.
[account_statement_import_base](account_statement_import_base/) | 16.0.1.0.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Base module for Bank Statement Import
[account_statement_import_camt](account_statement_import_camt/) | 16.0.1.0.3 |  | CAMT Format Bank Statements Import
[account_statement_import_camt54](account_statement_import_camt54/) | 16.0.1.0.0 |  | Bank Account Camt54 Import
[account_statement_import_file](account_statement_import_file/) | 16.0.1.1.3 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Import Statement Files
[account_statement_import_file_reconcile_oca](account_statement_import_file_reconcile_oca/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import Statement Files and Go Direct to Reconciliation
[account_statement_import_ofx](account_statement_import_ofx/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import OFX Bank Statement
[account_statement_import_ofx_by_acctid](account_statement_import_ofx_by_acctid/) | 16.0.1.0.0 |  | Import OFX Bank Statement by ACCTID
[account_statement_import_online](account_statement_import_online/) | 16.0.1.4.3 | <a href='https://github.com/alexey-pelykh'><img src='https://github.com/alexey-pelykh.png' width='32' height='32' style='border-radius:50%;' alt='alexey-pelykh'/></a> | Online bank statements update
[account_statement_import_online_gocardless](account_statement_import_online_gocardless/) | 16.0.1.2.10 |  | Online Bank Statements: GoCardless
[account_statement_import_online_ofx](account_statement_import_online_ofx/) | 16.0.1.0.0 |  | Online bank statements for OFX
[account_statement_import_online_paypal](account_statement_import_online_paypal/) | 16.0.1.0.3 | <a href='https://github.com/alexey-pelykh'><img src='https://github.com/alexey-pelykh.png' width='32' height='32' style='border-radius:50%;' alt='alexey-pelykh'/></a> | Online bank statements for PayPal.com
[account_statement_import_online_plaid](account_statement_import_online_plaid/) | 16.0.1.0.0 |  | Online Bank Statements: plaid.com
[account_statement_import_online_ponto](account_statement_import_online_ponto/) | 16.0.1.1.3 |  | Online Bank Statements: MyPonto.com
[account_statement_import_online_qonto](account_statement_import_online_qonto/) | 16.0.2.0.0 |  | Online Bank Statements: Qonto
[account_statement_import_qif](account_statement_import_qif/) | 16.0.1.0.0 |  | Import QIF Bank Statements
[account_statement_import_sheet_file](account_statement_import_sheet_file/) | 16.0.1.3.1 | <a href='https://github.com/alexey-pelykh'><img src='https://github.com/alexey-pelykh.png' width='32' height='32' style='border-radius:50%;' alt='alexey-pelykh'/></a> | Import TXT/CSV or XLSX files as Bank Statements in Odoo

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# brand
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/brand&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/brand/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/brand/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/brand/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/brand/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/brand/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/brand)
[![Translation Status](https://translation.odoo-community.org/widgets/brand-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/brand-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Manage brands for products and companies 

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_brand](account_brand/) | 16.0.1.0.0 | <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Send branded invoices and refunds
[analytic_brand](analytic_brand/) | 16.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This addon associate an analytic distribution to a brand that will be used as a default value where the brand is used if the analytic accounting is activated
[brand](brand/) | 16.0.1.0.2 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This is a base addon for brand modules. It adds the brand object and its menu and define an abstract model to be inherited from branded objects
[brand_external_report_layout](brand_external_report_layout/) | 16.0.1.0.3 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This module allows you to have a different layout by brand for your external reports.
[partner_brand](partner_brand/) | 16.0.1.0.0 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Define registered mark in partners according to brand settings
[product_brand](product_brand/) | 16.0.1.0.4 |  | Product Brand Manager
[product_brand_mrp](product_brand_mrp/) | 16.0.1.0.0 |  | This module allows to work with product_brand in MRP.
[product_brand_purchase](product_brand_purchase/) | 16.0.1.0.0 |  | This module allows to work with product_brand in purchase reports.
[product_brand_stock](product_brand_stock/) | 16.0.1.0.0 |  | This module allows to work with product_brand in Stock.
[product_brand_stock_account](product_brand_stock_account/) | 16.0.1.0.0 |  | This module allows to work with product_brand in Stock Account.
[product_brand_tag](product_brand_tag/) | 16.0.1.0.0 |  | Add tags to product brand
[sale_brand](sale_brand/) | 16.0.1.0.1 | <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Send branded sales orders
[stock_brand](stock_brand/) | 16.0.1.0.0 |  | Manage brands on stock picking documents

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/business-requirement


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/business-requirement&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/business-requirement/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/business-requirement/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/business-requirement/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/business-requirement/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/business-requirement/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/business-requirement)
[![Translation Status](https://translation.odoo-community.org/widgets/business-requirement-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/business-requirement-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# business-requirement

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[business_requirement](business_requirement/) | 16.0.1.0.1 |  | Manage the Business Requirements (stories, scenarios, gaps and test cases) for your customers
[business_requirement_crm](business_requirement_crm/) | 16.0.1.0.1 |  | Convert Leads to Business Requirement

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/calendar&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/calendar/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/calendar/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/calendar/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/calendar/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/calendar/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/calendar)
[![Translation Status](https://translation.odoo-community.org/widgets/calendar-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/calendar-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[calendar_event_link_base](calendar_event_link_base/) | 16.0.1.0.0 |  | This module add an abstract model that provide an action to link any model to calendar events
[calendar_event_type_color](calendar_event_type_color/) | 16.0.1.0.0 | <a href='https://github.com/yankinmax'><img src='https://github.com/yankinmax.png' width='32' height='32' style='border-radius:50%;' alt='yankinmax'/></a> | Colorize calendar view depending on event type color
[calendar_monthly_multi](calendar_monthly_multi/) | 16.0.1.0.0 |  | Calendar Monthly Extension
[microsoft_calendar_filter](microsoft_calendar_filter/) | 16.0.1.0.0 | <a href='https://github.com/NL66278'><img src='https://github.com/NL66278.png' width='32' height='32' style='border-radius:50%;' alt='NL66278'/></a> | Limit the records that are synchronized from Outlook to Odoo
[resource_booking](resource_booking/) | 16.0.1.5.3 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/ows-cloud'><img src='https://github.com/ows-cloud.png' width='32' height='32' style='border-radius:50%;' alt='ows-cloud'/></a> | Manage appointments and resource booking

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# commission
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/commission&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/commission/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/commission/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/commission/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/commission/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/commission/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/commission)
[![Translation Status](https://translation.odoo-community.org/widgets/commission-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/commission-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_commission](account_commission/) | 16.0.2.5.2 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Account commissions
[commission](commission/) | 16.0.2.4.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Commissions
[commission_delegated_partner](commission_delegated_partner/) | 16.0.1.0.1 |  | Allow to delegate the invoices of agent to a delegate partner
[commission_formula](commission_formula/) | 16.0.1.0.0 |  | Commissions computed by formulas
[hr_commission](hr_commission/) | 16.0.1.0.0 |  | HR commissions
[sale_commission](sale_commission/) | 16.0.1.0.3 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Sales commissions
[sale_commission_agent_restrict](sale_commission_agent_restrict/) | 16.0.1.0.0 | <a href='https://github.com/aleuffre'><img src='https://github.com/aleuffre.png' width='32' height='32' style='border-radius:50%;' alt='aleuffre'/></a> | Sales Commissions Agent Restrict
[sale_commission_margin](sale_commission_margin/) | 16.0.1.0.0 |  | This addons allows commissions to be deducted from the margin.
[sale_commission_product_criteria](sale_commission_product_criteria/) | 16.0.2.0.0 | <a href='https://github.com/ilyasProgrammer'><img src='https://github.com/ilyasProgrammer.png' width='32' height='32' style='border-radius:50%;' alt='ilyasProgrammer'/></a> | Advanced commissions rules
[sale_commission_product_criteria_country](sale_commission_product_criteria_country/) | 16.0.1.0.0 | <a href='https://github.com/tisho99'><img src='https://github.com/tisho99.png' width='32' height='32' style='border-radius:50%;' alt='tisho99'/></a> | Sale Commission Product Criteria Country
[sale_commission_product_criteria_discount](sale_commission_product_criteria_discount/) | 16.0.1.0.1 | <a href='https://github.com/aleuffre'><img src='https://github.com/aleuffre.png' width='32' height='32' style='border-radius:50%;' alt='aleuffre'/></a> <a href='https://github.com/ilyasProgrammer'><img src='https://github.com/ilyasProgrammer.png' width='32' height='32' style='border-radius:50%;' alt='ilyasProgrammer'/></a> <a href='https://github.com/renda-dev'><img src='https://github.com/renda-dev.png' width='32' height='32' style='border-radius:50%;' alt='renda-dev'/></a> <a href='https://github.com/PicchiSeba'><img src='https://github.com/PicchiSeba.png' width='32' height='32' style='border-radius:50%;' alt='PicchiSeba'/></a> | Advanced commissions rules with discount
[sale_commission_product_criteria_domain](sale_commission_product_criteria_domain/) | 16.0.1.0.3 | <a href='https://github.com/ilyasProgrammer'><img src='https://github.com/ilyasProgrammer.png' width='32' height='32' style='border-radius:50%;' alt='ilyasProgrammer'/></a> | Sale Commission Product Criteria Domain
[sale_commission_product_criteria_fiscal_position_type](sale_commission_product_criteria_fiscal_position_type/) | 16.0.1.0.0 | <a href='https://github.com/tisho99'><img src='https://github.com/tisho99.png' width='32' height='32' style='border-radius:50%;' alt='tisho99'/></a> | Sale Commission Product Criteria Fiscal Position Type
[sale_commission_salesman](sale_commission_salesman/) | 16.0.1.0.1 |  | Sales commissions from salesman

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# community-data-files
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/community-data-files&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/community-data-files/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/community-data-files/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/community-data-files/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/community-data-files/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/community-data-files/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/community-data-files)
[![Translation Status](https://translation.odoo-community.org/widgets/community-data-files-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/community-data-files-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_payment_unece](account_payment_unece/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | UNECE nomenclature for the payment methods
[account_tax_unece](account_tax_unece/) | 16.0.2.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | UNECE nomenclature for taxes
[base_bank_from_iban](base_bank_from_iban/) | 16.0.2.0.4 |  | Bank from IBAN
[base_currency_iso_4217](base_currency_iso_4217/) | 16.0.1.0.0 |  | Adds numeric code and full name to currencies, following the ISO 4217 specification
[base_iso3166](base_iso3166/) | 16.0.1.0.1 |  | ISO 3166
[base_unece](base_unece/) | 16.0.1.1.0 | <a href='https://github.com/astirpe'><img src='https://github.com/astirpe.png' width='32' height='32' style='border-radius:50%;' alt='astirpe'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Base module for UNECE code lists
[company_sanitary_registry](company_sanitary_registry/) | 16.0.1.2.0 |  | Sanitary Registry
[l10n_eu_nace](l10n_eu_nace/) | 16.0.1.1.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | European NACE partner categories
[product_fao_fishing](product_fao_fishing/) | 16.0.1.0.1 |  | Set fishing areas and capture technology
[product_packaging_unece](product_packaging_unece/) | 16.0.1.1.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | UNECE nomenclature for product packaging
[uom_unece](uom_unece/) | 16.0.1.3.1 | <a href='https://github.com/astirpe'><img src='https://github.com/astirpe.png' width='32' height='32' style='border-radius:50%;' alt='astirpe'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | UNECE nomenclature for the units of measure

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/connector&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/connector/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/connector/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/connector/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/connector/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/connector/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/connector)
[![Translation Status](https://translation.odoo-community.org/widgets/connector-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/connector-16-0/?utm_source=widget)

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
[component](component/) | 16.0.1.1.1 | <a href='https://github.com/guewen'><img src='https://github.com/guewen.png' width='32' height='32' style='border-radius:50%;' alt='guewen'/></a> | Add capabilities to register and use decoupled components, as an alternative to model classes
[component_event](component_event/) | 16.0.1.0.1 |  | Components Events
[connector](connector/) | 16.0.1.0.1 |  | Connector
[connector_base_product](connector_base_product/) | 16.0.1.0.0 |  | Connector Base Product
[test_component](test_component/) | 16.0.1.0.0 | <a href='https://github.com/guewen'><img src='https://github.com/guewen.png' width='32' height='32' style='border-radius:50%;' alt='guewen'/></a> | Automated tests for Components, do not install.
[test_connector](test_connector/) | 16.0.1.0.0 |  | Automated tests for Connector, do not install.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/connector-cmis


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/connector-cmis&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/connector-cmis/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/connector-cmis/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/connector-cmis/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/connector-cmis/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/connector-cmis/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/connector-cmis)
[![Translation Status](https://translation.odoo-community.org/widgets/connector-cmis-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/connector-cmis-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# connector-cmis

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[cmis](cmis/) | 16.0.1.0.1 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Connect Odoo with a CMIS server

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/connector-ecommerce


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/connector-ecommerce&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/connector-ecommerce/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/connector-ecommerce/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/connector-ecommerce/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/connector-ecommerce/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/connector-ecommerce/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/connector-ecommerce)
[![Translation Status](https://translation.odoo-community.org/widgets/connector-ecommerce-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/connector-ecommerce-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# connector-ecommerce

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[connector_ecommerce](connector_ecommerce/) | 16.0.1.0.0 |  | Connector for E-Commerce

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# connector-interfaces
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/connector-interfaces&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/connector-interfaces/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/connector-interfaces/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/connector-interfaces/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/connector-interfaces/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/connector-interfaces/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/connector-interfaces)
[![Translation Status](https://translation.odoo-community.org/widgets/connector-interfaces-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/connector-interfaces-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[connector_importer](connector_importer/) | 16.0.1.2.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | This module takes care of import sessions.
[connector_importer_product](connector_importer_product/) | 16.0.1.0.0 |  | Ease definition of product imports using `connector_importer`.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/connector-telephony&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/connector-telephony/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/connector-telephony/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/connector-telephony/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/connector-telephony/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/connector-telephony/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/connector-telephony)
[![Translation Status](https://translation.odoo-community.org/widgets/connector-telephony-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/connector-telephony-16-0/?utm_source=widget)

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
[asterisk_click2dial](asterisk_click2dial/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Asterisk-Odoo connector
[base_phone](base_phone/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Validate phone numbers
[hr_phone](hr_phone/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Validate phone numbers in HR
[hr_recruitment_phone](hr_recruitment_phone/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Validate phone numbers in HR Recruitment
[sms_alternative_provider](sms_alternative_provider/) | 16.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Base module for implementing alternative SMS gateways
[sms_dummy_provider](sms_dummy_provider/) | 16.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Send SMS via messagebird.com
[sms_messagebird](sms_messagebird/) | 16.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Send SMS via messagebird.com
[sms_no_automatic_delete](sms_no_automatic_delete/) | 16.0.1.0.0 |  | Avoid automatic delete of sended sms
[sms_ovh_http](sms_ovh_http/) | 16.0.1.0.0 | <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> | Send sms using ovh http API
[sms_twilio](sms_twilio/) | 16.0.1.0.0 | <a href='https://github.com/mariadforgeflow'><img src='https://github.com/mariadforgeflow.png' width='32' height='32' style='border-radius:50%;' alt='mariadforgeflow'/></a> | Send sms using Twilio API

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/contract&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/contract/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/contract/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/contract/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/contract/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/contract/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/contract)
[![Translation Status](https://translation.odoo-community.org/widgets/contract-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/contract-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[agreement_rebate_partner_company_group](agreement_rebate_partner_company_group/) | 16.0.1.0.0 |  | Rebate agreements applied to all company group members
[contract](contract/) | 16.0.2.15.0 |  | Recurring - Contracts Management
[contract_analytic_tag](contract_analytic_tag/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Contract Analytic Tag
[contract_forecast](contract_forecast/) | 16.0.1.1.0 |  | Contract forecast
[contract_invoice_start_end_dates](contract_invoice_start_end_dates/) | 16.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Contract Invoice Start End Dates
[contract_mandate](contract_mandate/) | 16.0.1.0.0 |  | Mandate in contracts and their invoices
[contract_payment_auto](contract_payment_auto/) | 16.0.1.0.1 |  | Adds automatic payments to contracts.
[contract_payment_mode](contract_payment_mode/) | 16.0.1.0.1 |  | Payment mode in contracts and their invoices
[contract_queue_job](contract_queue_job/) | 16.0.1.0.1 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> <a href='https://github.com/BurkhalterY'><img src='https://github.com/BurkhalterY.png' width='32' height='32' style='border-radius:50%;' alt='BurkhalterY'/></a> | This addon make contract invoicing cron plan each contract in a job instead of creating all invoices in one transaction
[contract_sale](contract_sale/) | 16.0.1.2.0 |  | Contract from Sale
[contract_sale_generation](contract_sale_generation/) | 16.0.1.2.0 |  | Contracts Management - Recurring Sales
[contract_sale_invoicing_pricelist](contract_sale_invoicing_pricelist/) | 16.0.1.0.0 |  | This module will set the invoice pricelist and currency based on the contract.
[contract_update_last_date_invoiced](contract_update_last_date_invoiced/) | 16.0.1.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | This module allows to update the last date invoiced if invoices are deleted.
[contract_variable_qty_timesheet](contract_variable_qty_timesheet/) | 16.0.1.0.1 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/danypr92'><img src='https://github.com/danypr92.png' width='32' height='32' style='border-radius:50%;' alt='danypr92'/></a> | Add formula to invoice
[contract_variable_quantity](contract_variable_quantity/) | 16.0.1.1.1 |  | Variable quantity in contract recurrent invoicing
[product_contract](product_contract/) | 16.0.1.0.2 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Recurring - Product Contract
[subscription_oca](subscription_oca/) | 16.0.1.3.1 |  | Generate recurring invoices.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/cooperative


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# Cooperative
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/cooperative&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/cooperative/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/cooperative/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/cooperative/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/cooperative/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/cooperative/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/cooperative)
[![Translation Status](https://translation.odoo-community.org/widgets/cooperative-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/cooperative-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Modules related to a cooperative registry (subscribtion requests, share transfer, ...).

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[cooperator](cooperator/) | 16.0.1.4.0 |  | Manage your cooperators
[cooperator_documentation](cooperator_documentation/) | 16.0.1.0.0 | <a href='https://github.com/carmenbianca'><img src='https://github.com/carmenbianca.png' width='32' height='32' style='border-radius:50%;' alt='carmenbianca'/></a> | Add a link to the documentation of the module to the menu bar.
[cooperator_portal](cooperator_portal/) | 16.0.1.1.0 |  | Show cooperator information in the website portal
[cooperator_website](cooperator_website/) | 16.0.1.2.0 |  | This module adds the cooperator subscription form allowing to subscribe for shares online.
[cooperator_website_payment](cooperator_website_payment/) | 16.0.1.0.0 |  | Enable direct online payment of cooperative shares
[cooperator_website_recaptcha](cooperator_website_recaptcha/) | 16.0.1.0.0 |  | Add reCAPTCHA to Subscription Request Form
[l10n_be_cooperator](l10n_be_cooperator/) | 16.0.1.2.1 |  | Cooperators Belgium Localization
[l10n_be_cooperator_national_number](l10n_be_cooperator_national_number/) | 16.0.2.1.1 |  | Ask for Belgian National Number in Cooperative Subscription Request.
[l10n_be_cooperator_portal](l10n_be_cooperator_portal/) | 16.0.1.0.0 |  | Give access to Tax Shelter Report in the portal.
[l10n_be_cooperator_portal_national_number](l10n_be_cooperator_portal_national_number/) | 16.0.1.0.0 | <a href='https://github.com/carmenbianca'><img src='https://github.com/carmenbianca.png' width='32' height='32' style='border-radius:50%;' alt='carmenbianca'/></a> | Add the ability to change national number on the account portal.
[l10n_be_cooperator_website_national_number](l10n_be_cooperator_website_national_number/) | 16.0.2.0.0 |  | Ask for Belgian National Number in Cooperative Subscription Request Frontend Form.
[l10n_ch_cooperator](l10n_ch_cooperator/) | 16.0.1.0.0 |  | Cooperators Switzerland localization
[l10n_de_cooperator](l10n_de_cooperator/) | 16.0.1.0.0 |  | German localization for Cooperators module
[l10n_es_cooperator](l10n_es_cooperator/) | 16.0.1.0.1 |  | Cooperator localization for Spain
[l10n_fr_cooperator](l10n_fr_cooperator/) | 16.0.1.0.0 |  | This is the French localization for the Cooperators module
[test_cooperator_website_payment](test_cooperator_website_payment/) | 16.0.1.0.0 |  | Test module for cooperator_website_payment

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/credit-control&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/credit-control/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/credit-control/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/credit-control/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/credit-control/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/credit-control/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/credit-control)
[![Translation Status](https://translation.odoo-community.org/widgets/credit-control-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/credit-control-16-0/?utm_source=widget)

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
[account_credit_control](account_credit_control/) | 16.0.2.0.2 |  | Account Credit Control
[account_credit_control_dunning_fees](account_credit_control_dunning_fees/) | 16.0.1.0.0 |  | Credit control dunning fees
[account_financial_risk](account_financial_risk/) | 16.0.1.4.1 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> | Manage customer risk
[account_invoice_overdue_reminder](account_invoice_overdue_reminder/) | 16.0.1.11.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Simple mail/letter/phone overdue customer invoice reminder
[account_invoice_overdue_warn](account_invoice_overdue_warn/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Show warning on customer form view if it has overdue invoices
[account_invoice_overdue_warn_sale](account_invoice_overdue_warn_sale/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Show overdue warning on sale order form view
[account_payment_return_financial_risk](account_payment_return_financial_risk/) | 16.0.1.0.2 |  | Partner Payment Return Risk
[partner_risk_insurance](partner_risk_insurance/) | 16.0.5.0.0 | <a href='https://github.com/Daniel-CA'><img src='https://github.com/Daniel-CA.png' width='32' height='32' style='border-radius:50%;' alt='Daniel-CA'/></a> <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/omar7r'><img src='https://github.com/omar7r.png' width='32' height='32' style='border-radius:50%;' alt='omar7r'/></a> <a href='https://github.com/Tardo'><img src='https://github.com/Tardo.png' width='32' height='32' style='border-radius:50%;' alt='Tardo'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Risk insurance partner information
[partner_risk_insurance_product_sticker_invoice_report](partner_risk_insurance_product_sticker_invoice_report/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Display a Sticker on Invoice Reports secured with Risk Insurance
[sale_financial_risk](sale_financial_risk/) | 16.0.1.1.4 |  | Manage partner risk in sales orders
[sale_financial_risk_info](sale_financial_risk_info/) | 16.0.1.0.2 |  | Adds risk consumption info in sales orders.
[sale_payment_sheet_financial_risk](sale_payment_sheet_financial_risk/) | 16.0.1.0.1 |  | Manage partner risk in sale payment sheet
[stock_financial_risk](stock_financial_risk/) | 16.0.1.0.0 |  | Manage partner risk in stock moves
[website_sale_financial_risk](website_sale_financial_risk/) | 16.0.1.0.0 |  | Website Sale Financial Risk

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# crm
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/crm&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/crm/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/crm/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/crm/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/crm/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/crm/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/crm)
[![Translation Status](https://translation.odoo-community.org/widgets/crm-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/crm-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[crm_claim](crm_claim/) | 16.0.1.2.0 |  | Track your customers/vendors claims and grievances.
[crm_claim_code](crm_claim_code/) | 16.0.1.1.0 |  | Sequential Code for Claims
[crm_claim_type](crm_claim_type/) | 16.0.1.0.0 |  | Claim types for CRM
[crm_date_deadline_required](crm_date_deadline_required/) | 16.0.1.0.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Field date deadline required in the opportunity
[crm_exception](crm_exception/) | 16.0.1.0.0 |  | CRM Exception
[crm_industry](crm_industry/) | 16.0.1.1.0 |  | Link leads/opportunities to industries
[crm_lead_code](crm_lead_code/) | 16.0.1.0.1 |  | Sequential Code for Leads / Opportunities
[crm_lead_currency](crm_lead_currency/) | 16.0.1.0.0 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | On leads/opportunities, add the amount in the customer's currency.
[crm_lead_firstname](crm_lead_firstname/) | 16.0.1.0.1 |  | Specify split names for contacts in leads
[crm_lead_product](crm_lead_product/) | 16.0.1.0.0 |  | Adds a lead line in the lead/opportunity model in odoo
[crm_lead_search_archive](crm_lead_search_archive/) | 16.0.1.0.1 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Add a filter to search both in active/archive lead
[crm_lead_to_task](crm_lead_to_task/) | 16.0.1.0.1 |  | Create Tasks from Leads/Opportunities
[crm_lead_vat](crm_lead_vat/) | 16.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Add VAT field to leads
[crm_location](crm_location/) | 16.0.1.0.1 |  | CRM location
[crm_location_nuts](crm_location_nuts/) | 16.0.1.0.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | NUTS Regions in CRM
[crm_partner_assign](crm_partner_assign/) | 16.0.0.1.2 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Assign a Partner to an Opportunity/Lead/Partner to indicate Partnership
[crm_partner_required](crm_partner_required/) | 16.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Field partner required in the opportunity
[crm_phonecall](crm_phonecall/) | 16.0.1.1.0 |  | CRM Phone Calls
[crm_project_create](crm_project_create/) | 16.0.1.1.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Allow create projects from lead/opportunity
[crm_project_task](crm_project_task/) | 16.0.1.0.2 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Create tasks from lead or opportunity
[crm_salesperson_planner](crm_salesperson_planner/) | 16.0.2.0.2 |  | Crm Salesperson Planner
[crm_salesperson_planner_sale](crm_salesperson_planner_sale/) | 16.0.1.0.0 |  | Crm Salesperson Planner Sale
[crm_security_group](crm_security_group/) | 16.0.1.2.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Add new group in Sales to show only CRM
[crm_stage_mail](crm_stage_mail/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Crm Stage Mail
[crm_stage_multi_team](crm_stage_multi_team/) | 16.0.1.0.1 |  | Allows multiple teams in crm stage
[crm_stage_probability](crm_stage_probability/) | 16.0.1.0.0 |  | Define fixed probability on the stages
[crm_team_zip_assign](crm_team_zip_assign/) | 16.0.1.0.0 |  | Auto-assign CRM teams to partners based on ZIP code patterns
[crm_won_restrict_per_stage](crm_won_restrict_per_stage/) | 16.0.1.0.1 | <a href='https://github.com/carolinafernandez-tecnativa'><img src='https://github.com/carolinafernandez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carolinafernandez-tecnativa'/></a> | CRM Won Restrict Per Stage
[marketing_crm_partner](marketing_crm_partner/) | 16.0.1.0.0 |  | Copy tracking fields from leads to partners

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/currency&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/currency/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/currency/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/currency/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/currency/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/currency/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/currency)
[![Translation Status](https://translation.odoo-community.org/widgets/currency-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/currency-16-0/?utm_source=widget)

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
[currency_old_rate_notify](currency_old_rate_notify/) | 16.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Notify accounting managers when currency rates are too old
[currency_rate_update](currency_rate_update/) | 16.0.1.1.2 |  | Update exchange rates using OCA modules
[currency_rate_update_xe](currency_rate_update_xe/) | 16.0.1.0.0 |  | Update exchange rates using XE.com

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/data-protection&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/data-protection/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/data-protection/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/data-protection/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/data-protection/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/data-protection/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/data-protection)
[![Translation Status](https://translation.odoo-community.org/widgets/data-protection-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/data-protection-16-0/?utm_source=widget)

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
[privacy](privacy/) | 16.0.1.0.0 |  | Provides data privacy and protection features to comply to regulations, such as GDPR.
[privacy_consent](privacy_consent/) | 16.0.1.0.1 |  | Allow people to explicitly accept or reject inclusion in some activity, GDPR compliant

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# ddmrp
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/ddmrp&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/ddmrp/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/ddmrp/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/ddmrp/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/ddmrp/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/ddmrp/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/ddmrp)
[![Translation Status](https://translation.odoo-community.org/widgets/ddmrp-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/ddmrp-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

DDMRP in Odoo.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[ddmrp](ddmrp/) | 16.0.1.16.2 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | Demand Driven Material Requirements Planning
[ddmrp_adjustment](ddmrp_adjustment/) | 16.0.1.7.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Allow to apply factor adjustments to buffers.
[ddmrp_chatter](ddmrp_chatter/) | 16.0.1.1.1 |  | Adds chatter and activities to stock buffers.
[ddmrp_cron_actions_as_job](ddmrp_cron_actions_as_job/) | 16.0.1.0.1 |  | Run DDMRP Buffer Calculation as jobs
[ddmrp_exclude_moves_adu_calc](ddmrp_exclude_moves_adu_calc/) | 16.0.1.1.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Define additional rules to exclude certain moves from ADU calculation
[ddmrp_exclude_moves_adu_calc_sales](ddmrp_exclude_moves_adu_calc_sales/) | 16.0.2.0.0 | <a href='https://github.com/DavidJForgeFlow'><img src='https://github.com/DavidJForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='DavidJForgeFlow'/></a> | DDMRP Exclude Moves ADU Calc integration with Sales app.
[ddmrp_history](ddmrp_history/) | 16.0.1.2.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Allow to store historical data of DDMRP buffers.
[ddmrp_product_replace](ddmrp_product_replace/) | 16.0.1.2.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Provides a assisting tool for product replacement.
[ddmrp_report_part_flow_index](ddmrp_report_part_flow_index/) | 16.0.1.3.1 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Provides the DDMRP Parts Flow Index Report
[ddmrp_sale](ddmrp_sale/) | 16.0.2.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | DDMRP integration with Sales app.
[ddmrp_sale_dropshipping](ddmrp_sale_dropshipping/) | 16.0.1.0.0 | <a href='https://github.com/JordiMForgeFlow'><img src='https://github.com/JordiMForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiMForgeFlow'/></a> | Ignore qualified demand of sale quotes that are dropshipped.
[ddmrp_sale_order_line_date](ddmrp_sale_order_line_date/) | 16.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | DDMRP Sale integration considering commitment date per order line.
[ddmrp_warning](ddmrp_warning/) | 16.0.1.3.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Adds configuration warnings on stock buffers.
[stock_buffer_route](stock_buffer_route/) | 16.0.1.2.0 |  | Allows to force a route to be used when procuring from Stock Buffers
[stock_buffer_sales_analysis](stock_buffer_sales_analysis/) | 16.0.1.0.0 |  | Allows to access the Sales Analysis from Stock Buffers

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# delivery-carrier
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/delivery-carrier&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/delivery-carrier/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/delivery-carrier/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/delivery-carrier/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/delivery-carrier/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/delivery-carrier/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/delivery-carrier)
[![Translation Status](https://translation.odoo-community.org/widgets/delivery-carrier-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/delivery-carrier-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_delivery_carrier_label](base_delivery_carrier_label/) | 16.0.2.0.0 |  | Base module for carrier labels
[carrier_account_environment](carrier_account_environment/) | 16.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Configure carriers with server_environment_files
[delivery_auto_refresh](delivery_auto_refresh/) | 16.0.2.0.3 |  | Auto-refresh delivery price in sales orders
[delivery_automatic_package](delivery_automatic_package/) | 16.0.1.0.0 |  | Allows to set a delivery package automatically when sending to shipper.
[delivery_carrier_account](delivery_carrier_account/) | 16.0.1.0.1 |  | Delivery Carrier Account
[delivery_carrier_agency](delivery_carrier_agency/) | 16.0.1.0.0 |  | Add a model for Carrier Agencies
[delivery_carrier_deposit](delivery_carrier_deposit/) | 16.0.1.0.0 |  | Create deposit slips
[delivery_carrier_info](delivery_carrier_info/) | 16.0.1.0.0 |  | Add code on carrier
[delivery_carrier_manual_price](delivery_carrier_manual_price/) | 16.0.1.0.0 |  | Allow setting manual shipping cost in sale order.
[delivery_carrier_manual_weight](delivery_carrier_manual_weight/) | 16.0.1.0.0 |  | Allow setting weight and shipping weight in stock transfers manually based on carrier.
[delivery_carrier_max_weight_constraint](delivery_carrier_max_weight_constraint/) | 16.0.1.0.1 |  | Constrain package maximum weight
[delivery_carrier_multi_zip](delivery_carrier_multi_zip/) | 16.0.1.0.0 |  | Multiple ZIP intervals for the same delivery method
[delivery_carrier_package_measure_required](delivery_carrier_package_measure_required/) | 16.0.1.0.0 |  | Allow the configuration of which package measurements are required on a delivery carrier basis.
[delivery_carrier_partner](delivery_carrier_partner/) | 16.0.1.0.0 |  | Add a partner in the delivery carrier
[delivery_correos_express](delivery_correos_express/) | 16.0.1.0.0 |  | Delivery Carrier implementation for Correos Express using their API
[delivery_cttexpress](delivery_cttexpress/) | 16.0.1.1.1 |  | Delivery Carrier implementation for CTT Express API
[delivery_dachser](delivery_dachser/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Delivery Carrier implementation for Dachser API
[delivery_deliverea](delivery_deliverea/) | 16.0.1.1.0 |  | Delivery Carrier implementation for Deliverea using their API
[delivery_driver](delivery_driver/) | 16.0.1.3.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Allow choose driver in delivery methods
[delivery_driver_stock_picking_batch](delivery_driver_stock_picking_batch/) | 16.0.1.1.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Add drivers from delivery in stock picking batch
[delivery_dropoff_site](delivery_dropoff_site/) | 16.0.1.0.1 |  | Send goods to sites in which customers come pick up package
[delivery_estimated_package_quantity_by_weight](delivery_estimated_package_quantity_by_weight/) | 16.0.1.0.0 |  | Compute the amount of packages a picking out should have depending on the weight of the products and the limit fixed by the carrier
[delivery_multi_destination](delivery_multi_destination/) | 16.0.2.0.0 |  | Multiple destinations for the same delivery method
[delivery_package_fee](delivery_package_fee/) | 16.0.1.2.0 |  | Add fees on delivered packages on shipping methods
[delivery_package_number](delivery_package_number/) | 16.0.3.0.0 |  | Set or compute number of packages for a picking
[delivery_package_type_number_parcels](delivery_package_type_number_parcels/) | 16.0.1.0.2 |  | Number of parcels in a package type
[delivery_postlogistics](delivery_postlogistics/) | 16.0.1.1.0 |  | Print PostLogistics shipping labels using the Barcode web service
[delivery_postlogistics_server_env](delivery_postlogistics_server_env/) | 16.0.1.0.0 |  | Server Environment layer for Delivery Postlogistics
[delivery_price_method](delivery_price_method/) | 16.0.1.1.0 |  | Provides fields to be able to contemplate the tracking statesand also adds a global fields
[delivery_purchase](delivery_purchase/) | 16.0.1.1.4 |  | Delivery costs in purchases
[delivery_roulier](delivery_roulier/) | 16.0.2.1.1 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> <a href='https://github.com/hparfr'><img src='https://github.com/hparfr.png' width='32' height='32' style='border-radius:50%;' alt='hparfr'/></a> | Integration of multiple carriers
[delivery_roulier_dpd_fr](delivery_roulier_dpd_fr/) | 16.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Generate Labels for DPD
[delivery_roulier_geodis_fr](delivery_roulier_geodis_fr/) | 16.0.1.1.1 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Generate Label for Geodis logistic
[delivery_roulier_laposte_fr](delivery_roulier_laposte_fr/) | 16.0.1.1.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Generate Label for La Poste/Colissimo
[delivery_roulier_option](delivery_roulier_option/) | 16.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Add options to roulier modules
[delivery_schenker](delivery_schenker/) | 16.0.1.0.0 |  | Delivery Carrier implementation for DB Schenker API
[delivery_state](delivery_state/) | 16.0.1.1.0 |  | Provides fields to be able to contemplate the tracking statesand also adds a global fields
[delivery_state_manual](delivery_state_manual/) | 16.0.1.0.0 | <a href='https://github.com/tisho99'><img src='https://github.com/tisho99.png' width='32' height='32' style='border-radius:50%;' alt='tisho99'/></a> | Manually edit the delivery state of pickings
[partner_delivery_schedule](partner_delivery_schedule/) | 16.0.1.1.0 |  | Set on partners a schedule for delivery goods
[partner_delivery_zone](partner_delivery_zone/) | 16.0.1.3.0 |  | This module allows to create partner delivery zones for physical products
[sale_order_warehouse_from_delivery_carrier](sale_order_warehouse_from_delivery_carrier/) | 16.0.1.0.0 |  | Sale Order WH from Delivery Carrier
[server_environment_delivery](server_environment_delivery/) | 16.0.1.0.0 |  | Configure prod environment for delivery carriers
[stock_picking_delivery_link](stock_picking_delivery_link/) | 16.0.1.2.0 |  | Adds link to the delivery on all intermediate operations.
[stock_picking_delivery_package_type_domain](stock_picking_delivery_package_type_domain/) | 16.0.1.0.1 |  | This module will allow to extend the domain to filter package type selection in 'Choose Delivery Package' wizard
[stock_picking_report_delivery_cost](stock_picking_report_delivery_cost/) | 16.0.1.1.1 |  | Show delivery cost in delivery slip and picking operations reports

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/dms&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/dms/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/dms/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/dms/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/dms/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/dms/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/dms)
[![Translation Status](https://translation.odoo-community.org/widgets/dms-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/dms-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_dms_field](account_dms_field/) | 16.0.1.0.2 |  | Add dms field for account
[dms](dms/) | 16.0.1.8.7 |  | Document Management System for Odoo
[dms_attachment_link](dms_attachment_link/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Dms Attachment Link
[dms_auto_classification](dms_auto_classification/) | 16.0.1.1.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Auto classify documents into DMS
[dms_field](dms_field/) | 16.0.1.1.7 |  | Create DMS View and allow to use them inside a record
[dms_field_auto_classification](dms_field_auto_classification/) | 16.0.1.0.3 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Auto classify files into embedded DMS
[dms_storage](dms_storage/) | 16.0.1.0.0 |  | Integrate DMS with external Storages
[dms_user_role](dms_user_role/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | DMS User Role
[hr_dms_field](hr_dms_field/) | 16.0.1.1.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Add dms field for employees
[sale_dms_field](sale_dms_field/) | 16.0.1.0.0 |  | Add dms field for sale
[web_editor_media_dialog_dms](web_editor_media_dialog_dms/) | 16.0.1.0.0 |  | Integrate DMS with media dialog of web editor

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# donation
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/donation&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/donation/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/donation/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/donation/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/donation/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/donation/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/donation)
[![Translation Status](https://translation.odoo-community.org/widgets/donation-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/donation-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Modules to manage donations in Odoo.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[donation](donation/) | 16.0.2.2.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Manage donations
[donation_bank_statement_oca](donation_bank_statement_oca/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Manage donations by credit transfer
[donation_base](donation_base/) | 16.0.2.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Base module for donations
[donation_direct_debit](donation_direct_debit/) | 16.0.2.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Auto-generate direct debit order on donation validation
[donation_recurring](donation_recurring/) | 16.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Manage recurring donations
[partner_match_or_create](partner_match_or_create/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Create a new partner or match an existing partner
[product_analytic_donation](product_analytic_donation/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Glue module between donation and product_analytic

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/e-commerce&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/e-commerce/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/e-commerce/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/e-commerce/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/e-commerce/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/e-commerce/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/e-commerce)
[![Translation Status](https://translation.odoo-community.org/widgets/e-commerce-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/e-commerce-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[product_template_multi_link](product_template_multi_link/) | 16.0.1.0.0 |  | Product Multi Links (Template)
[website_account_fiscal_position_partner_type](website_account_fiscal_position_partner_type/) | 16.0.1.0.0 | <a href='https://github.com/cubells'><img src='https://github.com/cubells.png' width='32' height='32' style='border-radius:50%;' alt='cubells'/></a> | Website Account Fiscal Position Partner Type
[website_sale_attribute_filter_form_submit](website_sale_attribute_filter_form_submit/) | 16.0.1.0.0 |  | Allow to apply manually the filters on the e-commerce
[website_sale_attribute_filter_multiselect](website_sale_attribute_filter_multiselect/) | 16.0.1.0.0 |  | Add multiselect display type for product and new filter for it
[website_sale_cart_expire](website_sale_cart_expire/) | 16.0.1.0.3 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Cancel carts without activity after a configurable time
[website_sale_cart_selectable](website_sale_cart_selectable/) | 16.0.1.0.1 |  | Add a toggle to products for enabling "Add to Cart" functionality in the e-commerce.
[website_sale_category_breadcrumb](website_sale_category_breadcrumb/) | 16.0.1.0.0 | <a href='https://github.com/Rad0van'><img src='https://github.com/Rad0van.png' width='32' height='32' style='border-radius:50%;' alt='Rad0van'/></a> | Displays Product Category Breadcrumb(s) in eCommerce
[website_sale_checkout_skip_payment](website_sale_checkout_skip_payment/) | 16.0.1.2.2 |  | Skip payment for logged users in checkout process
[website_sale_comparison_hide_price](website_sale_comparison_hide_price/) | 16.0.1.0.0 |  | Hide product prices on the shop
[website_sale_hide_price](website_sale_hide_price/) | 16.0.2.4.0 |  | Hide product prices on the shop
[website_sale_invoice_address](website_sale_invoice_address/) | 16.0.1.1.0 |  | Set e-Commerce sale orders invoice address as in backend
[website_sale_order_shipping_modification](website_sale_order_shipping_modification/) | 16.0.1.0.0 |  | Change the delivery address in quotes from the portal
[website_sale_order_type](website_sale_order_type/) | 16.0.1.0.2 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | This module allows sale_order_type to work with website_sale.
[website_sale_product_assortment](website_sale_product_assortment/) | 16.0.1.1.2 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Use product assortments to display products available on e-commerce.
[website_sale_product_attachment](website_sale_product_attachment/) | 16.0.1.1.0 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Let visitors download attachments from a product page
[website_sale_product_attribute_filter_collapse](website_sale_product_attribute_filter_collapse/) | 16.0.1.0.1 |  | Allows the attributes of the categories to be folded
[website_sale_product_attribute_value_filter_existing](website_sale_product_attribute_value_filter_existing/) | 16.0.1.2.1 |  | Allow hide attributes values not used in variants
[website_sale_product_brand](website_sale_product_brand/) | 16.0.1.0.1 |  | Product Brand Filtering in Website
[website_sale_product_description](website_sale_product_description/) | 16.0.1.0.0 |  | Shows custom e-Commerce description for products
[website_sale_product_detail_attribute_image](website_sale_product_detail_attribute_image/) | 16.0.1.0.1 |  | Display attributes images in shop product detail
[website_sale_product_image_sample](website_sale_product_image_sample/) | 16.0.1.0.0 |  | Display product image sample to select product variant on website
[website_sale_product_item_cart_custom_qty](website_sale_product_item_cart_custom_qty/) | 16.0.1.2.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Allows to add to cart from product items a custom quantity.
[website_sale_product_minimal_price](website_sale_product_minimal_price/) | 16.0.1.0.1 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Display minimal price for products that has variants
[website_sale_product_reference_displayed](website_sale_product_reference_displayed/) | 16.0.1.0.2 |  | Display product reference in e-commerce
[website_sale_require_legal](website_sale_require_legal/) | 16.0.1.0.2 |  | Force the user to accept legal tems to buy in the web shop
[website_sale_stock_available](website_sale_stock_available/) | 16.0.1.0.2 |  | Display 'Available to promise' in shop online instead of 'Free To Use Quantity'
[website_sale_stock_list_preview](website_sale_stock_list_preview/) | 16.0.1.0.2 |  | Show the stock of products on the product previews
[website_sale_stock_provisioning_date](website_sale_stock_provisioning_date/) | 16.0.1.0.0 |  | Display provisioning date for a product in shop online
[website_sale_suggest_create_account](website_sale_suggest_create_account/) | 16.0.1.1.0 |  | Suggest users to create an account when buying in the website
[website_sale_tax_toggle](website_sale_tax_toggle/) | 16.0.1.1.1 |  | Allow display price in Shop with or without taxes
[website_sale_vat_required](website_sale_vat_required/) | 16.0.1.0.1 |  | VAT number required in checkout form
[website_sale_wishlist_hide_price](website_sale_wishlist_hide_price/) | 16.0.1.0.0 |  | Hide product prices on the shop
[website_sale_wishlist_keep](website_sale_wishlist_keep/) | 16.0.1.0.1 |  | Allows to add products to my cart but keep it in my wishlist"
[website_snippet_product_category](website_snippet_product_category/) | 16.0.1.0.0 | <a href='https://github.com/Tardo'><img src='https://github.com/Tardo.png' width='32' height='32' style='border-radius:50%;' alt='Tardo'/></a> | Adds a new snippet to show e-commerce categories

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/e-learning&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/e-learning/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/e-learning/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/e-learning/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/e-learning/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/e-learning/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/e-learning)
[![Translation Status](https://translation.odoo-community.org/widgets/e-learning-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/e-learning-16-0/?utm_source=widget)

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
[website_slides_attendees_completed_time](website_slides_attendees_completed_time/) | 16.0.1.0.0 |  | Show course completed time in attendee views

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# edi
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/edi&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/edi/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/edi/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/edi/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/edi/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/edi/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/edi)
[![Translation Status](https://translation.odoo-community.org/widgets/edi-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/edi-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_edi_no_autocreate_partner](account_edi_no_autocreate_partner/) | 16.0.1.0.0 |  | Prevents auto-creation of partners during invoice import by assigning unmatched invoices to a protected “Partner Not Found” contact.
[account_edi_no_product_name_match](account_edi_no_product_name_match/) | 16.0.1.0.0 |  | Disable product matching by name in Account EDI imports
[account_edi_retrieve_partner](account_edi_retrieve_partner/) | 16.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This module extends EDI invoice import process by improving how vendor partners are identified from the XML file.
[account_edi_retrieve_partner_from_purchase_order](account_edi_retrieve_partner_from_purchase_order/) | 16.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Retrieves the partner from the related purchase order if set in UBL document
[account_edi_ubl_cii_additional_document](account_edi_ubl_cii_additional_document/) | 16.0.1.0.0 |  | Extends account_edi_ubl_cii to import all attachments from UBL invoices (not only PDFs) and link them to the vendor bill.
[account_edi_ubl_cii_check_total](account_edi_ubl_cii_check_total/) | 16.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This addon extends the UBL invoice import process to automatically populate the suppliers check total field based on the value found in the XML file.
[account_edi_ubl_cii_invoice_line_name_enhance](account_edi_ubl_cii_invoice_line_name_enhance/) | 16.0.1.0.0 |  | This module improves invoice line label generation when importing UBL vendor bills by including the product name when it is not already present.
[account_edi_ubl_cii_payment_unece](account_edi_ubl_cii_payment_unece/) | 16.0.1.0.0 |  | Import/Export UNECE payment codes in UBL and CII XML documents.
[account_edi_ubl_cii_purchase_match](account_edi_ubl_cii_purchase_match/) | 16.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Extend UBL vendor bill import to automatically match and link bill lines to purchase order lines using the OrderReference and product label.
[account_edi_ubl_cii_purchase_match_product_packaging](account_edi_ubl_cii_purchase_match_product_packaging/) | 16.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Allows retrieving the correct UoM and packaging from UNECE codes when matching invoice lines with purchase orders
[account_edi_ubl_cii_retrieve_tax](account_edi_ubl_cii_retrieve_tax/) | 16.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Match taxes on UBL import using UNECE tax codes
[account_edi_ubl_cii_supplier_invoice_number](account_edi_ubl_cii_supplier_invoice_number/) | 16.0.1.0.0 |  | This addon extends the UBL invoice import process to automatically populate the suppliers invoice number based on the value found in the XML file.
[account_edi_ubl_move_line_uom_and_packaging_unece](account_edi_ubl_move_line_uom_and_packaging_unece/) | 16.0.1.0.0 |  | Adds UNECE-based detection of UoM and packaging on invoice lines during UBL import.
[account_einvoice_generate](account_einvoice_generate/) | 16.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Technical module to generate PDF invoices with embedded XML file
[account_invoice_download](account_invoice_download/) | 16.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Auto-download supplier invoices and import them
[account_invoice_download_ovh](account_invoice_download_ovh/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Get OVH Invoice via the API
[account_invoice_edifact](account_invoice_edifact/) | 16.0.1.0.0 |  | Generate customer invoices with EDIFACT/D96A format
[account_invoice_export](account_invoice_export/) | 16.0.1.0.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Account Invoice Export
[account_invoice_export_job](account_invoice_export_job/) | 16.0.1.0.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Account Invoice Export Job
[account_invoice_facturx](account_invoice_facturx/) | 16.0.2.2.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Generate Factur-X/ZUGFeRD customer invoices
[account_invoice_facturx_py3o](account_invoice_facturx_py3o/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Generate Factur-X invoices with Py3o reporting engine
[account_invoice_import](account_invoice_import/) | 16.0.2.6.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import supplier invoices/refunds as PDF or XML files
[account_invoice_import_facturx](account_invoice_import_facturx/) | 16.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import Factur-X/ZUGFeRD Vendor Bills
[account_invoice_import_simple_pdf](account_invoice_import_simple_pdf/) | 16.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import simple PDF vendor bills
[account_invoice_import_ubl](account_invoice_import_ubl/) | 16.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import UBL XML supplier invoices/refunds
[account_invoice_ubl](account_invoice_ubl/) | 16.0.1.0.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Generate UBL XML file for customer invoices/refunds
[base_business_document_import](base_business_document_import/) | 16.0.1.4.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Provides technical tools to import sale orders or supplier invoices
[base_business_document_import_phone](base_business_document_import_phone/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Use phone numbers to match partners upon import of business documents
[base_ebill_payment_contract](base_ebill_payment_contract/) | 16.0.1.0.2 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Base for managing e-billing contracts
[base_edi](base_edi/) | 16.0.1.1.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Base module to aggregate EDI features.
[base_edifact](base_edifact/) | 16.0.1.6.0 | <a href='https://github.com/rmorant'><img src='https://github.com/rmorant.png' width='32' height='32' style='border-radius:50%;' alt='rmorant'/></a> | UN/EDIFACT/D96A utilities using pydifact parser
[base_facturx](base_facturx/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Base module for Factur-X/ZUGFeRD
[base_ubl](base_ubl/) | 16.0.1.3.0 |  | Base module for Universal Business Language (UBL)
[base_ubl_payment](base_ubl_payment/) | 16.0.1.0.1 |  | Payment-related code for Universal Business Language (UBL)
[base_wamas_ubl](base_wamas_ubl/) | 16.0.1.17.1 |  | Base module to aggregate WAMAS - UBL features.
[despatch_advice_import](despatch_advice_import/) | 16.0.1.2.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Despatch Advice import
[despatch_advice_import_ubl](despatch_advice_import_ubl/) | 16.0.1.1.0 |  | Import Despatch Advice files
[pdf_helper](pdf_helper/) | 16.0.1.1.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Provides helpers to work w/ PDFs
[purchase_order_ubl](purchase_order_ubl/) | 16.0.1.1.0 |  | Embed UBL XML file inside the PDF purchase order
[sale_order_import](sale_order_import/) | 16.0.1.5.0 |  | Import RFQ or sale orders from files
[sale_order_import_edifact](sale_order_import_edifact/) | 16.0.1.1.0 | <a href='https://github.com/rmorant'><img src='https://github.com/rmorant.png' width='32' height='32' style='border-radius:50%;' alt='rmorant'/></a> | EDIFACT/D96A Order

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/edi-framework&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/edi-framework/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/edi-framework/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/edi-framework/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/edi-framework/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/edi-framework/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/edi-framework)
[![Translation Status](https://translation.odoo-community.org/widgets/edi-framework-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/edi-framework-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

{'TODO': 'add repo description.'}

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[edi_account_oca](edi_account_oca/) | 16.0.1.1.0 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Define EDI Configuration for Account Moves
[edi_backend_partner_oca](edi_backend_partner_oca/) | 16.0.1.0.1 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Add the a partner field to EDI backend
[edi_edifact_oca](edi_edifact_oca/) | 16.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Define EDI backend type for EDIFACT.
[edi_endpoint_oca](edi_endpoint_oca/) | 16.0.1.1.1 |  | Base module allowing configuration of custom endpoints for EDI framework.
[edi_exchange_deduplicate_oca](edi_exchange_deduplicate_oca/) | 16.0.1.1.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Introduce a deduplication mechanism at the sending step
[edi_exchange_template_oca](edi_exchange_template_oca/) | 16.0.1.1.2 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Allows definition of exchanges via templates.
[edi_notification_oca](edi_notification_oca/) | 16.0.1.0.0 |  | Define notification activities on exchange records.
[edi_oca](edi_oca/) | 16.0.1.15.3 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Define backends, exchange types, exchange records, basic automation and views for handling EDI exchanges.
[edi_partner_oca](edi_partner_oca/) | 16.0.1.0.1 |  | EDI framework configuration and base logic for partners
[edi_party_data_oca](edi_party_data_oca/) | 16.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Allow to configure and retrieve party information for EDI exchanges.
[edi_product_multi_barcode_oca](edi_product_multi_barcode_oca/) | 16.0.1.0.0 |  | EDI framework configuration and base logic for product barcodes.
[edi_product_oca](edi_product_oca/) | 16.0.1.1.1 |  | EDI framework configuration and base logic for products and products packaging
[edi_record_metadata_oca](edi_record_metadata_oca/) | 16.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Allow to store metadata for related records.
[edi_sale_edifact_oca](edi_sale_edifact_oca/) | 16.0.1.1.0 |  | Provide a demo exchange type setting and common tests for EDIFACT standard in EDI on sales.
[edi_sale_oca](edi_sale_oca/) | 16.0.1.2.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Configuration and special behaviors for EDI on sales.
[edi_state_oca](edi_state_oca/) | 16.0.1.1.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Allow to assign specific EDI states to related records.
[edi_stock_oca](edi_stock_oca/) | 16.0.1.1.2 |  | Define EDI Configuration for Stock
[edi_storage_oca](edi_storage_oca/) | 16.0.1.2.3 |  | Base module to allow exchanging files via storage backend (eg: SFTP).
[edi_ubl_oca](edi_ubl_oca/) | 16.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Define EDI backend type for UBL.
[edi_utm_oca](edi_utm_oca/) | 16.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Automatically assigns the EDI source to records created through the EDI mechanism.
[edi_webservice_oca](edi_webservice_oca/) | 16.0.1.0.1 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Defines webservice integration from EDI Exchange records
[edi_xml_oca](edi_xml_oca/) | 16.0.1.1.2 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Base module for EDI exchange using XML files.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# event
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/event&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/event/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/event/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/event/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/event/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/event/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/event)
[![Translation Status](https://translation.odoo-community.org/widgets/event-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/event-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[event_contact](event_contact/) | 16.0.1.0.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | Add contacts to event and event type
[event_mail](event_mail/) | 16.0.1.1.0 |  | Mail settings in events
[event_project](event_project/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Event project
[event_registration_mass_mailing](event_registration_mass_mailing/) | 16.0.1.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | Put event registrations emails into mailing lists
[event_registration_multi_qty](event_registration_multi_qty/) | 16.0.1.0.1 |  | Allow registration grouped by quantities
[event_registration_partner_unique](event_registration_partner_unique/) | 16.0.1.0.0 |  | Enforces 1 registration per partner and event
[event_registration_qr_code](event_registration_qr_code/) | 16.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Automatically generate unique QR Codes for each registration
[event_sale_registration_multi_qty](event_sale_registration_multi_qty/) | 16.0.1.0.0 |  | Allows sell registrations with more than one attendee
[event_sale_session](event_sale_session/) | 16.0.1.1.0 |  | Sell Event Sessions
[event_session](event_session/) | 16.0.1.5.0 |  | Sessions in events
[event_session_registration_multi_qty](event_session_registration_multi_qty/) | 16.0.1.0.0 |  | Allow registration grouped by quantities in sessions
[partner_event](partner_event/) | 16.0.1.1.0 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Link partner to events
[website_event_contact](website_event_contact/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Display your event contacts on your event page
[website_event_external](website_event_external/) | 16.0.1.0.0 |  | External Event
[website_event_membership_restriction](website_event_membership_restriction/) | 16.0.1.2.0 |  | Restrict event registration to members only
[website_event_questions_by_ticket](website_event_questions_by_ticket/) | 16.0.1.0.0 |  | Events Questions conditional to the chosen ticket
[website_event_require_legal](website_event_require_legal/) | 16.0.1.0.0 |  | Website Event Require Legal
[website_event_require_login](website_event_require_login/) | 16.0.1.1.0 |  | Website Event Require Login
[website_event_sale_cart_quantity_readonly](website_event_sale_cart_quantity_readonly/) | 16.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Prevent the user to change the quantity of an event in the cart
[website_event_ticket_limit](website_event_ticket_limit/) | 16.0.1.0.0 |  | Website Event Ticket Limit

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# field-service
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/field-service&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/field-service/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/field-service/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/field-service/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/field-service/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/field-service/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/field-service)
[![Translation Status](https://translation.odoo-community.org/widgets/field-service-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/field-service-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_territory](base_territory/) | 16.0.1.1.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | This module allows you to define territories, branches, districts and regions to be used for Field Service operations or Sales.
[fieldservice](fieldservice/) | 16.0.1.13.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Manage Field Service Locations, Workers and Orders
[fieldservice_account](fieldservice_account/) | 16.0.2.2.1 | <a href='https://github.com/osimallen'><img src='https://github.com/osimallen.png' width='32' height='32' style='border-radius:50%;' alt='osimallen'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> | Track invoices linked to Field Service orders
[fieldservice_account_analytic](fieldservice_account_analytic/) | 16.0.1.1.0 | <a href='https://github.com/osimallen'><img src='https://github.com/osimallen.png' width='32' height='32' style='border-radius:50%;' alt='osimallen'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> | Track analytic accounts on Field Service locations and orders
[fieldservice_account_payment](fieldservice_account_payment/) | 16.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Allow workers to collect payments from the order.
[fieldservice_activity](fieldservice_activity/) | 16.0.1.0.1 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> | Field Service Activities are a set of actions that need to be performed on a service order
[fieldservice_calendar](fieldservice_calendar/) | 16.0.1.0.1 | <a href='https://github.com/hparfr'><img src='https://github.com/hparfr.png' width='32' height='32' style='border-radius:50%;' alt='hparfr'/></a> | Add calendar to FSM Orders
[fieldservice_crm](fieldservice_crm/) | 16.0.1.0.0 | <a href='https://github.com/patrickrwilson'><img src='https://github.com/patrickrwilson.png' width='32' height='32' style='border-radius:50%;' alt='patrickrwilson'/></a> | Create Field Service orders from the CRM
[fieldservice_digitized_signature](fieldservice_digitized_signature/) | 16.0.1.0.0 |  | Capture a digitized signature on Field Service orders
[fieldservice_equipment_stock](fieldservice_equipment_stock/) | 16.0.1.0.0 | <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> | Integrate stock operations with your field service equipments
[fieldservice_fleet](fieldservice_fleet/) | 16.0.1.0.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Link Field Service vehicles with Odoo Fleet
[fieldservice_geoengine](fieldservice_geoengine/) | 16.0.1.4.3 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Display Field Service locations on a map with Open Street Map
[fieldservice_isp_account](fieldservice_isp_account/) | 16.0.1.1.0 | <a href='https://github.com/osimallen'><img src='https://github.com/osimallen.png' width='32' height='32' style='border-radius:50%;' alt='osimallen'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> | Invoice Field Service orders based on employee time or contractor costs
[fieldservice_isp_flow](fieldservice_isp_flow/) | 16.0.1.1.0 | <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> | Field Service workflow for Internet Service Providers
[fieldservice_portal](fieldservice_portal/) | 16.0.1.1.0 | <a href='https://github.com/aleuffre'><img src='https://github.com/aleuffre.png' width='32' height='32' style='border-radius:50%;' alt='aleuffre'/></a> <a href='https://github.com/renda-dev'><img src='https://github.com/renda-dev.png' width='32' height='32' style='border-radius:50%;' alt='renda-dev'/></a> | Bridge module between fieldservice and portal.
[fieldservice_project](fieldservice_project/) | 16.0.1.0.0 |  | Create field service orders from a project or project task
[fieldservice_recurring](fieldservice_recurring/) | 16.0.2.1.3 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Manage recurring Field Service orders
[fieldservice_repair](fieldservice_repair/) | 16.0.1.0.0 | <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Integrate Field Service orders with MRP repair orders
[fieldservice_route](fieldservice_route/) | 16.0.1.0.1 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Organize the routes of each day.
[fieldservice_sale](fieldservice_sale/) | 16.0.1.3.1 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Sell field services.
[fieldservice_sale_recurring](fieldservice_sale_recurring/) | 16.0.1.0.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Sell recurring field services.
[fieldservice_size](fieldservice_size/) | 16.0.1.0.0 | <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> | Manage Sizes for Field Service Locations and Orders
[fieldservice_skill](fieldservice_skill/) | 16.0.1.0.0 | <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Manage your Field Service workers skills
[fieldservice_stage_validation](fieldservice_stage_validation/) | 16.0.1.0.0 | <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Validate input data when reaching a Field Service stage
[fieldservice_stock](fieldservice_stock/) | 16.0.1.2.1 | <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> | Integrate the logistics operations with Field Service
[fieldservice_stock_picking](fieldservice_stock_picking/) | 16.0.1.0.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Send out and receive materials through Field Service Orders using standard stock transfers
[fieldservice_stock_request](fieldservice_stock_request/) | 16.0.1.0.0 | <a href='https://github.com/brian10048'><img src='https://github.com/brian10048.png' width='32' height='32' style='border-radius:50%;' alt='brian10048'/></a> <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> | Integrate Stock Requests with Field Service Orders
[fieldservice_timeline](fieldservice_timeline/) | 16.0.1.1.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | This module is a display timeline view of the Field Service order in Odoo.
[fieldservice_vehicle](fieldservice_vehicle/) | 16.0.1.0.0 | <a href='https://github.com/wolfhall'><img src='https://github.com/wolfhall.png' width='32' height='32' style='border-radius:50%;' alt='wolfhall'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Manage Field Service vehicles and assign drivers

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# fleet
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/fleet&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/fleet/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/fleet/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/fleet/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/fleet/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/fleet/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/fleet)
[![Translation Status](https://translation.odoo-community.org/widgets/fleet-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/fleet-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[fleet_vehicle_calendar_year](fleet_vehicle_calendar_year/) | 16.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | This module extends the fleet management functionality. Allows the registration of the vehicle's calendar year.
[fleet_vehicle_category](fleet_vehicle_category/) | 16.0.1.0.0 |  | Add category definition for vehicles.
[fleet_vehicle_configuration](fleet_vehicle_configuration/) | 16.0.1.0.0 |  | add vehicle configuration capacity
[fleet_vehicle_fuel_capacity](fleet_vehicle_fuel_capacity/) | 16.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | This module extends the functionality of fleet management. It allows the registration of a vehicle's fuel capacity.
[fleet_vehicle_fuel_type_ethanol](fleet_vehicle_fuel_type_ethanol/) | 16.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | This module extends the fleet management functionality. This adds ethanol as another type of fuel to be used by a vehicle in the fleet.
[fleet_vehicle_history_date_end](fleet_vehicle_history_date_end/) | 16.0.1.0.0 | <a href='https://github.com/mamcode'><img src='https://github.com/mamcode.png' width='32' height='32' style='border-radius:50%;' alt='mamcode'/></a> <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Automatically assign date end in vehicle history when a new driver is assigned.
[fleet_vehicle_inspection](fleet_vehicle_inspection/) | 16.0.1.1.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | This module extends the Fleet module allowing the registration of vehicle entry and exit inspections.
[fleet_vehicle_inspection_template](fleet_vehicle_inspection_template/) | 16.0.2.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | This module extend module fleet_vehicle_inspection enable inspection templates feature
[fleet_vehicle_log_fuel](fleet_vehicle_log_fuel/) | 16.0.1.0.0 |  | Add Log Fuels for your vehicles.
[fleet_vehicle_ownership](fleet_vehicle_ownership/) | 16.0.1.0.1 | <a href='https://github.com/cubells'><img src='https://github.com/cubells.png' width='32' height='32' style='border-radius:50%;' alt='cubells'/></a> | Add vehicle ownership, linking partners to vehicles
[fleet_vehicle_purchase](fleet_vehicle_purchase/) | 16.0.1.0.0 |  | Allow to integrate Purcase with Fleet Vehicles
[fleet_vehicle_service_activity](fleet_vehicle_service_activity/) | 16.0.1.0.0 |  | Activity alerts for fleet services
[fleet_vehicle_service_calendar](fleet_vehicle_service_calendar/) | 16.0.1.0.1 | <a href='https://github.com/mamcode'><img src='https://github.com/mamcode.png' width='32' height='32' style='border-radius:50%;' alt='mamcode'/></a> <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Add a smart button in services to schedule meetings.
[fleet_vehicle_service_kanban](fleet_vehicle_service_kanban/) | 16.0.1.1.0 | <a href='https://github.com/mamcode'><img src='https://github.com/mamcode.png' width='32' height='32' style='border-radius:50%;' alt='mamcode'/></a> <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Add features of kanban to logs of vehicle services.
[fleet_vehicle_service_services](fleet_vehicle_service_services/) | 16.0.1.0.0 |  | Add subservices in Services.
[fleet_vehicle_stock](fleet_vehicle_stock/) | 16.0.1.1.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | This module is an add-on for the Fleet application in Odoo. It allows you to track your Fleet Vehicles in stock moves.
[fleet_vehicle_usage](fleet_vehicle_usage/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Fleet Vehicle Usage

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# geospatial
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/geospatial&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/geospatial/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/geospatial/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/geospatial/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/geospatial/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/geospatial/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/geospatial)
[![Translation Status](https://translation.odoo-community.org/widgets/geospatial-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/geospatial-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# geospatial

This project will enable real life GIS support on Odoo.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_geoengine](base_geoengine/) | 16.0.1.4.0 |  | Geospatial support for Odoo
[base_geoengine_demo](base_geoengine_demo/) | 16.0.1.0.0 |  | Geo spatial support Demo
[base_geolocalize_company](base_geolocalize_company/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add latitude and longitude fields on company model
[geoengine_base_geolocalize](geoengine_base_geolocalize/) | 16.0.1.1.0 |  | Geospatial support for base_geolocalize
[geoengine_partner](geoengine_partner/) | 16.0.1.0.1 |  | Geospatial support of partners
[web_leaflet_lib](web_leaflet_lib/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Bring leaflet.js librairy in odoo.
[web_view_leaflet_map](web_view_leaflet_map/) | 16.0.2.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add new 'leaflet_map' view, to display markers.
[web_view_leaflet_map_partner](web_view_leaflet_map_partner/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | TODO
[website_geoengine](website_geoengine/) | 16.0.1.0.0 |  | Geospatial Website
[website_geoengine_store_locator](website_geoengine_store_locator/) | 16.0.1.0.0 | <a href='https://github.com/Wouitmil'><img src='https://github.com/Wouitmil.png' width='32' height='32' style='border-radius:50%;' alt='Wouitmil'/></a> | Geospatial Website store locator

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/helpdesk&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/helpdesk/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/helpdesk/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/helpdesk/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/helpdesk/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/helpdesk/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/helpdesk)
[![Translation Status](https://translation.odoo-community.org/widgets/helpdesk-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/helpdesk-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[helpdesk_mgmt](helpdesk_mgmt/) | 16.0.2.13.1 |  | Helpdesk
[helpdesk_mgmt_account](helpdesk_mgmt_account/) | 16.0.1.0.0 |  | Link account moves and helpdesk tickets
[helpdesk_mgmt_activity](helpdesk_mgmt_activity/) | 16.0.1.0.0 |  | Create Activities for Odoo records from the Helpdesk
[helpdesk_mgmt_assign_method](helpdesk_mgmt_assign_method/) | 16.0.1.0.0 |  | Helpdesk Assign Method
[helpdesk_mgmt_fieldservice](helpdesk_mgmt_fieldservice/) | 16.0.1.1.0 |  | Create service orders from a ticket
[helpdesk_mgmt_merge](helpdesk_mgmt_merge/) | 16.0.1.0.1 |  | Wizard to merge helpdesk tickets
[helpdesk_mgmt_portal_follower](helpdesk_mgmt_portal_follower/) | 16.0.1.0.1 | <a href='https://github.com/BernatObrador'><img src='https://github.com/BernatObrador.png' width='32' height='32' style='border-radius:50%;' alt='BernatObrador'/></a> <a href='https://github.com/ppyczko'><img src='https://github.com/ppyczko.png' width='32' height='32' style='border-radius:50%;' alt='ppyczko'/></a> <a href='https://github.com/mpascuall'><img src='https://github.com/mpascuall.png' width='32' height='32' style='border-radius:50%;' alt='mpascuall'/></a> | Add ticket followers from website portal
[helpdesk_mgmt_project](helpdesk_mgmt_project/) | 16.0.2.3.1 |  | Add the option to select project in the tickets.
[helpdesk_mgmt_project_domain](helpdesk_mgmt_project_domain/) | 16.0.2.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Enable to set a project domain on ticket
[helpdesk_mgmt_project_stage](helpdesk_mgmt_project_stage/) | 16.0.1.0.1 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Keeps the stages of tickets and tasks in sync
[helpdesk_mgmt_rating](helpdesk_mgmt_rating/) | 16.0.1.0.1 |  | This module allows customer to rate the assistance received on a ticket.
[helpdesk_mgmt_sale](helpdesk_mgmt_sale/) | 16.0.1.0.1 |  | Add the option to select project in the sale orders.
[helpdesk_mgmt_sla](helpdesk_mgmt_sla/) | 16.0.1.0.0 |  | Add SLA to the tickets for Helpdesk Management.
[helpdesk_mgmt_stage_validation](helpdesk_mgmt_stage_validation/) | 16.0.1.0.1 |  | Validate input data when reaching a Helpdesk Ticket stage
[helpdesk_mgmt_stock](helpdesk_mgmt_stock/) | 16.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | This module allows to create helpdesk tickets during stock operations
[helpdesk_mgmt_template](helpdesk_mgmt_template/) | 16.0.1.0.0 |  | Create Helpdesk Ticket Template
[helpdesk_mgmt_timesheet](helpdesk_mgmt_timesheet/) | 16.0.1.7.2 |  | Add HR Timesheet to the tickets for Helpdesk Management.
[helpdesk_motive](helpdesk_motive/) | 16.0.1.0.2 | <a href='https://github.com/nelsonramirezs'><img src='https://github.com/nelsonramirezs.png' width='32' height='32' style='border-radius:50%;' alt='nelsonramirezs'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Keep the motive
[helpdesk_portal_priority](helpdesk_portal_priority/) | 16.0.1.0.0 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | Helpdesk Portal Priority
[helpdesk_portal_restriction](helpdesk_portal_restriction/) | 16.0.1.0.1 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | Helpdesk Portal Restriction
[helpdesk_product](helpdesk_product/) | 16.0.1.0.1 |  | Add the option to select product in the tickets.
[helpdesk_ticket_close_inactive](helpdesk_ticket_close_inactive/) | 16.0.1.1.2 | <a href='https://github.com/miquelalzanillas'><img src='https://github.com/miquelalzanillas.png' width='32' height='32' style='border-radius:50%;' alt='miquelalzanillas'/></a> | Helpdesk Ticket Close Inactive
[helpdesk_ticket_open_tab](helpdesk_ticket_open_tab/) | 16.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Helpdesk Ticket Open Tab
[helpdesk_ticket_partner_response](helpdesk_ticket_partner_response/) | 16.0.1.1.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Change ticket stage when partner response
[helpdesk_ticket_related](helpdesk_ticket_related/) | 16.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Link tickets to each other
[helpdesk_timesheet_time_type](helpdesk_timesheet_time_type/) | 16.0.1.0.0 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | Helpdesk Timesheet Time Type
[helpdesk_type](helpdesk_type/) | 16.0.1.1.0 | <a href='https://github.com/nelsonramirezs'><img src='https://github.com/nelsonramirezs.png' width='32' height='32' style='border-radius:50%;' alt='nelsonramirezs'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Add a type to your tickets

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# hr
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/hr&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/hr/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/hr/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/hr/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/hr/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/hr/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/hr)
[![Translation Status](https://translation.odoo-community.org/widgets/hr-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/hr-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[hr_appraisal_oca](hr_appraisal_oca/) | 16.0.1.0.0 | <a href='https://github.com/ebauza'><img src='https://github.com/ebauza.png' width='32' height='32' style='border-radius:50%;' alt='ebauza'/></a> <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Module for managing employee appraisals
[hr_contract_document](hr_contract_document/) | 16.0.1.0.0 |  | Documents attached to the contact
[hr_contract_employee_calendar_planning](hr_contract_employee_calendar_planning/) | 16.0.1.0.2 |  | Hr Contract Employee Calendar Planning
[hr_contract_multi_job](hr_contract_multi_job/) | 16.0.1.0.0 |  | HR Contract Multi Jobs
[hr_contract_reference](hr_contract_reference/) | 16.0.1.0.1 |  | HR Contract Reference
[hr_course](hr_course/) | 16.0.1.1.2 |  | This module allows your to manage employee's training courses
[hr_course_survey](hr_course_survey/) | 16.0.1.0.0 |  | Evaluate a course using a Schedule
[hr_department_code](hr_department_code/) | 16.0.1.0.0 |  | HR department code
[hr_employee_age](hr_employee_age/) | 16.0.1.0.1 |  | Age field for employee
[hr_employee_birth_name](hr_employee_birth_name/) | 16.0.1.0.0 |  | Employee Birth Name
[hr_employee_birthday_mail](hr_employee_birthday_mail/) | 16.0.1.1.0 |  | Automating birthday mail messages and fostering for a positive work environment.
[hr_employee_calendar_planning](hr_employee_calendar_planning/) | 16.0.1.1.11 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Employee Calendar Planning
[hr_employee_digitized_signature](hr_employee_digitized_signature/) | 16.0.1.0.0 | <a href='https://github.com/newtratip'><img src='https://github.com/newtratip.png' width='32' height='32' style='border-radius:50%;' alt='newtratip'/></a> | Employee Digitized Signature
[hr_employee_document](hr_employee_document/) | 16.0.1.0.1 |  | Documents attached to the employee profile
[hr_employee_document_from_applicant](hr_employee_document_from_applicant/) | 16.0.1.0.0 | <a href='https://github.com/ursais'><img src='https://github.com/ursais.png' width='32' height='32' style='border-radius:50%;' alt='ursais'/></a> | HR Employee Document from Applicant
[hr_employee_firstname](hr_employee_firstname/) | 16.0.1.0.3 | <a href='https://github.com/Savoir-faire Linux'><img src='https://github.com/Savoir-faire Linux.png' width='32' height='32' style='border-radius:50%;' alt='Savoir-faire Linux'/></a> <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Adds First Name to Employee
[hr_employee_firstname_partner_firstname](hr_employee_firstname_partner_firstname/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Glue module between partner_firstname and hr_employee_firstname
[hr_employee_group_overview_readonly](hr_employee_group_overview_readonly/) | 16.0.1.0.0 |  | HR Employee Group Overview Readonly
[hr_employee_id](hr_employee_id/) | 16.0.1.0.1 |  | Employee ID
[hr_employee_language](hr_employee_language/) | 16.0.1.0.1 |  | HR Employee Language
[hr_employee_lastnames](hr_employee_lastnames/) | 16.0.1.0.2 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Split Name in First Name, Father's Last Name and Mother's Last Name
[hr_employee_medical_examination](hr_employee_medical_examination/) | 16.0.1.1.0 |  | Adds information about employee's medical examinations
[hr_employee_partner_external](hr_employee_partner_external/) | 16.0.1.0.0 |  | Associate an external Partner to Employee
[hr_employee_phone_extension](hr_employee_phone_extension/) | 16.0.1.0.0 |  | Employee Phone Extension
[hr_employee_phone_pin](hr_employee_phone_pin/) | 16.0.1.0.0 | <a href='https://github.com/arielbarreiros96'><img src='https://github.com/arielbarreiros96.png' width='32' height='32' style='border-radius:50%;' alt='arielbarreiros96'/></a> | Employee Phone PIN
[hr_employee_ppe](hr_employee_ppe/) | 16.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> <a href='https://github.com/eduaparicio'><img src='https://github.com/eduaparicio.png' width='32' height='32' style='border-radius:50%;' alt='eduaparicio'/></a> | Personal Protective Equipment (PPE) Management
[hr_employee_relative](hr_employee_relative/) | 16.0.1.0.0 |  | Allows storing information about employee's family
[hr_employee_service](hr_employee_service/) | 16.0.1.0.0 |  | Employee service information & duration
[hr_employee_service_contract](hr_employee_service_contract/) | 16.0.1.0.0 |  | Employee service information & duration based on employee's contracts
[hr_employee_ssn](hr_employee_ssn/) | 16.0.1.0.0 |  | View/edit employee's SSN & SIN fields
[hr_holidays_team_manager](hr_holidays_team_manager/) | 16.0.1.0.0 |  | HR Holidays Team Manager
[hr_job_category](hr_job_category/) | 16.0.1.0.2 |  | Adds tags to employee through contract and job position
[hr_org_chart_overview](hr_org_chart_overview/) | 16.0.1.0.0 |  | Organizational Chart Overview
[hr_personal_equipment_request](hr_personal_equipment_request/) | 16.0.1.0.0 |  | This addon allows to manage employee personal equipment
[hr_personal_equipment_request_tier_validation](hr_personal_equipment_request_tier_validation/) | 16.0.1.0.1 |  | Enables tier validation from hr.personal.equipment.request
[hr_personal_equipment_stock](hr_personal_equipment_stock/) | 16.0.1.0.0 |  | This addon allows to integrate hr_personal_equipment_request with stock
[hr_personal_equipment_variant_configurator](hr_personal_equipment_variant_configurator/) | 16.0.1.0.0 |  | Manage variants of personal equipment
[hr_professional_category](hr_professional_category/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | HR Professional Category
[hr_recruitment_torecruit](hr_recruitment_torecruit/) | 16.0.1.1.0 |  | Age field for employee
[resource_multi_week_calendar](resource_multi_week_calendar/) | 16.0.1.0.0 | <a href='https://github.com/carmenbianca'><img src='https://github.com/carmenbianca.png' width='32' height='32' style='border-radius:50%;' alt='carmenbianca'/></a> | Allow a calendar to alternate between multiple weeks.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/hr-attendance&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/hr-attendance/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/hr-attendance/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/hr-attendance/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/hr-attendance/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/hr-attendance/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/hr-attendance)
[![Translation Status](https://translation.odoo-community.org/widgets/hr-attendance-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/hr-attendance-16-0/?utm_source=widget)

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
[hr_attendance_autoclose](hr_attendance_autoclose/) | 16.0.1.0.0 |  | Close stale Attendances
[hr_attendance_calendar_view](hr_attendance_calendar_view/) | 16.0.1.0.0 |  | This module adds the calendar view as an option to display attendance
[hr_attendance_geolocation](hr_attendance_geolocation/) | 16.0.1.0.2 |  | With this module the geolocation of the user is tracked at the check-in/check-out step
[hr_attendance_modification_tracking](hr_attendance_modification_tracking/) | 16.0.1.0.1 |  | Attendance changes will now be registered in the chatter.
[hr_attendance_reason](hr_attendance_reason/) | 16.0.1.1.0 |  | HR Attendance Reason
[hr_attendance_report_theoretical_time](hr_attendance_report_theoretical_time/) | 16.0.1.2.0 |  | Theoretical vs Attended Time Analysis
[hr_attendance_rfid](hr_attendance_rfid/) | 16.0.1.0.1 |  | HR Attendance RFID
[hr_birthday_welcome_message](hr_birthday_welcome_message/) | 16.0.1.0.0 |  | This addon adds a birthday message as welcome message when it is the employee's birthday
[hr_contract_update_overtime](hr_contract_update_overtime/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Update Overtime from HR Contract

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# hr-expense
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/hr-expense&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/hr-expense/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/hr-expense/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/hr-expense/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/hr-expense/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/hr-expense/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/hr-expense)
[![Translation Status](https://translation.odoo-community.org/widgets/hr-expense-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/hr-expense-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[hr_expense_advance_clearing](hr_expense_advance_clearing/) | 16.0.1.0.3 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Employee Advance and Clearing
[hr_expense_advance_clearing_sequence](hr_expense_advance_clearing_sequence/) | 16.0.1.0.0 |  | HR Expense Advance Clearing Sequence
[hr_expense_cancel](hr_expense_cancel/) | 16.0.1.0.3 |  | Hr expense cancel
[hr_expense_invoice](hr_expense_invoice/) | 16.0.2.0.3 |  | Supplier invoices on HR expenses
[hr_expense_journal](hr_expense_journal/) | 16.0.1.0.0 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Set the Journal for the payment type used to pay the expense
[hr_expense_pay_to_vendor](hr_expense_pay_to_vendor/) | 16.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | HR Expense - Pay To Vendor
[hr_expense_payment](hr_expense_payment/) | 16.0.1.0.2 |  | HR Expense Payment
[hr_expense_sequence](hr_expense_sequence/) | 16.0.1.0.1 |  | HR expense sequence
[hr_expense_sequence_option](hr_expense_sequence_option/) | 16.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Manage sequence options for hr.expense.sheet
[hr_expense_tier_validation](hr_expense_tier_validation/) | 16.0.2.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Expense Tier Validation
[hr_expense_work_acceptance](hr_expense_work_acceptance/) | 16.0.1.0.0 |  | Expense Work Acceptance

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# hr-holidays
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/hr-holidays&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/hr-holidays/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/hr-holidays/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/hr-holidays/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/hr-holidays/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/hr-holidays/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/hr-holidays)
[![Translation Status](https://translation.odoo-community.org/widgets/hr-holidays-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/hr-holidays-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[hr_holidays_auto_extend](hr_holidays_auto_extend/) | 16.0.1.0.1 |  | Allow to extend some kind of holidays
[hr_holidays_leave_auto_approve](hr_holidays_leave_auto_approve/) | 16.0.1.0.1 |  | Leave type for auto-validation of Leaves
[hr_holidays_natural_period](hr_holidays_natural_period/) | 16.0.1.2.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Apply natural days in holidays
[hr_holidays_natural_period_public](hr_holidays_natural_period_public/) | 16.0.1.1.0 |  | Allow excluding public holidays for natural days holidays
[hr_holidays_public](hr_holidays_public/) | 16.0.2.0.7 |  | Manage Public Holidays
[hr_holidays_public_city](hr_holidays_public_city/) | 16.0.2.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | HR Holidays Public City
[hr_holidays_settings](hr_holidays_settings/) | 16.0.1.0.0 |  | Enables Settings Form for HR Holidays.
[hr_holidays_summary_email](hr_holidays_summary_email/) | 16.0.1.0.1 | <a href='https://github.com/JordiMForgeFlow'><img src='https://github.com/JordiMForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiMForgeFlow'/></a> | Notify employees with daily or weekly leaves summaries of their company.
[hr_leave_custom_hour_interval](hr_leave_custom_hour_interval/) | 16.0.1.0.0 |  | Edit start and end of leaves using time intervals
[hr_leave_type_code](hr_leave_type_code/) | 16.0.1.0.1 |  | Add a code field to HR Leaves
[resource_leaves_geographic](resource_leaves_geographic/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Add geographic State to Resource Calendar Leaves

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/infrastructure&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/infrastructure/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/infrastructure/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/infrastructure/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/infrastructure/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/infrastructure/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/infrastructure)
[![Translation Status](https://translation.odoo-community.org/widgets/infrastructure-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/infrastructure-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# infrastructure

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_dns_infrastructure](base_dns_infrastructure/) | 16.0.1.0.1 |  | Base module for DNS infrastructure

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/interface-github&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/interface-github/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/interface-github/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/interface-github/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/interface-github/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/interface-github/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/interface-github)
[![Translation Status](https://translation.odoo-community.org/widgets/interface-github-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/interface-github-16-0/?utm_source=widget)

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
[github_connector](github_connector/) | 16.0.1.0.0 |  | Synchronize information from Github repositories
[github_connector_odoo](github_connector_odoo/) | 16.0.1.1.2 |  | Analyze Odoo modules information from Github repositories

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# intrastat-extrastat
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/intrastat-extrastat&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/intrastat-extrastat/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/intrastat-extrastat/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/intrastat-extrastat/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/intrastat-extrastat/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/intrastat-extrastat/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/intrastat-extrastat)
[![Translation Status](https://translation.odoo-community.org/widgets/intrastat-extrastat-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/intrastat-extrastat-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[intrastat_base](intrastat_base/) | 16.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/luc-demeyer'><img src='https://github.com/luc-demeyer.png' width='32' height='32' style='border-radius:50%;' alt='luc-demeyer'/></a> | Base module for Intrastat reporting
[intrastat_delivery](intrastat_delivery/) | 16.0.1.0.0 |  | Propagates the value of the incoterm fields from the order shipping method to the invoices
[intrastat_product](intrastat_product/) | 16.0.2.3.6 |  | Base module for Intrastat Product
[intrastat_product_generic](intrastat_product_generic/) | 16.0.1.0.0 |  | Generic Intrastat Product Declaration
[intrastat_product_hscodes_import](intrastat_product_hscodes_import/) | 16.0.1.0.1 |  | Module used to import HS Codes for Intrastat Product
[product_harmonized_system](product_harmonized_system/) | 16.0.2.0.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/luc-demeyer'><img src='https://github.com/luc-demeyer.png' width='32' height='32' style='border-radius:50%;' alt='luc-demeyer'/></a> | Base module for Product Import/Export reports
[product_harmonized_system_delivery](product_harmonized_system_delivery/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/luc-demeyer'><img src='https://github.com/luc-demeyer.png' width='32' height='32' style='border-radius:50%;' alt='luc-demeyer'/></a> | Hide native hs_code field provided by the delivery module
[product_harmonized_system_stock](product_harmonized_system_stock/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> <a href='https://github.com/luc-demeyer'><img src='https://github.com/luc-demeyer.png' width='32' height='32' style='border-radius:50%;' alt='luc-demeyer'/></a> | Adds a menu entry for H.S. codes

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/iot&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/iot/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/iot/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/iot/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/iot/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/iot/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/iot)
[![Translation Status](https://translation.odoo-community.org/widgets/iot-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/iot-16-0/?utm_source=widget)

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
[iot_amqp_oca](iot_amqp_oca/) | 16.0.1.0.0 |  | Integrate Iot Outputs with AMQP
[iot_input_oca](iot_input_oca/) | 16.0.1.0.1 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | IoT Input module
[iot_key_employee_rfid](iot_key_employee_rfid/) | 16.0.1.0.0 |  | Use an Employee RFID Card as an IoT Key
[iot_oca](iot_oca/) | 16.0.1.0.1 |  | IoT base module
[iot_output_oca](iot_output_oca/) | 16.0.1.0.1 |  | IoT allow multiple outputs
[iot_rule](iot_rule/) | 16.0.1.0.0 |  | Define IoT Rules (Keys that control Inputs)
[iot_template_oca](iot_template_oca/) | 16.0.1.0.1 |  | IoT module for managing templates

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# knowledge
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/knowledge&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/knowledge/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/knowledge/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/knowledge/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/knowledge/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/knowledge/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/knowledge)
[![Translation Status](https://translation.odoo-community.org/widgets/knowledge-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/knowledge-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# knowledge

Knowledge management addons. Also has some useful tools to handle attachments.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[attachment_zipped_download](attachment_zipped_download/) | 16.0.2.0.3 |  | Attachment Zipped Download
[document_knowledge](document_knowledge/) | 16.0.1.1.0 |  | Documents Knowledge
[document_page](document_page/) | 16.0.2.0.1 |  | Document Page
[document_page_access_group](document_page_access_group/) | 16.0.1.1.0 |  | Choose groups to access document pages
[document_page_access_group_user_role](document_page_access_group_user_role/) | 16.0.1.1.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Document Page Access Group User Role
[document_page_approval](document_page_approval/) | 16.0.2.0.0 |  | Document Page Approval
[document_page_group](document_page_group/) | 16.0.1.0.1 |  | Define access groups on documents
[document_page_partner](document_page_partner/) | 16.0.1.0.0 |  | Allows to link doucment pages to a partner
[document_page_project](document_page_project/) | 16.0.1.0.0 |  | This module links document pages to projects
[document_page_reference](document_page_reference/) | 16.0.2.0.0 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Include references on document pages
[document_page_tag](document_page_tag/) | 16.0.1.0.1 |  | Allows you to assign tags or keywords to pages and search for them afterwards
[document_page_tag_print_control](document_page_tag_print_control/) | 16.0.1.0.0 |  | Restricts document page printing based on assigned tags
[document_url](document_url/) | 16.0.1.0.4 |  | URL attachment
[document_url_google_drive](document_url_google_drive/) | 16.0.1.0.1 |  | Attach Google Drive link to Odoo document using Google Drive Picker

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-argentina


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-argentina&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-argentina/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-argentina/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-argentina/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-argentina/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-argentina/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-argentina)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-argentina-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-argentina-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Odoo addons for Argentina

Odoo addons for Argentina

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_ar_afipws](l10n_ar_afipws/) | 16.0.1.0.0 | <a href='https://github.com/nimarosa'><img src='https://github.com/nimarosa.png' width='32' height='32' style='border-radius:50%;' alt='nimarosa'/></a> <a href='https://github.com/ibuioli'><img src='https://github.com/ibuioli.png' width='32' height='32' style='border-radius:50%;' alt='ibuioli'/></a> | Integration for Argentina Electronic invoice webservices
[l10n_ar_afipws_fe](l10n_ar_afipws_fe/) | 16.0.1.0.0 | <a href='https://github.com/nimarosa'><img src='https://github.com/nimarosa.png' width='32' height='32' style='border-radius:50%;' alt='nimarosa'/></a> <a href='https://github.com/ibuioli'><img src='https://github.com/ibuioli.png' width='32' height='32' style='border-radius:50%;' alt='ibuioli'/></a> | Integrate AFIP webservice for Argentina electronic documents
[l10n_ar_bank](l10n_ar_bank/) | 16.0.1.0.0 |  | Listado de Bancos Argentinos

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# l10n-belgium
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-belgium&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-belgium/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-belgium/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-belgium/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-belgium/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-belgium/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-belgium)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-belgium-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-belgium-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_statement_import_coda](account_statement_import_coda/) | 16.0.1.1.0 |  | Import CODA Bank Statement
[companyweb_base](companyweb_base/) | 16.0.1.1.0 | <a href='https://github.com/xavier-bouquiaux'><img src='https://github.com/xavier-bouquiaux.png' width='32' height='32' style='border-radius:50%;' alt='xavier-bouquiaux'/></a> | Know who you are dealing with. Enhance Odoo partner data from companyweb.be.
[companyweb_payment_info](companyweb_payment_info/) | 16.0.1.0.4 | <a href='https://github.com/xavier-bouquiaux'><img src='https://github.com/xavier-bouquiaux.png' width='32' height='32' style='border-radius:50%;' alt='xavier-bouquiaux'/></a> | Send your customer payment information to Companyweb
[l10n_be_antibiotic_tax](l10n_be_antibiotic_tax/) | 16.0.1.0.1 |  | Data module to support antibiotics taxes
[l10n_be_apb_tax](l10n_be_apb_tax/) | 16.0.1.0.1 |  | Data module to support APB taxes
[l10n_be_bpost_address_autocomplete](l10n_be_bpost_address_autocomplete/) | 16.0.1.0.1 |  | Bpost address autocomplete
[l10n_be_eco_tax](l10n_be_eco_tax/) | 16.0.1.0.1 |  | Data module to support BEBAT and RECUPEL taxes
[l10n_be_intrastat_product](l10n_be_intrastat_product/) | 16.0.2.0.0 | <a href='https://github.com/luc-demeyer'><img src='https://github.com/luc-demeyer.png' width='32' height='32' style='border-radius:50%;' alt='luc-demeyer'/></a> <a href='https://github.com/jdidderen-noviat'><img src='https://github.com/jdidderen-noviat.png' width='32' height='32' style='border-radius:50%;' alt='jdidderen-noviat'/></a> | Intrastat Product Declaration for Belgium
[l10n_be_mis_reports](l10n_be_mis_reports/) | 16.0.2.0.1 |  | MIS Builder templates for the Belgium P&L, Balance Sheets and VAT Declaration
[l10n_be_mis_reports_xml](l10n_be_mis_reports_xml/) | 16.0.1.0.1 |  | Exports MIS Builder templates VAT Declaration as XML to load on the administration websites.
[l10n_be_partner_identification](l10n_be_partner_identification/) | 16.0.1.0.0 |  | Belgium Partner Identification Numbers
[l10n_be_partner_kbo_bce](l10n_be_partner_kbo_bce/) | 16.0.1.0.1 |  | Belgium - KBO/BCE numbers
[l10n_be_vat_reports](l10n_be_vat_reports/) | 16.0.1.0.3 |  | Belgium VAT Reports

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-brazil&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-brazil/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-brazil/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-brazil/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-brazil/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-brazil/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-brazil)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-brazil-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-brazil-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Odoo Brazilian Localization / Localização Brasileira do Odoo

A localização brasileira do Odoo, criada pela comunidade Open Source da Odoo Community Association (OCA), inclui um conjunto de módulos detalhados para atender às normas fiscais e legais do Brasil. Esta localização aprimora o Odoo com funcionalidades para:

- **Documentos fiscais:** Suporte abrangente a documentações conforme legislação nacional.
- **Tributos específicos:** Gestão de ICMS, IPI, ISS, PIS, COFINS, CSLL, IRPJ, e outros, incluindo substituição tributária e retenção de impostos.
- **Emissão de notas fiscais eletrônicas:** Compatível com NF-e, NFS-e e mais.
- **Integrações bancárias:** Ferramentas para importação de extratos OFX e geração de CNAB 240 e 400.

## Começando com a Localização

Instale o módulo `l10n_br_base` para configurar as bases da localização brasileira no Odoo. Adicione o `l10n_br_fiscal` para expandir a emissão e gestão de documentos fiscais eletrônicos.

## :arrow_forward: **Teste a Localização Agora!**

Não perca a chance de ver a localização em ação:

1. Clique no botão abaixo para iniciar um container no ambiente Runboat:

   [![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-brazil&target_branch=16.0)

2. Aguarde até o container ficar disponível (indicador verde).
3. Clique em **Live** para acessar o Odoo.
4. Entre com `admin/admin`.
5. Escolha a empresa demo com o regime tributário de seu interesse, seja Simples Nacional ou Lucro Presumido, e explore um ambiente rico em detalhes e funcionalidades.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_br_account](l10n_br_account/) | 16.0.17.0.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Invoicing and accounting entries for Brazil
[l10n_br_account_due_list](l10n_br_account_due_list/) | 16.0.2.1.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Brazilian Account Due List
[l10n_br_account_fleet](l10n_br_account_fleet/) | 16.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Brazilian Localization Account Fleet
[l10n_br_account_nfe](l10n_br_account_nfe/) | 16.0.10.0.0 | <a href='https://github.com/antoniospneto'><img src='https://github.com/antoniospneto.png' width='32' height='32' style='border-radius:50%;' alt='antoniospneto'/></a> <a href='https://github.com/felipemotter'><img src='https://github.com/felipemotter.png' width='32' height='32' style='border-radius:50%;' alt='felipemotter'/></a> <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> | Integration between l10n_br_account and l10n_br_nfe
[l10n_br_account_payment_brcobranca](l10n_br_account_payment_brcobranca/) | 16.0.6.3.0 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> | receivable Boletos and CNAB using the BRCobranca lib
[l10n_br_account_payment_order](l10n_br_account_payment_order/) | 16.0.9.1.1 | <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> | Brazilian Payment Order
[l10n_br_account_renegotiation](l10n_br_account_renegotiation/) | 16.0.1.0.1 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Allows renegotiating payment installments on posted invoices in Brazil
[l10n_br_account_withholding](l10n_br_account_withholding/) | 16.0.3.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Brazilian Withholding Invoice Generator
[l10n_br_base](l10n_br_base/) | 16.0.6.5.3 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Customization of base module for implementations in Brazil.
[l10n_br_cnab_structure](l10n_br_cnab_structure/) | 16.0.3.3.0 | <a href='https://github.com/antoniospneto'><img src='https://github.com/antoniospneto.png' width='32' height='32' style='border-radius:50%;' alt='antoniospneto'/></a> <a href='https://github.com/felipemotter'><img src='https://github.com/felipemotter.png' width='32' height='32' style='border-radius:50%;' alt='felipemotter'/></a> <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> <a href='https://github.com/kaynnan'><img src='https://github.com/kaynnan.png' width='32' height='32' style='border-radius:50%;' alt='kaynnan'/></a> | This module allows defining the structure for generating the CNAB file. Used to exchange information with Brazilian banks.
[l10n_br_cnpj_search](l10n_br_cnpj_search/) | 16.0.3.3.3 |  | Integração com os Webservices da ReceitaWS e SerPro
[l10n_br_coa](l10n_br_coa/) | 16.0.2.7.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | Base do Planos de Contas brasileiros
[l10n_br_coa_generic](l10n_br_coa_generic/) | 16.0.2.2.1 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | Plano de Contas para empresas do Regime normal (Micro e pequenas empresas)
[l10n_br_coa_simple](l10n_br_coa_simple/) | 16.0.2.1.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Plano de Contas ITG 1000 para Microempresas e Empresa de Pequeno Porte
[l10n_br_contract](l10n_br_contract/) | 16.0.7.0.3 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Customization of Contract module for implementations in Brazil.
[l10n_br_crm](l10n_br_crm/) | 16.0.5.2.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> | Brazilian Localization CRM
[l10n_br_crm_cnpj_search](l10n_br_crm_cnpj_search/) | 16.0.5.1.0 | <a href='https://github.com/corredato'><img src='https://github.com/corredato.png' width='32' height='32' style='border-radius:50%;' alt='corredato'/></a> <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | CNPJ search in CRM Lead
[l10n_br_cte](l10n_br_cte/) | 16.0.10.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Brazilian Electronic Invoice CT-e
[l10n_br_cte_spec](l10n_br_cte_spec/) | 16.0.1.2.1 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | CT-e abstract models generated by xsdata-odoo from the official xsd
[l10n_br_currency_rate_update](l10n_br_currency_rate_update/) | 16.0.1.1.2 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Update exchange rates using OCA modules for Brazil
[l10n_br_delivery](l10n_br_delivery/) | 16.0.4.0.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> | delivery module Brazilian Localization
[l10n_br_delivery_nfe](l10n_br_delivery_nfe/) | 16.0.2.0.0 | <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> | Brazilian Localization Delivery NFe
[l10n_br_fiscal](l10n_br_fiscal/) | 16.0.23.0.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Fiscal module/tax engine for Brazil
[l10n_br_fiscal_certificate](l10n_br_fiscal_certificate/) | 16.0.1.2.1 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | A1 fiscal certificate management for Brazil
[l10n_br_fiscal_closing](l10n_br_fiscal_closing/) | 16.0.3.0.0 |  | Period fiscal closing
[l10n_br_fiscal_dfe](l10n_br_fiscal_dfe/) | 16.0.1.3.0 |  | Distribuição de documentos fiscais
[l10n_br_fiscal_edi](l10n_br_fiscal_edi/) | 16.0.2.0.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | Common EDI fiscal features
[l10n_br_fiscal_notification](l10n_br_fiscal_notification/) | 16.0.2.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | Define fiscal document notifications
[l10n_br_fiscal_subsequent_document](l10n_br_fiscal_subsequent_document/) | 16.0.3.0.0 |  | Documentos Fiscais Subsequentes
[l10n_br_hr](l10n_br_hr/) | 16.0.4.4.0 |  | Brazilian Localization HR
[l10n_br_hr_contract](l10n_br_hr_contract/) | 16.0.1.3.0 |  | Brazilian Localization HR Contract
[l10n_br_hr_expense_invoice](l10n_br_hr_expense_invoice/) | 16.0.1.0.1 |  | Customization of HR Expense Invoice module for implementations in Brazil.
[l10n_br_ie_search](l10n_br_ie_search/) | 16.0.2.2.0 |  | Integração com a API SintegraWS e SEFAZ
[l10n_br_mdfe](l10n_br_mdfe/) | 16.0.5.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Brazilian Eletronic Invoice MDF-e
[l10n_br_mdfe_spec](l10n_br_mdfe_spec/) | 16.0.1.1.1 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | MDF-e abstract models generated by xsdata-odoo from the official xsd
[l10n_br_mis_report](l10n_br_mis_report/) | 16.0.1.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | Templates de relatórios contábeis brasileiros: Balanço Patrimonial e DRE
[l10n_br_nfe](l10n_br_nfe/) | 16.0.14.0.0 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Eletronic Invoicing for Brazil / NF-e
[l10n_br_nfe_spec](l10n_br_nfe_spec/) | 16.0.4.0.1 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | NF-e abstract models generated by xsdata-odoo from the official xsd
[l10n_br_nfse](l10n_br_nfse/) | 16.0.8.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/luismalta'><img src='https://github.com/luismalta.png' width='32' height='32' style='border-radius:50%;' alt='luismalta'/></a> <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Root electronic invoice for service / NFS-e module
[l10n_br_nfse_focus](l10n_br_nfse_focus/) | 16.0.3.0.0 | <a href='https://github.com/AndreMarcos'><img src='https://github.com/AndreMarcos.png' width='32' height='32' style='border-radius:50%;' alt='AndreMarcos'/></a> <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/ygcarvalh'><img src='https://github.com/ygcarvalh.png' width='32' height='32' style='border-radius:50%;' alt='ygcarvalh'/></a> <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | NFS-e (FocusNFE)
[l10n_br_nfse_paulistana](l10n_br_nfse_paulistana/) | 16.0.1.0.0 | <a href='https://github.com/gabrielcardoso21'><img src='https://github.com/gabrielcardoso21.png' width='32' height='32' style='border-radius:50%;' alt='gabrielcardoso21'/></a> <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/luismalta'><img src='https://github.com/luismalta.png' width='32' height='32' style='border-radius:50%;' alt='luismalta'/></a> <a href='https://github.com/CristianoMafraJunior'><img src='https://github.com/CristianoMafraJunior.png' width='32' height='32' style='border-radius:50%;' alt='CristianoMafraJunior'/></a> | NFS-e (Nota Paulistana)
[l10n_br_portal](l10n_br_portal/) | 16.0.2.1.2 |  | Campos Brasileiros no Portal
[l10n_br_pos](l10n_br_pos/) | 16.0.1.0.1 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/lfdivino'><img src='https://github.com/lfdivino.png' width='32' height='32' style='border-radius:50%;' alt='lfdivino'/></a> <a href='https://github.com/luismalta'><img src='https://github.com/luismalta.png' width='32' height='32' style='border-radius:50%;' alt='luismalta'/></a> <a href='https://github.com/ygcarvalh'><img src='https://github.com/ygcarvalh.png' width='32' height='32' style='border-radius:50%;' alt='ygcarvalh'/></a> | Ponto de venda adaptado a legislação Brasileira
[l10n_br_product_contract](l10n_br_product_contract/) | 16.0.2.0.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Criação de contratos através dos Pedidos de Vendas
[l10n_br_purchase](l10n_br_purchase/) | 16.0.6.0.5 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Brazilian Localization Purchase
[l10n_br_purchase_blanket_order](l10n_br_purchase_blanket_order/) | 16.0.1.4.0 | <a href='https://github.com/WesleyOliveira98'><img src='https://github.com/WesleyOliveira98.png' width='32' height='32' style='border-radius:50%;' alt='WesleyOliveira98'/></a> <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Brazilian Localization Purchase Blanket Order
[l10n_br_purchase_request](l10n_br_purchase_request/) | 16.0.2.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Purchase Request Brazilian Localization Purchase Request
[l10n_br_purchase_requisition](l10n_br_purchase_requisition/) | 16.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Brazilian Localization Purchase Requisition
[l10n_br_purchase_stock](l10n_br_purchase_stock/) | 16.0.2.0.1 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> | Brazilian Localization Purchase Stock
[l10n_br_resource](l10n_br_resource/) | 16.0.1.1.0 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> <a href='https://github.com/lfdivino'><img src='https://github.com/lfdivino.png' width='32' height='32' style='border-radius:50%;' alt='lfdivino'/></a> | This module extend core resource to create important brazilian informations. Define a Brazilian calendar and some tools to compute dates used in financial and payroll modules
[l10n_br_sale](l10n_br_sale/) | 16.0.8.1.4 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Brazilian Localization Sale
[l10n_br_sale_blanket_order](l10n_br_sale_blanket_order/) | 16.0.2.5.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Brazilian Localization Sale Blanket Order
[l10n_br_sale_commission](l10n_br_sale_commission/) | 16.0.2.0.1 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Brazilian Localization of Sales Commissions
[l10n_br_sale_invoice_plan](l10n_br_sale_invoice_plan/) | 16.0.3.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Brazilian Localization Sale Invoice Plan
[l10n_br_sale_stock](l10n_br_sale_stock/) | 16.0.3.0.2 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> | Brazilian Localization Sales and Warehouse
[l10n_br_setup_tests](l10n_br_setup_tests/) | 16.0.1.0.3 | <a href='https://github.com/antoniospneto'><img src='https://github.com/antoniospneto.png' width='32' height='32' style='border-radius:50%;' alt='antoniospneto'/></a> | Modules for Odoo's Brazil-focused usability with integration tests.
[l10n_br_sped_base](l10n_br_sped_base/) | 16.0.3.3.5 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | Framework abstrato pro SPED
[l10n_br_sped_ecd](l10n_br_sped_ecd/) | 16.0.4.2.0 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Arquivo ECD do SPED
[l10n_br_sped_efd_icms_ipi](l10n_br_sped_efd_icms_ipi/) | 16.0.1.0.2 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Arquivo EFD ICMS IPI do SPED / SPED Fiscal
[l10n_br_stock](l10n_br_stock/) | 16.0.3.0.1 |  | Brazilian Localization Warehouse
[l10n_br_stock_account](l10n_br_stock_account/) | 16.0.4.1.2 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> | Invoice from Picking (nota fiscal de remessa) and other WMS overrides
[l10n_br_stock_account_report](l10n_br_stock_account_report/) | 16.0.2.1.0 | <a href='https://github.com/mbcosta'><img src='https://github.com/mbcosta.png' width='32' height='32' style='border-radius:50%;' alt='mbcosta'/></a> | P7 Stock Valuation Report
[l10n_br_zip](l10n_br_zip/) | 16.0.2.7.0 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Brazilian Localisation ZIP Codes
[spec_driven_model](spec_driven_model/) | 16.0.3.1.5 | <a href='https://github.com/rvalyi'><img src='https://github.com/rvalyi.png' width='32' height='32' style='border-radius:50%;' alt='rvalyi'/></a> | XML binding for Odoo: XML to Odoo models and models to XML.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-croatia


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-croatia&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-croatia/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-croatia/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-croatia/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-croatia/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-croatia/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-croatia)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-croatia-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-croatia-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-croatia

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[currency_rate_update_hr_hnb](currency_rate_update_hr_hnb/) | 16.0.1.0.0 |  | Update exchange rates using Croatia HNB
[l10n_hr_bank](l10n_hr_bank/) | 16.0.1.0.1 |  | Croatia Banking localization
[l10n_hr_base](l10n_hr_base/) | 16.0.1.0.1 |  | Croatia base localization data
[l10n_hr_city](l10n_hr_city/) | 16.0.1.0.1 |  | Adds location data for Croatia - Cities, post offices etc.
[l10n_hr_nkd](l10n_hr_nkd/) | 16.0.1.0.1 |  | Hrvatska - Nacionalna Klasifikacija Djelatnosti

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-france&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-france/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-france/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-france/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-france/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-france/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-france)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-france-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-france-16-0/?utm_source=widget)

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
[account_balance_ebp_csv_export](account_balance_ebp_csv_export/) | 16.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Account Balance EBP CSV export
[account_banking_fr_lcr](account_banking_fr_lcr/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Create French LCR CFONB files
[account_statement_import_fr_cfonb](account_statement_import_fr_cfonb/) | 16.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Import CFONB bank statements files in Odoo
[l10n_fr_account_invoice_facturx](l10n_fr_account_invoice_facturx/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | France-specific module to generate Factur-X invoices
[l10n_fr_account_invoice_import_facturx](l10n_fr_account_invoice_import_facturx/) | 16.0.1.3.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | France-specific module to import Factur-X invoices
[l10n_fr_account_invoice_import_simple_pdf](l10n_fr_account_invoice_import_simple_pdf/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Invoice import simple PDF: match partners using SIREN
[l10n_fr_account_tax_unece](l10n_fr_account_tax_unece/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Auto-configure UNECE params on French taxes
[l10n_fr_account_vat_return](l10n_fr_account_vat_return/) | 16.0.8.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | VAT return for France: CA3, 3310-A, 3519
[l10n_fr_account_vat_return_einvoice_generate](l10n_fr_account_vat_return_einvoice_generate/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Glue module between account_einvoice_generate and l10n_fr_account_vat_return
[l10n_fr_account_vat_return_teledec](l10n_fr_account_vat_return_teledec/) | 16.0.3.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Teletransmit CA3 via Teledec.fr (subscription required)
[l10n_fr_business_document_import](l10n_fr_business_document_import/) | 16.0.1.2.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adapt the module base_business_document_import for France
[l10n_fr_chorus_account](l10n_fr_chorus_account/) | 16.0.2.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Generate Chorus-compliant e-invoices and transmit them via the Chorus API
[l10n_fr_chorus_facturx](l10n_fr_chorus_facturx/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Generate Chorus-compliant Factur-X invoices
[l10n_fr_chorus_sale](l10n_fr_chorus_sale/) | 16.0.2.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add checks on sale orders for Chorus Pro
[l10n_fr_cog](l10n_fr_cog/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add Code Officiel Géographique (COG) on countries
[l10n_fr_das2](l10n_fr_das2/) | 16.0.4.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | DAS2 (France)
[l10n_fr_department](l10n_fr_department/) | 16.0.1.1.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Populate Database with French Departments (Départements)
[l10n_fr_department_oversea](l10n_fr_department_oversea/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Populate Database with overseas French Departments (Départements d'outre-mer)
[l10n_fr_department_product_origin](l10n_fr_department_product_origin/) | 16.0.1.0.0 |  | Product Origin (French Departments)
[l10n_fr_fec_oca](l10n_fr_fec_oca/) | 16.0.1.2.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Fichier d'Échange Informatisé (FEC) for France
[l10n_fr_hr_check_ssnid](l10n_fr_hr_check_ssnid/) | 16.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Check validity of Social Security Numbers in French companies
[l10n_fr_intrastat_product](l10n_fr_intrastat_product/) | 16.0.2.3.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | EMEBI (ex-DEB) for France
[l10n_fr_intrastat_service](l10n_fr_intrastat_service/) | 16.0.1.6.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Module for Intrastat service reporting (DES) for France
[l10n_fr_mis_reports](l10n_fr_mis_reports/) | 16.0.1.0.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | MIS Report templates for the French P&L and Balance Sheets
[l10n_fr_oca](l10n_fr_oca/) | 16.0.3.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Fork of l10n_fr: fewer taxes, ready for OCA VAT return for France
[l10n_fr_pos_caisse_ap_ip](l10n_fr_pos_caisse_ap_ip/) | 16.0.1.4.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add support for Caisse-AP payment protocol used in France
[l10n_fr_pos_cert_update_draft_order_line](l10n_fr_pos_cert_update_draft_order_line/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | fixes the French certification module implemented by Odoo, authorizing the modification of draft sales lines.
[l10n_fr_siret](l10n_fr_siret/) | 16.0.1.4.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | French company identity numbers SIRET/SIREN/NIC
[l10n_fr_siret_lookup](l10n_fr_siret_lookup/) | 16.0.1.2.0 | <a href='https://github.com/remi-filament'><img src='https://github.com/remi-filament.png' width='32' height='32' style='border-radius:50%;' alt='remi-filament'/></a> <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Lookup partner via an API on the SIRENE directory
[l10n_fr_state](l10n_fr_state/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Populate Database with French States (Régions)

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-germany&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-germany/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-germany/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-germany/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-germany/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-germany/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-germany)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-germany-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-germany-16-0/?utm_source=widget)

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
[datev_export](datev_export/) | 16.0.1.0.1 |  | Export invoices and refunds as xml and pdf files zipped in DATEV format.
[datev_export_xml](datev_export_xml/) | 16.0.1.1.0 |  | Export invoices and refunds as xml and pdf files zipped in DATEV format.
[datev_import_csv_dtvf](datev_import_csv_dtvf/) | 16.0.1.1.0 |  | Import account moves generated by external software
[l10n_de_location_nuts](l10n_de_location_nuts/) | 16.0.1.1.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | NUTS specific options for German

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-indonesia


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-indonesia&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-indonesia/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-indonesia/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-indonesia/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-indonesia/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-indonesia/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-indonesia)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-indonesia-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-indonesia-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-indonesia

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[currency_rate_update_bi](currency_rate_update_bi/) | 16.0.1.0.0 | <a href='https://github.com/hitrosol'><img src='https://github.com/hitrosol.png' width='32' height='32' style='border-radius:50%;' alt='hitrosol'/></a> | Update exchange rates using Bank Indonesia (BI) official rates

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-iran&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-iran/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-iran/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-iran/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-iran/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-iran/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-iran)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-iran-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-iran-16-0/?utm_source=widget)

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
[l10n_ir_accounting](l10n_ir_accounting/) | 16.0.1.0.1 |  | iran accounting chart and localization.
[l10n_ir_hr_contract](l10n_ir_hr_contract/) | 16.0.1.0.0 |  | Iran Hr Contract
[l10n_ir_states](l10n_ir_states/) | 16.0.1.0.0 |  | Add Iran States and Cities

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# Odoo Italia Modules
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-italy&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-italy/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-italy/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-italy/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-italy/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-italy/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-italy)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-italy-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-italy-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Addons concerning Odoo Italian Localization.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_vat_period_end_statement](account_vat_period_end_statement/) | 16.0.1.3.2 |  | Allow to create the 'VAT Statement'.
[currency_rate_update_boi](currency_rate_update_boi/) | 16.0.1.0.1 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Update exchange rates using www.bancaditalia.it
[fiscal_epos_print](fiscal_epos_print/) | 16.0.1.0.1 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | ePOS-Print XML Fiscal Printer Driver - Stampanti Epson compatibili: FP81II, FP90III
[l10n_it_abicab](l10n_it_abicab/) | 16.0.1.0.1 | <a href='https://github.com/Borruso'><img src='https://github.com/Borruso.png' width='32' height='32' style='border-radius:50%;' alt='Borruso'/></a> | Base Bank ABI/CAB codes
[l10n_it_accompanying_invoice](l10n_it_accompanying_invoice/) | 16.0.1.0.1 |  | Stampa della fattura accompagnatoria
[l10n_it_account](l10n_it_account/) | 16.0.2.0.0 |  | Modulo base usato come dipendenza di altri moduli contabili
[l10n_it_account_stamp](l10n_it_account_stamp/) | 16.0.1.3.3 |  | Gestione automatica dell'imposta di bollo
[l10n_it_account_tax_kind](l10n_it_account_tax_kind/) | 16.0.1.0.1 |  | Gestione natura delle aliquote IVA
[l10n_it_amount_to_text](l10n_it_amount_to_text/) | 16.0.1.0.0 |  | Localizza le valute in italiano per amount_to_text
[l10n_it_appointment_code](l10n_it_appointment_code/) | 16.0.1.0.0 |  | Aggiunge la tabella dei codici carica da usare nelle dichiarazioni fiscali italiane
[l10n_it_asset_management](l10n_it_asset_management/) | 16.0.1.7.0 |  | Gestione Cespiti
[l10n_it_ateco](l10n_it_ateco/) | 16.0.1.1.1 |  | ITA - Codici Ateco
[l10n_it_bill_of_entry](l10n_it_bill_of_entry/) | 16.0.1.0.4 |  | ITA - Bolle doganali
[l10n_it_central_journal_reportlab](l10n_it_central_journal_reportlab/) | 16.0.1.0.9 | <a href='https://github.com/MarcoCalcagni'><img src='https://github.com/MarcoCalcagni.png' width='32' height='32' style='border-radius:50%;' alt='MarcoCalcagni'/></a> <a href='https://github.com/Borruso'><img src='https://github.com/Borruso.png' width='32' height='32' style='border-radius:50%;' alt='Borruso'/></a> | ITA - Libro giornale - Reportlab
[l10n_it_declaration_of_intent](l10n_it_declaration_of_intent/) | 16.0.1.1.2 |  | Gestione dichiarazioni di intento
[l10n_it_delivery_note](l10n_it_delivery_note/) | 16.0.1.5.5 | <a href='https://github.com/MarcoCalcagni'><img src='https://github.com/MarcoCalcagni.png' width='32' height='32' style='border-radius:50%;' alt='MarcoCalcagni'/></a> <a href='https://github.com/aleuffre'><img src='https://github.com/aleuffre.png' width='32' height='32' style='border-radius:50%;' alt='aleuffre'/></a> <a href='https://github.com/renda-dev'><img src='https://github.com/renda-dev.png' width='32' height='32' style='border-radius:50%;' alt='renda-dev'/></a> | Crea, gestisce e fattura i DDT partendo dalle consegne
[l10n_it_delivery_note_base](l10n_it_delivery_note_base/) | 16.0.1.0.2 | <a href='https://github.com/MarcoCalcagni'><img src='https://github.com/MarcoCalcagni.png' width='32' height='32' style='border-radius:50%;' alt='MarcoCalcagni'/></a> <a href='https://github.com/Borruso'><img src='https://github.com/Borruso.png' width='32' height='32' style='border-radius:50%;' alt='Borruso'/></a> | Crea e gestisce tabelle principali per gestire i DDT
[l10n_it_delivery_note_batch](l10n_it_delivery_note_batch/) | 16.0.1.1.0 | <a href='https://github.com/MarcoCalcagni'><img src='https://github.com/MarcoCalcagni.png' width='32' height='32' style='border-radius:50%;' alt='MarcoCalcagni'/></a> <a href='https://github.com/TheMule71'><img src='https://github.com/TheMule71.png' width='32' height='32' style='border-radius:50%;' alt='TheMule71'/></a> <a href='https://github.com/Borruso'><img src='https://github.com/Borruso.png' width='32' height='32' style='border-radius:50%;' alt='Borruso'/></a> <a href='https://github.com/aleuffre'><img src='https://github.com/aleuffre.png' width='32' height='32' style='border-radius:50%;' alt='aleuffre'/></a> <a href='https://github.com/PicchiSeba'><img src='https://github.com/PicchiSeba.png' width='32' height='32' style='border-radius:50%;' alt='PicchiSeba'/></a> <a href='https://github.com/renda-dev'><img src='https://github.com/renda-dev.png' width='32' height='32' style='border-radius:50%;' alt='renda-dev'/></a> | Crea i DDT partendo da gruppi di prelievi
[l10n_it_delivery_note_order_link](l10n_it_delivery_note_order_link/) | 16.0.1.0.1 | <a href='https://github.com/andreampiovesana'><img src='https://github.com/andreampiovesana.png' width='32' height='32' style='border-radius:50%;' alt='andreampiovesana'/></a> | Crea collegamento tra i DDT e ordine di vendita/acquisto
[l10n_it_fatturapa](l10n_it_fatturapa/) | 16.0.1.4.1 |  | Fatture elettroniche
[l10n_it_fatturapa_auto_sale_order](l10n_it_fatturapa_auto_sale_order/) | 16.0.1.0.0 |  | Automatically set sale orders as related documents
[l10n_it_fatturapa_export_zip](l10n_it_fatturapa_export_zip/) | 16.0.1.0.0 | <a href='https://github.com/sergiocorato'><img src='https://github.com/sergiocorato.png' width='32' height='32' style='border-radius:50%;' alt='sergiocorato'/></a> | Permette di esportare in uno ZIP diversi file XML di fatture elettroniche
[l10n_it_fatturapa_fatturhello](l10n_it_fatturapa_fatturhello/) | 16.0.1.0.0 | <a href='https://github.com/aleuffre'><img src='https://github.com/aleuffre.png' width='32' height='32' style='border-radius:50%;' alt='aleuffre'/></a> <a href='https://github.com/SirPyTech'><img src='https://github.com/SirPyTech.png' width='32' height='32' style='border-radius:50%;' alt='SirPyTech'/></a> | Invio e ricezione fatture elettroniche tramite Fatturhello
[l10n_it_fatturapa_import_zip](l10n_it_fatturapa_import_zip/) | 16.0.1.3.0 |  | Permette di importare in uno ZIP diversi file XML di fatture elettroniche
[l10n_it_fatturapa_import_zip_in_rc](l10n_it_fatturapa_import_zip_in_rc/) | 16.0.1.0.0 | <a href='https://github.com/SirAionTech'><img src='https://github.com/SirAionTech.png' width='32' height='32' style='border-radius:50%;' alt='SirAionTech'/></a> | Importare fatture elettroniche con inversione contabile da un file ZIP.
[l10n_it_fatturapa_in](l10n_it_fatturapa_in/) | 16.0.1.5.8 | <a href='https://github.com/MarcoCalcagni'><img src='https://github.com/MarcoCalcagni.png' width='32' height='32' style='border-radius:50%;' alt='MarcoCalcagni'/></a> <a href='https://github.com/Borruso'><img src='https://github.com/Borruso.png' width='32' height='32' style='border-radius:50%;' alt='Borruso'/></a> | Ricezione fatture elettroniche
[l10n_it_fatturapa_in_purchase](l10n_it_fatturapa_in_purchase/) | 16.0.1.0.1 | <a href='https://github.com/MarcoCalcagni'><img src='https://github.com/MarcoCalcagni.png' width='32' height='32' style='border-radius:50%;' alt='MarcoCalcagni'/></a> <a href='https://github.com/Borruso'><img src='https://github.com/Borruso.png' width='32' height='32' style='border-radius:50%;' alt='Borruso'/></a> | Modulo ponte tra ricezione fatture elettroniche e acquisti
[l10n_it_fatturapa_in_rc](l10n_it_fatturapa_in_rc/) | 16.0.1.0.2 | <a href='https://github.com/sergiocorato'><img src='https://github.com/sergiocorato.png' width='32' height='32' style='border-radius:50%;' alt='sergiocorato'/></a> | Modulo ponte tra e-fattura in acquisto e inversione contabile
[l10n_it_fatturapa_out](l10n_it_fatturapa_out/) | 16.0.1.9.1 |  | Emissione fatture elettroniche
[l10n_it_fatturapa_out_di](l10n_it_fatturapa_out_di/) | 16.0.1.0.3 |  | Dichiarazioni d'intento in fatturapa
[l10n_it_fatturapa_out_dn](l10n_it_fatturapa_out_dn/) | 16.0.1.1.0 |  | DDT in fatture elettroniche
[l10n_it_fatturapa_out_oss](l10n_it_fatturapa_out_oss/) | 16.0.1.0.2 |  | OSS in fatturapa
[l10n_it_fatturapa_out_rc](l10n_it_fatturapa_out_rc/) | 16.0.1.0.3 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Integrazione l10n_it_fatturapa_out e l10n_it_reverse_charge
[l10n_it_fatturapa_out_sp](l10n_it_fatturapa_out_sp/) | 16.0.1.0.0 |  | Scissione pagamenti in fatturapa
[l10n_it_fatturapa_out_stamp](l10n_it_fatturapa_out_stamp/) | 16.0.1.0.1 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Modulo ponte tra emissione fatture elettroniche e imposta di bollo
[l10n_it_fatturapa_out_triple_discount](l10n_it_fatturapa_out_triple_discount/) | 16.0.1.0.0 |  | Modulo ponte tra emissione fatture elettroniche e sconto triplo
[l10n_it_fatturapa_out_wt](l10n_it_fatturapa_out_wt/) | 16.0.1.0.2 |  | Modulo ponte tra emissione fatture elettroniche e ritenute.
[l10n_it_fatturapa_pec](l10n_it_fatturapa_pec/) | 16.0.1.2.4 |  | Invio fatture elettroniche tramite PEC
[l10n_it_fatturapa_sale](l10n_it_fatturapa_sale/) | 16.0.1.0.1 |  | Aggiunge alcuni dati per la fatturazione elettronica nell'ordine di vendita
[l10n_it_fatturapa_sdicoop](l10n_it_fatturapa_sdicoop/) | 16.0.1.1.0 |  | Invio fatture elettroniche tramite SDICoop
[l10n_it_financial_statement_eu](l10n_it_financial_statement_eu/) | 16.0.1.0.1 | <a href='https://github.com/mktsrl'><img src='https://github.com/mktsrl.png' width='32' height='32' style='border-radius:50%;' alt='mktsrl'/></a> | ITA - Bilancio UE con XBRL
[l10n_it_financial_statements_report](l10n_it_financial_statements_report/) | 16.0.1.1.0 |  | Rendicontazione .pdf e .xls per stato patrimoniale e conto economico a sezioni contrapposte
[l10n_it_fiscal_document_type](l10n_it_fiscal_document_type/) | 16.0.1.1.0 |  | ITA - Tipi di documento fiscale per dichiarativi
[l10n_it_fiscal_payment_term](l10n_it_fiscal_payment_term/) | 16.0.1.0.0 |  | Condizioni di pagamento delle fatture elettroniche
[l10n_it_fiscalcode](l10n_it_fiscalcode/) | 16.0.1.0.4 |  | ITA - Codice fiscale
[l10n_it_fiscalcode_sale](l10n_it_fiscalcode_sale/) | 16.0.1.0.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Mostra il codice fiscale del cliente nella stampa del preventivo
[l10n_it_hr_payroll_document](l10n_it_hr_payroll_document/) | 16.0.1.0.0 | <a href='https://github.com/SirPyTech'><img src='https://github.com/SirPyTech.png' width='32' height='32' style='border-radius:50%;' alt='SirPyTech'/></a> | Spacchetta e invia agli impiegati le buste paga.
[l10n_it_intrastat](l10n_it_intrastat/) | 16.0.1.2.2 |  | Riclassificazione merci e servizi per dichiarazioni Intrastat
[l10n_it_intrastat_statement](l10n_it_intrastat_statement/) | 16.0.1.3.4 |  | Dichiarazione Intrastat per l'Agenzia delle Dogane
[l10n_it_ipa](l10n_it_ipa/) | 16.0.1.0.1 |  | ITA - Codice IPA
[l10n_it_location_nuts](l10n_it_location_nuts/) | 16.0.1.0.0 |  | Opzioni NUTS specifiche per l'Italia
[l10n_it_payment_reason](l10n_it_payment_reason/) | 16.0.1.0.0 |  | Aggiunge la tabella delle causali di pagamento da usare ad esempio nelle ritenute d'acconto
[l10n_it_pec](l10n_it_pec/) | 16.0.1.0.0 |  | Aggiunge il campo email PEC al partner
[l10n_it_pos_fiscalcode](l10n_it_pos_fiscalcode/) | 16.0.1.0.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Gestione codice fiscale del cliente all'interno dell'interfaccia del POS
[l10n_it_rea](l10n_it_rea/) | 16.0.1.0.0 |  | Gestisce i campi del Repertorio Economico Amministrativo
[l10n_it_reverse_charge](l10n_it_reverse_charge/) | 16.0.1.0.11 |  | Inversione contabile
[l10n_it_reverse_charge_start_end_dates](l10n_it_reverse_charge_start_end_dates/) | 16.0.1.0.0 |  | Gestione delle date di competenza per le autofatture in reverse charge
[l10n_it_riba_oca](l10n_it_riba_oca/) | 16.0.1.10.2 |  | Ricevute bancarie
[l10n_it_sct_cbi](l10n_it_sct_cbi/) | 16.0.1.0.2 | <a href='https://github.com/monen17'><img src='https://github.com/monen17.png' width='32' height='32' style='border-radius:50%;' alt='monen17'/></a> | Usare gli standard CBI per SEPA Credit Transfer
[l10n_it_sdi_channel](l10n_it_sdi_channel/) | 16.0.1.1.2 | <a href='https://github.com/sergiocorato'><img src='https://github.com/sergiocorato.png' width='32' height='32' style='border-radius:50%;' alt='sergiocorato'/></a> | Aggiunge il canale di invio/ricezione dei file XML attraverso lo SdI
[l10n_it_split_payment](l10n_it_split_payment/) | 16.0.1.1.2 |  | Scissione pagamenti
[l10n_it_vat_payability](l10n_it_vat_payability/) | 16.0.1.0.0 |  | ITA - Esigibilità IVA
[l10n_it_vat_registries](l10n_it_vat_registries/) | 16.0.1.5.0 |  | ITA - Registri IVA
[l10n_it_vat_registries_rc](l10n_it_vat_registries_rc/) | 16.0.1.0.1 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Integrazione l10n_it_vat_registries e l10n_it_reverse_charge
[l10n_it_vat_registries_split_payment](l10n_it_vat_registries_split_payment/) | 16.0.1.0.0 |  | Modulo di congiunzione tra registri IVA e scissione dei pagamenti
[l10n_it_vat_settlement_date](l10n_it_vat_settlement_date/) | 16.0.1.1.0 |  | Settlement date for VAT Statement
[l10n_it_vat_settlement_date_rc](l10n_it_vat_settlement_date_rc/) | 16.0.1.0.0 |  | Use VAT Settlement Date in reverse charge.
[l10n_it_vat_statement_communication](l10n_it_vat_statement_communication/) | 16.0.1.0.1 |  | Comunicazione liquidazione IVA ed esportazione file xmlconforme alle specifiche dell'Agenzia delle Entrate
[l10n_it_vat_statement_split_payment](l10n_it_vat_statement_split_payment/) | 16.0.1.0.0 |  | Migliora la liquidazione dell'IVA tenendo in considerazione la scissione dei pagamenti
[l10n_it_website_portal_fatturapa](l10n_it_website_portal_fatturapa/) | 16.0.1.0.0 |  | Add fatturapa fields and checks in frontend user's details
[l10n_it_website_portal_fiscalcode](l10n_it_website_portal_fiscalcode/) | 16.0.1.0.0 |  | Add fiscal code to details of frontend user
[l10n_it_website_portal_ipa](l10n_it_website_portal_ipa/) | 16.0.1.0.1 |  | Aggiunge l'indice PA (IPA) tra i dettagli dell'utente nel portale.
[l10n_it_website_sale_fiscalcode](l10n_it_website_sale_fiscalcode/) | 16.0.1.0.0 |  | Website Sale FiscalCode
[l10n_it_withholding_tax](l10n_it_withholding_tax/) | 16.0.1.2.2 |  | ITA - Ritenute d'acconto
[l10n_it_withholding_tax_financial_report](l10n_it_withholding_tax_financial_report/) | 16.0.1.0.2 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Integrazione Ritenute d'acconto e Rendiconti contabili
[l10n_it_withholding_tax_payment](l10n_it_withholding_tax_payment/) | 16.0.1.1.0 |  | Gestisce le ritenute sulle fatture e sui pagamenti
[l10n_it_withholding_tax_payment_order](l10n_it_withholding_tax_payment_order/) | 16.0.1.0.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Integrazione Ritenute d'acconto e Ordini di pagamento
[l10n_it_withholding_tax_reason](l10n_it_withholding_tax_reason/) | 16.0.1.0.0 |  | ITA - Causali pagamento per ritenute d'acconto

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# l10n-japan
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-japan&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-japan/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-japan/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-japan/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-japan/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-japan/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-japan)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-japan-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-japan-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Odoo日本向けローカリゼーション (l10n-japan)

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_payment_term_cutoff_day](account_payment_term_cutoff_day/) | 16.0.1.1.0 |  | Account Payment Term Cutoff Day
[account_tax_rounding_method](account_tax_rounding_method/) | 16.0.1.0.0 |  | Account Tax Rounding Method
[l10n_jp_account_report_registration_number](l10n_jp_account_report_registration_number/) | 16.0.1.0.0 |  | Japan Account Report Registration Number
[l10n_jp_address_layout](l10n_jp_address_layout/) | 16.0.1.0.0 |  | Japan Address Layout
[l10n_jp_country_state](l10n_jp_country_state/) | 16.0.1.0.0 |  | Japan Country States
[l10n_jp_partner_title_qweb](l10n_jp_partner_title_qweb/) | 16.0.1.0.0 |  | Japan Partner Title QWeb
[l10n_jp_partner_zip_address](l10n_jp_partner_zip_address/) | 16.0.1.0.0 |  | Japan Partner Zip Address
[l10n_jp_summary_invoice](l10n_jp_summary_invoice/) | 16.0.1.5.0 |  | Japan Summary Invoice
[report_alternative_layout](report_alternative_layout/) | 16.0.1.3.0 |  | Report Alternative Layout

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-mexico&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-mexico/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-mexico/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-mexico/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-mexico/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-mexico/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-mexico)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-mexico-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-mexico-16-0/?utm_source=widget)

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
[l10n_mx_res_partner_csf](l10n_mx_res_partner_csf/) | 16.0.1.0.3 |  | Scan and extract information from CSF

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# l10n-netherlands
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-netherlands&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-netherlands/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-netherlands/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-netherlands/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-netherlands/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-netherlands/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-netherlands)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-netherlands-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-netherlands-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Odoo Dutch Localization

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_nl_account_tax_unece](l10n_nl_account_tax_unece/) | 16.0.1.0.0 |  | Auto-configure UNECE params on Dutch taxes
[l10n_nl_bank](l10n_nl_bank/) | 16.0.1.0.0 |  | Import all Dutch banks with BIC code
[l10n_nl_bsn](l10n_nl_bsn/) | 16.0.1.0.0 | <a href='https://github.com/astirpe'><img src='https://github.com/astirpe.png' width='32' height='32' style='border-radius:50%;' alt='astirpe'/></a> | Burgerservicenummer (BSN) for Partners
[l10n_nl_oin](l10n_nl_oin/) | 16.0.1.0.0 | <a href='https://github.com/astirpe'><img src='https://github.com/astirpe.png' width='32' height='32' style='border-radius:50%;' alt='astirpe'/></a> | Adds Dutch OIN field
[l10n_nl_partner_name](l10n_nl_partner_name/) | 16.0.1.0.1 |  | Adapt parter names to Dutch conventions (support infix)
[l10n_nl_postcode](l10n_nl_postcode/) | 16.0.1.0.0 | <a href='https://github.com/astirpe'><img src='https://github.com/astirpe.png' width='32' height='32' style='border-radius:50%;' alt='astirpe'/></a> | Dutch postcode validation for Partners
[l10n_nl_tax_statement](l10n_nl_tax_statement/) | 16.0.1.0.2 |  | Netherlands BTW Statement
[l10n_nl_tax_statement_date_range](l10n_nl_tax_statement_date_range/) | 16.0.1.0.0 |  | Netherlands BTW Statement - Date range
[l10n_nl_tax_statement_icp](l10n_nl_tax_statement_icp/) | 16.0.1.1.0 |  | Netherlands ICP Statement
[l10n_nl_tax_statement_icp_split](l10n_nl_tax_statement_icp_split/) | 16.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Manage your BTW and ICP statements separately
[l10n_nl_xaf_auditfile_export](l10n_nl_xaf_auditfile_export/) | 16.0.2.0.0 |  | Export XAF auditfiles for Dutch tax authorities

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-paraguay


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# l10n-paraguay
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-paraguay&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-paraguay/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-paraguay/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-paraguay/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-paraguay/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-paraguay/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-paraguay)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-paraguay-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-paraguay-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

l10n-paraguay

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_py](l10n_py/) | 16.0.1.1.0 |  | Localización contable para Paraguay
[l10n_py_account](l10n_py_account/) | 16.0.2.0.0 |  | Accounting extensions for Paraguay localization
[l10n_py_base](l10n_py_base/) | 16.0.1.2.0 |  | Base localization data for Paraguay
[l10n_py_edi_base](l10n_py_edi_base/) | 16.0.9.0.0 |  | Base module for Electronic Invoicing in Paraguay
[l10n_py_edi_sifen](l10n_py_edi_sifen/) | 16.0.13.0.0 |  | Direct SIFEN transmission via pysifen library

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-poland


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-poland&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-poland/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-poland/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-poland/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-poland/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-poland/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-poland)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-poland-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-poland-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-poland

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[currency_rate_update_nbp](currency_rate_update_nbp/) | 16.0.1.0.1 |  | Allows to download currency exchange rates from National bank of Poland

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-portugal&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-portugal/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-portugal/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-portugal/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-portugal/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-portugal/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-portugal)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-portugal-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-portugal-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[l10n_pt_account_invoicexpress](l10n_pt_account_invoicexpress/) | 16.0.1.3.0 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Portuguese certified invoices using InvoiceXpress
[l10n_pt_stock_invoicexpress](l10n_pt_stock_invoicexpress/) | 16.0.1.0.2 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Portuguese legal transport and shipping documents (Guias de Transporte e Guias de Remessa) generated with InvoiceXpress
[l10n_pt_stock_vehicle_daily](l10n_pt_stock_vehicle_daily/) | 16.0.1.0.0 |  | Daily documente with vehicle content, to communicate to Portuguese Tax Authorities
[l10n_pt_vat](l10n_pt_vat/) | 16.0.1.3.0 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Portuguese VAT requirements extensions

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-romania&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-romania/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-romania/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-romania/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-romania/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-romania/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-romania)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-romania-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-romania-16-0/?utm_source=widget)

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
[currency_rate_update_RO_BNR](currency_rate_update_RO_BNR/) | 16.0.1.5.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Currency Rate Update National Bank of Romania service
[l10n_ro_account](l10n_ro_account/) | 16.0.1.7.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Account
[l10n_ro_account_anaf_sync](l10n_ro_account_anaf_sync/) | 16.0.1.19.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Account ANAF Sync
[l10n_ro_account_bank_statement_import_mt940_alpha](l10n_ro_account_bank_statement_import_mt940_alpha/) | 16.0.1.2.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | MT940 Alpha Format Bank Statements Import
[l10n_ro_account_bank_statement_import_mt940_base](l10n_ro_account_bank_statement_import_mt940_base/) | 16.0.1.4.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - MT940 Bank Statements Import
[l10n_ro_account_bank_statement_import_mt940_bcr](l10n_ro_account_bank_statement_import_mt940_bcr/) | 16.0.1.3.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | MT940 BCR Format Bank Statements Import
[l10n_ro_account_bank_statement_import_mt940_brd](l10n_ro_account_bank_statement_import_mt940_brd/) | 16.0.1.3.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Import bank statements from BRD
[l10n_ro_account_bank_statement_import_mt940_ing](l10n_ro_account_bank_statement_import_mt940_ing/) | 16.0.1.4.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | MT940 ING Format Bank Statements Import
[l10n_ro_account_bank_statement_import_mt940_rffsn](l10n_ro_account_bank_statement_import_mt940_rffsn/) | 16.0.1.2.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Import bank statements from Raiffeisen
[l10n_ro_account_bank_statement_report](l10n_ro_account_bank_statement_report/) | 16.0.1.4.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Bank Statement Report
[l10n_ro_account_edi_ubl](l10n_ro_account_edi_ubl/) | 16.0.1.89.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - eFactura - Account EDI UBL
[l10n_ro_account_edit_currency_rate](l10n_ro_account_edit_currency_rate/) | 16.0.1.2.0 | <a href='https://github.com/mcojocaru'><img src='https://github.com/mcojocaru.png' width='32' height='32' style='border-radius:50%;' alt='mcojocaru'/></a> | Romania - Invoice Edit Currency Rate
[l10n_ro_account_period_close](l10n_ro_account_period_close/) | 16.0.3.7.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Account Period Closing
[l10n_ro_account_report_invoice](l10n_ro_account_report_invoice/) | 16.0.1.5.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Invoice Report
[l10n_ro_city](l10n_ro_city/) | 16.0.3.8.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - City
[l10n_ro_config](l10n_ro_config/) | 16.0.1.18.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Localization Install and Config Applications
[l10n_ro_dvi](l10n_ro_dvi/) | 16.0.1.9.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - DVI
[l10n_ro_etransport](l10n_ro_etransport/) | 16.0.0.12.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - E-Trasnport
[l10n_ro_fiscal_validation](l10n_ro_fiscal_validation/) | 16.0.1.6.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Fiscal Validation
[l10n_ro_message_spv](l10n_ro_message_spv/) | 16.0.1.18.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Mesaje SPV
[l10n_ro_nondeductible_vat](l10n_ro_nondeductible_vat/) | 16.0.0.4.0 | <a href='https://github.com/adrian-dks'><img src='https://github.com/adrian-dks.png' width='32' height='32' style='border-radius:50%;' alt='adrian-dks'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Nondeductible VAT
[l10n_ro_partner_create_by_vat](l10n_ro_partner_create_by_vat/) | 16.0.1.10.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Partner Create by VAT
[l10n_ro_partner_unique](l10n_ro_partner_unique/) | 16.0.1.1.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Creates a rule for vat and nrc unique for partners.
[l10n_ro_payment_receipt_report](l10n_ro_payment_receipt_report/) | 16.0.1.4.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Payment Receipt Report
[l10n_ro_payment_to_statement](l10n_ro_payment_to_statement/) | 16.0.2.13.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Add payment to cash statement
[l10n_ro_pos](l10n_ro_pos/) | 16.0.2.5.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Point of Sale
[l10n_ro_stock](l10n_ro_stock/) | 16.0.0.4.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock
[l10n_ro_stock_account](l10n_ro_stock_account/) | 16.0.1.28.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Accounting
[l10n_ro_stock_account_date](l10n_ro_stock_account_date/) | 16.0.1.8.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Accounting Date
[l10n_ro_stock_account_date_wizard](l10n_ro_stock_account_date_wizard/) | 16.0.1.4.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Accounting Date Wizard
[l10n_ro_stock_account_landed_cost](l10n_ro_stock_account_landed_cost/) | 16.0.1.27.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Accounting Landed Cost
[l10n_ro_stock_account_mrp](l10n_ro_stock_account_mrp/) | 16.0.0.4.0 | <a href='https://github.com/adrian-dks'><img src='https://github.com/adrian-dks.png' width='32' height='32' style='border-radius:50%;' alt='adrian-dks'/></a> | Fix mrp_production cost.
[l10n_ro_stock_account_notice](l10n_ro_stock_account_notice/) | 16.0.4.12.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/mcojocaru'><img src='https://github.com/mcojocaru.png' width='32' height='32' style='border-radius:50%;' alt='mcojocaru'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Stock Accounting Notice
[l10n_ro_stock_account_reception_in_progress](l10n_ro_stock_account_reception_in_progress/) | 16.0.0.5.0 | <a href='https://github.com/nct74'><img src='https://github.com/nct74.png' width='32' height='32' style='border-radius:50%;' alt='nct74'/></a> <a href='https://github.com/vasi26ro'><img src='https://github.com/vasi26ro.png' width='32' height='32' style='border-radius:50%;' alt='vasi26ro'/></a> | Romania - Stock Accounting Reception In progress
[l10n_ro_stock_account_tracking](l10n_ro_stock_account_tracking/) | 16.0.1.28.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Accounting
[l10n_ro_stock_picking_comment_template](l10n_ro_stock_picking_comment_template/) | 16.0.0.5.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | This model is going to add a a header and a footer at picking report depeding on the operation type.
[l10n_ro_stock_picking_valued_report](l10n_ro_stock_picking_valued_report/) | 16.0.0.8.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Picking Valued Report
[l10n_ro_stock_price_difference](l10n_ro_stock_price_difference/) | 16.0.5.10.0 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> <a href='https://github.com/mcojocaru'><img src='https://github.com/mcojocaru.png' width='32' height='32' style='border-radius:50%;' alt='mcojocaru'/></a> <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> | Romania - Stock Accounting Price Difference
[l10n_ro_stock_report](l10n_ro_stock_report/) | 16.0.6.15.0 | <a href='https://github.com/dhongu'><img src='https://github.com/dhongu.png' width='32' height='32' style='border-radius:50%;' alt='dhongu'/></a> <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - Stock Report (Fisa Magazie)
[l10n_ro_vat_on_payment](l10n_ro_vat_on_payment/) | 16.0.1.12.1 | <a href='https://github.com/feketemihai'><img src='https://github.com/feketemihai.png' width='32' height='32' style='border-radius:50%;' alt='feketemihai'/></a> | Romania - VAT on Payment

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-spain&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-spain/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-spain/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-spain/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-spain/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-spain/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-spain)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-spain-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-spain-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[delivery_gls_asm](delivery_gls_asm/) | 16.0.1.1.5 | <a href='https://github.com/hildickethan'><img src='https://github.com/hildickethan.png' width='32' height='32' style='border-radius:50%;' alt='hildickethan'/></a> | Delivery Carrier implementation for GLS with ASMRed API
[delivery_mrw](delivery_mrw/) | 16.0.1.0.0 |  | Delivery Carrier implementation for MRW with SAGEC API
[delivery_seur_atlas](delivery_seur_atlas/) | 16.0.1.0.0 |  | Integrate SEUR Atlas API
[l10n_es_account_asset](l10n_es_account_asset/) | 16.0.2.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Gestión de activos fijos para España
[l10n_es_account_banking_sepa_fsdd](l10n_es_account_banking_sepa_fsdd/) | 16.0.1.0.0 |  | Account Banking Sepa - FSDD (Anticipos de crédito)
[l10n_es_account_statement_import_n43](l10n_es_account_statement_import_n43/) | 16.0.1.1.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Importación de extractos bancarios españoles (Norma 43)
[l10n_es_aeat](l10n_es_aeat/) | 16.0.3.3.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Modulo base para declaraciones de la AEAT
[l10n_es_aeat_mod111](l10n_es_aeat_mod111/) | 16.0.1.1.1 |  | AEAT modelo 111
[l10n_es_aeat_mod115](l10n_es_aeat_mod115/) | 16.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | AEAT modelo 115
[l10n_es_aeat_mod123](l10n_es_aeat_mod123/) | 16.0.2.2.0 |  | AEAT modelo 123
[l10n_es_aeat_mod130](l10n_es_aeat_mod130/) | 16.0.1.0.2 |  | AEAT modelo 130
[l10n_es_aeat_mod190](l10n_es_aeat_mod190/) | 16.0.2.4.1 |  | AEAT modelo 190
[l10n_es_aeat_mod216](l10n_es_aeat_mod216/) | 16.0.2.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | AEAT modelo 216
[l10n_es_aeat_mod296](l10n_es_aeat_mod296/) | 16.0.1.1.1 |  | AEAT modelo 296
[l10n_es_aeat_mod303](l10n_es_aeat_mod303/) | 16.0.2.12.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | AEAT modelo 303
[l10n_es_aeat_mod303_oss](l10n_es_aeat_mod303_oss/) | 16.0.1.1.0 |  | AEAT modelo 303 - OSS
[l10n_es_aeat_mod303_vat_prorate](l10n_es_aeat_mod303_vat_prorate/) | 16.0.1.1.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Prorrata de IVA [303]
[l10n_es_aeat_mod347](l10n_es_aeat_mod347/) | 16.0.1.13.0 |  | AEAT modelo 347
[l10n_es_aeat_mod347_igic](l10n_es_aeat_mod347_igic/) | 16.0.1.0.2 | <a href='https://github.com/Christian-RB'><img src='https://github.com/Christian-RB.png' width='32' height='32' style='border-radius:50%;' alt='Christian-RB'/></a> | AEAT modelo 347 IGIC
[l10n_es_aeat_mod349](l10n_es_aeat_mod349/) | 16.0.1.4.4 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | AEAT modelo 349
[l10n_es_aeat_mod369](l10n_es_aeat_mod369/) | 16.0.1.1.2 |  | AEAT modelo 369
[l10n_es_aeat_mod390](l10n_es_aeat_mod390/) | 16.0.2.12.3 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | AEAT modelo 390
[l10n_es_aeat_mod390_oss](l10n_es_aeat_mod390_oss/) | 16.0.1.0.0 |  | AEAT modelo 390 - OSS
[l10n_es_aeat_mod592](l10n_es_aeat_mod592/) | 16.0.1.0.3 |  | AEAT modelo 592
[l10n_es_aeat_partner_check](l10n_es_aeat_partner_check/) | 16.0.1.1.0 |  | AEAT - Comprobación de Calidad de datos identificativos
[l10n_es_aeat_sii_force_type](l10n_es_aeat_sii_force_type/) | 16.0.2.0.1 |  | Force SII communication type on invoices
[l10n_es_aeat_sii_invoice_summary](l10n_es_aeat_sii_invoice_summary/) | 16.0.2.0.0 |  | Envio de factura simplificada resumen TPV a SII
[l10n_es_aeat_sii_match](l10n_es_aeat_sii_match/) | 16.0.2.0.2 | <a href='https://github.com/Abranes'><img src='https://github.com/Abranes.png' width='32' height='32' style='border-radius:50%;' alt='Abranes'/></a> <a href='https://github.com/Reyes4711-S73'><img src='https://github.com/Reyes4711-S73.png' width='32' height='32' style='border-radius:50%;' alt='Reyes4711-S73'/></a> | Sistema de comprobación y contraste de facturas enviadas al SII
[l10n_es_aeat_sii_oca](l10n_es_aeat_sii_oca/) | 16.0.2.5.9 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Suministro Inmediato de Información en el IVA
[l10n_es_aeat_sii_oss](l10n_es_aeat_sii_oss/) | 16.0.2.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Suministro Inmediato de Información en el IVA: OSS
[l10n_es_aeat_sii_taxfree](l10n_es_aeat_sii_taxfree/) | 16.0.2.0.2 |  | Régimen Especial de Viajeros - SII
[l10n_es_atc](l10n_es_atc/) | 16.0.1.0.2 |  | Modulo 'glue' de la AEAT para el menú de la ATC
[l10n_es_atc_mod415](l10n_es_atc_mod415/) | 16.0.1.0.1 | <a href='https://github.com/Christian-RB'><img src='https://github.com/Christian-RB.png' width='32' height='32' style='border-radius:50%;' alt='Christian-RB'/></a> | ATC Modelo 415
[l10n_es_atc_mod420](l10n_es_atc_mod420/) | 16.0.1.2.0 | <a href='https://github.com/Christian-RB'><img src='https://github.com/Christian-RB.png' width='32' height='32' style='border-radius:50%;' alt='Christian-RB'/></a> | ATC Modelo 420
[l10n_es_dua](l10n_es_dua/) | 16.0.1.0.0 |  | Importaciones con DUA
[l10n_es_dua_igic](l10n_es_dua_igic/) | 16.0.1.1.0 |  | Importaciones con DUA ATC
[l10n_es_dua_sii](l10n_es_dua_sii/) | 16.0.2.0.0 |  | Suministro Inmediato de Información de importaciones con DUA
[l10n_es_facturae](l10n_es_facturae/) | 16.0.1.13.1 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Creación de Facturae
[l10n_es_facturae_face](l10n_es_facturae_face/) | 16.0.1.3.3 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Envío de Facturae a FACe
[l10n_es_facturae_igic](l10n_es_facturae_igic/) | 16.0.1.0.0 | <a href='https://github.com/Christian-RB'><img src='https://github.com/Christian-RB.png' width='32' height='32' style='border-radius:50%;' alt='Christian-RB'/></a> | Creación de Facturae IGIC
[l10n_es_igic](l10n_es_igic/) | 16.0.1.5.0 |  | IGIC (Impuesto General Indirecto Canario
[l10n_es_igic_verifactu_oca](l10n_es_igic_verifactu_oca/) | 16.0.1.0.1 |  | Comunicación Veri*FACTU para IGIC
[l10n_es_intrastat_report](l10n_es_intrastat_report/) | 16.0.1.4.1 |  | Spanish Intrastat Product Declaration
[l10n_es_irnr](l10n_es_irnr/) | 16.0.1.2.1 |  | Retenciones IRNR (No residentes)
[l10n_es_irnr_sii](l10n_es_irnr_sii/) | 16.0.1.1.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Suministro Inmediato de Información de importaciones con IRNR
[l10n_es_location_nuts](l10n_es_location_nuts/) | 16.0.1.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | NUTS specific options for Spain
[l10n_es_mis_report](l10n_es_mis_report/) | 16.0.1.2.0 |  | Plantillas MIS Builder para informes contables españoles
[l10n_es_partner](l10n_es_partner/) | 16.0.2.2.5 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Adaptación de los clientes, proveedores y bancos para España
[l10n_es_partner_mercantil](l10n_es_partner_mercantil/) | 16.0.1.0.0 |  | Añade los datos del registro mercantil a la empresa
[l10n_es_payment_order_confirming_aef](l10n_es_payment_order_confirming_aef/) | 16.0.1.1.4 |  | Exportación de fichero bancario Confirming estándar AEF
[l10n_es_payment_order_confirming_sabadell](l10n_es_payment_order_confirming_sabadell/) | 16.0.1.0.2 |  | Exportación de fichero bancario Confirming para Banco Sabadell
[l10n_es_pos](l10n_es_pos/) | 16.0.1.0.3 |  | Punto de venta adaptado a la legislación española
[l10n_es_pos_by_device](l10n_es_pos_by_device/) | 16.0.1.0.2 | <a href='https://github.com/ao-landoo'><img src='https://github.com/ao-landoo.png' width='32' height='32' style='border-radius:50%;' alt='ao-landoo'/></a> | Múltiples dispositivos por sesión en el punto de venta
[l10n_es_pos_sii](l10n_es_pos_sii/) | 16.0.2.1.2 |  | Envío de pedidos del TPV al SII
[l10n_es_sigaus_account](l10n_es_sigaus_account/) | 16.0.1.0.3 |  | Sistema de gestión de aceites industriales usados en España - Facturación
[l10n_es_sigaus_purchase](l10n_es_sigaus_purchase/) | 16.0.1.0.3 |  | Sistema de gestión de aceites industriales usados en España - Compras
[l10n_es_sigaus_sale](l10n_es_sigaus_sale/) | 16.0.1.0.3 |  | Sist. gestión aceites industriales usados en España - Ventas
[l10n_es_sigaus_stock_picking_report_valued](l10n_es_sigaus_stock_picking_report_valued/) | 16.0.1.0.2 |  | Show SIGAUS amount in valued stock pickings.
[l10n_es_subcontractor_certificate](l10n_es_subcontractor_certificate/) | 16.0.1.0.0 |  | Certificado de subcontratista
[l10n_es_ticketbai](l10n_es_ticketbai/) | 16.0.1.2.1 | <a href='https://github.com/ao-landoo'><img src='https://github.com/ao-landoo.png' width='32' height='32' style='border-radius:50%;' alt='ao-landoo'/></a> | Declaración de todas las operaciones de venta realizadas por las personas y entidades que desarrollan actividades económicas
[l10n_es_ticketbai_api](l10n_es_ticketbai_api/) | 16.0.1.1.4 | <a href='https://github.com/ao-landoo'><img src='https://github.com/ao-landoo.png' width='32' height='32' style='border-radius:50%;' alt='ao-landoo'/></a> | TicketBAI - API
[l10n_es_ticketbai_api_batuz](l10n_es_ticketbai_api_batuz/) | 16.0.1.0.5 | <a href='https://github.com/ao-landoo'><img src='https://github.com/ao-landoo.png' width='32' height='32' style='border-radius:50%;' alt='ao-landoo'/></a> | TicketBAI (API) - Batuz - declaración de todas las operaciones de venta realizadas por las personas y entidades que desarrollan actividades económicas en Bizkaia
[l10n_es_ticketbai_batuz](l10n_es_ticketbai_batuz/) | 16.0.1.1.0 | <a href='https://github.com/enriquemartin'><img src='https://github.com/enriquemartin.png' width='32' height='32' style='border-radius:50%;' alt='enriquemartin'/></a> <a href='https://github.com/ao-landoo'><img src='https://github.com/ao-landoo.png' width='32' height='32' style='border-radius:50%;' alt='ao-landoo'/></a> | TicketBAI - Batuz - declaración de todas las operaciones de venta realizadas por las personas y entidades que desarrollan actividades económicas en Bizkaia
[l10n_es_ticketbai_oss](l10n_es_ticketbai_oss/) | 16.0.1.0.1 | <a href='https://github.com/ao-landoo'><img src='https://github.com/ao-landoo.png' width='32' height='32' style='border-radius:50%;' alt='ao-landoo'/></a> | TicketBAI - OSS
[l10n_es_ticketbai_pos](l10n_es_ticketbai_pos/) | 16.0.1.1.2 | <a href='https://github.com/ao-landoo'><img src='https://github.com/ao-landoo.png' width='32' height='32' style='border-radius:50%;' alt='ao-landoo'/></a> | TicketBAI - Point of Sale - declaración de todas las operaciones de venta realizadas por las personas y entidades que desarrollan actividades económicas
[l10n_es_toponyms](l10n_es_toponyms/) | 16.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Topónimos españoles
[l10n_es_vat_book](l10n_es_vat_book/) | 16.0.2.1.2 |  | Libros registro del IVA y del IRPF
[l10n_es_vat_book_igic](l10n_es_vat_book_igic/) | 16.0.1.0.2 | <a href='https://github.com/nicolasramos'><img src='https://github.com/nicolasramos.png' width='32' height='32' style='border-radius:50%;' alt='nicolasramos'/></a> | Libro de IGIC
[l10n_es_vat_book_invoice_summary](l10n_es_vat_book_invoice_summary/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Facturas resumen en libro de IVA
[l10n_es_vat_book_oss](l10n_es_vat_book_oss/) | 16.0.1.0.1 |  | Libro de IVA OSS
[l10n_es_vat_prorate](l10n_es_vat_prorate/) | 16.0.2.1.0 |  | Prorrata de IVA para la localización española
[l10n_es_verifactu_oca](l10n_es_verifactu_oca/) | 16.0.1.3.3 |  | Comunicación VERI*FACTU
[l10n_es_verifactu_oca_operation_date](l10n_es_verifactu_oca_operation_date/) | 16.0.1.0.0 |  | VERI*FACTU - Operation Date
[l10n_es_verifactu_oca_oss](l10n_es_verifactu_oca_oss/) | 16.0.1.0.1 |  | Comunicación VERI*FACTU: OSS
[l10n_es_verifactu_pos_oca](l10n_es_verifactu_pos_oca/) | 16.0.1.0.0 |  | Comunicación Veri*FACTU: TPV
[payment_redsys](payment_redsys/) | 16.0.1.0.4 |  | Payment Acquirer: Redsys Implementation

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# l10n-switzerland
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-switzerland&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-switzerland/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-switzerland/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-switzerland/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-switzerland/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-switzerland/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-switzerland)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-switzerland-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-switzerland-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[ebill_postfinance](ebill_postfinance/) | 16.0.1.0.1 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Postfinance eBill integration
[ebill_postfinance_server_env](ebill_postfinance_server_env/) | 16.0.1.0.0 |  | Server environment for eBill Postfinance
[ebill_postfinance_stock](ebill_postfinance_stock/) | 16.0.1.0.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Add stock integration to Postfinance eBill
[l10n_ch_account_tags](l10n_ch_account_tags/) | 16.0.1.0.0 |  | Switzerland Account Tags
[l10n_ch_mis_reports](l10n_ch_mis_reports/) | 16.0.1.0.0 |  | Specific MIS reports for switzerland localization
[l10n_ch_pain_base](l10n_ch_pain_base/) | 16.0.1.0.0 |  | ISO 20022 base module for Switzerland
[l10n_ch_pain_credit_transfer](l10n_ch_pain_credit_transfer/) | 16.0.1.1.0 | <a href='https://github.com/ecino'><img src='https://github.com/ecino.png' width='32' height='32' style='border-radius:50%;' alt='ecino'/></a> | Generate ISO 20022 credit transfert (SEPA and not SEPA)
[l10n_ch_partner_address_street3](l10n_ch_partner_address_street3/) | 16.0.1.0.0 |  | Take into account street3 in QR-bills
[l10n_ch_partner_company_type](l10n_ch_partner_company_type/) | 16.0.1.0.0 | <a href='https://github.com/mihien'><img src='https://github.com/mihien.png' width='32' height='32' style='border-radius:50%;' alt='mihien'/></a> | Data module to add swiss compay types

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-thailand&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-thailand/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-thailand/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-thailand/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-thailand/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-thailand/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-thailand)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-thailand-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-thailand-16-0/?utm_source=widget)

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
[currency_rate_update_TH_BOT](currency_rate_update_TH_BOT/) | 16.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Currency Rate Update - BOT
[l10n_th_account_asset_management](l10n_th_account_asset_management/) | 16.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Thai Localization - Assets Management
[l10n_th_account_tax](l10n_th_account_tax/) | 16.0.2.0.5 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Thai Localization - VAT and Withholding Tax
[l10n_th_account_tax_expense](l10n_th_account_tax_expense/) | 16.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Thai Localization - Expense Tax
[l10n_th_account_tax_multi](l10n_th_account_tax_multi/) | 16.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Thai Localization - Tax with Payment Multi Deduction
[l10n_th_account_tax_report](l10n_th_account_tax_report/) | 16.0.1.3.1 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Thai Localization - VAT and Withholding Tax Reports
[l10n_th_account_wht_cert_form](l10n_th_account_wht_cert_form/) | 16.0.1.2.0 | <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Thai Localization - Withholding Tax Certificate Form
[l10n_th_amount_to_text](l10n_th_amount_to_text/) | 16.0.1.0.0 | <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Convert Amount Text to Thai
[l10n_th_bank_payment_export](l10n_th_bank_payment_export/) | 16.0.1.0.0 | <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Base export payment text file to bank
[l10n_th_base_location](l10n_th_base_location/) | 16.0.1.0.1 |  | Thai Localization - Base Location
[l10n_th_base_sequence](l10n_th_base_sequence/) | 16.0.1.0.0 | <a href='https://github.com/sansirit'><img src='https://github.com/sansirit.png' width='32' height='32' style='border-radius:50%;' alt='sansirit'/></a> <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Thai Localization - Base Sequence
[l10n_th_fonts](l10n_th_fonts/) | 16.0.1.0.0 | <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Collection of all Thai fonts
[l10n_th_gov_purchase_agreement](l10n_th_gov_purchase_agreement/) | 16.0.1.0.0 | <a href='https://github.com/newtratip'><img src='https://github.com/newtratip.png' width='32' height='32' style='border-radius:50%;' alt='newtratip'/></a> | Thai Localization - Government Purchase Agreement
[l10n_th_mis_report](l10n_th_mis_report/) | 16.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Thai Localization - MIS Report
[l10n_th_partner](l10n_th_partner/) | 16.0.1.1.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Thai Localization - Partner
[l10n_th_promptpay](l10n_th_promptpay/) | 16.0.1.0.0 |  | Use PromptPay QR code with transfer acquirer.
[l10n_th_tax_address](l10n_th_tax_address/) | 16.0.1.1.1 | <a href='https://github.com/Saran440'><img src='https://github.com/Saran440.png' width='32' height='32' style='border-radius:50%;' alt='Saran440'/></a> | Thai Localization - Tax address
[l10n_th_tier_department](l10n_th_tier_department/) | 16.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Thai Localization - Tier Department Level
[l10n_th_tier_department_demo](l10n_th_tier_department_demo/) | 16.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Thai Localization - Tier Department Level Demo

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-usa&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-usa/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-usa/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-usa/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-usa/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-usa/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-usa)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-usa-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-usa-16-0/?utm_source=widget)

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
[account_banking_ach_base](account_banking_ach_base/) | 16.0.1.0.0 |  | Add fields required for North American Banking & Financials
[l10n_us_account_routing](l10n_us_account_routing/) | 16.0.1.0.0 |  | Add the routing numbers to the banks
[l10n_us_form_1099](l10n_us_form_1099/) | 16.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Manage 1099 Types and Suppliers
[l10n_us_gaap](l10n_us_gaap/) | 16.0.1.0.1 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> | United States Sample GAAP Chart of Accounts
[l10n_us_gaap_mis_report](l10n_us_gaap_mis_report/) | 16.0.1.0.1 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> | MIS Builder Templates for US Chart of Accounts
[l10n_us_mis_financial_report](l10n_us_mis_financial_report/) | 16.0.1.1.0 | <a href='https://github.com/Christian-RB'><img src='https://github.com/Christian-RB.png' width='32' height='32' style='border-radius:50%;' alt='Christian-RB'/></a> | Profit & Loss (US) / Balance sheet (US) MIS templates
[l10n_us_partner_legal_number](l10n_us_partner_legal_number/) | 16.0.1.0.0 |  | Add Legal Number for North American Banking & Financials
[partner_usps_address_validation](partner_usps_address_validation/) | 16.0.1.0.0 |  | Utilize the USPS open API for address validation

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/l10n-venezuela


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-venezuela&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-venezuela/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-venezuela/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-venezuela/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-venezuela/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-venezuela/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-venezuela)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-venezuela-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-venezuela-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# l10n-venezuela

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[res_currency_rate_provider_BCV](res_currency_rate_provider_BCV/) | 16.0.1.1.2 | <a href='https://github.com/lapinzon'><img src='https://github.com/lapinzon.png' width='32' height='32' style='border-radius:50%;' alt='lapinzon'/></a> | OCA version for BCV scrapping rates

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/maintenance&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/maintenance/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/maintenance/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/maintenance/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/maintenance/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/maintenance/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/maintenance)
[![Translation Status](https://translation.odoo-community.org/widgets/maintenance-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/maintenance-16-0/?utm_source=widget)

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
[base_maintenance](base_maintenance/) | 16.0.1.0.2 |  | Base Maintenance
[base_maintenance_config](base_maintenance_config/) | 16.0.1.0.0 |  | Provides general settings for the Maintenance App
[base_maintenance_group](base_maintenance_group/) | 16.0.1.0.0 |  | Provides base access groups for the Maintenance App
[hr_maintenance_security](hr_maintenance_security/) | 16.0.1.0.0 |  | HR Maintenance Security
[maintenance_account](maintenance_account/) | 16.0.1.1.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Account
[maintenance_equipment_category_hierarchy](maintenance_equipment_category_hierarchy/) | 16.0.1.0.0 |  | Equipment Categories Hierarchy
[maintenance_equipment_certification](maintenance_equipment_certification/) | 16.0.1.0.0 | <a href='https://github.com/cubells'><img src='https://github.com/cubells.png' width='32' height='32' style='border-radius:50%;' alt='cubells'/></a> | Add to store certifications associated with a equipment.
[maintenance_equipment_contract](maintenance_equipment_contract/) | 16.0.1.0.1 |  | Manage equipment contracts
[maintenance_equipment_hierarchy](maintenance_equipment_hierarchy/) | 16.0.1.1.0 | <a href='https://github.com/dalonsod'><img src='https://github.com/dalonsod.png' width='32' height='32' style='border-radius:50%;' alt='dalonsod'/></a> | Manage equipment hierarchy
[maintenance_equipment_image](maintenance_equipment_image/) | 16.0.1.0.0 | <a href='https://github.com/pedrocasi'><img src='https://github.com/pedrocasi.png' width='32' height='32' style='border-radius:50%;' alt='pedrocasi'/></a> | Adds images to equipment.
[maintenance_equipment_sequence](maintenance_equipment_sequence/) | 16.0.1.0.2 | <a href='https://github.com/AdriaGForgeFlow'><img src='https://github.com/AdriaGForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='AdriaGForgeFlow'/></a> | Adds sequence to maintenance equipment defined in the equipment's category
[maintenance_equipment_status](maintenance_equipment_status/) | 16.0.1.0.0 |  | Maintenance Equipment Status
[maintenance_equipment_tags](maintenance_equipment_tags/) | 16.0.1.0.0 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Adds category tags to equipment
[maintenance_equipment_usage](maintenance_equipment_usage/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Equipment Usage
[maintenance_location](maintenance_location/) | 16.0.1.0.0 |  | Define a location system for maintenance
[maintenance_plan](maintenance_plan/) | 16.0.1.0.0 |  | Extends preventive maintenance planning
[maintenance_plan_activity](maintenance_plan_activity/) | 16.0.1.0.0 |  | This module allows defining in the maintenance plan activities that will be created once the maintenance requests are created as a consequence of the plan itself.
[maintenance_product](maintenance_product/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Product
[maintenance_project](maintenance_project/) | 16.0.2.0.0 |  | Adds projects to maintenance equipments and requests
[maintenance_purchase](maintenance_purchase/) | 16.0.1.0.0 |  | Create Equipments with purchases
[maintenance_remote](maintenance_remote/) | 16.0.1.0.0 |  | Define remote on maintenance request
[maintenance_request_purchase](maintenance_request_purchase/) | 16.0.1.1.1 |  | Allows you to link PO with maintenance requests
[maintenance_request_repair](maintenance_request_repair/) | 16.0.1.0.0 |  | This is a bridge module between Maintenance and Repair
[maintenance_request_sequence](maintenance_request_sequence/) | 16.0.1.0.1 |  | Adds sequence to maintenance requests
[maintenance_request_stage_transition](maintenance_request_stage_transition/) | 16.0.1.0.0 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Manage transition visibility and management between stages
[maintenance_security](maintenance_security/) | 16.0.2.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Security
[maintenance_team_hierarchy](maintenance_team_hierarchy/) | 16.0.1.0.0 |  | Create hierarchies on teams
[maintenance_timesheet](maintenance_timesheet/) | 16.0.2.1.0 |  | Adds timesheets to maintenance requests
[maintenance_timesheet_time_control](maintenance_timesheet_time_control/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Timesheets Timesheet Time Control

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/management-system&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/management-system/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/management-system/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/management-system/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/management-system/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/management-system/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/management-system)
[![Translation Status](https://translation.odoo-community.org/widgets/management-system-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/management-system-16-0/?utm_source=widget)

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
[document_page_environment_manual](document_page_environment_manual/) | 16.0.1.0.1 |  | Document Management - Wiki - Environment Manual
[document_page_environmental_aspect](document_page_environmental_aspect/) | 16.0.1.0.1 |  | Environmental Aspects
[document_page_health_safety_manual](document_page_health_safety_manual/) | 16.0.1.0.1 |  | Health and Safety Manual
[document_page_procedure](document_page_procedure/) | 16.0.1.0.1 |  | Document Management - Wiki - Procedures
[document_page_quality_manual](document_page_quality_manual/) | 16.0.1.0.1 |  | Quality Manual
[document_page_work_instruction](document_page_work_instruction/) | 16.0.1.0.1 |  | Document Management - Wiki - Work Instructions
[mgmtsystem](mgmtsystem/) | 16.0.1.1.0 |  | Management System
[mgmtsystem_action](mgmtsystem_action/) | 16.0.1.0.1 |  | Management System - Action
[mgmtsystem_action_efficacy](mgmtsystem_action_efficacy/) | 16.0.1.0.0 |  | Add information on the application of the Action.
[mgmtsystem_action_hazard](mgmtsystem_action_hazard/) | 16.0.1.0.0 |  | Get access to actions related to a hazard
[mgmtsystem_action_template](mgmtsystem_action_template/) | 16.0.1.0.0 |  | Add Template management for Actions.
[mgmtsystem_audit](mgmtsystem_audit/) | 16.0.1.1.0 |  | Management System - Audit
[mgmtsystem_claim](mgmtsystem_claim/) | 16.0.1.1.1 |  | Management System - Claim
[mgmtsystem_environment](mgmtsystem_environment/) | 16.0.1.0.0 |  | Environment Management System
[mgmtsystem_evaluation](mgmtsystem_evaluation/) | 16.0.1.1.0 |  | Evaluate records within your management system
[mgmtsystem_evaluation_hr](mgmtsystem_evaluation_hr/) | 16.0.1.0.0 |  | Allow to use evaluations on Employees
[mgmtsystem_hazard](mgmtsystem_hazard/) | 16.0.1.2.0 |  | Hazard
[mgmtsystem_hazard_maintenance_equipment](mgmtsystem_hazard_maintenance_equipment/) | 16.0.1.0.0 |  | Management System - Maintenance Equipment
[mgmtsystem_hazard_risk](mgmtsystem_hazard_risk/) | 16.0.1.1.0 |  | Hazard Risk
[mgmtsystem_health_safety](mgmtsystem_health_safety/) | 16.0.1.0.1 |  | Health and Safety Management System
[mgmtsystem_info_security_manual](mgmtsystem_info_security_manual/) | 16.0.1.0.0 |  | Information Security Management System Manual
[mgmtsystem_manual](mgmtsystem_manual/) | 16.0.1.0.1 |  | Management System - Manual
[mgmtsystem_nonconformity](mgmtsystem_nonconformity/) | 16.0.1.4.1 |  | Management System - Nonconformity
[mgmtsystem_nonconformity_hazard](mgmtsystem_nonconformity_hazard/) | 16.0.1.0.0 |  | Management System - Nonconformity Hazard
[mgmtsystem_nonconformity_hr](mgmtsystem_nonconformity_hr/) | 16.0.1.0.0 |  | Bridge module between hr and mgmsystem and
[mgmtsystem_nonconformity_maintenance](mgmtsystem_nonconformity_maintenance/) | 16.0.1.0.0 |  | Bridge module between Maintenance and Non Conformities
[mgmtsystem_nonconformity_maintenance_equipment](mgmtsystem_nonconformity_maintenance_equipment/) | 16.0.1.0.0 |  | Management System - Nonconformity Maintenance Equipment
[mgmtsystem_nonconformity_mrp](mgmtsystem_nonconformity_mrp/) | 16.0.1.0.0 |  | Bridge module between mrp and mgmsystem
[mgmtsystem_nonconformity_product](mgmtsystem_nonconformity_product/) | 16.0.1.0.0 |  | Bridge module between Product and Management System.
[mgmtsystem_nonconformity_quality_control_oca](mgmtsystem_nonconformity_quality_control_oca/) | 16.0.1.0.1 |  | Bridge module between Quality Control and Non Conformities
[mgmtsystem_nonconformity_repair](mgmtsystem_nonconformity_repair/) | 16.0.1.0.0 |  | Bridge module between Repair and Non Conformities
[mgmtsystem_nonconformity_type](mgmtsystem_nonconformity_type/) | 16.0.1.1.0 |  | Add Nonconformity classification for the root context.
[mgmtsystem_partner](mgmtsystem_partner/) | 16.0.1.0.0 |  | Add Management System reference on Partner's Contacts.
[mgmtsystem_quality](mgmtsystem_quality/) | 16.0.1.0.2 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Manage your quality management system
[mgmtsystem_review](mgmtsystem_review/) | 16.0.2.0.0 |  | Management System - Review
[mgmtsystem_review_survey](mgmtsystem_review_survey/) | 16.0.2.0.0 |  | Management System - Review Survey
[mgmtsystem_survey](mgmtsystem_survey/) | 16.0.1.0.0 |  | Management System - Survey

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/manufacture&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/manufacture/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/manufacture/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/manufacture/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/manufacture/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/manufacture/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/manufacture)
[![Translation Status](https://translation.odoo-community.org/widgets/manufacture-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/manufacture-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_move_line_mrp_info](account_move_line_mrp_info/) | 16.0.1.1.0 |  | Account Move Line Mrp Info
[mrp_account_analytic](mrp_account_analytic/) | 16.0.1.0.0 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Consuming raw materials and operations generated Analytic Items
[mrp_attachment_mgmt](mrp_attachment_mgmt/) | 16.0.1.1.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Mrp Attachment Mgmt
[mrp_bom_component_menu](mrp_bom_component_menu/) | 16.0.1.0.0 |  | MRP BOM Component Menu
[mrp_bom_hierarchy](mrp_bom_hierarchy/) | 16.0.1.2.1 |  | Make it easy to navigate through BoM hierarchy.
[mrp_bom_image](mrp_bom_image/) | 16.0.1.0.1 |  | Add product Images to BoM
[mrp_bom_line_formula_quantity](mrp_bom_line_formula_quantity/) | 16.0.1.0.0 | <a href='https://github.com/SirAionTech'><img src='https://github.com/SirAionTech.png' width='32' height='32' style='border-radius:50%;' alt='SirAionTech'/></a> | Compute the quantity of a Production Line using a formula in the BoM Line.
[mrp_bom_line_net_qty](mrp_bom_line_net_qty/) | 16.0.1.0.0 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | MRP BoM Line Net and Gross Quantity
[mrp_bom_location](mrp_bom_location/) | 16.0.1.1.1 |  | Adds location field to Bill of Materials and its components.
[mrp_bom_note](mrp_bom_note/) | 16.0.1.1.0 |  | Notes in Bill of Materials
[mrp_bom_order_by_product_name](mrp_bom_order_by_product_name/) | 16.0.1.0.0 |  | Order BoM with their Product name
[mrp_bom_priority](mrp_bom_priority/) | 16.0.1.0.0 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Adds priority field to BoMs
[mrp_bom_produce_delay](mrp_bom_produce_delay/) | 16.0.1.0.0 |  | Add Product Delay in BoM, linked to Product Produce Delay.
[mrp_bom_produce_delay_in_hour](mrp_bom_produce_delay_in_hour/) | 16.0.1.0.0 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Glue module for mrp_bom_produce_delay and mrp_product_produce_delay_in_hour
[mrp_bom_product_price_margin](mrp_bom_product_price_margin/) | 16.0.1.1.0 |  | Handle Product Standard, Sale Price and Margin with its BoM cost
[mrp_bom_select_product_variant](mrp_bom_select_product_variant/) | 16.0.1.0.0 |  | Favors Product variant selection for BOM creation.
[mrp_bom_tag](mrp_bom_tag/) | 16.0.1.2.0 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Add tags on your BoM to find it easily
[mrp_bom_tracking](mrp_bom_tracking/) | 16.0.1.0.1 |  | Logs any change to a BoM in the chatter
[mrp_bom_version](mrp_bom_version/) | 16.0.1.0.1 |  | BoM versioning
[mrp_bom_weight](mrp_bom_weight/) | 16.0.1.0.0 |  | MRP BoM Weight
[mrp_bom_widget_section_and_note_one2many](mrp_bom_widget_section_and_note_one2many/) | 16.0.1.0.0 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Add section and note in Bills of Materials
[mrp_default_workorder_time](mrp_default_workorder_time/) | 16.0.1.0.0 | <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | Adds an MRP default workorder time
[mrp_lot_number_propagation](mrp_lot_number_propagation/) | 16.0.1.0.1 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Propagate a serial number from a component to a finished product
[mrp_lot_production_date](mrp_lot_production_date/) | 16.0.1.0.0 |  | MRP Lot Production Date
[mrp_mto_owner](mrp_mto_owner/) | 16.0.1.0.0 |  | Mrp MTO Owner
[mrp_multi_level](mrp_multi_level/) | 16.0.1.7.1 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | Adds an MRP Scheduler
[mrp_multi_level_estimate](mrp_multi_level_estimate/) | 16.0.1.2.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Allows to consider demand estimates using MRP multi level.
[mrp_packaging_default](mrp_packaging_default/) | 16.0.1.0.2 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Include packaging info in MRP by default
[mrp_planned_order_matrix](mrp_planned_order_matrix/) | 16.0.1.0.0 |  | Allows to create fixed planned orders on a grid view.
[mrp_product_characterisation](mrp_product_characterisation/) | 16.0.1.1.0 |  | Adds product characterisation 'Intermediate Products'.
[mrp_product_produce_delay_in_hour](mrp_product_produce_delay_in_hour/) | 16.0.1.0.0 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Handle MRP Product Produce Delay in hours not in days.
[mrp_production_allow_recursive](mrp_production_allow_recursive/) | 16.0.1.0.0 |  | MRP Production Allow Recursive
[mrp_production_back_to_draft](mrp_production_back_to_draft/) | 16.0.1.0.0 |  | Allows to return to draft a confirmed or cancelled MO.
[mrp_production_grouped_by_product](mrp_production_grouped_by_product/) | 16.0.1.0.0 |  | Production Grouped By Product
[mrp_production_move_line_auto_fill](mrp_production_move_line_auto_fill/) | 16.0.1.0.0 |  | Mrp Production Move Line Auto Fill
[mrp_production_note](mrp_production_note/) | 16.0.1.0.0 |  | Notes in production orders
[mrp_production_quant_manual_assign](mrp_production_quant_manual_assign/) | 16.0.1.1.0 |  | Production - Manual Quant Assignment
[mrp_production_serial_matrix](mrp_production_serial_matrix/) | 16.0.1.0.0 |  | MRP Production Serial Matrix
[mrp_production_unique_lot](mrp_production_unique_lot/) | 16.0.1.0.0 |  | MRP Production Unique Lot
[mrp_restrict_lot](mrp_restrict_lot/) | 16.0.1.0.3 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | MRP Restrict Lot
[mrp_sale_info](mrp_sale_info/) | 16.0.1.1.0 |  | Adds sale information to Manufacturing models
[mrp_stock_move_actual_date](mrp_stock_move_actual_date/) | 16.0.1.0.0 |  | MRP Stock Move Actual Date
[mrp_stock_owner_restriction](mrp_stock_owner_restriction/) | 16.0.1.0.1 |  | MRP Stock Owner Restriction
[mrp_subcontracting_bom_dual_use](mrp_subcontracting_bom_dual_use/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Mrp subcontracting bom dual use
[mrp_subcontracting_inhibit](mrp_subcontracting_inhibit/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Inhibit subcontracting flow on demand
[mrp_subcontracting_partner_management](mrp_subcontracting_partner_management/) | 16.0.1.1.0 |  | Subcontracting Partner Management
[mrp_subcontracting_purchase_link](mrp_subcontracting_purchase_link/) | 16.0.1.0.0 |  | Link Purchase Order Line to Subcontract Productions
[mrp_subcontracting_skip_no_negative](mrp_subcontracting_skip_no_negative/) | 16.0.1.0.4 |  | MRP Subcontracting Skip No Negative
[mrp_subcontracting_stock_owner_restriction](mrp_subcontracting_stock_owner_restriction/) | 16.0.1.0.0 |  | MRP Subcontracting Stock Owner Restriction
[mrp_tag](mrp_tag/) | 16.0.1.1.0 |  | Allows to add multiple tags to Manufacturing Orders
[mrp_unbuild_move_link](mrp_unbuild_move_link/) | 16.0.1.0.1 |  | Link the stock moves of manufacturing orders to the respective unbuild orders
[mrp_unbuild_restore_origin](mrp_unbuild_restore_origin/) | 16.0.1.1.0 |  | Mrp Unbuild Restore Origin
[mrp_unbuild_subcontracting](mrp_unbuild_subcontracting/) | 16.0.1.0.1 |  | Unbuild orders are created automatically when is returned a product subcontracted
[mrp_unbuild_valuation_layer_link](mrp_unbuild_valuation_layer_link/) | 16.0.1.0.1 |  | Unbuild orders display the connected valuation layers
[mrp_warehouse_calendar](mrp_warehouse_calendar/) | 16.0.1.0.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> | Considers the warehouse calendars in manufacturing
[mrp_workcenter_cost](mrp_workcenter_cost/) | 16.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Controls how to compute the workcenter cost (effective vs theoretical)
[mrp_workcenter_dashboard](mrp_workcenter_dashboard/) | 16.0.1.0.0 |  | Enables workcenter dashboard, disabled by default in Odoo
[mrp_workcenter_hierarchical](mrp_workcenter_hierarchical/) | 16.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Organise Workcenters by section
[mrp_workcenter_workorder_link](mrp_workcenter_workorder_link/) | 16.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Switch easily between Work Centers and Work Orders
[mrp_workorder_last_worker](mrp_workorder_last_worker/) | 16.0.1.1.0 |  | See the last user who worked on a workorder
[mrp_workorder_lot_display](mrp_workorder_lot_display/) | 16.0.1.0.0 | <a href='https://github.com/grindtildeath'><img src='https://github.com/grindtildeath.png' width='32' height='32' style='border-radius:50%;' alt='grindtildeath'/></a> | Display lot number on workorders kanban
[mrp_workorder_priority](mrp_workorder_priority/) | 16.0.1.0.0 |  | Add a priority field to workorders
[mrp_workorder_sequence](mrp_workorder_sequence/) | 16.0.0.1.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | adds sequence to production work orders.
[product_mrp_info](product_mrp_info/) | 16.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Adds smart button in product form view linking to manufacturing order list.
[quality_control_mrp_oca](quality_control_mrp_oca/) | 16.0.1.2.0 |  | MRP extension for quality control (OCA)
[quality_control_oca](quality_control_oca/) | 16.0.1.8.0 |  | Generic infrastructure for quality tests.
[quality_control_product_manufacturer](quality_control_product_manufacturer/) | 16.0.1.1.0 |  | Provides information related to Manufacturer under Inspection
[quality_control_stock_oca](quality_control_stock_oca/) | 16.0.1.4.0 |  | Quality control - Stock (OCA)

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/manufacture-reporting&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/manufacture-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/manufacture-reporting/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/manufacture-reporting/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/manufacture-reporting/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/manufacture-reporting/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/manufacture-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/manufacture-reporting-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/manufacture-reporting-16-0/?utm_source=widget)

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
[mrp_bom_current_stock](mrp_bom_current_stock/) | 16.0.1.0.0 |  | Add a report that explodes the bill of materials and show the stock available in the source location.
[mrp_bom_simple_report](mrp_bom_simple_report/) | 16.0.1.0.0 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Print simple report for your Bill of Materials
[mrp_bom_structure_xlsx](mrp_bom_structure_xlsx/) | 16.0.1.0.1 |  | Export BoM Structure to Excel .XLSX
[mrp_bom_structure_xlsx_level_1](mrp_bom_structure_xlsx_level_1/) | 16.0.1.0.0 |  | Export BOM Structure (Level 1) to Excel .XLSX
[mrp_flattened_bom_xlsx](mrp_flattened_bom_xlsx/) | 16.0.1.1.0 |  | Export Flattened BOM to Excel
[mrp_flattened_bom_xlsx_direct_materials_cost](mrp_flattened_bom_xlsx_direct_materials_cost/) | 16.0.1.0.1 |  | Export Flattened BOM to Excel with direct materials cost
[mrp_flattened_bom_xlsx_labour_cost](mrp_flattened_bom_xlsx_labour_cost/) | 16.0.1.0.0 |  | Export Flattened BOM to Excel with labour cost
[mrp_flattened_bom_xlsx_subcontracting_cost](mrp_flattened_bom_xlsx_subcontracting_cost/) | 16.0.1.0.0 |  | Export Flattened BOM to Excel with subcontracting cost
[mrp_order_report_lot](mrp_order_report_lot/) | 16.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Display Component's Lot on the Production Order Report
[mrp_order_report_lot_barcode](mrp_order_report_lot_barcode/) | 16.0.1.0.0 |  | Lot Barcode on the Production Order
[mrp_order_report_lot_reserved](mrp_order_report_lot_reserved/) | 16.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Display Component's Reserved Lots on the Production Order Report
[mrp_order_report_reserved](mrp_order_report_reserved/) | 16.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Display Component's Reserved Quantity on the Production Order Report

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# margin-analysis
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/margin-analysis&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/margin-analysis/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/margin-analysis/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/margin-analysis/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/margin-analysis/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/margin-analysis/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/margin-analysis)
[![Translation Status](https://translation.odoo-community.org/widgets/margin-analysis-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/margin-analysis-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_invoice_margin](account_invoice_margin/) | 16.0.1.0.1 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Show margin in invoices
[account_invoice_margin_sale](account_invoice_margin_sale/) | 16.0.1.0.4 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> | Set margin in invoices from sale orders
[product_margin_classification](product_margin_classification/) | 16.0.1.3.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Product Margin Classification
[product_replenishment_cost](product_replenishment_cost/) | 16.0.1.0.0 |  | Provides an overridable method on product which computethe Replenishment cost of a product
[product_standard_margin](product_standard_margin/) | 16.0.1.0.3 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Product Margin and Margin Rate
[product_standard_margin_security](product_standard_margin_security/) | 16.0.1.0.0 |  | Security for product standard margin
[sale_margin_delivered](sale_margin_delivered/) | 16.0.2.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Sale Margin Delivered
[sale_margin_delivered_dropshipping](sale_margin_delivered_dropshipping/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Sale Margin Delivered Dropshipping
[sale_margin_delivered_security](sale_margin_delivered_security/) | 16.0.1.2.1 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Glue module between sale margin delivered and sale margin security modules
[sale_margin_security](sale_margin_security/) | 16.0.3.1.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Sale Margin Security
[sale_margin_sync](sale_margin_sync/) | 16.0.1.0.1 |  | Recompute sale margin when stock move cost price is changed
[sale_report_margin](sale_report_margin/) | 16.0.1.0.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Sale Report Margin

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/mis-builder&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/mis-builder/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/mis-builder/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/mis-builder/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/mis-builder/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/mis-builder/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/mis-builder)
[![Translation Status](https://translation.odoo-community.org/widgets/mis-builder-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/mis-builder-16-0/?utm_source=widget)

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
[mis_builder](mis_builder/) | 16.0.5.8.0 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Build 'Management Information System' Reports and Dashboards
[mis_builder_budget](mis_builder_budget/) | 16.0.5.4.0 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Create budgets for MIS reports
[mis_builder_demo](mis_builder_demo/) | 16.0.1.0.3 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Demo addon for MIS Builder

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# mis-builder-contrib
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/mis-builder-contrib&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/mis-builder-contrib/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/mis-builder-contrib/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/mis-builder-contrib/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/mis-builder-contrib/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/mis-builder-contrib/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/mis-builder-contrib)
[![Translation Status](https://translation.odoo-community.org/widgets/mis-builder-contrib-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/mis-builder-contrib-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[mis_builder_analytic](mis_builder_analytic/) | 16.0.1.1.0 |  | Provide account analytic lines for MIS builder reports
[mis_builder_budget_product](mis_builder_budget_product/) | 16.0.1.0.0 |  | Offer more options for budgets for MIS reports
[mis_builder_total_committed_purchase](mis_builder_total_committed_purchase/) | 16.0.1.0.0 |  | Addon to create a alternative source based on all purchase order line with MIS Builder.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/module-composition-analysis&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/module-composition-analysis/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/module-composition-analysis/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/module-composition-analysis/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/module-composition-analysis/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/module-composition-analysis/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/module-composition-analysis)
[![Translation Status](https://translation.odoo-community.org/widgets/module-composition-analysis-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/module-composition-analysis-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Collect and explore data from Odoo modules repositories

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[odoo_project](odoo_project/) | 16.0.1.0.2 |  | Analyze your Odoo projects code bases.
[odoo_project_changelog](odoo_project_changelog/) | 16.0.1.0.1 |  | Generate Changelogs from repositories for installed modules.
[odoo_project_migration](odoo_project_migration/) | 16.0.1.1.2 |  | Analyze your Odoo project migrations.
[odoo_project_stat](odoo_project_stat/) | 16.0.1.0.1 |  | Get some stats about your Odoo Projects.
[odoo_repository](odoo_repository/) | 16.0.1.5.5 |  | Base module to host data collected from Odoo repositories.
[odoo_repository_migration](odoo_repository_migration/) | 16.0.1.3.4 |  | Collect modules migration data for Odoo Repositories.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# Tools for managing instances containing multiple companies
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/multi-company&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/multi-company/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/multi-company/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/multi-company/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/multi-company/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/multi-company/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/multi-company)
[![Translation Status](https://translation.odoo-community.org/widgets/multi-company-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/multi-company-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_invoice_inter_company](account_invoice_inter_company/) | 16.0.1.2.1 |  | Intercompany invoice rules
[account_move_change_company](account_move_change_company/) | 16.0.1.0.0 |  | Allow to change company of account moves
[account_multicompany_easy_creation](account_multicompany_easy_creation/) | 16.0.1.0.0 |  | This module adds a wizard to create companies easily
[account_period_lock_date_multi_company](account_period_lock_date_multi_company/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Provides a company tree view to manage accounting lock dates
[account_reconcile_model_multicompany_propagate](account_reconcile_model_multicompany_propagate/) | 16.0.1.2.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Propagate account reconcile model in companies with same chart template
[base_company_legal_info](base_company_legal_info/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Adds Legal informations on company model
[base_multi_company](base_multi_company/) | 16.0.3.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Provides a base for adding multi-company support to models.
[calendar_event_multi_company](calendar_event_multi_company/) | 16.0.1.0.0 |  | This module add multi-company management to calendar events
[calendar_event_type_multi_company](calendar_event_type_multi_company/) | 16.0.1.0.0 |  | This module add multi-company management to calendar event type
[company_dependent_flag](company_dependent_flag/) | 16.0.1.0.2 |  | Apply css style to company dependent fields
[crm_lost_reason_multi_company](crm_lost_reason_multi_company/) | 16.0.1.0.0 |  | This module add multi-company management to crm lost reason
[crm_stage_multi_company](crm_stage_multi_company/) | 16.0.1.0.0 |  | This module adds support for multi company on crm stage.
[crm_tag_multi_company](crm_tag_multi_company/) | 16.0.1.0.0 |  | This module add multi-company management to crm tag
[crm_tag_multi_company_event_crm](crm_tag_multi_company_event_crm/) | 16.0.1.0.0 |  | Ensure multi-company check in event lead rules tag ids
[crm_tag_multi_company_sale](crm_tag_multi_company_sale/) | 16.0.1.0.0 |  | Ensure multi-company check in sale order tag ids
[ir_actions_report_multi_company](ir_actions_report_multi_company/) | 16.0.1.0.0 |  | Make Report Actions multi-company aware
[ir_config_parameter_multi_company](ir_config_parameter_multi_company/) | 16.0.1.0.1 | <a href='https://github.com/deniscraciungabriel'><img src='https://github.com/deniscraciungabriel.png' width='32' height='32' style='border-radius:50%;' alt='deniscraciungabriel'/></a> <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Add res company field in ir config parameter
[login_all_company](login_all_company/) | 16.0.0.0.0 |  | Access all your companies when you log in
[mail_multicompany](mail_multicompany/) | 16.0.2.0.0 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Email Gateway Multi company
[mail_template_multi_company](mail_template_multi_company/) | 16.0.1.0.0 | <a href='https://github.com/Olivier-LAURENT'><img src='https://github.com/Olivier-LAURENT.png' width='32' height='32' style='border-radius:50%;' alt='Olivier-LAURENT'/></a> | Mail Template Multi Company
[mass_mailing_multi_company](mass_mailing_multi_company/) | 16.0.1.0.0 |  | Adds the company_id field to the models mailing.mailing, mailing.list and mailing.contact
[multicompany_configuration](multicompany_configuration/) | 16.0.1.0.0 |  | Simplify the configuration on multicompany environments
[partner_account_multicompany_default](partner_account_multicompany_default/) | 16.0.0.1.0 | <a href='https://github.com/camptocamp'><img src='https://github.com/camptocamp.png' width='32' height='32' style='border-radius:50%;' alt='camptocamp'/></a> | Set a default account for all companies of a partners
[partner_category_multi_company](partner_category_multi_company/) | 16.0.1.0.0 |  | This module add multi-company management to partner categories
[partner_category_multi_company_account](partner_category_multi_company_account/) | 16.0.1.0.0 |  | Multi-company check in Matching partner categories
[partner_category_multi_company_analytic](partner_category_multi_company_analytic/) | 16.0.1.0.0 |  | Multi-company check in Partner categories
[partner_multi_company](partner_multi_company/) | 16.0.2.0.2 |  | Select individually the partner visibility on each company
[pos_category_multicompany](pos_category_multicompany/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Point of Sale Category in Multi company context
[pos_restaurant_multi_company](pos_restaurant_multi_company/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | This module adds support for multi company on PoS Restaurant.
[product_account_multicompany_default](product_account_multicompany_default/) | 16.0.0.2.0 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Set a default account for all companies of a product
[product_category_company](product_category_company/) | 16.0.1.2.0 |  | Product categories as company dependent
[product_category_company_favorite](product_category_company_favorite/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Possilibity to set favorite product categories per company
[product_default_code_res_company_code](product_default_code_res_company_code/) | 16.0.1.0.0 |  | Generate product default code based on sequence defined by company, prefixed by company code
[product_multi_company](product_multi_company/) | 16.0.2.0.0 |  | Select individually the product template visibility on each company
[product_tax_multicompany_default](product_tax_multicompany_default/) | 16.0.1.0.2 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Product Tax Multi Company Default
[project_multi_company](project_multi_company/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | This module adds support for multi company on Project Module.
[purchase_sale_container_deposit_inter_company](purchase_sale_container_deposit_inter_company/) | 16.0.1.0.2 |  | Add compatibility between OCA product_packaging_container_deposit and purchase_sale_inter_company
[purchase_sale_inter_company](purchase_sale_inter_company/) | 16.0.1.1.5 |  | Intercompany PO/SO rules
[purchase_sale_stock_inter_company](purchase_sale_stock_inter_company/) | 16.0.1.0.3 |  | Intercompany PO/SO rules with warehouse
[purchase_sale_stock_inter_company_mrp](purchase_sale_stock_inter_company_mrp/) | 16.0.1.0.0 |  | Intercompany PO/SO rules with MRP
[res_company_access_all_children](res_company_access_all_children/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Give access to all children companies to users that have access to a parent company
[res_company_active](res_company_active/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add the 'active' feature on company model
[res_company_category](res_company_category/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Company Categories
[res_company_code](res_company_code/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add 'code' field on company model
[res_company_search_view](res_company_search_view/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add a search view for company model
[res_partner_category_multi_company](res_partner_category_multi_company/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Contact Tags - Multi Company
[sale_partner_company](sale_partner_company/) | 16.0.1.0.0 |  | Set sale company from partner
[sale_product_company](sale_product_company/) | 16.0.2.0.0 |  | Set selling companies on product
[sale_product_company_multi_add](sale_product_company_multi_add/) | 16.0.1.0.0 |  | Filter products by selling companies on sale order multi add
[sale_stock_warehouse_multicompany](sale_stock_warehouse_multicompany/) | 16.0.1.0.0 |  | Allow multiple companies to sell the stock of a shared warehouse
[stock_intercompany](stock_intercompany/) | 16.0.1.0.2 |  | Stock Intercompany Delivery-Reception
[stock_intercompany_bidirectional](stock_intercompany_bidirectional/) | 16.0.1.0.3 |  | Bidirectional operations for the Stock Intercomany module

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/odoo-pim


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# odoo-pim
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/odoo-pim&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/odoo-pim/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/odoo-pim/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/odoo-pim/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/odoo-pim/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/odoo-pim/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/odoo-pim)
[![Translation Status](https://translation.odoo-community.org/widgets/odoo-pim-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/odoo-pim-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[attribute_set](attribute_set/) | 16.0.1.3.0 |  | Attribute Set
[pim](pim/) | 16.0.1.0.0 |  | Product Information Management
[product_attribute_set](product_attribute_set/) | 16.0.1.2.0 |  | Product Attribute Set
[product_search_multi_value](product_search_multi_value/) | 16.0.1.0.1 |  | Product Search Multi Value

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# operating-unit
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/operating-unit&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/operating-unit/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/operating-unit/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/operating-unit/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/operating-unit/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/operating-unit/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/operating-unit)
[![Translation Status](https://translation.odoo-community.org/widgets/operating-unit-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/operating-unit-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_operating_unit](account_operating_unit/) | 16.0.1.1.2 |  | Introduces Operating Unit (OU) in invoices and Accounting Entries with clearing account
[analytic_operating_unit](analytic_operating_unit/) | 16.0.1.0.0 |  | Analytic Operating Unit
[contract_operating_unit](contract_operating_unit/) | 16.0.1.0.0 |  | Contract Operating Unit
[hr_operating_unit](hr_operating_unit/) | 16.0.1.0.0 |  | HR Operating Unit
[operating_unit](operating_unit/) | 16.0.1.1.3 |  | An operating unit (OU) is an organizational entity part of a company
[operating_unit_access_all](operating_unit_access_all/) | 16.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Access all Operating Units
[product_operating_unit](product_operating_unit/) | 16.0.1.0.1 |  | Adds the concept of operating unit (OU) in products
[project_operating_unit](project_operating_unit/) | 16.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | This module adds operating unit information to projects and tasks.
[report_qweb_operating_unit](report_qweb_operating_unit/) | 16.0.1.0.0 |  | Qweb Report With Operating Unit
[sale_operating_unit](sale_operating_unit/) | 16.0.1.0.0 |  | An operating unit (OU) is an organizational entity part of a company
[sale_operating_unit_sequence](sale_operating_unit_sequence/) | 16.0.1.0.1 |  | Sale Order Sequence by Operating Unit
[sale_stock_operating_unit](sale_stock_operating_unit/) | 16.0.1.0.1 |  | An operating unit (OU) is an organizational entity part of a company
[sales_team_operating_unit](sales_team_operating_unit/) | 16.0.1.0.0 |  | Sales Team Operating Unit
[stock_operating_unit](stock_operating_unit/) | 16.0.1.2.2 |  | Adds the concept of operating unit (OU) in stock management
[stock_operating_unit_access_all](stock_operating_unit_access_all/) | 16.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Access all OUs' Stock

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# Partner Contact
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/partner-contact&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/partner-contact/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/partner-contact/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/partner-contact/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/partner-contact/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/partner-contact/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/partner-contact)
[![Translation Status](https://translation.odoo-community.org/widgets/partner-contact-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/partner-contact-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Contact-related odoo addons.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_partner_company_group](account_partner_company_group/) | 16.0.1.0.0 |  | Adds the possibility to add a company group to a company
[animal](animal/) | 16.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Manage animals information
[base_country_state_translatable](base_country_state_translatable/) | 16.0.1.0.0 |  | Translate Country States
[base_location](base_location/) | 16.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Enhanced zip/npa management system
[base_location_geonames_import](base_location_geonames_import/) | 16.0.1.1.0 |  | Import zip entries from Geonames
[base_location_nuts](base_location_nuts/) | 16.0.1.1.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | NUTS Regions
[base_partner_company_group](base_partner_company_group/) | 16.0.1.0.0 |  | Adds the possibility to add a company group to a company
[base_partner_merge_user_consolidation](base_partner_merge_user_consolidation/) | 16.0.1.0.0 | <a href='https://github.com/ntsirintanis'><img src='https://github.com/ntsirintanis.png' width='32' height='32' style='border-radius:50%;' alt='ntsirintanis'/></a> | After merging contacts, automatically consolidate their linked user accounts.
[base_partner_sequence](base_partner_sequence/) | 16.0.1.1.0 |  | Sets customer's code from a sequence
[company_default_partner_pricelist](company_default_partner_pricelist/) | 16.0.1.0.0 |  | Define default partner pricelist per company.
[crm_partner_company_group](crm_partner_company_group/) | 16.0.1.0.0 |  | Adds the possibility to add a company group to a company
[partner_accreditation](partner_accreditation/) | 16.0.1.0.0 | <a href='https://github.com/victor-champonnois'><img src='https://github.com/victor-champonnois.png' width='32' height='32' style='border-radius:50%;' alt='victor-champonnois'/></a> | Add Accreditation to Partners
[partner_address_format_domestic](partner_address_format_domestic/) | 16.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Partner Address Format Domestic
[partner_address_split](partner_address_split/) | 16.0.1.0.0 |  | Add specific helper methods
[partner_address_street3](partner_address_street3/) | 16.0.1.0.0 |  | Add a third address line on partners
[partner_affiliate](partner_affiliate/) | 16.0.1.0.0 |  | Partner Affiliates
[partner_archive_propagate](partner_archive_propagate/) | 16.0.1.2.0 | <a href='https://github.com/ntsirintanis'><img src='https://github.com/ntsirintanis.png' width='32' height='32' style='border-radius:50%;' alt='ntsirintanis'/></a> | Archive/unarchive partner contacts hierarchically
[partner_auto_archive](partner_auto_archive/) | 16.0.1.0.0 |  | Archive periodically all contacts marked as auto-archive.
[partner_bank_acc_type_constraint](partner_bank_acc_type_constraint/) | 16.0.1.0.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adds constraint on bank account type
[partner_bank_code](partner_bank_code/) | 16.0.1.0.1 |  | Add fields information in banks
[partner_capital](partner_capital/) | 16.0.0.1.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Partners Capital
[partner_category_description](partner_category_description/) | 16.0.1.0.0 | <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Adds a description field to contact categories to improve organization and managment of customer relationships.
[partner_category_security](partner_category_security/) | 16.0.2.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Partner category security
[partner_category_security_crm](partner_category_security_crm/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Partner category security (crm extension)
[partner_category_type](partner_category_type/) | 16.0.1.0.0 | <a href='https://github.com/JordiMForgeFlow'><img src='https://github.com/JordiMForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiMForgeFlow'/></a> | Add a selection field 'Type' to classify Contact Tags.
[partner_company_default](partner_company_default/) | 16.0.1.2.0 |  | Partner Company Default
[partner_company_group](partner_company_group/) | 16.0.1.0.0 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Adds the possibility to add a company group to a company
[partner_company_type](partner_company_type/) | 16.0.2.0.0 |  | Adds a company type to partner that are companies
[partner_contact_access_link](partner_contact_access_link/) | 16.0.1.1.1 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Allow to visit the full contact form from a company
[partner_contact_address_default](partner_contact_address_default/) | 16.0.2.0.0 |  | Set a default delivery address, invoice address and contact for contacts
[partner_contact_age_range](partner_contact_age_range/) | 16.0.1.0.1 |  | Age Range for Contact's
[partner_contact_birthdate](partner_contact_birthdate/) | 16.0.1.0.0 |  | Contact's birthdate
[partner_contact_birthplace](partner_contact_birthplace/) | 16.0.1.0.0 |  | This module allows to define a birthplace for partners.
[partner_contact_department](partner_contact_department/) | 16.0.2.0.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Assign contacts to departments
[partner_contact_gender](partner_contact_gender/) | 16.0.1.0.0 |  | Add gender field to contacts
[partner_contact_in_several_companies](partner_contact_in_several_companies/) | 16.0.1.0.0 |  | Allow to have one contact in several partners
[partner_contact_job_position](partner_contact_job_position/) | 16.0.1.1.0 |  | Categorize job positions for contacts
[partner_contact_lang](partner_contact_lang/) | 16.0.1.0.0 |  | Manage language in contacts
[partner_contact_nationality](partner_contact_nationality/) | 16.0.1.0.1 |  | Add nationality field to contacts
[partner_contact_personal_information_page](partner_contact_personal_information_page/) | 16.0.1.0.1 |  | Add a page to contacts form to put personal information
[partner_contact_role](partner_contact_role/) | 16.0.1.0.0 |  | Add roles to partners.
[partner_contact_tags_in_popup](partner_contact_tags_in_popup/) | 16.0.1.0.0 | <a href='https://github.com/carmenbianca'><img src='https://github.com/carmenbianca.png' width='32' height='32' style='border-radius:50%;' alt='carmenbianca'/></a> | Display a contact's tags in the 'Contacts & Addresses' pop-up form view.
[partner_contact_type_end_user](partner_contact_type_end_user/) | 16.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Adds a new contact type 'End User'
[partner_country_state_required](partner_country_state_required/) | 16.0.1.0.0 |  | Partner Country State Required
[partner_deduplicate_acl](partner_deduplicate_acl/) | 16.0.1.0.1 |  | Contact deduplication with fine-grained permission control
[partner_deduplicate_by_ref](partner_deduplicate_by_ref/) | 16.0.1.0.0 |  | Deduplicate Contacts by reference
[partner_deduplicate_filter](partner_deduplicate_filter/) | 16.0.1.0.0 |  | Exclude records from the deduplication
[partner_disable_gravatar](partner_disable_gravatar/) | 16.0.1.0.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Disable automatic connection to gravatar.com
[partner_display_name_line_break](partner_display_name_line_break/) | 16.0.1.1.0 |  | Split the company and the partner name on two different lines
[partner_duns](partner_duns/) | 16.0.1.0.1 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Set DUNS (Data Universal Numbering System) on partners
[partner_email_check](partner_email_check/) | 16.0.1.0.0 |  | Validate email address field
[partner_email_duplicate_warn](partner_email_duplicate_warn/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Warning banner on partner form if another partner has the same email
[partner_employee_quantity](partner_employee_quantity/) | 16.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | Know how many employees a partner has
[partner_external_map](partner_external_map/) | 16.0.1.0.0 |  | Add Map and Map Routing buttons on partner form to open GMaps, OSM, Bing and others
[partner_fax](partner_fax/) | 16.0.1.0.0 |  | Add fax number on partner
[partner_firstname](partner_firstname/) | 16.0.1.0.4 |  | Split first name and last name for non company partners
[partner_identification](partner_identification/) | 16.0.1.0.3 |  | Partner Identification Numbers
[partner_identification_eori](partner_identification_eori/) | 16.0.1.0.0 |  | This addon extends "Partner Identification Numbers" to provide a number category for EORI Number
[partner_identification_gln](partner_identification_gln/) | 16.0.1.0.1 |  | This addon extends "Partner Identification Numbers" to provide a number category for GLN registration
[partner_industry_parent](partner_industry_parent/) | 16.0.1.0.0 |  | This module add a parent relation to the partner industry
[partner_industry_secondary](partner_industry_secondary/) | 16.0.1.1.0 |  | Add secondary partner industries
[partner_interest_group](partner_interest_group/) | 16.0.1.2.0 | <a href='https://github.com/victor-champonnois'><img src='https://github.com/victor-champonnois.png' width='32' height='32' style='border-radius:50%;' alt='victor-champonnois'/></a> | Add Interest Group to Partners
[partner_iterative_archive](partner_iterative_archive/) | 16.0.1.0.0 |  | Archive all contacts when parent is archived
[partner_label](partner_label/) | 16.0.1.0.0 |  | Print partner labels
[partner_lastname_uppercase](partner_lastname_uppercase/) | 16.0.1.0.1 |  | Uppercases the the last names of partners
[partner_manual_rank](partner_manual_rank/) | 16.0.1.1.2 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> <a href='https://github.com/frahikLV'><img src='https://github.com/frahikLV.png' width='32' height='32' style='border-radius:50%;' alt='frahikLV'/></a> | Be able to manually flag partners as customer or supplier.
[partner_middlename](partner_middlename/) | 16.0.1.0.0 |  | Have split Middle
[partner_mobile_duplicate_warn](partner_mobile_duplicate_warn/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Warning banner on partner form if another partner has the same mobile
[partner_multi_relation](partner_multi_relation/) | 16.0.1.5.0 |  | Partner Relations
[partner_multi_relation_archive_propagate](partner_multi_relation_archive_propagate/) | 16.0.1.1.0 | <a href='https://github.com/ntsirintanis'><img src='https://github.com/ntsirintanis.png' width='32' height='32' style='border-radius:50%;' alt='ntsirintanis'/></a> | Propagate archiving via partner_multi_relation relations
[partner_multi_relation_function](partner_multi_relation_function/) | 16.0.1.1.0 | <a href='https://github.com/NL66278'><img src='https://github.com/NL66278.png' width='32' height='32' style='border-radius:50%;' alt='NL66278'/></a> | Partner Relation Functions
[partner_phone_extension](partner_phone_extension/) | 16.0.1.0.0 |  | Partner Phone Number Extension
[partner_phonecall_schedule](partner_phonecall_schedule/) | 16.0.1.0.1 |  | Track the time and days your partners expect phone calls
[partner_pricelist_search](partner_pricelist_search/) | 16.0.1.0.0 |  | Partner pricelist search
[partner_property](partner_property/) | 16.0.1.1.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Partner Property
[partner_purchase_manager](partner_purchase_manager/) | 16.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Add purchase manager field in partner
[partner_quality_log](partner_quality_log/) | 16.0.1.0.0 | <a href='https://github.com/azucenatrey'><img src='https://github.com/azucenatrey.png' width='32' height='32' style='border-radius:50%;' alt='azucenatrey'/></a> | Add quality log to partner.
[partner_ref_unique](partner_ref_unique/) | 16.0.1.0.0 |  | Add an unique constraint to partner ref field
[partner_salesperson_propagate](partner_salesperson_propagate/) | 16.0.1.0.0 |  | Propagate any changes in the salesperson field from the partner to its contacts.
[partner_search_alias](partner_search_alias/) | 16.0.1.0.0 |  | Partner Search Alias
[partner_second_lastname](partner_second_lastname/) | 16.0.1.0.2 |  | Have split first and second lastnames
[partner_shipping_policy](partner_shipping_policy/) | 16.0.1.0.0 |  | Define shipping policy at partners level.
[partner_stage](partner_stage/) | 16.0.1.0.1 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Add lifecycle Stages to Partners
[partner_store](partner_store/) | 16.0.1.0.0 | <a href='https://github.com/wouitmil'><img src='https://github.com/wouitmil.png' width='32' height='32' style='border-radius:50%;' alt='wouitmil'/></a> | Add store type to Partners
[partner_street_number](partner_street_number/) | 16.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Allows to customize partner street number parsing and formatting
[partner_subject_to_vat](partner_subject_to_vat/) | 16.0.1.0.0 | <a href='https://github.com/victor-champonnois'><img src='https://github.com/victor-champonnois.png' width='32' height='32' style='border-radius:50%;' alt='victor-champonnois'/></a> | Record whether a company is subject to VAT.
[partner_tier_validation](partner_tier_validation/) | 16.0.1.0.1 | <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> | Support a tier validation process for Contacts
[partner_tz](partner_tz/) | 16.0.1.0.0 |  | Remove partner timezone default value and display on form
[partner_vat_unique](partner_vat_unique/) | 16.0.1.0.0 |  | Module to make the VAT number unique for customers and suppliers.
[purchase_supplier_rank](purchase_supplier_rank/) | 16.0.1.0.1 |  | Update Supplier Rank when creating a Purchase Order
[sale_customer_rank](sale_customer_rank/) | 16.0.1.0.0 |  | Update Customer Rank when creating a Sale Order
[sale_partner_address_restrict](sale_partner_address_restrict/) | 16.0.1.0.0 |  | Restrict addresses domain in the sales order form taking into account the partner selected
[sale_partner_company_group](sale_partner_company_group/) | 16.0.1.0.0 |  | Adds the possibility to add a company group to a company

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# Modules to manage your Payroll in Odoo
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/payroll&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/payroll/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/payroll/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/payroll/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/payroll/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/payroll/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/payroll)
[![Translation Status](https://translation.odoo-community.org/widgets/payroll-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/payroll-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Modules to manage your Payroll in Odoo

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[hr_payroll_document](hr_payroll_document/) | 16.0.1.3.2 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Manage payroll for each employee
[hr_payroll_document_pymupdf](hr_payroll_document_pymupdf/) | 16.0.1.0.1 | <a href='https://github.com/SirPyTech'><img src='https://github.com/SirPyTech.png' width='32' height='32' style='border-radius:50%;' alt='SirPyTech'/></a> | Try harder to read a PDF payslip with PyMuPDF.
[hr_payroll_period](hr_payroll_period/) | 16.0.1.1.0 | <a href='https://github.com/nimarosa'><img src='https://github.com/nimarosa.png' width='32' height='32' style='border-radius:50%;' alt='nimarosa'/></a> | Add payroll periods
[payroll](payroll/) | 16.0.1.6.4 | <a href='https://github.com/norlinhenrik'><img src='https://github.com/norlinhenrik.png' width='32' height='32' style='border-radius:50%;' alt='norlinhenrik'/></a> <a href='https://github.com/nimarosa'><img src='https://github.com/nimarosa.png' width='32' height='32' style='border-radius:50%;' alt='nimarosa'/></a> | Manage your employee payroll records
[payroll_account](payroll_account/) | 16.0.1.1.0 | <a href='https://github.com/appstogrow'><img src='https://github.com/appstogrow.png' width='32' height='32' style='border-radius:50%;' alt='appstogrow'/></a> <a href='https://github.com/nimarosa'><img src='https://github.com/nimarosa.png' width='32' height='32' style='border-radius:50%;' alt='nimarosa'/></a> | Manage your payroll to accounting
[payroll_contract_advantages](payroll_contract_advantages/) | 16.0.3.0.3 | <a href='https://github.com/nimarosa'><img src='https://github.com/nimarosa.png' width='32' height='32' style='border-radius:50%;' alt='nimarosa'/></a> | Allow to define contract advantages for employees.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# pms
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/pms&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/pms/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/pms/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/pms/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/pms/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/pms/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/pms)
[![Translation Status](https://translation.odoo-community.org/widgets/pms-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/pms-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Property Management System on Odoo.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[multi_pms_properties](multi_pms_properties/) | 16.0.1.0.1 |  | Multi Properties Manager
[pms](pms/) | 16.0.4.17.1 |  | A property management system
[pms_account_move_budget](pms_account_move_budget/) | 16.0.1.0.0 |  | Add Property Field in Account Move Budget
[pms_hr_property](pms_hr_property/) | 16.0.1.0.0 |  | Adds to the employee the property on which he works.
[pms_l10n_es](pms_l10n_es/) | 16.0.2.4.0 |  | PMS Spanish Adaptation
[pms_l10n_es_sii](pms_l10n_es_sii/) | 16.0.1.2.0 |  | PMS AEAT SII Integration
[pms_l10n_es_tbai](pms_l10n_es_tbai/) | 16.0.1.1.0 |  | PMS TicketBAI Integration
[pms_partner_identification](pms_partner_identification/) | 16.0.2.3.0 |  | Add identification models in pms
[pms_partner_second_lastname](pms_partner_second_lastname/) | 16.0.2.2.0 |  | Add lastname2 in pms models
[pos_pms_link](pos_pms_link/) | 16.0.1.0.0 |  | Allows to use PMS reservations on the POS interface

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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

# Point of Sale
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/pos&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/pos/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/pos/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/pos/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/pos/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/pos/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/pos)
[![Translation Status](https://translation.odoo-community.org/widgets/pos-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/pos-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Odoo modules for Point of Sale.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[pos_access_right](pos_access_right/) | 16.0.1.0.2 |  | Point of Sale - Extra Access Right for certain actions
[pos_auto_invoice](pos_auto_invoice/) | 16.0.1.0.0 |  | Allow to set POS orders as to-invoice by default
[pos_bypass_global_discount](pos_bypass_global_discount/) | 16.0.1.0.1 |  | POS Bypass Global Discount
[pos_cash_control_override](pos_cash_control_override/) | 16.0.1.0.0 |  | Override bare PoS user cash control restrictions
[pos_cash_move_reason](pos_cash_move_reason/) | 16.0.1.0.0 |  | POS cash in-out reason
[pos_cashback](pos_cashback/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Point of Sale - Cashback
[pos_category_complete_name](pos_category_complete_name/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Adds the complete name field on the pos category field.
[pos_config_logo](pos_config_logo/) | 16.0.1.0.0 |  | Set logotypes different from the company's one
[pos_container_deposit](pos_container_deposit/) | 16.0.1.0.1 |  | This module is used to manage container deposits for products in Point of Sale.
[pos_customer_comment](pos_customer_comment/) | 16.0.1.0.3 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Display Customer comment in the PoS front office and allow to edit and save it by the cashier
[pos_customer_tree_view_vat](pos_customer_tree_view_vat/) | 16.0.1.0.1 | <a href='https://github.com/mileo'><img src='https://github.com/mileo.png' width='32' height='32' style='border-radius:50%;' alt='mileo'/></a> | Point of Sale: Show VAT number at Customer Tree View
[pos_daily_sales_reports_category_only](pos_daily_sales_reports_category_only/) | 16.0.1.0.1 |  | Show Sales Reports by Category
[pos_default_partner](pos_default_partner/) | 16.0.1.0.3 |  | Add a default customer in pos order
[pos_discount_all](pos_discount_all/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Display discount amount on PoS cashier screen and print it on ticketcalculated from the difference between a sale with default pricelist
[pos_edit_order_line](pos_edit_order_line/) | 16.0.1.0.1 |  | POS Edit Order Line
[pos_escpos_status](pos_escpos_status/) | 16.0.1.0.1 |  | Point of sale: fetch status for 'escpos' driver
[pos_financial_risk](pos_financial_risk/) | 16.0.1.0.1 | <a href='https://github.com/geomer198'><img src='https://github.com/geomer198.png' width='32' height='32' style='border-radius:50%;' alt='geomer198'/></a> <a href='https://github.com/CetmixGitDrone'><img src='https://github.com/CetmixGitDrone.png' width='32' height='32' style='border-radius:50%;' alt='CetmixGitDrone'/></a> | Point of Sale Fonancial Risk
[pos_global_discount_in_line](pos_global_discount_in_line/) | 16.0.1.0.1 |  | Order discount in line instead of discount product
[pos_hide_banknote_button](pos_hide_banknote_button/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Hide useless Banknote buttons in the PoS (+10, +20, +50)
[pos_hide_empty_category](pos_hide_empty_category/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Hide PoS categories that doesn't have any products
[pos_hide_partner_info](pos_hide_partner_info/) | 16.0.1.0.0 |  | Hide phone and address fields in PoS customer list
[pos_hr_access_right](pos_hr_access_right/) | 16.0.1.0.1 | <a href='https://github.com/adasatorres'><img src='https://github.com/adasatorres.png' width='32' height='32' style='border-radius:50%;' alt='adasatorres'/></a> | Point of Sale HR - Extra Access Right for certain actions
[pos_lot_barcode](pos_lot_barcode/) | 16.0.1.0.1 |  | Scan barcode to enter lot/serial numbers
[pos_lot_selection](pos_lot_selection/) | 16.0.1.0.1 |  | POS Lot Selection
[pos_loyalty_exclude](pos_loyalty_exclude/) | 16.0.1.0.1 |  | Exclude products from sale loyalty program in POS
[pos_loyalty_redeem_payment](pos_loyalty_redeem_payment/) | 16.0.1.0.2 |  | Use vouchers as payment method in pos orders
[pos_margin](pos_margin/) | 16.0.1.0.2 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Margin on PoS Order
[pos_margin_stored](pos_margin_stored/) | 16.0.1.0.0 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Margin Stored on PoS Order and Pos Order Line
[pos_meal_voucher](pos_meal_voucher/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Handle meal vouchers in Point of Sale with eligible amount and max amount
[pos_membership](pos_membership/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Implement features of membership module in the Point of sale UI.
[pos_membership_extension](pos_membership_extension/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Prevent to sale product in the point of sale to customer that don't belong to membership categories
[pos_minimize_menu](pos_minimize_menu/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Reduce size of the main menu of the point of sale.
[pos_order_new_line](pos_order_new_line/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Allow cashier to create a new order line, instead of merging the quantity with a previous line
[pos_order_remove_line](pos_order_remove_line/) | 16.0.1.2.2 | <a href='https://github.com/robyf70'><img src='https://github.com/robyf70.png' width='32' height='32' style='border-radius:50%;' alt='robyf70'/></a> | Add button to remove POS order line.
[pos_order_reorder](pos_order_reorder/) | 16.0.0.1.3 |  | Simple Re-order in the Point of Sale
[pos_order_to_sale_order](pos_order_to_sale_order/) | 16.0.1.1.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | PoS Order To Sale Order
[pos_order_to_sale_order_delivery](pos_order_to_sale_order_delivery/) | 16.0.1.0.2 | <a href='https://github.com/GabbasovDinar'><img src='https://github.com/GabbasovDinar.png' width='32' height='32' style='border-radius:50%;' alt='GabbasovDinar'/></a> <a href='https://github.com/CetmixGitDrone'><img src='https://github.com/CetmixGitDrone.png' width='32' height='32' style='border-radius:50%;' alt='CetmixGitDrone'/></a> | Compatibility of pos_order_to_sale_order and delivery modules
[pos_order_to_sale_order_report](pos_order_to_sale_order_report/) | 16.0.1.0.2 |  | Report will be downloaded after the sales order is created.
[pos_order_to_sale_order_sale_financial_risk](pos_order_to_sale_order_sale_financial_risk/) | 16.0.1.0.1 | <a href='https://github.com/geomer198'><img src='https://github.com/geomer198.png' width='32' height='32' style='border-radius:50%;' alt='geomer198'/></a> <a href='https://github.com/CetmixGitDrone'><img src='https://github.com/CetmixGitDrone.png' width='32' height='32' style='border-radius:50%;' alt='CetmixGitDrone'/></a> | Sale Financial Risk control for Sales Orders created from POS
[pos_partner_alternative_pricelist_load_background](pos_partner_alternative_pricelist_load_background/) | 16.0.1.0.0 |  | Load partner alternative pricelist in background
[pos_partner_birthdate](pos_partner_birthdate/) | 16.0.1.0.5 | <a href='https://github.com/ecino'><img src='https://github.com/ecino.png' width='32' height='32' style='border-radius:50%;' alt='ecino'/></a> | Adds the birthdate in the customer screen of POS
[pos_partner_firstname](pos_partner_firstname/) | 16.0.2.0.0 | <a href='https://github.com/robyf70'><img src='https://github.com/robyf70.png' width='32' height='32' style='border-radius:50%;' alt='robyf70'/></a> | POS Support of partner firstname
[pos_partner_is_company](pos_partner_is_company/) | 16.0.2.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | POS Support of 'Is Company' partner field
[pos_partner_load_new_data](pos_partner_load_new_data/) | 16.0.1.0.0 | <a href='https://github.com/flaenen'><img src='https://github.com/flaenen.png' width='32' height='32' style='border-radius:50%;' alt='flaenen'/></a> | Load new partner data during a POS sale
[pos_partner_location_abstract](pos_partner_location_abstract/) | 16.0.1.0.1 |  | POS Partner Location Abstract
[pos_partner_location_google_map](pos_partner_location_google_map/) | 16.0.1.0.1 |  | POS Partner Location Google Map
[pos_partner_no_create](pos_partner_no_create/) | 16.0.1.0.0 |  | Forbid customer creation from the POS
[pos_partner_pricelist_load_background](pos_partner_pricelist_load_background/) | 16.0.1.0.0 |  | Pos
[pos_partner_sale_warning](pos_partner_sale_warning/) | 16.0.1.0.0 |  | Show partner sales warning in POS
[pos_payment_change](pos_payment_change/) | 16.0.1.1.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Allow cashier to change order payments, as long as the session is not closed.
[pos_payment_description](pos_payment_description/) | 16.0.1.1.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Payment description on order tree view
[pos_payment_method_cashdro](pos_payment_method_cashdro/) | 16.0.1.0.0 |  | Allows to pay with CashDro Terminals on the Point of Sale
[pos_payment_method_change_policy](pos_payment_method_change_policy/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Adds alternative way to handle Change in Point of Sale.
[pos_payment_method_image](pos_payment_method_image/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add images on Payment Methods available in the PoS
[pos_payment_restriction](pos_payment_restriction/) | 16.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Adds restrictions options on POS payment level
[pos_payment_show_order](pos_payment_show_order/) | 16.0.1.0.0 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Improve POS Payment Screen by displaying order
[pos_payment_terminal](pos_payment_terminal/) | 16.0.1.0.3 |  | Point of sale: support generic payment terminal
[pos_payment_usability](pos_payment_usability/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Improve payment screen in the PoS front office
[pos_picking_delayed](pos_picking_delayed/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Delay the creation of the picking when PoS order is created
[pos_picking_load](pos_picking_load/) | 16.0.1.1.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Load and confirm stock pickings via Point Of Sale
[pos_place](pos_place/) | 16.0.1.0.2 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Define places on PoS orders
[pos_price_to_weight](pos_price_to_weight/) | 16.0.1.1.0 |  | Compute weight based on barcodes with prices
[pos_pricelist_technical](pos_pricelist_technical/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Prevent technical pricelists from being displayed in the Point of Sale front-end UI
[pos_product_display_default_code](pos_product_display_default_code/) | 16.0.1.0.1 |  | pos: display product default code before product name
[pos_product_label](pos_product_label/) | 16.0.1.0.2 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Print product labels from the POS
[pos_product_mergeable_line](pos_product_mergeable_line/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Allows to configure at the product level, if an order line can be merged or not.
[pos_product_multi_barcode](pos_product_multi_barcode/) | 16.0.1.0.2 |  | Make product multi barcodes usable in the point of sale
[pos_product_packaging_container_deposit](pos_product_packaging_container_deposit/) | 16.0.1.1.0 |  | Add the container deposit fees in a POS order
[pos_product_packaging_multi_barcode](pos_product_packaging_multi_barcode/) | 16.0.1.0.0 |  | Make product packaging multi barcodes usable in the point of sale
[pos_product_pricelist_alternative](pos_product_pricelist_alternative/) | 16.0.1.0.0 |  | Calculate POS product price based on alternative pricelists
[pos_product_quick_info](pos_product_quick_info/) | 16.0.1.0.2 |  | Display product info by one click in Point of Sale
[pos_receipt_hide_info](pos_receipt_hide_info/) | 16.0.1.0.1 |  | Removes Information from POS receipt.
[pos_receipt_hide_price](pos_receipt_hide_price/) | 16.0.1.0.0 |  | Add button to remove price from receipt.
[pos_receipt_replace_user_by_trigram](pos_receipt_replace_user_by_trigram/) | 16.0.2.0.0 |  | Replace User by Trigram in POS receipt.
[pos_receipt_replace_user_by_trigram_hr](pos_receipt_replace_user_by_trigram_hr/) | 16.0.1.0.1 |  | Link module between pos_receipt_replace_user_by_trigram and pos_hr
[pos_receipt_usability](pos_receipt_usability/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Improve receipt screen in the PoS front office
[pos_receipt_vat_detail](pos_receipt_vat_detail/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add Vat Details on Receipt (base and vat amounts).
[pos_report_session_summary](pos_report_session_summary/) | 16.0.1.0.0 |  | Adds a Session Summary PDF report on the POS session
[pos_require_product_quantity](pos_require_product_quantity/) | 16.0.1.0.0 |  | A popup is shown if product quantity is set to 0 for one or more order lines when clicking on "Payment" button.
[pos_reset_search](pos_reset_search/) | 16.0.1.0.0 | <a href='https://github.com/fkawala'><img src='https://github.com/fkawala.png' width='32' height='32' style='border-radius:50%;' alt='fkawala'/></a> | Point of Sale - Clear product search when user clicks on a product.
[pos_restaurant_receipt_usability](pos_restaurant_receipt_usability/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Improve receipt screen in the PoS Restaurant front office
[pos_restaurant_split_order_usability](pos_restaurant_split_order_usability/) | 16.0.1.0.0 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Improve POS Split Screen by displaying already paid lines
[pos_sale_order_print](pos_sale_order_print/) | 16.0.1.0.2 |  | Print multiple sale orders in POS
[pos_sale_product_config_no_variant](pos_sale_product_config_no_variant/) | 16.0.1.0.1 | <a href='https://github.com/ursais'><img src='https://github.com/ursais.png' width='32' height='32' style='border-radius:50%;' alt='ursais'/></a> | Manage Point Of Sale via Configurator of no variant
[pos_screen_element_custom_size](pos_screen_element_custom_size/) | 16.0.1.0.0 |  | Set custom size for POS screen elements
[pos_session_pay_invoice](pos_session_pay_invoice/) | 16.0.1.0.3 |  | Pay and receive invoices from PoS Session
[pos_stock_available_online](pos_stock_available_online/) | 16.0.2.0.3 |  | Show the available quantity of products in the Point of Sale
[pos_supplierinfo_search](pos_supplierinfo_search/) | 16.0.1.0.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Search products by supplier data
[pos_tare](pos_tare/) | 16.0.1.1.0 | <a href='https://github.com/fkawala'><img src='https://github.com/fkawala.png' width='32' height='32' style='border-radius:50%;' alt='fkawala'/></a> <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Manage Tare in Point Of Sale module
[pos_ticket_extra_company_info](pos_ticket_extra_company_info/) | 16.0.1.0.1 |  | Add extra company infos on the ticket
[pos_ticket_extra_company_info_l10n_fr](pos_ticket_extra_company_info_l10n_fr/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add siret company infos on the ticket
[pos_timeout](pos_timeout/) | 16.0.1.0.0 |  | Set the timeout of the point of sale
[pos_to_weight_by_product_uom](pos_to_weight_by_product_uom/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Make 'To Weight' default value depending on product UoM settings

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# product-attribute
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/product-attribute&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/product-attribute/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/product-attribute/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/product-attribute/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/product-attribute/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/product-attribute/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/product-attribute)
[![Translation Status](https://translation.odoo-community.org/widgets/product-attribute-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/product-attribute-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_product_mass_addition](base_product_mass_addition/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Base Product Mass Addition
[pos_product_cost_security](pos_product_cost_security/) | 16.0.1.0.0 |  | Compatibility between Point of Sale and Product Cost Security
[product_abc_classification](product_abc_classification/) | 16.0.2.0.0 |  | ABC classification for sales and warehouse management
[product_abc_classification_sale_stock](product_abc_classification_sale_stock/) | 16.0.1.0.3 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> <a href='https://github.com/lmarion-source'><img src='https://github.com/lmarion-source.png' width='32' height='32' style='border-radius:50%;' alt='lmarion-source'/></a> | Compute ABC classification from the number of delivered sale order line by product
[product_assortment](product_assortment/) | 16.0.2.0.2 |  | Adds the ability to manage products assortment
[product_attachment_link](product_attachment_link/) | 16.0.1.0.0 |  | Product Attachment Link
[product_attachment_zipped_download](product_attachment_zipped_download/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Product Attachment Zipped Download
[product_attribute_archive](product_attribute_archive/) | 16.0.1.0.0 |  | Add an active field on product attributes
[product_attribute_company_favorite](product_attribute_company_favorite/) | 16.0.1.0.0 | <a href='https://github.com/victor-champonnois'><img src='https://github.com/victor-champonnois.png' width='32' height='32' style='border-radius:50%;' alt='victor-champonnois'/></a> | Possibility to set favorite product attributes per company
[product_attribute_model_link](product_attribute_model_link/) | 16.0.1.0.1 |  | Use any model records as product attribute values
[product_attribute_value_dependent_mixin](product_attribute_value_dependent_mixin/) | 16.0.1.2.0 |  | Mixin to make product attribute values fields on models
[product_attribute_value_menu](product_attribute_value_menu/) | 16.0.1.0.1 |  | Product attributes values tree and form. Import attribute values.
[product_catalog](product_catalog/) | 16.0.1.0.0 |  | Backport of Odoos v17 product catalog
[product_catalog_sale](product_catalog_sale/) | 16.0.1.0.0 |  | Backport of Odoos v17 product catalog for sale orders
[product_catalog_stock](product_catalog_stock/) | 16.0.1.0.0 |  | Use the product catalog on stock pickings
[product_category_active](product_category_active/) | 16.0.2.0.1 |  | Add option to archive product categories
[product_category_code](product_category_code/) | 16.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Allows to define a code on product categories
[product_category_code_unique](product_category_code_unique/) | 16.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Allows to set product category code field as unique
[product_category_description](product_category_description/) | 16.0.1.0.0 | <a href='https://github.com/MarcBForgeFlow'><img src='https://github.com/MarcBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='MarcBForgeFlow'/></a> | Allows to add a detailed description for a product category.
[product_category_hr_department](product_category_hr_department/) | 16.0.1.0.0 | <a href='https://github.com/smaciaosi'><img src='https://github.com/smaciaosi.png' width='32' height='32' style='border-radius:50%;' alt='smaciaosi'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Link product categories to hr departments
[product_category_level](product_category_level/) | 16.0.1.0.0 | <a href='https://github.com/PierrickBrun'><img src='https://github.com/PierrickBrun.png' width='32' height='32' style='border-radius:50%;' alt='PierrickBrun'/></a> | Add Level field on Product Categories to show the recursion level on the category
[product_category_product_qty](product_category_product_qty/) | 16.0.1.0.0 |  | Product Category - Product Quantity
[product_category_type](product_category_type/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add Type field on Product Categories to distinguish between parent and final categories
[product_category_usage_group](product_category_usage_group/) | 16.0.1.0.0 |  | Restrict Usage of Product Categories to a given Group
[product_code_mandatory](product_code_mandatory/) | 16.0.1.0.0 |  | Set Product Internal Reference as a required field
[product_code_mixin](product_code_mixin/) | 16.0.1.0.0 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Make product code available for any inherited model
[product_code_regex_validation](product_code_regex_validation/) | 16.0.1.0.0 |  | Configure regEx validation for product codes.
[product_code_unique](product_code_unique/) | 16.0.1.0.1 |  | Set Product Internal Reference as Unique
[product_company_default](product_company_default/) | 16.0.1.0.0 |  | Product Company Default
[product_compute_template_field_from_variant_helper](product_compute_template_field_from_variant_helper/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add technical helper to compute easily template fields from product variant fields
[product_cost_security](product_cost_security/) | 16.0.2.3.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Product cost security restriction view
[product_country_restriction](product_country_restriction/) | 16.0.1.0.1 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Allows to define product restrictions country based
[product_dimension](product_dimension/) | 16.0.1.2.0 |  | Product Dimension
[product_english_name](product_english_name/) | 16.0.1.0.0 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Display the product name in English besides the product name in the users language.
[product_expiry_configurable](product_expiry_configurable/) | 16.0.1.0.1 |  | This model allows setting expiry times on category and to use the 'end_of_life' date for the computation of lot dates
[product_get_price_helper](product_get_price_helper/) | 16.0.1.1.0 |  | This module provides a helper function to compute product prices.
[product_internal_reference_generator](product_internal_reference_generator/) | 16.0.1.0.0 | <a href='https://github.com/ilyasProgrammer'><img src='https://github.com/ilyasProgrammer.png' width='32' height='32' style='border-radius:50%;' alt='ilyasProgrammer'/></a> | Product template and variant reference based on sequence
[product_is_bulk](product_is_bulk/) | 16.0.2.0.0 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Compute or Set Product as Bulk
[product_list_price_from_pricelist](product_list_price_from_pricelist/) | 16.0.1.0.0 | <a href='https://github.com/carlos-lopez-tecnativa'><img src='https://github.com/carlos-lopez-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='carlos-lopez-tecnativa'/></a> | Compute product sales price from a pricelist
[product_logistics_uom](product_logistics_uom/) | 16.0.3.1.0 | <a href='https://github.com/hparfr'><img src='https://github.com/hparfr.png' width='32' height='32' style='border-radius:50%;' alt='hparfr'/></a> | Configure product weights and volume UoM
[product_logistics_uom_net_weight](product_logistics_uom_net_weight/) | 16.0.1.0.0 | <a href='https://github.com/factorlibre'><img src='https://github.com/factorlibre.png' width='32' height='32' style='border-radius:50%;' alt='factorlibre'/></a> | Integration module for product_logistics_uom and product_net_weight compatibility
[product_lot_sequence](product_lot_sequence/) | 16.0.1.0.2 |  | Adds ability to define a lot sequence from the product
[product_main_supplierinfo](product_main_supplierinfo/) | 16.0.1.0.0 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Display the main vendor of a product.
[product_manufacturer](product_manufacturer/) | 16.0.1.0.1 |  | Adds manufacturers and attributes on the product view.
[product_multi_category](product_multi_category/) | 16.0.1.0.0 |  | Product - Many Categories
[product_multi_image](product_multi_image/) | 16.0.1.0.0 |  | Add multiple images for a product, a.k.a. an image gallery.
[product_multi_price](product_multi_price/) | 16.0.1.0.0 |  | Product Multi Price
[product_net_weight](product_net_weight/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add 'Net Weight' on product models
[product_optional_product_quantity](product_optional_product_quantity/) | 16.0.1.1.0 |  | Specify optional products quantity for product
[product_origin](product_origin/) | 16.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Adds the origin of the product
[product_packaging_container_deposit](product_packaging_container_deposit/) | 16.0.1.2.1 |  | Add container deposit fees in a order
[product_packaging_dimension](product_packaging_dimension/) | 16.0.1.1.1 |  | Manage packaging dimensions and weight
[product_packaging_level](product_packaging_level/) | 16.0.1.2.1 |  | This module binds a product packaging to a packaging level
[product_packaging_level_purchasable](product_packaging_level_purchasable/) | 16.0.1.1.0 |  | Control purchase of products via packaging settings.
[product_packaging_level_salable](product_packaging_level_salable/) | 16.0.1.0.0 |  | Product Packaging level salable
[product_pricelist_alternative](product_pricelist_alternative/) | 16.0.1.2.1 |  | Calculate product price based on alternative pricelists
[product_pricelist_direct_print](product_pricelist_direct_print/) | 16.0.1.4.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Print price list from menu option, product templates, products variants or price lists
[product_pricelist_direct_print_company_group](product_pricelist_direct_print_company_group/) | 16.0.1.0.0 |  | Print Pricelist items using the company group model
[product_pricelist_direct_print_website_sale](product_pricelist_direct_print_website_sale/) | 16.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Extend Product Pricelist Direct Print for filter by public categories
[product_pricelist_direct_print_xlsx](product_pricelist_direct_print_xlsx/) | 16.0.1.1.0 |  | Print price list in XLSX format
[product_pricelist_fixed_currency_rate](product_pricelist_fixed_currency_rate/) | 16.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Set a fixed currency rate between pricelists
[product_pricelist_item_list_view](product_pricelist_item_list_view/) | 16.0.1.1.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | View and search the list of pricelist items
[product_pricelist_item_uom](product_pricelist_item_uom/) | 16.0.1.0.0 | <a href='https://github.com/SirAionTech'><img src='https://github.com/SirAionTech.png' width='32' height='32' style='border-radius:50%;' alt='SirAionTech'/></a> | Set UoM in Pricelist Rules.
[product_pricelist_margin](product_pricelist_margin/) | 16.0.1.1.0 |  | This module shows the product's cost and margin from the pricelists.
[product_pricelist_revision](product_pricelist_revision/) | 16.0.1.0.1 |  | Product Pricelist Revision
[product_pricelist_simulation](product_pricelist_simulation/) | 16.0.1.1.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Simulate the product price for all pricelists
[product_pricelist_simulation_margin](product_pricelist_simulation_margin/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add margin of product price for all pricelists
[product_pricelist_supplierinfo](product_pricelist_supplierinfo/) | 16.0.1.1.0 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Allows to create priceslists based on supplier info
[product_print_category](product_print_category/) | 16.0.1.0.8 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Define print categories for products and automate products print, when data has changed
[product_product_template_link](product_product_template_link/) | 16.0.1.0.0 |  | Adds a button in product to view the template
[product_profile](product_profile/) | 16.0.1.0.1 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> <a href='https://github.com/kevinkhao'><img src='https://github.com/kevinkhao.png' width='32' height='32' style='border-radius:50%;' alt='kevinkhao'/></a> | Allow to configure a product in 1 click
[product_restricted_type](product_restricted_type/) | 16.0.1.0.0 |  | Product Restricted Type
[product_route_mto](product_route_mto/) | 16.0.1.0.0 |  | This module allows to compute if a product is an 'MTO' one from its configured routes
[product_sale_description](product_sale_description/) | 16.0.1.0.1 |  | Long and short description for products
[product_secondary_unit](product_secondary_unit/) | 16.0.1.0.3 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Set a secondary unit per product
[product_sequence](product_sequence/) | 16.0.2.0.1 |  | Product Sequence
[product_set](product_set/) | 16.0.3.0.0 |  | Product set
[product_simple_seasonality](product_simple_seasonality/) | 16.0.1.0.0 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> <a href='https://github.com/kevinkhao'><img src='https://github.com/kevinkhao.png' width='32' height='32' style='border-radius:50%;' alt='kevinkhao'/></a> | Product seasonality
[product_standard_price_tax_included](product_standard_price_tax_included/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Brings a Cost Price Field Tax Included on Product Model
[product_state](product_state/) | 16.0.1.2.0 | <a href='https://github.com/emagdalenaC2i'><img src='https://github.com/emagdalenaC2i.png' width='32' height='32' style='border-radius:50%;' alt='emagdalenaC2i'/></a> | Module introducing a state field on product template
[product_sticker](product_sticker/) | 16.0.3.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Product Sticker
[product_stock_state](product_stock_state/) | 16.0.1.1.0 | <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/kevinkhao'><img src='https://github.com/kevinkhao.png' width='32' height='32' style='border-radius:50%;' alt='kevinkhao'/></a> | Compute the state of a product's stockthe stock level and sale_ok field
[product_supplierinfo_archive](product_supplierinfo_archive/) | 16.0.1.0.0 | <a href='https://github.com/GuillemCForgeFlow'><img src='https://github.com/GuillemCForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='GuillemCForgeFlow'/></a> <a href='https://github.com/AlvaroTForgeFlow'><img src='https://github.com/AlvaroTForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='AlvaroTForgeFlow'/></a> <a href='https://github.com/OriolVForgeFlow'><img src='https://github.com/OriolVForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='OriolVForgeFlow'/></a> | Add the active field to the product supplier info
[product_supplierinfo_code](product_supplierinfo_code/) | 16.0.1.0.0 |  | Allows to get main supplierinfo product_code on product level
[product_supplierinfo_for_customer](product_supplierinfo_for_customer/) | 16.0.1.0.6 |  | Allows to define prices for customers in the products
[product_supplierinfo_import_by_barcode](product_supplierinfo_import_by_barcode/) | 16.0.3.0.0 |  | Import supplier pricelists
[product_supplierinfo_import_by_barcode_margin](product_supplierinfo_import_by_barcode_margin/) | 16.0.1.0.0 |  | Import supplier pricelists by barcode and margins
[product_supplierinfo_revision](product_supplierinfo_revision/) | 16.0.1.0.0 |  | Product Supplierinfo Revision
[product_supplierinfo_standard_price](product_supplierinfo_standard_price/) | 16.0.1.0.0 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Product supplier easily connected to product's standard price
[product_supplierinfo_stock_picking_type](product_supplierinfo_stock_picking_type/) | 16.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Product supplierinfo stock picking type
[product_template_default_weight](product_template_default_weight/) | 16.0.1.0.0 | <a href='https://github.com/mathieudelva'><img src='https://github.com/mathieudelva.png' width='32' height='32' style='border-radius:50%;' alt='mathieudelva'/></a> <a href='https://github.com/Kev-Roche'><img src='https://github.com/Kev-Roche.png' width='32' height='32' style='border-radius:50%;' alt='Kev-Roche'/></a> | Add Product Template Default Weight logic
[product_template_has_one_variant](product_template_has_one_variant/) | 16.0.1.0.1 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Allows to define a field on product template level to determine if it has only one variant
[product_template_tags](product_template_tags/) | 16.0.1.1.0 | <a href='https://github.com/patrickrwilson'><img src='https://github.com/patrickrwilson.png' width='32' height='32' style='border-radius:50%;' alt='patrickrwilson'/></a> <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | This addon allow to add tags on products
[product_total_weight_from_packaging](product_total_weight_from_packaging/) | 16.0.1.0.0 |  | Compute estimated weight based on product's packaging weights
[product_uom_measure_type](product_uom_measure_type/) | 16.0.1.0.2 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Product - UoM Measure Type
[product_uom_po_domain](product_uom_po_domain/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Product - Domain on Purchase UoM
[product_uom_updatable](product_uom_updatable/) | 16.0.1.0.0 |  | allows products uom to be modified after be used in a stock picking if the product uom is of the same category
[product_uom_use_type](product_uom_use_type/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Define UoM for Sale and / or for Purchase purpose
[product_usability](product_usability/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Adds missing menu entries for Product module and adds extra groups to fine-tune access rights
[product_variant_attribute_name_manager](product_variant_attribute_name_manager/) | 16.0.1.1.0 | <a href='https://github.com/JordiMForgeFlow'><img src='https://github.com/JordiMForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiMForgeFlow'/></a> | Manage how to display the attributes on the product variant name.
[purchase_product_template_tags](purchase_product_template_tags/) | 16.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Show product tags menu in Purchase app
[sale_product_template_tags](sale_product_template_tags/) | 16.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Show product tags menu in Sale app
[stock_lot_is_archived](stock_lot_is_archived/) | 16.0.1.0.0 |  | This module adds a simple property on Lots that means a lot is archived
[stock_product_template_tags](stock_product_template_tags/) | 16.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Show product tags menu in Inventory app
[stock_production_lot_expired_date](stock_production_lot_expired_date/) | 16.0.1.0.1 |  | Stock production lot expired date
[uom_alias](uom_alias/) | 16.0.1.0.1 | <a href='https://github.com/renatonlima'><img src='https://github.com/renatonlima.png' width='32' height='32' style='border-radius:50%;' alt='renatonlima'/></a> | Adds alias for UOM
[uom_category_active](uom_category_active/) | 16.0.1.0.1 |  | Add option to archive UoM categories

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/product-configurator&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/product-configurator/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/product-configurator/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/product-configurator/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/product-configurator/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/product-configurator/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/product-configurator)
[![Translation Status](https://translation.odoo-community.org/widgets/product-configurator-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/product-configurator-16-0/?utm_source=widget)

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
[product_configurator](product_configurator/) | 16.0.1.1.2 | <a href='https://github.com/PCatinean'><img src='https://github.com/PCatinean.png' width='32' height='32' style='border-radius:50%;' alt='PCatinean'/></a> | Base for product configuration interface modules
[product_configurator_mrp](product_configurator_mrp/) | 16.0.1.0.0 | <a href='https://github.com/PCatinean'><img src='https://github.com/PCatinean.png' width='32' height='32' style='border-radius:50%;' alt='PCatinean'/></a> | BOM Support for configurable products
[product_configurator_sale](product_configurator_sale/) | 16.0.1.0.1 | <a href='https://github.com/PCatinean'><img src='https://github.com/PCatinean.png' width='32' height='32' style='border-radius:50%;' alt='PCatinean'/></a> | Product configuration interface modules for Sale

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/product-pack&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/product-pack/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/product-pack/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/product-pack/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/product-pack/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/product-pack/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/product-pack)
[![Translation Status](https://translation.odoo-community.org/widgets/product-pack-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/product-pack-16-0/?utm_source=widget)

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
[product_pack](product_pack/) | 16.0.1.1.0 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | This module allows you to set a product as a Pack
[purchase_product_pack](purchase_product_pack/) | 16.0.1.0.0 |  | This module allows you to buy product packs
[sale_product_pack](sale_product_pack/) | 16.0.1.0.3 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | This module allows you to sell product packs
[sale_stock_product_pack](sale_stock_product_pack/) | 16.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Compatibility module for packs that are storable products
[stock_product_pack](stock_product_pack/) | 16.0.2.0.0 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | This module allows you to get the right available quantities of the packs
[website_sale_product_pack](website_sale_product_pack/) | 16.0.1.0.0 |  | Compatibility module of product pack with e-commerce

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# product-variant
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/product-variant&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/product-variant/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/product-variant/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/product-variant/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/product-variant/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/product-variant/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/product-variant)
[![Translation Status](https://translation.odoo-community.org/widgets/product-variant-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/product-variant-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[product_variant_attribute_tax](product_variant_attribute_tax/) | 16.0.1.0.1 |  | Set taxes on the product attribute values
[product_variant_configurator](product_variant_configurator/) | 16.0.1.0.8 |  | Provides an abstract model for product variant configuration.
[product_variant_default_code](product_variant_default_code/) | 16.0.1.1.4 | <a href='https://github.com/Kev-Roche'><img src='https://github.com/Kev-Roche.png' width='32' height='32' style='border-radius:50%;' alt='Kev-Roche'/></a> | Allow to automatically generate the variant default code
[product_variant_name](product_variant_name/) | 16.0.1.0.0 |  | Product Variant Name
[product_variant_sale_price](product_variant_sale_price/) | 16.0.1.0.2 |  | Allows to write fixed prices in product variants
[product_variant_specific_description](product_variant_specific_description/) | 16.0.1.0.1 |  | Product Variant Specific Description
[purchase_variant_configurator](purchase_variant_configurator/) | 16.0.2.0.2 |  | Product variants in purchase management
[sale_order_line_variant_description](sale_order_line_variant_description/) | 16.0.1.1.0 |  | Sale order line variant description
[sale_product_variant_attribute_tax](sale_product_variant_attribute_tax/) | 16.0.1.0.0 |  | Bring the taxes associated to product values
[sale_variant_configurator](sale_variant_configurator/) | 16.0.1.0.4 |  | Product variants in sale management

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# project
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/project&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/project/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/project/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/project/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/project/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/project/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/project)
[![Translation Status](https://translation.odoo-community.org/widgets/project-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/project-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[project_administrator_restricted_visibility](project_administrator_restricted_visibility/) | 16.0.1.0.2 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | Adds a 'Project Administrator' access group with restricted visibility to 'Projects'
[project_department](project_department/) | 16.0.1.0.0 |  | Project Department Categorization
[project_duplicate_subtask](project_duplicate_subtask/) | 16.0.1.0.0 |  | The module adds an action to duplicate tasks with the child subtasks
[project_hr](project_hr/) | 16.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Link HR with project
[project_internal_access_from_portal](project_internal_access_from_portal/) | 16.0.1.0.1 |  | Show internal projects in portal
[project_key](project_key/) | 16.0.2.0.1 |  | Module decorates projects and tasks with Project Key
[project_list](project_list/) | 16.0.1.0.1 |  | Projects list view
[project_merge](project_merge/) | 16.0.1.0.0 |  | Wizard to merge project tasks
[project_milestone_status](project_milestone_status/) | 16.0.1.0.0 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | Project Milestone Status
[project_milestone_tree](project_milestone_tree/) | 16.0.1.0.0 |  | This module adds an access to the Milestone tree view.
[project_parent](project_parent/) | 16.0.1.1.0 |  | Project Parent
[project_parent_task_filter](project_parent_task_filter/) | 16.0.1.1.0 |  | Add a filter to show the parent tasks
[project_pivot](project_pivot/) | 16.0.1.0.1 |  | Pivot view for projects
[project_portal_task_visibility](project_portal_task_visibility/) | 16.0.1.1.0 |  | Project Portal Task Visibility
[project_purchase_link](project_purchase_link/) | 16.0.1.0.0 |  | Project Purchase Link
[project_required_field_by_stage](project_required_field_by_stage/) | 16.0.1.0.0 |  | This module adds checks to allow certain stages to be set only if some fields are populated. After install every stage can have mandatory fields associated.
[project_reviewer](project_reviewer/) | 16.0.1.0.0 |  | Add the possibility to assign reviewer to a task
[project_risk](project_risk/) | 16.0.1.0.0 |  | MOR risk management method
[project_role](project_role/) | 16.0.1.0.4 | <a href='https://github.com/alexey-pelykh'><img src='https://github.com/alexey-pelykh.png' width='32' height='32' style='border-radius:50%;' alt='alexey-pelykh'/></a> | Project role-based roster
[project_sale_order_link](project_sale_order_link/) | 16.0.1.0.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Sales order linked to project, tasks or employee map
[project_sequence](project_sequence/) | 16.0.1.1.1 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/anddago78'><img src='https://github.com/anddago78.png' width='32' height='32' style='border-radius:50%;' alt='anddago78'/></a> | Add a sequence field to projects, filled automatically
[project_stage_extra_info](project_stage_extra_info/) | 16.0.1.0.0 |  | Project Stage Extra Info
[project_stage_last_update_date](project_stage_last_update_date/) | 16.0.1.0.0 |  | Project Stage Last Update Date
[project_status](project_status/) | 16.0.1.0.0 | <a href='https://github.com/patrickrwilson'><img src='https://github.com/patrickrwilson.png' width='32' height='32' style='border-radius:50%;' alt='patrickrwilson'/></a> | Project Status
[project_stock](project_stock/) | 16.0.2.0.3 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Project Stock
[project_stock_analytic_tag](project_stock_analytic_tag/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Project Stock Analytic Tag
[project_stock_product_set](project_stock_product_set/) | 16.0.2.1.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Project Stock Product Set
[project_tag_hierarchy](project_tag_hierarchy/) | 16.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Project Tag Hierarchy
[project_tag_multicompany](project_tag_multicompany/) | 16.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Project Tag Multicompany
[project_tag_security](project_tag_security/) | 16.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Project Tag Security
[project_task_add_very_high](project_task_add_very_high/) | 16.0.1.1.0 | <a href='https://github.com/astirpe'><img src='https://github.com/astirpe.png' width='32' height='32' style='border-radius:50%;' alt='astirpe'/></a> | Adds extra options 'High' and 'Very High' on tasks
[project_task_code](project_task_code/) | 16.0.1.2.0 |  | Sequential Code for Tasks
[project_task_code_portal](project_task_code_portal/) | 16.0.1.2.0 |  | Use custom task code in customer portal
[project_task_creation_description_notification](project_task_creation_description_notification/) | 16.0.1.0.0 |  | Project task description in notifications
[project_task_default_stage](project_task_default_stage/) | 16.0.1.0.2 |  | Recovery default task stages for projects from v8
[project_task_description_portal](project_task_description_portal/) | 16.0.1.0.0 |  | Dedicated task description for portal users
[project_task_description_template](project_task_description_template/) | 16.0.1.0.0 |  | Add a description template to project tasks
[project_task_link](project_task_link/) | 16.0.1.0.1 |  | Project Task Link
[project_task_material](project_task_material/) | 16.0.1.0.0 |  | Record products spent in a Task
[project_task_name_with_id](project_task_name_with_id/) | 16.0.1.0.1 |  | Project Task Name with ID
[project_task_note](project_task_note/) | 16.0.1.0.1 | <a href='https://github.com/carolina-fernandez'><img src='https://github.com/carolina-fernandez.png' width='32' height='32' style='border-radius:50%;' alt='carolina-fernandez'/></a> | Add notes in project tasks
[project_task_parent_completion_blocking](project_task_parent_completion_blocking/) | 16.0.1.0.0 | <a href='https://github.com/david-banon-tecnativa'><img src='https://github.com/david-banon-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='david-banon-tecnativa'/></a> | Prevents a parent task from being completed if any children task isn't.
[project_task_parent_due_auto](project_task_parent_due_auto/) | 16.0.1.0.1 | <a href='https://github.com/david-banon-tecnativa'><img src='https://github.com/david-banon-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='david-banon-tecnativa'/></a> | Recalculates parent task's due date when child task changes
[project_task_personal_stage_auto_fold](project_task_personal_stage_auto_fold/) | 16.0.1.0.0 |  | Moves task to the first fold personal stage when done
[project_task_project_required](project_task_project_required/) | 16.0.1.1.0 |  | Set project on task as a mandatory field
[project_task_pull_request](project_task_pull_request/) | 16.0.1.1.0 |  | Adds a field for a PR URI to project tasks
[project_task_pull_request_state](project_task_pull_request_state/) | 16.0.1.0.0 |  | Track Pull Request state in tasks
[project_task_recurring_activity](project_task_recurring_activity/) | 16.0.1.0.0 | <a href='https://github.com/dessanhemrayev'><img src='https://github.com/dessanhemrayev.png' width='32' height='32' style='border-radius:50%;' alt='dessanhemrayev'/></a> <a href='https://github.com/CetmixGitDrone'><img src='https://github.com/CetmixGitDrone.png' width='32' height='32' style='border-radius:50%;' alt='CetmixGitDrone'/></a> | Project Task Recurring Activity
[project_task_stage_change_restriction](project_task_stage_change_restriction/) | 16.0.1.0.0 |  | Restrict project task stage
[project_task_stage_mgmt](project_task_stage_mgmt/) | 16.0.1.0.0 | <a href='https://github.com/DavidJForgeFlow'><img src='https://github.com/DavidJForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='DavidJForgeFlow'/></a> | Allows to assign and create task stages on project creation wizard
[project_task_stage_state](project_task_stage_state/) | 16.0.1.0.0 |  | Restore State attribute removed from Project Stages in 8.0
[project_task_tag](project_task_tag/) | 16.0.1.0.0 |  | Limit tags available on task
[project_template](project_template/) | 16.0.1.0.0 | <a href='https://github.com/patrickrwilson'><img src='https://github.com/patrickrwilson.png' width='32' height='32' style='border-radius:50%;' alt='patrickrwilson'/></a> | Project Templates
[project_timeline](project_timeline/) | 16.0.2.2.0 |  | Timeline view for projects
[project_timeline_hr_timesheet](project_timeline_hr_timesheet/) | 16.0.1.0.0 |  | Shows the progress of tasks on the timeline view.
[project_timesheet_time_control](project_timesheet_time_control/) | 16.0.1.0.4 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | Project timesheet time control
[project_type](project_type/) | 16.0.1.0.1 |  | Project Types
[project_update_portal](project_update_portal/) | 16.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Allows portal access for project and update followers
[project_update_visible](project_update_visible/) | 16.0.1.0.0 |  | Visible project_id in project.update view form.
[project_version](project_version/) | 16.0.1.0.0 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | Project Version
[sale_project_copy_tasks](sale_project_copy_tasks/) | 16.0.1.0.4 | <a href='https://github.com/shide'><img src='https://github.com/shide.png' width='32' height='32' style='border-radius:50%;' alt='shide'/></a> <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Copy tasks into sale order's project
[task_project_status](task_project_status/) | 16.0.1.0.0 |  | Show project status on the task.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/project-reporting


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/project-reporting&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/project-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/project-reporting/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/project-reporting/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/project-reporting/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/project-reporting/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/project-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/project-reporting-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/project-reporting-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# project-reporting

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[project_task_report](project_task_report/) | 16.0.1.0.0 |  | Basic report for project tasks.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/purchase-reporting&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/purchase-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/purchase-reporting/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/purchase-reporting/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/purchase-reporting/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/purchase-reporting/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/purchase-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/purchase-reporting-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/purchase-reporting-16-0/?utm_source=widget)

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
[purchase_backorder](purchase_backorder/) | 16.0.1.0.0 | <a href='https://github.com/smangukiya'><img src='https://github.com/smangukiya.png' width='32' height='32' style='border-radius:50%;' alt='smangukiya'/></a> | Report of Un-Invoiced Goods Received and Backorders
[purchase_comment_template](purchase_comment_template/) | 16.0.1.0.0 |  | Comments texts templates on Purchase documents
[purchase_order_report_hide_tax](purchase_order_report_hide_tax/) | 16.0.1.0.2 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Hide taxes column when they don't add value
[purchase_packaging_report](purchase_packaging_report/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Packaging data in purchase reports
[purchase_report_date_format](purchase_report_date_format/) | 16.0.1.0.1 |  | Purchase Report Date Format
[purchase_report_payment_term](purchase_report_payment_term/) | 16.0.1.0.0 |  | Purchase Report Payment Term
[purchase_report_shipping_address](purchase_report_shipping_address/) | 16.0.1.0.0 |  | Purchase Report Shipping Address

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/purchase-workflow&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/purchase-workflow/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/purchase-workflow/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/purchase-workflow/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/purchase-workflow/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/purchase-workflow/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/purchase-workflow)
[![Translation Status](https://translation.odoo-community.org/widgets/purchase-workflow-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/purchase-workflow-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[partner_supplierinfo_smartbutton](partner_supplierinfo_smartbutton/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Access supplied products from the vendor
[procurement_purchase_no_grouping](procurement_purchase_no_grouping/) | 16.0.1.0.0 |  | Procurement Purchase No Grouping
[product_main_seller](product_main_seller/) | 16.0.1.0.2 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Main Vendor for a product
[product_supplier_code_purchase](product_supplier_code_purchase/) | 16.0.1.0.0 |  | This module adds to the purchase order line the supplier code defined in the product.
[product_supplierinfo_disable_autocreation](product_supplierinfo_disable_autocreation/) | 16.0.1.0.0 |  | Add option to disable automatic creation of pricelists for suppliers
[product_supplierinfo_purchase_contact](product_supplierinfo_purchase_contact/) | 16.0.1.0.0 |  | Add Purchase Contact in product supplier info
[product_supplierinfo_qty_multiplier](product_supplierinfo_qty_multiplier/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Product supplierinfo qty multiplier
[product_supplierinfo_security](product_supplierinfo_security/) | 16.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Restricts access to supplier information on products.
[product_supplierinfo_update_price](product_supplierinfo_update_price/) | 16.0.1.0.0 |  | Updates the product's vendor price with the price set in a purchase order.
[purchase_advance_payment](purchase_advance_payment/) | 16.0.1.2.1 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Allow to add advance payments on purchase orders
[purchase_all_shipments](purchase_all_shipments/) | 16.0.1.0.1 |  | Purchase All Shipments
[purchase_allowed_product](purchase_allowed_product/) | 16.0.2.1.1 |  | This module allows to select only products that can be supplied by the vendor
[purchase_analytic_global](purchase_analytic_global/) | 16.0.1.0.0 |  | This module allows to a Global analytic plan in purchases
[purchase_blanket_order](purchase_blanket_order/) | 16.0.2.1.3 |  | Purchase Blanket Orders
[purchase_cancel_reason](purchase_cancel_reason/) | 16.0.1.0.1 |  | Purchase Cancel Reason
[purchase_commercial_partner](purchase_commercial_partner/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add stored related field 'Commercial Supplier' on POs
[purchase_date_planned_manual](purchase_date_planned_manual/) | 16.0.1.0.1 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | This module makes the system to always respect the planned (or scheduled) date in PO lines.
[purchase_default_terms_conditions](purchase_default_terms_conditions/) | 16.0.1.0.3 |  | This module allows purchase default terms & conditions
[purchase_delivery_split_date](purchase_delivery_split_date/) | 16.0.1.0.5 |  | Allows Purchase Order you confirm to generate one Incoming Shipment for each expected date indicated in the Purchase Order Lines
[purchase_deposit](purchase_deposit/) | 16.0.1.1.1 |  | Option to create deposit from purchase order
[purchase_discount](purchase_discount/) | 16.0.2.0.5 |  | Purchase order lines with discounts
[purchase_exception](purchase_exception/) | 16.0.1.0.1 |  | Custom exceptions on purchase order
[purchase_fop_shipping](purchase_fop_shipping/) | 16.0.1.0.1 |  | Purchase Free-Of-Payment shipping
[purchase_force_invoiced](purchase_force_invoiced/) | 16.0.1.0.2 |  | Allows to force the billing status of the purchase order to "Invoiced"
[purchase_force_invoiced_quantity](purchase_force_invoiced_quantity/) | 16.0.1.1.0 |  | Add manual invoice quantity in purchase order lines
[purchase_fully_invoiced](purchase_fully_invoiced/) | 16.0.1.0.0 |  | Useful filters in Purchases to know the actual status of invoices.
[purchase_fully_received](purchase_fully_received/) | 16.0.1.0.0 |  | Useful filters in Purchases to know the actual status of shipments.and invoices
[purchase_invoice_method](purchase_invoice_method/) | 16.0.1.0.0 |  | Allow to force the invoice method of a purchase
[purchase_invoice_new_picking_line](purchase_invoice_new_picking_line/) | 16.0.1.0.0 |  | When creating an invoice from a purchase order, this module also adds invoice lines for products that were in the order's pickings but not in the order itself.
[purchase_invoice_partial_status](purchase_invoice_partial_status/) | 16.0.1.0.0 |  | Adds a 'Partially Invoiced' status to purchase orders for better invoice tracking.
[purchase_invoice_plan](purchase_invoice_plan/) | 16.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Add to purchases order, ability to manage future invoice plan
[purchase_invoice_status_line](purchase_invoice_status_line/) | 16.0.1.0.0 | <a href='https://github.com/JoanSForgeFlow'><img src='https://github.com/JoanSForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JoanSForgeFlow'/></a> | Add invoice status on purchase order lines
[purchase_landed_cost](purchase_landed_cost/) | 16.0.1.0.2 |  | Purchase cost distribution
[purchase_last_price_info](purchase_last_price_info/) | 16.0.1.0.2 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Purchase Product Last Price Info
[purchase_line_procurement_group](purchase_line_procurement_group/) | 16.0.1.0.0 |  | Group purchase order line according to procurement group
[purchase_location_by_line](purchase_location_by_line/) | 16.0.1.0.1 |  | Allows to define a specific destination location on each PO line
[purchase_lot](purchase_lot/) | 16.0.2.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Purchase Lot
[purchase_manual_delivery](purchase_manual_delivery/) | 16.0.2.0.3 |  | Prevents pickings to be auto generated upon Purchase Order confirmation and adds the ability to manually generate them as the supplier confirms the different purchase order lines.
[purchase_merge](purchase_merge/) | 16.0.1.0.3 |  | Wizard to merge purchase with required conditions
[purchase_minimum_amount](purchase_minimum_amount/) | 16.0.1.0.0 |  | Purchase Minimum Amount
[purchase_mto_owner](purchase_mto_owner/) | 16.0.1.0.0 |  | Purchase MTO Owner
[purchase_no_rfq](purchase_no_rfq/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Purchase Order - No Request For Quotation
[purchase_only_by_packaging](purchase_only_by_packaging/) | 16.0.1.0.2 |  | Manage purchase of packaging
[purchase_open_qty](purchase_open_qty/) | 16.0.3.0.1 |  | Allows to identify the purchase orders that have quantities pending to invoice or to receive.
[purchase_order_approval_block](purchase_order_approval_block/) | 16.0.1.0.0 |  | Purchase Order Approval Block
[purchase_order_approved](purchase_order_approved/) | 16.0.1.0.2 |  | Add a new state 'Approved' in purchase orders.
[purchase_order_archive](purchase_order_archive/) | 16.0.1.0.0 |  | Archive Purchase Orders
[purchase_order_downpayment](purchase_order_downpayment/) | 16.0.1.0.0 |  | Allow to add payments from Purchase order view
[purchase_order_duplicate_check](purchase_order_duplicate_check/) | 16.0.1.0.0 |  | Prevents overordering in the Purchase app with a Confirmation Wizard, 'Pending Orders' field, and activity tracking for repeated orders.
[purchase_order_general_discount](purchase_order_general_discount/) | 16.0.1.0.0 |  | General discount per purchase order
[purchase_order_hide_receipt_status](purchase_order_hide_receipt_status/) | 16.0.1.0.1 |  | Purchase Order Hide Receipt Status
[purchase_order_line_deep_sort](purchase_order_line_deep_sort/) | 16.0.1.0.0 |  | Purchase Order Line Sort
[purchase_order_line_menu](purchase_order_line_menu/) | 16.0.2.1.2 |  | Adds Purchase Order Lines Menu
[purchase_order_line_receipt_status](purchase_order_line_receipt_status/) | 16.0.1.0.0 |  | Manage customizations on purchase order line
[purchase_order_line_sequence](purchase_order_line_sequence/) | 16.0.1.0.0 |  | Adds sequence to PO lines and propagates it toInvoice lines and Stock Moves
[purchase_order_line_stock_available](purchase_order_line_stock_available/) | 16.0.1.0.0 |  | Purchase order line stock available
[purchase_order_no_zero_price](purchase_order_no_zero_price/) | 16.0.1.0.1 |  | Prevent zero price lines on Purchase Orders
[purchase_order_owner](purchase_order_owner/) | 16.0.1.0.0 |  | Purchase Order Owner
[purchase_order_price_recalculation](purchase_order_price_recalculation/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Price recalculation in purchases orders
[purchase_order_product_attachment_mgmt](purchase_order_product_attachment_mgmt/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Purchase Order Product Attachment Mgmt
[purchase_order_product_recommendation](purchase_order_product_recommendation/) | 16.0.1.1.0 |  | Recommend products to buy to supplier based on history
[purchase_order_purchase_manager](purchase_order_purchase_manager/) | 16.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Purchase Manager from Supplier in Purchase Order
[purchase_order_qty_change_no_recompute](purchase_order_qty_change_no_recompute/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Prevent recompute if only quantity has changed in purchase order line
[purchase_order_revision](purchase_order_revision/) | 16.0.1.0.0 |  | Keep track of revised quotations
[purchase_order_secondary_unit](purchase_order_secondary_unit/) | 16.0.1.0.0 |  | Purchase product in a secondary unit
[purchase_order_supplier_return](purchase_order_supplier_return/) | 16.0.1.0.0 |  | Return product to supplier and update quantiy received
[purchase_order_supplierinfo_update](purchase_order_supplierinfo_update/) | 16.0.2.0.0 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | Update product supplierinfo with the last purchase price
[purchase_order_type](purchase_order_type/) | 16.0.1.0.3 |  | Purchase Order Type
[purchase_order_type_dashboard](purchase_order_type_dashboard/) | 16.0.1.0.0 | <a href='https://github.com/dalonsod'><img src='https://github.com/dalonsod.png' width='32' height='32' style='border-radius:50%;' alt='dalonsod'/></a> | Purchase Order Type Dashboard
[purchase_order_uninvoiced_amount](purchase_order_uninvoiced_amount/) | 16.0.1.0.2 |  | Purchase Order Univoiced Amount
[purchase_order_uninvoiced_amount_line](purchase_order_uninvoiced_amount_line/) | 16.0.1.0.0 |  | Purchase Order Line Uninvoiced Amount
[purchase_order_weight_volume](purchase_order_weight_volume/) | 16.0.2.2.0 | <a href='https://github.com/ilyasProgrammer'><img src='https://github.com/ilyasProgrammer.png' width='32' height='32' style='border-radius:50%;' alt='ilyasProgrammer'/></a> | Display purchase order weight and volume
[purchase_packaging_default](purchase_packaging_default/) | 16.0.1.1.0 |  | Set default packaging in purchase
[purchase_packaging_level_qty](purchase_packaging_level_qty/) | 16.0.2.0.0 |  | Display purchase order packaging level quantity
[purchase_partner_incoterm](purchase_partner_incoterm/) | 16.0.1.0.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Add a an incoterm field for supplier and use it on purchase order
[purchase_partner_selectable_option](purchase_partner_selectable_option/) | 16.0.1.0.3 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Purchase Partner Selectable Option
[purchase_planned_date_container_deposit](purchase_planned_date_container_deposit/) | 16.0.1.0.0 |  | Glue module between purchase_date_planned_manual and purchase_product_packaging_container_deposit
[purchase_product_packaging_container_deposit](purchase_product_packaging_container_deposit/) | 16.0.1.1.0 |  | Purchase Product Packaging Container Deposit
[purchase_quick](purchase_quick/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Quick Purchase order
[purchase_quick_discount](purchase_quick_discount/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Glue module to add discount field for quick purchase
[purchase_quick_triple_discount](purchase_quick_triple_discount/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Glue module to add discount fields for quick purchase
[purchase_reception_status](purchase_reception_status/) | 16.0.1.0.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add reception status on purchase orders
[purchase_reorder_control](purchase_reorder_control/) | 16.0.1.0.0 |  | Restrict reordering unpurchaseable product
[purchase_request](purchase_request/) | 16.0.2.4.3 |  | Use this module to have notification of requirements of materials and/or external services and keep track of such requirements.
[purchase_request_department](purchase_request_department/) | 16.0.1.1.0 |  | Purchase Request Department
[purchase_request_exception](purchase_request_exception/) | 16.0.1.0.0 |  | Custom exceptions on purchase request
[purchase_request_tier_validation](purchase_request_tier_validation/) | 16.0.1.1.1 |  | Extends the functionality of Purchase Requests to support a tier validation process.
[purchase_request_type](purchase_request_type/) | 16.0.1.2.1 |  | Purchase Request Type
[purchase_requisition_tier_validation](purchase_requisition_tier_validation/) | 16.0.1.0.2 |  | Extends the functionality of Purchase Agreements to support a tier validation process.
[purchase_return](purchase_return/) | 16.0.1.0.4 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> | Manage return orders.
[purchase_sale_link_by_origin](purchase_sale_link_by_origin/) | 16.0.1.0.0 |  | Link PO/SO by the PO's Origin in addition to the default behavior that only links them by their lines
[purchase_security](purchase_security/) | 16.0.2.0.2 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | See only your purchase orders
[purchase_sign](purchase_sign/) | 16.0.1.0.0 |  | Purchase Sign
[purchase_split_by_route](purchase_split_by_route/) | 16.0.1.0.0 | <a href='https://github.com/mathieudelva'><img src='https://github.com/mathieudelva.png' width='32' height='32' style='border-radius:50%;' alt='mathieudelva'/></a> | Purchase Split Route
[purchase_stock_cost_update](purchase_stock_cost_update/) | 16.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Allows to update valuation layers once the purchase is received
[purchase_stock_packaging](purchase_stock_packaging/) | 16.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Allows to transmit the product packaging from the procurement values to the generated purchase order line
[purchase_stock_picking_actual_date_show_currency_rate](purchase_stock_picking_actual_date_show_currency_rate/) | 16.0.1.0.0 |  | Purchase Stock Picking Actual Date Show Currency Rate
[purchase_stock_picking_show_currency_rate](purchase_stock_picking_show_currency_rate/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Show currency rate in purchase stock picking.
[purchase_stock_price_unit_sync](purchase_stock_price_unit_sync/) | 16.0.1.0.1 |  | Update cost price in stock moves already done
[purchase_stock_tier_validation](purchase_stock_tier_validation/) | 16.0.1.0.0 | <a href='https://github.com/bosd'><img src='https://github.com/bosd.png' width='32' height='32' style='border-radius:50%;' alt='bosd'/></a> | Exclude RFQs pending to validate when procuring
[purchase_supplierinfo_editable_tree](purchase_supplierinfo_editable_tree/) | 16.0.1.0.1 |  | Set the supplierinfo tree view as editablee
[purchase_tag](purchase_tag/) | 16.0.1.1.0 |  | Allows to add multiple tags to purchase orders
[purchase_tier_validation](purchase_tier_validation/) | 16.0.1.1.1 |  | Extends the functionality of Purchase Orders to support a tier validation process.
[purchase_transport_mode](purchase_transport_mode/) | 16.0.1.1.0 |  | Purchase expection based on constraints
[purchase_triple_discount](purchase_triple_discount/) | 16.0.3.0.4 |  | Manage triple discount on purchase order lines
[purchase_uninvoiced_amount_force_invoiced_line](purchase_uninvoiced_amount_force_invoiced_line/) | 16.0.1.0.0 | <a href='https://github.com/JoanSForgeFlow'><img src='https://github.com/JoanSForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JoanSForgeFlow'/></a> | Glue module between uninvoiced amount line and force invoiced line
[purchase_vendor_promotion](purchase_vendor_promotion/) | 16.0.2.0.0 |  | Purchase Vendor Promotion
[purchase_warn_message](purchase_warn_message/) | 16.0.1.0.0 |  | Add a popup warning on purchase to ensure warning is populated
[purchase_work_acceptance](purchase_work_acceptance/) | 16.0.1.0.0 | <a href='https://github.com/ps-tubtim'><img src='https://github.com/ps-tubtim.png' width='32' height='32' style='border-radius:50%;' alt='ps-tubtim'/></a> | Purchase Work Acceptance
[purchase_work_acceptance_evaluation](purchase_work_acceptance_evaluation/) | 16.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Purchase Work Acceptance Evaluation
[sale_purchase_force_vendor](sale_purchase_force_vendor/) | 16.0.1.0.3 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Sale Purchase Force Vendor
[supplier_calendar](supplier_calendar/) | 16.0.1.0.1 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Supplier Calendar

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# Queue Job
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/queue&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/queue/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/queue/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/queue/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/queue/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/queue/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/queue)
[![Translation Status](https://translation.odoo-community.org/widgets/queue-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/queue-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Asynchronous Job Queue. Delay Model methods in asynchronous jobs, executed in the background as soon as possible or on a schedule. Support Channels to segregates jobs in different queues with different capacities. Unlike scheduled tasks, a job captures arguments for later processing.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_export_async](base_export_async/) | 16.0.1.2.0 |  | Asynchronous export with job queue
[base_import_async](base_import_async/) | 16.0.1.2.1 |  | Import CSV files in the background
[queue_job](queue_job/) | 16.0.3.0.2 | <a href='https://github.com/guewen'><img src='https://github.com/guewen.png' width='32' height='32' style='border-radius:50%;' alt='guewen'/></a> <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Job Queue
[queue_job_batch](queue_job_batch/) | 16.0.1.0.1 |  | Job Queue Batch
[queue_job_cron](queue_job_cron/) | 16.0.2.1.0 |  | Scheduled Actions as Queue Jobs
[queue_job_cron_jobrunner](queue_job_cron_jobrunner/) | 16.0.1.1.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Run jobs without a dedicated JobRunner
[queue_job_subscribe](queue_job_subscribe/) | 16.0.1.1.0 |  | Control which users are subscribed to queue job notifications
[queue_job_web_notify](queue_job_web_notify/) | 16.0.1.0.0 |  | This module allows to display a notification to the related user of a failed job. It uses the web_notify notification feature.
[test_queue_job](test_queue_job/) | 16.0.2.5.1 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Queue Job Tests
[test_queue_job_batch](test_queue_job_batch/) | 16.0.1.0.0 |  | Test Job Queue Batch


Unported addons
---------------
addon | version | maintainers | summary
--- | --- | --- | ---
[test_base_import_async](test_base_import_async/) | 14.0.1.0.1 (unported) |  | Test suite for base_import_async. Normally you don't need to install this.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# Repair
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/repair&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/repair/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/repair/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/repair/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/repair/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/repair/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/repair)
[![Translation Status](https://translation.odoo-community.org/widgets/repair-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/repair-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Odoo modules related to repairs.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_repair_config](base_repair_config/) | 16.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Provides general settings for the Repair App
[repair_calendar_view](repair_calendar_view/) | 16.0.1.0.0 |  | Repair Calendar View
[repair_comment_template](repair_comment_template/) | 16.0.1.0.0 | <a href='https://github.com/cubells'><img src='https://github.com/cubells.png' width='32' height='32' style='border-radius:50%;' alt='cubells'/></a> | Comments templates on Repair documents
[repair_discount](repair_discount/) | 16.0.1.0.0 |  | Repair Discount
[repair_follow_lot_location](repair_follow_lot_location/) | 16.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Auto-sync repair currentlocation from the lot’s location
[repair_picking_after_done](repair_picking_after_done/) | 16.0.1.0.2 |  | Transfer repaired move to another location directly from repaire order
[repair_purchase_return](repair_purchase_return/) | 16.0.1.0.1 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> | Create a Purchase Return from a Repair
[repair_quality_control](repair_quality_control/) | 16.0.1.0.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Create quality controls from repair order
[repair_reason](repair_reason/) | 16.0.1.0.0 |  | Repair Reason
[repair_refurbish](repair_refurbish/) | 16.0.1.0.0 |  | Create refurbished products during repair
[repair_reinvoice](repair_reinvoice/) | 16.0.1.0.0 |  | Repair Reinvoice in odoo
[repair_sale_order](repair_sale_order/) | 16.0.1.0.1 | <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | Repair To Sale Order
[repair_security](repair_security/) | 16.0.1.0.0 |  | Create security groups for Repair
[repair_stock](repair_stock/) | 16.0.1.0.0 |  | Repair Stock
[repair_stock_move](repair_stock_move/) | 16.0.1.1.0 |  | Ongoing Repair Stock Moves Definition in odoo
[repair_type](repair_type/) | 16.0.1.0.2 |  | Repair type
[repair_type_refurbish](repair_type_refurbish/) | 16.0.1.0.0 |  | Repair type
[repair_type_sequence](repair_type_sequence/) | 16.0.1.0.0 | <a href='https://github.com/AaronHForgeFlow'><img src='https://github.com/AaronHForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='AaronHForgeFlow'/></a> | Adds sequence to repair orders defined in the repairs's type
[repair_warehouse](repair_warehouse/) | 16.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This addon

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# report-print-send
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/report-print-send&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/report-print-send/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/report-print-send/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/report-print-send/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/report-print-send/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/report-print-send/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/report-print-send)
[![Translation Status](https://translation.odoo-community.org/widgets/report-print-send-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/report-print-send-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_report_to_label_printer](base_report_to_label_printer/) | 16.0.1.0.1 |  | Report to label printer
[base_report_to_printer](base_report_to_printer/) | 16.0.1.5.2 |  | Report to printer
[base_report_to_printer_mail](base_report_to_printer_mail/) | 16.0.1.0.0 |  | Report to printer - Mail extension
[pingen](pingen/) | 16.0.1.1.0 | <a href='https://github.com/ajaniszewska-dev'><img src='https://github.com/ajaniszewska-dev.png' width='32' height='32' style='border-radius:50%;' alt='ajaniszewska-dev'/></a> <a href='https://github.com/grindtildeath'><img src='https://github.com/grindtildeath.png' width='32' height='32' style='border-radius:50%;' alt='grindtildeath'/></a> | pingen.com integration
[pingen_env](pingen_env/) | 16.0.1.1.0 | <a href='https://github.com/ajaniszewska-dev'><img src='https://github.com/ajaniszewska-dev.png' width='32' height='32' style='border-radius:50%;' alt='ajaniszewska-dev'/></a> <a href='https://github.com/grindtildeath'><img src='https://github.com/grindtildeath.png' width='32' height='32' style='border-radius:50%;' alt='grindtildeath'/></a> | pingen.com server environment
[printer_zpl2](printer_zpl2/) | 16.0.1.1.2 |  | Add a ZPL II label printing feature
[printing_simple_configuration](printing_simple_configuration/) | 16.0.1.1.0 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Allow to set printing configuration in company or in warehouse
[remote_report_to_printer](remote_report_to_printer/) | 16.0.1.0.1 |  | Report to printer on remotes

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/reporting-engine&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/reporting-engine/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/reporting-engine/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/reporting-engine/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/reporting-engine/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/reporting-engine/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/reporting-engine)
[![Translation Status](https://translation.odoo-community.org/widgets/reporting-engine-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/reporting-engine-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_comment_template](base_comment_template/) | 16.0.2.3.0 |  | Add conditional mako template to any reporton models that inherits comment.template.
[bi_sql_editor](bi_sql_editor/) | 16.0.2.0.2 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | BI Views builder, based on Materialized or Normal SQL Views
[bi_view_editor](bi_view_editor/) | 16.0.1.1.0 |  | Graphical BI views builder for Odoo
[bi_view_editor_spreadsheet_dashboard](bi_view_editor_spreadsheet_dashboard/) | 16.0.1.0.0 |  | Glue module for BI View Editor and Spreadsheet Dashboard
[report_async](report_async/) | 16.0.1.1.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Central place to run reports live or async
[report_company_details_translatable](report_company_details_translatable/) | 16.0.1.0.0 |  | Report Company Details Translatable
[report_context](report_context/) | 16.0.1.0.0 |  | Adding context to reports
[report_csv](report_csv/) | 16.0.2.1.1 |  | Base module to create csv report
[report_display_name_in_footer](report_display_name_in_footer/) | 16.0.1.1.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Show document name in report footer
[report_docx](report_docx/) | 16.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Create report templates in DOCX and receive DOCX files
[report_footer_html](report_footer_html/) | 16.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Show HTML content in desired Footer Reports
[report_generate_helper](report_generate_helper/) | 16.0.1.0.0 |  | Helper to easily generate report
[report_label](report_label/) | 16.0.1.0.1 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Print configurable self-adhesive labels reports
[report_paperformat_company_dependent](report_paperformat_company_dependent/) | 16.0.1.0.0 |  | Report Paperformat Company Dependent
[report_partner_address](report_partner_address/) | 16.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Translatable partner address details for reports and portal
[report_py3o](report_py3o/) | 16.0.1.0.6 |  | Reporting engine based on Libreoffice (ODT -> ODT, ODT -> PDF, ODT -> DOC, ODT -> DOCX, ODS -> ODS, etc.)
[report_py3o_fusion_server](report_py3o_fusion_server/) | 16.0.1.0.0 |  | Let the fusion server handle format conversion.
[report_qr](report_qr/) | 16.0.1.0.0 |  | Web QR Manager
[report_qweb_decimal_place](report_qweb_decimal_place/) | 16.0.1.0.0 |  | Report Qweb Decimal Place
[report_qweb_element_page_visibility](report_qweb_element_page_visibility/) | 16.0.1.0.1 |  | Report Qweb Element Page Visibility
[report_qweb_encrypt](report_qweb_encrypt/) | 16.0.1.0.2 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Allow to encrypt qweb pdfs
[report_qweb_field_option](report_qweb_field_option/) | 16.0.1.0.3 |  | Report Qweb Field Option
[report_qweb_parameter](report_qweb_parameter/) | 16.0.1.0.1 |  | Add new parameters for qweb templates in order to reduce field length and check minimal length
[report_qweb_pdf_cover](report_qweb_pdf_cover/) | 16.0.1.0.0 |  | Add front and back covers to your QWeb PDF reports
[report_qweb_pdf_watermark](report_qweb_pdf_watermark/) | 16.0.1.0.1 |  | Add watermarks to your QWEB PDF reports
[report_qweb_signer](report_qweb_signer/) | 16.0.1.0.5 |  | Sign Qweb PDFs usign a PKCS#12 certificate
[report_substitute](report_substitute/) | 16.0.1.1.2 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This module allows to create substitution rules for report actions.
[report_text_format_option](report_text_format_option/) | 16.0.1.0.0 |  | Report Text Format Option
[report_wkhtmltopdf_param](report_wkhtmltopdf_param/) | 16.0.1.0.0 |  | Add new parameters for a paper format to be used by wkhtmltopdf command as arguments.
[report_xlsx](report_xlsx/) | 16.0.2.0.2 |  | Base module to create xlsx report
[report_xlsx_helper](report_xlsx_helper/) | 16.0.1.0.0 |  | Report xlsx helpers
[report_xml](report_xml/) | 16.0.1.1.3 |  | Allow to generate XML reports
[sql_export](sql_export/) | 16.0.2.2.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Export data in csv file with SQL requests
[sql_export_delta](sql_export_delta/) | 16.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Support exporting only the changes from last export
[sql_export_excel](sql_export_excel/) | 16.0.1.0.1 |  | Allow to export a sql query to an excel file.
[sql_export_mail](sql_export_mail/) | 16.0.2.1.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Send csv file generated by sql query by mail.
[sql_request_abstract](sql_request_abstract/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Abstract Model to manage SQL Requests

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# Rest Frameworks
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/rest-framework&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/rest-framework/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/rest-framework/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/rest-framework/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/rest-framework/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/rest-framework/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/rest-framework)
[![Translation Status](https://translation.odoo-community.org/widgets/rest-framework-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/rest-framework-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

This repository has nice modules to interact with Odoo using JSON and HTTP requests.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[api_log](api_log/) | 16.0.1.1.0 | <a href='https://github.com/paradoxxxzero'><img src='https://github.com/paradoxxxzero.png' width='32' height='32' style='border-radius:50%;' alt='paradoxxxzero'/></a> | Log API requests in database
[api_log_mail](api_log_mail/) | 16.0.1.0.2 | <a href='https://github.com/SirPyTech'><img src='https://github.com/SirPyTech.png' width='32' height='32' style='border-radius:50%;' alt='SirPyTech'/></a> | Notify logged exceptions.
[auth_partner](auth_partner/) | 16.0.1.0.1 |  | Implements the base features for a authenticable partner
[base_rest](base_rest/) | 16.0.1.0.6 |  | Develop your own high level REST APIs for Odoo thanks to this addon.
[base_rest_auth_api_key](base_rest_auth_api_key/) | 16.0.1.0.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Base Rest: Add support for the auth_api_key security policy into the openapi documentation
[base_rest_datamodel](base_rest_datamodel/) | 16.0.1.0.0 |  | Datamodel binding for base_rest
[base_rest_demo](base_rest_demo/) | 16.0.2.0.4 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Demo addon for Base REST
[base_rest_pydantic](base_rest_pydantic/) | 16.0.2.0.1 |  | Pydantic binding for base_rest
[datamodel](datamodel/) | 16.0.1.0.2 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | This addon allows you to define simple data models supporting serialization/deserialization
[extendable](extendable/) | 16.0.1.0.2 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Extendable classes registry loader for Odoo
[extendable_fastapi](extendable_fastapi/) | 16.0.2.1.2 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Allows the use of extendable into fastapi apps
[fastapi](fastapi/) | 16.0.2.0.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Odoo FastAPI endpoint
[fastapi_auth_jwt](fastapi_auth_jwt/) | 16.0.1.0.4 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | JWT bearer token authentication for FastAPI.
[fastapi_auth_jwt_demo](fastapi_auth_jwt_demo/) | 16.0.2.0.1 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Test/demo module for fastapi_auth_jwt.
[fastapi_auth_partner](fastapi_auth_partner/) | 16.0.1.0.0 |  | This provides an implementation of auth_partner for FastAPI
[fastapi_encrypted_errors](fastapi_encrypted_errors/) | 16.0.1.0.1 | <a href='https://github.com/paradoxxxzero'><img src='https://github.com/paradoxxxzero.png' width='32' height='32' style='border-radius:50%;' alt='paradoxxxzero'/></a> | Adds encrypted error messages to FastAPI error responses.
[fastapi_endpoint_context](fastapi_endpoint_context/) | 16.0.1.0.0 | <a href='https://github.com/paradoxxxzero'><img src='https://github.com/paradoxxxzero.png' width='32' height='32' style='border-radius:50%;' alt='paradoxxxzero'/></a> | Provides an overridable request context for FastAPI endpoints
[fastapi_log](fastapi_log/) | 16.0.1.1.0 | <a href='https://github.com/paradoxxxzero'><img src='https://github.com/paradoxxxzero.png' width='32' height='32' style='border-radius:50%;' alt='paradoxxxzero'/></a> | Log Fastapi requests in database
[fastapi_log_mail](fastapi_log_mail/) | 16.0.1.1.0 | <a href='https://github.com/SirPyTech'><img src='https://github.com/SirPyTech.png' width='32' height='32' style='border-radius:50%;' alt='SirPyTech'/></a> | Notify logged exceptions.
[graphql_base](graphql_base/) | 16.0.1.0.2 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Base GraphQL/GraphiQL controller
[graphql_demo](graphql_demo/) | 16.0.1.0.1 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | GraphQL Demo
[pydantic](pydantic/) | 16.0.1.0.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Utility addon to ease mapping between Pydantic and Odoo models
[rest_log](rest_log/) | 16.0.1.0.4 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Track REST API calls into DB


Unported addons
---------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_rest_auth_jwt](base_rest_auth_jwt/) | 15.0.1.1.0 (unported) | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Base Rest: Add support for the auth_jwt security policy into the openapi documentation
[base_rest_auth_user_service](base_rest_auth_user_service/) | 15.0.1.0.1 (unported) |  | Login/logout from session using a REST call
[model_serializer](model_serializer/) | 15.0.1.2.0 (unported) | <a href='https://github.com/fdegrave'><img src='https://github.com/fdegrave.png' width='32' height='32' style='border-radius:50%;' alt='fdegrave'/></a> | Automatically translate Odoo models into Datamodels for (de)serialization

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# rma
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/rma&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/rma/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/rma/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/rma/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/rma/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/rma/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/rma)
[![Translation Status](https://translation.odoo-community.org/widgets/rma-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/rma-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[product_warranty](product_warranty/) | 16.0.1.0.0 | <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Product Warranty
[rma](rma/) | 16.0.5.3.7 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Return Merchandise Authorization (RMA)
[rma_delivery](rma_delivery/) | 16.0.1.1.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allow to choose a default delivery carrier for returns
[rma_lot](rma_lot/) | 16.0.1.0.1 |  | Manage lot in RMA
[rma_lot_autocreate](rma_lot_autocreate/) | 16.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Auto-generate stock lot at RMA confirm using per-operation sequence
[rma_procurement_customer](rma_procurement_customer/) | 16.0.1.0.0 |  | Rma Procurement Customer
[rma_reason](rma_reason/) | 16.0.1.0.1 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Rma Reason
[rma_repair](rma_repair/) | 16.0.1.2.0 | <a href='https://github.com/peluko00'><img src='https://github.com/peluko00.png' width='32' height='32' style='border-radius:50%;' alt='peluko00'/></a> | Create a repair order from rma
[rma_sale](rma_sale/) | 16.0.4.0.2 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Sale Order - Return Merchandise Authorization (RMA)
[rma_sale_lot](rma_sale_lot/) | 16.0.1.0.0 |  | Manage sale returns with lot.
[rma_sale_mrp](rma_sale_mrp/) | 16.0.2.2.2 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allow doing RMAs from MRP kits
[rma_sale_reason](rma_sale_reason/) | 16.0.1.1.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Rma Sale Reason

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sale-blanket&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/sale-blanket/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/sale-blanket/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/sale-blanket/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/sale-blanket/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/sale-blanket/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-blanket)
[![Translation Status](https://translation.odoo-community.org/widgets/sale-blanket-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sale-blanket-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

sale-blanket

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[sale_order_blanket_order](sale_order_blanket_order/) | 16.0.1.2.3 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Manage blanket order and call of order
[sale_order_blanket_order_sale_margin](sale_order_blanket_order_sale_margin/) | 16.0.1.0.0 |  | Ensure sale margins are properly set on call off order lines
[sale_order_blanket_order_stock_prebook](sale_order_blanket_order_stock_prebook/) | 16.0.1.0.1 |  | Allow to prebook stock for blanket order
[sale_order_blanket_order_stock_prebook_release](sale_order_blanket_order_stock_prebook_release/) | 16.0.1.2.0 |  | Ensure that the date priotity when releasing qty is the start date of the blanker order

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# Sale Channel
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sale-channel&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/sale-channel/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/sale-channel/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/sale-channel/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/sale-channel/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/sale-channel/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-channel)
[![Translation Status](https://translation.odoo-community.org/widgets/sale-channel-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sale-channel-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Add the concept of channel on sale order, invoice...

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[sale_channel](sale_channel/) | 16.0.0.2.2 |  | Adds the notion of sale channels
[sale_channel_category](sale_channel_category/) | 16.0.1.0.2 |  | Link Category with sale channel
[sale_channel_partner](sale_channel_partner/) | 16.0.0.0.0 |  | Bind sale channels to contacts
[sale_channel_product](sale_channel_product/) | 16.0.1.0.2 |  | Link Product with sale channel
[sale_channel_search_engine](sale_channel_search_engine/) | 16.0.0.1.2 |  | Abstract module for configuring a search engine on a sale channel
[sale_channel_search_engine_category](sale_channel_search_engine_category/) | 16.0.0.1.2 |  | Implement an export of category in search engine based on sale channel link
[sale_channel_search_engine_demo](sale_channel_search_engine_demo/) | 16.0.0.0.1 |  | Implement an export of category in search engine based on sale channel link
[sale_channel_search_engine_product](sale_channel_search_engine_product/) | 16.0.0.1.1 |  | Implement an export of category in search engine based on sale channel link
[sale_import_base](sale_import_base/) | 16.0.2.0.1 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Base for importing Sale Orders through a JSON file format

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sale-prebook&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/sale-prebook/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/sale-prebook/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/sale-prebook/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/sale-prebook/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/sale-prebook/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-prebook)
[![Translation Status](https://translation.odoo-community.org/widgets/sale-prebook-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sale-prebook-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Manage stock reservations for non confirmed sales orders

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[sale_exception_stock_prebook](sale_exception_stock_prebook/) | 16.0.1.1.0 | <a href='https://github.com/mt-software-de'><img src='https://github.com/mt-software-de.png' width='32' height='32' style='border-radius:50%;' alt='mt-software-de'/></a> | Glue Addon to no release reservation if sale order has exceptions
[sale_stock_prebook](sale_stock_prebook/) | 16.0.2.1.1 | <a href='https://github.com/mt-software-de'><img src='https://github.com/mt-software-de.png' width='32' height='32' style='border-radius:50%;' alt='mt-software-de'/></a> | Add process to prebook a sale order's stock before confirming it
[sale_stock_prebook_cancel_line](sale_stock_prebook_cancel_line/) | 16.0.1.0.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Takes into account prebook pickings into the computation of cancelled qty on the sale order lines
[sale_stock_prebook_stock_available_to_promise_release](sale_stock_prebook_stock_available_to_promise_release/) | 16.0.1.1.0 | <a href='https://github.com/mt-software-de'><img src='https://github.com/mt-software-de.png' width='32' height='32' style='border-radius:50%;' alt='mt-software-de'/></a> | Extends the previous available qty to promised with moves of a reservation

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sale-promotion&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/sale-promotion/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/sale-promotion/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/sale-promotion/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/sale-promotion/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/sale-promotion/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-promotion)
[![Translation Status](https://translation.odoo-community.org/widgets/sale-promotion-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sale-promotion-16-0/?utm_source=widget)

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
[coupon_chatter](coupon_chatter/) | 16.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Register messages and activities on the sale coupon records
[loyalty_criteria_multi_product](loyalty_criteria_multi_product/) | 16.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allows to set as promotion criteria multi-product conditions
[loyalty_incompatibility](loyalty_incompatibility/) | 16.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allows to set incompatibility rules between promotions
[loyalty_initial_date_validity](loyalty_initial_date_validity/) | 16.0.1.0.1 |  | Set a start date for a promotion
[loyalty_limit](loyalty_limit/) | 16.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Restrict number of promotions per customer or salesman
[loyalty_mass_mailing](loyalty_mass_mailing/) | 16.0.2.0.0 |  | Loyalty Mass Mailing
[loyalty_multi_gift](loyalty_multi_gift/) | 16.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allows to configure multiple gift rewards per promotion
[loyalty_partner_applicability](loyalty_partner_applicability/) | 16.0.4.0.0 |  | Enables the definition of a customer filter for promotion rules that will only be applied to customers who meet the specified conditions in the filter.
[sale_loyalty_auto_refresh](sale_loyalty_auto_refresh/) | 16.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/SilvioC2C'><img src='https://github.com/SilvioC2C.png' width='32' height='32' style='border-radius:50%;' alt='SilvioC2C'/></a> | Allows to auto-apply the coupons with no user intervention
[sale_loyalty_criteria_multi_product](sale_loyalty_criteria_multi_product/) | 16.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allows to set as promotion criteria multi-product conditions
[sale_loyalty_incompatibility](sale_loyalty_incompatibility/) | 16.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allows to set incompatibility rules between promotions in sale orders
[sale_loyalty_initial_date_validity](sale_loyalty_initial_date_validity/) | 16.0.1.0.1 |  | Sale Loyalty Initial Date Validity
[sale_loyalty_limit](sale_loyalty_limit/) | 16.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Restrict number of promotions per customer or salesman
[sale_loyalty_multi_gift](sale_loyalty_multi_gift/) | 16.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allows to configure multiple gift rewards per promotion in sales
[sale_loyalty_order_info](sale_loyalty_order_info/) | 16.0.1.0.0 |  | Add info on sale order about applied loyalties
[sale_loyalty_order_line_link](sale_loyalty_order_line_link/) | 16.0.1.1.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Adds a link between loyalty programs and their generated order linesfor easing tracking
[sale_loyalty_order_suggestion](sale_loyalty_order_suggestion/) | 16.0.1.0.5 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Suggest promotions in the sale order line
[sale_loyalty_order_suggestion_multi_gift](sale_loyalty_order_suggestion_multi_gift/) | 16.0.1.0.1 |  | Suggest promotions with rewards multi gift in the sale order line
[sale_loyalty_order_suggestion_multi_product](sale_loyalty_order_suggestion_multi_product/) | 16.0.1.0.2 |  | Suggest promotions with criteria multi product in the sale order line
[sale_loyalty_partner](sale_loyalty_partner/) | 16.0.1.0.0 |  | Sale Loyalty Partner
[sale_loyalty_partner_applicability](sale_loyalty_partner_applicability/) | 16.0.3.0.0 |  | Enables the definition of a customer filter for promotion rules that will only be applied to customers who meet the specified conditions in the filter.
[website_sale_loyalty_page](website_sale_loyalty_page/) | 16.0.1.0.0 |  | Website Sale Loyalty Page
[website_sale_loyalty_suggestion_wizard](website_sale_loyalty_suggestion_wizard/) | 16.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Suggests promotions and allows you to configure and apply these promotions directly from the website
[website_sale_loyalty_suggestion_wizard_multi_gift](website_sale_loyalty_suggestion_wizard_multi_gift/) | 16.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Suggests promotions multi-gift and allows you to configure and apply these promotions directly from the website
[website_sale_loyalty_suggestion_wizard_multi_product](website_sale_loyalty_suggestion_wizard_multi_product/) | 16.0.1.0.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Suggests promotions multi-product and allows you to configure and apply these promotions directly from the website

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# sale-reporting
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sale-reporting&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/sale-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/sale-reporting/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/sale-reporting/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/sale-reporting/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/sale-reporting/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/sale-reporting-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sale-reporting-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_multicompany_reporting_currency](account_multicompany_reporting_currency/) | 16.0.1.0.0 | <a href='https://github.com/yankinmax'><img src='https://github.com/yankinmax.png' width='32' height='32' style='border-radius:50%;' alt='yankinmax'/></a> <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Adds Amount in multicompany reporting currency to Account Moves
[base_multicompany_reporting_currency](base_multicompany_reporting_currency/) | 16.0.2.0.0 |  | Adds the possibility to specify Multicompany Reporting Currency
[product_sold_by_delivery_week](product_sold_by_delivery_week/) | 16.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Adds a field that graphically hints the weekly product sales
[sale_comment_template](sale_comment_template/) | 16.0.1.0.1 |  | Comments texts templates on Sale documents
[sale_layout_category_hide_detail](sale_layout_category_hide_detail/) | 16.0.1.1.2 |  | Hide details for sections in sale orders and invoices for reports and customer portal
[sale_multicompany_reporting_currency](sale_multicompany_reporting_currency/) | 16.0.1.0.0 | <a href='https://github.com/yankinmax'><img src='https://github.com/yankinmax.png' width='32' height='32' style='border-radius:50%;' alt='yankinmax'/></a> | Adds Amount in multicompany reporting currency to Sale Order
[sale_order_line_position](sale_order_line_position/) | 16.0.1.3.0 |  | Adds position number on sale order line.
[sale_order_product_recommendation_product_sold_by_delivery_week](sale_order_product_recommendation_product_sold_by_delivery_week/) | 16.0.1.1.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Adds the weekly sales field to the recommendation wizard
[sale_order_report_hide_tax](sale_order_report_hide_tax/) | 16.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Hide taxes column when they don't add value
[sale_order_report_product_image](sale_order_report_product_image/) | 16.0.1.0.1 |  | Show product images on Sale documents
[sale_order_weight](sale_order_weight/) | 16.0.1.0.0 |  | Add products weight in report for sale order
[sale_packaging_report](sale_packaging_report/) | 16.0.1.1.0 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Packaging data in sale reports
[sale_report_commitment_date](sale_report_commitment_date/) | 16.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Display the commitment date on Sales Order analysis reports
[sale_report_country_state](sale_report_country_state/) | 16.0.1.0.0 |  | Sale Report Filter by State
[sale_report_delivered](sale_report_delivered/) | 16.0.2.2.5 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Sale Report Delivered
[sale_report_delivered_attribute_values](sale_report_delivered_attribute_values/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Allow to view Attribute values of Lines on Sale Report Delivered
[sale_report_delivered_deposit](sale_report_delivered_deposit/) | 16.0.2.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Allow to view Customer Deposits on Sale Report Delivered
[sale_report_delivered_price_compliance](sale_report_delivered_price_compliance/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Allow to view Price Compliance Tiers on Sale Report Delivered
[sale_report_delivered_subtotal](sale_report_delivered_subtotal/) | 16.0.1.0.1 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Sale Report Delivered subtotal
[sale_report_delivered_volume](sale_report_delivered_volume/) | 16.0.1.0.0 |  | Sale Report Delivered Volume
[sale_report_salesman](sale_report_salesman/) | 16.0.1.0.0 | <a href='https://github.com/carolina-fernandez'><img src='https://github.com/carolina-fernandez.png' width='32' height='32' style='border-radius:50%;' alt='carolina-fernandez'/></a> | Sale Report Salesman
[sale_report_salesperson_from_partner](sale_report_salesperson_from_partner/) | 16.0.1.1.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Sale Report Salesperson From Partner

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# sale-workflow
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sale-workflow&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/sale-workflow/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/sale-workflow/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/sale-workflow/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/sale-workflow/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/sale-workflow/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-workflow)
[![Translation Status](https://translation.odoo-community.org/widgets/sale-workflow-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sale-workflow-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_invoice_pricelist_technical](account_invoice_pricelist_technical/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Prevent technical pricelists from being selected on invoice forms
[partner_contact_sale_info_propagation](partner_contact_sale_info_propagation/) | 16.0.1.0.1 |  | Propagate Salesperson and Sales Channel from Company to Contacts
[partner_sale_pivot](partner_sale_pivot/) | 16.0.1.0.0 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | Sales analysis from customer form view
[portal_sale_accept_terms](portal_sale_accept_terms/) | 16.0.1.0.1 | <a href='https://github.com/SirAionTech'><img src='https://github.com/SirAionTech.png' width='32' height='32' style='border-radius:50%;' alt='SirAionTech'/></a> | Portal Sale accept Terms
[portal_sale_order_search](portal_sale_order_search/) | 16.0.1.1.0 | <a href='https://github.com/pilarvargas-tecnativa'><img src='https://github.com/pilarvargas-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='pilarvargas-tecnativa'/></a> | Allow customers to set and search their own order reference in portal
[portal_sale_personal_data_only](portal_sale_personal_data_only/) | 16.0.1.0.0 |  | Portal Sale Personal Data Only
[pricelist_cache](pricelist_cache/) | 16.0.1.0.0 |  | Provide a new model to cache price lists and update it, to make it easier to retrieve them.
[pricelist_price_base_custom](pricelist_price_base_custom/) | 16.0.1.0.0 |  | Use custom value as a base for pricelist calculation.
[product_form_sale_link](product_form_sale_link/) | 16.0.1.0.1 |  | Adds a button on product forms to access Sale Lines
[product_price_category](product_price_category/) | 16.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Add Price Category field on product and allow to apply a pricelist on this field.
[product_supplierinfo_for_customer_sale](product_supplierinfo_for_customer_sale/) | 16.0.1.0.2 |  | Loads in every sale order line the customer code defined in the product
[sale_advance_payment](sale_advance_payment/) | 16.0.1.1.2 |  | Allow to add advance payments on sales and then use them on invoices
[sale_attached_product](sale_attached_product/) | 16.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Define products that will be added automatically when adding another in a sales order
[sale_auto_remove_zero_quantity_lines](sale_auto_remove_zero_quantity_lines/) | 16.0.1.1.0 |  | On sale confirmation remove lines with zero quantities
[sale_automatic_workflow](sale_automatic_workflow/) | 16.0.1.1.1 |  | Sale Automatic Workflow
[sale_automatic_workflow_job](sale_automatic_workflow_job/) | 16.0.1.0.0 |  | Execute sale automatic workflows in queue jobs
[sale_automatic_workflow_payment_mode](sale_automatic_workflow_payment_mode/) | 16.0.1.0.0 |  | Sale Automatic Workflow - Payment Mode
[sale_blanket_order](sale_blanket_order/) | 16.0.2.3.1 |  | Blanket Orders
[sale_block_no_stock](sale_block_no_stock/) | 16.0.2.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Block Sales if products has not enough Quantity based on a chosen field
[sale_cancel_reason](sale_cancel_reason/) | 16.0.1.0.1 |  | Sale Cancel Reason
[sale_commercial_partner](sale_commercial_partner/) | 16.0.1.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add stored related field 'Commercial Entity' on sale orders
[sale_company_currency](sale_company_currency/) | 16.0.1.0.1 |  | Company Currency in Sale Orders
[sale_delivery_split_date](sale_delivery_split_date/) | 16.0.2.0.0 |  | Sale Deliveries split by date
[sale_delivery_state](sale_delivery_state/) | 16.0.2.0.1 |  | Show the delivery state on the sale order
[sale_discount_display_amount](sale_discount_display_amount/) | 16.0.1.2.2 |  | This addon intends to display the amount of the discount computed on sale_order_line and sale_order level
[sale_elaboration](sale_elaboration/) | 16.0.1.8.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Set an elaboration for any sale line
[sale_exception](sale_exception/) | 16.0.2.0.0 |  | Custom exceptions on sale order
[sale_exception_holidays_public](sale_exception_holidays_public/) | 16.0.1.0.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Raise a sale exception if there is a commitment_date on the SO and this date is a public holidays for the shipping partner address
[sale_fixed_discount](sale_fixed_discount/) | 16.0.1.0.3 |  | Allows to apply fixed amount discounts in sales orders.
[sale_force_invoiced](sale_force_invoiced/) | 16.0.2.1.2 |  | Allows to force the invoice status of the sales order to Invoiced
[sale_force_invoiced_quantity](sale_force_invoiced_quantity/) | 16.0.1.0.0 |  | Add manual invoice quantity in sales order lines
[sale_fully_invoiced](sale_fully_invoiced/) | 16.0.1.0.0 |  | Useful filters in Sales to know the actual status of invoices.
[sale_global_discount](sale_global_discount/) | 16.0.2.0.0 |  | Sale Global Discount
[sale_invoice_blocking](sale_invoice_blocking/) | 16.0.1.0.1 |  | Allow you to block the creation of invoices from a sale order.
[sale_invoice_frequency](sale_invoice_frequency/) | 16.0.1.2.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Define the invoice frequency for customers
[sale_invoice_plan](sale_invoice_plan/) | 16.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Add to sales order, ability to manage future invoice plan
[sale_invoice_policy](sale_invoice_policy/) | 16.0.3.0.0 |  | Sales Management: let the user choose the invoice policy on the order
[sale_invoice_split_payment](sale_invoice_split_payment/) | 16.0.1.0.0 |  | Split by payment term generated invoices from sale orders
[sale_isolated_quotation](sale_isolated_quotation/) | 16.0.1.0.0 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Sale Isolated Quotation
[sale_last_price_info](sale_last_price_info/) | 16.0.1.0.0 |  | Product Last Price Info - Sale
[sale_loyalty_exclude](sale_loyalty_exclude/) | 16.0.1.2.0 |  | Exclude products from sale loyalty program
[sale_manual_delivery](sale_manual_delivery/) | 16.0.1.1.0 |  | Create manually your deliveries
[sale_margin_update](sale_margin_update/) | 16.0.1.0.0 |  | Recalculate expected unit price from margin.
[sale_mrp_bom](sale_mrp_bom/) | 16.0.1.0.0 |  | Allows define a BOM in the sales lines.
[sale_numeric_step](sale_numeric_step/) | 16.0.1.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Improve mobile/tablet sale process by adding numeric step widgets
[sale_order_amount_to_invoice](sale_order_amount_to_invoice/) | 16.0.1.0.0 |  | Show total amount to invoice in quotations/sales orders
[sale_order_archive](sale_order_archive/) | 16.0.1.0.0 |  | Archive Sale Orders
[sale_order_carrier_auto_assign](sale_order_carrier_auto_assign/) | 16.0.1.2.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Auto assign delivery carrier on sale order confirmation
[sale_order_country_allowed_product](sale_order_country_allowed_product/) | 16.0.1.0.0 |  | Restrict products in sales by country
[sale_order_currency_rate](sale_order_currency_rate/) | 16.0.2.0.0 |  | Currency Rate in Sale Order
[sale_order_end_user](sale_order_end_user/) | 16.0.1.0.0 |  | Allows to define the end user in sale orders if there is an intermediate between shipping and this end user
[sale_order_general_discount](sale_order_general_discount/) | 16.0.1.2.0 |  | General discount per sale order
[sale_order_general_discount_triple](sale_order_general_discount_triple/) | 16.0.2.1.0 | <a href='https://github.com/ashishhirapara'><img src='https://github.com/ashishhirapara.png' width='32' height='32' style='border-radius:50%;' alt='ashishhirapara'/></a> | General discount per sale order with triple
[sale_order_invoice_amount](sale_order_invoice_amount/) | 16.0.1.0.3 |  | Display the invoiced and uninvoiced total in the sale order
[sale_order_invoicing_finished_task](sale_order_invoicing_finished_task/) | 16.0.2.0.0 |  | Control invoice order lines if their related task has been set to invoiceable
[sale_order_invoicing_picking_filter](sale_order_invoicing_picking_filter/) | 16.0.1.1.0 |  | Create invoices from sale orders based on the products in pickings.
[sale_order_line_cancel](sale_order_line_cancel/) | 16.0.2.0.1 |  | Sale cancel remaining
[sale_order_line_cancel_sale_stock](sale_order_line_cancel_sale_stock/) | 16.0.2.0.1 |  | Sale cancel remaining stock
[sale_order_line_date](sale_order_line_date/) | 16.0.1.1.2 |  | Adds a commitment date to each sale order line.
[sale_order_line_delivery_state](sale_order_line_delivery_state/) | 16.0.1.0.0 |  | Show the delivery state on the sale order line
[sale_order_line_description](sale_order_line_description/) | 16.0.1.0.0 |  | Sale order line description
[sale_order_line_effective_date](sale_order_line_effective_date/) | 16.0.1.1.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Calculated effective dates in Sale Order Lines
[sale_order_line_field_from_product_attribute](sale_order_line_field_from_product_attribute/) | 16.0.1.0.0 |  | Store Attribute value sis Sales Order line fields
[sale_order_line_input](sale_order_line_input/) | 16.0.1.0.1 |  | Search, create or modify directly sale order lines
[sale_order_line_menu](sale_order_line_menu/) | 16.0.1.3.2 |  | Adds a Sale Order Lines Menu
[sale_order_line_move_to_optional](sale_order_line_move_to_optional/) | 16.0.1.0.0 |  | Move sale order line to optional products.
[sale_order_line_multi_warehouse](sale_order_line_multi_warehouse/) | 16.0.1.0.0 |  | Sale Order Line Multi Warehouse
[sale_order_line_no_print](sale_order_line_no_print/) | 16.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Hide order lines in reports
[sale_order_line_price_history](sale_order_line_price_history/) | 16.0.1.2.2 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Sale order line price history
[sale_order_line_price_lock_by_pricelist](sale_order_line_price_lock_by_pricelist/) | 16.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Lock price or discount edition depending on pricelist items
[sale_order_line_product_attribute_values](sale_order_line_product_attribute_values/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Store Product Attribute Values in Sale Order Lines
[sale_order_line_remove](sale_order_line_remove/) | 16.0.1.0.0 |  | Allows removal of sale order lines from confirmed orders if not invoiced or received
[sale_order_line_sequence](sale_order_line_sequence/) | 16.0.2.2.0 |  | Propagates SO line sequence to invoices and stock picking.
[sale_order_line_tag](sale_order_line_tag/) | 16.0.1.0.0 | <a href='https://github.com/smaciaosi'><img src='https://github.com/smaciaosi.png' width='32' height='32' style='border-radius:50%;' alt='smaciaosi'/></a> <a href='https://github.com/dreispt'><img src='https://github.com/dreispt.png' width='32' height='32' style='border-radius:50%;' alt='dreispt'/></a> <a href='https://github.com/ckolobow'><img src='https://github.com/ckolobow.png' width='32' height='32' style='border-radius:50%;' alt='ckolobow'/></a> | Add tags to classify sales order line reasons
[sale_order_lot_generator](sale_order_lot_generator/) | 16.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> <a href='https://github.com/mourad-ehm'><img src='https://github.com/mourad-ehm.png' width='32' height='32' style='border-radius:50%;' alt='mourad-ehm'/></a> <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Sale Order Lot Generator
[sale_order_lot_selection](sale_order_lot_selection/) | 16.0.2.0.1 | <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> | Sale Order Lot Selection
[sale_order_mass_action](sale_order_mass_action/) | 16.0.1.0.1 |  | Allows to easy mass operations on sale orders.
[sale_order_minimum_amount](sale_order_minimum_amount/) | 16.0.1.0.0 |  | Restrict confirmation of sales orders below a configured minimum total amount
[sale_order_note_template](sale_order_note_template/) | 16.0.1.1.0 |  | Add sale orders terms and conditions template that can be used to quickly fullfill sale order terms and conditions
[sale_order_ordered_weight](sale_order_ordered_weight/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add Ordered weights on sale order and sale order line levels
[sale_order_partner_no_autofollow](sale_order_partner_no_autofollow/) | 16.0.1.0.0 |  | Do not add customer as follower in Sales Orders
[sale_order_payment_terms_from_invoice_address](sale_order_payment_terms_from_invoice_address/) | 16.0.1.0.0 |  | Adds a config option to make the payment terms on sale orders computed based on the "invoice address" (`partner_invoice_id`) instead of the "customer" (`partner_id`).
[sale_order_price_recalculation](sale_order_price_recalculation/) | 16.0.1.1.0 |  | Recalculate prices / Reset descriptions on sale order lines
[sale_order_priority](sale_order_priority/) | 16.0.1.0.0 |  | Define priority on sale orders
[sale_order_product_assortment](sale_order_product_assortment/) | 16.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Module that allows to use the assortments on sale orders
[sale_order_product_availability_inline](sale_order_product_availability_inline/) | 16.0.1.0.0 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | Show product availability in sales order line product drop-down.
[sale_order_product_picker](sale_order_product_picker/) | 16.0.1.2.2 |  | Sale Order Product Picker
[sale_order_product_recommendation](sale_order_product_recommendation/) | 16.0.3.0.2 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Recommend products to sell to customer based on history
[sale_order_product_recommendation_elaboration](sale_order_product_recommendation_elaboration/) | 16.0.2.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Include elaborations when generating or accepting sale order product recommendations
[sale_order_product_recommendation_packaging_default](sale_order_product_recommendation_packaging_default/) | 16.0.3.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Quickly add recommended products to sale order by packagings
[sale_order_product_recommendation_quick_add](sale_order_product_recommendation_quick_add/) | 16.0.1.1.0 |  | Add recommended products to sale order in a single click
[sale_order_qty_change_no_recompute](sale_order_qty_change_no_recompute/) | 16.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Prevent recompute if only quantity has changed in sale order line
[sale_order_recurrence](sale_order_recurrence/) | 16.0.1.0.0 |  | Duplication Tools for Sale Orders with a certain recurrence
[sale_order_report_without_price](sale_order_report_without_price/) | 16.0.1.0.0 |  | Allow you to generate quotation and order reports without price.
[sale_order_revision](sale_order_revision/) | 16.0.1.0.2 |  | Keep track of revised quotations
[sale_order_safe_commitment_date](sale_order_safe_commitment_date/) | 16.0.1.3.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Avoid confirming a commitment date previous to the expected date
[sale_order_search_line](sale_order_search_line/) | 16.0.1.0.0 |  | Sale Order Search Line
[sale_order_secondary_unit](sale_order_secondary_unit/) | 16.0.1.0.0 |  | Sale product in a secondary unit
[sale_order_tag](sale_order_tag/) | 16.0.1.0.1 | <a href='https://github.com/patrickrwilson'><img src='https://github.com/patrickrwilson.png' width='32' height='32' style='border-radius:50%;' alt='patrickrwilson'/></a> | Adds Tags to Sales Orders.
[sale_order_type](sale_order_type/) | 16.0.1.1.2 |  | Sale Order Type
[sale_order_warehouse_location](sale_order_warehouse_location/) | 16.0.1.0.0 |  | Set warehouse in sales orders based on delivery country/state.
[sale_order_warn_message](sale_order_warn_message/) | 16.0.1.0.1 |  | Add a popup warning on sale to ensure warning is populated
[sale_packaging_default](sale_packaging_default/) | 16.0.2.2.1 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Simplify using products default packaging for sales
[sale_partner_incoterm](sale_partner_incoterm/) | 16.0.1.0.0 |  | Set the customer preferred incoterm on each sales order
[sale_partner_pricelist](sale_partner_pricelist/) | 16.0.1.0.0 |  | Sale Partner Pricelist
[sale_partner_selectable_option](sale_partner_selectable_option/) | 16.0.1.1.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Sale Partner Selectable Option
[sale_payment_sheet](sale_payment_sheet/) | 16.0.1.1.3 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Allow to create invoice payments to commercial users without accounting permissions
[sale_planner_calendar](sale_planner_calendar/) | 16.0.3.1.0 |  | Sale planner calendar
[sale_price_compliance](sale_price_compliance/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Visual price compliance based on product, category and company thresholds
[sale_pricelist_display_surcharge](sale_pricelist_display_surcharge/) | 16.0.1.0.0 |  | This module shows to the customer the surcharges if wanted.
[sale_pricelist_from_commitment_date](sale_pricelist_from_commitment_date/) | 16.0.1.0.1 |  | Use sale order commitment date to compute line price from pricelist
[sale_pricelist_item_advanced](sale_pricelist_item_advanced/) | 16.0.1.0.0 |  | Pricelist items menu
[sale_pricelist_technical](sale_pricelist_technical/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Prevent some pricelists from being selected on order and customer forms
[sale_pricelist_triple_discount](sale_pricelist_triple_discount/) | 16.0.1.0.0 |  | Sale Pricelist Triple Discount
[sale_procurement_customer](sale_procurement_customer/) | 16.0.1.0.0 |  | Allows to transmit the customer to the procurement group
[sale_procurement_group_by_line](sale_procurement_group_by_line/) | 16.0.1.0.1 |  | Base module for multiple procurement group by Sale order
[sale_product_category_menu](sale_product_category_menu/) | 16.0.1.0.0 |  | Shows 'Product Categories' menu item in Sales
[sale_product_email](sale_product_email/) | 16.0.1.0.0 |  | Send a product-specific email to its buyers
[sale_product_multi_add](sale_product_multi_add/) | 16.0.1.1.0 |  | Sale Product Multi Add
[sale_product_packaging_container_deposit](sale_product_packaging_container_deposit/) | 16.0.1.1.1 |  | Sale Product Packaging Container Deposit
[sale_product_set](sale_product_set/) | 16.0.3.0.1 |  | Sale product set
[sale_quotation_number](sale_quotation_number/) | 16.0.2.0.0 |  | Different sequence for sale quotations
[sale_readonly_security](sale_readonly_security/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Sale Readonly Security
[sale_resource_booking](sale_resource_booking/) | 16.0.1.0.0 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Link resource bookings with sales
[sale_restricted_qty](sale_restricted_qty/) | 16.0.1.0.0 | <a href='https://github.com/ashishhirapara'><img src='https://github.com/ashishhirapara.png' width='32' height='32' style='border-radius:50%;' alt='ashishhirapara'/></a> | Sale order min quantity
[sale_seasonality](sale_seasonality/) | 16.0.1.0.1 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> <a href='https://github.com/kevinkhao'><img src='https://github.com/kevinkhao.png' width='32' height='32' style='border-radius:50%;' alt='kevinkhao'/></a> | Sale Seasonality
[sale_shipping_info_helper](sale_shipping_info_helper/) | 16.0.1.0.0 |  | Add shipping amounts on sale order
[sale_sourced_by_line](sale_sourced_by_line/) | 16.0.1.0.0 |  | Multiple warehouse source locations for Sale order
[sale_start_end_dates](sale_start_end_dates/) | 16.0.1.0.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Adds start date and end date on sale order lines
[sale_stock_cancel_restriction](sale_stock_cancel_restriction/) | 16.0.1.0.0 |  | Sale Stock Cancel Restriction
[sale_stock_delivery_state](sale_stock_delivery_state/) | 16.0.1.0.2 |  | Change the way to compute the delivery state
[sale_stock_expiry_date_on_qty_at_date_widget](sale_stock_expiry_date_on_qty_at_date_widget/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Show next Expiry Date on Qty at Date Widget
[sale_stock_line_sequence](sale_stock_line_sequence/) | 16.0.1.0.0 |  | Glue Module for Sale Order Line Sequence and Stock Picking Line Sequence
[sale_stock_partner_warehouse](sale_stock_partner_warehouse/) | 16.0.1.0.0 |  | Allow to choose by default a warehouse on SO based on a Partner parameter
[sale_stock_picking_blocking](sale_stock_picking_blocking/) | 16.0.1.3.1 |  | Allow you to block the creation of deliveries from a sale order.
[sale_stock_picking_note](sale_stock_picking_note/) | 16.0.1.1.1 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Add picking note in sale and purchase order
[sale_stock_product_recommendation](sale_stock_product_recommendation/) | 16.0.1.0.1 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Display stock info when recommending products to sell
[sale_stock_reservation_issue_on_qty_at_date_widget](sale_stock_reservation_issue_on_qty_at_date_widget/) | 16.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Warn user when a reservation issue will happen when confirming an order
[sale_stock_secondary_unit](sale_stock_secondary_unit/) | 16.0.1.0.0 |  | Get product quantities in a secondary unit
[sale_substate](sale_substate/) | 16.0.1.0.0 |  | Sale Sub State
[sale_tier_validation](sale_tier_validation/) | 16.0.1.1.3 |  | Extends the functionality of Sale Orders to support a tier validation process.
[sale_timesheet_project_manual](sale_timesheet_project_manual/) | 16.0.1.0.0 |  | Allows to create the project/tasks before the sale confirmation
[sale_transaction_form_link](sale_transaction_form_link/) | 16.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Allows to display a link to payment transactions on Sale Order form view.
[sale_triple_discount](sale_triple_discount/) | 16.0.1.0.7 |  | Manage triple discount on sale order lines
[sale_validity_auto_cancel](sale_validity_auto_cancel/) | 16.0.1.0.0 | <a href='https://github.com/JordiMForgeFlow'><img src='https://github.com/JordiMForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiMForgeFlow'/></a> | Automatically cancel quotations after validity period.
[sale_wishlist](sale_wishlist/) | 16.0.1.0.0 |  | Handle sale wishlist for partners
[sales_team_security](sales_team_security/) | 16.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | New group for seeing only sales channel's documents
[sales_team_security_sale](sales_team_security_sale/) | 16.0.1.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Integrates sales_team_security with sale
[sell_only_by_packaging](sell_only_by_packaging/) | 16.0.1.2.0 |  | Manage sale of packaging

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/search-engine&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/search-engine/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/search-engine/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/search-engine/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/search-engine/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/search-engine/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/search-engine)
[![Translation Status](https://translation.odoo-community.org/widgets/search-engine-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/search-engine-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[connector_elasticsearch](connector_elasticsearch/) | 16.0.1.0.0 |  | Connector For Elasticsearch Search Engine
[connector_search_engine](connector_search_engine/) | 16.0.1.1.2 |  | Connector Search Engine
[connector_search_engine_serializer_ir_export](connector_search_engine_serializer_ir_export/) | 16.0.1.0.2 |  | Use Exporter (ir.exports) as serializer for index
[connector_typesense](connector_typesense/) | 16.0.1.0.1 |  | Connector For Typesense Search Engine
[search_engine_image_thumbnail](search_engine_image_thumbnail/) | 16.0.1.0.7 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Generate thumbnails for binded record
[search_engine_serializer_pydantic](search_engine_serializer_pydantic/) | 16.0.1.0.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Defines base class for pydantic baser serializer


Unported addons
---------------
addon | version | maintainers | summary
--- | --- | --- | ---
[connector_algolia](connector_algolia/) | 14.0.2.2.0 (unported) |  | Connector For Algolia Search Engine

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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

# Server Authentication
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-auth&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/server-auth/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/server-auth/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/server-auth/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/server-auth/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/server-auth/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-auth)
[![Translation Status](https://translation.odoo-community.org/widgets/server-auth-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-auth-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Modules for handling various authentication schemes

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[auth_admin_passkey](auth_admin_passkey/) | 16.0.1.0.0 |  | Allows system administrator to authenticate with any account
[auth_api_key](auth_api_key/) | 16.0.1.0.1 |  | Authenticate http requests from an API key
[auth_api_key_group](auth_api_key_group/) | 16.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Allow grouping API keys together. Grouping per se does nothing. This feature is supposed to be used by other modules to limit access to services or records based on groups of keys.
[auth_api_key_server_env](auth_api_key_server_env/) | 16.0.1.0.1 |  | Configure api keys via server env. This can be very useful to avoid mixing your keys between your various environments when restoring databases. All you have to do is to add a new section to your configuration file according to the following convention:
[auth_jwt](auth_jwt/) | 16.0.1.2.0 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | JWT bearer token authentication.
[auth_jwt_demo](auth_jwt_demo/) | 16.0.1.1.1 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Test/demo module for auth_jwt.
[auth_jwt_server_env](auth_jwt_server_env/) | 16.0.1.0.0 |  | This addon adds auth.jwt.validator fields to server env
[auth_ldaps](auth_ldaps/) | 16.0.1.0.0 |  | Allows to use LDAP over SSL authentication
[auth_oauth_autologin](auth_oauth_autologin/) | 16.0.1.0.0 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Automatically redirect to the OAuth provider for login
[auth_oauth_filter_by_domain](auth_oauth_filter_by_domain/) | 16.0.1.0.0 | <a href='https://github.com/natuan9'><img src='https://github.com/natuan9.png' width='32' height='32' style='border-radius:50%;' alt='natuan9'/></a> | Filter OAuth providers by domain
[auth_oauth_multi_token](auth_oauth_multi_token/) | 16.0.1.0.0 |  | Allow multiple connection with the same OAuth account
[auth_oauth_ropc](auth_oauth_ropc/) | 16.0.1.0.0 |  | Allow to login with OAuth Resource Owner Password Credentials Grant
[auth_oidc](auth_oidc/) | 16.0.1.4.0 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Allow users to login through OpenID Connect Provider
[auth_oidc_environment](auth_oidc_environment/) | 16.0.1.0.0 |  | This module allows to use server env for OIDC configuration
[auth_saml](auth_saml/) | 16.0.1.2.1 | <a href='https://github.com/vincent-hatakeyama'><img src='https://github.com/vincent-hatakeyama.png' width='32' height='32' style='border-radius:50%;' alt='vincent-hatakeyama'/></a> | SAML2 Authentication
[auth_session_timeout](auth_session_timeout/) | 16.0.1.0.1 |  | This module disable all inactive sessions since a given delay
[auth_signup_verify_email](auth_signup_verify_email/) | 16.0.1.0.1 |  | Force uninvited users to use a good email for signup
[auth_user_case_insensitive](auth_user_case_insensitive/) | 16.0.1.0.0 |  | Makes the user login field case insensitive
[base_user_show_email](base_user_show_email/) | 16.0.1.0.0 |  | Untangle user login and email
[cross_connect_client](cross_connect_client/) | 16.0.1.1.0 | <a href='https://github.com/paradoxxxzero'><img src='https://github.com/paradoxxxzero.png' width='32' height='32' style='border-radius:50%;' alt='paradoxxxzero'/></a> | Cross Connect Client allows to connect to a Cross Connect Server enabled odoo instance.
[cross_connect_server](cross_connect_server/) | 16.0.1.1.0 | <a href='https://github.com/paradoxxxzero'><img src='https://github.com/paradoxxxzero.png' width='32' height='32' style='border-radius:50%;' alt='paradoxxxzero'/></a> | Cross Connect Server allows Cross Connect Client to connect to it.
[impersonate_login](impersonate_login/) | 16.0.1.0.1 | <a href='https://github.com/Kev-Roche'><img src='https://github.com/Kev-Roche.png' width='32' height='32' style='border-radius:50%;' alt='Kev-Roche'/></a> | tools
[password_security](password_security/) | 16.0.1.0.4 |  | Allow admin to set password security requirements.
[user_log_view](user_log_view/) | 16.0.1.0.0 | <a href='https://github.com/trojikman'><img src='https://github.com/trojikman.png' width='32' height='32' style='border-radius:50%;' alt='trojikman'/></a> | Allow to see user's actions log
[users_ldap_groups](users_ldap_groups/) | 16.0.1.0.1 |  | Adds user accounts to groups based on rules defined by the administrator.
[users_ldap_mail](users_ldap_mail/) | 16.0.1.0.0 | <a href='https://github.com/joao-p-marques'><img src='https://github.com/joao-p-marques.png' width='32' height='32' style='border-radius:50%;' alt='joao-p-marques'/></a> | LDAP mapping for user name and e-mail
[users_ldap_populate](users_ldap_populate/) | 16.0.1.0.2 | <a href='https://github.com/joao-p-marques'><img src='https://github.com/joao-p-marques.png' width='32' height='32' style='border-radius:50%;' alt='joao-p-marques'/></a> | LDAP Populate
[vault](vault/) | 16.0.1.0.3 |  | Password vault integration in Odoo
[vault_share](vault_share/) | 16.0.1.0.1 |  | Implementation of a mechanism to share secrets

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# server-backend
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-backend&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/server-backend/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/server-backend/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/server-backend/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/server-backend/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/server-backend/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-backend)
[![Translation Status](https://translation.odoo-community.org/widgets/server-backend-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-backend-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Mainly base modules used by others

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_external_dbsource](base_external_dbsource/) | 16.0.1.0.1 |  | External Database Sources
[base_external_dbsource_mssql](base_external_dbsource_mssql/) | 16.0.1.1.0 | <a href='https://github.com/anddago78'><img src='https://github.com/anddago78.png' width='32' height='32' style='border-radius:50%;' alt='anddago78'/></a> | External Database Source - MSSQL
[base_external_dbsource_mysql](base_external_dbsource_mysql/) | 16.0.1.0.0 |  | External Database Source - MySQL
[base_external_dbsource_sqlite](base_external_dbsource_sqlite/) | 16.0.1.0.2 | <a href='https://github.com/anddago78'><img src='https://github.com/anddago78.png' width='32' height='32' style='border-radius:50%;' alt='anddago78'/></a> | External Database Source - SQLite
[base_external_system](base_external_system/) | 16.0.1.0.0 |  | Data models allowing for connection to external systems.
[base_external_system_odoorpc](base_external_system_odoorpc/) | 16.0.1.0.0 |  | Connect to a remote Odoo instance via the odoorpc library.
[base_global_discount](base_global_discount/) | 16.0.1.1.0 |  | Base Global Discount
[base_group_backend](base_group_backend/) | 16.0.1.2.0 | <a href='https://github.com/FranzPoize'><img src='https://github.com/FranzPoize.png' width='32' height='32' style='border-radius:50%;' alt='FranzPoize'/></a> <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Group backend
[base_import_match](base_import_match/) | 16.0.1.1.0 |  | Try to avoid duplicates before importing
[base_portal_type](base_portal_type/) | 16.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Base module to allow different types of portals
[base_user_effective_permissions](base_user_effective_permissions/) | 16.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Inspect effective permissions applying to a user
[base_user_role](base_user_role/) | 16.0.1.4.5 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> <a href='https://github.com/jcdrubay'><img src='https://github.com/jcdrubay.png' width='32' height='32' style='border-radius:50%;' alt='jcdrubay'/></a> <a href='https://github.com/novawish'><img src='https://github.com/novawish.png' width='32' height='32' style='border-radius:50%;' alt='novawish'/></a> | User roles
[base_user_role_company](base_user_role_company/) | 16.0.1.2.2 |  | User roles by company
[base_user_role_history](base_user_role_history/) | 16.0.1.0.0 | <a href='https://github.com/ThomasBinsfeld'><img src='https://github.com/ThomasBinsfeld.png' width='32' height='32' style='border-radius:50%;' alt='ThomasBinsfeld'/></a> | This module allows to track the changes on users roles.
[server_action_navigate](server_action_navigate/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/ashishhirpara'><img src='https://github.com/ashishhirpara.png' width='32' height='32' style='border-radius:50%;' alt='ashishhirpara'/></a> | Navigate between any items of any Odoo Models
[server_action_sort](server_action_sort/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Sort any lines of any models by any criterias

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-brand&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/server-brand/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/server-brand/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/server-brand/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/server-brand/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/server-brand/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-brand)
[![Translation Status](https://translation.odoo-community.org/widgets/server-brand-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-brand-16-0/?utm_source=widget)

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
[disable_odoo_online](disable_odoo_online/) | 16.0.1.0.0 |  | Remove odoo.com Bindings
[hr_expense_remove_mobile_link](hr_expense_remove_mobile_link/) | 16.0.1.0.0 |  | Remove Odoo Enterprise mobile app download links
[portal_odoo_debranding](portal_odoo_debranding/) | 16.0.1.0.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Remove Odoo Branding from Website
[remove_odoo_enterprise](remove_odoo_enterprise/) | 16.0.2.0.4 |  | Remove enterprise modules and setting items

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# server-env
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-env&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/server-env/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/server-env/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/server-env/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/server-env/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/server-env/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-env)
[![Translation Status](https://translation.odoo-community.org/widgets/server-env-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-env-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[data_encryption](data_encryption/) | 16.0.1.0.1 |  | Store accounts and credentials encrypted by environment
[mail_environment](mail_environment/) | 16.0.1.0.3 |  | Configure mail servers with server_environment_files
[mail_environment_google_gmail](mail_environment_google_gmail/) | 16.0.1.1.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Configure Gmail mail servers with server_environment_files
[pos_environment](pos_environment/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Custom messages on the bill depending on the environment
[server_environment](server_environment/) | 16.0.1.1.3 |  | move some configurations out of the database
[server_environment_data_encryption](server_environment_data_encryption/) | 16.0.1.0.0 |  | Server Environment Data Encryption
[server_environment_ir_config_parameter](server_environment_ir_config_parameter/) | 16.0.1.1.0 |  | Override System Parameters from server environment file

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# server-tools
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-tools&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/server-tools/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/server-tools/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/server-tools/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/server-tools/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/server-tools/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-tools)
[![Translation Status](https://translation.odoo-community.org/widgets/server-tools-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-tools-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[attachment_delete_restrict](attachment_delete_restrict/) | 16.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/Kev-Roche'><img src='https://github.com/Kev-Roche.png' width='32' height='32' style='border-radius:50%;' alt='Kev-Roche'/></a> | Restrict Deletion of Attachments
[attachment_logging](attachment_logging/) | 16.0.1.0.0 |  | Show attachment information in chatter
[attachment_queue](attachment_queue/) | 16.0.1.2.1 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> | Base module adding the concept of queue for processing files
[attachment_synchronize](attachment_synchronize/) | 16.0.1.0.2 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> <a href='https://github.com/GSLabIt'><img src='https://github.com/GSLabIt.png' width='32' height='32' style='border-radius:50%;' alt='GSLabIt'/></a> <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Attachment Synchronize
[attachment_unindex_content](attachment_unindex_content/) | 16.0.1.0.0 | <a href='https://github.com/moylop260'><img src='https://github.com/moylop260.png' width='32' height='32' style='border-radius:50%;' alt='moylop260'/></a> <a href='https://github.com/ebirbe'><img src='https://github.com/ebirbe.png' width='32' height='32' style='border-radius:50%;' alt='ebirbe'/></a> <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> | Disable indexing of attachments
[auditlog](auditlog/) | 16.0.3.0.5 |  | Audit Log
[auto_backup](auto_backup/) | 16.0.1.0.3 |  | Backups database
[autovacuum_message_attachment](autovacuum_message_attachment/) | 16.0.1.0.1 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Automatically delete old mail messages and attachments
[base_changeset](base_changeset/) | 16.0.1.0.0 | <a href='https://github.com/astirpe'><img src='https://github.com/astirpe.png' width='32' height='32' style='border-radius:50%;' alt='astirpe'/></a> | Track record changesets
[base_conditional_image](base_conditional_image/) | 16.0.1.0.0 |  | This module extends the functionality to support conditional images
[base_cron_exclusion](base_cron_exclusion/) | 16.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | Allow you to select scheduled actions that should not run simultaneously.
[base_domain_inverse_function](base_domain_inverse_function/) | 16.0.1.0.1 | <a href='https://github.com/grindtildeath'><img src='https://github.com/grindtildeath.png' width='32' height='32' style='border-radius:50%;' alt='grindtildeath'/></a> | Provide function to inverse domain into parts
[base_exception](base_exception/) | 16.0.2.1.0 | <a href='https://github.com/hparfr'><img src='https://github.com/hparfr.png' width='32' height='32' style='border-radius:50%;' alt='hparfr'/></a> <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> | This module provide an abstract model to manage customizable exceptions to be applied on different models (sale order, invoice, ...)
[base_fontawesome](base_fontawesome/) | 16.0.6.6.1 |  | Up to date Fontawesome resources.
[base_force_record_noupdate](base_force_record_noupdate/) | 16.0.1.0.0 |  | Manually force noupdate=True on models
[base_import_default_enable_tracking](base_import_default_enable_tracking/) | 16.0.1.0.0 | <a href='https://github.com/benwillig'><img src='https://github.com/benwillig.png' width='32' height='32' style='border-radius:50%;' alt='benwillig'/></a> | This modules simply enables history tracking when doing an import.
[base_import_odoo](base_import_odoo/) | 16.0.1.0.1 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> <a href='https://github.com/thomaspaulb'><img src='https://github.com/thomaspaulb.png' width='32' height='32' style='border-radius:50%;' alt='thomaspaulb'/></a> | Import records from another Odoo instance
[base_kanban_stage](base_kanban_stage/) | 16.0.1.0.0 |  | Provides stage model and abstract logic for inheritance
[base_m2m_custom_field](base_m2m_custom_field/) | 16.0.1.0.0 |  | Customizations of Many2many
[base_model_restrict_update](base_model_restrict_update/) | 16.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Update Restrict Model
[base_multi_image](base_multi_image/) | 16.0.1.0.1 |  | Allow multiple images for database objects
[base_name_search_improved](base_name_search_improved/) | 16.0.1.0.2 |  | Friendlier search when typing in relation fields
[base_partition](base_partition/) | 16.0.1.0.0 |  | Base module that provide the partition method on all models
[base_remote](base_remote/) | 16.0.1.0.3 |  | Remote Base
[base_report_auto_create_qweb](base_report_auto_create_qweb/) | 16.0.1.0.0 |  | Report qweb auto generation
[base_search_fuzzy](base_search_fuzzy/) | 16.0.1.0.0 |  | Fuzzy search with the PostgreSQL trigram extension
[base_sequence_default](base_sequence_default/) | 16.0.1.0.2 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Use sequences for default values of fields when creating a new record
[base_sequence_option](base_sequence_option/) | 16.0.1.0.1 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Alternative sequence options for specific models
[base_sparse_field_list_support](base_sparse_field_list_support/) | 16.0.1.0.0 |  | add list support to convert_to_cache()
[base_technical_user](base_technical_user/) | 16.0.1.0.1 |  | Add a technical user parameter on the company
[base_time_window](base_time_window/) | 16.0.1.1.0 |  | Base model to handle time windows
[base_view_inheritance_extension](base_view_inheritance_extension/) | 16.0.1.2.2 |  | Adds more operators for view inheritance
[bus_alt_connection](bus_alt_connection/) | 16.0.1.0.0 |  | Needed when using PgBouncer as a connection pooler
[cron_daylight_saving_time_resistant](cron_daylight_saving_time_resistant/) | 16.0.1.0.1 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Run cron on fixed hours
[database_cleanup](database_cleanup/) | 16.0.2.0.0 |  | Database cleanup
[datetime_formatter](datetime_formatter/) | 16.0.1.0.0 |  | Helper functions to give correct format to date[time] fields
[dbfilter_from_header](dbfilter_from_header/) | 16.0.1.0.1 |  | Filter databases with HTTP headers
[excel_import_export](excel_import_export/) | 16.0.1.3.2 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Base module for developing Excel import/export/report
[excel_import_export_demo](excel_import_export_demo/) | 16.0.1.1.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Excel Import/Export/Report Demo
[excel_import_export_unidecode](excel_import_export_unidecode/) | 16.0.1.0.1 |  | Add unidecode option to excel import/export/report
[fetchmail_attach_from_folder](fetchmail_attach_from_folder/) | 16.0.2.0.0 | <a href='https://github.com/NL66278'><img src='https://github.com/NL66278.png' width='32' height='32' style='border-radius:50%;' alt='NL66278'/></a> | Attach mails in an IMAP folder to existing objects
[fetchmail_notify_error_to_sender](fetchmail_notify_error_to_sender/) | 16.0.1.0.0 |  | If fetching mails gives error, send an email to sender
[fetchmail_notify_error_to_sender_test](fetchmail_notify_error_to_sender_test/) | 16.0.1.0.0 |  | Test for Fetchmail Notify Error to Sender
[field_vector](field_vector/) | 16.0.1.0.1 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | New specialized field to store vector data
[html_image_url_extractor](html_image_url_extractor/) | 16.0.1.0.0 |  | Extract images found in any HTML field
[html_text](html_text/) | 16.0.1.0.1 |  | Generate excerpts from any HTML field
[iap_alternative_provider](iap_alternative_provider/) | 16.0.1.0.0 | <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> | Base module for providing alternative provider for iap apps
[jsonifier](jsonifier/) | 16.0.0.1.0 |  | JSON-ify data for all models
[letsencrypt](letsencrypt/) | 16.0.1.1.1 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Request SSL certificates from letsencrypt.org
[mail_cleanup](mail_cleanup/) | 16.0.1.0.0 |  | Mark as read or delete mails after a set time
[mail_template_attachment_i18n](mail_template_attachment_i18n/) | 16.0.1.0.0 |  | Set language specific attachments on mail templates.
[module_analysis](module_analysis/) | 16.0.1.0.5 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add analysis tools regarding installed modules to know which installed modules comes from Odoo Core, OCA, or are custom modules
[module_auto_update](module_auto_update/) | 16.0.1.1.0 |  | Automatically update Odoo modules
[module_change_auto_install](module_change_auto_install/) | 16.0.1.0.2 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Customize auto installables modules by configuration
[nsca_client](nsca_client/) | 16.0.1.0.2 |  | Send passive alerts to monitor your Odoo application.
[odoo_test_xmlrunner](odoo_test_xmlrunner/) | 16.0.1.0.1 |  | This module override Odoo testing method to run them with xmlrunner tool.
[onchange_helper](onchange_helper/) | 16.0.1.0.1 |  | Technical module that ease execution of onchange in Python code
[postgres_vacuum](postgres_vacuum/) | 16.0.1.0.0 |  | Vacuum or analyze Odoo's database tables
[rpc_helper](rpc_helper/) | 16.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Helpers for disabling RPC calls
[scheduler_error_mailer](scheduler_error_mailer/) | 16.0.1.0.0 |  | Scheduler Error Mailer
[sentry](sentry/) | 16.0.3.0.3 | <a href='https://github.com/barsi'><img src='https://github.com/barsi.png' width='32' height='32' style='border-radius:50%;' alt='barsi'/></a> <a href='https://github.com/naglis'><img src='https://github.com/naglis.png' width='32' height='32' style='border-radius:50%;' alt='naglis'/></a> <a href='https://github.com/versada'><img src='https://github.com/versada.png' width='32' height='32' style='border-radius:50%;' alt='versada'/></a> <a href='https://github.com/moylop260'><img src='https://github.com/moylop260.png' width='32' height='32' style='border-radius:50%;' alt='moylop260'/></a> <a href='https://github.com/fernandahf'><img src='https://github.com/fernandahf.png' width='32' height='32' style='border-radius:50%;' alt='fernandahf'/></a> | Report Odoo errors to Sentry
[sequence_python](sequence_python/) | 16.0.1.0.0 |  | Calculate a sequence number from a Python expression
[server_action_logging](server_action_logging/) | 16.0.1.0.0 |  | Module that provides a logging mechanism for server actions
[session_db](session_db/) | 16.0.1.0.7 | <a href='https://github.com/sbidoul'><img src='https://github.com/sbidoul.png' width='32' height='32' style='border-radius:50%;' alt='sbidoul'/></a> | Store sessions in DB
[test_auditlog](test_auditlog/) | 16.0.1.0.2 |  | Additional unit tests for Audit Log based on accounting models
[tracking_manager](tracking_manager/) | 16.0.1.1.10 | <a href='https://github.com/Kev-Roche'><img src='https://github.com/Kev-Roche.png' width='32' height='32' style='border-radius:50%;' alt='Kev-Roche'/></a> <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> | This module tracks all fields of a model, including one2many and many2many ones.
[upgrade_analysis](upgrade_analysis/) | 16.0.1.2.3 | <a href='https://github.com/StefanRijnhart'><img src='https://github.com/StefanRijnhart.png' width='32' height='32' style='border-radius:50%;' alt='StefanRijnhart'/></a> <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Performs a difference analysis between modules installed on two different Odoo instances
[url_attachment_search_fuzzy](url_attachment_search_fuzzy/) | 16.0.1.0.0 | <a href='https://github.com/mariadforgelow'><img src='https://github.com/mariadforgelow.png' width='32' height='32' style='border-radius:50%;' alt='mariadforgelow'/></a> | Fuzzy Search of URL in Attachments

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-ux&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/server-ux/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/server-ux/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/server-ux/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/server-ux/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/server-ux/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-ux)
[![Translation Status](https://translation.odoo-community.org/widgets/server-ux-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-ux-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# server-ux

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[announcement](announcement/) | 16.0.1.1.0 |  | Notify internal users about relevant organization stuff
[announcement_dialog_size](announcement_dialog_size/) | 16.0.1.0.0 |  | Allow set announcement dialogs fullsized by default
[barcode_action](barcode_action/) | 16.0.1.0.1 |  | Allows to use barcodes as a launcher
[base_archive_security](base_archive_security/) | 16.0.1.0.1 | <a href='https://github.com/imlopes'><img src='https://github.com/imlopes.png' width='32' height='32' style='border-radius:50%;' alt='imlopes'/></a> <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Controls who can archive or unarchive records
[base_binary_url_import](base_binary_url_import/) | 16.0.1.0.0 |  | Wizard to import binary files from URL on existing records
[base_cancel_confirm](base_cancel_confirm/) | 16.0.1.0.2 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Base Cancel Confirm
[base_custom_filter](base_custom_filter/) | 16.0.1.1.1 | <a href='https://github.com/AshishHirapara'><img src='https://github.com/AshishHirapara.png' width='32' height='32' style='border-radius:50%;' alt='AshishHirapara'/></a> <a href='https://github.com/ForgeFlow'><img src='https://github.com/ForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ForgeFlow'/></a> | Add custom filters in standard filters and group by dropdowns
[base_export_manager](base_export_manager/) | 16.0.1.0.3 |  | Manage model export profiles
[base_import_security_group](base_import_security_group/) | 16.0.1.0.0 |  | Group-based permissions for importing CSV files
[base_menu_visibility_restriction](base_menu_visibility_restriction/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Restrict (with groups) menu visibilty
[base_optional_quick_create](base_optional_quick_create/) | 16.0.1.0.0 |  | Avoid "quick create" on m2o fields, on a "by model" basis
[base_revision](base_revision/) | 16.0.1.0.2 |  | Keep track of revised document
[base_rule_visibility_restriction](base_rule_visibility_restriction/) | 16.0.1.0.0 | <a href='https://github.com/GuillemCForgeFlow'><img src='https://github.com/GuillemCForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='GuillemCForgeFlow'/></a> | Exclude Record Rules for certain groups
[base_search_custom_field_filter](base_search_custom_field_filter/) | 16.0.1.0.1 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Add custom filters for fields via UI
[base_substate](base_substate/) | 16.0.1.0.1 |  | Base Sub State
[base_technical_features](base_technical_features/) | 16.0.1.0.1 |  | Access to technical features without activating debug mode
[base_tier_validation](base_tier_validation/) | 16.0.4.0.2 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Implement a validation process based on tiers.
[base_tier_validation_board](base_tier_validation_board/) | 16.0.1.0.0 | <a href='https://github.com/JasminSForgeFlow'><img src='https://github.com/JasminSForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JasminSForgeFlow'/></a> | Add Tier Review Boards
[base_tier_validation_correction](base_tier_validation_correction/) | 16.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Correct tier.review data after it has been created.
[base_tier_validation_definition_server_action](base_tier_validation_definition_server_action/) | 16.0.1.0.0 |  | Server action for Base tier validation
[base_tier_validation_formula](base_tier_validation_formula/) | 16.0.1.0.2 |  | Formulas for Base tier validation
[base_tier_validation_forward](base_tier_validation_forward/) | 16.0.2.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Forward option for base tiers
[base_tier_validation_report](base_tier_validation_report/) | 16.0.1.0.1 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Reports related to tier validation
[base_tier_validation_server_action](base_tier_validation_server_action/) | 16.0.1.0.0 | <a href='https://github.com/kittiu'><img src='https://github.com/kittiu.png' width='32' height='32' style='border-radius:50%;' alt='kittiu'/></a> | Add option to call server action when a tier is validated
[base_tier_validation_waiting](base_tier_validation_waiting/) | 16.0.1.0.1 |  | Base Tier Validation Extension to add waiting status
[base_user_chatter](base_user_chatter/) | 16.0.1.0.0 |  | User Chatter
[base_user_locale](base_user_locale/) | 16.0.1.1.1 |  | User Locale Settings
[confirmation_wizard](confirmation_wizard/) | 16.0.1.0.0 |  | This module adds a confirmation wizard that can be called with code. It does nothing by itself.
[date_range](date_range/) | 16.0.1.0.9 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Manage all kind of date range
[date_range_account](date_range_account/) | 16.0.1.0.1 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Add Date Range menu entry in Invoicing app
[developer_menu](developer_menu/) | 16.0.1.0.0 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Menu Shortcut for developer usage
[document_quick_access](document_quick_access/) | 16.0.1.0.1 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Document quick access
[document_quick_access_folder_auto_classification](document_quick_access_folder_auto_classification/) | 16.0.1.0.2 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Auto classification of Documents after reading a QR
[filter_multi_user](filter_multi_user/) | 16.0.1.0.1 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Allows to share user-defined filters filters among several users.
[mail_message_destiny_link_template](mail_message_destiny_link_template/) | 16.0.1.0.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Mail template to show destiny records in chatter.
[mail_suggested_recipient_unchecked](mail_suggested_recipient_unchecked/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Mail suggested recipient unchecked
[misc_settings](misc_settings/) | 16.0.1.0.0 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Miscellaneous settings to be an anchor for your custom settings
[multi_step_wizard](multi_step_wizard/) | 16.0.1.0.0 |  | Multi-Steps Wizards
[multisearch_field](multisearch_field/) | 16.0.1.0.1 |  | add modification on search to search multi_value with separator
[sequence_check_digit](sequence_check_digit/) | 16.0.1.0.1 |  | Adds a check digit on sequences
[sequence_reset_period](sequence_reset_period/) | 16.0.1.0.0 |  | Auto-generate yearly/monthly/weekly/daily sequence period ranges
[server_action_mass_edit](server_action_mass_edit/) | 16.0.2.1.1 |  | Mass Editing
[template_content_swapper](template_content_swapper/) | 16.0.1.1.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/AungKoKoLin1997'><img src='https://github.com/AungKoKoLin1997.png' width='32' height='32' style='border-radius:50%;' alt='AungKoKoLin1997'/></a> | Template Content Swapper
[test_base_binary_url_import](test_base_binary_url_import/) | 16.0.1.0.1 |  | Unittests for Base Binary URL Import module
[user_all_groups](user_all_groups/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Automatically add admin user to all the groups

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# Odoo modules for signing purposes
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sign&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/sign/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/sign/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/sign/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/sign/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/sign/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/sign)
[![Translation Status](https://translation.odoo-community.org/widgets/sign-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sign-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Here are OCA modules that have digital signature functionalities.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[maintenance_sign_oca](maintenance_sign_oca/) | 16.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Maintenance Sign Oca
[project_task_sign_oca](project_task_sign_oca/) | 16.0.1.0.1 |  | Project Task Sign Oca
[sign_oca](sign_oca/) | 16.0.5.2.1 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Allow to sign documents inside Odoo CE

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# social
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/social&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/social/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/social/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/social/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/social/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/social/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/social)
[![Translation Status](https://translation.odoo-community.org/widgets/social-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/social-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

{'TODO': 'add repo description.'}Better integration of Odoo with mail and social media

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_search_mail_content](base_search_mail_content/) | 16.0.1.0.5 |  | Base Search Mail Content
[base_user_signature](base_user_signature/) | 16.0.1.0.0 | <a href='https://github.com/imlopes'><img src='https://github.com/imlopes.png' width='32' height='32' style='border-radius:50%;' alt='imlopes'/></a> | Base User Signature
[email_template_qweb](email_template_qweb/) | 16.0.1.0.1 |  | Use the QWeb templating mechanism for emails
[fetchmail_thread_default](fetchmail_thread_default/) | 16.0.1.1.0 |  | Post unkonwn messages to an existing thread
[mail_activity_board](mail_activity_board/) | 16.0.1.2.0 |  | Add Activity Boards
[mail_activity_done](mail_activity_done/) | 16.0.1.4.0 |  | Mail Activity Done
[mail_activity_filter_internal_user](mail_activity_filter_internal_user/) | 16.0.1.0.0 |  | Filter on internal user by default when assigning someone to an activity.
[mail_activity_meeting_reminder](mail_activity_meeting_reminder/) | 16.0.1.0.0 |  | Allow to enforce reminders on meeting activity types
[mail_activity_partner](mail_activity_partner/) | 16.0.1.0.0 |  | Add Partner to Activities
[mail_activity_plan](mail_activity_plan/) | 16.0.1.0.1 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Mail activity plan
[mail_activity_reminder](mail_activity_reminder/) | 16.0.1.0.1 |  | Reminder notifications about planned activities
[mail_activity_reply_creator](mail_activity_reply_creator/) | 16.0.1.0.0 |  | Assign new to its creator
[mail_activity_team](mail_activity_team/) | 16.0.1.1.0 |  | Add Teams to Activities
[mail_activity_unlink_log](mail_activity_unlink_log/) | 16.0.1.0.0 |  | Leave a message when an activity is unlinked
[mail_attach_existing_attachment](mail_attach_existing_attachment/) | 16.0.1.1.0 |  | Adding attachment on the object by sending this one
[mail_attach_existing_attachment_account](mail_attach_existing_attachment_account/) | 16.0.1.0.1 |  | Module to use attach existing attachment for account module
[mail_autogenerated_header](mail_autogenerated_header/) | 16.0.1.0.1 |  | Add headers to Odoo's mails indicating they are autogenerated
[mail_autosubscribe](mail_autosubscribe/) | 16.0.1.0.1 |  | Automatically subscribe partners to its company's business documents
[mail_composer_cc_bcc](mail_composer_cc_bcc/) | 16.0.2.0.6 | <a href='https://github.com/trisdoan'><img src='https://github.com/trisdoan.png' width='32' height='32' style='border-radius:50%;' alt='trisdoan'/></a> | This module enables sending mail to CC and BCC partners in mail composer form.
[mail_composer_cc_bcc_account](mail_composer_cc_bcc_account/) | 16.0.2.0.0 | <a href='https://github.com/hailangvn2023'><img src='https://github.com/hailangvn2023.png' width='32' height='32' style='border-radius:50%;' alt='hailangvn2023'/></a> | This module enables sending mail to CC and BCC partners for invoices.
[mail_debrand](mail_debrand/) | 16.0.1.0.2 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> <a href='https://github.com/joao-p-marques'><img src='https://github.com/joao-p-marques.png' width='32' height='32' style='border-radius:50%;' alt='joao-p-marques'/></a> | Remove Odoo branding in sent emails Removes anchor <a href odoo.com togheder with it's parent ( for powerd by) form all the templates removes any 'odoo' that are in tempalte texts > 20characters
[mail_disable_follower_notification](mail_disable_follower_notification/) | 16.0.1.0.0 |  | Don't send emails by default when adding followers to records
[mail_discuss_security](mail_discuss_security/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add a group to display 'Discuss' Application menu entry
[mail_drop_target](mail_drop_target/) | 16.0.1.1.0 |  | Attach emails to Odoo by dragging them from your desktop
[mail_edit](mail_edit/) | 16.0.1.0.0 |  | Edit, Delete or Move messages to any model
[mail_gateway](mail_gateway/) | 16.0.1.3.4 |  | Set a gateway
[mail_gateway_telegram](mail_gateway_telegram/) | 16.0.1.1.0 |  | Set a gateway for telegram
[mail_gateway_whatsapp](mail_gateway_whatsapp/) | 16.0.1.1.3 |  | Set a gateway for whatsapp
[mail_improved_tracking_value](mail_improved_tracking_value/) | 16.0.1.0.0 |  | Improves tracking changed values for certain type of fields.Adds a user-friendly view to consult them.
[mail_inline_css](mail_inline_css/) | 16.0.0.1.0 |  | Convert style tags in inline style in your mails
[mail_layout_force](mail_layout_force/) | 16.0.2.0.0 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Force a mail layout on selected email templates
[mail_layout_preview](mail_layout_preview/) | 16.0.1.0.0 |  | Preview email templates in the browser
[mail_message_search](mail_message_search/) | 16.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Mail Message Search
[mail_notification_custom_subject](mail_notification_custom_subject/) | 16.0.1.0.0 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Apply a custom subject to mail notifications
[mail_optional_autofollow](mail_optional_autofollow/) | 16.0.1.0.0 |  | Choose if you want to automatically add new recipients as followers on mail.compose.message
[mail_optional_follower_notification](mail_optional_follower_notification/) | 16.0.1.1.0 |  | Choose to notify followers on mail.compose.message
[mail_outbound_static](mail_outbound_static/) | 16.0.1.0.2 |  | Allows you to configure the from header for a mail server.
[mail_partner_opt_out](mail_partner_opt_out/) | 16.0.1.1.0 |  | Add the partner's email to the blackmailed list. Allow also removing or adding partners emails to the backlist in mass.
[mail_post_defer](mail_post_defer/) | 16.0.1.1.3 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Faster and cancellable outgoing messages
[mail_quoted_reply](mail_quoted_reply/) | 16.0.1.0.3 |  | Make a reply using a message
[mail_restrict_follower_selection](mail_restrict_follower_selection/) | 16.0.1.0.0 |  | Define a domain from which followers can be selected
[mail_restrict_send_button](mail_restrict_send_button/) | 16.0.1.0.1 |  | Security for Send Message Button on Chatter Area
[mail_send_confirmation](mail_send_confirmation/) | 16.0.1.0.0 |  | Mail Send Confirmation
[mail_show_follower](mail_show_follower/) | 16.0.1.2.1 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Show CC document followers in mails.
[mail_template_multi_attachment](mail_template_multi_attachment/) | 16.0.1.0.0 |  | Module who allows to generate multi attachments on an email template.
[mail_template_substitute](mail_template_substitute/) | 16.0.1.0.1 |  | This module allows to create substitution rules for mail templates.
[mail_tracking](mail_tracking/) | 16.0.1.0.8 |  | Email tracking system for all mails sent
[mail_tracking_mailgun](mail_tracking_mailgun/) | 16.0.1.0.1 |  | Mail tracking and Mailgun webhooks integration
[mail_tracking_mass_mailing](mail_tracking_mass_mailing/) | 16.0.1.0.0 |  | Improve mass mailing email tracking
[mass_mailing_contact_active](mass_mailing_contact_active/) | 16.0.1.0.0 |  | Adds active feature on mailing list contact and subscriptions
[mass_mailing_custom_unsubscribe](mass_mailing_custom_unsubscribe/) | 16.0.1.1.0 |  | Know and track (un)subscription reasons, GDPR compliant
[mass_mailing_disable_tracking](mass_mailing_disable_tracking/) | 16.0.1.0.0 | <a href='https://github.com/huguesdk'><img src='https://github.com/huguesdk.png' width='32' height='32' style='border-radius:50%;' alt='huguesdk'/></a> | Allow to disable open and link click tracking in mass mailing messages
[mass_mailing_event_registration_exclude](mass_mailing_event_registration_exclude/) | 16.0.1.0.0 |  | Link mass mailing with event for excluding recipients
[mass_mailing_list_dynamic](mass_mailing_list_dynamic/) | 16.0.2.1.0 |  | Mass mailing lists that get autopopulated
[mass_mailing_list_prune_blacklisted](mass_mailing_list_prune_blacklisted/) | 16.0.1.0.0 | <a href='https://github.com/SirPyTech'><img src='https://github.com/SirPyTech.png' width='32' height='32' style='border-radius:50%;' alt='SirPyTech'/></a> | Allow to remove blacklisted emails from mailing lists.
[mass_mailing_partner](mass_mailing_partner/) | 16.0.2.0.2 |  | Link partners with mass-mailing
[mass_mailing_resend](mass_mailing_resend/) | 16.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Resend mass mailings
[mass_mailing_unique](mass_mailing_unique/) | 16.0.1.1.0 |  | Avoids duplicate mailing lists and contacts
[outgoing_email_by_model](outgoing_email_by_model/) | 16.0.1.0.0 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Outgoing Email by Model
[res_company_gitlab_link](res_company_gitlab_link/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add gitlab url at company model
[res_company_mastodon_link](res_company_mastodon_link/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add mastodon url at company model

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/spreadsheet&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/spreadsheet/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/spreadsheet/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/spreadsheet/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/spreadsheet/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/spreadsheet/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/spreadsheet)
[![Translation Status](https://translation.odoo-community.org/widgets/spreadsheet-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/spreadsheet-16-0/?utm_source=widget)

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
[spreadsheet_dashboard_oca](spreadsheet_dashboard_oca/) | 16.0.1.3.0 |  | Use OCA Spreadsheets on dashboards configuration
[spreadsheet_oca](spreadsheet_oca/) | 16.0.1.9.2 |  | Allow to edit spreadsheets

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-availability&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-availability/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-availability/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/stock-logistics-availability/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-availability/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-availability/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-availability)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-availability-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-availability-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Stock Availability

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
[sale_stock_available_info_popup](sale_stock_available_info_popup/) | 16.0.1.0.0 |  | Adds an 'Available to promise' quantity to the popover shown in sale order line that display stock info of the product
[stock_available](stock_available/) | 16.0.1.1.0 |  | Stock available to promise
[stock_available_base_exclude_location](stock_available_base_exclude_location/) | 16.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Base module to exclude locations for product available quantities
[stock_available_exclude_location](stock_available_exclude_location/) | 16.0.1.0.0 |  | Exclude locations for product available quantities
[stock_available_immediately](stock_available_immediately/) | 16.0.1.0.1 |  | Ignore planned receptions in quantity available to promise
[stock_available_immediately_exclude_location](stock_available_immediately_exclude_location/) | 16.0.1.1.1 |  | Exclude locations from immediately usable quantity
[stock_available_location_get_domain](stock_available_location_get_domain/) | 16.0.1.0.0 |  | This is a technical helper module in order to reuse the standard _get_domain_locations() function for locations and not quants
[stock_available_mrp](stock_available_mrp/) | 16.0.1.1.0 |  | Consider the production potential is available to promise
[stock_available_unreserved](stock_available_unreserved/) | 16.0.1.0.1 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Quantity of stock available for immediate use
[stock_free_quantity](stock_free_quantity/) | 16.0.1.0.0 |  | Stock Free Quantity
[stock_quant_available_quantity](stock_quant_available_quantity/) | 16.0.1.0.0 | <a href='https://github.com/tisho99'><img src='https://github.com/tisho99.png' width='32' height='32' style='border-radius:50%;' alt='tisho99'/></a> | Shows Available Quantity in the stock quant views

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# stock-logistics-barcode
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-barcode&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-barcode/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-barcode/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/stock-logistics-barcode/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-barcode/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-barcode/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-barcode)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-barcode-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-barcode-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[barcodes_generator_abstract](barcodes_generator_abstract/) | 16.0.3.1.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Generate Barcodes for Any Models
[barcodes_generator_location](barcodes_generator_location/) | 16.0.1.0.0 |  | Generate Barcodes for Stock Locations
[barcodes_generator_package](barcodes_generator_package/) | 16.0.1.1.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Generate Barcodes for Product Packaging
[barcodes_generator_product](barcodes_generator_product/) | 16.0.2.1.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Generate Barcodes for Products (Templates and Variants)
[product_barcode_constraint_per_company](product_barcode_constraint_per_company/) | 16.0.1.0.2 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Change the product barcode constraint, allowing the same barcode for differents companies
[product_multi_barcode](product_multi_barcode/) | 16.0.1.1.0 |  | Multiple barcodes on products
[product_multi_barcode_constraint_per_company](product_multi_barcode_constraint_per_company/) | 16.0.1.0.1 |  | Glue module for product_multi_barcode andproduct_barcode_constraint_per_company
[product_multi_barcode_stock_menu](product_multi_barcode_stock_menu/) | 16.0.1.0.0 |  | Multiple barcodes menu
[product_packaging_multi_barcode](product_packaging_multi_barcode/) | 16.0.1.3.0 |  | Multiple barcodes on product packagings
[stock_barcodes](stock_barcodes/) | 16.0.2.2.4 |  | It provides read barcode on stock operations.
[stock_barcodes_picking_batch](stock_barcodes_picking_batch/) | 16.0.2.0.0 |  | It provides read barcodes on stock operations from batch pickings.
[stock_picking_product_barcode_report](stock_picking_product_barcode_report/) | 16.0.1.0.2 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | It provides a wizard to select how many barcodes print.
[stock_picking_product_barcode_report_secondary_unit](stock_picking_product_barcode_report_secondary_unit/) | 16.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Set by default the maximum quantity of labels to print.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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

# Stock Logistics Orderpoint
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-orderpoint&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-orderpoint/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-orderpoint/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/stock-logistics-orderpoint/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-orderpoint/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-orderpoint/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-orderpoint)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-orderpoint-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-orderpoint-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

This repository contains modules to extend reordering rules (available on warehouses locations) functionalities.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[sale_stock_orderpoint_mto_as_mts](sale_stock_orderpoint_mto_as_mts/) | 16.0.1.0.1 |  | Ensure orderpoint when so line route is mto
[stock_location_orderpoint](stock_location_orderpoint/) | 16.0.3.0.0 | <a href='https://github.com/mt-software-de'><img src='https://github.com/mt-software-de.png' width='32' height='32' style='border-radius:50%;' alt='mt-software-de'/></a> <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Declare orderpoint on a location allowing to replenish any product with the same criteria.
[stock_location_orderpoint_average_daily_sale](stock_location_orderpoint_average_daily_sale/) | 16.0.1.0.0 |  | This module allows to base replenishments quantities (on stock locations) on average daily sales
[stock_location_orderpoint_cleanup](stock_location_orderpoint_cleanup/) | 16.0.1.0.0 |  | This module allows to clean moves generated by orderpoint
[stock_orderpoint_default_location](stock_orderpoint_default_location/) | 16.0.1.0.0 |  | This module allows to define a different default location than the stock location
[stock_orderpoint_move_link](stock_orderpoint_move_link/) | 16.0.1.0.1 |  | Link Reordering rules to stock moves
[stock_orderpoint_mto_as_mts](stock_orderpoint_mto_as_mts/) | 16.0.1.3.1 |  | Materialize need from MTO route through orderpoint
[stock_orderpoint_no_horizon](stock_orderpoint_no_horizon/) | 16.0.1.0.0 |  | Consider all future moves, do not limit horizon to the rule lead days.
[stock_orderpoint_origin](stock_orderpoint_origin/) | 16.0.1.0.0 |  | Link Purchase Orders to the replenishment demand Sales Orders
[stock_orderpoint_origin_mrp_link](stock_orderpoint_origin_mrp_link/) | 16.0.1.0.0 |  | Link Purchase Orders to the replenishment demand MOs
[stock_orderpoint_purchase_link](stock_orderpoint_purchase_link/) | 16.0.1.0.0 |  | Link Reordering rules to purchase orders
[stock_orderpoint_route](stock_orderpoint_route/) | 16.0.1.0.0 |  | Allows to force a route to be used when procuring from orderpoints

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-reporting&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-reporting/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-reporting/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/stock-logistics-reporting/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-reporting/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-reporting/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-reporting)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-reporting-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-reporting-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[delivery_line_sale_line_position](delivery_line_sale_line_position/) | 16.0.1.1.0 |  | Adds the sale line position to the delivery report lines
[stock_account_valuation_discrepancy_adjust](stock_account_valuation_discrepancy_adjust/) | 16.0.1.0.0 | <a href='https://github.com/AaronHForgeFlow'><img src='https://github.com/AaronHForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='AaronHForgeFlow'/></a> | Implements Wizard for Adjust Discrepancies on Account Inventory Valuation
[stock_account_valuation_report](stock_account_valuation_report/) | 16.0.1.1.1 |  | Improves logic of the Inventory Valuation Report
[stock_average_daily_sale](stock_average_daily_sale/) | 16.0.3.0.2 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Allows to gather consumed products on daily basis
[stock_card_report](stock_card_report/) | 16.0.1.0.2 |  | Add stock card report on Inventory Reporting.
[stock_move_value_report](stock_move_value_report/) | 16.0.1.0.0 |  | Stock Move Cost Value Report
[stock_picking_batch_report](stock_picking_batch_report/) | 16.0.1.0.0 |  | Stock Picking Batch Report
[stock_picking_comment_template](stock_picking_comment_template/) | 16.0.1.0.0 | <a href='https://github.com/cubells'><img src='https://github.com/cubells.png' width='32' height='32' style='border-radius:50%;' alt='cubells'/></a> | Comments texts templates on Picking documents
[stock_picking_operations_multilang](stock_picking_operations_multilang/) | 16.0.1.0.0 |  | Stock Picking Operations Multilang
[stock_picking_report_custom_description](stock_picking_report_custom_description/) | 16.0.1.0.2 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> | Show moves description in picking reports
[stock_picking_report_delivery_custom_name](stock_picking_report_delivery_custom_name/) | 16.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allows to hide the product display name in favor of the picking description
[stock_picking_report_delivery_driver](stock_picking_report_delivery_driver/) | 16.0.1.1.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Delivery Driver info in Stock Picking reports
[stock_picking_report_external_note](stock_picking_report_external_note/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Adds a note in Stock Picking shown on external reports like Delivery Slip
[stock_picking_report_header_repeater](stock_picking_report_header_repeater/) | 16.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Stock Picking Report Header Repeater
[stock_picking_report_incoming_delivery_address](stock_picking_report_incoming_delivery_address/) | 16.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Allow show delivery address in report when picking type is incoming
[stock_picking_report_internal_delivery_address](stock_picking_report_internal_delivery_address/) | 16.0.1.0.0 |  | Show delivery address when picking type is internal
[stock_picking_report_product_sticker](stock_picking_report_product_sticker/) | 16.0.1.0.4 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Stock Picking Report - Product Sticker
[stock_picking_report_qty_undelivered](stock_picking_report_qty_undelivered/) | 16.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Print a summary of the undelivered quantity
[stock_picking_report_salesperson](stock_picking_report_salesperson/) | 16.0.1.1.0 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Salesperson info in Stock Picking reports
[stock_picking_report_summary](stock_picking_report_summary/) | 16.0.1.0.0 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Stock Picking Report Summary
[stock_picking_report_valued](stock_picking_report_valued/) | 16.0.1.2.1 |  | Adding Valued Picking on Delivery Slip report
[stock_picking_report_valued_sale_mrp](stock_picking_report_valued_sale_mrp/) | 16.0.1.0.0 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Allow to summarize the picking related with the selled kits
[stock_portal_lot_list_download](stock_portal_lot_list_download/) | 16.0.1.0.0 |  | Allows portal users to download lot list of delivery pickings in Excel format.
[stock_quantity_history_location](stock_quantity_history_location/) | 16.0.1.1.0 | <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> <a href='https://github.com/rolandojduartem'><img src='https://github.com/rolandojduartem.png' width='32' height='32' style='border-radius:50%;' alt='rolandojduartem'/></a> | Provides stock quantity by location on past date
[stock_report_quantity_by_location](stock_report_quantity_by_location/) | 16.0.1.0.0 |  | Stock Report Quantity By Location

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-request&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-request/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-request/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/stock-logistics-request/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-request/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-request/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-request)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-request-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-request-16-0/?utm_source=widget)

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
[stock_request](stock_request/) | 16.0.1.1.3 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Internal request for stock
[stock_request_direction](stock_request_direction/) | 16.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | From or to your warehouse?
[stock_request_kanban](stock_request_kanban/) | 16.0.1.0.0 |  | Adds a stock request order, and takes stock requests as lines
[stock_request_mrp](stock_request_mrp/) | 16.0.1.0.2 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Manufacturing request for stock
[stock_request_picking_type](stock_request_picking_type/) | 16.0.1.0.0 | <a href='https://github.com/max3903'><img src='https://github.com/max3903.png' width='32' height='32' style='border-radius:50%;' alt='max3903'/></a> | Add Stock Requests to the Inventory App
[stock_request_purchase](stock_request_purchase/) | 16.0.1.0.3 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Internal request for stock
[stock_request_submit](stock_request_submit/) | 16.0.1.0.0 |  | Add submit state on Stock Requests
[stock_request_tier_validation](stock_request_tier_validation/) | 16.0.2.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Extends the functionality of Stock Requests to support a tier validation process.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# stock-logistics-tracking
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-tracking&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-tracking/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-tracking/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/stock-logistics-tracking/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-tracking/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-tracking/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-tracking)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-tracking-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-tracking-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[internal_stock_quant_package](internal_stock_quant_package/) | 16.0.1.0.0 |  | This module allows to declare internal stock quant package
[stock_quant_package_multi_reference](stock_quant_package_multi_reference/) | 16.0.1.0.1 |  | Package multi reference

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# stock-logistics-transport
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-transport&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-transport/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-transport/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/stock-logistics-transport/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-transport/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-transport/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-transport)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-transport-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-transport-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[shipment_advice](shipment_advice/) | 16.0.1.11.0 |  | Manage your (un)loading process through shipment advices.
[shipment_advice_planner](shipment_advice_planner/) | 16.0.1.1.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | This module is used to plan ready transfers in shipment advices.
[shipment_advice_planner_toursolver](shipment_advice_planner_toursolver/) | 16.0.3.2.0 |  | Shipment advices planning by geo-optimization (TourSolver)
[shipment_advice_planner_toursolver_queue_job](shipment_advice_planner_toursolver_queue_job/) | 16.0.1.0.0 |  | Run TourSolver queries in queue jobs
[stock_depot](stock_depot/) | 16.0.1.0.0 |  | This module allows users to manage partners stock depots.
[stock_dock](stock_dock/) | 16.0.1.0.1 |  | Manage the loading docks of your warehouse.
[stock_location_address](stock_location_address/) | 16.0.1.0.0 |  | Adds an address on locations
[stock_location_address_purchase](stock_location_address_purchase/) | 16.0.1.0.0 |  | Uses the location address on purchases

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# stock-logistics-warehouse
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-warehouse&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-warehouse/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-warehouse/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/stock-logistics-warehouse/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-warehouse/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-warehouse/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-warehouse)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-warehouse-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-warehouse-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_move_line_product](account_move_line_product/) | 16.0.1.0.0 |  | Displays the product in the journal entries and items
[account_move_line_stock_info](account_move_line_stock_info/) | 16.0.1.1.2 |  | Account Move Line Stock Info
[base_product_merge](base_product_merge/) | 16.0.1.0.3 | <a href='https://github.com/JasminSForgeFlow'><img src='https://github.com/JasminSForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JasminSForgeFlow'/></a> | Merge duplicate products
[procurement_auto_create_group](procurement_auto_create_group/) | 16.0.1.1.0 |  | Allows to configure the system to propose automatically new procurement groups during the procurement run.
[product_packaging_usability](product_packaging_usability/) | 16.0.1.0.1 |  | Add sugar to Product Packaging
[product_route_profile](product_route_profile/) | 16.0.1.0.0 | <a href='https://github.com/Kev-Roche'><img src='https://github.com/Kev-Roche.png' width='32' height='32' style='border-radius:50%;' alt='Kev-Roche'/></a> | Add Route profile concept on product
[product_view_inventory_no_search_default_my_count](product_view_inventory_no_search_default_my_count/) | 16.0.1.0.0 |  | Product View Inventory No Search Default My Count
[scrap_reason_code](scrap_reason_code/) | 16.0.1.1.1 | <a href='https://github.com/bodedra'><img src='https://github.com/bodedra.png' width='32' height='32' style='border-radius:50%;' alt='bodedra'/></a> | Reason code for scrapping
[stock_cycle_count](stock_cycle_count/) | 16.0.2.2.1 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | Adds the capability to schedule cycle counts in a warehouse through different rules defined by the user.
[stock_demand_estimate](stock_demand_estimate/) | 16.0.1.2.1 |  | Allows to create demand estimates.
[stock_demand_estimate_matrix](stock_demand_estimate_matrix/) | 16.0.1.0.1 |  | Allows to create demand estimates.
[stock_exception](stock_exception/) | 16.0.1.1.1 |  | Custom exceptions on stock picking
[stock_helper](stock_helper/) | 16.0.1.1.0 |  | Add methods shared between various stock modules
[stock_inventory](stock_inventory/) | 16.0.3.0.0 |  | Allows to do an easier follow up of the Inventory Adjustments
[stock_inventory_count_to_zero](stock_inventory_count_to_zero/) | 16.0.1.0.1 |  | Request an inventory count filling the quantities to zero as default
[stock_inventory_discrepancy](stock_inventory_discrepancy/) | 16.0.2.1.1 |  | Adds the capability to show the discrepancy of every line in an inventory and to block the inventory validation when the discrepancy is over a user defined threshold.
[stock_inventory_justification](stock_inventory_justification/) | 16.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> <a href='https://github.com/ThomasBinsfeld'><img src='https://github.com/ThomasBinsfeld.png' width='32' height='32' style='border-radius:50%;' alt='ThomasBinsfeld'/></a> | This module allows to set justification on inventories
[stock_inventory_lockdown](stock_inventory_lockdown/) | 16.0.1.0.1 |  | Lock down stock locations during inventories.
[stock_inventory_preparation_filter](stock_inventory_preparation_filter/) | 16.0.1.1.1 |  | More filters for inventory adjustments
[stock_inventory_quantity_history](stock_inventory_quantity_history/) | 16.0.1.0.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Keep theoretical and real quantities history
[stock_location_children](stock_location_children/) | 16.0.1.0.2 |  | Add relation between stock location and all its children
[stock_location_fill_state](stock_location_fill_state/) | 16.0.1.0.2 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | This module allows to identify the fill state of stock locations
[stock_location_lockdown](stock_location_lockdown/) | 16.0.1.0.2 |  | Prevent to add stock on locked locations
[stock_location_package_restriction](stock_location_package_restriction/) | 16.0.1.0.2 |  | Control if the location can contain products in a package
[stock_location_pending_move](stock_location_pending_move/) | 16.0.1.0.2 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | This module allows to show pending stock moves (outgoing and incoming) on a stock location
[stock_location_position](stock_location_position/) | 16.0.1.0.1 |  | Add coordinate attributes on stock location.
[stock_location_product_restriction](stock_location_product_restriction/) | 16.0.1.2.2 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Prevent to mix different products into the same stock location
[stock_location_release_channel_restriction](stock_location_release_channel_restriction/) | 16.0.1.2.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | This module allows to restrict location content to products that are in the same release channel (moves).
[stock_location_zone](stock_location_zone/) | 16.0.1.0.2 |  | Classify locations with zones.
[stock_lot_multi_image](stock_lot_multi_image/) | 16.0.1.0.1 |  | This module implements the possibility to have multiple images for a stock lot
[stock_move_auto_assign](stock_move_auto_assign/) | 16.0.1.1.3 |  | Try to reserve moves when goods enter in a location
[stock_move_auto_assign_auto_release](stock_move_auto_assign_auto_release/) | 16.0.1.2.2 |  | Auto release moves after auto assign
[stock_move_auto_assign_auto_release_exclude_location](stock_move_auto_assign_auto_release_exclude_location/) | 16.0.1.0.1 |  | Exclude locations from auto release moves after auto assign
[stock_move_common_dest](stock_move_common_dest/) | 16.0.1.0.2 |  | Adds field for common destination moves
[stock_move_location](stock_move_location/) | 16.0.1.4.3 |  | This module allows to move all stock in a stock location to an other one.
[stock_move_packaging_qty](stock_move_packaging_qty/) | 16.0.1.5.0 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Add packaging fields in the stock moves
[stock_mts_mto_rule](stock_mts_mto_rule/) | 16.0.1.0.3 |  | Add a MTS+MTO route
[stock_package_type_category](stock_package_type_category/) | 16.0.1.0.1 |  | This module allows to group package types in different categories
[stock_package_type_volume](stock_package_type_volume/) | 16.0.1.0.1 |  | Compute volume of a package type
[stock_packaging_calculator](stock_packaging_calculator/) | 16.0.1.0.2 |  | Compute product quantity to pick by packaging
[stock_packaging_calculator_packaging_level](stock_packaging_calculator_packaging_level/) | 16.0.1.0.0 |  | Glue module for packaging level
[stock_picking_batch_packaging_qty](stock_picking_batch_packaging_qty/) | 16.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Add packaging fields in stock picking batch
[stock_picking_commercial_partner](stock_picking_commercial_partner/) | 16.0.1.0.1 |  | Add Commercial Partner on the Stock Picking
[stock_picking_dock](stock_picking_dock/) | 16.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Link docks to pickings.
[stock_picking_location_check](stock_picking_location_check/) | 16.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Ensure picking and move line locations are consistent
[stock_picking_procure_method](stock_picking_procure_method/) | 16.0.1.0.2 |  | Allows to force the procurement method from the picking
[stock_picking_product_interchangeable](stock_picking_product_interchangeable/) | 16.0.1.0.1 | <a href='https://github.com/CetmixGitDrone'><img src='https://github.com/CetmixGitDrone.png' width='32' height='32' style='border-radius:50%;' alt='CetmixGitDrone'/></a> | Stock Picking Product Interchangeable
[stock_picking_show_linked](stock_picking_show_linked/) | 16.0.1.0.0 |  | This addon allows to easily access related pickings (in the case of chained routes) through a button in the parent picking view.
[stock_picking_volume](stock_picking_volume/) | 16.0.1.1.2 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Compute volume information on stock moves and pickings
[stock_picking_volume_packaging](stock_picking_volume_packaging/) | 16.0.1.0.1 |  | Use volume information on potential product packaging to compute the volume of a stock.move
[stock_product_qty_by_packaging](stock_product_qty_by_packaging/) | 16.0.1.1.0 |  | Compute product quantity to pick by packaging
[stock_production_lot_quantity_tree](stock_production_lot_quantity_tree/) | 16.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Allows to display product quantity field on production lot tree view
[stock_pull_list](stock_pull_list/) | 16.0.1.0.1 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | The pull list checks the stock situation and calculates needed quantities.
[stock_putaway_product_template](stock_putaway_product_template/) | 16.0.1.1.0 | <a href='https://github.com/kevinkhao'><img src='https://github.com/kevinkhao.png' width='32' height='32' style='border-radius:50%;' alt='kevinkhao'/></a> <a href='https://github.com/sebastienbeau'><img src='https://github.com/sebastienbeau.png' width='32' height='32' style='border-radius:50%;' alt='sebastienbeau'/></a> | Add product template in putaway strategies from the product view
[stock_quant_cost_info](stock_quant_cost_info/) | 16.0.1.0.0 |  | Shows the cost of the quants
[stock_quant_expiration_date_tree](stock_quant_expiration_date_tree/) | 16.0.1.1.0 | <a href='https://github.com/manuelcalerosolis'><img src='https://github.com/manuelcalerosolis.png' width='32' height='32' style='border-radius:50%;' alt='manuelcalerosolis'/></a> | Allows to display expirations dates on stock quant tree view
[stock_quant_manual_assign](stock_quant_manual_assign/) | 16.0.1.3.1 |  | Stock - Manual Quant Assignment
[stock_quant_reservation_info](stock_quant_reservation_info/) | 16.0.1.0.1 |  | Allows to see the reserved info of Products
[stock_quant_reservation_info_mrp](stock_quant_reservation_info_mrp/) | 16.0.1.0.1 |  | Allows to see the manufacturing order related to the reserved info of Products
[stock_quant_safe_inventory](stock_quant_safe_inventory/) | 16.0.1.0.1 |  | Prevents the quantity on the quant from being updated if quantities have already been picked but not validated in pickings in progress.
[stock_removal_location_by_priority](stock_removal_location_by_priority/) | 16.0.1.0.1 |  | Establish a removal priority on stock locations.
[stock_request_purchase_request](stock_request_purchase_request/) | 16.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | Stock Request Purchase Request
[stock_reservation_date_show](stock_reservation_date_show/) | 16.0.1.0.0 |  | Display reservation date of stock moves
[stock_reserve](stock_reserve/) | 16.0.1.3.1 |  | Stock reservations on products
[stock_reserve_rule](stock_reserve_rule/) | 16.0.1.0.1 |  | Configure reservation rules by location
[stock_route_mto](stock_route_mto/) | 16.0.1.0.1 |  | Allows to identify MTO routes through a checkbox and availability to filter them.
[stock_scrap_location_default](stock_scrap_location_default/) | 16.0.1.0.1 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Allows to define a setting at company level that reference a default scrap location
[stock_search_supplierinfo_code](stock_search_supplierinfo_code/) | 16.0.1.0.1 |  | Allows to search for picking from supplierinfo code
[stock_secondary_unit](stock_secondary_unit/) | 16.0.1.1.2 |  | Get product quantities in a secondary unit
[stock_storage_category_capacity_name](stock_storage_category_capacity_name/) | 16.0.1.0.1 |  | Allows to have a better display name for Stock Storage Category Capacity model
[stock_valuation_layer_accounting_date](stock_valuation_layer_accounting_date/) | 16.0.1.0.3 |  | Stock Valuation Layer Accounting Date
[stock_valuation_layer_inventory_filter](stock_valuation_layer_inventory_filter/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Allows to filter Inventory Adjustments on Stock Valuation Layers
[stock_valuation_layer_total_value](stock_valuation_layer_total_value/) | 16.0.1.0.1 |  | Show total value on tree and form view
[stock_vlm_mgmt](stock_vlm_mgmt/) | 16.0.1.0.3 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Light self contained alternative for VLM integrations
[stock_vlm_mgmt_kardex](stock_vlm_mgmt_kardex/) | 16.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Light alternative for Kardex VLM integrations
[stock_vlm_mgmt_modula](stock_vlm_mgmt_modula/) | 16.0.1.0.1 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Light alternative for Modula VLM integrations
[stock_warehouse_calendar](stock_warehouse_calendar/) | 16.0.1.0.2 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> | Adds a calendar to the Warehouse
[stock_warehouse_relationship](stock_warehouse_relationship/) | 16.0.1.0.0 | <a href='https://github.com/petrus-v'><img src='https://github.com/petrus-v.png' width='32' height='32' style='border-radius:50%;' alt='petrus-v'/></a> | Technical module to add warehouse_id field on various stock.* models
[stock_warehouse_security](stock_warehouse_security/) | 16.0.1.0.0 | <a href='https://github.com/petrus-v'><img src='https://github.com/petrus-v.png' width='32' height='32' style='border-radius:50%;' alt='petrus-v'/></a> | Restrict user access in multi-warehouse environment


Unported addons
---------------
addon | version | maintainers | summary
--- | --- | --- | ---
[stock_package_type_button_box](stock_package_type_button_box/) | 16.0.1.0.0 (unported) | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | DEPRECATED - This module is a technical module that allows to fill in a button box for Stock Package Type form view

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# stock-logistics-workflow
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/stock-logistics-workflow&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/stock-logistics-workflow/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-workflow/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/stock-logistics-workflow/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/stock-logistics-workflow/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/stock-logistics-workflow/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/stock-logistics-workflow)
[![Translation Status](https://translation.odoo-community.org/widgets/stock-logistics-workflow-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/stock-logistics-workflow-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[delivery_procurement_group_carrier](delivery_procurement_group_carrier/) | 16.0.1.2.2 |  | Delivery Procurement Group Carrier
[delivery_total_weight_from_packaging](delivery_total_weight_from_packaging/) | 16.0.1.0.1 |  | Include packaging weight on move, transfer and package.
[procurement_auto_create_group_carrier](procurement_auto_create_group_carrier/) | 16.0.1.0.0 |  | Procurement Auto Create Group Carrier
[product_cost_price_avco_sync](product_cost_price_avco_sync/) | 16.0.1.0.0 | <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Set product cost price from updated moves
[product_expiry_simple](product_expiry_simple/) | 16.0.1.2.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Simpler and better alternative to the official product_expiry module
[product_supplierinfo_for_customer_picking](product_supplierinfo_for_customer_picking/) | 16.0.1.0.0 | <a href='https://github.com/aleuffre'><img src='https://github.com/aleuffre.png' width='32' height='32' style='border-radius:50%;' alt='aleuffre'/></a> <a href='https://github.com/renda-dev'><img src='https://github.com/renda-dev.png' width='32' height='32' style='border-radius:50%;' alt='renda-dev'/></a> <a href='https://github.com/PicchiSeba'><img src='https://github.com/PicchiSeba.png' width='32' height='32' style='border-radius:50%;' alt='PicchiSeba'/></a> | This module makes the product customer code visible in the stock moves of a picking.
[purchase_stock_picking_invoice_link](purchase_stock_picking_invoice_link/) | 16.0.1.0.1 |  | Adds link between purchases, pickings and invoices
[sale_line_returned_qty](sale_line_returned_qty/) | 16.0.1.0.0 |  | Track returned quantity of sale order lines.
[sale_order_global_stock_route](sale_order_global_stock_route/) | 16.0.1.1.1 |  | Add the possibility to choose one warehouse path for an order
[sale_stock_restocking_fee_invoicing](sale_stock_restocking_fee_invoicing/) | 16.0.1.0.0 |  | On demand charge restocking fee for accepting returned goods .
[stock_account_product_run_fifo_hook](stock_account_product_run_fifo_hook/) | 16.0.2.1.2 |  | Add more flexibility in the run fifo method.
[stock_auto_move](stock_auto_move/) | 16.0.1.0.0 |  | Automatic Move Processing
[stock_customer_deposit](stock_customer_deposit/) | 16.0.1.2.2 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Customer deposits in your warehouse
[stock_customer_deposit_elaboration](stock_customer_deposit_elaboration/) | 16.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Glue module betwen stock_customer_deposit and sale_elaboration
[stock_customer_deposit_sale_margin](stock_customer_deposit_sale_margin/) | 16.0.1.0.2 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Set purchase price to zero when deliver customer deposit
[stock_delivery_note](stock_delivery_note/) | 16.0.1.0.0 |  | This module allows to fill in a delivery note that will be displayed on delivery report
[stock_grn](stock_grn/) | 16.0.1.2.0 |  | Goods Received Note
[stock_landed_costs_currency](stock_landed_costs_currency/) | 16.0.1.0.0 |  | Stock Landed Costs Currency
[stock_landed_costs_delivery](stock_landed_costs_delivery/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Stock landed costs delivery
[stock_landed_costs_priority](stock_landed_costs_priority/) | 16.0.1.0.0 |  | Add priority to landed costs
[stock_landed_costs_purchase_auto](stock_landed_costs_purchase_auto/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Stock landed costs purchase auto
[stock_landed_costs_security](stock_landed_costs_security/) | 16.0.1.0.0 | <a href='https://github.com/cesar-tecnativa'><img src='https://github.com/cesar-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='cesar-tecnativa'/></a> | Stock landed costs security
[stock_lock_lot](stock_lock_lot/) | 16.0.1.0.0 |  | Stock Lock Lot
[stock_lot_on_hand_first](stock_lot_on_hand_first/) | 16.0.1.0.0 | <a href='https://github.com/grindtildeath'><img src='https://github.com/grindtildeath.png' width='32' height='32' style='border-radius:50%;' alt='grindtildeath'/></a> | Allows to display lots on hand first in M2o fields
[stock_lot_production_date](stock_lot_production_date/) | 16.0.1.0.0 |  | Stock Lot Production Date
[stock_lot_remove](stock_lot_remove/) | 16.0.1.0.1 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Automatically move remaining quants with a past removal date out " "of your stock
[stock_lot_scrap](stock_lot_scrap/) | 16.0.1.0.0 |  | This module adds a button in Production Lot/Serial Number view form to Scrap all products contained.
[stock_move_actual_date](stock_move_actual_date/) | 16.0.2.1.0 |  | Stock Move Actual Date
[stock_move_free_reservation_reassign](stock_move_free_reservation_reassign/) | 16.0.1.0.1 |  | Try to reassign a move when its reservation is removed due to the related quant becoming unavailable
[stock_move_line_auto_fill](stock_move_line_auto_fill/) | 16.0.1.1.1 |  | Stock Move Line auto fill
[stock_move_line_change_lot](stock_move_line_change_lot/) | 16.0.1.2.0 |  | Stock Move Line Change Lot
[stock_move_line_dates](stock_move_line_dates/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Add Date Scheduled and Deadline dates in move lines
[stock_move_line_expiration_date_required](stock_move_line_expiration_date_required/) | 16.0.1.0.2 |  | Stock Move Line Expiration Date Required
[stock_move_line_lock_qty_done](stock_move_line_lock_qty_done/) | 16.0.1.1.0 |  | Restrict modifications to the done quantity in validated stock moves
[stock_move_line_reserved_quant](stock_move_line_reserved_quant/) | 16.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | This module allows to get the link from a stock move line to the reserved quant
[stock_move_line_serial_unique](stock_move_line_serial_unique/) | 16.0.1.0.0 |  | Stock Move Line Serial Unique
[stock_move_manage_priority](stock_move_manage_priority/) | 16.0.1.0.1 |  | Stock Move Priority Management
[stock_move_not_merge_by_dest_moves](stock_move_not_merge_by_dest_moves/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Do not merge stock moves that go to different destination moves
[stock_move_original_date](stock_move_original_date/) | 16.0.1.0.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> | adds the Original Date Scheduled to stock moves.
[stock_move_priority_picking_assign](stock_move_priority_picking_assign/) | 16.0.1.0.0 |  | This module allows to create a stock movement with a priority and transfer it to the picking during assignation (for new ones)
[stock_move_propagate_first_move](stock_move_propagate_first_move/) | 16.0.1.1.0 |  | This addon propagate the picking type of the original move to all next moves created from procurement
[stock_move_quick_lot](stock_move_quick_lot/) | 16.0.1.0.0 |  | Set lot name and end date directly on picking operations
[stock_no_negative](stock_no_negative/) | 16.0.1.0.2 |  | Disallow negative stock levels by default
[stock_override_procurement](stock_override_procurement/) | 16.0.1.0.0 |  | This technical module allow to override procurement values
[stock_owner_restriction](stock_owner_restriction/) | 16.0.1.1.2 |  | Do not reserve quantity with assigned owner
[stock_partner_delivery_window](stock_partner_delivery_window/) | 16.0.1.1.0 |  | Define preferred delivery time windows for partners
[stock_picking_auto_create_lot](stock_picking_auto_create_lot/) | 16.0.3.2.0 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Auto create lots for incoming pickings
[stock_picking_auto_create_lot_qty](stock_picking_auto_create_lot_qty/) | 16.0.1.0.0 |  | Auto batch generation by quantity
[stock_picking_auto_create_lot_sequence](stock_picking_auto_create_lot_sequence/) | 16.0.1.0.0 |  | Stock Picking Auto Create Lot Sequence
[stock_picking_availability_filter](stock_picking_availability_filter/) | 16.0.1.0.0 |  | Adds availability filters to the transfers tree view
[stock_picking_back2draft](stock_picking_back2draft/) | 16.0.1.0.0 |  | Reopen cancelled pickings
[stock_picking_batch_extended](stock_picking_batch_extended/) | 16.0.1.1.1 | <a href='https://github.com/gurneyalex'><img src='https://github.com/gurneyalex.png' width='32' height='32' style='border-radius:50%;' alt='gurneyalex'/></a> <a href='https://github.com/carlosdauden'><img src='https://github.com/carlosdauden.png' width='32' height='32' style='border-radius:50%;' alt='carlosdauden'/></a> <a href='https://github.com/i-vyshnevska'><img src='https://github.com/i-vyshnevska.png' width='32' height='32' style='border-radius:50%;' alt='i-vyshnevska'/></a> | Allows manage a lot of pickings in batch
[stock_picking_batch_extended_account](stock_picking_batch_extended_account/) | 16.0.1.0.3 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | Generates invoices when batch is set to Done state
[stock_picking_batch_extended_account_sale_type](stock_picking_batch_extended_account_sale_type/) | 16.0.1.0.3 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | Generates invoices when batch is set to Done state
[stock_picking_batch_invoice_frequency](stock_picking_batch_invoice_frequency/) | 16.0.1.0.2 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Invoice Sale Orders from Stock Pickin Batch
[stock_picking_batch_print_invoices](stock_picking_batch_print_invoices/) | 16.0.1.1.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Print invoices from stock picking batchs
[stock_picking_batch_print_pickings](stock_picking_batch_print_pickings/) | 16.0.1.1.0 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Print Picking from Stock Picking Batch
[stock_picking_batch_start](stock_picking_batch_start/) | 16.0.1.0.0 |  | This module depends on the `stock_picking_start` module, which allows for users to start of all individual pickings through buttons accessible on the batch form view.
[stock_picking_batch_validate_confirm](stock_picking_batch_validate_confirm/) | 16.0.1.1.2 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Request confirmation when validating batch if there are pending origin moves
[stock_picking_customer_ref](stock_picking_customer_ref/) | 16.0.1.0.0 |  | This module displays the sale reference/description in the pickings
[stock_picking_date_deadline_syncs_scheduled_date](stock_picking_date_deadline_syncs_scheduled_date/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> | Sync Scheduled Date with Date Deadline in Stock Picking
[stock_picking_filter_lot](stock_picking_filter_lot/) | 16.0.1.0.0 |  | In picking out lots' selection, filter lots based on their location
[stock_picking_grn_mandatory](stock_picking_grn_mandatory/) | 16.0.1.1.0 |  | This module allows to require a GRN (Goods Receive Note) when doing a Stock Picking
[stock_picking_group_by_base](stock_picking_group_by_base/) | 16.0.1.0.1 |  | Allows to define a way to create index on extensible domain
[stock_picking_group_by_max_weight](stock_picking_group_by_max_weight/) | 16.0.1.1.1 |  | Allows to filter available pickings for which a maximum weight is not exceeded.
[stock_picking_group_by_partner_by_carrier](stock_picking_group_by_partner_by_carrier/) | 16.0.2.0.0 |  | Stock Picking: group by partner and carrier
[stock_picking_group_by_partner_by_carrier_by_date](stock_picking_group_by_partner_by_carrier_by_date/) | 16.0.1.0.0 |  | Stock Picking: group by partner and carrier and scheduled date
[stock_picking_import_serial_number](stock_picking_import_serial_number/) | 16.0.1.0.1 | <a href='https://github.com/sergio-teruel'><img src='https://github.com/sergio-teruel.png' width='32' height='32' style='border-radius:50%;' alt='sergio-teruel'/></a> | Import S/N from excel file for incoming pickings
[stock_picking_info_lot](stock_picking_info_lot/) | 16.0.1.0.0 |  | Add lot information on Stock Transfer lines
[stock_picking_invoice_link](stock_picking_invoice_link/) | 16.0.1.1.6 |  | Adds link between pickings and invoices
[stock_picking_kind](stock_picking_kind/) | 16.0.1.0.0 |  | Computes the kind of picking based on locations
[stock_picking_late_activity](stock_picking_late_activity/) | 16.0.1.0.0 | <a href='https://github.com/ernestotejeda'><img src='https://github.com/ernestotejeda.png' width='32' height='32' style='border-radius:50%;' alt='ernestotejeda'/></a> | Add an scheduled action that creates late picking activities
[stock_picking_line_sequence](stock_picking_line_sequence/) | 16.0.1.0.1 |  | Manages the order of stock moves by displaying its sequence
[stock_picking_mass_action](stock_picking_mass_action/) | 16.0.1.1.1 |  | Stock Picking Mass Action
[stock_picking_move_package_to_package](stock_picking_move_package_to_package/) | 16.0.1.0.1 |  | Move entire package to another package
[stock_picking_operation_quick_change](stock_picking_operation_quick_change/) | 16.0.1.0.0 |  | Change location of all picking operations
[stock_picking_origin_reference](stock_picking_origin_reference/) | 16.0.1.0.0 |  | Add clickable button to the Transfer Source Document.
[stock_picking_origin_reference_purchase](stock_picking_origin_reference_purchase/) | 16.0.1.0.0 |  | Transfer to Purchase Order navigation from the Source Document.
[stock_picking_origin_reference_sale](stock_picking_origin_reference_sale/) | 16.0.1.0.0 |  | Transfer to Sales Order navigation from the Source Document.
[stock_picking_partner_note](stock_picking_partner_note/) | 16.0.1.1.0 |  | Add partner notes on picking
[stock_picking_portal](stock_picking_portal/) | 16.0.1.0.0 |  | Show customer delivery orders in portal
[stock_picking_product_assortment](stock_picking_product_assortment/) | 16.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Stock Picking Product Assortment
[stock_picking_product_link](stock_picking_product_link/) | 16.0.1.0.0 | <a href='https://github.com/robinkeunen'><img src='https://github.com/robinkeunen.png' width='32' height='32' style='border-radius:50%;' alt='robinkeunen'/></a> | Adds a "Product" smart button on stock pickings.
[stock_picking_progress](stock_picking_progress/) | 16.0.1.0.0 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> <a href='https://github.com/JuMiSanAr'><img src='https://github.com/JuMiSanAr.png' width='32' height='32' style='border-radius:50%;' alt='JuMiSanAr'/></a> | Compute the stock.picking progression
[stock_picking_purchase_order_link](stock_picking_purchase_order_link/) | 16.0.1.0.1 |  | Link between picking and purchase order
[stock_picking_putaway_recompute](stock_picking_putaway_recompute/) | 16.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | This module allows to recompute the picking operations putaways if configurations have changed
[stock_picking_putinpack_restriction](stock_picking_putinpack_restriction/) | 16.0.1.0.1 |  | Adds a restriction on transfer type to force or disallow the use of destination package.
[stock_picking_quick](stock_picking_quick/) | 16.0.1.0.0 | <a href='https://github.com/PierrickBrun'><img src='https://github.com/PierrickBrun.png' width='32' height='32' style='border-radius:50%;' alt='PierrickBrun'/></a> <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Quick Stock Picking
[stock_picking_restrict_cancel_printed](stock_picking_restrict_cancel_printed/) | 16.0.1.0.3 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Prevent canceling a stock transfer if printed.
[stock_picking_return_empty_package](stock_picking_return_empty_package/) | 16.0.1.0.0 |  | Ensure that only package content is put in stock during a picking return
[stock_picking_return_lot](stock_picking_return_lot/) | 16.0.1.1.0 |  | Propagate SN/lots from origin picking to return picking.
[stock_picking_return_restricted_qty](stock_picking_return_restricted_qty/) | 16.0.1.0.0 |  | Restrict the return to delivered quantity
[stock_picking_sale_order_link](stock_picking_sale_order_link/) | 16.0.1.0.1 |  | Link between picking and sale order
[stock_picking_send_by_mail](stock_picking_send_by_mail/) | 16.0.1.0.0 |  | Send stock picking by email
[stock_picking_show_backorder](stock_picking_show_backorder/) | 16.0.1.0.0 |  | Provides a new field on stock pickings, allowing to display the corresponding backorders.
[stock_picking_show_return](stock_picking_show_return/) | 16.0.1.0.1 |  | Show returns on stock pickings
[stock_picking_start](stock_picking_start/) | 16.0.1.2.0 |  | Add button to start picking
[stock_picking_status_notification](stock_picking_status_notification/) | 16.0.1.0.0 |  | Notify selected internal users of changes in picking states
[stock_picking_supplier_ref](stock_picking_supplier_ref/) | 16.0.1.0.0 |  | Adds a supplier reference field inside supplier's pickings and allows search for this reference.
[stock_picking_to_batch_group_fields](stock_picking_to_batch_group_fields/) | 16.0.1.0.1 | <a href='https://github.com/EmilioPascual'><img src='https://github.com/EmilioPascual.png' width='32' height='32' style='border-radius:50%;' alt='EmilioPascual'/></a> | Allows to create batches grouped by picking fields.
[stock_picking_type_bypass_reservation](stock_picking_type_bypass_reservation/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Bypass reservation on desired Stock Picking Types
[stock_picking_warn_message](stock_picking_warn_message/) | 16.0.1.0.0 |  | Add a popup warning on picking to ensure warning is populated
[stock_procurement_customer](stock_procurement_customer/) | 16.0.1.0.1 |  | Allows to store customer if different from the partner
[stock_product_set](stock_product_set/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Add product sets in pickings
[stock_production_lot_active](stock_production_lot_active/) | 16.0.1.0.0 | <a href='https://github.com/ThomasBinsfeld'><img src='https://github.com/ThomasBinsfeld.png' width='32' height='32' style='border-radius:50%;' alt='ThomasBinsfeld'/></a> | Allow to archive/unarchive lots/serial numbers
[stock_putaway_hook](stock_putaway_hook/) | 16.0.1.0.1 |  | Add hooks allowing modules to add more putaway strategies
[stock_quant_package_dimension](stock_quant_package_dimension/) | 16.0.1.0.1 |  | Use dimensions on packages
[stock_quant_package_dimension_total_weight_from_packaging](stock_quant_package_dimension_total_weight_from_packaging/) | 16.0.1.0.0 |  | Estimated weight of a package
[stock_quant_package_product_packaging](stock_quant_package_product_packaging/) | 16.0.1.0.1 |  | Use product packagings on packages
[stock_receipt_lot_info](stock_receipt_lot_info/) | 16.0.1.1.0 |  | Be able to introduce more info on lot/serial number while processing a receipt.
[stock_reporting_access](stock_reporting_access/) | 16.0.1.0.0 | <a href='https://github.com/yostashiro'><img src='https://github.com/yostashiro.png' width='32' height='32' style='border-radius:50%;' alt='yostashiro'/></a> <a href='https://github.com/aungkokolin1997'><img src='https://github.com/aungkokolin1997.png' width='32' height='32' style='border-radius:50%;' alt='aungkokolin1997'/></a> | Add a security group for inventory reporting access
[stock_restrict_lot](stock_restrict_lot/) | 16.0.2.1.0 | <a href='https://github.com/florian-dacosta'><img src='https://github.com/florian-dacosta.png' width='32' height='32' style='border-radius:50%;' alt='florian-dacosta'/></a> | Base module that add back the concept of restrict lot on stock move
[stock_rule_reserve_max_quantity](stock_rule_reserve_max_quantity/) | 16.0.1.0.1 | <a href='https://github.com/Shide'><img src='https://github.com/Shide.png' width='32' height='32' style='border-radius:50%;' alt='Shide'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Allows to reserve max available quantity when a move comes from an stock rule
[stock_split_picking](stock_split_picking/) | 16.0.2.0.0 |  | Split a picking in two not transferred pickings
[stock_split_picking_dimension](stock_split_picking_dimension/) | 16.0.2.0.0 |  | Split a picking in two not transferred pickings to ensure that the first one doesn't exceed given dimensions (nbr lines, volume, weight)
[stock_valuation_layer_usage](stock_valuation_layer_usage/) | 16.0.2.1.0 |  | Trace where has the stock valuation been used in, including the quantities taken.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# storage
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/storage&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/storage/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/storage/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/storage/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/storage/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/storage/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/storage)
[![Translation Status](https://translation.odoo-community.org/widgets/storage-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/storage-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[fs_attachment](fs_attachment/) | 16.0.3.1.1 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Store attachments on external object store
[fs_attachment_environment](fs_attachment_environment/) | 16.0.1.0.0 |  | Allows to use server environment with fs storage attachment
[fs_attachment_s3](fs_attachment_s3/) | 16.0.3.1.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Store attachments into S3 complient filesystem
[fs_attachment_s3_environment](fs_attachment_s3_environment/) | 16.0.1.0.0 |  | Allows to use server environment with fs storage attachment S3
[fs_base_multi_image](fs_base_multi_image/) | 16.0.1.1.2 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Mulitple Images from External File System
[fs_base_multi_media](fs_base_multi_media/) | 16.0.1.0.2 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Give the possibility to store media data in external filesystem from odoo
[fs_file](fs_file/) | 16.0.1.0.7 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Field to store files into filesystem storages
[fs_file_demo](fs_file_demo/) | 16.0.1.0.2 |  | Demo addon for fs_file and fs_image
[fs_image](fs_image/) | 16.0.1.0.5 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Field to store images into filesystem storages
[fs_image_thumbnail](fs_image_thumbnail/) | 16.0.1.0.3 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Generate and store thumbnail for images
[fs_product_brand_multi_image](fs_product_brand_multi_image/) | 16.0.1.0.1 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Link images to product brands
[fs_product_multi_image](fs_product_multi_image/) | 16.0.1.1.6 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Manage multi images from extenal file system on product
[fs_product_multi_media](fs_product_multi_media/) | 16.0.1.0.3 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> | Link media to products and categories
[fs_product_public_category_multi_image](fs_product_public_category_multi_image/) | 16.0.1.0.1 |  | Manage multi images from extenal file system on eCommerce public categories
[fs_storage](fs_storage/) | 16.0.2.0.0 |  | Implement the concept of Storage with amazon S3, sftp...
[fs_storage_backup](fs_storage_backup/) | 16.0.2.0.0 |  | Filesystem Storage Backup
[fs_storage_backup_environment](fs_storage_backup_environment/) | 16.0.1.0.0 |  | Allows to use server environment with fs storage attachment
[fs_storage_environment](fs_storage_environment/) | 16.0.1.0.0 |  | Allows to use server environment with fs storage
[image_tag](image_tag/) | 16.0.2.0.0 |  | Image tag model
[image_tag_environment](image_tag_environment/) | 16.0.2.0.0 |  | Server environment features for the Image Tag model
[storage_backend](storage_backend/) | 16.0.1.1.0 |  | Implement the concept of Storage with amazon S3, sftp...
[storage_backend_ftp](storage_backend_ftp/) | 16.0.1.0.0 |  | Implement FTP Storage
[storage_backend_sftp](storage_backend_sftp/) | 16.0.1.0.2 |  | Implement SFTP Storage
[storage_file](storage_file/) | 16.0.1.0.1 |  | Storage file in storage backend

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# survey
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/survey&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/survey/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/survey/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/survey/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/survey/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/survey/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/survey)
[![Translation Status](https://translation.odoo-community.org/widgets/survey-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/survey-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[partner_survey](partner_survey/) | 16.0.1.1.0 |  | Link partners with their survey results
[survey_certification_branding](survey_certification_branding/) | 16.0.1.0.0 |  | This module enables customization of certification reports by allowing a custom logo and company name per certification.
[survey_contact_generation](survey_contact_generation/) | 16.0.1.1.2 | <a href='https://github.com/chienandalu'><img src='https://github.com/chienandalu.png' width='32' height='32' style='border-radius:50%;' alt='chienandalu'/></a> | Generate new contacts from surveys
[survey_formio](survey_formio/) | 16.0.1.0.0 |  | This module allows the generation of a form.io compatible JSON for a survey.
[survey_link_base](survey_link_base/) | 16.0.1.0.0 |  | This addon creates a mixin and a wizard to enable the generation of surveys from other models.
[survey_question_type_binary](survey_question_type_binary/) | 16.0.1.0.0 |  | This module add binary field as question type for survey page
[survey_question_type_five_star](survey_question_type_five_star/) | 16.0.1.0.0 |  | This module adds five stars rating as question type for survey page
[survey_question_type_nps](survey_question_type_nps/) | 16.0.1.0.0 |  | This module add nps rating as question type for survey page
[survey_resource_booking](survey_resource_booking/) | 16.0.1.0.0 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Access survey answers from resource booking
[survey_xlsx](survey_xlsx/) | 16.0.1.0.0 |  | XLSX Report to show the survey results

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/timesheet&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/timesheet/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/timesheet/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/timesheet/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/timesheet/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/timesheet/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/timesheet)
[![Translation Status](https://translation.odoo-community.org/widgets/timesheet-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/timesheet-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[crm_timesheet](crm_timesheet/) | 16.0.1.1.0 |  | CRM Timesheet
[hr_employee_cost_history](hr_employee_cost_history/) | 16.0.1.1.0 | <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | Adds an history to employee's costs.
[hr_timesheet_begin_end](hr_timesheet_begin_end/) | 16.0.1.0.1 |  | Timesheet - Begin/End Hours
[hr_timesheet_calendar](hr_timesheet_calendar/) | 16.0.1.0.3 | <a href='https://github.com/lbarry-apsl'><img src='https://github.com/lbarry-apsl.png' width='32' height='32' style='border-radius:50%;' alt='lbarry-apsl'/></a> | HR Timesheet Calendar
[hr_timesheet_date_order_desc](hr_timesheet_date_order_desc/) | 16.0.1.0.0 |  | Add new timesheet entries to the top of the list and order by date descending
[hr_timesheet_editable_top](hr_timesheet_editable_top/) | 16.0.1.0.0 |  | Add new timesheet entries to the top of the list
[hr_timesheet_employee_analytic_tag](hr_timesheet_employee_analytic_tag/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Hr Timesheet Employee Analytic Tag
[hr_timesheet_name_customer](hr_timesheet_name_customer/) | 16.0.1.1.0 |  | Add 'Description Customer' field for timesheets
[hr_timesheet_portal](hr_timesheet_portal/) | 16.0.1.0.0 |  | Fill in timesheets via the portal
[hr_timesheet_predefined_description](hr_timesheet_predefined_description/) | 16.0.1.0.0 | <a href='https://github.com/juanjosesegui-tecnativa'><img src='https://github.com/juanjosesegui-tecnativa.png' width='32' height='32' style='border-radius:50%;' alt='juanjosesegui-tecnativa'/></a> | Predefined descriptions for timesheet entries
[hr_timesheet_predefined_description_rules](hr_timesheet_predefined_description_rules/) | 16.0.1.0.0 |  | Manage predefined descriptions for timesheet entries
[hr_timesheet_report](hr_timesheet_report/) | 16.0.1.1.0 | <a href='https://github.com/alexey-pelykh'><img src='https://github.com/alexey-pelykh.png' width='32' height='32' style='border-radius:50%;' alt='alexey-pelykh'/></a> | Generate Timesheet Report from Task Logs
[hr_timesheet_report_rounded](hr_timesheet_report_rounded/) | 16.0.1.0.0 |  | Show rounded time in the Timesheet Reports
[hr_timesheet_sheet](hr_timesheet_sheet/) | 16.0.1.2.0 |  | Timesheet Sheets, Activities
[hr_timesheet_sheet_attendance](hr_timesheet_sheet_attendance/) | 16.0.1.0.2 |  | HR Timesheet Sheet Attendance
[hr_timesheet_sheet_autodraft](hr_timesheet_sheet_autodraft/) | 16.0.1.0.1 |  | Automatically draft a Timesheet Sheet for every time entry that does not have a relevant Timesheet Sheet existing.
[hr_timesheet_sheet_policy_department_manager](hr_timesheet_sheet_policy_department_manager/) | 16.0.1.0.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | Allows setting Department Manager as Reviewer
[hr_timesheet_sheet_policy_project_manager](hr_timesheet_sheet_policy_project_manager/) | 16.0.1.0.0 |  | Allows setting Project Manager as Reviewer
[hr_timesheet_task_domain](hr_timesheet_task_domain/) | 16.0.1.0.0 |  | Limit task selection to tasks on currently-selected project
[hr_timesheet_task_required](hr_timesheet_task_required/) | 16.0.1.0.0 |  | Set task on timesheet as a mandatory field
[hr_timesheet_task_stage](hr_timesheet_task_stage/) | 16.0.1.0.1 |  | Open/Close task from corresponding Task Log entry
[hr_timesheet_time_restriction](hr_timesheet_time_restriction/) | 16.0.1.0.1 |  | Restrictions on the creation of time sheets for past dates
[hr_timesheet_time_type](hr_timesheet_time_type/) | 16.0.1.0.1 |  | Ability to add time type in timesheet lines.
[hr_timesheet_type_non_billable](hr_timesheet_type_non_billable/) | 16.0.1.0.0 | <a href='https://github.com/mpascuall'><img src='https://github.com/mpascuall.png' width='32' height='32' style='border-radius:50%;' alt='mpascuall'/></a> | HR Timesheet Type Non Billable
[project_task_analytic_propagation](project_task_analytic_propagation/) | 16.0.2.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/sabrinaRMartin'><img src='https://github.com/sabrinaRMartin.png' width='32' height='32' style='border-radius:50%;' alt='sabrinaRMartin'/></a> | Updates timesheet's analytic account when their task changes the analytic.
[project_task_stage_allow_timesheet](project_task_stage_allow_timesheet/) | 16.0.1.0.1 |  | Allows to tell that a task stage is opened for timesheets.
[sale_timesheet_budget](sale_timesheet_budget/) | 16.0.1.0.0 | <a href='https://github.com/victoralmau'><img src='https://github.com/victoralmau.png' width='32' height='32' style='border-radius:50%;' alt='victoralmau'/></a> | Sale timesheet budget
[sale_timesheet_invoice_link](sale_timesheet_invoice_link/) | 16.0.1.0.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Link invoices with timesheet lines
[sale_timesheet_line_exclude](sale_timesheet_line_exclude/) | 16.0.1.2.0 |  | Exclude Timesheet Line from Sale Order
[sale_timesheet_rounded](sale_timesheet_rounded/) | 16.0.1.0.0 |  | Round timesheet entries amount based on project settings.
[sale_timesheet_task_exclude](sale_timesheet_task_exclude/) | 16.0.1.0.0 |  | Exclude Task and related Timesheets from Sale Order
[sale_timesheet_timeline](sale_timesheet_timeline/) | 16.0.1.0.0 |  | Dates planning in sales order lines

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/vertical-abbey


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# vertical-abbey
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/vertical-abbey&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/vertical-abbey/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/vertical-abbey/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/vertical-abbey/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/vertical-abbey/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/vertical-abbey/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/vertical-abbey)
[![Translation Status](https://translation.odoo-community.org/widgets/vertical-abbey-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/vertical-abbey-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Odoo modules for abbeys

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[donation_mass](donation_mass/) | 16.0.2.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Ability to create mass from donation lines
[donation_stay](donation_stay/) | 16.0.2.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Create donations from a stay
[mass](mass/) | 16.0.2.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Manage Mass
[stay](stay/) | 16.0.2.1.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Simple management of stays and meals
[stay_api](stay_api/) | 16.0.1.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | REST API for stay module
[stay_report_py3o](stay_report_py3o/) | 16.0.2.0.0 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Replace Qweb report by Py3o report on stay module

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# vertical-association
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/vertical-association&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/vertical-association/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/vertical-association/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/vertical-association/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/vertical-association/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/vertical-association/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/vertical-association)
[![Translation Status](https://translation.odoo-community.org/widgets/vertical-association-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/vertical-association-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[contract_membership_delegated_partner](contract_membership_delegated_partner/) | 16.0.1.0.1 |  | Set delegate membership on the contract
[membership_delegated_partner](membership_delegated_partner/) | 16.0.1.0.3 |  | Delegate membership on a specific partner
[membership_extension](membership_extension/) | 16.0.3.1.0 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Improves user experience of membership addon
[membership_initial_fee](membership_initial_fee/) | 16.0.1.0.1 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | Initial fee for memberships
[membership_prorate](membership_prorate/) | 16.0.1.0.2 |  | Prorate membership fee
[membership_prorate_variable_period](membership_prorate_variable_period/) | 16.0.1.0.2 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/edlopen'><img src='https://github.com/edlopen.png' width='32' height='32' style='border-radius:50%;' alt='edlopen'/></a> | Prorate membership fee for variable periods
[membership_variable_period](membership_variable_period/) | 16.0.1.1.0 |  | Variable period for memberships
[membership_withdrawal](membership_withdrawal/) | 16.0.1.0.0 |  | Log membership withdrawal reason and date of request
[website_membership_gamification](website_membership_gamification/) | 16.0.1.0.1 |  | Show badges assigned to users on website
[website_membership_random_order](website_membership_random_order/) | 16.0.1.0.0 | <a href='https://github.com/pedrobaeza'><img src='https://github.com/pedrobaeza.png' width='32' height='32' style='border-radius:50%;' alt='pedrobaeza'/></a> | Online Members Directory - Random order

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/vertical-construction


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/vertical-construction&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/vertical-construction/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/vertical-construction/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/vertical-construction/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/vertical-construction/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/vertical-construction/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/vertical-construction)
[![Translation Status](https://translation.odoo-community.org/widgets/vertical-construction-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/vertical-construction-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# vertical-construction

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[bc3_importer](bc3_importer/) | 16.0.1.0.0 |  | BC3 files importer

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/vertical-hotel&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/vertical-hotel/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/vertical-hotel/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/vertical-hotel/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/vertical-hotel/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/vertical-hotel/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/vertical-hotel)
[![Translation Status](https://translation.odoo-community.org/widgets/vertical-hotel-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/vertical-hotel-16-0/?utm_source=widget)

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
[hotel](hotel/) | 16.0.1.0.0 |  | Hotel Management to Manage Folio and Hotel Configuration
[hotel_housekeeping](hotel_housekeeping/) | 16.0.1.0.0 |  | Manages Housekeeping Activities and its Process

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/vertical-rental


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# vertical-rental
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/vertical-rental&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/vertical-rental/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/vertical-rental/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/vertical-rental/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/vertical-rental/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/vertical-rental/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/vertical-rental)
[![Translation Status](https://translation.odoo-community.org/widgets/vertical-rental-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/vertical-rental-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[rental_base](rental_base/) | 16.0.1.0.2 |  | Manage Rental of Products
[rental_offday](rental_offday/) | 16.0.1.0.0 |  | Manage off-days in rentals on daily basis
[rental_pricelist](rental_pricelist/) | 16.0.1.0.1 |  | Enables the user to define different rental prices with time uom ("Month", "Day" and "Hour").
[rental_product_pack](rental_product_pack/) | 16.0.1.0.0 |  | Manage rentals with product packs
[sale_rental](sale_rental/) | 16.0.1.0.4 | <a href='https://github.com/alexis-via'><img src='https://github.com/alexis-via.png' width='32' height='32' style='border-radius:50%;' alt='alexis-via'/></a> | Manage Rental of Products

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/web&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/web/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/web/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/web/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/web/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/web/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/web)
[![Translation Status](https://translation.odoo-community.org/widgets/web-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/web-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[web_action_conditionable](web_action_conditionable/) | 16.0.1.0.0 |  | web_action_conditionable
[web_advanced_search](web_advanced_search/) | 16.0.1.0.6 | <a href='https://github.com/ivantodorovich'><img src='https://github.com/ivantodorovich.png' width='32' height='32' style='border-radius:50%;' alt='ivantodorovich'/></a> | Easier and more powerful searching tools
[web_apply_field_style](web_apply_field_style/) | 16.0.1.0.1 |  | Apply css class style to fields from a dict parameters
[web_calendar_slot_duration](web_calendar_slot_duration/) | 16.0.1.1.0 | <a href='https://github.com/Yajo'><img src='https://github.com/Yajo.png' width='32' height='32' style='border-radius:50%;' alt='Yajo'/></a> | Customizable calendar slot durations
[web_chatter_camera](web_chatter_camera/) | 16.0.1.0.0 |  | Allow to use the camera on mobile views for adding attachments
[web_chatter_position](web_chatter_position/) | 16.0.1.0.5 | <a href='https://github.com/trisdoan'><img src='https://github.com/trisdoan.png' width='32' height='32' style='border-radius:50%;' alt='trisdoan'/></a> | Add an option to change the chatter position
[web_company_color](web_company_color/) | 16.0.1.2.3 |  | Web Company Color
[web_copy_confirm](web_copy_confirm/) | 16.0.1.0.0 |  | Show confirmation dialogue before copying records
[web_dark_mode](web_dark_mode/) | 16.0.1.0.2 |  | Enabled Dark Mode for the Odoo Backend
[web_dashboard_tile](web_dashboard_tile/) | 16.0.1.0.3 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add Overview Dashboards with Tiles
[web_datetime_picker_default_time](web_datetime_picker_default_time/) | 16.0.1.0.0 | <a href='https://github.com/grindtildeath'><img src='https://github.com/grindtildeath.png' width='32' height='32' style='border-radius:50%;' alt='grindtildeath'/></a> | Allows to define a default time on datetime picker
[web_dialog_size](web_dialog_size/) | 16.0.1.0.4 |  | A module that lets the user expand a dialog box to the full screen width.
[web_disable_export_group](web_disable_export_group/) | 16.0.1.0.0 |  | Web Disable Export Group
[web_domain_field](web_domain_field/) | 16.0.1.0.1 |  | Use computed field as domain
[web_edit_user_filter](web_edit_user_filter/) | 16.0.1.0.0 |  | Edit User Filters
[web_editor_class_selector](web_editor_class_selector/) | 16.0.1.1.0 |  | Web editor class selector
[web_environment_ribbon](web_environment_ribbon/) | 16.0.1.0.0 |  | Web Environment Ribbon
[web_export_html_as_text](web_export_html_as_text/) | 16.0.1.0.0 |  | Web Export Html As Text
[web_field_numeric_formatting](web_field_numeric_formatting/) | 16.0.1.0.0 |  | Allow to render float and integer fields without thousands separator
[web_field_tooltip](web_field_tooltip/) | 16.0.1.2.0 |  | Displays customizable tooltips for fields
[web_font_size_report_layout](web_font_size_report_layout/) | 16.0.1.1.0 |  | Adds a font size selector (pt) to the Document Layout wizard
[web_form_banner](web_form_banner/) | 16.0.1.1.0 |  | Web Form Banner
[web_group_by_percentage](web_group_by_percentage/) | 16.0.1.0.1 |  | Show the percentage of the total sum in group by rows
[web_group_expand](web_group_expand/) | 16.0.1.0.0 |  | Group Expand Buttons
[web_help](web_help/) | 16.0.2.0.1 |  | Help Framework
[web_hide_field_with_key](web_hide_field_with_key/) | 16.0.1.0.1 | <a href='https://github.com/franzpoize'><img src='https://github.com/franzpoize.png' width='32' height='32' style='border-radius:50%;' alt='franzpoize'/></a> | Hide fields for models
[web_ir_actions_act_multi](web_ir_actions_act_multi/) | 16.0.1.0.1 |  | Enables triggering of more than one action on ActionManager
[web_ir_actions_act_window_message](web_ir_actions_act_window_message/) | 16.0.1.0.1 |  | Show a message box to users
[web_ir_actions_act_window_page](web_ir_actions_act_window_page/) | 16.0.1.0.0 |  | Allows a developer to trigger a pager to show the previous or next next record in the form view
[web_ir_actions_close_wizard_refresh_view](web_ir_actions_close_wizard_refresh_view/) | 16.0.1.0.0 |  | Allow to refresh view data without reload the page.
[web_listview_range_select](web_listview_range_select/) | 16.0.1.0.0 |  | Enables selecting a range of records using the shift key
[web_m2x_options](web_m2x_options/) | 16.0.1.1.3 |  | web_m2x_options
[web_m2x_options_manager](web_m2x_options_manager/) | 16.0.1.0.0 |  | Adds an interface to manage the "Create" and "Create and Edit" options for specific models and fields.
[web_merge_notebook_tab](web_merge_notebook_tab/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Merge many tabs into a single one, for notebook present in form views of any models
[web_no_bubble](web_no_bubble/) | 16.0.1.0.0 |  | Remove the bubbles from the web interface
[web_notify](web_notify/) | 16.0.3.2.0 |  | Send notification messages to user
[web_notify_channel_message](web_notify_channel_message/) | 16.0.1.1.0 |  | Send an instant notification to channel users when a new message is posted
[web_notify_upgrade](web_notify_upgrade/) | 16.0.1.0.0 |  | Notify active users when a module is installed or updated
[web_phone_field_whatsapp](web_phone_field_whatsapp/) | 16.0.1.0.0 | <a href='https://github.com/adasatorres'><img src='https://github.com/adasatorres.png' width='32' height='32' style='border-radius:50%;' alt='adasatorres'/></a> | This module adds a shortcut functionality to WhatsApp Web or the WhatsApp application in the phone widget.
[web_pivot_computed_measure](web_pivot_computed_measure/) | 16.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Web Pivot Computed Measure
[web_pwa_oca](web_pwa_oca/) | 16.0.1.0.0 | <a href='https://github.com/eLBati'><img src='https://github.com/eLBati.png' width='32' height='32' style='border-radius:50%;' alt='eLBati'/></a> | Make Odoo a PWA
[web_quick_start_screen](web_quick_start_screen/) | 16.0.1.0.0 |  | Configurable start screen for quick actions
[web_refresh_from_backend](web_refresh_from_backend/) | 16.0.1.0.0 |  | Refresh views from backend
[web_refresher](web_refresher/) | 16.0.3.1.5 |  | Web Refresher
[web_remember_tree_column_width](web_remember_tree_column_width/) | 16.0.1.0.2 | <a href='https://github.com/frahikLV'><img src='https://github.com/frahikLV.png' width='32' height='32' style='border-radius:50%;' alt='frahikLV'/></a> <a href='https://github.com/luisg123v'><img src='https://github.com/luisg123v.png' width='32' height='32' style='border-radius:50%;' alt='luisg123v'/></a> <a href='https://github.com/cuongnmtm'><img src='https://github.com/cuongnmtm.png' width='32' height='32' style='border-radius:50%;' alt='cuongnmtm'/></a> | Remember the tree columns' widths across sessions.
[web_responsive](web_responsive/) | 16.0.1.4.0 | <a href='https://github.com/Tardo'><img src='https://github.com/Tardo.png' width='32' height='32' style='border-radius:50%;' alt='Tardo'/></a> <a href='https://github.com/SplashS'><img src='https://github.com/SplashS.png' width='32' height='32' style='border-radius:50%;' alt='SplashS'/></a> | Responsive web client, community-supported
[web_responsive_company](web_responsive_company/) | 16.0.1.0.1 |  | Improve the diplay of the list of the companies
[web_save_discard_button](web_save_discard_button/) | 16.0.1.0.2 | <a href='https://github.com/synconics'><img src='https://github.com/synconics.png' width='32' height='32' style='border-radius:50%;' alt='synconics'/></a> | Save & Discard Buttons
[web_search_with_and](web_search_with_and/) | 16.0.1.0.0 |  | Use AND conditions on omnibar search
[web_searchbar_full_width](web_searchbar_full_width/) | 16.0.1.0.0 |  | Show search bar in full screen width
[web_select_all_companies](web_select_all_companies/) | 16.0.1.0.2 |  | Allows you to select all companies in one click.
[web_send_message_popup](web_send_message_popup/) | 16.0.1.0.0 |  | Web Send Message as Popup
[web_sheet_full_width](web_sheet_full_width/) | 16.0.1.0.0 |  | Use the whole available screen width when displaying sheets
[web_sort_menu](web_sort_menu/) | 16.0.1.0.0 |  | Sort Apps in DropDown/NavBar Menu alphabetically
[web_systray_button_init_action](web_systray_button_init_action/) | 16.0.1.0.2 |  | Add a button to go to the user init action.
[web_theme_classic](web_theme_classic/) | 16.0.1.0.2 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Contrasted style on fields to improve the UI.
[web_time_range_menu_custom](web_time_range_menu_custom/) | 16.0.1.0.0 |  | Web Time Range Menu Custom
[web_timeline](web_timeline/) | 16.0.2.0.1 | <a href='https://github.com/tarteo'><img src='https://github.com/tarteo.png' width='32' height='32' style='border-radius:50%;' alt='tarteo'/></a> | Interactive visualization chart to show events in time
[web_touchscreen](web_touchscreen/) | 16.0.1.0.1 | <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> | UX improvements for touch screens
[web_tree_duplicate](web_tree_duplicate/) | 16.0.1.0.1 | <a href='https://github.com/tarteo'><img src='https://github.com/tarteo.png' width='32' height='32' style='border-radius:50%;' alt='tarteo'/></a> | Duplicate records directly from the tree view.
[web_tree_dynamic_colored_field](web_tree_dynamic_colored_field/) | 16.0.1.0.0 |  | Allows you to dynamically color fields on tree views
[web_tree_many2one_clickable](web_tree_many2one_clickable/) | 16.0.1.0.1 |  | Open the linked resource when clicking on their name
[web_widget_bokeh_chart](web_widget_bokeh_chart/) | 16.0.1.1.0 | <a href='https://github.com/LoisRForgeFlow'><img src='https://github.com/LoisRForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='LoisRForgeFlow'/></a> <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | This widget allows to display charts using Bokeh library.
[web_widget_char_size](web_widget_char_size/) | 16.0.1.0.1 |  | Add size option to Char widget
[web_widget_datepicker_fulloptions](web_widget_datepicker_fulloptions/) | 16.0.1.0.0 |  | Web Widget DatePicker Full Options
[web_widget_domain_editor_dialog](web_widget_domain_editor_dialog/) | 16.0.1.0.0 |  | Recovers the Domain Editor Dialog functionality
[web_widget_dropdown_dynamic](web_widget_dropdown_dynamic/) | 16.0.2.0.0 |  | This module adds support for dynamic dropdown widget
[web_widget_image_download](web_widget_image_download/) | 16.0.1.0.0 |  | Allows to download any image from its widget
[web_widget_image_webcam](web_widget_image_webcam/) | 16.0.1.0.0 |  | Allows to take image with WebCam
[web_widget_mpld3_chart](web_widget_mpld3_chart/) | 16.0.1.0.0 | <a href='https://github.com/JordiBForgeFlow'><img src='https://github.com/JordiBForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='JordiBForgeFlow'/></a> <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | This widget allows to display charts using MPLD3 library.
[web_widget_numeric_step](web_widget_numeric_step/) | 16.0.1.1.5 | <a href='https://github.com/rafaelbn'><img src='https://github.com/rafaelbn.png' width='32' height='32' style='border-radius:50%;' alt='rafaelbn'/></a> <a href='https://github.com/yajo'><img src='https://github.com/yajo.png' width='32' height='32' style='border-radius:50%;' alt='yajo'/></a> | Web Widget Numeric Step
[web_widget_one2many_tree_line_duplicate](web_widget_one2many_tree_line_duplicate/) | 16.0.1.0.0 |  | Web Widget One2many Tree Line Duplicate
[web_widget_open_tab](web_widget_open_tab/) | 16.0.2.0.0 |  | Allow to open record from trees on new tab from tree views
[web_widget_pattern](web_widget_pattern/) | 16.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Allows to define a regex for validating input on the backend
[web_widget_pattern_partner_autocomplete](web_widget_pattern_partner_autocomplete/) | 16.0.1.0.0 | <a href='https://github.com/hbrunn'><img src='https://github.com/hbrunn.png' width='32' height='32' style='border-radius:50%;' alt='hbrunn'/></a> | Allows to define a regex for validating input on the backend
[web_widget_plotly_chart](web_widget_plotly_chart/) | 16.0.1.0.0 | <a href='https://github.com/robyf70'><img src='https://github.com/robyf70.png' width='32' height='32' style='border-radius:50%;' alt='robyf70'/></a> | Allow to draw plotly charts.
[web_widget_product_label_section_and_note](web_widget_product_label_section_and_note/) | 16.0.1.0.5 |  | unify the product and name into a single column
[web_widget_progressbar_gradient](web_widget_progressbar_gradient/) | 16.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | This module allows to display progressbar with gradient
[web_widget_remaining_days_exact_date](web_widget_remaining_days_exact_date/) | 16.0.1.0.0 | <a href='https://github.com/CarlosRoca13'><img src='https://github.com/CarlosRoca13.png' width='32' height='32' style='border-radius:50%;' alt='CarlosRoca13'/></a> | Allows displaying the exact date alongside the remaining days
[web_widget_x2many_2d_matrix](web_widget_x2many_2d_matrix/) | 16.0.1.1.4 | <a href='https://github.com/ChrisOForgeFlow'><img src='https://github.com/ChrisOForgeFlow.png' width='32' height='32' style='border-radius:50%;' alt='ChrisOForgeFlow'/></a> | Show list fields as a matrix

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Support the OCA](https://odoo-community.org/readme-banner-image)](https://odoo-community.org/get-involved?utm_source=repo-readme)

# Web API
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/web-api&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/web-api/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/web-api/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/web-api/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/web-api/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/web-api/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/web-api)
[![Translation Status](https://translation.odoo-community.org/widgets/web-api-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/web-api-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

Collect Odoo modules that help exposing web APIs and/or deal with external web APIs.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[endpoint](endpoint/) | 16.0.1.4.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Provide custom endpoint machinery.
[endpoint_auth_api_key](endpoint_auth_api_key/) | 16.0.1.1.2 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Provide API key auth for endpoints.
[endpoint_route_handler](endpoint_route_handler/) | 16.0.1.1.2 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Provide mixin and tool to generate custom endpoints on the fly.
[webservice](webservice/) | 16.0.1.6.0 | <a href='https://github.com/etobella'><img src='https://github.com/etobella.png' width='32' height='32' style='border-radius:50%;' alt='etobella'/></a> | Defines webservice abstract definition to be used generally

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/website&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/website/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/website/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/website/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/website/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/website/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/website)
[![Translation Status](https://translation.odoo-community.org/widgets/website-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/website-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[website_analytics_matomo](website_analytics_matomo/) | 16.0.1.1.0 |  | Track website users using matomo
[website_cookiebot](website_cookiebot/) | 16.0.2.0.0 |  | Ask for cookies consent connecting with Cookiebot
[website_cookiefirst](website_cookiefirst/) | 16.0.2.0.0 |  | Cookiefirst integration
[website_crm_privacy_policy](website_crm_privacy_policy/) | 16.0.2.0.0 |  | Website CRM privacy policy
[website_crm_quick_answer](website_crm_quick_answer/) | 16.0.1.0.0 |  | Add an automatic answer for contacts asking for info
[website_form_require_legal](website_form_require_legal/) | 16.0.1.1.0 |  | Add possibility to require confirm legal terms.
[website_forum_subscription](website_forum_subscription/) | 16.0.1.0.0 |  | Adds a button to allow subscription from the website
[website_google_tag_manager](website_google_tag_manager/) | 16.0.1.1.0 |  | Add support for Google Tag Manager
[website_legal_page](website_legal_page/) | 16.0.1.1.0 |  | Website Legal Page
[website_llms](website_llms/) | 16.0.1.0.0 | <a href='https://github.com/marcelsavegnago'><img src='https://github.com/marcelsavegnago.png' width='32' height='32' style='border-radius:50%;' alt='marcelsavegnago'/></a> | This module adds support for serving a /llms.txt file in the website root. The content can be configured per website in the website settings.
[website_menu_by_user_status](website_menu_by_user_status/) | 16.0.1.0.0 |  | Allow to manage the display of website.menus
[website_odoo_debranding](website_odoo_debranding/) | 16.0.1.0.0 |  | Remove Odoo Branding from Website
[website_recaptcha_v2](website_recaptcha_v2/) | 16.0.1.0.0 |  | Helper module to add reCAPTCHA v2 to website forms
[website_require_login](website_require_login/) | 16.0.1.1.0 |  | Website Login Required
[website_snippet_country_dropdown](website_snippet_country_dropdown/) | 16.0.1.0.0 |  | Allow to select country in a dropdown
[website_snippet_country_phone_code_dropdown](website_snippet_country_phone_code_dropdown/) | 16.0.1.0.0 |  | Allow to select country in a dropdown, and fill with phone code
[website_whatsapp](website_whatsapp/) | 16.0.1.1.0 | <a href='https://github.com/ioans73'><img src='https://github.com/ioans73.png' width='32' height='32' style='border-radius:50%;' alt='ioans73'/></a> | Whatsapp integration

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

## From OCA/website-cms


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/website-cms&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/website-cms/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/website-cms/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/website-cms/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/website-cms/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/website-cms/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/website-cms)
[![Translation Status](https://translation.odoo-community.org/widgets/website-cms-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/website-cms-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# website-cms

CMS features for Odoo portal and websites. Ease creation of forms, status message, actions and more.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[cms_form](cms_form/) | 16.0.1.3.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Basic content type form
[cms_info](cms_info/) | 16.0.1.2.0 |  | A set of basic information needed to expose any kind of record in your CMS.
[cms_status_message](cms_status_message/) | 16.0.1.0.1 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Basic status messages for your CMS system


Unported addons
---------------
addon | version | maintainers | summary
--- | --- | --- | ---
[cms_form_example](cms_form_example/) | 13.0.1.0.1 (unported) |  | Basic content type form example

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

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


[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/wms&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/wms/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/wms/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/wms/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/wms/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/wms/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/wms)
[![Translation Status](https://translation.odoo-community.org/widgets/wms-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/wms-16-0/?utm_source=widget)

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
[delivery_carrier_warehouse](delivery_carrier_warehouse/) | 16.0.1.0.1 |  | Get delivery method used in sales orders from warehouse
[sale_stock_available_to_promise_release](sale_stock_available_to_promise_release/) | 16.0.1.2.0 |  | Integration between Sales and Available to Promise Release
[sale_stock_available_to_promise_release_block](sale_stock_available_to_promise_release_block/) | 16.0.1.1.1 |  | Block release of deliveries from sales orders.
[sale_stock_release_channel](sale_stock_release_channel/) | 16.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Sales Stock Release Channel
[sale_stock_release_channel_delivery](sale_stock_release_channel_delivery/) | 16.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Sales Stock Release Channel Delivery
[sale_stock_release_channel_delivery_date](sale_stock_release_channel_delivery_date/) | 16.0.1.1.2 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Compute expected date based on available release channels
[sale_stock_release_channel_partner_by_date](sale_stock_release_channel_partner_by_date/) | 16.0.1.1.0 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Release channels integration with Sales
[sale_stock_release_channel_partner_by_date_delivery](sale_stock_release_channel_partner_by_date_delivery/) | 16.0.1.1.1 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Filters channels on sales based on selected carrier.
[shopfloor](shopfloor/) | 16.0.2.25.1 | <a href='https://github.com/guewen'><img src='https://github.com/guewen.png' width='32' height='32' style='border-radius:50%;' alt='guewen'/></a> <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | manage warehouse operations with barcode scanners
[shopfloor_base](shopfloor_base/) | 16.0.1.2.2 | <a href='https://github.com/guewen'><img src='https://github.com/guewen.png' width='32' height='32' style='border-radius:50%;' alt='guewen'/></a> <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Core module for creating mobile apps
[shopfloor_batch_automatic_creation](shopfloor_batch_automatic_creation/) | 16.0.1.2.0 | <a href='https://github.com/guewen'><img src='https://github.com/guewen.png' width='32' height='32' style='border-radius:50%;' alt='guewen'/></a> | Create batch transfers for Cluster Picking
[shopfloor_gs1](shopfloor_gs1/) | 16.0.1.1.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> | Integrate GS1 barcode scan into Shopfloor app
[shopfloor_mobile](shopfloor_mobile/) | 16.0.1.8.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Mobile frontend for WMS Shopfloor app
[shopfloor_mobile_base](shopfloor_mobile_base/) | 16.0.1.3.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Mobile frontend for WMS Shopfloor app
[shopfloor_mobile_base_auth_api_key](shopfloor_mobile_base_auth_api_key/) | 16.0.1.0.0 |  | Provides authentication via API key to Shopfloor base mobile app
[shopfloor_product_dimension](shopfloor_product_dimension/) | 16.0.1.0.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | This module allow to enrich product available details about its dimension in shopfloor
[shopfloor_reception](shopfloor_reception/) | 16.0.1.16.1 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> <a href='https://github.com/JuMiSanAr'><img src='https://github.com/JuMiSanAr.png' width='32' height='32' style='border-radius:50%;' alt='JuMiSanAr'/></a> | Reception scenario for shopfloor
[shopfloor_reception_add_packaging](shopfloor_reception_add_packaging/) | 16.0.1.0.0 |  | Enables to add a packaging during Reception scenario in Shopfloor.
[shopfloor_reception_add_packaging_mobile](shopfloor_reception_add_packaging_mobile/) | 16.0.1.0.0 |  | Add a 'create new packaging' button in 'set_quantity' screen of Shopfloor.
[shopfloor_reception_dock](shopfloor_reception_dock/) | 16.0.1.2.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/nicolas-delbovier-acsone'><img src='https://github.com/nicolas-delbovier-acsone.png' width='32' height='32' style='border-radius:50%;' alt='nicolas-delbovier-acsone'/></a> | Add docks info to shopfloor
[shopfloor_reception_dock_mobile](shopfloor_reception_dock_mobile/) | 16.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/nicolas-delbovier-acsone'><img src='https://github.com/nicolas-delbovier-acsone.png' width='32' height='32' style='border-radius:50%;' alt='nicolas-delbovier-acsone'/></a> | Add docks info to picking cards in shopfloor app.
[shopfloor_reception_grn](shopfloor_reception_grn/) | 16.0.1.0.0 |  | Enables to select a reception by scanning its GRN.
[shopfloor_reception_grn_mobile](shopfloor_reception_grn_mobile/) | 16.0.1.0.0 |  | Adds GRN on the receptions cards in Shopfloor Reception.
[shopfloor_reception_helpdesk](shopfloor_reception_helpdesk/) | 16.0.1.0.0 |  | This module allows to create helpdesk tickets in reception scenarios
[shopfloor_reception_helpdesk_mobile](shopfloor_reception_helpdesk_mobile/) | 16.0.1.0.0 |  | This module allows to manage front display for helpdesk management in reception scenario
[shopfloor_reception_mobile](shopfloor_reception_mobile/) | 16.0.1.9.0 | <a href='https://github.com/JuMiSanAr'><img src='https://github.com/JuMiSanAr.png' width='32' height='32' style='border-radius:50%;' alt='JuMiSanAr'/></a> | Scenario for receiving products
[shopfloor_reception_packaging_dimension](shopfloor_reception_packaging_dimension/) | 16.0.1.2.1 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Collect Packaging Dimension from the Reception scenario
[shopfloor_reception_packaging_dimension_mobile](shopfloor_reception_packaging_dimension_mobile/) | 16.0.1.1.0 | <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Frontend for the packaging dimension on reception scenario
[shopfloor_reception_product_barcode](shopfloor_reception_product_barcode/) | 16.0.1.2.1 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Collect Product Barcode from the Reception scenario
[shopfloor_reception_product_barcode_mobile](shopfloor_reception_product_barcode_mobile/) | 16.0.1.1.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Frontend for the product barcode on reception scenario
[shopfloor_reception_putinpack_restriction](shopfloor_reception_putinpack_restriction/) | 16.0.1.1.0 |  | Restrict the use of packages in shopfloor reception
[shopfloor_reception_refund_return](shopfloor_reception_refund_return/) | 16.0.1.0.0 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Mark created return as to refund
[shopfloor_rest_log](shopfloor_rest_log/) | 16.0.1.0.0 | <a href='https://github.com/simahawk'><img src='https://github.com/simahawk.png' width='32' height='32' style='border-radius:50%;' alt='simahawk'/></a> | Integrate rest_log into Shopfloor app
[shopfloor_single_product_transfer](shopfloor_single_product_transfer/) | 16.0.1.0.0 | <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> | Move an item from one location to another.
[shopfloor_single_product_transfer_mobile](shopfloor_single_product_transfer_mobile/) | 16.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/TDu'><img src='https://github.com/TDu.png' width='32' height='32' style='border-radius:50%;' alt='TDu'/></a> <a href='https://github.com/mmequignon'><img src='https://github.com/mmequignon.png' width='32' height='32' style='border-radius:50%;' alt='mmequignon'/></a> | Mobile frontend for single product transfer scenario
[shopfloor_workstation](shopfloor_workstation/) | 16.0.1.0.0 |  | Manage warehouse workstation with barcode scanners
[shopfloor_workstation_mobile](shopfloor_workstation_mobile/) | 16.0.1.0.0 |  | Shopfloor mobile app integration for workstation
[stock_available_to_promise_release](stock_available_to_promise_release/) | 16.0.3.9.0 |  | Release Operations based on available to promise
[stock_available_to_promise_release_block](stock_available_to_promise_release_block/) | 16.0.1.1.2 |  | Block Release of Operations
[stock_available_to_promise_release_dynamic_routing](stock_available_to_promise_release_dynamic_routing/) | 16.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Glue between moves release and dynamic routing
[stock_available_to_promise_release_exclude_location](stock_available_to_promise_release_exclude_location/) | 16.0.1.0.0 |  | Exclude locations from available stock
[stock_dynamic_routing](stock_dynamic_routing/) | 16.0.1.0.4 |  | Dynamic routing of stock moves
[stock_full_location_reservation](stock_full_location_reservation/) | 16.0.1.1.0 | <a href='https://github.com/mt-software-de'><img src='https://github.com/mt-software-de.png' width='32' height='32' style='border-radius:50%;' alt='mt-software-de'/></a> | Extend reservation to full content of location
[stock_picking_batch_creation](stock_picking_batch_creation/) | 16.0.2.2.0 | <a href='https://github.com/lmignon'><img src='https://github.com/lmignon.png' width='32' height='32' style='border-radius:50%;' alt='lmignon'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Create a batch of pickings to be processed all together
[stock_picking_completion_info](stock_picking_completion_info/) | 16.0.1.0.1 |  | Display on current document completion information according to next operations
[stock_picking_type_shipping_policy](stock_picking_type_shipping_policy/) | 16.0.1.0.0 |  | Define different shipping policies according to picking type
[stock_release_channel](stock_release_channel/) | 16.0.3.1.2 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/mt-software-de'><img src='https://github.com/mt-software-de.png' width='32' height='32' style='border-radius:50%;' alt='mt-software-de'/></a> | Manage workload in WMS with release channels
[stock_release_channel_auto_release](stock_release_channel_auto_release/) | 16.0.1.1.0 |  | Add an automatic release mode to the release channel
[stock_release_channel_batch_mode_commercial_partner](stock_release_channel_batch_mode_commercial_partner/) | 16.0.1.0.2 |  | Release pickings into channels by batch of same commercial entity
[stock_release_channel_cutoff](stock_release_channel_cutoff/) | 16.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Add the cutoff time to the release channel
[stock_release_channel_delivery](stock_release_channel_delivery/) | 16.0.3.0.0 |  | Add a carrier selection criteria on the release channel
[stock_release_channel_depot](stock_release_channel_depot/) | 16.0.1.0.0 |  | This module allows users to add partner depot to stock release channel.
[stock_release_channel_geoengine](stock_release_channel_geoengine/) | 16.0.2.0.0 |  | Release channel based on geo-localization
[stock_release_channel_partner_by_date](stock_release_channel_partner_by_date/) | 16.0.2.1.0 | <a href='https://github.com/sebalix'><img src='https://github.com/sebalix.png' width='32' height='32' style='border-radius:50%;' alt='sebalix'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Set release channels for specific delivery dates
[stock_release_channel_partner_by_date_delivery_window](stock_release_channel_partner_by_date_delivery_window/) | 16.0.1.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Glue Stock Release Channels for Delivery Dates and Delivery window
[stock_release_channel_partner_by_date_public_holidays](stock_release_channel_partner_by_date_public_holidays/) | 16.0.2.0.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Glue Stock Release Channels for Delivery Dates and Public holidays
[stock_release_channel_partner_delivery_window](stock_release_channel_partner_delivery_window/) | 16.0.2.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Allows to define an end date (and time) on a release channel and propagate it to the concerned pickings
[stock_release_channel_partner_public_holidays](stock_release_channel_partner_public_holidays/) | 16.0.2.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Add an option to exclude the public holidays when assigning th release channel
[stock_release_channel_plan](stock_release_channel_plan/) | 16.0.1.3.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Manage release channel preparation plan
[stock_release_channel_plan_depot](stock_release_channel_plan_depot/) | 16.0.1.0.0 |  | This module allows users to set partner depot on stock release channel preparation plan.
[stock_release_channel_plan_process_end_time](stock_release_channel_plan_process_end_time/) | 16.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Glue module between release channel plan and process end time
[stock_release_channel_plan_shipment_lead_time](stock_release_channel_plan_shipment_lead_time/) | 16.0.1.1.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Stock release channel plan shipment lead time
[stock_release_channel_process_end_time](stock_release_channel_process_end_time/) | 16.0.1.7.0 | <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Allows to define an end date (and time) on a release channel and propagate it to the concerned pickings
[stock_release_channel_propagate_channel_picking](stock_release_channel_propagate_channel_picking/) | 16.0.1.2.0 |  | Allows to propagate the channel to every picking that is created from the original one.
[stock_release_channel_shipment_advice](stock_release_channel_shipment_advice/) | 16.0.1.2.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Plan shipment advices for ready and released pickings
[stock_release_channel_shipment_advice_deliver](stock_release_channel_shipment_advice_deliver/) | 16.0.2.0.2 |  | This module adds an action to the release channel to automate the delivery of its shippings.
[stock_release_channel_shipment_advice_process_end_time](stock_release_channel_shipment_advice_process_end_time/) | 16.0.1.0.0 |  | This module allows to set a delay time (in minutes) between the release channel process end time and the shipment advice arrival to the dock time.
[stock_release_channel_shipment_advice_toursolver](stock_release_channel_shipment_advice_toursolver/) | 16.0.1.1.0 |  | Use TourSolver to plan shipment advices for ready and released pickings
[stock_release_channel_shipment_lead_time](stock_release_channel_shipment_lead_time/) | 16.0.2.1.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Release channel with shipment lead time
[stock_release_channel_show_volume](stock_release_channel_show_volume/) | 16.0.1.1.0 |  | Display volumes of stock release channels
[stock_release_channel_show_weight](stock_release_channel_show_weight/) | 16.0.1.1.0 |  | Display weights of stock release channels
[stock_release_channel_warehouse_calendar](stock_release_channel_warehouse_calendar/) | 16.0.1.0.1 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> | Glue module between release channel and warehouse calendar
[stock_storage_type](stock_storage_type/) | 16.0.2.2.0 | <a href='https://github.com/jbaudoux'><img src='https://github.com/jbaudoux.png' width='32' height='32' style='border-radius:50%;' alt='jbaudoux'/></a> <a href='https://github.com/rousseldenis'><img src='https://github.com/rousseldenis.png' width='32' height='32' style='border-radius:50%;' alt='rousseldenis'/></a> | Manage packages and locations storage types
[stock_storage_type_putaway_abc](stock_storage_type_putaway_abc/) | 16.0.1.0.0 |  | Advanced storage strategy ABC for WMS
[stock_warehouse_flow](stock_warehouse_flow/) | 16.0.1.1.0 |  | Configure routing flow for stock moves
[stock_warehouse_flow_delivery_refresh](stock_warehouse_flow_delivery_refresh/) | 16.0.1.0.0 |  | Allow to refresh delivery flow when carrier changes
[stock_warehouse_flow_release](stock_warehouse_flow_release/) | 16.0.1.1.0 |  | Warehouse flows integrated with Operation Release

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.


---

