def pre_init_hook(env):
    # Add new column to avoid computing at install
    env.cr.execute(
        "ALTER TABLE sale_order "
        "ADD COLUMN IF NOT EXISTS stock_is_reserved BOOLEAN default(FALSE)"
    )
    env.cr.execute("ALTER TABLE sale_order alter column stock_is_reserved drop default")
