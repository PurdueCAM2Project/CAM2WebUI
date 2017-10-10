from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^getimg/$', views.getimg, name='image'),
    url(r'^getdbimg/$', views.getdbimg, name='dbimage'),
]