Run a reception's quality control inspections directly from the Barcode app.

When a reception (incoming picking) generates quality inspections through
[quality_control_stock_oca](https://github.com/OCA/manufacture) (from the
operation type and product quality triggers), this module surfaces them as a
**Quality** tab inside the reception screen. The operator answers each check —
picking a value for qualitative checks, entering a measure for quantitative ones
— and confirms; when an inspection does not pass, a photo can be attached to it
as evidence.

This is a feature module on top of `barcode_stock`: it adds the Quality tab by
extending the reception screen, without modifying `barcode_stock` itself.
