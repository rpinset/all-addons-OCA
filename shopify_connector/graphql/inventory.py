"""GraphQL documents for inventory synchronization."""

LOCATIONS_QUERY = """
query ShopifyLocations($after: String) {
  locations(first: 100, after: $after, includeInactive: true) {
    nodes {
      id
      legacyResourceId
      name
      isActive
      fulfillsOnlineOrders
      address {
        address1
        address2
        city
        provinceCode
        zip
        countryCode
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

INVENTORY_LEVEL_QUERY = """
query InventoryLevelForItem($inventoryItemId: ID!, $locationId: ID!) {
  inventoryItem(id: $inventoryItemId) {
    id
    tracked
    inventoryLevel(locationId: $locationId, includeInactive: true) {
      id
      isActive
      quantities(names: ["available"]) {
        name
        quantity
      }
    }
  }
}
"""

INVENTORY_LEVELS_BULK_QUERY = """
{
  inventoryItems {
    edges {
      node {
        id
        tracked
        inventoryLevels {
          edges {
            node {
              id
              isActive
              location {
                id
              }
              quantities(names: ["available"]) {
                name
                quantity
              }
            }
          }
        }
      }
    }
  }
}
"""

INVENTORY_SET_QUANTITIES_MUTATION = """
mutation InventorySetQuantities($input: InventorySetQuantitiesInput!) {
  inventorySetQuantities(input: $input) {
    inventoryAdjustmentGroup {
      createdAt
      reason
      referenceDocumentUri
      changes {
        name
        delta
      }
    }
    userErrors {
      code
      field
      message
    }
  }
}
"""
