"""Shopify Payments GraphQL documents for API version 2026-01."""

MONEY_FIELDS = "amount currencyCode"

SHOPIFY_PAYMENTS_PAYOUTS_QUERY = f"""
query ShopifyPaymentsPayouts($first: Int!, $after: String, $query: String) {{
  shopifyPaymentsAccount {{
    id
    activated
    defaultCurrency
    payouts(
      first: $first
      after: $after
      query: $query
      sortKey: ISSUED_AT
    ) {{
      pageInfo {{ hasNextPage endCursor }}
      nodes {{
        id
        legacyResourceId
        externalTraceId
        issuedAt
        status
        transactionType
        net {{ {MONEY_FIELDS} }}
        summary {{
          adjustmentsFee {{ {MONEY_FIELDS} }}
          adjustmentsGross {{ {MONEY_FIELDS} }}
          advanceFees {{ {MONEY_FIELDS} }}
          advanceGross {{ {MONEY_FIELDS} }}
          chargesFee {{ {MONEY_FIELDS} }}
          chargesGross {{ {MONEY_FIELDS} }}
          refundsFee {{ {MONEY_FIELDS} }}
          refundsFeeGross {{ {MONEY_FIELDS} }}
          reservedFundsFee {{ {MONEY_FIELDS} }}
          reservedFundsGross {{ {MONEY_FIELDS} }}
          retriedPayoutsFee {{ {MONEY_FIELDS} }}
          retriedPayoutsGross {{ {MONEY_FIELDS} }}
          usdcRebateCreditAmount {{ {MONEY_FIELDS} }}
        }}
      }}
    }}
  }}
}}
"""

SHOPIFY_PAYMENTS_TRANSACTIONS_QUERY = f"""
query ShopifyPaymentsTransactions(
  $first: Int!
  $after: String
  $query: String!
) {{
  shopifyPaymentsAccount {{
    balanceTransactions(first: $first, after: $after, query: $query) {{
      pageInfo {{ hasNextPage endCursor }}
      nodes {{
        id
        type
        displayType
        sourceType
        sourceId
        sourceOrderTransactionId
        transactionDate
        test
        adjustmentReason
        amount {{ {MONEY_FIELDS} }}
        fee {{ {MONEY_FIELDS} }}
        net {{ {MONEY_FIELDS} }}
        associatedOrder {{ id name }}
        associatedPayout {{ id status }}
      }}
    }}
  }}
}}
"""

SHOPIFY_PAYMENTS_DISPUTES_QUERY = f"""
query ShopifyPaymentsDisputes(
  $first: Int!
  $after: String
  $query: String
) {{
  shopifyPaymentsAccount {{
    disputes(first: $first, after: $after, query: $query) {{
      pageInfo {{ hasNextPage endCursor }}
      nodes {{
        id
        initiatedAt
        evidenceDueBy
        evidenceSentOn
        finalizedOn
        status
        type
        amount {{ {MONEY_FIELDS} }}
        order {{ id name }}
        reasonDetails {{ reason networkReasonCode }}
      }}
    }}
  }}
}}
"""
