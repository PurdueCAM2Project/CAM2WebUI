from django.conf.urls import url
from django.views.generic.base import TemplateView, RedirectView
from . import views

urlpatterns = [
    url(r'^admin/$', views.admin_send_email, name='admin_send_email'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    url(r'^contact/email_sent/$', TemplateView.as_view(template_name='email_system/email_sent.html'), name='email_sent'),
    url(r'^join_us/$', RedirectView.as_view(url='https://purduehelps.org/join.html'), name='join_us'),
    url(r'^join_us/join_email_sent/$', TemplateView.as_view(template_name='email_system/join_email_sent.html'), name='join_email_sent'),
]
