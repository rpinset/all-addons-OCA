To use this module, you need to:

1. Go to a partner
2. Set the partner's country to a country with the street name parse regex filled
3. Fill in a street name supported by the country's configuration
4. Observe that the fields `street_name`, `street_number` and `street_number2` are filled according to the country's configuration

For bulk updating partner fields (ie after you've changed the configuration of some country wrt street name parsing/formatting), use the ``Update partner street fields`` wizard, available for group ``Contact Creation``.

In case you always want to edit the street name components manually, activate setting `Use split fields for street name in partner form`.
