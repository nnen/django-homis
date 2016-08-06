# urls.py


from django.conf.urls import url, include
from django.contrib import admin


import homis_core.views
import finances.views


urlpatterns = [
    # Examples:
    # url(r'^$', 'django_homis.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls), name = "admin"),

    #url(r'^$', "finances.views.index"),
    url(r'^$', finances.views.index),

    url(r'^finances/', include('finances.urls', namespace = "finances")),
    url(r'^core/', include('homis_core.urls', namespace = "homis_core")),
]


