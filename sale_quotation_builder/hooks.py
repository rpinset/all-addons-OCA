def pre_init_hook(env):
    """Allow installing sale_quotation_builder in databases
    with large sale.order / sale.order.line tables.

    Since website_description fields computation is based
    on new fields added by the module, they will be empty anyway.

    By avoiding the computation of those fields,
    we reduce the installation time noticeably
    """
    env.cr.execute(
        """
        ALTER TABLE "sale_order"
        ADD COLUMN "website_description" text
    """
    )
    env.cr.execute(
        """
        ALTER TABLE "sale_order_line"
        ADD COLUMN "website_description" text
    """
    )
    env.cr.execute(
        """
        ALTER TABLE "sale_order_template_line"
        ADD COLUMN "website_description" text
    """
    )
    env.cr.execute(
        """
        ALTER TABLE "sale_order_template_option"
        ADD COLUMN "website_description" text
    """
    )
