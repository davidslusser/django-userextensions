"""
Views used specifically for handling AJAX Requests
"""
# import django modules
from django.template import loader
from handyhelpers.views.ajax import AjaxGetView

# import models
from django.contrib.auth.models import Group
from userextensions.models import ServiceAccountTokenHistory


class GetUsersPerGroup(AjaxGetView):
    """
    Description:
        Get all users in a group.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    template = loader.get_template('userextensions/ajax/get_users_per_group.htm')
    
    def get(self, request, *args, **kwargs):
        obj_id = request.GET['client_response']
        self.data = Group.objects.get(id=obj_id).user_set.all().order_by('username')
        return super().get(request, *args, **kwargs)


class GetSerivceAccountTokenHistory(AjaxGetView):
    """
    Description:
        Get the API token refresh history for a give ServiceAccount.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    template = loader.get_template('userextensions/ajax/get_token_history_for_srv_acct.htm')
    
    def get(self, request, *args, **kwargs):
        obj_id = request.GET['client_response']
        self.data = ServiceAccountTokenHistory.objects.filter(srv_acct__id=obj_id).order_by('-timestamp')
        return super().get(request, *args, **kwargs)


class GetSerivceAccountToken(AjaxGetView):
    """
    Description:
        Show the API token for a service account.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    template = loader.get_template('userextensions/ajax/show_srv_acct_token.htm')
    
    def get(self, request, *args, **kwargs):
        self.data = request.GET['client_response']
        return super().get(request, *args, **kwargs)
