.. _internals:


Internals
=========

The documentation below details some of the internal workings of django-userextensions and its components. This
documentation is automatically generated from the source code. See the source code in github for full details.

https://github.com/davidslusser/django-userextensions


Middleware
----------
.. automodule:: userextensions.middleware
    :members: UserRecentsMiddleware


Signals
-------
.. automodule:: userextensions.signals
    :members: add_user_preference, trim_recents, create_srv_account_token


Models
------
.. automodule:: userextensions.models
    :members: Theme, UserPreference, UserRecent, UserFavorite, ServiceAccount


Action Views
------------
.. automodule:: userextensions.views.action
    :members: RefreshApiToken, RefreshSrvAcctApiToken, AddFavorite, DeleteFavorite, DeleteRecent, UserLoginRedirect, SetStartPage, CreateServiceAccount, DeleteServiceAccount, EnableServiceAccount, DisableServiceAccount


GUI Views
---------
.. automodule:: userextensions.views.gui
    :members: ListRecents, ListFavorites, DetailUser, ManageServiceAccounts
