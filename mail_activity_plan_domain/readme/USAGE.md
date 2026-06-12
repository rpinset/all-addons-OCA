To use this module:

1. Go to **Discuss > Configuration > Activity Plans**.
2. Open or create an activity plan.
3. In the **Domain** field, set the domain that records must match for this
   plan to appear in the scheduling wizard
   (e.g. `[('is_company', '=', True)]` to restrict the plan to company-type
   partners). Leave empty or use `[]` to apply to all records.
4. In the plan lines, each activity template also has its own **Domain** field.
   Set it to skip that activity for records that do not match
   (e.g. `[('is_company', '=', False)]` to schedule an activity only for
   individual contacts). Leave empty or use `[]` to always schedule the
   activity.

When scheduling a plan from a record, only plans whose **Domain** matches that
record will be listed. During execution, activities whose template domain does
not match the record are silently skipped.
