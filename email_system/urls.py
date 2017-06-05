from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.admin_send_email, name='admin_send_email'),
]