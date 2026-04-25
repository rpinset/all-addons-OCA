# Bulgarian Company Registry Integration

This module provides real-time integration with the official Bulgarian Trade
Registry API (portal.registryagency.bg) to automatically fetch and populate
company data.

## Key Features
- Real-time API integration with portal.registryagency.bg
- Search companies by EIK (Bulgarian company identification number)
- Automatically populate partner data including:
  - Company name (Bulgarian)
  - Complete structured address (city, street, postal code, district)
  - Legal form (ООД, ЕООД, АД, ЕТ, etc.)
  - Registration date and court
  - Economic activity (NACE/NKID code and description)
  - Company managers and representatives
  - Contact information (email, phone)
- Smart address parsing supporting Bulgarian formats:
  - Streets (ул.) and boulevards (бул.)
  - Residential complexes (ж.к.)
  - Resort complexes (к.к.)
  - Localities (м.) and quarters (кв.)
  - With district information (р-н)
  - Email and phone extraction from addresses
- No offline database needed - always fresh data
- Works with l10n_bg_config module for EIK/UIC validation
