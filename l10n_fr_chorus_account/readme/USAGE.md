On the customer form view of a French public administration, in the
*Accounting* tab, set the *Customer Invoice Transmission Method* to
*Chorus Pro*. You will then see a new section *Chorus Pro*. In this
section, you should set the *Info required for Chorus* and, if the
administration is *Service required*, you must create the Chorus
services.

If you enabled the Chorus API, just click on the button *Update Info
Required for Chorus* and it will set the field *Info required for
Chorus* and download all the Chorus services of that administration.

When you try to validate a customer invoice/refund for a customer for
which you send the invoices via Chorus Pro, it will check the value of
the field *Info required for Chorus* and check that this invoice has an
order reference or/and a Chorus service if required for that customer.

If you enabled the Chorus API, you should see a button *Send to Chorus*
on validated customer invoices and refunds that have a transmission
method set to *Chorus Pro*. You can also select several customer
invoices/refunds and do *Action \> Send to Chorus Pro*.

Sending an invoice via the Chorus API creates a Chorus Flow, cf menu
*Accounting \> Configuration \> Chorus Pro \> Chorus Flows* (it is not
really a configuration thing... so we could argue that it should not be
in the configuration menu !). You can click on the button *Update Flow
Status* to refresh the status of the flow, until it reaches the status
*IN_INTEGRE*. Then, click on the button *Get Chorus Invoice Identifiers*
to get the technical identifiers of the invoice in Chorus (and write it
on the invoice in Odoo) and get the status of the invoice in Chorus.
Eventually, on the invoice, you can click on the button *Update Chorus
Invoice Status* to refresh the *Chorus Invoice Status*. All these
actions to refresh the status of the Chorus flows and of the invoice are
automated via the *Scheduled Action* named *Chorus Pro Invoice Status
Update*. So, if that scheduled action is active, you should not have to
manually perform the actions described in this paragraph.

In the list view of customer invoices, you can group by *Chorus Status*:
that way, you get on overview of the status of all the invoices you sent
to Chorus Pro, and you can easily spot if an invoice has been refused
for example.
