from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings

admin.autodiscover()
urlpatterns = patterns(
    '',
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^', include('core.urls')),
    url(r'^core/', include('core.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/change_password/?', 'django.contrib.auth.views.password_change', {'template_name':'registration/password_change.html'}),
    url(r'^accounts/chpasswd/done/?', 'django.contrib.auth.views.password_change_done', {'template_name':'registration/password_change_done.html'}),
    (r'^accounts/logout/$', 'core.views.logout_view'),
    (r'^accounts/profile/$', 'core.views.profile_dashboard'),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^_admin/', include(admin.site.urls)),
    url(r'', include('django.contrib.staticfiles.urls')),
)
