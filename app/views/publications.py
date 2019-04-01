from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from ..models import Publication

def publications(request):
    """Renders content for the Publications page

    Retrieves information from the Publications database using the matching Django Model structure.

    Args:
        request: the HttpRequest corresponding to the page to be accessed.

    Returns:
        A render that displays the page publications.html, complete with information from the Publications database.
    """

    # Test if the contents are supposed to be cards or a list
    if request.GET.get('list') == "true":
        publication_list = Publication.objects.all()
        return render(request, 'app/publications_list.html', {'publication_list': publication_list})

    # Use the current query to filter results shown to the user
    query = request.GET.get('q')
    if query:
        query = query.strip()
        publication_list = Publication.objects.filter(Q(paperinfo__contains=query) | Q(conference__contains=query) | Q(authors__contains=query))
    else:
        publication_list = Publication.objects.all()

    # Pagnate the publications
    paginator = Paginator(publication_list, 6)
    page = request.GET.get('page')

    # Get publications on the current page
    try:
        publication_paginator = paginator.page(page)
    except PageNotAnInteger:
        publication_paginator = paginator.page(1)
    except EmptyPage:
        publication_paginator = paginator.page(paginator.num_pages)

    # Create buttons at the bottom of the page that let you change pages
    index = publication_paginator.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {'publication_list': publication_paginator, 'page_range':page_range, "query":query}
    return render(request, 'app/publications.html', context)
