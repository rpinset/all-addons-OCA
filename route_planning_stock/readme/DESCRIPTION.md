Integration between Route Planning and Stock to automatically generate routes and checkpoints from pickings.

This module automates route and checkpoint creation directly from stock pickings and integrates inventory transit locations and stock rules into Route Planning workflows.

**Key Features:**
- Automatic generation of a Transit Location per Route Area and corresponding stock rules.
- Automatic route and checkpoint generation upon picking validation.
- Automated validation of pickings when route checkpoints are marked as completed.

When you use the transit location created for the Route Area, the delivery is performed in two steps:

The first step moves the stock from the internal location where it is stored to the transit location. This movement represents the physical transfer from your warehouse to the transport vehicle that will perform the delivery.
A second picking is created when you validate the first picking. This picking waits for the corresponding checkpoint to be completed when the delivery is completed at the customer. Once the checkpoint is completed, the picking is automatically validated.

Note: For better integration and simplicity, we recommend using this module with the `route_planning_delivery` module installed.