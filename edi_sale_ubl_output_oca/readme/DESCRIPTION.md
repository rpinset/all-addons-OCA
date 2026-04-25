Provides some basic templates for generating order responses in UBL format within the EDI framework.

## Templates

``qweb_tmpl_ubl_party``: to be used to render a party (res.partner)
``qweb_tmpl_ubl_address``: to be used to render a party's address (aka res.partner)
``qwb_tmpl_ubl_order_response_out``: example for a full ORDRSP output. 

NOTE: the latter is not fully complete and above all should not be used directly to avoid overrides. Always define your own template for the customer.
