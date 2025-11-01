1. **Create an RMA** for a tracked product (lot or serial) without specifying an existing lot
2. Assign an **RMA Operation** that has:
   - Auto-create Lot/Serial enabled
   - A Lot Sequence defined
3. Confirm the RMA
   - The system will generate a new stock lot using the defined sequence
   - The lot will be linked to the RMA

If configured, the lot will receive Expiration and Removal date (removal_date = expiration_date − N days).