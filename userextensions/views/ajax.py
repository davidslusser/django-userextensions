"""
Views used specifically for handling AJAX Requests on Amazon objects
"""
# import system modules
import json

# import django modules
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.http import require_GET

# import models
from django.contrib.auth.models import Group
from userextensions.models import ServiceAccountTokenHistory


@require_GET
def get_users_per_group(request):
    """
    Description:
        Get all users in a group.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            obj_id = request.GET['client_response']
            obj = Group.objects.get(id=obj_id)
            template = loader.get_template('userextensions/ajax/get_users_per_group.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': obj.user_set.all()})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_srv_acct_token_history(request):
    """
    Description:
        Get the API token refresh history for a give ServiceAccount.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            obj_id = request.GET['client_response']
            queryset = ServiceAccountTokenHistory.objects.filter(srv_acct__id=obj_id).order_by('-timestamp')
            template = loader.get_template('userextensions/ajax/get_token_history_for_srv_acct.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)
