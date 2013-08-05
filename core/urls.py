from django.conf.urls import patterns, url

from core import views

urlpatterns = patterns(
    '',
    url(r'^introduction$',
        views.introduction, name='introduction'),
    url(r'^create/learned$',
        views.create_learned, name='learn'),
    url(r'^create/failed$',
        views.create_failed, name='fail'),
    url(r'^create/succeeded$',
        views.create_succeeded, name='success'),
    url(r'^create/general$',
        views.general_retrospection, name='general'),
    url(r'^create/done$',
        views.finish_creation, name='done'),
    url(r'^create/project$',
        views.create_project, name='project'),
    url(r'^change/project$',
        views.change_project, name='change_project'),
    url(r'^create/thanks$',
        views.thanks, name='thanks'),
    url(r'^$', views.index, name='index'),
)
