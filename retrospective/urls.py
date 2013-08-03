from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from core.models import *

admin.site.register(Retrospection)
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'retrospective.views.home', name='home'),
    url(r'^core/', include('core.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^_admin/', include(admin.site.urls)),
)
