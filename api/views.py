
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from rest_framework.response import Response
from api import statistics
from rest_framework.decorators import api_view


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

