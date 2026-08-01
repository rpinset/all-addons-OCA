"""GraphQL documents for customer and Shopify Plus B2B synchronization."""

CUSTOMERS_BULK_QUERY = """
{
  customers {
    edges {
      node {
        id
        firstName
        lastName
        displayName
        email
        phone
        tags
        taxExempt
        updatedAt
        emailMarketingConsent {
          marketingState
          consentUpdatedAt
          marketingOptInLevel
        }
        defaultAddress {
          id
        }
        addressesV2 {
          edges {
            node {
              id
              firstName
              lastName
              company
              address1
              address2
              city
              province
              provinceCode
              country
              countryCodeV2
              zip
              phone
            }
          }
        }
      }
    }
  }
}
"""

CUSTOMER_BY_ID_QUERY = """
query CustomerById($id: ID!) {
  customer(id: $id) {
    id
    firstName
    lastName
    displayName
    email
    phone
    tags
    taxExempt
    updatedAt
    emailMarketingConsent {
      marketingState
      consentUpdatedAt
      marketingOptInLevel
    }
    defaultAddress {
      id
    }
    addressesV2(first: 250) {
      nodes {
        id
        firstName
        lastName
        company
        address1
        address2
        city
        province
        provinceCode
        country
        countryCodeV2
        zip
        phone
      }
    }
  }
}
"""

CUSTOMER_UPDATE_MUTATION = """
mutation CustomerUpdate($input: CustomerInput!) {
  customerUpdate(input: $input) {
    customer {
      id
      updatedAt
    }
    userErrors {
      field
      message
    }
  }
}
"""

COMPANIES_QUERY = """
query Companies($after: String) {
  companies(first: 50, after: $after) {
    nodes {
      id
      name
      externalId
      updatedAt
      locations(first: 100) {
        nodes {
          id
          name
          phone
          billingAddress {
            address1
            address2
            city
            province
            countryCode
            zip
          }
          shippingAddress {
            address1
            address2
            city
            province
            countryCode
            zip
          }
          roleAssignments(first: 100) {
            nodes {
              id
              role {
                id
                name
              }
              contact {
                id
                title
                customer {
                  id
                  displayName
                  email
                  phone
                }
              }
            }
          }
        }
      }
      contacts(first: 100) {
        nodes {
          id
          title
          customer {
            id
            displayName
            email
            phone
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

CATALOGS_QUERY = """
query Catalogs($after: String) {
  catalogs(first: 50, after: $after, type: COMPANY_LOCATION) {
    nodes {
      id
      title
      status
      priceList {
        id
        name
        currency
        prices(first: 250) {
          nodes {
            variant {
              id
            }
            price {
              amount
              currencyCode
            }
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

PRICE_LIST_PRICES_QUERY = """
query PriceListPrices($id: ID!, $after: String) {
  priceList(id: $id) {
    id
    prices(first: 250, after: $after) {
      nodes {
        variant {
          id
        }
        price {
          amount
          currencyCode
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
