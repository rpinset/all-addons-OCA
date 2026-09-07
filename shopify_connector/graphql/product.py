"""GraphQL documents for product and collection synchronization."""

PRODUCTS_BULK_QUERY = """
{
  products {
    edges {
      node {
        id
        title
        descriptionHtml
        handle
        status
        updatedAt
        options {
          id
          name
          position
          optionValues {
            id
            name
          }
        }
        variants {
          edges {
            node {
              id
              title
              sku
              barcode
              price
              updatedAt
              inventoryItem {
                id
                tracked
              }
              selectedOptions {
                name
                value
              }
              media {
                edges {
                  node {
                    id
                  }
                }
              }
            }
          }
        }
        media {
          edges {
            node {
              id
              alt
              mediaContentType
              ... on MediaImage {
                image {
                  url
                }
              }
            }
          }
        }
        collections {
          edges {
            node {
              id
              title
              handle
              updatedAt
              ruleSet {
                appliedDisjunctively
              }
            }
          }
        }
      }
    }
  }
}
"""

PRODUCT_BY_ID_QUERY = """
query ProductById(
  $id: ID!
  $variantsAfter: String
  $mediaAfter: String
  $collectionsAfter: String
) {
  product(id: $id) {
    id
    title
    descriptionHtml
    handle
    status
    updatedAt
    options {
      id
      name
      position
      optionValues {
        id
        name
      }
    }
    variants(first: 100, after: $variantsAfter) {
      nodes {
        id
        title
        sku
        barcode
        price
        updatedAt
        inventoryItem {
          id
          tracked
        }
        selectedOptions {
          name
          value
        }
        media(first: 100) {
          nodes {
            id
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
    media(first: 100, after: $mediaAfter) {
      nodes {
        id
        alt
        mediaContentType
        ... on MediaImage {
          image {
            url
          }
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
    collections(first: 100, after: $collectionsAfter) {
      nodes {
        id
        title
        handle
        updatedAt
        ruleSet {
          appliedDisjunctively
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
"""

PRODUCT_VARIANT_MEDIA_QUERY = """
query ProductVariantMedia($id: ID!, $after: String) {
  productVariant(id: $id) {
    media(first: 100, after: $after) {
      nodes {
        id
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
"""

PRODUCTS_PAGE_QUERY = """
query ProductsPage($after: String) {
  products(first: 50, after: $after) {
    nodes {
      id
      title
      handle
      status
      updatedAt
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

COLLECTIONS_PAGE_QUERY = """
query CollectionsPage($after: String) {
  collections(first: 100, after: $after) {
    nodes {
      id
      title
      handle
      updatedAt
      ruleSet {
        appliedDisjunctively
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

PRODUCT_CUSTOM_ID_DEFINITION_QUERY = """
query ProductCustomIdDefinition(
  $identifier: MetafieldDefinitionIdentifierInput!
) {
  metafieldDefinition(identifier: $identifier) {
    id
  }
}
"""

PRODUCT_CUSTOM_ID_DEFINITION_CREATE = """
mutation CreateProductCustomIdDefinition(
  $definition: MetafieldDefinitionInput!
) {
  metafieldDefinitionCreate(definition: $definition) {
    createdDefinition {
      id
    }
    userErrors {
      code
      field
      message
    }
  }
}
"""

PRODUCT_VARIANT_APPEND_MEDIA_MUTATION = """
mutation AppendProductVariantMedia(
  $productId: ID!
  $variantMedia: [ProductVariantAppendMediaInput!]!
) {
  productVariantAppendMedia(
    productId: $productId
    variantMedia: $variantMedia
  ) {
    product {
      id
    }
    userErrors {
      code
      field
      message
    }
  }
}
"""

PRODUCT_VARIANT_DETACH_MEDIA_MUTATION = """
mutation DetachProductVariantMedia(
  $productId: ID!
  $variantMedia: [ProductVariantDetachMediaInput!]!
) {
  productVariantDetachMedia(
    productId: $productId
    variantMedia: $variantMedia
  ) {
    product {
      id
    }
    userErrors {
      code
      field
      message
    }
  }
}
"""

PRODUCT_SET_MUTATION = """
mutation ProductSet(
  $identifier: ProductSetIdentifiers
  $input: ProductSetInput!
) {
  productSet(identifier: $identifier, input: $input, synchronous: true) {
    product {
      id
      title
      handle
      status
      updatedAt
      variants(first: 250) {
        nodes {
          id
          sku
          barcode
          price
          inventoryItem {
            id
            tracked
          }
          selectedOptions {
            name
            value
          }
        }
      }
      media(first: 250) {
        nodes {
          id
          alt
          mediaContentType
          ... on MediaImage {
            image {
              url
            }
          }
        }
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
