from django.db import models
from django.contrib.auth.models import User as DefaultUser


class User(DefaultUser):
    pass


class Project(models.Model):
    description = models.TextField()
    user = models.OneToOneField(User)


class Retrospective(models.Model):
    user = models.ForeignKey('User')
    summary = models.TextField(blank=True)
    direction = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return "Retrospection id=%d of user %s" % (
            self.id, self.user)
    

class LearnedEntry(models.Model):
    retrospection = models.ForeignKey('Retrospective', null=True)
    category = models.CharField(max_length=50, blank=True)
    skill = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    goal = models.CharField(max_length=80, blank=True)
    previous_usage = models.CharField(max_length=80, blank=True)
    future_usages = models.CharField(max_length=80, blank=True)


class OutputEntry(models.Model):
    retrospection = models.ForeignKey('Retrospective', null=True)
    project = models.ForeignKey('Project', null=True)
    goal = models.CharField(max_length=80, blank=True)
    problems = models.TextField(blank=True)
    notes = models.TextField(blank=True)


class SuccessEntry(OutputEntry):
    pass


class FailedEntry(OutputEntry):
    pass


