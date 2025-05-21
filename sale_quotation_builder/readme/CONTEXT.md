After this PR (https://github.com/odoo/odoo/pull/133773), Odoo removed the `sale_quotation_builder` module and added a new one called `sale_pdf_quote_builder`.

Both features work fine, but there is no direct equivalence between them. For new customers, it's okay to use the new module to upload PDF documents. However, customers upgrading from older versions may want to keep the old behavior.

This module restores those features.