
from core.models import Retrospective, SuccessEntry, FailedEntry, LearnedEntry, Project

from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['description', 'title']


class SuccessEntrySerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    class Meta:
        model = SuccessEntry
        fields = ['project', 'goal', 'problems', 'notes']


class FailedEntrySerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    class Meta:
        model = FailedEntry
        fields = ['project', 'goal', 'problems', 'notes']


class LearnedEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnedEntry
        fields = ['category', 'skill', 'description', 'goal',
                     'previous_usage', 'future_usages']

class RetrospectiveSerializer(serializers.ModelSerializer):
    successentry_set = SuccessEntrySerializer(many=True)
    learnedentry_set = LearnedEntrySerializer(many=True)
    failedentry_set = FailedEntrySerializer(many=True)

    class Meta:
        model = Retrospective
        fields = ('created', 'learnedentry_set', 'failedentry_set', 'successentry_set', 'direction', 'summary')
