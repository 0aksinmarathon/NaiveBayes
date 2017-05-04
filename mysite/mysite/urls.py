from django.conf.urls import include, url


urlpatterns = [
    url(r'^hello/', include('hello.urls', namespace='hello')),
]