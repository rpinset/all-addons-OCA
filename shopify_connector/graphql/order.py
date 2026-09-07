"""Shopify Admin GraphQL documents for order lifecycle imports."""

from __future__ import annotations

from datetime import date, datetime

MONEY_FIELDS = """
    shopMoney { amount currencyCode }
    presentmentMoney { amount currencyCode }
"""

ORDER_FIELDS = f"""
    id
    name
    orderNumber
    createdAt
    updatedAt
    cancelledAt
    displayFinancialStatus
    displayFulfillmentStatus
    sourceName
    sourceIdentifier
    retailLocation {{ id name }}
    totalCashRoundingAdjustment {{
      paymentSet {{ {MONEY_FIELDS} }}
      refundSet {{ {MONEY_FIELDS} }}
    }}
    taxesIncluded
    note
    tags
    currencyCode
    presentmentCurrencyCode
    customer {{ id }}
    shippingAddress {{ countryCodeV2 }}
    billingAddress {{ countryCodeV2 }}
    discountCodes
    currentSubtotalPriceSet {{ {MONEY_FIELDS} }}
    currentTotalDiscountsSet {{ {MONEY_FIELDS} }}
    currentShippingPriceSet {{ {MONEY_FIELDS} }}
    currentTotalTaxSet {{ {MONEY_FIELDS} }}
    currentTotalPriceSet {{ {MONEY_FIELDS} }}
    risk {{
      assessments {{ riskLevel }}
      recommendation
    }}
    lineItems(first: 250) {{
      nodes {{
        id
        name
        sku
        quantity
        currentQuantity
        refundableQuantity
        isGiftCard
        variant {{ id sku }}
        product {{ id isGiftCard }}
        originalUnitPriceSet {{ {MONEY_FIELDS} }}
        discountedUnitPriceAfterAllDiscountsSet {{ {MONEY_FIELDS} }}
        discountedTotalSet {{ {MONEY_FIELDS} }}
        discountAllocations {{
          allocatedAmountSet {{ {MONEY_FIELDS} }}
          discountApplication {{
            ... on DiscountCodeApplication {{ code targetType }}
            ... on ManualDiscountApplication {{ title targetType }}
            ... on AutomaticDiscountApplication {{ title targetType }}
          }}
        }}
        taxLines {{
          title
          rate
          priceSet {{ {MONEY_FIELDS} }}
        }}
      }}
    }}
    shippingLines(first: 100) {{
      nodes {{
        id
        title
        code
        originalPriceSet {{ {MONEY_FIELDS} }}
        currentDiscountedPriceSet {{ {MONEY_FIELDS} }}
        taxLines {{
          title
          rate
          priceSet {{ {MONEY_FIELDS} }}
        }}
      }}
    }}
    transactions(first: 100) {{
      id
      gateway
      formattedGateway
      kind
      status
      processedAt
      amountSet {{ {MONEY_FIELDS} }}
    }}
    refunds {{ id }}
    returns(first: 100) {{
      nodes {{ id }}
    }}
"""

ORDER_BY_ID_QUERY = (
    "query ShopifyOrder($id: ID!) { order(id: $id) {" + ORDER_FIELDS + "} }"
)

REFUND_BY_ID_QUERY = f"""
query ShopifyRefund($id: ID!) {{
  refund(id: $id) {{
    id
    createdAt
    note
    totalRefundedSet {{ {MONEY_FIELDS} }}
    refundLineItems(first: 250) {{
      nodes {{
        id
        quantity
        restockType
        subtotalSet {{ {MONEY_FIELDS} }}
        totalTaxSet {{ {MONEY_FIELDS} }}
        lineItem {{ id }}
      }}
    }}
    refundShippingLines(first: 100) {{
      nodes {{
        id
        subtotalAmountSet {{ {MONEY_FIELDS} }}
      }}
    }}
    orderAdjustments(first: 100) {{
      nodes {{
        id
        reason
        amountSet {{ {MONEY_FIELDS} }}
        taxAmountSet {{ {MONEY_FIELDS} }}
      }}
    }}
    transactions(first: 100) {{
      nodes {{
        id
        gateway
        kind
        status
        processedAt
        amountSet {{ {MONEY_FIELDS} }}
      }}
    }}
  }}
}}
"""

RETURN_BY_ID_QUERY = """
query ShopifyReturn($id: ID!) {
  return(id: $id) {
    id
    name
    status
    createdAt
    closedAt
    totalQuantity
    returnLineItems(first: 250) {
      nodes {
        ... on ReturnLineItem {
          id
          quantity
          refundableQuantity
          refundedQuantity
          returnReasonNote
          fulfillmentLineItem { lineItem { id } }
        }
      }
    }
    exchangeLineItems(first: 250, includeRemovedItems: true) {
      nodes {
        id
        quantity
        variantId
        lineItem { id }
      }
    }
  }
}
"""


def _search_date(value: date | datetime | str | None) -> str:
    if not value:
        return ""
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value)[:10]


def orders_bulk_query(
    date_from: date | datetime | str | None = None,
    date_to: date | datetime | str | None = None,
) -> str:
    """Build a bulk query with an explicit, safely formatted date range."""
    terms = []
    if date_from:
        terms.append(f"created_at:>={_search_date(date_from)}")
    if date_to:
        terms.append(f"created_at:<={_search_date(date_to)}")
    search = " ".join(terms)
    root = f'orders(query: "{search}")' if search else "orders"
    return "{ " + root + " { edges { node { id name updatedAt } } } }"


DRAFT_ORDER_FIELDS = f"""
    id
    name
    status
    createdAt
    updatedAt
    completedAt
    note2
    tags
    taxesIncluded
    currencyCode
    presentmentCurrencyCode
    customer {{ id }}
    shippingAddress {{ countryCodeV2 }}
    billingAddress {{ countryCodeV2 }}
    order {{ id }}
    discountCodes
    subtotalPriceSet {{ {MONEY_FIELDS} }}
    totalDiscountsSet {{ {MONEY_FIELDS} }}
    totalShippingPriceSet {{ {MONEY_FIELDS} }}
    totalTaxSet {{ {MONEY_FIELDS} }}
    totalPriceSet {{ {MONEY_FIELDS} }}
    lineItems(first: 250) {{
      nodes {{
        id
        name
        sku
        quantity
        variant {{ id }}
        product {{ id }}
        originalUnitPriceSet {{ {MONEY_FIELDS} }}
        discountedTotalSet {{ {MONEY_FIELDS} }}
        taxLines {{
          title
          rate
          priceSet {{ {MONEY_FIELDS} }}
        }}
      }}
    }}
    shippingLine {{
      id
      title
      code
      originalPriceSet {{ {MONEY_FIELDS} }}
      discountedPriceSet {{ {MONEY_FIELDS} }}
      taxLines {{
        title
        rate
        priceSet {{ {MONEY_FIELDS} }}
      }}
    }}
"""

DRAFT_ORDERS_QUERY = (
    "query ShopifyDraftOrders($after: String, $query: String) {"
    " draftOrders(first: 100, after: $after, query: $query) {"
    " nodes {" + DRAFT_ORDER_FIELDS + "} pageInfo { hasNextPage endCursor } } }"
)

DRAFT_ORDER_BY_ID_QUERY = (
    "query ShopifyDraftOrder($id: ID!) { draftOrder(id: $id) {"
    + DRAFT_ORDER_FIELDS
    + "} }"
)

__all__ = [
    "DRAFT_ORDER_BY_ID_QUERY",
    "DRAFT_ORDERS_QUERY",
    "ORDER_BY_ID_QUERY",
    "REFUND_BY_ID_QUERY",
    "RETURN_BY_ID_QUERY",
    "orders_bulk_query",
]
