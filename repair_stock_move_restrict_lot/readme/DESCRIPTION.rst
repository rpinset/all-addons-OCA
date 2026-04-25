Glue module between repair_stock_move and stock_restrict_lot.
It assigns the repair lot to the stock moves on creation. Otherwise in the
_action_assign it may reserve the incorrect quant and then and error is raised
when unreserving the quant: https://github.com/odoo/odoo/blob/15.0/addons/stock/models/stock_move_line.py#L388
