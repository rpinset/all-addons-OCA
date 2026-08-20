Generic UBL party/address qweb templates for use with the EDI framework
(`edi_exchange_template_oca`), split out of `edi_sale_ubl_output_oca` so
they can be reused (e.g. by purchase-side UBL output) without depending on
`sale`.

## Templates

- ``qweb_tmpl_ubl_party``: renders a `cac:Party` block (EndpointID,
  PartyIdentification, PartyName) from the `party` vals shape produced by
  `edi_party_data_oca`/`edi_exchange_template_party_data`'s `get_party_data()`.
- ``qweb_tmpl_ubl_address``: renders the contents of a postal address
  (StreetName/CityName/PostalZone/AddressLine/Country) from a `res.partner`.
