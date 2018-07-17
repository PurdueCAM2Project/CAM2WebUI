"""
A custom middleware for basic authentication.
Used to protect the staging server.
"""
import base64

from django.http import HttpResponse
from django.conf import settings


class BasicAuthMiddleware(object):  # pylint: disable=too-few-public-methods
    """Callable middleware class for basic authentication"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            (method, auth) = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            assert method.lower() == 'basic'
            auth = base64.b64decode(auth.strip()).decode('utf-8')
            username, password = auth.split(':', 1)
            assert username == settings.BASICAUTH_USERNAME
            assert password == settings.BASICAUTH_PASSWORD
        except (KeyError, AssertionError):
            response = HttpResponse('Unauthorized', status=401)
            response['WWW-Authenticate'] = 'Basic'
        else:
            response = self.get_response(request)

        return response
