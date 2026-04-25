Generate Portuguese tax authority legal transport documents ("Guias de
Transporte") using InvoiceXpress.

The InvoiceXpress document is automatically generated when an ougoing
Transfer or Delivery Order is validated.

This feature depends on the InvoiceXpress Invoice generation feature.
See
<https://github.com/OCA/l10n-portugal/blob/14.0/l10n_pt_account_invoicexpress/README.rst>
for more details.


**Update March/2026:**

- Can set a specific loading date on the Picking Document.
  For example, to allow preparing transport document on the day before.
- Can re-create the transport document after confirming the Picking.
  For example, to create a new document for the same shipment if the 
  original one ended not happening and its dates are obsolete.
- Use the pikcing line description on the transport document.
- Option to include UoM in line descriptions, configured on the Operation Type.

**UPDATE November/2021:**

Deliveries:

- Added support to the different document types, Transport ("Guia de
  Transporte") and Shipment ("Guia de Remessa"). The default document
  type is set on the Operation Type.
- Changed the line description to be the Product name, instead of the
  original Sales Order description, so that it uses the most up to date
  product description.
- Added tax details to the document lines.
