## 19.0.1.0.4 (2026-05-13)

UI improvement:

- The "needs to be validated" banner shown above tier-validated
  documents now surfaces *who* is expected to act, when known.
  Reads "Pending validation by John" or "Pending validation by
  Group Accountants" instead of the generic
  "This Record needs to be validated", with a fallback to the
  model-name phrasing for the defensive edge case where no review
  has reached ``pending`` yet. Reuses ``tier.review.todo_by`` so
  every review type (individual user, group, ``res.users`` /
  ``res.groups`` field) is handled uniformly. The banner template
  now reads from the long-standing ``to_validate_message`` Html
  field, which was previously defined on the model but never
  rendered.

## 19.0.1.0.1 (2026-05-12)

Fixes:

- Restore auto-promotion of the lowest-sequence review to ``pending``
  immediately after ``request_validation`` so the workflow can move
  forward without an external trigger. The 19.0 migration had moved
  this side-effect out of ``_compute_can_review`` into a separate
  ``_update_review_status`` that was only invoked when the requester
  was themself the first reviewer or when ``notify_on_create`` was
  set, leaving reviews stuck in ``waiting`` in every other case.
- Coerce ``next_review`` to ``False`` when no review is pending, so
  the "needs to be validated" banner no longer leaks the empty
  ``tier.review()`` recordset repr into its ``Char`` field.
- Fix ``_notify_review_available`` so the reviewer reached by
  ``notify_on_pending`` is actually delivered the message. The
  tier-validation subtypes have ``default=False`` so a plain
  ``message_subscribe(partner_ids=...)`` left the reviewer subscribed
  only to default subtypes; ``message_post`` with the
  ``mt_tier_validation_requested`` subtype then routed to nobody. Pass
  ``subtype_ids`` explicitly (mirroring ``_notify_review_requested``).

## 17.0.1.0.0 (2024-01-10)

Migrated to Odoo 17.
Merged module with tier_validation_waiting.
To support sending messages in a validation sequence when it is their turn to validate.

## 14.0.1.0.0 (2020-11-19)

Migrated to Odoo 14.

## 13.0.1.2.2 (2020-08-30)

Fixes:

- When using approve_sequence option in any tier.definition there can be
  inconsistencies in the systray notifications
- When using approve_sequence, still not approve only the needed
  sequence, but also other sequence for the same approver

## 12.0.3.3.1 (2019-12-02)

Fixes:

- Show comment on Reviews Table.
- Edit notification with approve_sequence.

## 12.0.3.3.0 (2019-11-27)

New features:

- Add comment on Reviews Table.
- Approve by sequence.

## 12.0.3.2.1 (2019-11-26)

Fixes:

- Remove message_subscribe_users

## 12.0.3.2.0 (2019-11-25)

New features:

- Notify reviewers

## 12.0.3.1.0 (2019-07-08)

Fixes:

- Singleton error

## 12.0.3.0.0 (2019-12-02)

Fixes:

- Edit Reviews Table

## 12.0.2.1.0 (2019-05-29)

Fixes:

- Edit drop-down style width and position

## 12.0.2.0.0 (2019-05-28)

New features:

- Pass parameters as functions.
- Add Systray.

## 12.0.1.0.0 (2019-02-18)

Migrated to Odoo 12.

## 11.0.1.0.0 (2018-05-09)

Migrated to Odoo 11.

## 10.0.1.0.0 (2018-03-26)

Migrated to Odoo 10.

## 9.0.1.0.0 (2017-12-02)

First version.
