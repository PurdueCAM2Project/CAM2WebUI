from django.conf.urls import url, include
from . import views as app_views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView, RedirectView

urlpatterns = [
    url(r'^$', app_views.index, name="index"),
    url(r'^cameras/$', app_views.cameras, name='cameras'),
    url(r'^good_cameras/$', TemplateView.as_view(template_name='app/good_cameras.html'), name='good_cameras'),
    url(r'^team/$', app_views.team, name='team'),
    url(r'^team_poster/$', app_views.team_poster, name='team_poster'),
    url(r'^advice/$', TemplateView.as_view(template_name='app/advice.html'), name='advice'),
    url(r'^history/$', app_views.history, name='history'),
    url(r'^publications/$', app_views.publications, name='publications'),
    url(r'^publications_list/$', RedirectView.as_view(url='/publications/?list=true'), name='publications_list'),
    url(r'^privacy/$', TemplateView.as_view(template_name='app/privacy.html'), name='privacy'),
    url(r'^ack/$', TemplateView.as_view(template_name='app/ack.html'), name='acknowledgement'),
    url(r'^faqs/$', app_views.faqs, name='faqs'),
    url(r'^terms/$', TemplateView.as_view(template_name='app/terms.html'), name='terms'),

    #user authentication
    url(r'^profile/$', app_views.profile, name='profile'),
    url(r'^register/$', app_views.register, name='register'),
    url(r'^oauthinfo/$', app_views.oauthinfo, name='more info'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page='/')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),#don't add $ after oauth/
    url(r'^email_confirmation_sent/$', TemplateView.as_view(template_name='app/email_confirmation_sent.html'), name='email_confirmation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        app_views.activate, name='activate'),
    url(r'^email_confirmation_invalid/$', TemplateView.as_view(template_name='app/email_confirmation_invalid.html'), name='email_confirmation_invalid'),
    url(r'^account_activated/$', TemplateView.as_view(template_name='app/account_activated.html'), name='account_activated'),
    url(r'', include('django.contrib.auth.urls')),

    #for testing API response
    url(r'^api_access/$', TemplateView.as_view(template_name='app/api_access.html'), name='api_access'),
    url(r'^videos/$', app_views.videos, name ='videos'),
    url(r'^collaborators/$', app_views.collaborators, name='collaborators'),
    url(r'^sponsors/$', app_views.sponsors, name='sponsors'),
    url(r'^location/$', app_views.location, name='location'),
    url(r'calendar/$', app_views.calendar, name='calendar'),

    #things for current members
]
