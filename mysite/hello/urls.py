from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.hello_world, name='hello_world'),
    url(r'^template/$', views.hello_template, name='hello_template'),
    url(r'^get/$', views.hello_get_query, name='hello_get_query'),
]
