from django import forms
from core.models import LearnedEntry, SuccessEntry, FailedEntry


class LearnedForm(forms.ModelForm):
    class Meta:
        model = LearnedEntry
        fields = ['category', 'skill', 'description', 'goal',
                  'previous_usage', 'future_usages']

    def is_valid(self):
        return True


class SuccessForm(forms.ModelForm):
    class Meta:
        model = SuccessEntry
        fields = ['project', 'goal', 'problems', 'notes']

    def is_valid(self):
        return True


class FailedForm(forms.ModelForm):
    class Meta:
        model = FailedEntry
        fields = ['project', 'goal', 'problems', 'notes']

    def is_valid(self):
        return True