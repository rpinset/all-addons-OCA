Nothing to configure for the module itself. The precision a measure is kept at
is Odoo's, though, and its defaults are coarser than most GS1 labels.

A measure becomes a quantity rounded twice, as anywhere in stock: to the
*Rounding Precision* of the product's unit, and to the decimals of the
*Product Unit of Measure* accuracy. Both default to two decimals, so the
2.497 kg a label states is stored as 2.50 kg, and the app shows 2.50 so that the
quantity on screen is the one that will be stored.

To keep the grams a label states, for products stocked in kilograms:

- set the *Rounding Precision* of *kg* to 0.001, under
  *Inventory → Configuration → Units of Measures → UoM Categories → Weight*
  (the *Units of Measure* option must be enabled in the Inventory settings);
- set the digits of *Product Unit of Measure* to 3, under
  *Settings → Technical → Database Structure → Decimal Accuracy* (developer
  mode).

The accuracy applies to every quantity in the database, not only to scans.
