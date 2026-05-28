This addon automatically links RMA records to the most relevant sale order
lines based on delivered quantities and an eligibility period defined on the
RMA operation.

The module will:

* Search sale order lines delivered to the same partner
* Filter them by the operation's allowed return period
* Consume delivered quantities in chronological order
* Link the RMA to the corresponding stock move(s)
* Split the RMA if multiple deliveries or partial matches are needed
* Flag the RMA if no matching sale delivery was found
