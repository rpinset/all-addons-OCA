This module intends to create a base to be extended by local EDI rules
for project management.

In order to add customizations for projects, create a listener:

```python
from odoo.addons.component.core import Component


class ProjectEventListenerExample(Component):
    _name = "project.project.event.listener.example"
    _inherit = "base.event.listener"
    _apply_on = ["project.project"]

    def on_record_create(self, record, fields=None):
        """Do stuff after the project has been created"""

    def on_record_write(self, record, fields=None):
        """Do stuff after the project has been updated"""

    def on_record_unlink(self, record):
        """Do stuff before the project gets deleted"""
```

In order to add customizations for tasks, create a listener:

```python
from odoo.addons.component.core import Component


class ProjectTaskEventListenerExample(Component):
    _name = "project.task.event.listener.example"
    _inherit = "base.event.listener"
    _apply_on = ["project.task"]

    def on_record_create(self, record, fields=None):
      """Do stuff after the task has been created"""

    def on_record_write(self, record, fields=None):
      """Do stuff after the task has been updated"""

    def on_record_unlink(self, record):
      """Do stuff before the task gets deleted"""
```

Use ``@skip_if()`` decorator to avoid triggering a listener's method if necessary:

```python
from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if


class ProjectTaskEventListenerExample(Component):
    _name = "project.task.event.listener.example"
    _inherit = "base.event.listener"
    _apply_on = ["project.task"]

    @skip_if(lambda self, task: not task.stage_id)  # Do nothing if the task has no stage
    def on_record_update(self, record, fields=None):
        """Do stuff after the task has been created"""
```
