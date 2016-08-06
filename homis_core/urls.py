# homis_core/urls.py


from django.conf.urls import url

from homis_core import views


urlpatterns = [
    #url(r'^$', views.index, name='index'),

    url(r'log_in', views.log_in),
    url(r'log_out', views.log_out),

    url(r'people', views.people),
]


