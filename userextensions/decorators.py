
from .models import ServiceAccount


def enforce_srv_account_enabled(func):
    """
    Decorator used on an API intended to enforce service account enabled status. If use attempting action is NOT a
    service account, proceed normally.
    If the service account has enabled = False OR admin_enabled = False, attempted action will blocked. Otherwise,
    proceed normally.
    """
    pass
