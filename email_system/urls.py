from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^admin/$', views.admin_send_email, name='admin_send_email'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^contact/email_sent/$', views.email_sent, name='email_sent'),
    url(r'^join_us/$', views.join, name='join_us'),
    url(r'^join_us/join_email_sent/$', views.join_email_sent, name='join_email_sent'),
]
