To use this module, you need to:

1. Go to Commissions > Configuration > Commission Types.
2. Create or open a Commission Type with type = "Product criteria".
3. Open or create a rule, appart from the "Apply On" field, you can fill the "Customer Country" to filter whose customers this rule will be applied to. If the field is empty, it will be applied to all customers.
4. The rules will be sorted according to his priority, rules with countries are more prioritary than rules without it.

When selling or invoicing to a customer, Odoo will query the commission rules, filtering by the country of the customer if set. Before that, odoo will apply the first commission rule found, as it is done in the sale_commission_product_criteria module.
