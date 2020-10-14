from django.db.models.signals import post_save
from django.dispatch import receiver
import sys

# import models
from django.contrib.auth.models import User
from userextensions.models import (UserPreference, UserRecent, ServiceAccount)


@receiver(post_save, sender=User, dispatch_uid='add_user_preference')
def add_user_preference(sender, instance, created, **kwargs):
    """ This post-save signal adds a UserPreference object when a User is created """
    if created:
        UserPreference.objects.create(user=instance)


@receiver(post_save, sender=UserRecent, dispatch_uid='trim_recents')
def trim_recents(sender, instance, created, **kwargs):
    """ This post-save signal trims a users recents to only maintain the x most recent urls, where x is the
    recents_count configured in the UserPreference table """
    # do not execute signal when running tests
    if 'manage.py' in sys.argv[0] and 'test' in sys.argv:
        return

    # get recents count from user preferences if available; else default to 25
    try:
        recents_count = instance.user.preference.recents_count
    except:
        recents_count = 25

    # don't need to trim if recents count is < recents_count
    if UserRecent.objects.filter(user=instance.user).count() <= recents_count:
        return
    recent_id_list = UserRecent.objects.filter(user=instance.user
                                               ).order_by('-updated_at')[:recents_count].values_list('id', flat=True)
    UserRecent.objects.filter(user=instance.user).exclude(pk__in=list(recent_id_list)).delete()


@receiver(post_save, sender=ServiceAccount, dispatch_uid='create_srv_account_token')
def create_srv_account_token(sender, instance, created, **kwargs):
    """ This post-save signal creates a drf token when a new ServiceAccount is created """
    if created:
        instance.create_drf_token()
