# Installation

## Prerequisites

- Odoo 16.0
- `l10n_py_base` module installed
- `account` module (core Odoo)

## Installation Steps

1. **Copy Module**:
   Place the module in your Odoo addons directory

2. **Update Apps List**:
   - Go to **Apps**
   - Click **Update Apps List**

3. **Install Module**:
   - Search for "Paraguay - Accounting"
   - Click **Install**

## Post-Installation

After installation:
1. Configure your company's fiscal data in `l10n_py_base`
2. Review and adjust chart of accounts if needed
3. Configure tax rates on products
4. Set up accounting journals (install `l10n_py_account` for extended features)

## Dependencies

The module will automatically install required dependencies:
- `account`
- `l10n_py_base`

## Recommended Modules

For a complete Paraguayan localization, also install:
- `l10n_py_account`: Journal and authorization management
- `l10n_py_edi_base`: Electronic invoicing support

