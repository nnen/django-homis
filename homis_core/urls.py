from django.conf.urls import patterns, url

from homis_core import views


urlpatterns = patterns('',
    #url(r'^$', views.index, name='index'),

    url(r'log_in', views.log_in),
    url(r'log_out', views.log_out),
)
