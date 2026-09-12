This module is the **base framework** of the Barcode suite: a fast,
full-screen scanning application shell for Odoo that other modules extend.

It ships no business logic of its own. Instead it exposes the building blocks
feature modules plug into, the same way Odoo widgets self-register:

- a full-screen client action and a lightweight in-app router;
- registries for screens, scan handlers and home-screen menu tiles
  (`barcode_screens`, `barcode_scan_handlers`, `barcode_menu_tiles`);
- the barcode input service (hardware/keyboard wedge), audio/vibration
  feedback, an ORM/API wrapper and shared hooks.

Install a feature module on top — such as `barcode_stock` — to get actual
warehouse operations.
