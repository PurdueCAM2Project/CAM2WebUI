from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.labelimgindex, name='labelimgindex'),
    url(r'^getimg/$', views.getimg, name='image'),
]
