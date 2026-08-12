On your exchange type configured for UBL outbound exchanges
select "UBL output generator for purchase orders" as "Generator".

Example of full flow configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Create an exchange type for UBL output, with "UBL output generator for purchase orders" as generator.
2. Create an `edi.configuration` for purchase orders with

  a. the exchange type created at step 1,
  b. the model `purchase.order`,
  c. the trigger "On PO state change"
  d. snippet like

      if record.state == 'purchase':
        record._edi_send_via_edi(conf.type_id)


3. Assign the configuration to a supplier
4. Create a PO for that supplier and confirm the order
