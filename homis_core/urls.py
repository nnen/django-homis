# homis_core/urls.py


from django.conf.urls import url

from homis_core import views


app_name = "homis_core"


urlpatterns = [
    #url(r'^$',     views.index,   name='index'),

    url(r'log_in',  views.log_in,  name = "log-in"),
    url(r'log_out', views.log_out, name = "log-out"),

    url(r'people',  views.people,  name = "people"),
]


