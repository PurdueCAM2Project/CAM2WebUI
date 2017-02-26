from django.conf.urls import include, url
from django.conf.urls import *
from django.contrib import admin
from .views import home
urlpatterns = [
    url(r'^home/$',home, name="home"),
]