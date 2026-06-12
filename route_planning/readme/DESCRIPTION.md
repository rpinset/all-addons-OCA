This module allows to manage delivery routes, checkpoints, and visit windows.

Before using this module, you must configure the required master data: **Route Areas**,
**Checkpoints**, and **Routes**. Without this data, the route planning functionality will
not be operational.

## Models

### Route Area

Defines a geographic or logical zone used to group routes. Each area helps organize
delivery operations by region or territory.

### Checkpoint

Represents a specific stop or delivery point within a route. Checkpoints define the
locations that must be visited, along with any time window constraints for the visit.

### Route

A route is an ordered sequence of checkpoints assigned to a specific area. It defines
the order in which checkpoints must be visited, making it possible to optimize daily
or weekly operations for any kind of service or delivery workflow.

### Visit Windows

A visit window defines the time interval during which a checkpoint must be reached.
Windows are configured on the **contact (partner)**, where one or more slots can be
defined specifying the earliest arrival time (*time from*) and the latest allowed
arrival time (*time to*). This allows the same availability constraints to be reused
across different routes and checkpoints.
