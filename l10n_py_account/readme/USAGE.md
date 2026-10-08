# Usage

## Creating Invoices with Timbrado

### Standard Invoice Flow

1. Go to **Accounting > Customers > Invoices**
2. Click **Create**
3. Select customer and add invoice lines
4. The system automatically:
   - Assigns the active timbrado from the journal
   - Generates the next document number
   - Validates timbrado status
5. Click **Confirm**

### Invoice Number Format

Invoices will have the format:
```
XXX-XXX-NNNNNNN
```
- XXX: Establishment (e.g., 001)
- XXX: Point of Sale (e.g., 001)
- NNNNNNN: Sequential number (e.g., 0000001)

Example: `001-001-0000123`

## Managing Timbrados

### Checking Timbrado Status

1. Go to **Accounting > Configuration > Timbrados**
2. View list of all timbrados
3. Status indicators show:
   - **Active**: Green (currently valid and in range)
   - **Expired**: Red (past end date)
   - **Exhausted**: Orange (all numbers used)

### When Timbrado is Expiring

The system will warn you when:
- End date is approaching (configurable threshold)
- Document numbers are running low (e.g., <100 remaining)

Action required:
1. Request new timbrado from SET
2. Create new timbrado record in system
3. Update journal to use new timbrado when ready

### Switching Between Timbrados

To change timbrado on a journal:
1. Go to **Accounting > Configuration > Journals**
2. Edit the journal
3. Change the **Timbrado** field
4. Save
5. New documents will use the new timbrado

## Vendor Bills

For vendor bills:
1. Create bill as usual
2. Enter vendor's timbrado information if required
3. System validates format and structure

## Reports and Monitoring

### Timbrado Usage Report

Monitor timbrado usage:
1. Go to **Accounting > Reporting > Timbrado Report**
2. View:
   - Numbers used
   - Numbers remaining
   - Expiration status
   - Document count

### Fiscal Period Closing

When closing fiscal periods:
1. Verify all timbrados for the period are valid
2. Check document number sequences are complete
3. Generate required fiscal reports

## Common Scenarios

### Scenario 1: Starting a New Establishment

1. Create new timbrado with new establishment code
2. Create or update journal with new establishment
3. Link timbrado to journal
4. Start issuing documents

### Scenario 2: Renewing Expired Timbrado

1. Obtain new authorization from SET
2. Create new timbrado record
3. Set start date (can overlap with old one)
4. Switch journal to new timbrado
5. Old timbrado remains for historical reference

### Scenario 3: Multiple Points of Sale

1. Create timbrado for each point of sale
2. Create separate journal for each
3. Each journal uses its own timbrado
4. Users select appropriate journal when creating documents

## Troubleshooting

### Error: "Timbrado Expired"

Solution:
1. Create new timbrado
2. Update journal configuration
3. Try creating document again

### Error: "Document Number Out of Range"

Solution:
1. Request new timbrado from SET with higher range
2. Create new timbrado record
3. Switch journal to new timbrado

### Warning: "Timbrado Expiring Soon"

Action:
1. Request renewal from SET
2. Create new timbrado in system
3. Plan transition date
4. Update journal when ready

