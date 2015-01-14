from django.conf.urls import patterns, url

from finances import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
