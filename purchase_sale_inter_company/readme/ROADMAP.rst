* No synchronization is made from the generated sale order back to the purchase order.
  This would be interesting in the case of price changes and discounts, that would be
  transmitted to the purchase so both documents couldn't have different total amounts,
  taxes, etc. A mechanism for synching from the sale to the purchase order would be
  needed.

* Module is not very robust in complex situations, such as multi-step receipts
  and multi-step deliveries, with backorders. Multi-step receipts
  could be improved further.
