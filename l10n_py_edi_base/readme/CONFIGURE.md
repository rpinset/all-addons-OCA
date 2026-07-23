# Configuration

## Initial Setup

### Step 1: Company Configuration

1. Go to **Settings > General Settings > Companies**
2. Edit your company
3. Navigate to **Electronic Invoicing** tab:
   - Enable **Electronic Invoicing**
   - Configure **Environment** (Test/Production)
   - Set **EDI Provider** (factpy/facturasend)

### Step 2: Select EDI Provider

Choose and configure your provider:

#### Option A: FactPy
1. Install `l10n_py_edi_factpy` module
2. Configure credentials in connector settings

#### Option B: FacturaSend
1. Install `l10n_py_edi_facturasend` module
2. Configure credentials in connector settings

### Step 3: Configure Products

For each product/service:
1. Go to **Products**
2. Edit product
3. In **Invoicing** tab:
   - Set **NCM Code** (if applicable)
   - Configure **GTIN** (barcode for SET)
   - Set tax information

### Step 4: Partner Configuration

Ensure customers have complete fiscal data:
1. Valid **RUC** (if taxpayer)
2. Correct **Taxpayer Type**
3. Complete **Address** (required for electronic invoicing)
4. **Email** (for sending electronic documents)

## Document Type Configuration

### Available Document Types

The module pre-configures these document types:
- **Factura Electrónica (1)**: Standard invoice
- **Nota de Crédito (4)**: Credit note
- **Nota de Débito (5)**: Debit note
- **Nota de Remisión (7)**: Delivery note
- **Autofactura (2)**: Self-invoice

### Journal Configuration

1. Go to **Accounting > Configuration > Journals**
2. For each sales journal:
   - Enable **Electronic Invoicing**
   - Select **Document Type**
   - Ensure timbrado is configured

## Security Groups

Configure user permissions:
1. Go to **Settings > Users & Companies > Users**
2. Edit user
3. In **Electronic Invoicing** section:
   - **User**: Can create and send documents
   - **Manager**: Can configure and cancel documents

## Automatic Operations

### Cron Jobs

The module includes automatic jobs:
1. **Check Document Status**: Polls provider for status updates
2. **Retry Failed Documents**: Attempts to resend failed documents

Configure in **Settings > Technical > Automation > Scheduled Actions**:
- Adjust frequency as needed
- Enable/disable jobs

### Automatic Sending

Configure automatic sending on invoice confirmation:
1. Go to company settings
2. In **Electronic Invoicing** tab:
   - Enable **Auto Send on Confirm**
   - Set **Auto Download PDF/XML**

## Environment Configuration

### Test Environment

For testing:
1. Set **Environment** = "Test"
2. Use test credentials from provider
3. Documents won't be legally valid

### Production Environment

For production:
1. Set **Environment** = "Production"
2. Use production credentials
3. Ensure all fiscal data is accurate
4. Test thoroughly before going live

## KUDE Configuration

KUDE (Código Único de Documento Electrónico) settings:
1. QR codes are generated automatically
2. Configure QR size in report templates if needed
3. KUDE appears on printed invoices

## Contingency Mode

Configure fallback when EDI service is unavailable:
1. Enable **Contingency Mode** in company settings
2. Set **Contingency Reason** options
3. Documents can be sent later when service recovers

## Email Configuration

For automatic email sending:
1. Configure **Outgoing Mail Server** in Odoo
2. Set email template in **Settings > Technical > Email Templates**
3. Customize "Electronic Invoice" template

