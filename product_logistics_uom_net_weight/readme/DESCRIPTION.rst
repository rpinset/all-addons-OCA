This module solves compatibility issues between ``product_logistics_uom`` and ``product_net_weight``
when both modules are installed simultaneously and products use different Units of Measure (UoM) for weight.

The problem occurs because:

* ``product_logistics_uom`` stores weight values converted to the system's base UoM
* ``product_net_weight`` assumes all weight fields use the same UoM for validation
* This causes ``ValidationError`` when comparing net weight vs gross weight in different UoM

This integration module provides:

* A new ``product_net_weight`` field that displays net weight in the product's configured UoM
* Proper UoM conversion between product-specific and system UoM
* Maintains compatibility with existing data through a migration hook
* Preserves all functionality from both original modules
* **Automatic installation** when both dependency modules are present

**Auto-Installation Behavior**

This module is configured for automatic installation when both ``product_logistics_uom`` 
and ``product_net_weight`` are installed in the same database. This ensures seamless 
compatibility without manual intervention, preventing ValidationError issues from occurring.

The validation logic is corrected to compare weights in the same UoM, preventing false
validation errors while maintaining data integrity.
