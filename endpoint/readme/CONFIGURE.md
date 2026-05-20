Endpoints are managed under **Technical → Endpoints**.

Each record represents a single HTTP route exposed by Odoo and executed
according to its configuration.

## Identification

- **Name**: human-readable label used in lists and logs.
- **Route**: URL path served by the endpoint (e.g. `/my/custom/path`).
  Routes must be unique across **all** endpoint-consumer models, not
  only within `endpoint.endpoint`.
- **Route group**: free-text tag to classify related routes together.
  Useful for filtering and for downstream modules that group endpoints.

## Authentication

- **Auth type**:
  - `User`: the request must be authenticated as an Odoo user (default).
  - `Public`: the route is accessible without authentication.
- **Exec as user**: the user under which the code snippet runs.
  - **Mandatory** when *Auth type* is `Public` (the public user has no
    real privileges, so the endpoint must impersonate a real user to
    perform any meaningful work).
  - Optional otherwise; if set, the snippet is evaluated as that user
    instead of the caller.

## Request

- **Request method**: `GET`, `POST`, `PUT` or `DELETE`. Requests using
  any other method are rejected with `405 Method Not Allowed`.
- **Request content type**: expected `Content-Type` of the incoming
  request body. Mandatory for `POST`/`PUT`. Available values:
  - `text/plain`, `text/csv`
  - `application/json`
  - `application/xml`
  - `application/x-www-form-urlencoded`

  When set, requests with a different `Content-Type` header are rejected
  with `415 Unsupported Media Type`.

### Request content schema (optional)

For `POST`/`PUT` endpoints whose content type is `application/json` or
`application/xml`, an optional **Request Schema** tab is shown. When a
schema is provided, the request body is validated against it before the
code snippet runs; on failure, the request is rejected with a structured
validation error (`RequestValidationError`).

The accepted schema format depends on the content type:

- **JSON** (`application/json`): a JSON Schema (Draft 2020-12). The field
  accepts both JSON and YAML syntax — YAML is convenient when authoring
  schemas inline.
- **XML** (`application/xml`): an XML Schema (XSD).

Example JSON Schema (YAML form):

```yaml
type: object
required: [name, qty]
properties:
  name: { type: string }
  qty:  { type: integer, minimum: 1 }
```

Example XSD:

```xml
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="greeting" type="xs:string"/>
</xs:schema>
```

> **Tip:** when shipping endpoints from a module, the schema can live in
> a separate file and be loaded into the field at install time using the
> `file` attribute on the data record:
>
> ```xml
> <field name="request_content_schema" type="char" file="endpoint/demo/content_schema.xsd" />
> ```

## Execution

- **Exec mode**: how the request is handled. The base module ships
  `Execute code`; downstream modules can register additional modes.
- **Code snippet** *(when exec mode is `code`)*: Python code evaluated
  via `safe_eval` for every request. The snippet must assign a `dict`
  to the `result` variable; it can either contain a ready-made
  `Response` (under the `response` key) or `payload`, `headers` and
  `status_code` to be assembled by the framework.

  Variables exposed to the snippet (see the **Code Help** tab on the
  form for the live, up-to-date list):

  - `env`, `user`, `endpoint`, `request`
  - `datetime`, `dateutil`, `time`, `json`
  - `Response` (Odoo's `http.Response`)
  - `werkzeug` (limited to `NotFound`, `BadRequest`, `Unauthorized`)
  - `exceptions` (limited to `UserError`, `ValidationError`)
  - `hashlib`, `hmac` (subset of the standard library)
  - `log(message, level="info")` — writes to `ir.logging`

  Raising `UserError` or `ValidationError` from the snippet is converted
  to `400 Bad Request`.

Minimal snippet:

```python
result = {"response": Response("Hello, World!")}
```

## Registry synchronization

Endpoints are registered in a routing registry that lives outside the
ORM. After creating, modifying or archiving a record, the warning
*"Registry out of sync"* appears on the form, and the record is shown in
the **To sync** filter on the list view. Run the **Sync registry**
action to commit the changes to the live routing table — until then, the
new configuration is **not** served.
