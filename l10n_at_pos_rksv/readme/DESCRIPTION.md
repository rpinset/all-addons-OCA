This module integrates the Austrian RKSV (*Registrierkassensicherheitsverordnung*)
signing flow into the Odoo Point of Sale.

It uses the [a.sign RK](https://www.a-trust.at/de/asignrk/) online service of
A-Trust to sign every receipt with a chained AES-encrypted turnover counter,
producing the QR code, DEP entry and zero/start receipts required by the
Austrian fiscal authority.
