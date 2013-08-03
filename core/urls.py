from django.conf.urls import patterns, url

from core import views

urlpatterns = patterns(
    '',
    url(r'^create/learned$',
        views.create_learned, name='learn'),
    url(r'^create/failed$',
        views.create_failed, name='fail'),
    url(r'^create/succeeded$',
        views.create_succeeded, name='success'),
    url(r'^create/done$',
        views.finish_creation, name='done'),
    url(r'^$', views.index, name='index'),
)
