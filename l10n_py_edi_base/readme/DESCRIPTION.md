# Paraguay - Electronic Invoicing Base

This module provides the base functionality for electronic invoicing (facturación electrónica) in Paraguay, compliant with SET (Subsecretaría de Estado de Tributación) requirements.

## Features

### Document Types Support
- **Factura Electrónica**: Electronic invoice
- **Nota de Crédito Electrónica**: Electronic credit note
- **Nota de Débito Electrónica**: Electronic debit note
- **Nota de Remisión Electrónica**: Electronic delivery note
- **Autofactura Electrónica**: Electronic self-invoice

### Core Functionality
- **Data Models**: Complete models for electronic documents
- **Field Extensions**: Enhanced account.move, res.partner, and res.company
- **Fiscal Validation**: RUC and DV validation
- **JSON Builder**: Automatic generation of JSON for SIFEN
- **QR Code Generation**: Ready for KUDE (Código Único de Documento Electrónico)
- **Log System**: Complete audit trail of EDI operations

### Compliance
- **SIFEN Compatible**: Sistema Integrado de Facturación Electrónica Nacional
- **SET Requirements**: Meets all SET regulatory requirements
- **Contingency Mode**: Support for offline operation
- **KUDE Support**: Ready for electronic document codes

### Integration Ready
This is a base module that requires a connector:
- `l10n_py_edi_factpy`: FactPy integration
- `l10n_py_edi_facturasend`: FacturaSend integration

## Technical Architecture

- **Provider-agnostic**: Works with multiple EDI providers
- **Extensible**: Easy to add new document types
- **Robust**: Error handling and retry mechanisms
- **Auditable**: Complete logging of all operations

## Dependencies

- `account`: Core accounting
- `l10n_py_base`: Base Paraguayan localization
- `l10n_py_account`: Accounting extensions (timbrado management)
- `product`: Product management
- `sale`: Sales management

