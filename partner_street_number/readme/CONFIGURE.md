To configure this module, you need to:

1. Go to the form of a country
2. Fill in the fields 'Parse Regex' and 'Format Expression'
3. 'Parse Regex' should contain [named groups](https://docs.python.org/3/library/re.html#index-18) with names `street_name`, `street_number`, `street_number2` that parses the split fields from the content of the ``street`` field
4. 'Format Expression' is an Odoo [template expression](https://www.odoo.com/documentation/16.0/applications/general/companies/email_template.html#dynamic-placeholders) that generates the content of the ``street`` field based on the split fields
5. You can fill in some string to test your expressions, first this string will be decomposed using 'Parse Regex', and then the parts will be joined together using 'Format Expression'. Ideally, that should yield the same value as you filled in
