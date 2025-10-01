This module includes a pre-installation hook that migrates existing ``net_weight`` data 
to the new ``product_net_weight`` field.

Migration Process
~~~~~~~~~~~~~~~~~

The hook performs the following operations:

1. **Database Schema**: Creates the new ``product_net_weight`` columns
2. **Data Migration**: Copies existing ``net_weight`` values to ``product_net_weight``
3. **No UoM Conversion**: Direct value copy is safe because existing ``net_weight`` data
   is already stored in the system's base UoM

Why No UoM Conversion is Needed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The migration performs a direct copy without UoM conversion due to architectural analysis:

**1. Impossibility of Different UoM Data**

Before this integration module, it was impossible to have ``net_weight`` values 
in a UoM different from the system's base UoM:

* **Without product_logistics_uom**: Products always use system UoM for weight
* **With product_logistics_uom**: Only display UoM changes, storage remains in system UoM
* **The compatibility bug**: Prevented users from successfully entering net_weight with custom UoM

**2. Data Integrity Guarantee**

Existing ``net_weight`` values are guaranteed to be in the system's base UoM, 
making direct migration both safe and correct.

**3. Post-Installation Behavior**

After installation, computed fields automatically handle proper UoM conversions 
for new data entry and display, ensuring future data consistency.

**4. Performance Optimization**

Direct SQL migration is significantly faster than computed field recalculation 
for databases with many existing products.

This approach ensures data consistency while maintaining optimal performance 
during the migration process.
