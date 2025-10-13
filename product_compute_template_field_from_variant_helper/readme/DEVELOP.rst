Replace this code:

.. code-block:: python

  class ProductTemplate(models.Model):
      _inherit = "product.template"

      net_weight = fields.Float(
          compute="_compute_net_weight",
          inverse="_inverse_net_weight",
          store=True,
      )

      @api.depends("product_variant_ids", "product_variant_ids.net_weight")
      def _compute_net_weight(self):
          for template in self:
              if template.product_variant_count == 1:
                  template.net_weight = template.product_variant_ids.net_weight
              else:
                  template.net_weight = 0.0

      def _inverse_net_weight(self):
          for template in self:
              if len(template.product_variant_ids) == 1:
                  template.product_variant_ids.net_weight = template.net_weight

    def _get_related_fields_variant_template(self):
        res = super()._get_related_fields_variant_template()
        res.append("net_weight")
        return res

By this code:

.. code-block:: python

  class ProductTemplate(models.Model):
      _inherit = "product.template"

      net_weight = fields.Float(
          compute=lambda x: x._compute_template_field_from_variant_field("net_weight"),
          inverse=lambda x: x._set_product_variant_field("net_weight"),
          store=True,
      )

    def _get_related_fields_variant_template(self):
        res = super()._get_related_fields_variant_template()
        res.append("net_weight")
        return res
