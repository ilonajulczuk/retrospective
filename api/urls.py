from django.conf.urls.defaults import url, patterns, include

from rest_framework import routers
from api.views import *



# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^retrospective/frequency', retrospective_frequency),
    url(r'^retrospective/content', retrospective_content),
    url(r'^retrospectives', retrospectives),
    url(r'^projects', projects_data),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)