# Usage

## Sending Electronic Invoices

### Method 1: Automatic Sending

If auto-send is enabled:
1. Create invoice as usual
2. Click **Confirm**
3. System automatically sends to EDI provider
4. Status updates to "Sent" when successful

### Method 2: Manual Sending

1. Create and confirm invoice
2. Click **Send EDI** button
3. Wizard appears - review information
4. Click **Send**
5. Wait for confirmation

### Document Status

Electronic invoices have these statuses:
- **Draft**: Not yet confirmed
- **To Send**: Confirmed, ready to send
- **Sending**: Being sent to provider
- **Sent**: Successfully sent
- **Approved**: Approved by SET
- **Rejected**: Rejected by SET
- **Cancelled**: Cancelled document
- **Error**: Error occurred

## Checking Document Status

### View Status

1. Open invoice
2. Check **EDI Status** field
3. View **EDI Information** tab for details

### Manual Status Update

To manually check status:
1. Open invoice
2. Click **Update EDI Status** button
3. System queries provider
4. Status and messages update

## Cancelling Electronic Documents

### Requirements
- Document must be approved by SET
- Within cancellation timeframe (per SET rules)
- Valid cancellation reason

### Process
1. Open approved invoice
2. Click **Cancel EDI** button
3. Select **Cancellation Reason**
4. Enter **Reason Details**
5. Click **Cancel Document**
6. System sends cancellation to SET

## Downloading Documents

### PDF Download
1. Open invoice
2. Click **Download EDI PDF** button
3. PDF opens/downloads
4. Contains KUDE QR code

### XML Download
1. Open invoice
2. Click **Download EDI XML** button
3. XML file downloads
4. Valid SET-compliant XML

## Credit and Debit Notes

### Creating Credit Note
1. From invoice, click **Add Credit Note**
2. Select reason
3. System creates note with EDI reference
4. Send to EDI as usual

### Creating Debit Note
1. From invoice, click **Add Debit Note**
2. Enter reason
3. System creates note with EDI reference
4. Send to EDI as usual

## Monitoring EDI Operations

### EDI Log

View all EDI operations:
1. Go to **Facturación Electrónica > EDI Logs**
2. Filter by:
   - Document
   - Status
   - Date
   - Error type

### Error Handling

When errors occur:
1. Check **EDI Logs** for details
2. Review error message
3. Fix issue (e.g., missing data)
4. Click **Retry** button
5. Document resends

## Printing KUDE

### Invoice with KUDE

When printing invoices:
1. Click **Print** on invoice
2. Select **KUDE Report**
3. Report includes:
   - QR code
   - CDC (Código de Control)
   - All fiscal information
   - SET-compliant format

### QR Code

The QR code contains:
- Document number
- RUC
- CDC
- Amounts
- Validation URL

Customers can scan to verify authenticity.

## Batch Operations

### Sending Multiple Documents

1. Go to invoice list view
2. Select multiple invoices
3. Click **Action > Send EDI**
4. System sends all selected documents
5. Check status individually

### Updating Multiple Statuses

1. Select documents
2. Click **Action > Update EDI Status**
3. System checks all selected documents

## Customer Portal

Customers can:
1. Access their invoices via portal
2. Download PDF with KUDE
3. Download XML if needed
4. View EDI status

## Reports and Analytics

### EDI Dashboard

View EDI metrics:
1. Go to **Facturación Electrónica > Dashboard**
2. See:
   - Documents sent today/week/month
   - Success rate
   - Pending documents
   - Errors

### Custom Reports

Create custom reports:
1. Use invoice filters
2. Filter by **EDI Status**
3. Group by status, date, customer
4. Export to Excel

## Troubleshooting Common Issues

### Issue: "Missing Customer Email"

Solution:
1. Add email to customer record
2. Retry sending

### Issue: "Invalid RUC"

Solution:
1. Verify customer RUC format
2. Check verification digit
3. Update customer record
4. Retry

### Issue: "Timbrado Expired"

Solution:
1. Update timbrado in journal
2. May need to cancel and recreate invoice

### Issue: "Connection Error"

Solution:
1. Check internet connection
2. Verify provider credentials
3. Check provider service status
4. Try again or enable contingency mode

## Best Practices

1. **Test First**: Use test environment before production
2. **Monitor Logs**: Regularly check EDI logs
3. **Keep Updated**: Update status of pending documents
4. **Backup**: Download and store PDF/XML copies
5. **Validate**: Ensure all fiscal data is complete before sending

