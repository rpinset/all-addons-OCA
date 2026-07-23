# Configuration

## Journal Configuration

Configure journals for Paraguayan fiscal documents:

1. Navigate to **Accounting > Configuration > Journals**
2. Select or create a sales/purchase journal
3. Configure Paraguayan fields:
   - **Establishment** (Punto de Expedición): e.g., "001"
   - **Point of Sale** (Punto de Emisión): e.g., "001"
   - Link to active **Timbrado**

## Timbrado (Authorization) Management

### Creating a New Timbrado

1. Go to **Accounting > Configuration > Timbrados**
2. Click **Create**
3. Fill in required information:
   - **Authorization Number** (Timbrado): e.g., "12345678"
   - **Start Date**: Authorization start date
   - **End Date**: Authorization expiration date
   - **Document Range**: From and To numbers
   - **Establishment**: e.g., "001"
   - **Point of Sale**: e.g., "001"
4. Click **Save**

### Timbrado Fields Explained

- **Authorization Number**: The timbrado number issued by SET
- **Start/End Date**: Validity period of the authorization
- **From Number**: Starting document number (e.g., 1)
- **To Number**: Ending document number (e.g., 50000)
- **Establishment**: Physical location code (001, 002, etc.)
- **Point of Sale**: Point of emission code (001, 002, etc.)

### Activating a Timbrado

1. Timbrados are automatically active if:
   - Current date is between start and end dates
   - Document numbers are not exhausted
2. System shows active status with indicators

### Linking Timbrado to Journal

1. Go to **Accounting > Configuration > Journals**
2. Edit the journal
3. Select the active timbrado from the dropdown
4. System will use this timbrado for all documents in this journal

## Document Number Sequences

The module automatically manages sequences:
- Sequences are created based on timbrado configuration
- Format: XXX-XXX-NNNNNNN (Establishment-Point of Sale-Number)
- Numbers increment automatically
- System warns when approaching limit

## Automatic Validations

The system validates:
- Timbrado is active and not expired
- Document numbers are within authorized range
- Establishment and point of sale match
- Date is within authorization period

## Multiple Timbrados

You can have multiple timbrados:
- Different establishments
- Different points of sale
- Overlapping periods (for transition)

Best practice:
1. Create new timbrado before current one expires
2. Activate new timbrado when ready
3. Old timbrado becomes inactive automatically

