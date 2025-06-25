from psycopg2.extras import Json


def pre_init_hook(env):
    """Initialices product_packaging_quantity with the data of product_packaging_qty."""
    # Read initial data from orm because product_packaging_qty is computed store False
    sml_data = (
        env["stock.move.line"]
        .search([("move_id.product_packaging_id", "!=", False)])
        .read(["product_packaging_qty"])
    )
    # Create unexisting column
    env.cr.execute(
        "ALTER TABLE stock_move_line ADD COLUMN IF NOT EXISTS "
        "product_packaging_quantity FLOAT DEFAULT 0.0"
    )
    # Fill column with readed data to avoid recomputing it
    env.cr.execute(
        """
        UPDATE stock_move_line
        SET product_packaging_quantity = data.product_packaging_qty
        FROM json_to_recordset(%s) AS data (
            id INT,
            product_packaging_qty FLOAT
        )
        WHERE stock_move_line.id = data.id;
        """,
        (Json(sml_data),),
    )
