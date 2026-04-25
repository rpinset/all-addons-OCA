env = locals().get("env")
# set specific pricelist
pricelist_main = env["product.pricelist"].create({"name": "Pricelist for main company"})
company = env["res.company"].create({"name": "Product migration test company"})
pricelist = (
    env["product.pricelist"]
    .with_company(company)
    .create({"name": "Pricelist for demo company"})
)
partner = env.ref("base.user_demo").partner_id

partner.property_product_pricelist = pricelist_main
partner.with_company(company).property_product_pricelist = pricelist

env.cr.commit()
