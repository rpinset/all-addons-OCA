"""GraphQL documents used by the pure-Python foundation."""

BULK_OPERATION_RUN = """
mutation RunBulkQuery($query: String!) {
  bulkOperationRunQuery(query: $query) {
    bulkOperation {
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

BULK_OPERATION_POLL = """
query BulkOperation($id: ID!) {
  bulkOperation(id: $id) {
    id
    status
    errorCode
    objectCount
    fileSize
    url
    partialDataUrl
  }
}
"""
