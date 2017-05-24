from django.conf.urls import url, include
from . import views as app_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', app_views.index, name="index"),
    url(r'^cameras/$', app_views.cameras, name='cameras'),
    url(r'^team/$', app_views.team, name='team'),
    url(r'^privacy/$', app_views.privacy, name='privacy'),
    url(r'^ack/$', app_views.acknowledgement, name='acknowledgement'),
    url(r'^contact/$', app_views.contact, name='contact'),
    url(r'^faqs/$', app_views.faqs, name='faqs'),
    url(r'^terms/$', app_views.terms, name='terms'),
    url(r'^profile/$', app_views.profile, name='profile'),
    #url(r'^login/', app_views.login, name='login'),
    url(r'^login/$', auth_views.login, {'template_name': 'app/login.html'}, name='login'),
	url(r'^register/$', app_views.register, name='register'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}),
    url(r'^oauth/', include('social_django.urls', namespace='social')),#don't add $ after oauth/
]
