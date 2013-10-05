from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User


class Workflow(models.Model):
    public = models.BooleanField(default=False)
    entries_metadata = JSONField()
    creator = models.ForeignKey(User)

class EntrySchema(models.Model):
    creator = models.ForeignKey(User)
    fields = JSONField()
    workflows = models.ManyToManyField(Workflow, related_name="entryschemas")


class Entry(models.Model):
    schema = models.ForeignKey(EntrySchema)
    data = JSONField()
