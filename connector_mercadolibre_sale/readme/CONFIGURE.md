1.  Open the Mercado Libre backend and the page **Sales**.
2.  Choose an **Automatic Workflow**. **Import orders** stays available only when a
    workflow is set. Confirmation, invoicing, and delivery validation stay in
    `sale_automatic_workflow`.
3.  Set the sales team and the fiscal position copied onto imported orders.
4.  Choose service products for the shipping cost and the marketplace fee.
5.  Optionally set a tracking carrier. Tracking numbers are exported only for the
    seller-provided modes `custom` and `me1`.
6.  Map seller warehouses on the **Catalog** page before enabling **Export stock**.
    An unmapped seller logistic type (`drop_off`, `xd_drop_off`, `cross_docking`,
    `self_service`) raises a sale exception. Fulfillment stock is never pushed.
