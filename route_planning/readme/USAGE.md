Follow these steps before creating routes and checkpoints.

**Create Areas**

Go to `Route Planning > Configuration > Areas` and create the areas that represent the geographic or logical zones where routes will operate. At least one area is required. Each area must have a responsible user assigned.

**Configure Visit Window Templates (optional)**

Go to `Route Planning > Configuration > Visit Window Templates` to define
reusable sets of time windows. Templates can later be applied to contacts to populate their visit windows quickly.

**Configure Contacts**

Open any contact form (`Contacts` app) and go to the `Route Planning` tab.
There you can:

- Assign the contact to an `Area`.
- Define the contact’s `Latitude and Longitude`.
- Set one or more `Visit Windows`, either manually or by selecting a `Visit Window Template`.

At least the contacts that will be used as checkpoint destinations should be
configured.

**Create Routes**

Go to `Route Planning > Operations > Routes` and create a route. 
Assign it to an area and add the checkpoints directly from the route form. 
Only the areas where the current user is the responsible user are available when
creating the route. A checkpoint can be linked to a contact or defined only
with its own latitude and longitude. 
When the route is planned, the checkpoints are reordered automatically using `OR-Tools`, 
which suggests the best route based on the available coordinates and time windows.

A `map button` is available on the route form to visualize all checkpoints on a map.

**Day-to-day operations**

Users can go to `Route Planning > Operations > Checkpoints` to see the
checkpoints assigned to them and manage the status and details of each stop.
Each checkpoint also includes a `map view` to locate the stop geographically.
