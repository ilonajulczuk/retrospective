from django.db import models
from django.contrib.auth.models import User
from core.tablefy import TablefyMixin
from core.workflow import *

# TODO wipe out this tablefying thing

class Project(models.Model):
    description = models.TextField()
    user = models.ForeignKey(User)
    title = models.CharField(max_length=40, blank=True, null=True)
    def __unicode__(self):
        return self.title


class Retrospective(models.Model):
    user = models.ForeignKey(User)
    summary = models.TextField(blank=True)
    direction = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def is_invalid(self):
        if not self.learnedentry_set.exists():
            return True
        if not self.failedentry_set.exists():
            return True
        if not self.successentry_set.exists():
            return True
        return False

    def __unicode__(self):
        return "Retrospection id=%d of user %s" % (
            self.id, self.user)

    def tablefy_queryset(self, queryset):
        table_header = "<thead>" + queryset.all()[0].__class__.as_header() + "</thead>"
        table_body = "<tbody>" + "\n".join(
            [q.as_table_row(number=i) for i, q in enumerate(queryset.all())]) + "</tbody>"
        return "<table class='table'>" + table_header + table_body + "</table>"
    
    def as_table(self):
        general_info = (
            "<h3>Retrospection summary</h3>"
            "<p>%s</p>" % (self.summary) +
            "<h3>Direction</h3>" +
            "<p>%s</p>" % (self.direction)
        )
        learned_table = self.tablefy_queryset(self.learnedentry_set)
        failed_table = self.tablefy_queryset(self.failedentry_set)
        success_table = self.tablefy_queryset(self.successentry_set)
        return (
            general_info +
            "<h3>What I learned</h3>" +
            learned_table + 
            "<h3>Failures</h3>" +
            failed_table + 
            "<h3>Successes</h3>" +
            success_table
        )


class LearnedEntry(models.Model, TablefyMixin):
    retrospective = models.ForeignKey('Retrospective', null=True)
    category = models.CharField(max_length=50, blank=True)
    skill = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    goal = models.CharField(max_length=80, blank=True)
    previous_usage = models.CharField(max_length=80, blank=True)
    future_usages = models.CharField(max_length=80, blank=True)

    public_fields = ['category', 'skill', 'description', 'goal',
                     'previous_usage', 'future_usages']


    def __unicode__(self):
        return "LearnedEntry id=%d, skill=%s, description=%s" % (
            self.id, self.skill, self.description)


class OutputEntry(models.Model):
    project = models.ForeignKey('Project', null=True)
    goal = models.CharField(max_length=80, blank=True)
    problems = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    public_fields = ['project', 'goal', 'problems', 'notes']


class SuccessEntry(OutputEntry, TablefyMixin):
    retrospective = models.ForeignKey('Retrospective', null=True)

    def __unicode__(self):
        return "%s id=%d, goal=%s, problems=%s" % (
            "SuccessEntry", self.id, self.goal, self.problems)


class FailedEntry(OutputEntry, TablefyMixin):
    retrospective = models.ForeignKey('Retrospective', null=True)

    def __unicode__(self):
        return "%s id=%d, goal=%s, problems=%s" % (
            "FailedEntry", self.id, self.goal, self.problems)


