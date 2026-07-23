# Installation

## Prerequisites

- Odoo 16.0
- `account` module (core Odoo)
- `l10n_py_base` module installed
- Valid timbrado from SET (for production use)

## Installation Steps

1. **Install Base Module**:
   Ensure `l10n_py_base` is installed first

2. **Install Module**:
   - Go to **Apps**
   - Click **Update Apps List**
   - Search for "Paraguay - Accounting Extensions"
   - Click **Install**

3. **Verify Installation**:
   Check that new menus appear:
   - **Accounting > Configuration > Timbrados**
   - Enhanced journal configuration options

## Post-Installation Setup

### Step 1: Configure Company

Ensure company fiscal data is complete in `l10n_py_base`

### Step 2: Create First Timbrado

1. Go to **Accounting > Configuration > Timbrados**
2. Click **Create**
3. Enter your SET-provided authorization:
   - Authorization number
   - Validity dates
   - Document number range
   - Establishment and point of sale codes

### Step 3: Configure Sales Journal

1. Go to **Accounting > Configuration > Journals**
2. Edit your sales journal
3. Set:
   - Establishment code
   - Point of sale code
   - Link to timbrado
4. Save

### Step 4: Test Invoice Creation

1. Create a test invoice
2. Verify document number format: XXX-XXX-NNNNNNN
3. Check timbrado information appears correctly
4. Cancel test invoice if in production

## Demo Data

The module includes demo data:
- Sample timbrados
- Configured journals

**Note**: Delete demo data before using in production:
1. Go to **Settings > Technical > Database Structure > Demo Data**
2. Remove demo timbrados and journal configurations

## Configuration Checklist

Before going live:
- [ ] Company fiscal data complete
- [ ] Valid timbrado from SET
- [ ] Timbrado record created in system
- [ ] Sales journals configured
- [ ] Purchase journals configured (if needed)
- [ ] Document number sequences tested
- [ ] User permissions configured

## Required Information from SET

Before you can use this module in production, obtain from SET:
1. **Timbrado Number**: Authorization number
2. **Validity Period**: Start and end dates
3. **Document Range**: From/to numbers authorized
4. **Establishment Code**: Your establishment code
5. **Point of Sale Code**: Your point of emission code

## Dependencies

This module requires:
- `account`: Core accounting functionality
- `l10n_py_base`: Paraguayan base localization

## Optional Modules

For complete functionality, consider:
- `l10n_py`: Paraguayan chart of accounts
- `l10n_py_edi_base`: Electronic invoicing

## Troubleshooting Installation

### Menu Items Not Appearing

If configuration menus don't show:
1. Refresh browser
2. Check user permissions (Accounting / Manager)
3. Verify module is fully installed

### Timbrado Fields Not in Journal

If timbrado fields don't appear in journals:
1. Update module
2. Restart Odoo server
3. Clear browser cache

