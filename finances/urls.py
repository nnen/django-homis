#finances/url.py


from django.conf.urls import url

from finances import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_simple_payment', views.add_simple_payment, name="add_simple_payment"),
    url(r'^add_transaction', views.add_transaction),

    url(r'^person/(\d+)', views.person),
]


