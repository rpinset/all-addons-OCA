This module changes the default behavior when cancelling a confirmed sales order.

In standard Odoo, when you click "Cancel" on a confirmed sales order, a wizard
opens proposing to send an email notification to the customer. This can lead to
accidental emails being sent to customers.

With this module installed:

- The **Cancel** button directly cancels the order without showing any wizard
- A new **Send Email and Cancel** button is added (secondary style) that opens
  the wizard when you explicitly want to notify the customer about the cancellation
- The wizard only shows the "Send and cancel" and "Discard" buttons (the redundant
  "Cancel" button is removed from the wizard)
