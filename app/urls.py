from django.conf.urls import include, url
from django.conf.urls import *
from django.contrib import admin
from .views import index

urlpatterns = [
    url(r'^$', index, name="index"),
    
    url(r'^contact/$',views.contact, name='contact'),
]
