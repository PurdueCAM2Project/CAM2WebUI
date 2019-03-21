from django.shortcuts import render
from django.apps import apps
from ..apps import AppConfig as a
from .. import models

def pure(template, **models):
    return lambda request: render(request, template, {k: v.objects.all() for (k, v) in models.items()})

index = pure('app/index.html', slide_list=models.Homepage)
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
