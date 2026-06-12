To use this module:

1. Go to **Settings > Technical > Email > Templates**.
2. Open or create a mail template.
3. In the **Apply on** field (Settings tab), set the domain that records must
   match for this template to appear in the composer
   (e.g. `[('is_company', '=', True)]` to show the template only on contacts
   where **Is a Company** is set).
4. Leave **Apply on** empty to keep the template available for all records of
   the model (default behaviour).

When a user opens the email composer from a record, only templates whose
**Apply on** domain matches that record will be listed in the *Load template*
dropdown.
