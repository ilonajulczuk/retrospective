from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User


class Workflow(models.Model):
    public = models.BooleanField(default=False)
    entries_metadata = JSONField()
    creator = models.ForeignKey(User)

    def __str__(self):
        return "id: %s, title: '%s', created by %s" % (
            self.id, self.title, self.creator
        )

    title = models.CharField(default="noname", max_length=80)

class EntrySchema(models.Model):
    creator = models.ForeignKey(User)
    fields = JSONField()
    workflows = models.ManyToManyField(Workflow, related_name="entryschemas")
    title = models.CharField(default="noname", max_length=80)

    def __str__(self):
        return "id: %s, title: '%s'" % (
            self.id, self.title
        )


class Entry(models.Model):
    schema = models.ForeignKey(EntrySchema)
    data = JSONField()

