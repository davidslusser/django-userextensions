import re
from django.http import JsonResponse
from rest_framework import status
from .models import ServiceAccount


class ServiceAccountControlMixin:
    """ A mixin for Django Rest Framework viewsets that checks if the request is made from a ServiceAccount and only
    allows access to the endpoint if the ServiceAccount is enabled and admin_enabled. If the ServiceAccount is disabled
    by the owner or an admin, a 403 error will be received instead of the API response. This currently works for APIs
    using TokenAuthentication (rest_framework.authentication.TokenAuthentication). """
    def dispatch(self, request, *args, **kwargs):
        mo = re.search('Token (\S+)', request.META.get('HTTP_AUTHORIZATION', ''))
        if mo:
            srv_acct = ServiceAccount.objects.get_object_or_none(user__auth_token__key=mo.group(1))
            if srv_acct:
                if srv_acct.admin_enabled is False:
                    return JsonResponse(data={'detail': 'this service account has been administratively disabled'},
                                        status=status.HTTP_403_FORBIDDEN)
                elif srv_acct.enabled is False:
                    return JsonResponse(data={'detail': 'this service account has been disabled'},
                                        status=status.HTTP_403_FORBIDDEN)
        return super().dispatch(request, *args, **kwargs)


class AllowOnlyServiceAccountMixin:
    """ A mixin for Django Rest Framework viewsets that only allows responses to requests made from ServiceAccounts.
    This currently works for APIs using TokenAuthentication (rest_framework.authentication.TokenAuthentication)."""
    def dispatch(self, request, *args, **kwargs):
        mo = re.search('Token (\S+)', request.META.get('HTTP_AUTHORIZATION', ''))
        if mo:
            srv_acct = ServiceAccount.objects.get_object_or_none(user__auth_token__key=mo.group(1))
            if not srv_acct:
                return JsonResponse(data={'detail': 'access to this endpoint is only available to service accounts'},
                                    status=status.HTTP_403_FORBIDDEN)
        return super().dispatch(request, *args, **kwargs)


class AllowOnlyEnabledServiceAccountMixin:
    """ A mixin for Django Rest Framework viewsets that checks if the request is made from a ServiceAccount and only
    allows access to the endpoint if an enabled ServiceAccount made the request. If the ServiceAccount is disabled
    by the owner or an admin, a 403 error will be received instead of the API response. This currently works for APIs
    using TokenAuthentication (rest_framework.authentication.TokenAuthentication). """
    def dispatch(self, request, *args, **kwargs):
        mo = re.search('Token (\S+)', request.META.get('HTTP_AUTHORIZATION', ''))
        if mo:
            srv_acct = ServiceAccount.objects.get_object_or_none(user__auth_token__key=mo.group(1))
            if srv_acct:
                if srv_acct.admin_enabled is False:
                    return JsonResponse(data={'detail': 'this service account has been administratively disabled'},
                                        status=status.HTTP_403_FORBIDDEN)
                elif srv_acct.enabled is False:
                    return JsonResponse(data={'detail': 'this service account has been disabled'},
                                        status=status.HTTP_403_FORBIDDEN)
            else:
                return JsonResponse(data={'detail': 'access to this endpoint is only available to enabled '
                                                    'service accounts'}, status=status.HTTP_403_FORBIDDEN)
        return super().dispatch(request, *args, **kwargs)
