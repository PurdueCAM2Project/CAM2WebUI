from django.conf.urls import url, include
from . import views as app_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', app_views.index, name="index"),
    url(r'^cameras/$', app_views.cameras, name='cameras'),
    url(r'^good_cameras/$', app_views.good_cameras, name='good_cameras'),
    url(r'^team/$', app_views.team, name='team'),
    url(r'^team_poster/$', app_views.team_poster, name='team_poster'),
    url(r'^advice/$', app_views.advice, name='advice'),
    url(r'^history/$', app_views.history, name='history'),
    url(r'^publications/$', app_views.publications, name='publications'),
    url(r'^privacy/$', app_views.privacy, name='privacy'),
    url(r'^ack/$', app_views.acknowledgement, name='acknowledgement'),
    url(r'^faqs/$', app_views.faqs, name='faqs'),
    url(r'^terms/$', app_views.terms, name='terms'),
    url(r'^profile/$', app_views.profile, name='profile'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
	url(r'^register/$', app_views.register, name='register'),
    url(r'^oauthinfo/$', app_views.oauthinfo, name='more info'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page='/')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),#don't add $ after oauth/
    url(r'^email_confirmation_sent/$', app_views.email_confirmation_sent, name='email_confirmation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        app_views.activate, name='activate'),
    url(r'^email_confirmation_invalid/$', app_views.email_confirmation_invalid, name='email_confirmation_invalid'),
    url(r'^account_activated/$', app_views.account_activated, name='account_activated'),

    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset_email_sent/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^password_reset/complete/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^new_map/$', app_views.new_map, name='new_map'),
    url(r'^good_map/$', app_views.good_map, name='good_map'),

    #for testing API response
    url(r'^api_access/$', app_views.api_request, name='api_access'),
    url(r'^videos/$', app_views.videos, name ='videos'),
    url(r'^collaborators/$', app_views.collaborators, name='collaborators'),
    url(r'^sponsors/$', app_views.sponsors, name='sponsors'),
    url(r'^location/$', app_views.location, name='location'),
    url(r'calendar/$', app_views.calendar, name='calendar'),
    url(r'publications_list/$', app_views.publications_list, name='publications_list'),

]
