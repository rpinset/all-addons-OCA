The board's **Late** indicator (the kanban "rotten" colour and the *Late*
search filter) flags a review that has been waiting for a decision longer than
a configurable number of days.

To tune it:

1.  Go to *Settings > Technical > Parameters > System Parameters*.
2.  Create or edit `base_tier_validation.late_after_days` (default `7`).

This is the same parameter the reviewer systray uses for its *Late* bucket, so
the board and the systray always agree on one threshold.
