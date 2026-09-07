def assert_shopify_models_have_company_rules(testcase):
    """Fail with all concrete Shopify models missing an ir.rule."""
    models = testcase.env["ir.model"].search([("model", "=like", "shopify.%")])
    missing = []
    for model in models:
        runtime = testcase.env.registry.get(model.model)
        if not runtime or runtime._abstract:
            continue
        if not testcase.env["ir.rule"].search_count(
            [("model_id", "=", model.id)], limit=1
        ):
            missing.append(model.model)
    testcase.assertFalse(
        missing,
        "Shopify models without a company record rule: " + ", ".join(sorted(missing)),
    )
