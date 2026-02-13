## Creating an RMA Batch Manually

1.  Go to *Returns: RMA Batches*.
2.  Click *New* to create a batch.
3.  Fill in general information such as:
4.  Add one or more RMAs in the *RMA* tab.

## Batch States

- **Draft:** The batch is being prepared; RMAs can be added or edited.
- **Ready:** All information is complete and the batch is ready for
  confirmation.
- **Confirmed:** The batch and all contained RMAs are confirmed
  together.
- **Cancelled:** The batch and its RMAs are cancelled.

## Automatic Batch Creation from Stock Returns

When performing a *Return Picking* with `Create RMA = True`:

- If the return involves only one product, a single RMA is created (no
  batch).
- If multiple RMAs are created, the system automatically groups them
  into a new RMA Batch in the *Confirmed* state.

You can view the created batch under *Returns: RMA Batches* or access it
from any linked RMA.
