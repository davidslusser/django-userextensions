from django.utils import timezone
from django.conf import settings
from django.urls import resolve
from urllib.parse import urlparse

# Use MiddlewareMixin when present (Django >= 1.10)
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

# import models
from userextensions.models import UserRecent


class UserRecentsMiddleware(MiddlewareMixin):
    """ This middleware parses data from requests and, where applicable, stores the full url path in the request to the
    users list of recently viewed pages (recents). No recents will be stored if the user is not authenticated, user can
    not be determined, or if the URL is invalid.

    Tracking can be filtered byt methods, URL prefixes, and static URLs
    via parameters in the settings.py file. The following are configurable:

        method: tracks only specified methods; defaults to GET
                TRACK_METHOD_LIST = ['GET', ]

        URL prefixes: will not track URLs that start with the specified prefixes
                SKIP_URL_PREFIX_LIST = ['/admin/', '/__debug__/']

        static URLs: will not track the specified URLs
                SKIP_FIXED_URL_LIST = ['/', '/login/', '/logout/', ]
    """
    def process_request(self, request):
        """ read user and url (path) from request, if valid and not in a skip list, add to recents """

        # do not track ajax requests
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return

        # do not track htmx requests
        if request.headers.get("Hx-Request", None):
            return

        # only track specified methods
        track_method_list = getattr(settings, 'TRACK_METHOD_LIST', ['GET'])
        if request.method not in track_method_list:
            return

        # do not track url if user is not authenticated
        if not request.user.is_authenticated:
            return
        if not getattr(request, 'user'):
            return

        # do not track if url (full path) can not be determined
        path = getattr(request, 'get_full_path')()
        if not path:
            return

        # do not track admin or debug urls
        skip_url_prefix_list = getattr(settings, 'SKIP_URL_PREFIX_LIST', ['/admin/', '/__debug__/'])
        for prefix in skip_url_prefix_list:
            if path.startswith(prefix):
                return

        # do not track urls in the skip_fixed_url_list
        skip_fixed_url_list = getattr(settings, 'SKIP_FIXED_URL_LIST', ['/', '/login/', '/logout/',
                                                                        '/userextensions/list_recents/',
                                                                        '/userextensions/user_login_redirect/'])
        for url in skip_fixed_url_list:
            if path == url:
                return

        # do not track invalid urls
        try:
            resolve(urlparse(path).path)
        except:
            return

        # add recent
        UserRecent.objects.update_or_create(url=request.get_full_path(),
                                            user=request.user,
                                            defaults=dict(url=request.get_full_path(),
                                                          user=request.user,
                                                          updated_at=timezone.now())
                                            )
