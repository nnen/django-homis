# urls.py


from django.conf.urls import url, include
from django.contrib import admin


import homis_core.views
import finances.views


ROOT_URL = r"^homis/"


urlpatterns = [
    # Examples:
    # url(r'^$', 'django_homis.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(ROOT_URL + r'$',         finances.views.index),

    url(ROOT_URL + r'finances/', include('finances.urls', namespace = "finances")),
    url(ROOT_URL + r'core/',     include('homis_core.urls', namespace = "homis_core")),

    url(ROOT_URL + r'admin/',    include(admin.site.urls), name = "admin"),
]


