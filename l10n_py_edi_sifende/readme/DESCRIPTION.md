[Sifende](https://sifende.com.py) connector for Paraguay electronic invoicing.

It registers Sifende as a provider in `l10n_py_edi_base`. Odoo still numbers the invoices
and builds the document data; Sifende signs the XML, sends it to SIFEN and returns the result
and the KuDE. Odoo needs no certificate, CSC or `sifen` library.

Supported documents: invoice (FE), credit note (NCE), debit note (NDE), delivery note (NRE)
and self-invoice (AFE).

Sending is asynchronous. After sending, the document is *Processing* with its CDC and QR.
Sifende notifies Odoo through a webhook when SIFEN answers, and a cron that polls every
5 minutes acts as a fallback. When SIFEN approves, the document becomes *Accepted* with the
signed XML and the KuDE attached.

Every hour the cron also polls the accepted documents that are still within their
cancellation window, in case they were cancelled in Sifende and the notification was lost.
Each run polls up to 200 documents per connector. Documents still waiting for SIFEN or for
their files go first; the accepted documents under watch take the room that is left. Within
each group the ones polled longest ago go first across all companies, so no company is left
without its turn. A poll that does not change the document's state is not written to the EDI
log; failed polls and state changes are.
