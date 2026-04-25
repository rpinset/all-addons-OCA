> [!WARNING]
> Backport from Odoo work in progress in
> https://github.com/odoo/odoo/pull/196102
>
> Can have changes without notice.
> Should be removed once the upstream WIP is merged.


This commit implements many requirements for Portugal:

Hash
----
Sale journals should be hashed. For this, the following fields are used:
`date`, `l10n_pt_hashed_on`, `name`, `amount_total` as well as the hash
of the previous `account.move`. These are sent to IAP, where we'll use
a private key (belonging to Odoo) to sign the documents.
To avoid too many RPC calls to IAP, the documents are signed only when
sent&printed, or manually when clicking on the 'Lock' button. At that
point, moves are batched such that we have only once RPC call to IAP.

AT Series
---------
This is a new model. It represents a mapping between the Odoo series
(e.g. INV2024), and the series from the Autoridade Tributaria (AT).
The user has to manually create these on the government portal.
The series given by the government is unique across all accounting
softwares. It will be useful for the ATCUD and QR code below. They are
available from the Accounting Settings.

ATCUD
-----
The ATCUD code is a unique code that represents a unique document in
Portugal. It's the simple concatenation of the AT series and the
sequence number within that series. It must be displayed on the
document whenever it is signed.

QR Code
-------
A QR code must also be displayed on any signed document. This QR code
contains several info such as the customer VAT (if any), the total
amount of the document, or the tax totals.

Misc requirements
-----------------

- if a product is exempted from VAT, we must mention why choosing
one of the predefined categories. This is a new field on `account.tax`

- we cannot change tax number of an existing client with already issued
documents. However, missing tax number can only be entered if the field
is empty (or filled with generic client tax 999999990)

- do not allow change the name of client (if it already has issued docs)
who has no tax number. Limitation ends when client has a tax number.

- do not allow change ProductDescription if already issued docs

Layout requirements
-------------------

- Documents that are not invoices must indicate
"Este documento não serve de fatura"

- Signed documents must indicate
"E.g.: HASH - Processado por programa certificado n.º 0000/AT"
where HASH is the 1st, 11th, 21st, 31st chars of the hash/signature.

- Non-signed documents that are invoices must indicate
"Emitido por programa certificado n.º 0000/AT"

- Each page must contain: the document name, page number, total number
of pages, and the accumulated amount for that page. The latter
requirement is not possible with wkhtmltopdf as we don't know in
advance of many pages the pdf version will have, so we cannot calculate
the sub amount for each page. For this reason, we add an accumulated
amount column only if we are in a pdf version, and that we have more
than 5 invoice lines (i.g. when we might have more than one page).

Training mode
-------------
A boolean field is present on the `res.company` model. If it's activated
documents should have the mention "Documento emitido para fins de
Formação". And indicate in the header the data identifying the software
developer company (Odoo) instead of the customer’s company.

Links
-----
- https://info.portaldasfinancas.gov.pt/pt/docs/Portug_tax_system/Documents/Order_No_8632_2014_of_the_3rd_July.pdf
- https://info.portaldasfinancas.gov.pt/pt/docs/Portug_tax_system/Documents/Ordinance_363_2010_Certification_of_computer_invoicing_programs.pdf
- https://info.portaldasfinancas.gov.pt/pt/docs/Conteudos_1pagina/Documents/QR_Code_Technical_Specifications.pdf

