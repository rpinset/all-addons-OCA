This module extends Odoo's activity plan feature with domain-based filtering at
two levels:

**Plan domain**

Each activity plan gains a *Domain* field. Only records matching this domain
will have the plan available in the scheduling wizard
(`mail.activity.schedule`). This lets you restrict plans to, for example,
company-type partners or records in a specific stage.

**Template domain**

Each line of an activity plan (template) gains its own *Domain* field. When
executing a plan, activities whose template domain does not match the target
record are silently skipped. This allows a single plan to cover heterogeneous
records while still generating only the relevant activities per record.

**Notes**

- The error preview shown in the scheduling wizard (missing responsible,
  etc.) deliberately ignores template domains so that all potential
  configuration issues remain visible.
- When scheduling a plan on multiple records, execution is serialized
  record by record so that each record is evaluated independently against
  both plan and template domains.
- Domain syntax follows the standard Odoo domain format,
  e.g. `[('is_company', '=', True)]`.
