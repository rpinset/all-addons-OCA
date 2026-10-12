# Installation

## Prerequisites

### Required Modules
- Odoo 16.0
- `account`: Core accounting module
- `l10n_py_base`: Paraguayan base localization
- `l10n_py_account`: Accounting extensions with timbrado
- `product`: Product management
- `sale`: Sales management

### Required Python Packages
The module requires these Python packages:
- `qrcode`: QR code generation
- `requests`: HTTP client for API calls
- `cryptography`: Encryption and security

### EDI Provider
You must choose and configure one provider:
- FactPy (install `l10n_py_edi_factpy`)
- FacturaSend (install `l10n_py_edi_facturasend`)

## Installation Steps

### Step 1: Install Dependencies

Install required Python packages:
```bash
pip install qrcode requests cryptography
```

### Step 2: Install Base Modules

1. Install prerequisites in order:
   - `l10n_py_base`
   - `l10n_py_account`

### Step 3: Install EDI Base

1. Go to **Apps**
2. Click **Update Apps List**
3. Search for "Paraguay - Electronic Invoicing Base"
4. Click **Install**

### Step 4: Install EDI Connector

Choose and install a connector:

#### Option A: FactPy
1. Search for "Paraguay - FactPy EDI Connector"
2. Click **Install**

#### Option B: FacturaSend
1. Search for "Paraguay - FacturaSend EDI Connector"
2. Click **Install**

## Post-Installation Configuration

### Step 1: Verify Installation

Check that new menus appear:
- **Facturación Electrónica** main menu
- **EDI Logs** submenu
- **Connectors** submenu

### Step 2: Configure Company

1. Go to **Settings > Companies**
2. Edit your company
3. Configure **Electronic Invoicing** tab:
   - Enable EDI
   - Select environment (Test/Production)
   - Choose provider

### Step 3: Configure EDI Provider

Follow provider-specific configuration:
- See `l10n_py_edi_factpy` documentation, or
- See `l10n_py_edi_facturasend` documentation

### Step 4: Configure Security

1. Go to **Settings > Users & Companies > Groups**
2. Assign users to EDI groups:
   - **Electronic Invoicing / User**
   - **Electronic Invoicing / Manager**

### Step 5: Initial Test

1. Set environment to **Test**
2. Create a test invoice
3. Try sending to EDI
4. Verify reception and approval
5. Check logs for errors

## Data Initialization

The module loads:
- Electronic document type definitions
- Cron job configurations
- Email templates
- Report templates

No manual data loading required.

## System Parameters

Configure in **Settings > Technical > Parameters > System Parameters**:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `l10n_py.edi_provider` | Active EDI provider | `factpy` or `facturasend` |
| `l10n_py.edi_environment` | Environment | `test` or `production` |
| `l10n_py.edi_auto_send` | Auto-send on confirm | `True` or `False` |

## Database Preparation

### Existing Invoices

For existing invoices (pre-EDI):
- They will NOT be sent to EDI automatically
- You can migrate them manually if needed
- New invoices will use EDI

### Product Updates

Update products with:
1. Tax configuration
2. NCM codes (if applicable)
3. GTIN/barcodes

### Partner Updates

Ensure all partners have:
1. Complete address
2. Valid RUC (for taxpayers)
3. Email address
4. Taxpayer type

## Testing Checklist

Before going to production:

- [ ] Test environment configured
- [ ] Test credentials working
- [ ] Sample invoice sent successfully
- [ ] PDF download works
- [ ] XML download works
- [ ] QR code generates correctly
- [ ] Status updates work
- [ ] Credit note flow tested
- [ ] Cancellation tested
- [ ] Error handling tested
- [ ] Email sending tested
- [ ] All users have correct permissions

## Production Deployment

### Pre-Production

1. Backup database
2. Complete all testing
3. Train users
4. Prepare support documentation

### Go-Live

1. Switch to production environment
2. Update provider credentials
3. Configure production parameters
4. Send first real invoice
5. Monitor logs closely

### Post-Go-Live

1. Monitor EDI logs daily
2. Check success rate
3. Respond to errors quickly
4. Keep system updated

## Troubleshooting Installation

### Python Packages Not Found

If packages are missing:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install qrcode requests cryptography
```

### Module Not Installing

If installation fails:
1. Check Odoo logs
2. Verify all dependencies installed
3. Check file permissions
4. Restart Odoo server

### Menus Not Appearing

If menus don't show:
1. Check user permissions
2. Refresh browser
3. Clear browser cache
4. Verify module is installed (not just downloaded)

## Uninstallation

To uninstall (not recommended):
1. First uninstall connector module
2. Then uninstall base module
3. Data will be preserved but EDI features disabled

**Warning**: Uninstalling will:
- Disable EDI functionality
- Remove EDI menus
- Keep existing data but make it inaccessible

## Upgrade Notes

When upgrading:
1. Backup database first
2. Test in staging environment
3. Check changelog for breaking changes
4. Update connectors to matching versions
5. Test EDI functionality after upgrade

