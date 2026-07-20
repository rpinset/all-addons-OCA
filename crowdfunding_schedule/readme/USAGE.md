The module provides backend as well as frontend functionality.

For the backend:

#. Go to Crowdfunding.
#. Create a new crowdfunding challenge or open an existing one.
#. Set the challenge information, including:

    * Start Datetime
    * End Datetime

#. Save the challenge.

For the frontend:

#. Navigate to `/crowdfunding` on your Odoo website.
#. Select a challenge from the list.
#. Depending on the configured schedule:

    * Before the start datetime, a message indicates that the challenge is not yet active and a countdown shows the remaining   time until it starts.
    * During the active period, a countdown shows the remaining time until the challenge ends.
    * After the end datetime, a message indicates that the challenge has ended.

#. Visitors can submit pledges only when the challenge is in the Open state and the current date and time is between the configured start and end datetimes.
