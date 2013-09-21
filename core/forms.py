from django import forms
from core.models import (
    LearnedEntry, SuccessEntry, FailedEntry,
    Retrospective, Project)


class LearnedForm(forms.ModelForm):
    class Meta:
        model = LearnedEntry
        fields = ['category', 'skill', 'description', 'goal',
                  'previous_usage', 'future_usages']


class SuccessForm(forms.ModelForm):
    class Meta:
        model = SuccessEntry
        fields = ['project', 'goal', 'problems', 'notes']

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', None)
        if initial:
            retrospective_id = initial.get('retrospective_id', None)
        else:
            retrospective_id = None
        super(SuccessForm, self).__init__(*args, **kwargs)
        if retrospective_id:
            userid = Retrospective.objects.get(id=retrospective_id).user_id
            self.fields['project'].queryset = Project.objects.filter(user_id=userid)

class FailedForm(forms.ModelForm):
    class Meta:
        model = FailedEntry
        fields = ['project', 'goal', 'problems', 'notes']

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', None)
        if initial:
            retrospective_id = initial.get('retrospective_id', None)
        else:
            retrospective_id = None
        super(FailedForm, self).__init__(*args, **kwargs)
        if retrospective_id:
            userid = Retrospective.objects.get(id=retrospective_id).user_id
            self.fields['project'].queryset = Project.objects.filter(user_id=userid)


class RetrospectiveGeneralForm(forms.ModelForm):
    class Meta:
        model = Retrospective
        fields = ['summary', 'direction']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description',]
