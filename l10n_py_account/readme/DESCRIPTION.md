# Paraguay - Accounting Extensions

This module extends the base Paraguayan accounting localization with specific functionality required for Paraguayan fiscal compliance.

## Features

- **Journal Extensions**: Enhanced journal configuration with Paraguayan-specific fields
  - Establishment (punto de expedición)
  - Point of Sale (punto de emisión)
  - Timbrado (tax stamp authorization)

- **Authorization Management**: Complete timbrado lifecycle management
  - Authorization number tracking
  - Validity period control
  - Document number range management
  - Automatic sequence generation

- **Account Move Extensions**: Enhanced invoice/bill features
  - Automatic timbrado assignment
  - Document number formatting
  - Fiscal validations

- **Fiscal Validations**: 
  - Valid timbrado verification
  - Document number range validation
  - Expiration date checking

## Purpose

This module bridges the gap between Odoo's standard accounting and Paraguayan fiscal requirements, particularly focusing on timbrado management which is mandatory for all fiscal documents in Paraguay.

## Dependencies

- `account`: Odoo core accounting
- `l10n_py_base`: Base Paraguayan localization

