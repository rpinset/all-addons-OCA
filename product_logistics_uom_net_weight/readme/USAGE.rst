This module automatically integrates ``product_logistics_uom`` and ``product_net_weight`` functionality.
It installs automatically when both dependency modules are present in your system.

After automatic installation, you can:

* Configure different weight UoM per product in the Inventory tab
* Set net weight values that will be properly converted and validated
* View net weight in the product's configured UoM while maintaining system consistency

Example scenario:

* System UoM: kg (kilograms)
* Product UoM: g (grams) 
* Product weight: 1000 g → stored as 1 kg in system
* Net weight: 800 g → displayed as 800 g, stored as 0.8 kg, validated correctly

The module ensures that weight comparisons are made in the same UoM, preventing
validation errors that occurred when using both modules independently.

**Note**: Existing net weight values are migrated automatically during installation.
The migration assumes existing data is in the system's base UoM, which is the standard
behavior before this integration module.
