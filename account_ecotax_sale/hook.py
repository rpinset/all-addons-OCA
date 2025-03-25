def pre_init_hook(cr):

    cr.execute(
        """
        ALTER TABLE sale_order ADD COLUMN IF NOT EXISTS amount_ecotax numeric
        """
    )
    cr.execute(
        """
        UPDATE sale_order SET amount_ecotax = 0.0 WHERE amount_ecotax IS NULL
        """
    )
    cr.execute(
        """
        ALTER TABLE sale_order_line ADD COLUMN IF NOT EXISTS subtotal_ecotax numeric
        """
    )
    cr.execute(
        """
        ALTER TABLE sale_order_line ADD COLUMN IF NOT EXISTS ecotax_amount_unit numeric
        """
    )
    cr.execute(
        """
        UPDATE sale_order_line
        SET ecotax_amount_unit = 0.0, subtotal_ecotax = 0.0
        WHERE ecotax_amount_unit IS NULL
        """
    )
