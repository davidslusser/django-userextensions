"""

"""
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db import models
from django.core.exceptions import ValidationError

from handyhelpers.managers import HandyHelperModelManager
from rest_framework.authtoken.models import Token


class UserExtensionBaseModel(models.Model):
    """ base model for UserExtension tables """
    objects = HandyHelperModelManager()
    created_at = models.DateTimeField(auto_now_add=True, help_text='date/time when this row was first created')
    updated_at = models.DateTimeField(auto_now=True, help_text='date/time this row was last updated')

    class Meta:
        abstract = True


class Theme(UserExtensionBaseModel):
    """ This model tracks themes. It can be used to provide user preferred frontend styling options based on
    defined css files. """
    name = models.CharField(max_length=32, unique=True, help_text='name of theme')
    css_file = models.CharField(max_length=255, unique=True, blank=True, null=True,
                                help_text='path to css file for theme')

    def __str__(self):
        return self.name


class UserPreference(UserExtensionBaseModel):
    """ This table tracks user preferences. Fields include theme, recents_count, page_refresh_time, and start_page. """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preference')
    theme = models.ForeignKey(Theme, blank=True, null=True, help_text='theme to use for web pages',
                              on_delete=models.CASCADE)
    recents_count = models.IntegerField(default=25, blank=True, null=True,
                                        help_text='number of recents to keep a record of')
    page_refresh_time = models.IntegerField(default=5, blank=True, null=True,
                                            help_text='time, in minutes, to auto-refresh a page (where applicable')
    start_page = models.CharField(max_length=255, blank=True, null=True, help_text='url to redirect to after login')

    def __str__(self):
        return self.user.username


class UserRecent(UserExtensionBaseModel):
    """ This table stored recently visited urls. """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recent')
    url = models.URLField(help_text='url endpoint')

    class Meta:
        unique_together = (('url', 'user'), )

    def __str__(self):
        return self.url


class UserFavorite(UserExtensionBaseModel):
    """ This table stores user-defined favorites. """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite')
    name = models.CharField(max_length=32, blank=True, null=True, help_text='name/label/reference for this favorite')
    url = models.URLField(help_text='url endpoint')

    class Meta:
        unique_together = (('url', 'user'), )

    def __str__(self):
        return self.url


class ServiceAccount(UserExtensionBaseModel):
    """ This table stores service accounts and maps to a (service account) user and group """
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True, help_text='enable/disable state of user')
    description = models.CharField(max_length=254, blank=True, null=True, help_text='optional description')

    class Meta:
        unique_together = (('user', 'group'), )

    def __str__(self):
        return self.user.username

    def clean(self):
        """ clean/update/validate data before saving """
        if not self.user:
            # Create name based on prefix + group + suffix; prefix and/or suffix is required. The prefix & suffix values
            # are provided by django settings variables. If neither is set, a default suffix ('_srv') will be used.
            prefix = getattr(settings, 'SRV_ACCOUNT_PREFIX', '')
            suffix = getattr(settings, 'SRV_ACCOUNT_SUFFIX', '')
            if not prefix and not suffix:
                suffix = '_srv'
            username = prefix + self.group.name + suffix
        else:
            username = self.user.username

        # before creating the service account, we need to get_or_create the user
        self.user = User.objects.get_or_create(username=username)[0]
        # add now add the new user to the matching group
        self.user.groups.add(self.group)

        # check if multiple service accounts per group are allowed. This is set in the django settings file with
        # the ALLOW_MULTIPLE_SRV_ACCOUNTS variable. By default, only one service account per group is allowed. To
        # enabled multiple service accounts per group, set SRV_ALLOW_MULTIPLE_ACCOUNTS=True
        if not self.pk:
            allow_multiple = getattr(settings, 'ALLOW_MULTIPLE_SRV_ACCOUNTS', False)
            existing = ServiceAccount.objects.filter(group=self.group)
            if existing and allow_multiple is False:
                raise ValidationError({'group': 'Multiple service accounts per group is currently not allowed. To '
                                                'enable multiple accounts per group, set '
                                                'ALLOW_MULTIPLE_SRV_ACCOUNTS=True in the django settings. '})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def create_drf_token(self):
        """ create a drf token for this service account """
        Token.objects.get_or_create(user=self.user)
