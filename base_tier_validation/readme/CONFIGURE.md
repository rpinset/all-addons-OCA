To configure this module, you need to:

1.  Go to *Settings \> Technical \> Tier Validations \> Tier
    Definition*.
2.  Create as many tiers as you want for any model having tier
    validation functionality.

**Note:**

- If check *Notify Reviewers on Creation*, all possible reviewers will
  be notified by email when this definition is triggered.
- If check *Notify reviewers on reaching pending* if you want to send a notification when pending status is reached.
  This is usefull in a approve by sequence scenario to only notify reviewers when it is their turn in the sequence.
- If check *Comment*, reviewers can comment after click Validate or
  Reject.
- If check *Approve by sequence*, reviewers is forced to review by
  specified sequence.

To tune when a pending review is flagged as *Late* in the reviewer
systray, you need to:

1.  Go to *Settings \> Technical \> Parameters \> System Parameters*.
2.  Create or edit the `base_tier_validation.late_after_days` parameter.

**Note:**

- The tier-review systray splits your reviews into *Late*, *Pending*
  and *Future* buckets. A review is counted as *Late* once it
  has been pending for more than `base_tier_validation.late_after_days`
  days (default `7`). With *Approve by sequence*, that counts from when
  the previous tier was validated. Lower the value to be alerted sooner, raise it to
  be more tolerant. The parameter is read on each systray refresh, so a
  change takes effect immediately without restarting.

To configure Tier Validation Exceptions, you need to:

1. Go to *Settings > Technical > Tier Validations > Tier Validation Exceptions*.
2. Create as many tiers validation exceptions as you want for any model
   having tier validation functionality.
3. Add desired fields to be checked in *Fields*.
4. Add desired groups that can use this Exception in *Groups*.
5. You must check *Write under Validation*, *Write after Validation* or both.

**Note:**

* If you don't create any exception, the Validated record will be readonly and cannot be modified.
* If check *Write under Validation*, records will be able to be modified only in the defined fields when the Validation process is ongoing.
* If check *Write after Validation*, records will be able to be modified only in the defined fields when the Validation process is finished.
* If check *Write after Validation* and *Write under Validation*, records will be able to be modified defined fields always.
