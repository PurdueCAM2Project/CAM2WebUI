from django.shortcuts import render
from ..models import *

def index(request):
    slide = Homepage.objects.reverse()
    context = {'slide_list': slide}
    return render(request, 'app/index.html', context)

def good_cameras(request):
    return render(request, 'app/good_cameras.html')

def team_poster(request):
    poster_images = Poster.objects.reverse()
    context = {"poster_images": poster_images}
    return render(request, 'app/team_poster.html', context)

def training(request):
    return render(request, 'app/training.html')

def privacy(request):
    return render(request, 'app/privacy.html')

def terms(request):
    return render(request, 'app/terms.html')

def acknowledgement(request):
    return render(request, 'app/ack.html')

def collaborators(request):
    collab = Collab.objects.reverse()
    context = {'collab_list': collab}
    return render(request, 'app/collaborators.html', context)

def sponsors(request):
    sponsor = Sponsor.objects.reverse()
    context = {'sponsor_list': sponsor}
    return render(request, 'app/sponsors.html', context)

def calendar(request):
    cal = Calendar.objects.reverse()
    context = {'calendar_list': cal}
    return render(request, 'app/calendar.html', context)

def location(request):
    loc = Location.objects.reverse()
    context = {'loc_list': loc}
    return render(request, 'app/location.html', context)

def faqs(request):
    """Renders content for the FAQs page

    Retrieves information from the FAQ database using the matching Django Model structure.

    Args:
        request: the HttpRequest corresponding to the page to be accessed.

    Returns:
        A render that displays the page faq.html, complete with information from the FAQs database.
    """
    question_list = FAQ.objects.reverse()
    context = {'question_list': question_list}
    return render(request, 'app/faq.html', context)

def history(request):
    """Renders content for the History page

    Retrieves information from the History database using the matching Django Model structure.

    Args:
        request: the HttpRequest corresponding to the page to be accessed.

    Returns:
        A render that displays the page history.html, complete with information from the History database.
    """
    history_list = History.objects.order_by('-year', '-month')
    context = {'history_list': history_list}
    return render(request, 'app/history.html', context)

def advice(request):
    return render(request, 'app/advice.html')

def email_confirmation_sent(request):
    return render(request, 'app/email_confirmation_sent.html')

def email_confirmation_invalid(request):
    return render(request, 'app/email_confirmation_invalid.html')

def account_activated(request):
    return render(request, 'app/account_activated.html')

def error500(request):
    return render(request, 'app/500.html')

def error404(request, exception, template_name='app/404.html'):
    return render(request, 'app/404.html')

def api_request(request):
    template_name = 'app/api_access.html'
    return render(request, template_name)

def videos(request):
    video = Video.objects.all()
    context = {'videos_list': video}
    return render(request, 'app/videos.html', context)

def publications_list(request):
    publication_list = Publication.objects.reverse()
    context = {'publication_list': publication_list}
    return render(request, 'app/publications_list.html', context)
