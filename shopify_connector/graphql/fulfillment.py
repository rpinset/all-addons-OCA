"""Shopify Admin GraphQL documents for fulfillment synchronization."""

FULFILLMENT_ORDER_FIELDS = """
    id
    status
    requestStatus
    assignedLocation {
      location { id name }
    }
    supportedActions { action }
    fulfillmentHolds {
      id
      reason
      reasonNotes
      heldByRequestingApp
    }
    lineItems(first: 250) {
      nodes {
        id
        totalQuantity
        remainingQuantity
        lineItem { id }
      }
    }
"""

ORDER_FULFILLMENT_ORDERS_QUERY = (
    "query ShopifyOrderFulfillmentOrders($id: ID!) {"
    " order(id: $id) { id fulfillmentOrders(first: 250) { nodes {"
    + FULFILLMENT_ORDER_FIELDS
    + "} } } }"
)

FULFILLMENT_BY_ID_QUERY = """
query ShopifyFulfillment($id: ID!) {
  fulfillment(id: $id) {
    id
    name
    status
    createdAt
    updatedAt
    order { id }
    location { id }
    fulfillmentOrders(first: 250) {
      nodes { id }
    }
    trackingInfo {
      company
      number
      url
    }
    fulfillmentLineItems(first: 250) {
      nodes {
        id
        quantity
        lineItem { id }
      }
    }
  }
}
"""

FULFILLMENT_CREATE_MUTATION = """
mutation ShopifyFulfillmentCreate($fulfillment: FulfillmentInput!) {
  fulfillmentCreate(fulfillment: $fulfillment) {
    fulfillment {
      id
      name
      status
      createdAt
      updatedAt
      location { id }
      trackingInfo {
        company
        number
        url
      }
    }
    userErrors {
      field
      message
    }
  }
}
"""

FULFILLMENT_ORDER_MOVE_MUTATION = """
mutation ShopifyFulfillmentOrderMove($id: ID!, $newLocationId: ID!) {
  fulfillmentOrderMove(id: $id, newLocationId: $newLocationId) {
    movedFulfillmentOrder {
      id
      status
      requestStatus
    }
    originalFulfillmentOrder {
      id
      status
      requestStatus
    }
    remainingFulfillmentOrder {
      id
      status
      requestStatus
    }
    userErrors {
      field
      message
    }
  }
}
"""

FULFILLMENT_ORDER_RELEASE_HOLD_MUTATION = """
mutation ShopifyFulfillmentOrderReleaseHold($id: ID!, $holdIds: [ID!]) {
  fulfillmentOrderReleaseHold(id: $id, holdIds: $holdIds) {
    fulfillmentOrder {
      id
      status
      requestStatus
    }
    userErrors {
      field
      message
    }
  }
}
"""

FULFILLMENT_CANCEL_MUTATION = """
mutation ShopifyFulfillmentCancel($id: ID!) {
  fulfillmentCancel(id: $id) {
    fulfillment {
      id
      status
    }
    userErrors {
      field
      message
    }
  }
}
"""
