from django import forms
from core.models import (
    LearnedEntry, SuccessEntry, FailedEntry, Retrospective)


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
    

class FailedForm(forms.ModelForm):
    class Meta:
        model = FailedEntry
        fields = ['project', 'goal', 'problems', 'notes']
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