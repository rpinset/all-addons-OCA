# EasyPay API
API_URL_TEST = "https://api.test.easypay.pt"
API_URL_PROD = "https://api.prod.easypay.pt"

# Map EasyPay API codes to Odoo payment method codes
# Only include codes that need translation; others use the payment.method code directly
EASYPAY_TO_ODOO = {
    "cc": "card",
    "mb": "multibanco",
    "mbw": "mbway",
}

# Reverse mapping for Odoo code -> EasyPay API code lookups
ODOO_TO_EASYPAY = {v: k for k, v in EASYPAY_TO_ODOO.items()}

# Payment types
PAYMENT_TYPE_SALE = "sale"

# Default payment method codes supported by EasyPay
DEFAULT_PAYMENT_METHOD_CODES = {
    "card",
    "multibanco",
    "mbway",
    "dd",
    "vi",
    "ap",
    "gp",
    "sw",
    "easypay",
}
