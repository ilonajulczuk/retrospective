from django.db import models
from django.contrib.auth.models import User as DefaultUser


class User(DefaultUser):
    pass


class Project(models.Model):
    description = models.TextField()
    user = models.OneToOneField(User)


class Retrospection(models.Model):
    user = models.ForeignKey('User')
    summary = models.TextField()
    direction = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return "Retrospection id=%d of user %s" % (
            self.id, self.user)
    

class LearnedEntry(models.Model):
    retrospection = models.ForeignKey('Retrospection')
    category = models.CharField(max_length=50)
    skill = models.CharField(max_length=50)
    description = models.TextField()
    goal = models.CharField(max_length=80)
    previous_usage = models.CharField(max_length=80)
    future_usages = models.CharField(max_length=80)


class OutputEntry(models.Model):
    retrospection = models.ForeignKey('Retrospection')
    project = models.ForeignKey('Project')
    goal = models.CharField(max_length=80)
    problems = models.TextField()
    notes = models.TextField()


class SuccessEntry(OutputEntry):
    pass


class FailedEntry(OutputEntry):
    pass


