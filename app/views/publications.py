from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from ..models import Publication

def publications(request):
    """Renders content for the Publications page

    Retrieves information from the Publications database using the matching Django Model structure.

    Args:
        request: the HttpRequest corresponding to the page to be accessed.

    Returns:
        A render that displays the page publications.html, complete with information from the Publications database.
    """
    publication_list = Publication.objects.reverse()
    paginator = Paginator(publication_list, 6)
    page = request.GET.get('page')

    try:
        publication_paginator = paginator.page(page)
    except PageNotAnInteger:
        publication_paginator = paginator.page(1)
    except EmptyPage:
        publication_paginator = paginator.page(paginator.num_pages)


    index = publication_paginator.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {'publication_list': publication_paginator, 'page_range':page_range}
    return render(request, 'app/publications.html', context)
