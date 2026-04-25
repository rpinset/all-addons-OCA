## Creation

First step is to create a Platform.
In the platform we need to set the host (you might need to create it on gitlab) and add some Platform Keys.

This keys will allow us to integrate with the origin system.

## Refresh

By default, the system provides some refresh rules for platforms and repositories, however we can deactivate or activate it manualy.

## Management of rules

One of the capabilities of this module is the generation of rules.

This rules allow us to know some information of the repository.

By default, the system adds some rules aligned with odoo to make it easier and allows you to see some examples.

In order to launch this rules, the system must download the code locally.

By default the system is using the following main path (in order, the first one not null is selected):

- Parameter vcp_management.source_code_local_path
- In odoo configuration file, the option source_code_local_path 
- System parameter SOURCE_CODE_LOCAL_PATH
