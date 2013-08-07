from django.db import models
from django import forms
from django.contrib.auth.models import User


DAYS_OF_WEEK = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday',
]

DAY_TUPLES = [
    (day, day) for day in DAYS_OF_WEEK
]

class MailConfiguration(models.Model):
    
    user = models.ForeignKey(User)
    every_week = models.BooleanField(default=True)
    day_of_the_week = models.CharField(
        max_length=20,
        choices=DAY_TUPLES,
        default="Monday",
    )

    periodically = models.BooleanField(default=False)
    period_between_in_days = models.SmallIntegerField(default=0)

    last_sent = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return "MailConfiguration of user %s, id=%d" % (
            self.user,
            self.id,
        )

        
class BasicMailConfigurationForm(forms.ModelForm):
    day_of_the_week = forms.ChoiceField(
        choices=DAY_TUPLES
    )
    class Meta:
        model = MailConfiguration
        fields = ['day_of_the_week']
