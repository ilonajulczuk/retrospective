from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from core.models import *
from django.conf import settings


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^core/', include('core.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'core.views.logout_view'),
    (r'^accounts/profile/$', 'core.views.profile_dashboard'),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^_admin/', include(admin.site.urls)),
    url(r'', include('django.contrib.staticfiles.urls')),
)
