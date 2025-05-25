This module add multi-company management to mail templates.

This module also adds a fallback mechanism for templates that are hardcoded using their XMLID.
For example: the `sale` module will propose the template `sale.mail_template_sale_confirmation` when an order is confirmed.

If the template is not found due to access rules (for instance because it has been linked to another company), nothing is found.
With this module, the field "Original XMLID template" can be filled with the template that corresponds to `sale.mail_template_sale_confirmation` (that is done automatically if the template is copied).
With this configuration, the new template will be found.
