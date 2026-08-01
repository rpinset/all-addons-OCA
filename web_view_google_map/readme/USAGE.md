## Google Map view

Add a `google_map` view on any model that stores latitude/longitude:

```xml
<record id="view_partner_google_map" model="ir.ui.view">
    <field name="name">res.partner.google_map</field>
    <field name="model">res.partner</field>
    <field name="arch" type="xml">
        <google_map
            string="Map"
            lat="partner_latitude"
            lng="partner_longitude"
            colors="blue:company_type=='person';green:company_type=='company';"
        >
            <field name="partner_latitude" />
            <field name="partner_longitude" />
            <field name="display_name" />
            <field name="company_type" />
        </google_map>
    </field>
</record>
```

Include `google_map` in the action `view_mode`, for example
`list,form,google_map`.

Contacts already expose a Google Map mode on the partner action.

## Places widgets

```xml
<field
    name="street"
    widget="gplaces_address_form"
    options="{'lat': 'partner_latitude', 'lng': 'partner_longitude'}"
/>
<field
    name="name"
    widget="gplaces_autocomplete"
    options="{'lat': 'partner_latitude', 'lng': 'partner_longitude'}"
/>
```
