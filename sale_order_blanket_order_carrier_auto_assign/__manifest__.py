{
    "name": "Sale Order Blanket Order — Carrier Auto Assign Compatibility",
    "summary": (
        "Glue between sale_order_blanket_order and sale_order_carrier_auto_assign: "
        "keep auto-assigned carrier (delivery-fee) lines out of blanket-order "
        "call-off matching so they cannot consume blanket call-off capacity."
    ),
    "version": "18.0.1.0.1",
    "license": "AGPL-3",
    "author": "Camptocamp, BCIM, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-blanket",
    "depends": ["sale_order_blanket_order", "sale_order_carrier_auto_assign"],
    "auto_install": True,
    "installable": True,
}
