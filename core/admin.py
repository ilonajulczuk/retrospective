from django.contrib import admin

from core.workflow import Workflow, EntrySchema, Entry
from core.models import Retrospective


admin.site.register(Workflow)
admin.site.register(Entry)
admin.site.register(EntrySchema)
admin.site.register(Retrospective)
