# Roadmap

## Current Version: 16.0.1.0.0

This document outlines planned features and improvements for the Paraguay Electronic Invoicing module.

## Short Term (Next Release)

### Enhanced Validation
- [ ] More comprehensive RUC validation
- [ ] Automatic DV calculation for RUC
- [ ] Product code validation against SET catalog
- [ ] Real-time validation before sending

### Improved User Experience
- [ ] Better error messages with suggested fixes
- [ ] Inline EDI status on invoice form
- [ ] Dashboard with EDI statistics
- [ ] Bulk operations improvement

### Additional Reports
- [ ] Monthly EDI summary report
- [ ] Tax authority compliance report
- [ ] Document tracking report
- [ ] Error analysis report

## Medium Term (2-3 Releases)

### Additional Document Types
- [ ] Comprobante de Retención (Retention receipt)
- [ ] Factura de Exportación (Export invoice)
- [ ] Factura de Importación (Import invoice)
- [ ] Boleta de Venta (Sales receipt)

### Integration Enhancements
- [ ] Direct SIFEN integration (bypass third-party)
- [ ] Webhook support for status updates
- [ ] Batch sending optimization
- [ ] Offline mode improvements

### Advanced Features
- [ ] Electronic credit management
- [ ] Payment integration with electronic documents
- [ ] Multi-currency support for EDI
- [ ] Document routing rules

### Compliance Updates
- [ ] Support for SET regulation changes
- [ ] Enhanced contingency mode
- [ ] Document versioning
- [ ] Legal archive management (7-year retention)

## Long Term (Future Vision)

### AI and Automation
- [ ] Intelligent error detection and correction
- [ ] Automatic document classification
- [ ] Predictive timbrado expiration alerts
- [ ] Smart retry strategies

### Integration Ecosystem
- [ ] Point of Sale (POS) integration
- [ ] E-commerce integration
- [ ] Accounting software exports
- [ ] Bank reconciliation integration

### Analytics and Intelligence
- [ ] Advanced EDI analytics
- [ ] Customer behavior insights
- [ ] Tax optimization suggestions
- [ ] Compliance scoring

### Mobile Support
- [ ] Mobile app for document approval
- [ ] QR code scanning verification
- [ ] Mobile notifications
- [ ] Offline mobile capabilities

### Additional Providers
- [ ] Additional EDI provider integrations
- [ ] Provider comparison tools
- [ ] Automatic failover between providers
- [ ] Cost optimization across providers

## Technical Improvements

### Performance
- [ ] Asynchronous document sending
- [ ] Caching layer for provider responses
- [ ] Database query optimization
- [ ] Bulk operation performance

### Code Quality
- [ ] Increase test coverage to 90%+
- [ ] API documentation
- [ ] Developer guide
- [ ] Code refactoring for maintainability

### Security
- [ ] Enhanced credential encryption
- [ ] Audit trail improvements
- [ ] Role-based access control refinement
- [ ] Security compliance certifications

## Community Requests

We track community feature requests. Top requests:

1. **Multi-company enhancements** - Better support for groups
2. **Import automation** - Automatically import vendor electronic invoices
3. **API exposure** - REST API for external systems
4. **Customs integration** - Integration with customs systems
5. **Transportation documents** - Support for e-transport documents

## Contributing

Want to contribute to the roadmap?

1. Submit feature requests via GitHub issues
2. Vote on existing feature requests
3. Contribute code via pull requests
4. Join development discussions

## Version Planning

### v16.0.2.0.0 (Q2 2024)
- Enhanced validation
- Additional reports
- UX improvements

### v16.0.3.0.0 (Q3 2024)
- New document types
- Improved integrations
- Performance optimizations

### v17.0.1.0.0 (Q4 2024)
- Odoo 17 migration
- New features from roadmap
- Architecture improvements

## Deprecation Notices

### Planned Deprecations
- Legacy provider adapters will be deprecated in v17.0
- Old XML format support ends in v16.0.5.0.0
- Python 3.7 support ends with v16.0 series

### Migration Paths
Documentation will be provided for all deprecations with clear migration paths and timelines.

## Feedback

This roadmap is subject to change based on:
- SET regulatory changes
- Community feedback
- Technical constraints
- Resource availability

Submit feedback:
- GitHub issues
- Community forums
- Direct contact with maintainers

---

Last updated: 2024

