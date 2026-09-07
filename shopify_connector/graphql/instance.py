"""GraphQL documents used by Shopify instance operations."""

SHOP_QUERY = """
query ShopIdentity {
  shop {
    name
    currencyCode
  }
}
"""

CURRENT_APP_SCOPES_QUERY = """
query CurrentAppScopes {
  currentAppInstallation {
    accessScopes {
      handle
    }
  }
}
"""

SHOP_TAX_SETTINGS_QUERY = """
query ShopTaxSettings {
  shop {
    taxesIncluded
    taxShipping
    shopAddress {
      countryCodeV2
    }
  }
}
"""

WEBHOOK_SUBSCRIPTIONS_QUERY = """
query WebhookSubscriptions {
  webhookSubscriptions(first: 250) {
    nodes {
      id
      topic
      endpoint {
        ... on WebhookHttpEndpoint {
          callbackUrl
        }
      }
    }
  }
}
"""

WEBHOOK_SUBSCRIPTION_CREATE = """
mutation CreateWebhookSubscription(
  $topic: WebhookSubscriptionTopic!
  $subscription: WebhookSubscriptionInput!
) {
  webhookSubscriptionCreate(topic: $topic, webhookSubscription: $subscription) {
    webhookSubscription {
      id
      topic
    }
    userErrors {
      field
      message
    }
  }
}
"""

WEBHOOK_SUBSCRIPTION_UPDATE = """
mutation UpdateWebhookSubscription(
  $id: ID!
  $subscription: WebhookSubscriptionInput!
) {
  webhookSubscriptionUpdate(id: $id, webhookSubscription: $subscription) {
    webhookSubscription {
      id
      topic
    }
    userErrors {
      field
      message
    }
  }
}
"""
