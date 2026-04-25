Microsoft -- Odoo Calendar synchronization, how it works

# Preparation

Odoo sysadmin must connect server with Microsoft.

Follow the instructions in the link below to create a registered Microsoft Application
or Entra ID, which should result in a client ID and a client secret.

<https://www.odoo.com/documentation/18.0/applications/productivity/calendar/outlook.html>

Then in General Settings, under Integrations it is possible to enable Outlook Calendar
and then fill in the Client ID and secret.

There is a cron for the Outlook Calendar synchronization that needs to be configured to
run when and how often.

There are a few settings for finetuning, but basically this completes the general server
configuration.

Each user will have, if so desired, to activate (or stop) the calendar synchronization
for his/her/its own calendar. To use that they need to go to the calendar view of the
calendar app. In the sidebar on the right, under the month overview, there are buttons
to login to either google or outlook, so activate the synchronization.

Activation will set fields in the res.users model:

In microsoft_account module the fields are defined for the authentication of the user:

microsoft_calendar_rtoken

microsoft_calendar_token

microsoft_calendar_token_validity

Defined in microsoft_calendar module:

microsoft_calendar_sync_token: will be used to limit synchronization to what still needs
to be done;

microsoft_synchronization_stopped: will be set to False.

# High level overview of the synchronization

The synchronization is run from the res.users model. The method called is
\_sync_all_microsoft_calendar() which will select all users that have a valid refresh
token (defined in microsoft_account module) and where synchronization has not been
stopped. For all of those users the method \_sync_microsoft_calendar() will be called.

For each user to be synchronized a connection is made with the MS calendar service:

calendar_service = self.env\[\"calendar.event\"\].\_get_microsoft_service()

Then either all microsoft events for this user are retrieved (when no sync token in
user), or everything that has changed since the last synchronization. Apart from the
events we get a new synchronization token, that will be used on a next call to not have
a full synchronization each time:

events, next_sync_token =
calendar_service.get_events(self.microsoft_calendar_sync_token, token=token)

If there are any MS events to be synchronized that will be done. So this is **from
Microsoft to Odoo**. This synchronization returns both normal calendar events, as well
as recurring events:

synced_events, synced_recurrences =
self.env\[\'calendar.event\'\].\_sync_microsoft2odoo(events)

Now it is time to synchronize **from Odoo to Microsoft**. This will be done seperately
for recurring events and single calendar events:

First all recurrences that might be synchronized with Microsoft are searched. The
occurences that just have been synced from Microsoft are excluded. The synchronization
is run. Any calendar events that belong to the recurrences are added to the already
synced events:

recurrences =
self.env\[\'calendar.recurrence\'\].\_get_microsoft_records_to_sync(full_sync=full_sync)

recurrences -= synced_recurrences

recurrences.\_sync_odoo2microsoft()

synced_events \|= recurrences.calendar_event_ids

Now it is time to synchronize the single calendar events, that are not part of a
recurrence, and that have not been synchronized from Microsoft to Odoo:

events =
self.env\[\'calendar.event\'\].\_get_microsoft_records_to_sync(full_sync=full_sync)

(events -- synced_events).\_sync_odoo2microsoft()

# Microsoft Events

To make it easier to deal with events retrieved from Microsoft, or to be created/updated
at Microsoft, these events are stored in an Event object that has many parallels with
the Odoo objects that reflect rows in the postgress database.

The classes are defined in:

odoo/addons/microsoft_calendar/utils/microsoft_event.py

# Synchronization from Microsoft to Odoo

The synchronization from Microsoft to Odoo is defined in a mixin that will be used to
extend both the calendar.event and the calendar.recurrence models:
microsoft.calendar.sync.

The basic sequence is as follows:

Odoo and microsoft events are matched. This separates MS Events that are new, from those
that can be updated.

-- Events cancelled on the Microsoft side are cancelled on Odoo;

-- New events that are not recurrences are added;

-- Recurrences and updated events are gathered;

-- Recurrences and events cancelled on the Odoo site are cancelled on Microsoft

(So this is actually from Odoo to Microsoft!)

-- Looping over the existing events (minus those cancelled), the Odoo events and
recurrences are updated if the update time on Microsoft is after the update time on
Odoo.

(This supposes the clocks on both systems are more or less in sync);

-- The synced events and synced recurrences are returned.

# Synchronization from Odoo to Microsoft

This is defined in the mixin class microsoft.calendar.sync in the method
\_sync_odoo2microsoft.

First all active records are selected, and all the others assigned to cancelled_records.

Then it is determined which records already exist on the Microsoft side. The rest is
new.

The cancelled records that exist on Microsoft are deleted there.

The new records are created on the Microsoft side.

The updated records are checked for the need to synchronize, and if they are the
Microsoft side is updated ('patched').
