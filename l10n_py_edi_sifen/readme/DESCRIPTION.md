Direct SIFEN (Sistema Integrado de Facturación Electrónica Nacional) connector
for Paraguay electronic invoicing.

This module extends the generic EDI connector from `l10n_py_edi_base` to provide
direct transmission to SIFEN using the `pysifen` library, without intermediary
services like FactPy or FacturaSend.

Features:

- Direct SOAP/mTLS communication with SIFEN
- Digital signature via PKCS12 certificate
- RDe (Documento Electrónico) building from invoice data
- Support for FE, NCE, NDE, NRE, AFE document types
- Test and Production environment support
