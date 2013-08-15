from django import forms
from core.models import (
    LearnedEntry, SuccessEntry, FailedEntry,
    Retrospective, Project)


class LearnedForm(forms.ModelForm):
    description = forms.CharField(
                widget=forms.Textarea(
                    attrs={'class':'form-control',
                           'rows': 2,
                           'style': "resize: none;"}))
    class Meta:
        model = LearnedEntry
        fields = ['category', 'skill', 'description', 'goal',
                  'previous_usage', 'future_usages']


class SuccessForm(forms.ModelForm):
    class Meta:
        model = SuccessEntry
        fields = ['project', 'goal', 'problems', 'notes']
    problems = forms.CharField(
                widget=forms.Textarea(
                    attrs={'class':'form-control',
                           'rows': 2}))
    notes = forms.CharField(
                widget=forms.Textarea(
                    attrs={'class':'form-control',
                           'rows': 2,
                           'style': "resize: none;"}))

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', None)
        if initial:
            retrospective_id = initial.get('retrospective_id', None)
        else:
            retrospective_id = None
        super(SuccessForm, self).__init__(*args, **kwargs)
        print retrospective_id
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

    problems = forms.CharField(
                widget=forms.Textarea(
                    attrs={'class':'form-control',
                           'rows': 4,
                           'style': "resize: none;"}))
    notes = forms.CharField(
                widget=forms.Textarea(
                    attrs={'class':'form-control',
                           'rows': 2,
                           'style': "resize: none;"}))
    
class RetrospectiveGeneralForm(forms.ModelForm):
    class Meta:
        model = Retrospective
        fields = ['summary', 'direction']
    summary = forms.CharField(
                widget=forms.Textarea(
                    attrs={'class':'form-control',
                           'rows': 2,
                           'style': "resize: none;"}))
    direction = forms.CharField(
                widget=forms.Textarea(
                    attrs={'class':'form-control',
                           'rows': 1,
                           'style': "resize: none;"}))


class ProjectForm(forms.ModelForm):
    description = forms.CharField(
            widget=forms.Textarea(
                attrs={'class':'form-control',
                       'rows': 2,
                       'style': "resize: none;"}))
    class Meta:
        model = Project
        fields = ['title', 'description',]