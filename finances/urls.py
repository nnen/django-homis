from django.conf.urls import patterns, url

from finances import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^add_simple_payment', views.add_simple_payment, name="add_simple_payment"),

    url(r'^person/(\d+)', views.person),
)
