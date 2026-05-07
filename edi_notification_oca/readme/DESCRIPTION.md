This module creates activities for users when an exchange record's process fails.

Exchange types must be configured properly to create such activities:

- field "Notify On Process Error" must be checked to activate the feature
  for the current exchange type
- field "Activity Type Used When Notify On Process Error" is used to define
  the type of the newly created activity
- fields "Notify Groups On Process Error" and "Notify Users On Process Error" are used
  to define the users that will be assigned to the newly created activity
