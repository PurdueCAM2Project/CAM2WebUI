from django.conf.urls import url, include
from . import views as app_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', app_views.index, name="index"),
    url(r'^cameras/$', app_views.cameras, name='cameras'),
    url(r'^team/$', app_views.team, name='team'),
    url(r'^history/$', app_views.history, name='history'),
    url(r'^publications/$', app_views.publications, name='publications'),
    url(r'^api_resources/README$', app_views.api_resources_readme, name='README'),
    url(r'^api_resources/documentation$', app_views.api_resources_documentation, name='Documentation'),
    url(r'^api_resources/console$', app_views.api_resources_console, name='API console'),           
    url(r'^privacy/$', app_views.privacy, name='privacy'),
    url(r'^ack/$', app_views.acknowledgement, name='acknowledgement'),
    #url(r'^contact/$', app_views.contact, name='contact'),
    url(r'^faqs/$', app_views.faqs, name='faqs'),
    url(r'^terms/$', app_views.terms, name='terms'),
    url(r'^profile/$', app_views.profile, name='profile'),
    url(r'^login/$', auth_views.login, {'template_name': 'app/login.html'}, name='login'),
	url(r'^register/$', app_views.register, name='register'),
    url(r'^oauthinfo/$', app_views.oauthinfo, name='more info'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}),
    url(r'^oauth/', include('social_django.urls', namespace='social')),#don't add $ after oauth/
    url(r'^email_confirmation_sent/$', app_views.email_confirmation_sent, name='email_confirmation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        app_views.activate, name='activate'),
    url(r'^email_confirmation_invalid/$', app_views.email_confirmation_invalid, name='email_confirmation_invalid'),
    url(r'^account_activated/$', app_views.account_activated, name='account_activated'),

]
