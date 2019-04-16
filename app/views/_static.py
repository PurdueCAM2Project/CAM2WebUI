from django.shortcuts import render
from django.apps import apps
import requests
from ..apps import AppConfig as a
from .. import models

def pure(template, **models):
    """ Helper method for automatically generating static template views in one line.
    This reduces boilerplate code for the programmer by allowing them to easily read
    what models are used on each page.
    
    These two pieces of code are equivalent:
    team_poster = pure('app/team_poster.html', poster_images=models.Poster)

    def team_poster(request):
        poster_images = models.Poster.objects.all()
        context = {'poster_images': poster_images}
        return render(request, 'app/team_poster.html', context)

    In both of these cases, the template located at 'app/team_poster.html' is
    rendered with the context variable 'poster_images' set to all of the 'Poster' model.
    """
    return lambda request: render(request, template, {k: v.objects.all() for (k, v) in models.items()})

def index(request):
    """ Renders the homepage of the website.
    This page requires additional information from the Purdue HELPS website in order
    to run properly, particularly the news. Otherwise, this is a pretty normal static
    page.
    """
    try:
        news = requests.get('http://www.purduehelps.org/assets/json/news.json').json()
    except:
        news = None
    return render(request, 'app/index.html', {'slide_list': models.Homepage.objects.all(), 'news': news})

team_poster = pure('app/team_poster.html', poster_images=models.Poster)
collaborators = pure('app/collaborators.html', collab_list=models.Collab)
sponsors = pure('app/sponsors.html', sponsor_list=models.Sponsor)
calendar = pure('app/calendar.html', calendar_list=models.Calendar)
location = pure('app/location.html', loc_list=models.Location)
faqs = pure('app/faq.html', question_list=models.FAQ)
history = pure('app/history.html', history_list=models.History)
videos = pure('app/videos.html', videos_list=models.Video)

error404 = pure('app/404.html')
error500 = pure('app/500.html')
