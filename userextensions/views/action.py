"""
This file contains views that perform a well defined action and redirect to a rendered page, typically the referrer. No
page rendering views are contained here.
"""

from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.views.generic import View, DeleteView
from rest_framework.authtoken.models import Token
from braces.views import LoginRequiredMixin

# import models
from django.contrib.auth.models import User, Group
from userextensions.models import (UserRecent, UserFavorite, ServiceAccount)


class RefreshApiToken(LoginRequiredMixin, View):
    """ delete current user API (auth) token and create a new one """
    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            Token.objects.get_or_create(user=request.user)
        except Exception as err:
            messages.add_message(request, messages.ERROR, f'Could not complete requested action: {err}',
                                 extra_tags='alert-danger')
        return redirect(self.request.META.get('HTTP_REFERER'))


class RefreshSrvAcctApiToken(LoginRequiredMixin, View):
    """ delete current the API (auth) token for a provided service account and create a new one """
    def post(self, request):
        srv_acct_id = self.request.GET.dict().get('srv_acct_id', None)
        try:
            srv_acct = ServiceAccount.objects.get(id=srv_acct_id)
            token = Token.objects.get(user=srv_acct.user)
            token.delete()
            Token.objects.get_or_create(user=srv_acct.user)
            messages.add_message(request, messages.INFO, 'API token refreshed',
                                 extra_tags='alert-info')
        except Exception as err:
            messages.add_message(request, messages.ERROR, f'Could not complete requested action: {err}',
                                 extra_tags='alert-danger')
        return redirect(self.request.META.get('HTTP_REFERER'))


class AddFavorite(LoginRequiredMixin, View):
    """ add (the current) url to the list of user favorites """
    def post(self, request):
        referrer = self.request.META.get('HTTP_REFERER')
        name = self.request.POST.dict().get('name', None)

        # do not track url if user is not authenticated or user can not be determined
        if not request.user.is_authenticated:
            return redirect(referrer)
        user = getattr(request, 'user')
        if not user:
            return redirect(referrer)

        try:
            recent, is_new = UserFavorite.objects.get_or_create(url=referrer,
                                                                user=request.user,
                                                                defaults=dict(url=referrer,
                                                                              user=request.user,
                                                                              name=name,
                                                                              updated_at=timezone.now())
                                                                )
            if is_new:
                messages.add_message(request, messages.INFO, 'Successfully added favorite',
                                     extra_tags='alert-info')
            else:
                messages.add_message(request, messages.INFO, 'This url is already in your favorites',
                                     extra_tags='alert-info')
        except Exception as err:
            messages.add_message(request, messages.ERROR, f'Error adding favorite: {err}',
                                 extra_tags='alert-danger')
        return redirect(referrer)


class DeleteFavorite(LoginRequiredMixin, DeleteView):
    """ delete a favorite (by pk) and return to the referring page """
    def delete(self, request, *args, **kwargs):
        UserFavorite.objects.filter(**kwargs).delete()
        messages.add_message(self.request, messages.INFO, 'Favorite successfully deleted', extra_tags='alert-info')
        return redirect(self.request.META.get('HTTP_REFERER'))


class DeleteRecent(LoginRequiredMixin, DeleteView):
    """ delete a recent (by pk) and return to the referring page """
    def delete(self, request, *args, **kwargs):
        UserRecent.objects.filter(**kwargs).delete()
        messages.add_message(self.request, messages.INFO, 'Recent successfully deleted', extra_tags='alert-info')
        return redirect(self.request.META.get('HTTP_REFERER'))


class UserLoginRedirect(LoginRequiredMixin, View):
    """ Check if a user has a preferred 'start page' to load after login. If so, redirect to that page after login, else
        redirect to the project root page.
        To enable this redirect, set the LOGIN_REDIRECT_URL parameter in the settings.py to
        /userextensions/user_login_redirect and include userextensions.urls in the project level urls.py
    """
    @staticmethod
    def get(request):
        # get the users preferred start page
        try:
            start_page = request.user.preference.start_page
            if start_page:
                return redirect(start_page)
            else:
                return redirect(getattr(settings, 'LOGIN_REDIRECT_URL_DEFAULT', '/'))
        except Exception as err:
            messages.add_message(request, messages.ERROR, f'Error getting start page; redirect to root: {err}',
                                 extra_tags='alert-danger')
            return redirect("/")


class SetStartPage(LoginRequiredMixin, View):
    """ set the current page as the users preferred 'start page' to be redirected to after login """
    def post(self, request):
        referrer = self.request.META.get('HTTP_REFERER')
        try:
            # do not set start page if user is not authenticated or user can not be determined
            if not request.user.is_authenticated:
                return redirect(referrer)

            # set current url as start page
            request.user.preference.start_page = referrer
            request.user.preference.save()
            messages.add_message(request, messages.INFO, 'start page updated!', extra_tags='alert-info')
        except Exception as err:
            messages.add_message(request, messages.ERROR, f'Error setting start page: {err}',
                                 extra_tags='alert-danger')
        return redirect(referrer)


class CreateServiceAccount(LoginRequiredMixin, View):
    """ create a new service account based on a provided group """
    def post(self, request):
        referrer = self.request.META.get('HTTP_REFERER')
        try:
            group_id = self.request.GET.dict().get('group_id', None)
            description = self.request.GET.dict().get('description', None)
            group = Group.objects.get(id=group_id)

            # only create service account if user is a member of the linked group
            if request.user not in group.user_set.all():
                messages.add_message(request, messages.ERROR, 'You are not authorized to delete this service account',
                                     extra_tags='alert-danger')
                return redirect(referrer)

            srv_acct = ServiceAccount.objects.create(group=group, description=description)
            messages.add_message(request, messages.INFO, f'Service account {srv_acct.user.username} created',
                                 extra_tags='alert-info')
        except Exception as err:
            messages.add_message(request, messages.ERROR, f'Error creating service account: {err}',
                                 extra_tags='alert-danger')
        return redirect(referrer)


class DeleteServiceAccount(LoginRequiredMixin, View):
    """ delete a service account """
    def post(self, request):
        referrer = self.request.META.get('HTTP_REFERER')
        try:
            srv_acct_id = self.request.GET.dict().get('srv_acct_id', None)
            srv_acct = ServiceAccount.objects.get_object_or_none(id=srv_acct_id)
            srv_acct_name = srv_acct.user.username
            if not srv_acct:
                messages.add_message(request, messages.ERROR, 'invalid service account provided',
                                     extra_tags='alert-danger')
                return redirect(referrer)

            # only delete if user is a member of the group linked to this srv_acct
            if request.user not in srv_acct.group.user_set.all():
                messages.add_message(request, messages.ERROR, 'You are not authorized to delete this service account',
                                     extra_tags='alert-danger')
                return redirect(referrer)

            # delete the User entry; all cascaded models (including ServiceAccount) will be deleted
            srv_acct.user.delete()
            messages.add_message(request, messages.INFO, f'Service account {srv_acct_name} deleted',
                                 extra_tags='alert-info')

        except Exception as err:
            messages.add_message(request, messages.ERROR, f'Error deleting service account: {err}',
                                 extra_tags='alert-danger')
        return redirect(referrer)


class EnableServiceAccount(LoginRequiredMixin, View):
    """ enable a service account """
    def post(self, request):
        referrer = self.request.META.get('HTTP_REFERER')
        try:
            srv_acct_id = self.request.GET.dict().get('srv_acct_id', None)
            srv_acct = ServiceAccount.objects.get_object_or_none(id=srv_acct_id)
            if not srv_acct:
                messages.add_message(request, messages.ERROR, 'invalid service account provided',
                                     extra_tags='alert-danger')
                return redirect(referrer)

            # only enable if user is a member of the group linked to this srv_acct
            if request.user not in srv_acct.group.user_set.all():
                messages.add_message(request, messages.ERROR, 'You are not authorized to enable this service account',
                                     extra_tags='alert-danger')
                return redirect(referrer)

            srv_acct.enabled = True
            srv_acct.save()
            messages.add_message(request, messages.INFO, f'Service account {srv_acct.user.username} enabled',
                                 extra_tags='alert-info')

        except Exception as err:
            messages.add_message(request, messages.ERROR, f'Error enabling service account: {err}',
                                 extra_tags='alert-danger')
        return redirect(referrer)


class DisableServiceAccount(LoginRequiredMixin, View):
    """ disable a service account """
    def post(self, request):
        referrer = self.request.META.get('HTTP_REFERER')
        try:
            srv_acct_id = self.request.GET.dict().get('srv_acct_id', None)
            srv_acct = ServiceAccount.objects.get_object_or_none(id=srv_acct_id)
            if not srv_acct:
                messages.add_message(request, messages.ERROR, 'invalid service account provided',
                                     extra_tags='alert-danger')
                return redirect(referrer)

            # only enable if user is a member of the group linked to this srv_acct
            if request.user not in srv_acct.group.user_set.all():
                messages.add_message(request, messages.ERROR, 'You are not authorized to disable this service account',
                                     extra_tags='alert-danger')
                return redirect(referrer)
            srv_acct.enabled = False
            srv_acct.save()
            messages.add_message(request, messages.INFO, f'Service account {srv_acct.user.username} disabled',
                                 extra_tags='alert-info')

        except Exception as err:
            messages.add_message(request, messages.ERROR, f'Error disabling service account: {err}',
                                 extra_tags='alert-danger')
        return redirect(referrer)
