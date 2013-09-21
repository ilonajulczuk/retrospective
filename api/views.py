
from api import statistics
from api.serializers import RetrospectiveSerializer
from core.models import Retrospective
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    model = User

class GroupViewSet(viewsets.ModelViewSet):
    model = Group

@api_view(['GET'])
def retrospective_frequency(request):
    user = request.user
    frequency = statistics.get_data_about_retrospective_frequency(user)
    return Response(frequency)

@api_view(['GET'])
def retrospective_content(request):
    user = request.user
    content_data = statistics.get_data_about_retrospective_content(user)
    return Response(content_data)


@api_view(['GET'])
def projects_data(request):
    user = request.user
    projects_data = statistics.get_data_about_projects(user)
    return Response(projects_data)


@api_view(['GET'])
def retrospectives(request):
    user = request.user
    retrospectives = Retrospective.objects.filter(user=user)

    serializer = RetrospectiveSerializer(retrospectives, many=True)
    return Response(serializer.data)